"""
SKILL TEMPLATE — copy this file to add your own skill.
Remove this docstring and rename the file (no leading underscore).

How to create a skill:
1. Write one or more Python functions that do something useful.
2. Add them to the SKILLS list at the bottom.
3. Reload skills in Jarvis (Settings → Reload Skills) or restart.

Each entry in SKILLS must have:
  name          - unique snake_case identifier (matches the JSON action name)
  description   - one-line description shown to the LLM
  trigger_phrases - list of lowercase strings that hint at this skill
  func          - the callable to run
"""


def my_skill(message: str = "Hello from my skill!") -> str:
    """Example skill function."""
    return f"[my_skill] {message}"


SKILLS = [
    {
        "name": "my_skill",
        "description": "A custom example skill that returns a message.",
        "trigger_phrases": ["my skill", "example skill"],
        "func": my_skill,
    },
]
