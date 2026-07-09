import json


def extract_and_analyze_lyrics(
    song_title: str = "",
    artist: str = "",
    raw_lyrics: str = "",
) -> str:
    """Extracts or processes song lyrics to analyze structural sentiment, core themes, and deeper meanings."""
    lyrics_to_analyze = raw_lyrics.strip()
    title_clean = song_title.strip()
    artist_clean = artist.strip()

    # If no explicit lyrics are passed, look up matching tracks from the 2026 global music archive
    if not lyrics_to_analyze and title_clean:
        lookup_key = f"{title_clean.lower()} by {artist_clean.lower()}".or_strip()
        
        # Local mock registry for prominent charting titles in 2026
        lyric_archive = {
            "drop dead": (
                "If you let me stay the night / Well I think I might just have to stay forever / "
                "You make me feel so dizzy, counting down the lines / Drop dead, you look so beautiful it hurts."
            ),
            "the cure": (
                "I tried to piece it back together but the glue won't stick / "
                "Turns out that love, ultimately, can't save her / Finding my own way out of the thick."
            ),
            "stateside": (
                "Cause I fly Stockholm to LA, leave my feelings on the plane / "
                "Catching sun rays in the stateside, running from the structural pain."
            ),
        }

        # Attempt to resolve lookup against database keys
        for key, lyrics_text in lyric_archive.items():
            if key in title_clean.lower():
                lyrics_to_analyze = lyrics_text
                break

    if not lyrics_to_analyze:
        if title_clean:
            return f"[lyrics_extractor] Error: Could not find recorded lyrics for '{title_clean}' in the local library index. Please supply raw_lyrics text."
        return "[lyrics_extractor] Error: Please provide either a valid song_title or explicit raw_lyrics text blocks to run the analyzer."

    # Execute text-mining processing for sentiment weights and structural keywords
    lyrics_lower = lyrics_to_analyze.lower()
    
    # Emotional profiling catalogs
    positive_indicators = ["love", "beautiful", "forever", "stay", "sun", "free", "together", "bright"]
    negative_indicators = ["hurt", "pain", "sad", "can't", "plane", "leave", "won't", "dead", "thick"]

    pos_score = sum(lyrics_lower.count(word) for word in positive_indicators)
    neg_score = sum(lyrics_lower.count(word) for word in negative_indicators)

    # Determine aggregated dominant score paths
    if pos_score > neg_score:
        sentiment = "Positive / Romantic / Uplifting"
    elif neg_score > pos_score:
        sentiment = "Negative / Melancholic / Introspective"
    else:
        sentiment = "Mixed / Conflicted / Nuanced"

    # Identify recurring structural thematic frameworks
    themes = []
    if any(w in lyrics_lower for w in ["love", "forever", "stay", "beautiful"]):
        themes.append("Romantic Devotion & Infatuation")
    if any(w in lyrics_lower for w in ["hurt", "pain", "save", "cure"]):
        themes.append("Emotional Vulnerability & Healing")
    if any(w in lyrics_lower for w in ["plane", "la", "stockholm", "running", "leave"]):
        themes.append("Escapism & Geographic Boundaries")
    
    if not themes:
        themes.append("General Abstract / Experiential Human Conditions")

    analysis_payload = {
        "analyzed_title": title_clean if title_clean else "Unknown Track",
        "analyzed_artist": artist_clean if artist_clean else "Unknown Artist",
        "extracted_lyrics_excerpt": (lyrics_to_analyze[:120] + "...") if len(lyrics_to_analyze) > 120 else lyrics_to_analyze,
        "computed_sentiment": sentiment,
        "primary_identified_themes": themes,
    }

    formatted_json = json.dumps(analysis_payload, ensure_ascii=False)
    return f"[lyrics_extractor] Processing loop analysis completed successfully: {formatted_json}"


SKILLS = [
    {
        "name": "lyrics_extractor",
        "description": "Extracts lyrics from songs to process textual sentiment profiles, thematic scopes, and hidden meanings.",
        "trigger_phrases": [
            "extract lyrics",
            "analyze lyric meaning",
            "find song themes",
            "sentiment of lyrics",
            "what do these lyrics mean",
            "lyrics extractor",
            "explain lyrics",
        ],
        "func": extract_and_analyze_lyrics,
    },
]