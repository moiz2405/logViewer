import os
import re
import json
import random
from collections import defaultdict, Counter
from typing import List

# =====================================================================
# Regex patterns & keyword sets
# =====================================================================
SERVICE_REGEX = re.compile(r"\[(.*?)\]")

ERROR_TYPE_KEYWORDS = {
    "Database Error": ["database", "sql", "connection failed", "SQLException"],
    "Network Error": ["timeout", "connection refused", "unavailable", "503", "502"],
    "Payment Error": ["chargeback", "suspended", "payment", "merchant"],
    "Business Logic Error": ["conflict", "optimistic locking"],
    "Communication Error": ["smtp", "mail", "messaging"],
    "Unknown": []
}

# =====================================================================
# Utility Functions
# =====================================================================

def extract_service(line: str, known_services: List[str]) -> str:
    """Extracts the second bracketed value as the service name, if available."""
    matches = SERVICE_REGEX.findall(line)
    if len(matches) >= 2:
        return matches[1]
    if known_services:
        return random.choice(known_services)
    return random.choice([
        "auth-service", "api-gateway", "user-service",
        "payment-service", "notification-service", "inventory-service"
    ])

def extract_severity(line: str) -> str:
    """Classify log severity using contextual keyword detection."""
    line_lower = line.lower()

    # Ignore successful or neutral messages
    if any(word in line_lower for word in ["success", "connected successfully", "completed", "started", "running"]):
        return "Low"

    # High-severity indicators
    if any(word in line_lower for word in [
        "fatal", "critical", "emergency", "crash", "panic",
        "exception", "error 5", "failed", "503", "500", "unavailable"
    ]):
        return "High"

    # Medium-severity indicators
    if any(word in line_lower for word in ["warn", "retry", "timeout", "delay", "degraded", "slow"]):
        return "Medium"

    # Low-severity or neutral logs
    if any(word in line_lower for word in ["info", "debug", "connected", "success", "started", "completed"]):
        return "Low"

    return "Low"

def extract_error_type(line: str) -> str:
    """Detects the general error type based on known keywords."""
    line_lower = line.lower()

    # Avoid classifying successful messages
    if any(word in line_lower for word in ["success", "completed", "connected", "running"]):
        return "None"

    for etype, keywords in ERROR_TYPE_KEYWORDS.items():
        if etype == "Unknown":
            continue
        if any(k in line_lower for k in keywords):
            return etype
    return "Unknown"

def count_errors_per_n_logs(entries, n=10):
    """Compute weighted error count over rolling batches."""
    severity_weights = {"High": 1.0, "Medium": 0.3, "Low": 0.0}
    batches = [entries[i:i+n] for i in range(0, len(entries), n)]
    return [sum(severity_weights.get(e["severity_level"], 0) for e in batch) for batch in batches]

def avg_errors_per_full_batches(errors_per_n, total_logs, n=10):
    """Compute average errors across full batches."""
    full_batches = total_logs // n
    if full_batches == 0:
        return 0
    return sum(errors_per_n[:full_batches]) / full_batches

def determine_service_health(entries):
    """Evaluates health based on severity ratios."""
    severity_counts = Counter(e["severity_level"] for e in entries)
    total_logs = len(entries)
    if total_logs == 0:
        return "healthy"

    high_ratio = severity_counts["High"] / total_logs
    medium_ratio = severity_counts["Medium"] / total_logs

    if high_ratio > 0.05:        # more than 5% high severity logs
        return "unhealthy"
    elif medium_ratio > 0.1:     # more than 10% medium severity logs
        return "warning"
    else:
        return "healthy"

# =====================================================================
# Core Function: Stream Processing
# =====================================================================

def process_and_summarize_stream(log_iterable, output_dir: str):
    """
    Processes logs from a stream (like stdin) and generates summaries + dashboard.
    """
    os.makedirs(output_dir, exist_ok=True)

    processed = {}
    grouped = defaultdict(list)
    summaries = {}
    error_timeline = defaultdict(list)

    # First pass: identify all known services
    lines = [line.strip() for line in log_iterable if line.strip()]
    known_services = list({SERVICE_REGEX.search(line).group(1)
                           for line in lines if SERVICE_REGEX.search(line)})

    # Process each line
    for idx, line in enumerate(lines, 1):
        service = extract_service(line, known_services)
        severity = extract_severity(line)
        error_type = extract_error_type(line)

        timestamp_match = re.search(r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:,\d+)?", line)
        timestamp = timestamp_match.group(0) if timestamp_match else "UNKNOWN"

        entry = {
            "timestamp": timestamp,
            "service": service,
            "error_type": error_type,
            "severity_level": severity,
            "line": line,
            "line_number": idx
        }

        processed[str(idx)] = entry
        grouped[service].append(entry)
        error_timeline[service].append({
            "timestamp": timestamp,
            "error_type": error_type,
            "severity": severity,
            "line": line
        })

    # Summaries
    errors_per_10 = count_errors_per_n_logs(list(processed.values()), 10)
    avg_errors = avg_errors_per_full_batches(errors_per_10, len(processed), 10)

    # Dashboard Summary
    dashboard = {
        "services": list(grouped.keys()),
        "total_services": len(grouped),
        "service_health": {},
        "severity_distribution": {},
        "most_common_errors": {},
        "recent_errors": {},
        "first_error_timestamp": {},
        "latest_error_timestamp": {},
        "error_types": {},
        "errors_per_10_logs": errors_per_10,
        "avg_errors_per_10_logs": avg_errors
    }

    for service, entries in grouped.items():
        severity_counts = Counter(e["severity_level"] for e in entries)
        error_type_counts = Counter(e["error_type"] for e in entries)

        health = determine_service_health(entries)

        dashboard["service_health"][service] = health
        dashboard["severity_distribution"][service] = dict(severity_counts)
        dashboard["most_common_errors"][service] = (
            error_type_counts.most_common(1)[0][0] if error_type_counts else "Other"
        )
        dashboard["recent_errors"][service] = entries[-5:]

        timestamps = [e["timestamp"] for e in entries if e["timestamp"] != "UNKNOWN"]
        dashboard["first_error_timestamp"][service] = min(timestamps) if timestamps else "UNKNOWN"
        dashboard["latest_error_timestamp"][service] = max(timestamps) if timestamps else "UNKNOWN"
        dashboard["error_types"][service] = list({e["error_type"] for e in entries})

    # Save outputs
    with open(os.path.join(output_dir, "processed_logs.json"), "w") as f:
        json.dump(processed, f, indent=2)
    with open(os.path.join(output_dir, "grouped_logs.json"), "w") as f:
        json.dump({"grouped": grouped, "summaries": summaries}, f, indent=2)
    with open(os.path.join(output_dir, "dashboard_summary.json"), "w") as f:
        json.dump(dashboard, f, indent=2)

    return dashboard

# =====================================================================
# CLI Entry Point
# =====================================================================

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python -m backend.app.smart_log_processor <outputdir>")
        sys.exit(1)
    outputdir = sys.argv[1]
    dashboard = process_and_summarize_stream(sys.stdin, outputdir)
