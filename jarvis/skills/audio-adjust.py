import platform
import subprocess


def control_audio(action: str, volume_level: int = None) -> str:
    """Controls system volume and mute state across Windows, macOS, and Linux."""
    sys = platform.system()
    action = action.lower()

    try:
        if sys == "Windows":
            if action == "mute":
                subprocess.run(
                    [
                        "powershell",
                        "-Command",
                        "(New-Object -ComObject WScript.Shell).SendKeys([char]173)",
                    ],
                    capture_output=True,
                )
                return "Toggled mute state."
            elif action == "set" and volume_level is not None:
                return f"Volume set request to {volume_level}% (Requires 'pycaw' for precise Windows adjustments)."

        elif sys == "Darwin":
            if action == "mute":
                subprocess.run(
                    ["osascript", "-e", "set volume with muted"],
                    capture_output=True,
                )
                return "Muted system audio."
            elif action == "unmute":
                subprocess.run(
                    ["osascript", "-e", "set volume without muted"],
                    capture_output=True,
                )
                return "Unmuted system audio."
            elif action == "set" and volume_level is not None:
                scaled = round((volume_level / 100) * 7)
                subprocess.run(
                    ["osascript", "-e", f"set volume {scaled}"],
                    capture_output=True,
                )
                return f"Volume set to {volume_level}%."

        elif sys == "Linux":
            if action == "mute":
                subprocess.run(
                    ["amixer", "-D", "pulse", "sset", "Master", "mute"],
                    capture_output=True,
                )
                return "Muted system audio."
            elif action == "unmute":
                subprocess.run(
                    ["amixer", "-D", "pulse", "sset", "Master", "unmute"],
                    capture_output=True,
                )
                return "Unmuted system audio."
            elif action == "set" and volume_level is not None:
                subprocess.run(
                    [
                        "amixer",
                        "-D",
                        "pulse",
                        "sset",
                        "Master",
                        f"{volume_level}%",
                    ],
                    capture_output=True,
                )
                return f"Volume set to {volume_level}%."

        return "Audio action not recognized or unsupported on this OS."
    except Exception as e:
        return f"Audio control failed: {e}"


SKILLS = [
    {
        "name": "control_audio",
        "description": "Mute, unmute or set the audio volume level.",
        "trigger_phrases": ["mute", "unmute", "set volume", "change volume"],
        "func": control_audio,
    },
]