import random

def idea_generation(topic: str, constraint: str = "none") -> str:
    """Generate new creative ideas and concepts based on a given prompt, topic, or constraint."""
    # Seed idea framework angles
    frameworks = [
        "The Direct Disruption: Invert the most common assumption about this topic.",
        "The Hybrid Cross: Merge this topic with a completely unrelated industry or hobby.",
        "The Accessibility Angle: Redesign this for someone who only has 5 minutes a day or zero technical skill.",
        "The Automation Focus: How could AI or a simple script handle 90% of the friction in this area?"
    ]
    
    selected_angle = random.choice(frameworks)
    
    return (
        f"[idea_generation] Topic: '{topic}' | Constraint: '{constraint}'\n"
        f"Suggested Brainstorming Angle: {selected_angle}\n"
        f"Idea Draft: [Placeholder: Use text-generation pipelines or an LLM endpoint "
        f"to expand this structural angle into a full set of concrete brainstormed concepts]."
    )


SKILLS = [
    {
        "name": "idea_generation",
        "description": "Generate new ideas based on a given prompt, topic, or constraint.",
        "trigger_phrases": [
            "generate ideas",
            "brainstorm concepts",
            "give me ideas for",
            "creative ideation",
            "think of an alternative",
            "idea generation"
        ],
        "func": idea_generation,
    },
]