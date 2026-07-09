import os

def find_path(target_name: str, search_root: str = "~") -> str:
    """Finds the absolute path of a specific file or directory starting from a root location."""
    clean_target = target_name.strip("'\"")
    # Resolve home directories like ~ to absolute paths
    resolved_root = os.path.abspath(os.path.expanduser(search_root.strip("'\"")))
    
    if not os.path.exists(resolved_root):
        return f"[find_path] Error: The search root directory '{resolved_root}' does not exist."

    matches = []
    # Walk the file system tree up to a reasonable depth or match count
    for root, dirs, files in os.walk(resolved_root):
        if clean_target in files:
            matches.append(os.path.join(root, clean_target))
        if clean_target in dirs:
            matches.append(os.path.join(root, clean_target))
        
        # Prevent massive memory bloat if running on raw root structures
        if len(matches) >= 5:
            break
            
    if not matches:
        return f"[find_path] Could not find any files or folders named '{clean_target}' under '{resolved_root}'."
        
    formatted_paths = "\n".join([f"- {path}" for path in matches])
    return f"[find_path] Found matching target locations:\n{formatted_paths}"


SKILLS = [
    {
        "name": "find_path",
        "description": "Locates the absolute path of a specified file or directory by walking down from a given root path location.",
        "trigger_phrases": ["find path", "locate file", "where is file", "search folder location", "path finder"],
        "func": find_path,
    },
]