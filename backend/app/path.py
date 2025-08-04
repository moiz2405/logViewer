from app.models.logsPreprocessor import process_logs
from app.models.logsClassifier import classify_logs


pre_input = "app/logs/dockerLogs.log"
pre_output = "app/outputs/processed_logs.json"
classified_output = "app/outputs/classified_logs.json"

# process_logs(pre_input,pre_output)



classify_logs(pre_output,classified_output)