import sys
import subprocess
import webbrowser

def open_application(app_name: str) -> str:
    """Opens a web application or a local system application based on the name provided."""
    app_name_lower = app_name.lower().strip()

    # Web-based shortcuts
    web_apps = {
        "youtube": "https://www.youtube.com",
        "google": "https://www.google.com",
        "github": "https://www.github.com",
    }

    if app_name_lower in web_apps:
        webbrowser.open(web_apps[app_name_lower])
        return f"[open_application] Successfully opened {app_name} in the default web browser."

    # Windows native execution
    if sys.platform == "win32":
        win_apps = {
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "cmd": "cmd.exe",
            "explorer": "explorer.exe",
        }
        if app_name_lower in win_apps:
            subprocess.Popen([win_apps[app_name_lower]])
            return f"[open_application] Successfully launched local application: {app_name}."
        
        # Fallback to Windows 'start' command for general items/URLs
        try:
            subprocess.Popen(f"start {app_name}", shell=True)
            return f"[open_application] Attempted to launch '{app_name}' via Windows system shell."
        except Exception as e:
            return f"[open_application] Failed to launch '{app_name}'. Error: {str(e)}"

    # Linux native execution fallback (fixing the xdg-open issue on Windows)
    else:
        try:
            subprocess.Popen([app_name_lower], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            return f"[open_application] Successfully launched local application: {app_name}."
        except FileNotFoundError:
            try:
                subprocess.Popen(["xdg-open", app_name])
                return f"[open_application] Handled target via xdg-open."
            except Exception as e:
                return f"[open_application] Failed to execute target on Linux. Error: {str(e)}"


SKILLS = [
    {
        "name": "open_application",
        "description": "Opens designated local applications or websites like YouTube, Notepad, or Google by name.",
        "trigger_phrases": ["open", "launch", "start up", "go to website"],
        "func": open_application,
    },
]