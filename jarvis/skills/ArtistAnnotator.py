import json
import os


def annotate_artist(
    artist_name: str, requested_info: str = "all"
) -> str:
    """Annotates an artist with metadata such as biography, awards, or discography."""
    if not artist_name:
        return "[artist_annotator] Error: Artist name parameter is required."

    artist_clean = artist_name.strip().lower()
    requested_info = requested_info.lower()

    # Simulated local metadata storage dictionary
    artist_database = {
        "the beatles": {
            "bio": "An English rock band formed in Liverpool in 1960, widely regarded as the most influential band in history.",
            "awards": "7 Grammy Awards, 1 Academy Award, 15 Ivor Novello Awards.",
            "discography": "Please Please Me (1963), Revolver (1966), Abbey Road (1969), Let It Be (1970).",
        },
        "daft punk": {
            "bio": "French electronic music duo formed in 1993 in Paris, achieving popularity in the late 1990s house movement.",
            "awards": "6 Grammy Awards, 2 World Music Awards.",
            "discography": "Homework (1997), Discovery (2001), Human After All (2005), Random Access Memories (2013).",
        },
        "miles davis": {
            "bio": "American trumpeter, bandleader, and composer, among the most influential figures in the history of jazz.",
            "awards": "8 Grammy Awards, Grammy Lifetime Achievement Award.",
            "discography": "Birth of the Cool (1957), Kind of Blue (1959), Bitches Brew (1970).",
        },
    }

    # Match artist data or build dynamic placeholder annotations
    if artist_clean in artist_database:
        data = artist_database[artist_clean]
    else:
        # Fallback profile for unknown artists
        data = {
            "bio": f"No biography entry found for '{artist_name}'.",
            "awards": f"No recorded award entries found for '{artist_name}'.",
            "discography": f"No discography records found for '{artist_name}'.",
        }

    # Filter fields based on selection criteria
    response_data = {}
    if requested_info in ["bio", "all"]:
        response_data["Biography"] = data["bio"]
    if requested_info in ["awards", "all"]:
        response_data["Awards"] = data["awards"]
    if requested_info in ["discography", "all"]:
        response_data["Discography"] = data["discography"]

    if not response_data:
        return f"[artist_annotator] Error: Invalid information segment '{requested_info}' requested."

    formatted_json = json.dumps(response_data, ensure_ascii=False)
    return f"[artist_annotator] Artist Profile for '{artist_name}': {formatted_json}"


SKILLS = [
    {
        "name": "artist_annotator",
        "description": "Annotates artists with metadata info like bio, awards, and discography lists.",
        "trigger_phrases": [
            "annotate artist",
            "artist info",
            "get artist bio",
            "artist awards",
            "artist discography",
            "find artist biography",
            "look up musician details",
        ],
        "func": annotate_artist,
    },
]