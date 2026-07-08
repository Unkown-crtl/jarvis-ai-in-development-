"""
planner.py

Planner Agent

This module creates an execution plan for a user request before the
assistant generates the final response.

Usage:

    from planner import create_plan

    plan = create_plan(user_prompt)
"""

from __future__ import annotations

from datetime import datetime
from textwrap import dedent


class Planner:
    """Simple planning agent."""

    def create_plan(self, prompt: str) -> str:
        prompt = prompt.strip()

        if not prompt:
            return "No task to plan."

        steps = [
            "Understand the user's request.",
            "Identify the desired output.",
            "Identify any missing information.",
            "Determine whether tools or APIs are required.",
            "Break the task into smaller subtasks.",
            "Solve each subtask in order.",
            "Verify correctness.",
            "Generate the final response.",
        ]

        plan = [
            "=" * 60,
            "PLANNER",
            "=" * 60,
            f"Created: {datetime.now()}",
            "",
            "GOAL:",
            prompt,
            "",
            "EXECUTION PLAN:",
        ]

        for i, step in enumerate(steps, start=1):
            plan.append(f"{i}. {step}")

        plan.extend(
            [
                "",
                "EXPECTED OUTPUT:",
                "A complete, correct response that follows the plan.",
            ]
        )

        return "\n".join(plan)


planner = Planner()


def create_plan(prompt: str) -> str:
    """Convenience function."""
    return planner.create_plan(prompt)


def planner_agent() -> str:
    """
    Background agent entry.

    Since scheduled agents don't receive a prompt, this simply
    reports that the planner is loaded.
    """
    return ""


AGENTS = [
    {
        "name": "planner",
        "description": "Plans user requests before execution.",
        "interval": 0,
        "enabled": True,
        "func": planner_agent,
    },
]


if __name__ == "__main__":
    while True:
        print()
        prompt = input("User > ")

        if prompt.lower() in {"exit", "quit"}:
            break

        print()
        print(create_plan(prompt))