import json


def analyze_playlist(playlist_data: str) -> str:
    """Analyzes a structured playlist dataset to extract genre distributions, trends, and tracking insight summaries."""
    if not playlist_data:
        return "[playlist_analyzer] Error: Missing playlist data parameter."

    try:
        # Expecting either a raw JSON string payload list or a comma-separated list of tracks
        if playlist_data.strip().startswith("[") or playlist_data.strip().startswith("{"):
            tracks = json.loads(playlist_data)
        else:
            # Fallback parse for raw text structures
            tracks = [{"title": t.strip()} for t in playlist_data.split(",") if t.strip()]

        if not tracks:
            return "[playlist_analyzer] Error: Playlist track queue contains zero tracks."

        total_tracks = len(tracks)
        genre_counts = {}
        artist_counts = {}
        tempo_sum = 0
        has_tempo_data = False

        for track in tracks:
            if not isinstance(track, dict):
                continue

            # Extract implicit attributes safely
            genre = track.get("genre", "Unknown").strip().capitalize()
            artist = track.get("artist", "Unknown").strip()
            tempo = track.get("tempo", track.get("bpm", None))

            genre_counts[genre] = genre_counts.get(genre, 0) + 1
            artist_counts[artist] = artist_counts.get(artist, 0) + 1

            if tempo is not None:
                try:
                    tempo_sum += float(tempo)
                    has_tempo_data = True
                except ValueError:
                    pass

        # Compute insights metrics
        top_genre = max(genre_counts, key=genre_counts.get) if genre_counts else "Unknown"
        top_artist = max(artist_counts, key=artist_counts.get) if artist_counts else "Unknown"
        avg_tempo = round(tempo_sum / total_tracks, 1) if (has_tempo_data and total_tracks > 0) else None

        insights = {
            "total_tracks": total_tracks,
            "dominant_genre": top_genre,
            "top_contributing_artist": top_artist,
            "genre_distribution_map": genre_counts,
        }
        
        if avg_tempo:
            insights["average_estimated_bpm"] = avg_tempo

        formatted_json = json.dumps(insights, ensure_ascii=False)
        return f"[playlist_analyzer] Analysis complete: {formatted_json}"

    except Exception as e:
        return f"[playlist_analyzer] Error processing structural analysis: {str(e)}"


SKILLS = [
    {
        "name": "playlist_analyzer",
        "description": "Analyzes playlists to extract structured trends, patterns, genre balances, and behavioral track insights.",
        "trigger_phrases": [
            "analyze playlist",
            "playlist analysis",
            "playlist trends",
            "check my playlist patterns",
            "get breakdown of my tracks",
            "playlist insights",
            "breakdown playlist",
        ],
        "func": analyze_playlist,
    },
]