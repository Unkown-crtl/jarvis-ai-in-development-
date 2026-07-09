import random

def joke_generation(topic: str = "general") -> str:
    """Create humorous jokes and puns on a given topic or theme."""
    topic_lower = topic.lower()
    
    jokes_database = {
        "programming": [
            "Why do programmers wear glasses? Because they can't C#.",
            "There are 10 types of people in the world: those who understand binary, and those who don't.",
            "How many programmers does it take to change a light bulb? None, that's a hardware problem."
        ],
        "science": [
            "Why can't you trust an atom? Because they make up everything!",
            "Have you heard the one about cobalt, radon, and yttrium? It's CoRnY.",
            "What did the biologist wear to their first date? Designer genes."
        ],
        "general": [
            "Why don't scientists trust atoms? Because they make up everything!",
            "I told my doctor that I broke my arm in two places. He told me to stop going to those places.",
            "What do you call a fake noodle? An impasta."
        ]
    }
    
    for key in jokes_database:
        if key in topic_lower:
            joke = random.choice(jokes_database[key])
            return f"[joke_generation] Topic: {key.capitalize()} | Joke: {joke}"
            
    joke = random.choice(jokes_database["general"])
    return f"[joke_generation] Topic: {topic} | Joke: {joke}"


SKILLS = [
    {
        "name": "joke_generation",
        "description": "Create humorous jokes and puns on a given topic or theme.",
        "trigger_phrases": [
            "tell me a joke",
            "make me laugh",
            "generate a pun",
            "tell a funny story",
            "crack a joke",
            "joke generation"
        ],
        "func": joke_generation,
    },
]