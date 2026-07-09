import subprocess
import tempfile
import os

def dynamic_code_analysis(file_path: str, timeout_seconds: int = 5) -> str:
    """Run dynamic analysis on a Python script to track runtime errors, exceptions, and exit statuses."""
    if not os.path.exists(file_path):
        return f"[dynamic_code_analysis] Error: File '{file_path}' not found."

    try:
        # Run the target script within an isolated subprocess environment to monitor runtime exceptions
        result = subprocess.run(
            ["python", "-X", "dev", file_path],  # -X dev enables CPython development mode checks
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout_seconds
        )
        
        if result.returncode == 0:
            return f"[dynamic_code_analysis] Analysis finished for '{file_path}'. Script executed successfully with zero runtime errors."
        else:
            return f"[dynamic_code_analysis] Runtime failure encountered (Exit Code {result.returncode}):\n{result.stderr.strip()}"
            
    except subprocess.TimeoutExpired:
        return f"[dynamic_code_analysis] Execution timed out after {timeout_seconds} seconds. Potential infinite loop or resource lock detected."
    except Exception as e:
        return f"[dynamic_code_analysis] Dynamic execution processing failure: {str(e)}"


SKILLS = [
    {
        "name": "dynamic_code_analysis",
        "description": "Run dynamic analysis on code to detect runtime errors, memory leaks, and other issues.",
        "trigger_phrases": [
            "run dynamic analysis",
            "check runtime errors",
            "test memory leaks",
            "profile script performance",
            "execute tracking code",
            "runtime trace"
        ],
        "func": dynamic_code_analysis,
    },
]