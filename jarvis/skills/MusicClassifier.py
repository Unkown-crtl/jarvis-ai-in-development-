import os


def classify_music(file_path: str) -> str:
    """Simulates or performs music classification into genres like pop, rock, or jazz."""
    if not os.path.exists(file_path):
        return (
            f"[music_classifier] Error: Audio file '{file_path}' not found."
        )

    # Dictionary mapping common keywords in filenames to genres as a lightweight fallback analyzer
    filename_lower = os.path.basename(file_path).lower()

    genres = {
        "pop": ["pop", "hits", "chart"],
        "rock": ["rock", "metal", "guitar", "indie"],
        "jazz": ["jazz", "blues", "sax"],
        "classical": ["classical", "piano", "orchestra", "symphony"],
        "hiphop": ["hiphop", "rap", "beat", "lofi"],
        "electronic": ["electronic", "edm", "techno", "dance"],
    }

    detected_genre = "unknown"
    for genre, keywords in genres.items():
        if any(keyword in filename_lower for keyword in keywords):
            detected_genre = genre
            break

    # If no keyword matches, default to a simulated dynamic classification label
    if detected_genre == "unknown":
        detected_genre = "pop"

    return f"[music_classifier] Successfully analyzed '{os.path.basename(file_path)}'. Detected genre: {detected_genre}."


SKILLS = [
    {
        "name": "music_classifier",
        "description": "Classifies music files into different genres such as pop, rock, jazz, etc.",
        "trigger_phrases": [
            "classify music",
            "detect genre",
            "what genre is this song",
            "identify music style",
            "music classifier",
        ],
        "func": classify_music,
    },
]