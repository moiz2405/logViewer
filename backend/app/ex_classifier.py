import re
from datetime import datetime
from enum import Enum
from typing import Optional


class Service(str, Enum):
    AUTH = "auth-service"
    API_GATEWAY = "api-gateway"
    USER = "user-service"
    PAYMENT = "payment-service"
    NOTIFICATION = "notification-service"
    INVENTORY = "inventory-service"


class ErrorType(str, Enum):
    APPLICATION_EXCEPTION = "Application Exception"
    INFRASTRUCTURE_ERROR = "Infrastructure Error"
    NETWORK_ERROR = "Network Error"
    DATABASE_ERROR = "Database Error"
    SECURITY_ALERT = "Security Alert"
    RESOURCE_EXHAUSTION = "Resource Exhaustion"
    DEPLOYMENT_ISSUE = "Deployment Issue"
    TIMEOUT_ERROR = "Timeout"
    UNKNOWN_ERROR = "Unknown"


class ErrorSubtype(str, Enum):
    STACK_TRACE = "Stack Trace"
    NULL_POINTER = "Null Pointer Exception"
    CONNECTION_REFUSED = "Connection Refused"
    TIMEOUT = "Timeout"
    OOM_KILLED = "Out of Memory (OOMKilled)"
    DB_CONN_FAILED = "Database Connection Failed"
    AUTH_FAILURE = "Authentication Failure"
    RATE_LIMIT_HIT = "Rate Limit Hit"
    CONFIG_MISMATCH = "Configuration Mismatch"
    SSL_HANDSHAKE_ERROR = "SSL Handshake Error"
    PERMISSION_DENIED = "Permission Denied"
    SERVICE_UNAVAILABLE = "Service Unavailable"
    UNKNOWN = "Unknown"


class SeverityLevel(str, Enum):
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


class LogParser:
    def __init__(self):
        self.service_keywords = {
            Service.AUTH: ["auth", "login", "token"],
            Service.API_GATEWAY: ["gateway", "nginx", "proxy"],
            Service.USER: ["user", "profile", "account"],
            Service.PAYMENT: ["payment", "transaction", "gateway"],
            Service.NOTIFICATION: ["notify", "email", "sms", "webhook"],
            Service.INVENTORY: ["stock", "inventory", "item", "warehouse"]
        }

    def classify_service(self, line: str) -> Optional[Service]:
        for service, keywords in self.service_keywords.items():
            if any(keyword in line.lower() for keyword in keywords):
                return service
        return None

    def classify_error_type(self, line: str) -> ErrorType:
        line = line.lower()
        if "timeout" in line:
            return ErrorType.TIMEOUT_ERROR
        if "exception" in line or "traceback" in line:
            return ErrorType.APPLICATION_EXCEPTION
        if "connection refused" in line or "network" in line:
            return ErrorType.NETWORK_ERROR
        if "oom" in line or "memory" in line:
            return ErrorType.RESOURCE_EXHAUSTION
        if "db" in line or "sql" in line:
            return ErrorType.DATABASE_ERROR
        if "unauthorized" in line or "forbidden" in line:
            return ErrorType.SECURITY_ALERT
        if "deployment" in line or "rollout" in line:
            return ErrorType.DEPLOYMENT_ISSUE
        return ErrorType.UNKNOWN_ERROR

    def classify_error_subtype(self, line: str) -> ErrorSubtype:
        line = line.lower()
        if "nullpointer" in line:
            return ErrorSubtype.NULL_POINTER
        if "connection refused" in line:
            return ErrorSubtype.CONNECTION_REFUSED
        if "timeout" in line:
            return ErrorSubtype.TIMEOUT
        if "oomkilled" in line or "out of memory" in line:
            return ErrorSubtype.OOM_KILLED
        if "auth fail" in line or "invalid token" in line:
            return ErrorSubtype.AUTH_FAILURE
        if "rate limit" in line:
            return ErrorSubtype.RATE_LIMIT_HIT
        if "ssl handshake" in line:
            return ErrorSubtype.SSL_HANDSHAKE_ERROR
        if "permission denied" in line:
            return ErrorSubtype.PERMISSION_DENIED
        if "db conn" in line:
            return ErrorSubtype.DB_CONN_FAILED
        if "config" in line:
            return ErrorSubtype.CONFIG_MISMATCH
        if "service unavailable" in line:
            return ErrorSubtype.SERVICE_UNAVAILABLE
        if "traceback" in line:
            return ErrorSubtype.STACK_TRACE
        return ErrorSubtype.UNKNOWN

    def determine_severity(self, line: str) -> SeverityLevel:
        line = line.lower()
        if "critical" in line or "panic" in line:
            return SeverityLevel.HIGH
        if "warn" in line:
            return SeverityLevel.MEDIUM
        if "info" in line:
            return SeverityLevel.LOW
        if "error" in line:
            return SeverityLevel.HIGH
        return SeverityLevel.MEDIUM

    def parse_line(self, line: str) -> Optional[dict]:
        line = line.strip()
        if not line or "info" in line.lower():  # Skip pure info logs
            return None

        timestamp_match = re.search(r"\d{4}-\d{2}-\d{2}[ T]\d{2}:\d{2}:\d{2}(?:,\d+)?", line)
        timestamp = (
            datetime.strptime(timestamp_match.group(), "%Y-%m-%d %H:%M:%S")
            if timestamp_match else None
        )

        service = self.classify_service(line)
        if not service:
            return None  # Skip logs not belonging to a known service

        return {
            "timestamp": timestamp.isoformat() if timestamp else None,
            "service": service.value,
            "error_type": self.classify_error_type(line).value,
            "error_subtype": self.classify_error_subtype(line).value,
            "severity": self.determine_severity(line).value,
            "raw": line
        }
