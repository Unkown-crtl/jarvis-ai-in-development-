"""
Reasoning Engine — Plan → Reason → Act pipeline.

For complex requests, Jarvis first creates a structured plan,
then reasons step-by-step before acting. This mirrors chain-of-thought
prompting and gives the user visibility into Jarvis's thinking.
"""
import json
import re
from typing import Generator
from core.brain import chat


PLANNER_PROMPT = """You are a strategic planner for an AI assistant named Jarvis.
Given the user's request, produce a concise JSON plan:

{
  "goal": "one-sentence goal",
  "steps": ["step 1", "step 2", "..."],
  "requires_skills": ["skill_name_1"],
  "complexity": "simple|moderate|complex",
  "reasoning_needed": true|false
}

Only output valid JSON, nothing else."""


REASONER_PROMPT = """You are the reasoning core of Jarvis.
You have been given a plan and must reason through it step by step.

Plan: {plan}

Reason through each step carefully, then conclude with your final action.
Format:
THINKING: <your step-by-step reasoning>
CONCLUSION: <what you will do>
ACTION: <optional json action block if a skill should be called>"""


COMPLEXITY_THRESHOLD = 15  # words — short requests skip planning


def is_complex(text: str) -> bool:
    """Decide if a request needs the plan→reason pipeline."""
    words = len(text.split())
    triggers = [
        "debug", "fix", "analyze", "review", "compare", "explain how",
        "step by step", "refactor", "upgrade", "test", "plan", "create a",
        "build", "write a", "find all", "why is", "optimize"
    ]
    return words > COMPLEXITY_THRESHOLD or any(t in text.lower() for t in triggers)


def plan(user_input: str) -> dict:
    """Generate a structured plan for a request."""
    messages = [
        {"role": "system", "content": PLANNER_PROMPT},
        {"role": "user", "content": user_input},
    ]
    try:
        raw = chat(messages, stream=False)
        # Strip markdown fences if present
        raw = re.sub(r"```json|```", "", raw).strip()
        return json.loads(raw)
    except Exception:
        return {
            "goal": user_input,
            "steps": ["Process request", "Respond"],
            "requires_skills": [],
            "complexity": "moderate",
            "reasoning_needed": True,
        }


def reason_stream(user_input: str, plan_data: dict, skill_descriptions: str) -> Generator[str, None, None]:
    """Stream reasoning + conclusion given a plan."""
    prompt = REASONER_PROMPT.format(plan=json.dumps(plan_data, indent=2))
    messages = [
        {"role": "system", "content": prompt + f"\n\nAvailable skills:\n{skill_descriptions}"},
        {"role": "user", "content": user_input},
    ]
    yield from chat(messages, stream=True)
