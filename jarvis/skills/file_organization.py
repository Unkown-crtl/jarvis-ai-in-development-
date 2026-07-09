import os

def file_organization(directory_path: str, action: str = "categorize") -> str:
    """Help users organize and categorize files on local or cloud storage systems."""
    if not os.path.exists(directory_path):
        return f"[file_organization] Error: The path '{directory_path}' does not exist."

    # Mapping common extensions to folder categories
    extensions_map = {
        "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".pptx", ".csv"],
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
        "Audio": [".mp3", ".wav", ".aac", ".flac"],
        "Video": [".mp4", ".mkv", ".avi", ".mov"],
        "Archives": [".zip", ".tar", ".gz", ".rar", ".7z"],
        "Scripts": [".py", ".js", ".html", ".css", ".sh", ".bat"]
    }

    try:
        files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]
        moved_summary = {}

        if action == "categorize":
            for file in files:
                _, ext = os.path.splitext(file)
                ext = ext.lower()
                
                target_folder = "Others"
                for folder, exts in extensions_map.items():
                    if ext in exts:
                        target_folder = folder
                        break
                
                target_dir = os.path.join(directory_path, target_folder)
                if not os.path.exists(target_dir):
                    os.makedirs(target_dir)
                    
                os.rename(os.path.join(directory_path, file), os.path.join(target_dir, file))
                moved_summary[target_folder] = moved_summary.get(target_folder, 0) + 1

            summary_str = ", ".join([f"{count} into {folder}" for folder, count in moved_summary.items()])
            return f"[file_organization] Success: Organized {len(files)} files ({summary_str or 'No files sorted'})."
            
        return f"[file_organization] Action '{action}' is not supported. Use 'categorize'."
        
    except Exception as e:
        return f"[file_organization] Error processing directory: {str(e)}"


SKILLS = [
    {
        "name": "file_organization",
        "description": "Help users organize and categorize files on their computer or cloud storage services such as Dropbox or Google Drive.",
        "trigger_phrases": ["organize files", "sort my directory", "categorize documents", "clean up folder", "file organization", "google drive sorting"],
        "func": file_organization,
    },
]