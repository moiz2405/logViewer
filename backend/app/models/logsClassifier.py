import json
from typing import List
from pydantic import BaseModel, Field
from agno.agent import Agent
from agno.models.groq import Groq

# from backend.app.types.classifierTypes import SeverityLevel  # Types already defined elsewhere
from app.types.classifierTypes import SeverityLevel
# --------------------------------------------
# Response Schema
# --------------------------------------------

class LogsClassifier(BaseModel):
    service: str = Field(..., description="Microservice name like auth-service, payment-service etc.")
    error_type: str = Field(..., description="General category like Application Exception, Database Error, etc.")
    error_sub_type: str = Field(..., description="Specific kind like Timeout, Stack Trace, etc.")
    error_desc: str = Field(..., description="Concise human-readable error excerpt.")
    severity_level: SeverityLevel = Field(..., description="How urgent or severe: Low, Medium, High.")

# --------------------------------------------
# Agent Setup
# --------------------------------------------

def get_agent() -> Agent:
    return Agent(
        model=Groq(id="llama-3.3-70b-versatile"),
        description=(
            "You are a log classifier.\n"
            "From each log entry, extract the following fields:\n"
            "- `service`: (e.g., auth-service, user-service, payment-service)\n"
            "- `error_type`: (Application Exception, Infrastructure Error, Network Error, etc.)\n"
            "- `error_sub_type`: (Null Pointer Exception, Timeout, Stack Trace, etc.)\n"
            "- `error_desc`: A concise description (e.g., 'NullPointerException in UserController.java')\n"
            "- `severity_level`: One of Low, Medium, or High\n"
        ),
        markdown=True,
        response_model=LogsClassifier,
    )

AGENT_MAIN = get_agent()

# --------------------------------------------
# Core Classification Logic
# --------------------------------------------

def classify_log(log_line: str) -> LogsClassifier:
    prompt = f"Classify this log into structured fields:\n{log_line}"
    response = AGENT_MAIN.run(prompt, stream=False)
    return response.content

# --------------------------------------------
# Main Classification Handler
# --------------------------------------------

def classify_logs(input_path: str, output_path: str) -> List[LogsClassifier]:
    results = []

    with open(input_path, "r") as f:
        log_data = json.load(f)

    for key, log_entry in log_data.items():
        try:
            structured = classify_log(log_entry)
            results.append(structured)
        except Exception as e:
            print(f"[!] Error processing log {key}: {e}")

    with open(output_path, "w") as f:
        json.dump([log.dict() for log in results], f, indent=2)

    print(f"\nSaved {len(results)} structured logs to {output_path}")
    return results

# --------------------------------------------
# CLI Entrypoint
# --------------------------------------------

if __name__ == "__main__":
    input_file = "backend/app/outputs/processed_logs.log"
    output_file = "backend/app/outputs/structured_logs.json"
    classify_logs(input_file, output_file)
