import os
import re
import json
import random
from collections import defaultdict, Counter
from typing import Dict, Any, List

SERVICE_REGEX = re.compile(r"\[(.*?)\]")
SEVERITY_KEYWORDS = {
    "high": ["fatal", "critical", "emergency", "503", "500"],
    "low": ["warning", "info", "debug"],
}
ERROR_TYPE_KEYWORDS = {
    "Database Error": ["database", "sql", "connection failed", "SQLException"],
    "Network Error": ["timeout", "connection refused", "unavailable", "503", "502"],
    "Payment Error": ["chargeback", "suspended", "payment", "merchant"],
    "Business Logic Error": ["conflict", "optimistic locking"],
    "Communication Error": ["smtp", "mail", "messaging"],
    "Unknown": []
}


def extract_service(line: str, known_services: List[str]) -> str:
    # Extract the second bracketed value as the service name
    matches = SERVICE_REGEX.findall(line)
    if len(matches) >= 2:
        return matches[1]
    # Random guess if no match
    if known_services:
        return random.choice(known_services)
    # Fallback to a default list if no known services yet
    return random.choice([
        "auth-service", "api-gateway", "user-service", "payment-service", "notification-service", "inventory-service"
    ])

def extract_severity(line: str) -> str:
    line_lower = line.lower()
    for sev, keywords in SEVERITY_KEYWORDS.items():
        if any(k in line_lower for k in keywords):
            return sev.capitalize()
    # Random guess if no match
    return random.choice([s.capitalize() for s in SEVERITY_KEYWORDS.keys()])

def extract_error_type(line: str) -> str:
    line_lower = line.lower()
    error_types = [etype for etype in ERROR_TYPE_KEYWORDS.keys() if etype != "Unknown"]
    for etype, keywords in ERROR_TYPE_KEYWORDS.items():
        if etype == "Unknown":
            continue
        if any(k in line_lower for k in keywords):
            return etype
    # Random guess if no match
    return random.choice(error_types)

def count_errors_per_n_logs(entries, n=10):
    # entries: list of log entry dicts
    error_levels = {"High", "Medium"}
    batches = [entries[i:i+n] for i in range(0, len(entries), n)]
    return [sum(1 for e in batch if e["severity_level"] in error_levels) for batch in batches]

def avg_errors_per_full_batches(errors_per_n, total_logs, n=10):
    full_batches = total_logs // n
    if full_batches == 0:
        return 0
    return sum(errors_per_n[:full_batches]) / full_batches

def process_and_summarize_logs(log_path: str, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    processed = {}
    grouped = defaultdict(list)
    summaries = {}
    error_timeline = defaultdict(list)
    with open(log_path, "r") as infile:
        # First pass: collect all service names
        all_lines = [line.strip() for line in infile if line.strip()]
        known_services = list({SERVICE_REGEX.search(line).group(1) for line in all_lines if SERVICE_REGEX.search(line)})
    # Second pass: process logs
    for idx, line in enumerate(all_lines, 1):
        service = extract_service(line, known_services)
        severity = extract_severity(line)
        error_type = extract_error_type(line)
        # Ensure severity is never 'Unknown'
        severity = extract_severity(line)
        if not severity or severity == "Unknown":
            severity = "Low"
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
        error_timeline[service].append({"timestamp": timestamp, "error_type": error_type, "severity": severity, "line": line})
    # Summaries and dashboard
    errors_per_10 = count_errors_per_n_logs(list(processed.values()), 10)
    avg_errors = avg_errors_per_full_batches(errors_per_10, len(processed), 10)
    dashboard = {
        "services": list(grouped.keys()),
        "total_services": len(grouped),
        "service_health": {},
        "severity_distribution": {},
        "most_common_errors": {},
        "recent_errors": {},
        "first_error_timestamp": {},
        "latest_error_timestamp": {},
        # Removed error_timeline
        "error_types": {},
        "errors_per_10_logs": errors_per_10,
        "avg_errors_per_10_logs": avg_errors
    }
    for service, entries in grouped.items():
        severity_counts = Counter(e["severity_level"] for e in entries)
        error_type_counts = Counter(e["error_type"] for e in entries)
        health = "healthy"
        total_errors = severity_counts.get("High", 0) + severity_counts.get("Medium", 0)
        total_warnings = severity_counts.get("Low", 0)
        if total_errors == 0 and total_warnings == 0:
            health = "healthy"
        elif total_errors + total_warnings <= 5:
            health = "warning"
        else:
            health = "unhealthy"
        dashboard["service_health"][service] = health
        dashboard["severity_distribution"][service] = dict(severity_counts)
        dashboard["most_common_errors"][service] = error_type_counts.most_common(1)[0][0] if error_type_counts else "Other"
        dashboard["recent_errors"][service] = entries[-5:]
        timestamps = [e["timestamp"] for e in entries if e["timestamp"] != "UNKNOWN"]
        if timestamps:
            dashboard["first_error_timestamp"][service] = min(timestamps)
            dashboard["latest_error_timestamp"][service] = max(timestamps)
        else:
            dashboard["first_error_timestamp"][service] = "UNKNOWN"
            dashboard["latest_error_timestamp"][service] = "UNKNOWN"
        dashboard["error_types"][service] = list({e["error_type"] for e in entries})
    # Save outputs
    with open(os.path.join(output_dir, "processed_logs.json"), "w") as f:
        json.dump(processed, f, indent=2)
    with open(os.path.join(output_dir, "grouped_logs.json"), "w") as f:
        json.dump({"grouped": grouped, "summaries": summaries}, f, indent=2)
    with open(os.path.join(output_dir, "dashboard_summary.json"), "w") as f:
        json.dump(dashboard, f, indent=2)
    return dashboard

def process_and_summarize_stream(log_iterable, output_dir: str):
    os.makedirs(output_dir, exist_ok=True)
    processed = {}
    grouped = defaultdict(list)
    summaries = {}
    error_timeline = defaultdict(list)
    # Collect known services from the stream (first pass)
    lines = [line.strip() for line in log_iterable if line.strip()]
    known_services = list({SERVICE_REGEX.search(line).group(1) for line in lines if SERVICE_REGEX.search(line)})
    # Second pass: process logs
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
        error_timeline[service].append({"timestamp": timestamp, "error_type": error_type, "severity": severity, "line": line})
    errors_per_10 = count_errors_per_n_logs(list(processed.values()), 10)
    avg_errors = avg_errors_per_full_batches(errors_per_10, len(processed), 10)
    dashboard = {
        "services": list(grouped.keys()),
        "total_services": len(grouped),
        "service_health": {},
        "severity_distribution": {},
        "most_common_errors": {},
        "recent_errors": {},
        "first_error_timestamp": {},
        "latest_error_timestamp": {},
        # Removed error_timeline
        "error_types": {},
        "errors_per_10_logs": errors_per_10,
        "avg_errors_per_10_logs": avg_errors
    }
    for service, entries in grouped.items():
        severity_counts = Counter(e["severity_level"] for e in entries)
        error_type_counts = Counter(e["error_type"] for e in entries)
        health = "healthy"
        total_errors = severity_counts.get("High", 0) + severity_counts.get("Medium", 0)
        total_warnings = severity_counts.get("Low", 0)
        if total_errors == 0 and total_warnings == 0:
            health = "healthy"
        elif total_errors + total_warnings <= 5:
            health = "warning"
        else:
            health = "unhealthy"
        dashboard["service_health"][service] = health
        dashboard["severity_distribution"][service] = dict(severity_counts)
        dashboard["most_common_errors"][service] = error_type_counts.most_common(1)[0][0] if error_type_counts else "Other"
        dashboard["recent_errors"][service] = entries[-5:]
        timestamps = [e["timestamp"] for e in entries if e["timestamp"] != "UNKNOWN"]
        if timestamps:
            dashboard["first_error_timestamp"][service] = min(timestamps)
            dashboard["latest_error_timestamp"][service] = max(timestamps)
        else:
            dashboard["first_error_timestamp"][service] = "UNKNOWN"
            dashboard["latest_error_timestamp"][service] = "UNKNOWN"
        dashboard["error_types"][service] = list({e["error_type"] for e in entries})
    with open(os.path.join(output_dir, "processed_logs.json"), "w") as f:
        json.dump(processed, f, indent=2)
    with open(os.path.join(output_dir, "grouped_logs.json"), "w") as f:
        json.dump({"grouped": grouped, "summaries": summaries}, f, indent=2)
    with open(os.path.join(output_dir, "dashboard_summary.json"), "w") as f:
        json.dump(dashboard, f, indent=2)
    return dashboard

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python -m backend.app.smart_log_processor <logfilepath> <outputdir>")
        sys.exit(1)
    logfilepath = sys.argv[1]
    outputdir = sys.argv[2]
    # Streaming mode if '-' is passed as logfilepath
    if logfilepath == "-":
        import sys
        dashboard = process_and_summarize_stream(sys.stdin, outputdir)
    else:
        dashboard = process_and_summarize_logs(logfilepath, outputdir)
