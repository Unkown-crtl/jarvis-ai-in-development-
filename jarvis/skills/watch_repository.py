import os
import json

def watch_repository(repo_path: str = "", branch: str = "main", action: str = "add", repository_url: str = "") -> str:
    """Configures, registers, or modifies tracking targets for the background git_watcher agent, supporting dynamic system args."""
    # Fallback capture if framework routes parameters into unexpected kwargs
    target_path = repo_path if repo_path else repository_url
    clean_path = target_path.strip("'\"")
    config_file = "workspace/git_watcher_config.json"
    
    try:
        os.makedirs(os.path.dirname(config_file), exist_ok=True)
        
        if action.lower().strip() == "add":
            if not clean_path:
                return "[watch_repository] Error: No repository path or tracking URL was supplied."
                
            if not os.path.exists(clean_path):
                return f"[watch_repository] Error: The local path '{clean_path}' does not exist."
                
            git_dir = os.path.join(clean_path, ".git")
            if not os.path.exists(git_dir):
                return f"[watch_repository] Error: Path '{clean_path}' is not a valid Git repository initialization."
                
            config_data = {
                "repo_path": os.path.abspath(clean_path),
                "branch": branch.strip(),
                "last_seen_sha": ""
            }
            
            with open(config_file, "w", encoding="utf-8") as f:
                json.dump(config_data, f, indent=4)
                
            return f"[watch_repository] Successfully registered tracking route for branch '{branch}' at: {config_data['repo_path']}"
            
        elif action.lower().strip() == "remove":
            if os.path.exists(config_file):
                os.remove(config_file)
                return "[watch_repository] Removed active repository tracking profile from file configurations."
            return "[watch_repository] No active configuration found to remove."
            
        return f"[watch_repository] Invalid management action option specified: '{action}'"
        
    except Exception as e:
        return f"[watch_repository] Management pipeline broken down. Error: {str(e)}"


SKILLS = [
    {
        "name": "watch_repository",
        "description": "Registers, edits, or deletes targeted repository profiles monitored by the system git_watcher agent background thread. Safely maps path inputs.",
        "trigger_phrases": ["watch repo", "track repository", "monitor branch", "stop watching repository", "add git watcher destination", "track git url"],
        "func": watch_repository,
    },
]