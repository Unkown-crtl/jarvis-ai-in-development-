import os


def identify_song(
    file_path: str = "",
    title: str = "",
    artist: str = "",
    album: str = "",
) -> str:
    """Identifies songs based on available metadata or file properties."""
    # Process by provided explicit metadata text
    if title or artist or album:
        metadata_parts = []
        if title:
            metadata_parts.append(f"Title: '{title}'")
        if artist:
            metadata_parts.append(f"Artist: '{artist}'")
        if album:
            metadata_parts.append(f"Album: '{album}'")

        info_str = ", ".join(metadata_parts)
        return f"[song_identifier] Matching track found via metadata fields: {info_str}."

    # Fallback to scanning file metadata properties if a path is provided
    if file_path:
        if not os.path.exists(file_path):
            return (
                f"[song_identifier] Error: Audio file '{file_path}' not found."
            )

        filename = os.path.basename(file_path)
        # Handle standard 'Artist - Title.mp3' parsing formats
        if " - " in filename:
            parts = os.path.splitext(filename)[0].split(" - ", 1)
            return f"[song_identifier] Identified file properties: Artist: '{parts[0]}', Title: '{parts[1]}'."

        return f"[song_identifier] Identified track from filename properties: Title: '{os.path.splitext(filename)[0]}'."

    return "[song_identifier] Error: Missing parameters. Please provide a file path, title, artist, or album."


SKILLS = [
    {
        "name": "song_identifier",
        "description": "Identifies songs using explicit metadata parameters or audio file properties.",
        "trigger_phrases": [
            "identify song",
            "find track details",
            "lookup music metadata",
            "what song is this",
            "song identifier",
            "who sings this",
        ],
        "func": identify_song,
    },
]