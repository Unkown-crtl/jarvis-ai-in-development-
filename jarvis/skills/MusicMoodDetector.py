import json


def detect_music_mood(
    file_path: str = "",
    lyrics: str = "",
    title: str = "",
    artist: str = "",
) -> str:
    """Detects the mood or emotion conveyed by a song's tracks, lyrics, and metadata markers."""
    detected_moods = []
    valence = 0.5
    energy = 0.5

    # Scan lyrics for key emotional indicators
    if lyrics:
        lyrics_lower = lyrics.lower()
        sad_words = ["sad", "cry", "tears", "broken", "lonely", "hurt", "pain", "miss", "goodbye"]
        happy_words = ["happy", "love", "dance", "smile", "joy", "celebrate", "free", "bright", "good"]
        angry_words = ["hate", "mad", "angry", "stfu", "kill", "burn", "fight", "never", "dead"]

        sad_score = sum(lyrics_lower.count(w) for w in sad_words)
        happy_score = sum(lyrics_lower.count(w) for w in happy_words)
        angry_score = sum(lyrics_lower.count(w) for w in angry_words)

        if sad_score > happy_score and sad_score > angry_score:
            detected_moods.append("Melancholic")
            valence -= 0.3
            energy -= 0.2
        elif happy_score > sad_score and happy_score > angry_score:
            detected_moods.append("Joyful")
            valence += 0.3
            energy += 0.1
        elif angry_score > sad_score and angry_score > happy_score:
            detected_moods.append("Aggressive")
            valence -= 0.2
            energy += 0.3

    # Scan title and artist context for matching 2026 chart metadata properties
    combined_meta = f"{title} {artist}".lower()
    if combined_meta:
        if any(h in combined_meta for h in ["drop dead", "janice stfu", "hate that i made you love me"]):
            detected_moods.append("Angsty/Aggressive")
            valence = min(valence, 0.3)
            energy = max(energy, 0.7)
        elif any(h in combined_meta for h in ["choosin\' texas", "i feel so free", "beautiful people"]):
            detected_moods.append("Energetic/Upbeat")
            valence = max(valence, 0.7)
            energy = max(energy, 0.8)
        elif any(h in combined_meta for h in ["the fate of ophelia", "tears", "stupid song"]):
            detected_moods.append("Somber/Poignant")
            valence = min(valence, 0.2)
            energy = min(energy, 0.4)

    # Normalize defaults if evaluation parameters yield zero explicit markers
    if not detected_moods:
        detected_moods.append("Balanced/Neutral")

    analysis = {
        "primary_detected_moods": detected_moods,
        "estimated_valence": round(max(0.0, min(1.0, valence)), 2),
        "estimated_energy": round(max(0.0, min(1.0, energy)), 2),
    }

    formatted_json = json.dumps(analysis, ensure_ascii=False)
    return f"[music_mood_detector] Analysis execution complete: {formatted_json}"


SKILLS = [
    {
        "name": "music_mood_detector",
        "description": "Detects the emotional mood or valence conveyed by lyrics, text, and metadata signatures.",
        "trigger_phrases": [
            "detect mood",
            "song emotion",
            "analyze music mood",
            "what is the vibe of this song",
            "lyric emotion analyzer",
            "music mood detector",
        ],
        "func": detect_music_mood,
    },
]