import os

def write_file(path: str, content: str) -> str:
    """Writes text or code content to a specified file path, creating parent directories if missing."""
    clean_path = path.strip("'\"")
    
    try:
        directory = os.path.dirname(clean_path)
        if directory and not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            
        with open(clean_path, "w", encoding="utf-8") as f:
            f.write(content)
            
        return f"[write_file] Successfully wrote to file: {clean_path}"
        
    except Exception as e:
        return f"[write_file] Failed to write file. Error: {str(e)}"


SKILLS = [
    {
        "name": "write_file",
        "description": "Writes text or code content to a file path. Automatically handles missing folder creation to prevent directory errors.",
        "trigger_phrases": ["write file", "save file", "create file", "edit code", "update config"],
        "func": write_file,
    },
]