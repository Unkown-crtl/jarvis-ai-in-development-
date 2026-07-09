import subprocess
import os

def unit_testing_frameworks(test_path: str, framework: str = "pytest") -> str:
    """Integrate with unit testing frameworks to run tests and analyze results."""
    if not os.path.exists(test_path):
        return f"[unit_testing_frameworks] Error: Path '{test_path}' does not exist."

    framework_lower = framework.lower()

    try:
        if framework_lower == "pytest":
            result = subprocess.run(
                ["pytest", test_path, "-v"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30
            )
            return f"[unit_testing_frameworks] Pytest results for '{test_path}':\n{result.stdout or result.stderr}"
            
        elif framework_lower == "junit":
            # Expecting path to a compiled JUnit runner or a Maven/Gradle configuration
            if os.path.isdir(test_path) and os.path.exists(os.path.join(test_path, "pom.xml")):
                cmd = ["mvn", "test", "-f", test_path]
            elif os.path.isdir(test_path) and os.path.exists(os.path.join(test_path, "build.gradle")):
                cmd = ["gradle", "test", "-p", test_path]
            else:
                return f"[unit_testing_frameworks] JUnit requires a valid Maven or Gradle directory path structure."
                
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=60
            )
            return f"[unit_testing_frameworks] JUnit/Build tool results for '{test_path}':\n{result.stdout or result.stderr}"
            
        else:
            return f"[unit_testing_frameworks] Framework '{framework}' is not directly supported. Choose 'pytest' or 'junit'."
            
    except subprocess.TimeoutExpired:
        return f"[unit_testing_frameworks] Test execution timed out."
    except Exception as e:
        return f"[unit_testing_frameworks] Execution error: {str(e)}"


SKILLS = [
    {
        "name": "unit_testing_frameworks",
        "description": "Integrate with unit testing frameworks such as JUnit or Pytest to help users write and run tests.",
        "trigger_phrases": [
            "run tests",
            "pytest framework",
            "junit test suite",
            "execute unit tests",
            "test coverage check",
            "run automated tests"
        ],
        "func": unit_testing_frameworks,
    },
]