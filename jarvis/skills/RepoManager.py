import json


def manage_repo_branches(
    action: str,
    repo_name: str,
    branch_name: str,
    target_branch: str = "main",
) -> str:
    """Manages GitHub repository branching strategies including creation, tracking status updates, destruction, or merges."""
    if not repo_name or not branch_name:
        return "[repo_manager] Error: Parameters 'repo_name' and 'branch_name' are required."

    action = action.lower().strip()
    branch_clean = branch_name.strip()
    target_clean = target_branch.strip()

    # Isolated repository simulator track
    mock_active_branches = ["main", "dev", "feature/auth", "staging"]

    try:
        if action == "create":
            if branch_clean in mock_active_branches:
                return f"[repo_manager] Error: Branch '{branch_clean}' already exists in '{repo_name}'."
            
            payload = {
                "repository": repo_name,
                "action": "branch_creation",
                "new_branch": branch_clean,
                "upstream_source": target_clean,
                "status": "Success"
            }
            return f"[repo_manager] Operational branch update: {json.dumps(payload)}"

        elif action == "update":
            payload = {
                "repository": repo_name,
                "action": "branch_metadata_update",
                "target_branch": branch_clean,
                "tracking_status": "Synchronized with remote tracking origin",
                "status": "Success"
            }
            return f"[repo_manager] Operational branch update: {json.dumps(payload)}"

        elif action == "delete":
            if branch_clean in ["main", "master", "prod"]:
                return f"[repo_manager] Error: Deleting protected administrative branch '{branch_clean}' is prohibited."
            
            payload = {
                "repository": repo_name,
                "action": "branch_deletion",
                "deleted_branch": branch_clean,
                "status": "Success"
            }
            return f"[repo_manager] Operational branch update: {json.dumps(payload)}"

        elif action == "merge":
            payload = {
                "repository": repo_name,
                "action": "branch_merge_transaction",
                "source_branch": branch_clean,
                "destination_branch": target_clean,
                "merge_strategy": "three-way merge",
                "status": "Success"
            }
            return f"[repo_manager] Operational branch update: {json.dumps(payload)}"

        else:
            return f"[repo_manager] Error: Unsupported branch operation action '{action}'. Use create, update, delete, or merge."

    except Exception as e:
        return f"[repo_manager] Fatal exception processing transaction endpoints: {str(e)}"


SKILLS = [
    {
        "name": "repo_manager",
        "description": "Manages GitHub repository branch states by processing creation, updates, deletions, and merge routines.",
        "trigger_phrases": [
            "manage repository branches",
            "create branch github",
            "delete git branch",
            "merge branches",
            "update github branch",
            "repo manager",
            "git merge tool",
        ],
        "func": manage_repo_branches,
    },
]