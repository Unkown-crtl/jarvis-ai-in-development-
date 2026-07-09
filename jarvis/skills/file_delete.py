import os

def delete_file(filename: str, folder_name: str = "Downloads") -> str:
    """Locates and deletes a specified file from a folder path map."""
    clean_filename = filename.strip("'\"")
    clean_folder = folder_name.strip("'\"")
    
    # Resolve standard system directories directly
    if clean_folder.lower() in ["downloads", "desktop", "documents"]:
        target_dir = os.path.abspath(os.path.expanduser(f"~/{clean_folder.capitalize()}"))
    else:
        # Dynamically scan local user directory structures for custom folders
        target_dir = ""
        home_root = os.path.abspath(os.path.expanduser("~"))
        for root, dirs, _ in os.walk(home_root):
            if clean_folder in dirs:
                target_dir = os.path.join(root, clean_folder)
                break

    if not target_dir or not os.path.exists(target_dir):
        # Last fallback check within working space folder layout
        target_dir = os.path.abspath("workspace")

    full_file_path = os.path.join(target_dir, clean_filename)

    try:
        if os.path.exists(full_file_path):
            if os.path.isdir(full_file_path):
                return f"[delete_file] Error: Target '{full_file_path}' is a directory, not a file target."
            os.remove(full_file_path)
            return f"[delete_file] Successfully purged target file from path location: {full_file_path}"
        else:
            return f"[delete_file] Error: Could not locate file '{clean_filename}' inside target space: {target_dir}"
    except Exception as e:
        return f"[delete_file] Failed executing deletion routine sequence. Error: {str(e)}"


SKILLS = [
    {
        "name": "delete_file",
        "description": "Deletes a targeted file from a folder path location by checking system directories.",
        "trigger_phrases": ["delete file", "remove file", "purge file", "erase text file", "delete from downloads"],
        "func": delete_file,
    },
]