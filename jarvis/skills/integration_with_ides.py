import os
import sys
import subprocess

def integration_with_ides(ide_name: str, project_path: str = "") -> str:
    """Launches or integrates with target IDEs (VS Code, IntelliJ, Eclipse) opening specified project directories."""
    ide_lower = ide_name.lower().strip()
    target_path = project_path.strip("'\"") if project_path else os.getcwd()
    
    if project_path and not os.path.exists(target_path):
        return f"[integration_with_ides] Error: Specified project path '{target_path}' does not exist."

    # Windows Integration Layouts
    if sys.platform == "win32":
        if "code" in ide_lower or "vs" in ide_lower:
            try:
                subprocess.Popen(["code", target_path], shell=True)
                return f"[integration_with_ides] Successfully opened Visual Studio Code at: {target_path}"
            except Exception:
                return "[integration_with_ides] Failed to trigger 'code' command. Ensure VS Code is added to your environment PATH."
                
        elif "intellij" in ide_lower or "idea" in ide_lower:
            # Common default paths for community and ultimate editions
            possible_paths = [
                os.path.expandvars(r"%PROGRAMFILES%\JetBrains\IntelliJ IDEA Community Edition *\bin\idea64.exe"),
                os.path.expandvars(r"%PROGRAMFILES%\JetBrains\IntelliJ IDEA *\bin\idea64.exe"),
            ]
            import glob
            for path_mask in possible_paths:
                found = glob.glob(path_mask)
                if found:
                    subprocess.Popen([found[0], target_path])
                    return f"[integration_with_ides] Successfully opened IntelliJ IDEA at: {target_path}"
            return "[integration_with_ides] IntelliJ IDEA executable path could not be located automatically."

        elif "eclipse" in ide_lower:
            try:
                subprocess.Popen(["eclipse", "-data", target_path], shell=True)
                return f"[integration_with_ides] Attempted to launch Eclipse Workspace at: {target_path}"
            except Exception as e:
                return f"[integration_with_ides] Failed to execute Eclipse execution thread. Error: {str(e)}"

    # Linux / macOS Fallback Execution
    else:
        if "code" in ide_lower or "vs" in ide_lower:
            try:
                subprocess.Popen(["code", target_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return f"[integration_with_ides] Safely deployed VS Code instance for environment context: {target_path}"
            except FileNotFoundError:
                return "[integration_with_ides] 'code' binary not found in Unix path environment."
        else:
            try:
                subprocess.Popen([ide_lower, target_path], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                return f"[integration_with_ides] Fired execution sequence for binary tool: {ide_name}"
            except FileNotFoundError:
                return f"[integration_with_ides] Requested terminal app structure '{ide_name}' was not found."

    return f"[integration_with_ides] IDE environment target '{ide_name}' matches no specific layout handler."


SKILLS = [
    {
        "name": "integration_with_ides",
        "description": "Opens specified directories, code frameworks, or workspaces directly into development tools like VS Code, IntelliJ, or Eclipse.",
        "trigger_phrases": ["open ide", "open in vs code", "launch intellij", "start eclipse workspace", "ide workspace"],
        "func": integration_with_ides,
    },
]