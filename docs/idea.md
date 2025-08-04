
## **Project Title:** LogViewer – Intelligent Log Analysis & Classification System

---

### **Core Idea:**

A backend tool that:

* Ingests system/service logs (e.g., Docker logs).
* **Preprocesses logs** to filter out noise and irrelevant entries.
* **Classifies anomalies** (like errors, failures, and warnings) by type, subtype, severity, and affected service.
* Outputs a **compact JSON summary** of critical issues for further analysis or visualization.

---

### **Objectives:**

1. Parse and clean large log files (from Docker containers, etc.).
2. Detect and extract meaningful error/anomaly lines.
3. Categorize each anomaly by:

   * Service (e.g., auth-service, payment-service)
   * Error Type (e.g., Database Error, Network Error)
   * Error Subtype (e.g., Timeout, Connection Refused)
   * Severity (High, Medium, Low)
4. Save structured summaries to a file for further consumption.

---

### **Tech Stack:**

#### ➤ **Language & Runtime**

* Python 3.11+

#### ➤ **Folder Structure**

```
backend/
├── app/
│   ├── models/
│   │   ├── logsPreprocessor.py      # Cleans and filters log lines
│   │   ├── logsClassifier.py        # Classifies logs into structured format
│   ├── outputs/
│   │   ├── processed_logs.json      # Intermediate preprocessed logs
│   │   ├── classified_logs.json     # Final structured classification
│   ├── logs/
│   │   ├── dockerLogs.log           # Raw input log file
│   ├── types/
│   │   └── classifierTypes.py       # Enums for Service, ErrorType, Subtype, Severity
│   └── path.py                      # Entrypoint for preprocessing + classification
```

#### ➤ **Key Python Modules**

* `re` (regex) – for parsing logs
* `json` – for input/output file handling
* `enum` – for structured categorization
* `os` – for file path handling

---

### 🔍 **Classification Logic:**

Uses predefined enums in `classifierTypes.py`:

* `Service`: e.g., `auth-service`, `inventory-service`
* `ErrorType`: e.g., `Database Error`, `Security Alert`
* `ErrorSubtype`: e.g., `Timeout`, `Connection Refused`
* `SeverityLevel`: `High`, `Medium`, `Low`

---

### **Sample Output Format:**

```json
{
  "1": "Database connection failed in payment-service",
  "2": "Out of memory error in inventory-service",
  "3": "Authentication failure in auth-service"
}
```

---

### **Flow Overview:**

1. 🔁 `logsPreprocessor.py`:

   * Input: Raw log file
   * Output: `processed_logs.json` (cleaned, numbered lines)

2. 🎯 `logsClassifier.py`:

   * Input: Cleaned log file
   * Process: Classify based on error keywords, severity, and services
   * Output: `classified_logs.json`

3. ▶️ `path.py`:

   * Combines both stages (preprocess + classify) with file path management

---

### **Future Ideas:**

* Add timestamp-based filtering
* Export CSV or visualization-ready formats
* REST API wrapper
* UI frontend (React/Next.js) for viewing & filtering logs
* ML model for adaptive anomaly detection
