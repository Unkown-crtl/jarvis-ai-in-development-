import json


def recommend_albums(
    favorite_genres: str = "",
    favorite_artists: str = "",
    listening_history: str = "",
) -> str:
    """Recommends albums based on provided genre preferences, favorite artists, or historical records."""
    # Internal relational recommendation database mapping genres/artists to top albums
    catalog = {
        "rock": [
            {
                "album": "The Dark Side of the Moon",
                "artist": "Pink Floyd",
                "year": "1973",
            },
            {
                "album": "Abbey Road",
                "artist": "The Beatles",
                "year": "1969",
            },
        ],
        "pop": [
            {"album": "Future Nostalgia", "artist": "Dua Lipa", "year": "2020"},
            {"album": "Thriller", "artist": "Michael Jackson", "year": "1982"},
        ],
        "jazz": [
            {"album": "Kind of Blue", "artist": "Miles Davis", "year": "1959"},
            {"album": "A Love Supreme", "artist": "John Coltrane", "year": "1965"},
        ],
        "electronic": [
            {
                "album": "Random Access Memories",
                "artist": "Daft Punk",
                "year": "2013",
            },
            {"album": "Untrue", "artist": "Burial", "year": "2007"},
        ],
    }

    recommendations = []

    # Parse inputs to scan matches against our catalog
    genres_list = [g.strip().lower() for g in favorite_genres.split(",") if g.strip()]
    artists_list = [a.strip().lower() for a in favorite_artists.split(",") if a.strip()]
    history_str = listening_history.lower()

    # Priority 1: Match explicit favorite genres
    for genre in genres_list:
        if genre in catalog:
            recommendations.extend(catalog[genre])

    # Priority 2: Match explicit favorite artists or history flags
    for genre_key, albums in catalog.items():
        for item in albums:
            # Avoid adding duplicates
            if item in recommendations:
                continue
            
            # Check artist association
            if any(artist in item["artist"].lower() for artist in artists_list):
                recommendations.append(item)
                continue
                
            # Check history crossover relevance
            if history_str and (item["artist"].lower() in history_str or item["album"].lower() in history_str):
                recommendations.append(item)

    # Fallback default if no explicit parameters cross-referenced successfully
    if not recommendations:
        recommendations = catalog["rock"] + catalog["jazz"]

    # Limit payload stack size down to a clean top 3 recommendation set
    final_picks = recommendations[:3]

    formatted_json = json.dumps(final_picks, ensure_ascii=False)
    return f"[album_recommender] Recommendations based on user profile context: {formatted_json}"


SKILLS = [
    {
        "name": "album_recommender",
        "description": "Recommends musical albums based on preferred genres, artists, and listening history flags.",
        "trigger_phrases": [
            "recommend albums",
            "suggest music albums",
            "album recommendations",
            "what album should i listen to",
            "find music matching my taste",
            "album recommender",
        ],
        "func": recommend_albums,
    },
]