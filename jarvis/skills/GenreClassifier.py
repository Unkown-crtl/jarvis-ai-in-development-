import json


def classify_genre_by_features(
    tempo: float = 0.0,
    timbre: str = "",
    energy: float = 0.5,
    danceability: float = 0.5,
) -> str:
    """Classifies musical genre based on raw physical acoustic properties like tempo, timbre, energy, and danceability."""
    # Normalize timbre text descriptors for easier classification logic matching
    timbre_clean = timbre.lower().strip()

    # Rule-based acoustic boundary checking matrix
    if tempo >= 120 and "electronic" in timbre_clean or "synth" in timbre_clean:
        predicted_genre = "Electronic / EDM"
        confidence = 0.88
    elif tempo >= 110 and danceability >= 0.7 and ("punchy" in timbre_clean or "bright" in timbre_clean):
        predicted_genre = "Pop"
        confidence = 0.85
    elif "distorted" in timbre_clean or "guitar" in timbre_clean or "crunchy" in timbre_clean:
        predicted_genre = "Rock / Metal"
        confidence = 0.91
    elif tempo >= 70 and tempo <= 100 and "boombap" in timbre_clean or "sub" in timbre_clean:
        predicted_genre = "Hip-Hop"
        confidence = 0.84
    elif "brass" in timbre_clean or "sax" in timbre_clean or "smooth" in timbre_clean:
        predicted_genre = "Jazz"
        confidence = 0.89
    elif "orchestral" in timbre_clean or "strings" in timbre_clean or "piano" in timbre_clean:
        predicted_genre = "Classical"
        confidence = 0.93
    else:
        # Fallback multi-factorial heuristics based on acoustic energy balances
        if energy >= 0.7:
            predicted_genre = "Rock / Pop (High Energy Variant)"
            confidence = 0.60
        else:
            predicted_genre = "Ambient / Indie-Folk (Low Energy Variant)"
            confidence = 0.55

    payload = {
        "acoustic_profile_received": {
            "tempo_bpm": tempo if tempo > 0 else "Not specified",
            "timbre_signature": timbre if timbre else "Not specified",
            "energy_coefficient": energy,
            "danceability_coefficient": danceability,
        },
        "classification_result": {
            "predicted_genre": predicted_genre,
            "confidence_score": confidence,
        },
    }

    formatted_json = json.dumps(payload, ensure_ascii=False)
    return f"[genre_classifier] Acoustic feature modeling complete: {formatted_json}"


SKILLS = [
    {
        "name": "genre_classifier",
        "description": "Classifies musical genres by parsing acoustic features like tempo, timbre profiles, energy, and danceability keys.",
        "trigger_phrases": [
            "classify genre by features",
            "acoustic genre classification",
            "determine genre from tempo",
            "analyze audio features genre",
            "genre classifier",
            "detect style from audio traits",
        ],
        "func": classify_genre_by_features,
    },
]