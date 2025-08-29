from backend.app.models.logsPreprocessor import process_logs
from backend.app.models.logsClassifier import classify_logs
from backend.app.models.groupLogs import group_logs

pre_input = "backend/app/logs/exLogs.log"
pre_output = "backend/app/outputs/processed_logs.json"
classified_output = "backend/app/outputs/classified_logs.json"
grouped_output = "backend/app/outputs/grouped_logs.json"

# process_logs(pre_input,pre_output)
# classify_logs(pre_output,classified_output)

group_logs(classified_output,grouped_output)