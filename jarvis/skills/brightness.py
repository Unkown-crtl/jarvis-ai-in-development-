import platform
import subprocess


def control_brightness(level: int) -> str:
    """Adjusts visual monitor brightness percentage bounds."""
    sys = platform.system()
    if level < 0 or level > 100:
        return "Brightness level must remain balanced between 0 and 100."

    try:
        if sys == "Windows":
            cmd = f"Get-CimInstance -Namespace root/WMI -ClassName WmiMonitorBrightnessMethods | Invoke-CimMethod -MethodName WmiSetBrightness -Arguments @{{Timeout = 1; Brightness = {level}}}"
            subprocess.run(["powershell", "-Command", cmd], capture_output=True)
            return f"Brightness set to {level}%."

        elif sys == "Darwin":
            scaled = level / 100
            script = f'tell application "System Events" to repeat with i from 1 to count of displays\nset brightness of display i to {scaled}\nend repeat'
            subprocess.run(["osascript", "-e", script], capture_output=True)
            return f"Brightness modified to {level}% via AppleScript target."

        elif sys == "Linux":
            res = subprocess.run(
                "xrandr | grep ' connected' | awk '{print $1}'",
                shell=True,
                capture_output=True,
                text=True,
            )
            output_device = res.stdout.strip().split("\n")[0]
            if output_device:
                scaled = level / 100
                subprocess.run(
                    ["xrandr", "--output", output_device, "--brightness", str(scaled)],
                    capture_output=True,
                )
                return f"Brightness set to {level}% on {output_device}."

        return "Brightness configuration failed or unsupported on this host OS setup."
    except Exception as e:
        return f"Brightness adjustment failed: {e}"


SKILLS = [
    {
        "name": "control_brightness",
        "description": "Change display back-light monitoring visibility brightness.",
        "trigger_phrases": ["set brightness", "dim screen", "make screen brighter"],
        "func": control_brightness,
    },
]