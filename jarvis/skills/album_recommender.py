import json


def recommend_musical_albums(
    genre: str = "rock",
    era: str = "all",
    preference_weights: dict = None,
) -> str:
    """Recommends classic and modern musical albums based on genre filters, era, and characteristic preference weights."""
    genre_target = genre.lower().strip()
    era_target = era.lower().strip()

    # Database of representative landmark musical albums across common genres
    album_vault = [
        {"title": "The Dark Side of the Moon", "artist": "Pink Floyd", "genre": "rock", "year": 1973, "attributes": {"melodic": 0.9, "energetic": 0.4, "experimental": 0.8}},
        {"title": "Abbey Road", "artist": "The Beatles", "genre": "rock", "year": 1969, "attributes": {"melodic": 0.95, "energetic": 0.6, "experimental": 0.5}},
        {"title": "Kind of Blue", "artist": "Miles Davis", "genre": "jazz", "year": 1959, "attributes": {"melodic": 0.85, "energetic": 0.2, "experimental": 0.6}},
        {"title": "A Love Supreme", "artist": "John Coltrane", "genre": "jazz", "year": 1965, "attributes": {"melodic": 0.6, "energetic": 0.7, "experimental": 0.9}},
        {"title": "To Pimp a Butterfly", "artist": "Kendrick Lamar", "genre": "hip-hop", "year": 2015, "attributes": {"melodic": 0.7, "energetic": 0.8, "experimental": 0.85}},
        {"title": "The Low End Theory", "artist": "A Tribe Called Quest", "genre": "hip-hop", "year": 1991, "attributes": {"melodic": 0.8, "energetic": 0.7, "experimental": 0.4}},
        {"title": "Random Access Memories", "artist": "Daft Punk", "genre": "electronic", "year": 2013, "attributes": {"melodic": 0.9, "energetic": 0.85, "experimental": 0.6}},
        {"title": "Untrue", "artist": "Burial", "genre": "electronic", "year": 2007, "attributes": {"melodic": 0.5, "energetic": 0.4, "experimental": 0.9}},
    ]

    # Default weight distribution matching vectors if none are specified
    weights = preference_weights if preference_weights else {"melodic": 1.0, "energetic": 1.0, "experimental": 1.0}

    filtered_albums = []
    for album in album_vault:
        # 1. Filter by broad genre match matches
        if genre_target != "all" and album["genre"] != genre_target:
            continue

        # 2. Filter by chronological release era properties
        year = album["year"]
        if era_target == "classic" and year >= 2000:
            continue
        if era_target == "modern" and year < 2000:
            continue

        # Calculate a matrix similarity rating score based on attributes weights
        score = 0.0
        attrs = album["attributes"]
        for key in weights:
            if key in attrs:
                score += float(attrs[key]) * float(weights[key])

        album_entry = album.copy()
        album_entry["recommendation_score"] = round(score, 2)
        filtered_albums.append(album_entry)

    # Sort results to place highest-rated recommendation indices at the front stack
    filtered_albums.sort(key=lambda x: x["recommendation_score"], reverse=True)

    report = {
        "applied_genre_filter": genre_target,
        "applied_era_filter": era_target,
        "preference_profiles_evaluated": weights,
        "recommendations_found_count": len(filtered_albums),
        "recommended_albums": filtered_albums[:3]
    }

    return f"[album_recommender] Recommendation scoring pipeline execution complete: {json.dumps(report, ensure_ascii=False)}"


SKILLS = [
    {
        "name": "album_recommender",
        "description": "Recommends musical albums matching explicit acoustic attributes, profile preferences, genres, and production eras.",
        "trigger_phrases": [
            "album recommender",
            "recommend musical albums",
            "suggest music albums",
            "find albums to listen to",
            "music recommendation system",
            "get custom album suggestions",
        ],
        "func": recommend_musical_albums,
    },
]