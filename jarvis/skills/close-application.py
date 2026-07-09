import sys
import subprocess

def close_application(app_name: str) -> str:
    """Closes or terminates an active system process/application by its name."""
    app_name_lower = app_name.lower().strip()

    # Define standard process mappings to catch common names
    process_mapping = {
        "filezilla": "filezilla",
        "notepad": "notepad",
        "calculator": "calc",
        "chrome": "chrome",
        "browser": "chrome",
        "cmd": "cmd",
        "explorer": "explorer"
    }

    target_process = process_mapping.get(app_name_lower, app_name_lower)

    # Windows process termination
    if sys.platform == "win32":
        if not target_process.endswith(".exe") and target_process != "explorer":
            executable = f"{target_process}.exe"
        else:
            executable = target_process
            
        try:
            # Using taskkill to gracefully close or force close on Windows
            result = subprocess.run(
                ["taskkill", "/IM", executable, "/F"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if "SUCCESS" in result.stdout:
                return f"[close_application] Successfully terminated {app_name} ({executable})."
            elif "not found" in result.stderr:
                return f"[close_application] Application '{app_name}' ({executable}) was not found running."
            else:
                return f"[close_application] System reported: {result.stderr.strip()}"
        except Exception as e:
            return f"[close_application] Failed to close '{app_name}' on Windows. Error: {str(e)}"

    # Linux / macOS process termination fallback
    else:
        try:
            # Fallback to killall if pkill caused issues previously
            result = subprocess.run(
                ["killall", "-9", target_process],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            if result.returncode == 0:
                return f"[close_application] Successfully terminated process: {target_process}."
            else:
                return f"[close_application] Could not find or terminate process: {target_process}."
        except FileNotFoundError:
            try:
                subprocess.run(["pkill", "-f", target_process])
                return f"[close_application] Executed pkill sequence against '{target_process}'."
            except Exception as e:
                return f"[close_application] Failed to execute kill sequence on Unix. Error: {str(e)}"


SKILLS = [
    {
        "name": "close_application",
        "description": "Closes, kills, or terminates open running desktop applications like FileZilla, Notepad, or Chrome by name.",
        "trigger_phrases": ["close", "kill", "terminate", "exit application", "stop"],
        "func": close_application,
    },
]