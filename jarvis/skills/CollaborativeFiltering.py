import json


def recommend_by_collaborative_filtering(
    user_id: str,
    top_n: int = 3,
) -> str:
    """Recommends tracks based on listening similarities and matrix overlap intersections between active user profiles."""
    if not user_id:
        return "[collaborative_filtering] Error: Parameter 'user_id' is highly required."

    user_key = user_id.strip().lower()

    # Matrix representation of tracking matrices containing user similarity clusters
    mock_matrix_clusters = {
        "user_101": {
            "similar_peers": ["user_204", "user_509"],
            "peer_listening_pool": [
                {"title": "Choosin' Texas", "artist": "Morgan Wallen", "score": 0.98},
                {"title": "Drop Dead", "artist": "Nessa Barrett", "score": 0.94},
                {"title": "Janice STFU", "artist": "SZA", "score": 0.89},
            ],
        },
        "user_102": {
            "similar_peers": ["user_112", "user_890"],
            "peer_listening_pool": [
                {"title": "Kind of Blue", "artist": "Miles Davis", "score": 0.96},
                {"title": "A Love Supreme", "artist": "John Coltrane", "score": 0.91},
                {"title": "Blue Train", "artist": "John Coltrane", "score": 0.85},
            ],
        },
    }

    # Extract match properties or use fallback defaults for unindexed keys
    if user_key in mock_matrix_clusters:
        cluster = mock_matrix_clusters[user_key]
        recommendations = cluster["peer_listening_pool"]
        peers_calculated = cluster["similar_peers"]
    else:
        # Fallback profile generating recommendations from the general trending global matrix pool
        peers_calculated = ["global_cluster_alpha", "global_cluster_beta"]
        recommendations = [
            {"title": "I Knew It, I Knew You", "artist": "Luke Combs", "score": 0.92},
            {"title": "Drop Dead", "artist": "Nessa Barrett", "score": 0.88},
            {"title": "Abbey Road", "artist": "The Beatles", "score": 0.81},
        ]

    # Constrain output dimensions down to requested index ranges safely
    final_recommendations = recommendations[:max(1, top_n)]

    payload = {
        "target_user": user_id,
        "nearest_neighbor_peers": peers_calculated,
        "collaborative_filtering_recommendations": final_recommendations,
    }

    formatted_json = json.dumps(payload, ensure_ascii=False)
    return f"[collaborative_filtering] Matrix matching loop completed: {formatted_json}"


SKILLS = [
    {
        "name": "collaborative_filtering",
        "description": "Generates personalized musical track recommendations based on vector overlaps of similar consumer listening matrix metrics.",
        "trigger_phrases": [
            "collaborative filtering",
            "recommend music from similar users",
            "what are similar users listening to",
            "user behavior music recommendations",
            "find music matches based on peers",
            "peer recommendations tracker",
        ],
        "func": recommend_by_collaborative_filtering,
    },
]