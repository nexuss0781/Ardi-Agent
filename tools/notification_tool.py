import os
import datetime
from langchain.tools import tool

# This file implements a simple, file-based notification tool.
# In a production system, this could be replaced with a real email or Slack API call.

_LOGS_DIR = os.path.join(os.getcwd(), "logs")
_NOTIFICATION_FILE = os.path.join(_LOGS_DIR, "notifications.log")

# Ensure the logs directory exists
os.makedirs(_LOGS_DIR, exist_ok=True)

@tool
def send_completion_notification(project_summary: str, run_id: str) -> str:
    """
    Sends a "notification" upon project completion by logging it to a file.
    
    Args:
        project_summary: A brief summary of the completed project.
        run_id: The unique ID of the agent run.
    """
    try:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = (
            f"--- NOTIFICATION ---\n"
            f"Timestamp: {timestamp}\n"
            f"Run ID: {run_id}\n"
            f"Project Status: COMPLETED\n"
            f"Summary: {project_summary}\n"
            f"--------------------\n\n"
        )
        
        with open(_NOTIFICATION_FILE, "a", encoding="utf-8") as f:
            f.write(log_message)
            
        print(f"--- [Tool] Completion notification logged for run_id: {run_id} ---")
        return "Notification logged successfully."
        
    except Exception as e:
        error_message = f"Failed to log notification: {e}"
        print(f"--- [Tool] ERROR: {error_message} ---")
        return error_message