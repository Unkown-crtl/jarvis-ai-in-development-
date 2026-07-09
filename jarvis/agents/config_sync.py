import os
import shutil
import json

def config_sync() -> str:
    """Synchronizes system profile configurations, environment parameters, and dotfiles across a centralized repository."""
    sync_config_file = "workspace/config_sync_manifest.json"
    
    if not os.path.exists(sync_config_file):
        return ""  # Idle pass if the synchronization tracking manifest does not exist
        
    try:
        with open(sync_config_file, "r", encoding="utf-8") as f:
            manifest = json.load(f)
            
        sync_directory = manifest.get("sync_directory", "").strip("'\"")
        tracked_files = manifest.get("tracked_files", [])  # List of dicts: {"source": "...", "target_name": "..."}
        
        if not sync_directory or not os.path.exists(sync_directory):
            return f"[config_sync] Error: Targeted synchronization directory '{sync_directory}' cannot be resolved."
            
        sync_logs = []
        changes_made = False
        
        for item in tracked_files:
            source = os.path.expandvars(item.get("source", "")).strip("'\"")
            target_name = item.get("target_name", "").strip("'\"")
            
            if not source or not os.path.exists(source) or os.path.isdir(source):
                continue  # Skip files that are unresolvable or point to directories
                
            destination_path = os.path.join(sync_directory, target_name)
            
            # Create subdirectories if specified within target names
            dest_dir = os.path.dirname(destination_path)
            if dest_dir and not os.path.exists(dest_dir):
                os.makedirs(dest_dir, exist_ok=True)
                
            # Check if the file needs updating by comparing modifications
            should_copy = True
            if os.path.exists(destination_path):
                source_mtime = os.path.getmtime(source)
                dest_mtime = os.path.getmtime(destination_path)
                if source_mtime <= dest_mtime:
                    should_copy = False
                    
            if should_copy:
                shutil.copy2(source, destination_path)
                sync_logs.append(f"Updated: {target_name}")
                changes_made = True
                
        if changes_made:
            return f"[config_sync] Synchronized local profile profiles to central layout:\n" + "\n".join(sync_logs)
            
        return ""  # Configurations remain in complete alignment
        
    except Exception as e:
        return f"[config_sync] Failed executing synchronization loop. Error: {str(e)}"


AGENTS = [
    {
        "name": "config_sync",
        "description": "Monitors changes across development profile settings and environment parameters, syncing them with a centralized backup layout.",
        "interval": 600,
        "enabled": True,
        "func": config_sync,
    }
]