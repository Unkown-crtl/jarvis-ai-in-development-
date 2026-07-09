"""
Desktop Control Skills
- Open applications
- Take screenshots
- Search the web
- Run shell commands
- Get system info
"""
import os
import platform
import subprocess
import webbrowser
import datetime


def open_app(app: str, **kwargs) -> str:
    sys = platform.system()
    try:
        if sys == "Darwin":
            subprocess.Popen(["open", "-a", app])
        elif sys == "Windows":
            os.startfile(app)
        else:  # Linux
            subprocess.Popen([app])
        return f"Opened {app}."
    except Exception as e:
        return f"Could not open {app}: {e}"


def take_screenshot(filename: str = "", **kwargs) -> str:
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    name = filename or f"screenshot_{ts}.png"
    try:
        import pyautogui
        pyautogui.screenshot(name)
        return f"Screenshot saved to {name}"
    except ImportError:
        return "pyautogui not installed. Run: pip install pyautogui"
    except Exception as e:
        return f"Screenshot failed: {e}"


def search_web(query: str, **kwargs) -> str:
    url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
    webbrowser.open(url)
    return f"Opened browser: {url}"


def run_command(command: str, **kwargs) -> str:
    try:
        result = subprocess.run(
            command, shell=True, capture_output=True, text=True, timeout=15
        )
        out = result.stdout.strip() or result.stderr.strip()
        return out or f"Command ran (exit {result.returncode})"
    except subprocess.TimeoutExpired:
        return "Command timed out."
    except Exception as e:
        return f"Error: {e}"


def get_system_info(**kwargs) -> str:
    import platform
    try:
        import psutil
        cpu = psutil.cpu_percent(interval=0.5)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        return (f"CPU: {cpu}% | "
                f"RAM: {mem.percent}% used ({mem.available // 1024**2} MB free) | "
                f"Disk: {disk.percent}% used ({disk.free // 1024**3} GB free)")
    except ImportError:
        return f"OS: {platform.system()} {platform.release()} | psutil not installed (pip install psutil)"


def get_time(**kwargs) -> str:
    now = datetime.datetime.now()
    return now.strftime("It's %A, %B %d %Y — %H:%M:%S")


def open_url(url: str, **kwargs) -> str:
    webbrowser.open(url)
    return f"Opened: {url}"


def write_file(path: str, content: str, **kwargs) -> str:
    try:
        with open(path, "w") as f:
            f.write(content)
        return f"File written: {path}"
    except Exception as e:
        return f"Write failed: {e}"


def read_file(path: str, **kwargs) -> str:
    try:
        with open(path) as f:
            return f.read()[:2000]
    except Exception as e:
        return f"Read failed: {e}"


SKILLS = [
    {
        "name": "open_app",
        "description": "Open a desktop application by name.",
        "trigger_phrases": ["open ", "launch ", "start "],
        "func": open_app,
    },
    {
        "name": "take_screenshot",
        "description": "Take a screenshot of the current screen.",
        "trigger_phrases": ["screenshot", "capture screen"],
        "func": take_screenshot,
    },
    {
        "name": "search_web",
        "description": "Search Google for a query in the browser.",
        "trigger_phrases": ["search for", "google", "look up"],
        "func": search_web,
    },
    {
        "name": "run_command",
        "description": "Run a shell command and return the output.",
        "trigger_phrases": ["run command", "execute", "terminal"],
        "func": run_command,
    },
    {
        "name": "get_system_info",
        "description": "Get CPU, RAM, and disk usage stats. Safely handles unexpected automated parameters.",
        "trigger_phrases": ["system info", "cpu", "memory", "disk"],
        "func": get_system_info,
    },
    {
        "name": "get_time",
        "description": "Get the current date and time.",
        "trigger_phrases": ["what time", "current time", "what's the date"],
        "func": get_time,
    },
    {
        "name": "open_url",
        "description": "Open a specific URL in the default browser.",
        "trigger_phrases": ["open url", "go to", "visit"],
        "func": open_url,
    },
    {
        "name": "write_file",
        "description": "Write content to a file at the given path.",
        "trigger_phrases": ["write file", "save file", "create file"],
        "func": write_file,
    },
    {
        "name": "read_file",
        "description": "Read and return the content of a file.",
        "trigger_phrases": ["read file", "show file", "open file"],
        "func": read_file,
    },
]