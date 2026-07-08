"""
Reminder Agent
Checks every 30 seconds if there are pending reminders in reminders.json
"""
import json
import os
import datetime


REMINDERS_FILE = "reminders.json"


def check_reminders() -> str:
    if not os.path.exists(REMINDERS_FILE):
        return ""

    with open(REMINDERS_FILE) as f:
        reminders = json.load(f)

    now = datetime.datetime.now()
    triggered = []
    remaining = []

    for r in reminders:
        due = datetime.datetime.fromisoformat(r["due"])
        if now >= due:
            triggered.append(r["message"])
        else:
            remaining.append(r)

    if triggered:
        with open(REMINDERS_FILE, "w") as f:
            json.dump(remaining, f, indent=2)
        return "🔔 REMINDER: " + " | ".join(triggered)

    return ""


AGENTS = [
    {
        "name": "reminder",
        "description": "Checks reminders.json every 30s and fires due reminders.",
        "interval": 30,
        "enabled": True,
        "func": check_reminders,
    }
]
