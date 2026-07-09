import os

def syntax_highlighting(path: str) -> str:
    """Reads a code file and returns its content enclosed in language-accurate Markdown code fences for layout presentation."""
    clean_path = path.strip("'\"")
    
    if not os.path.exists(clean_path):
        return f"[syntax_highlighting] Error: File '{clean_path}' does not exist."
        
    try:
        with open(clean_path, "r", encoding="utf-8") as f:
            code_content = f.read()
            
        ext = os.path.splitext(clean_path)[1].lower()
        
        # Map common extensions to Markdown syntax highlighters
        lang_mapping = {
            ".py": "python",
            ".js": "javascript",
            ".ts": "typescript",
            ".html": "html",
            ".css": "css",
            ".json": "json",
            ".md": "markdown",
            ".sh": "bash",
            ".bat": "batch",
            ".ps1": "powershell",
            ".cpp": "cpp",
            ".c": "c",
            ".cs": "csharp",
            ".java": "java",
            ".go": "go",
            ".rs": "rust",
            ".yaml": "yaml",
            ".yml": "yaml",
            ".xml": "xml"
        }
        
        lang = lang_mapping.get(ext, "")
        
        return (
            f"[syntax_highlighting] Displaying rendered syntax layout for '{clean_path}':\n\n"
            f"```{lang}\n"
            f"{code_content}\n"
            f"```"
        )
        
    except Exception as e:
        return f"[syntax_highlighting] Failed to parse file for highlighting. Error: {str(e)}"


SKILLS = [
    {
        "name": "syntax_highlighting",
        "description": "Reads a code file and returns its content enclosed in language-accurate Markdown code fences for layout presentation.",
        "trigger_phrases": ["syntax highlight", "highlight code", "show syntax", "render code colors", "display code file"],
        "func": syntax_highlighting,
    },
]