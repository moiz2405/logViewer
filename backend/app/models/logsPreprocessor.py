import re
import json

# Common anomaly patterns
ANOMALY_KEYWORDS = [
    "exception", "failed", "error", "refused", "timeout", "unavailable", "denied",
    "panic", "stacktrace", "crash", "fatal", "killed"
]

def is_anomalous(log_line: str) -> bool:
    log_level_match = re.search(r"\b(INFO|DEBUG|TRACE)\b", log_line, re.IGNORECASE)
    if log_level_match:
        return False  # Skip non-error logs
    for keyword in ANOMALY_KEYWORDS:
        if keyword in log_line.lower():
            return True
    return False

def extract_compact_error(log_line: str) -> str:
    # Try to extract the service and a summary
    match = re.search(r"\[(.*?)\].*?(Exception|Failed|Error|Refused|Timeout|Killed|Unavailable|Crash|Panic)", log_line, re.IGNORECASE)
    if match:
        service = match.group(1)
        issue = re.search(r"(Exception.*|Failed.*|Error.*|Refused.*|Timeout.*|Killed.*|Unavailable.*|Crash.*|Panic.*)", log_line, re.IGNORECASE)
        if issue:
            return f"{issue.group(0).strip()} in {service}"
    return f"Anomaly detected: {log_line.replace('\t', ' ').strip()}"

def process_logs(input_path: str, output_path: str) -> dict:
    """
    Processes logs from input_path, extracts anomalies without duplicates,
    and writes them to output_path. Also returns the extracted anomalies as a dictionary.
    """
    result = {}
    seen_anomalies = set()
    count = 1

    with open(input_path, "r") as infile:
        for line in infile:
            if is_anomalous(line):
                compact_error = extract_compact_error(line)
                if compact_error not in seen_anomalies:
                    seen_anomalies.add(compact_error)
                    result[str(count)] = compact_error
                    count += 1

    with open(output_path, "w") as outfile:
        json.dump(result, outfile, indent=2)

    print(f"Extracted {count - 1} unique anomalies to {output_path}")
    return result

if __name__ == "__main__":
    input_file = "backend/app/logs/exLogs.log"
    output_file = "backend/app/outputs/compact_anomalies.json"
    process_logs(input_file, output_file)
