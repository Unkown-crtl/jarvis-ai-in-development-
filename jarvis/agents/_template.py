"""
AGENT TEMPLATE — copy this file to add your own agent.

Agents run automatically in the background at a set interval.
They are great for monitoring, reminders, data polling, and automation.

How to create an agent:
1. Write a Python function that does periodic work.
2. Return a string output (empty string = no log entry).
3. Add it to the AGENTS list below.
4. Reload in Jarvis (Settings → Reload Agents) or restart.

Each entry in AGENTS must have:
  name        - unique identifier
  description - shown in the Agents panel
  interval    - seconds between runs (0 = run once at startup)
  enabled     - whether it starts active
  func        - the callable to run
"""
import datetime


def my_agent() -> str:
    """Example: log the time every 5 minutes."""
    return f"Ping at {datetime.datetime.now().strftime('%H:%M:%S')}"


AGENTS = [
    {
        "name": "my_agent",
        "description": "Example agent that logs a ping every 5 minutes.",
        "interval": 300,
        "enabled": False, 
        "func": my_agent,
    }
]
