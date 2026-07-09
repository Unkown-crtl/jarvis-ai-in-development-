import os
import subprocess
import json

def get_branches(repo_path: str = "", repository_url: str = "") -> str:
    """Queries a git repository to list all tracking branches, automatically cloning remote URLs if needed."""
    target_url = repository_url.strip("'\"") if repository_url else ""
    clean_path = repo_path.strip("'\"") if repo_path else ""
    config_file = "workspace/git_watcher_config.json"
    
    # Try to resolve path from active config if everything else is blank
    if not clean_path and not target_url and os.path.exists(config_file):
        try:
            with open(config_file, "r", encoding="utf-8") as f:
                config = json.load(f)
                clean_path = config.get("repo_path", "").strip("'\"")
        except Exception:
            pass

    # If given a URL directly or as a fallback path string
    if target_url or clean_path.startswith(("http://", "https://", "git@")):
        url_to_use = target_url if target_url else clean_path
        repo_name = url_to_use.split("/")[-1].replace(".git", "")
        workspace_dir = os.path.abspath("workspace")
        os.makedirs(workspace_dir, exist_ok=True)
        local_target = os.path.join(workspace_dir, repo_name)
        
        # Auto-clone fallback if repository does not exist locally yet
        if not os.path.exists(local_target):
            try:
                subprocess.run(
                    ["git", "clone", url_to_use, local_target],
                    capture_output=True, text=True, check=True, timeout=90
                )
            except subprocess.CalledProcessError as e:
                return f"[get_branches] Automated clone failure for remote URL: {e.stderr.strip()}"
            except Exception as e:
                return f"[get_branches] Cloning routine failure. Error: {str(e)}"
                
        clean_path = local_target

    if not clean_path or not os.path.exists(clean_path):
        return f"[get_branches] Error: Target repository context path '{clean_path}' could not be resolved."

    git_dir = os.path.join(clean_path, ".git")
    if not os.path.exists(git_dir):
        return f"[get_branches] Error: Path '{clean_path}' is missing its .git structural directory layout."

    try:
        # Fetch latest state from remote tracking layout branches
        subprocess.run(["git", "fetch", "--prune"], cwd=clean_path, capture_output=True, text=True, check=True)
        
        # Extract branch arrays
        result = subprocess.run(
            ["git", "branch", "-a"], 
            cwd=clean_path, capture_output=True, text=True, check=True
        )
        
        raw_branches = result.stdout.splitlines()
        branches = []
        for b in raw_branches:
            clean_b = b.replace("*", "").strip()
            if clean_b and "->" not in clean_b:
                branches.append(clean_b)
                
        branch_list_str = "\n".join([f"- {br}" for br in branches])
        return f"[get_branches] Active branch tracking list for '{os.path.basename(clean_path)}':\n{branch_list_str}"
        
    except subprocess.CalledProcessError as e:
        return f"[get_branches] Git core command failed execution: {e.stderr.strip()}"
    except Exception as e:
        return f"[get_branches] Verification framework failure. Error: {str(e)}"


SKILLS = [
    {
        "name": "get_branches",
        "description": "Queries a Git repository and lists all branches. Automatically pulls down and clones remote target URLs into the local workspace layout.",
        "trigger_phrases": ["get branches", "list branches", "show git branches", "what branches are in that repository", "check branches"],
        "func": get_branches,
    },
]