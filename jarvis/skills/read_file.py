import os

def read_file(path: str) -> str:
    """Reads and returns the complete text or code content of a specified file path safely."""
    clean_path = path.strip("'\"")
    
    if not os.path.exists(clean_path):
        return f"[read_file] Error: File '{clean_path}' does not exist."
        
    if os.path.isdir(clean_path):
        return f"[read_file] Error: Path '{clean_path}' is a directory, not a file."
        
    try:
        with open(clean_path, "r", encoding="utf-8", errors="replace") as f:
            content = f.read()
            
        return content
        
    except Exception as e:
        return f"[read_file] Failed to read target file. Error: {str(e)}"


SKILLS = [
    {
        "name": "read_file",
        "description": "Reads and retrieves the exact string or script text contents from a specified file system path.",
        "trigger_phrases": ["read file", "view file", "show content of file", "open file source", "get file text"],
        "func": read_file,
    },
]