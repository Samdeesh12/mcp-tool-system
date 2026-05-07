# frontend/utils/logger.py
# Logs every conversation to a file so we have a full audit trail

import json
import os
from datetime import datetime

LOG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "logs"
)

def ensure_log_dir():
    os.makedirs(LOG_PATH, exist_ok=True)

def log_conversation(user_message: str, ai_response: str, tool_used: str = None):
    """Save a conversation turn to today's log file."""
    ensure_log_dir()
    today = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(LOG_PATH, f"session_{today}.json")

    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user_message,
        "assistant": ai_response,
        "tool_used": tool_used
    }

    # Load existing log or start fresh
    if os.path.exists(log_file):
        with open(log_file, "r") as f:
            data = json.load(f)
    else:
        data = []

    data.append(entry)

    with open(log_file, "w") as f:
        json.dump(data, f, indent=2)

def get_all_logs() -> list:
    """Return all logged conversations across all sessions."""
    ensure_log_dir()
    all_entries = []
    for filename in sorted(os.listdir(LOG_PATH)):
        if filename.endswith(".json"):
            with open(os.path.join(LOG_PATH, filename), "r") as f:
                all_entries.extend(json.load(f))
    return all_entries

def get_tool_usage_stats() -> dict:
    """Count how many times each tool was used across all sessions."""
    logs = get_all_logs()
    stats = {}
    for entry in logs:
        tool = entry.get("tool_used")
        if tool:
            stats[tool] = stats.get(tool, 0) + 1
    return stats