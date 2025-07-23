import os
from datetime import datetime

LOG_FILE = "logs/swarm.log"

os.makedirs("logs", exist_ok=True)

def log_msg(text: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {text}\n")

FEEDBACK_LOG = "logs/swarm_feedback.log"

def log_feedback(text: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    with open(FEEDBACK_LOG, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {text}\n")
