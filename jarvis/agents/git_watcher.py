import os
import subprocess

def git_watcher() -> str:
    """Monitors local git repository branches for new commits by comparing local heads against remote targets."""
    # Central config track or local repo environment check
    repo_config_file = "workspace/git_watcher_config.json"
    
    if not os.path.exists(repo_config_file):
        return ""  # Idle pass if tracking configuration file layout is not initialized
        
    try:
        import json
        with open(repo_config_file, "r", encoding="utf-8") as f:
            config = json.load(f)
            
        repo_path = config.get("repo_path", "").strip("'\"")
        branch = config.get("branch", "main")
        last_seen_sha = config.get("last_seen_sha", "")
        
        if not repo_path or not os.path.exists(repo_path):
            return f"[git_watcher] Error: Configured repository path '{repo_path}' is invalid or missing."
            
        # Execute git commands inside target repository environment path
        # Fetch latest state from remote without merging
        subprocess.run(["git", "fetch"], cwd=repo_path, capture_output=True, text=True, check=True)
        
        # Get current tracking branch commit hash SHA reference
        result = subprocess.run(
            ["git", "rev-parse", f"origin/{branch}"], 
            cwd=repo_path, capture_output=True, text=True, check=True
        )
        current_sha = result.stdout.strip()
        
        # Initial run initialization configuration capture
        if not last_seen_sha:
            config["last_seen_sha"] = current_sha
            with open(repo_config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)
            return f"[git_watcher] Initialization complete. Tracking branch 'origin/{branch}' starting at commit {current_sha[:7]}."
            
        # Code structure change detection logic
        if current_sha != last_seen_sha:
            # Extract log details of commits since last check iteration sequence
            log_result = subprocess.run(
                ["git", "log", f"{last_seen_sha}..{current_sha}", "--oneline"],
                cwd=repo_path, capture_output=True, text=True, check=True
            )
            commit_logs = log_result.stdout.strip()
            
            # Update configuration file context memory layout
            config["last_seen_sha"] = current_sha
            with open(repo_config_file, "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)
                
            return f"[git_watcher] New code activity detected on 'origin/{branch}':\n{commit_logs}"
            
        return ""  # No new changes detected on tracking layout frame
        
    except subprocess.CalledProcessError as e:
        return f"[git_watcher] Git operation failure execution error: {e.stderr.strip()}"
    except Exception as e:
        return f"[git_watcher] Tracking pipeline error breakdown. Error: {str(e)}"


AGENTS = [
    {
        "name": "git_watcher",
        "description": "Monitors remote Git branch layouts at intervals to identify incoming commits and output structured update summaries.",
        "interval": 60,
        "enabled": True,
        "func": git_watcher,
    }
]