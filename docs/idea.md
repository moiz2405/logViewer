
# **LogViewer – Intelligent Log Analysis & Classification System**

## **Project Overview**

LogViewer is a comprehensive full-stack application that transforms raw system logs into structured, actionable insights through intelligent analysis and classification. The system combines advanced log processing, AI-powered classification, and an intuitive web interface to help developers and DevOps teams quickly identify and resolve issues in distributed systems.

---

## **🎯 Core Objectives**

1. **Automated Log Processing**: Parse and clean large log files from various sources (Docker containers, microservices, etc.)
2. **Intelligent Anomaly Detection**: Identify critical errors, failures, and warnings using pattern recognition
3. **Smart Classification**: Categorize anomalies by service, error type, severity, and metadata
4. **Structured Output**: Generate clean JSON summaries for analysis, monitoring, and visualization
5. **User-Friendly Interface**: Provide web-based dashboard for log management and analysis
6. **Scalable Architecture**: Support multiple applications and log sources with efficient processing

---

## **🏗️ System Architecture**

### **Full-Stack Structure**
```
logviewer/
├── backend/                    # Python-based log processing engine
│   ├── app/
│   │   ├── models/            # Core processing models
│   │   ├── types/             # Type definitions and enums
│   │   ├── logs/              # Raw log storage
│   │   ├── outputs/           # Processed results
│   │   └── path.py           # Main processing pipeline
│   └── requirements.txt       # Python dependencies
├── frontend/                   # Next.js web application
│   ├── app/
│   │   ├── components/        # React components
│   │   ├── dashboard/         # Dashboard pages
│   │   └── layout.tsx        # App layout
│   └── package.json          # Node.js dependencies
├── docs/                      # Documentation
└── README.md                 # Project documentation
```

---

## **🔧 Backend Implementation**

### **Tech Stack**
- **Language**: Python 3.11+
- **AI/ML**: Agno + Groq (LLM-powered classification)
- **Data Models**: Pydantic for type validation
- **Processing**: Regex-based parsing + AI classification
- **Output**: JSON structured data

### **1. Log Preprocessing (`logsPreprocessor.py`)**

**Purpose**: Clean and filter raw log files to extract meaningful anomalies

**Key Features**:
- **Anomaly Detection**: Uses keyword-based filtering to identify error patterns
- **Timestamp Extraction**: Extracts timestamps using regex patterns
- **Service Identification**: Parses service names from log format `[service-name]`
- **Metadata Enrichment**: Adds line numbers, source files, and compact error descriptions
- **Duplicate Prevention**: Prevents duplicate anomaly entries

**Implementation Details**:
```python
ANOMALY_KEYWORDS = [
    "exception", "failed", "error", "refused", "timeout", 
    "unavailable", "denied", "panic", "stacktrace", "crash", "fatal", "killed"
]

def extract_anomaly_metadata(log_line: str, line_number: int, source_file: str = None) -> dict:
    return {
        "timestamp": extract_timestamp(log_line),
        "compact_error": extract_compact_error(log_line),
        "line": log_line.strip(),
        "line_number": line_number,
        "source_file": os.path.basename(source_file) if source_file else None
    }
```

**Output Format**:
```json
{
  "1": {
    "timestamp": "2025-07-30 08:00:08,567",
    "compact_error": "Database connection failed: Connection refused in payment-service",
    "line": "2025-07-30 08:00:08,567 ERROR [payment-service] Database connection failed",
    "line_number": 12,
    "source_file": "exLogs.log"
  }
}
```

### **2. Log Classification (`logsClassifier.py`)**

**Purpose**: Use AI to classify preprocessed logs into structured categories

**Key Features**:
- **LLM Integration**: Uses Groq/Agno for intelligent classification
- **Enum-Based Types**: Structured categorization using predefined enums
- **Retry Logic**: Exponential backoff with fallback classification
- **Agent Management**: Performance optimization with preloaded agents
- **Normalization**: Consistent error type and service name mapping

**Classification Schema**:
```python
class LogsClassifier(BaseModel):
    service: str                           # e.g., "payment-service"
    error_type: ErrorType                  # e.g., "Database Error"
    error_sub_type: ErrorSubtype          # e.g., "Connection Refused"
    error_desc: str                       # Human-readable description
    severity_level: SeverityLevel         # High, Medium, Low
    timestamp: Optional[str]              # When the error occurred
```

**Error Type Mappings**:
```python
ERROR_TYPES = {
    "timeout": (ErrorType.TIMEOUT_ERROR, ErrorSubtype.TIMEOUT),
    "database": (ErrorType.DATABASE_ERROR, ErrorSubtype.DB_CONN_FAILED),
    "authentication": (ErrorType.SECURITY_ALERT, ErrorSubtype.AUTH_FAILURE),
    "503": (ErrorType.INFRASTRUCTURE_ERROR, ErrorSubtype.HTTP_5XX),
    "conflict": (ErrorType.BUSINESS_LOGIC_ERROR, ErrorSubtype.CONFLICT),
    # ... and many more
}
```

### **3. Log Grouping (`groupLogs.py`)**

**Purpose**: Aggregate and summarize classified logs by service

**Key Features**:
- **Service Grouping**: Groups logs by microservice
- **Statistical Analysis**: Counts by severity, error type, and frequency
- **Time Range Analysis**: Identifies first and latest errors
- **Deduplication**: Combines similar errors with occurrence counts
- **Summary Generation**: Creates executive summaries for each service

**Output Structure**:
```json
{
  "payment-service": {
    "summary": {
      "total_errors": 15,
      "severity_breakdown": {"High": 10, "Medium": 3, "Low": 2},
      "most_common_error_type": "Database Error",
      "first_error": "2025-07-30 08:00:08",
      "latest_error": "2025-07-30 08:45:23"
    },
    "compacted_logs": [...] // Deduplicated errors with counts
  }
}
```

### **4. Type System (`classifierTypes.py`)**

**Purpose**: Define structured enums for consistent classification

**Enum Categories**:
- **Service**: `auth-service`, `payment-service`, `api-gateway`, etc.
- **ErrorType**: `Application Exception`, `Database Error`, `Security Alert`, etc.
- **ErrorSubtype**: `Timeout`, `Connection Refused`, `Authentication Failure`, etc.
- **SeverityLevel**: `High`, `Medium`, `Low`

---

## **🎨 Frontend Implementation**

### **Tech Stack**
- **Framework**: Next.js 15.5.2 with App Router
- **Language**: TypeScript
- **Styling**: Tailwind CSS 4.1.12
- **UI Components**: Custom components with glass morphism effects
- **Icons**: Lucide React

### **1. Application Layout (`layout.tsx`)**

**Features**:
- **Global Layout**: Consistent navigation and styling across all pages
- **Font Integration**: Geist Sans and Geist Mono from Google Fonts
- **SEO Optimization**: Proper metadata configuration
- **Responsive Design**: Mobile-first approach

### **2. Navigation (`navbar.tsx`)**

**Features**:
- **Glass Morphism**: Backdrop blur with semi-transparent background
- **Responsive Menu**: Mobile hamburger menu with smooth animations
- **Hover Effects**: Animated underlines and scale transformations
- **Fixed Positioning**: Always visible navigation bar

**Key Animations**:
```css
/* Underline animation */
.group-hover:w-full   /* Expands from 0 to full width */

/* Button scaling */
.hover:scale-105      /* Slight scale on hover */

/* Mobile menu slide */
.transition-all duration-300   /* Smooth open/close */
```

### **3. Hero Section (`hero.tsx`)**

**Features**:
- **Centered Design**: Clean, minimal layout with proper spacing
- **Feature Highlights**: Three-column grid showcasing key capabilities
- **Call-to-Action**: Navigation to dashboard with smooth routing
- **Responsive Grid**: Stacks on mobile, grid on desktop

**Design Elements**:
- **Typography Hierarchy**: Clear heading, subtitle, and description structure
- **Icon Integration**: SVG icons with consistent styling
- **Color Scheme**: Professional blue and gray palette
- **Spacing System**: Consistent margins and padding throughout

### **4. Dashboard System**

**Structure**:
- **App Registration**: Form for registering new applications
- **Log Management**: Interface for viewing and analyzing processed logs
- **State Management**: React hooks for application data

---

## **📊 Data Flow & Processing Pipeline**

### **Step 1: Log Ingestion**
```
Raw Logs (Docker/Service) → logsPreprocessor.py
```
- Filters noise (INFO, DEBUG, TRACE logs)
- Extracts anomalies using keyword matching
- Adds metadata (timestamps, line numbers, source files)

### **Step 2: AI Classification**
```
Processed Logs → logsClassifier.py → LLM (Groq)
```
- Sends cleaned logs to AI model for classification
- Applies normalization rules for consistency
- Handles API failures with intelligent fallbacks

### **Step 3: Aggregation & Analysis**
```
Classified Logs → groupLogs.py
```
- Groups by service for easier analysis
- Generates statistical summaries
- Deduplicates similar errors

### **Step 4: Web Interface**
```
JSON Output → Frontend Dashboard
```
- Displays processed results in user-friendly interface
- Provides registration for new applications
- Enables log file uploads and analysis

---

## **🔍 Advanced Features**

### **1. AI-Powered Classification**
- **LLM Integration**: Uses large language models for intelligent error categorization
- **Retry Mechanism**: 3-attempt retry with exponential backoff
- **Fallback System**: Rule-based classification when AI fails
- **Performance Optimization**: Agent preloading for batch processing

### **2. Robust Error Handling**
- **Graceful Degradation**: System continues working even with partial failures
- **Comprehensive Logging**: Detailed logs for debugging and monitoring
- **Type Safety**: Pydantic models ensure data consistency
- **Input Validation**: Thorough validation of all inputs and outputs

### **3. Scalability Features**
- **Batch Processing**: Efficient handling of multiple log files
- **Memory Management**: Streaming processing for large files
- **Modular Architecture**: Easy to extend with new log sources
- **Performance Monitoring**: Built-in timing and progress tracking

---

## **🚀 Getting Started**

### **Backend Setup**
```bash
cd backend
pip install -r requirements.txt
python -m backend.app.path  # Run processing pipeline
```

### **Frontend Setup**
```bash
cd frontend
npm install
npm run dev  # Start development server
```

---

## **📈 Future Enhancements**

### **Planned Features**
1. **Real-time Processing**: Live log streaming and analysis
2. **Machine Learning**: Custom ML models for pattern detection
3. **API Integration**: RESTful API for external system integration
4. **Visualization**: Charts and graphs for trend analysis
5. **Alerting System**: Notifications for critical errors
6. **Multi-tenant Support**: Support for multiple organizations
7. **Log Correlation**: Cross-service error tracking
8. **Export Capabilities**: CSV, PDF, and dashboard exports

### **Technical Improvements**
- **Database Integration**: Persistent storage for historical data
- **Caching Layer**: Redis for improved performance
- **Authentication**: User management and security
- **Container Deployment**: Docker and Kubernetes support
- **CI/CD Pipeline**: Automated testing and deployment
- **Monitoring**: Application performance monitoring

---

## **💡 Key Innovation**

LogViewer's unique value proposition lies in its **hybrid approach** combining:
- **Rule-based preprocessing** for fast, reliable anomaly detection
- **AI-powered classification** for intelligent categorization
- **Structured output** ready for analysis and visualization
- **User-friendly interface** for non-technical stakeholders

This combination ensures both **accuracy and performance** while maintaining **ease of use** and **scalability** for enterprise environments.
