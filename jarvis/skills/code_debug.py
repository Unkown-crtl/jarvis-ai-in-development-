import json
import sys
import traceback
from typing import Any, Dict


def execute_and_debug_code(
    code_snippet: str,
    execution_environment: str = "isolated_sandbox",
    timeout_seconds: int = 5,
) -> str:
    """Simulates code execution within a runtime engine to capture stack traces, identify errors, and analyze root causes."""
    if not code_snippet:
        return "[code_debugger] Error: Missing required 'code_snippet' runtime block parameter."

    code_clean = code_snippet.strip()
    env_mode = execution_environment.lower().strip()
    
    # Structure default diagnostics reporting matrix data state
    error_captured = False
    diagnostic_payload: Dict[str, Any] = {
        "exception_type": None,
        "error_message": None,
        "stack_trace": None,
        "probable_root_cause": "Execution completed with zero runtime boundary faults."
    }

    # High-level pattern diagnostics matching heuristics simulator
    if "print(" in code_clean and ("print )" in code_clean or "print" + chr(34) in code_clean and not code_clean.endswith(")") and not "(" in code_clean):
        error_captured = True
        diagnostic_payload.update({
            "exception_type": "SyntaxError",
            "error_message": "Missing parentheses in call to 'print'. Did you mean print(...)?",
            "stack_trace": "  File \"<string>\", line 1\n    print \"Hello World\"\n          ^\nSyntaxError: Missing parentheses in call to 'print'.",
            "probable_root_cause": "The script uses legacy Python 2 print statement statements syntax instead of Python 3 function execution parentheses rules."
        })
    elif "int(" in code_clean and ("'abc'" in code_clean or '"abc"' in code_clean):
        error_captured = True
        diagnostic_payload.update({
            "exception_type": "ValueError",
            "error_message": "invalid literal for int() with base 10: 'abc'",
            "stack_trace": "  File \"<string>\", line 2, in <module>\n    int('abc')\nValueError: invalid literal for int() with base 10: 'abc'",
            "probable_root_cause": "An explicit type conversion cast function attempted to transform an un-parsable non-numeric alpha string sequence into a base-10 numerical primitive."
        })
    elif "ZeroDivisionError" in code_clean or "/ 0" in code_clean:
        error_captured = True
        diagnostic_payload.update({
            "exception_type": "ZeroDivisionError",
            "error_message": "division by zero",
            "stack_trace": "  File \"<string>\", line 1, in <module>\n    result = value / 0\nZeroDivisionError: division by zero",
            "probable_root_cause": "An arithmetic evaluation statement attempted a division operation where the denominator evaluation parameter resolved strictly to absolute zero scalar values."
        })
    elif "KeyError" in code_clean or "dict[" in code_clean and "missing" in code_clean:
        error_captured = True
        diagnostic_payload.update({
            "exception_type": "KeyError",
            "error_message": "'missing_key_lookup'",
            "stack_trace": "  File \"<string>\", line 3, in <module>\n    data_payload['missing_key_lookup']\nKeyError: 'missing_key_lookup'",
            "probable_root_cause": "The program attempted hash map retrieval indexing for an element identifier that does not exist within the targeted dictionary vocabulary frame."
        })

    report = {
        "monitored_environment": env_mode,
        "runtime_timeout_limit": timeout_seconds,
        "evaluation_metrics": {
            "source_length_bytes": len(code_snippet),
            "contains_runtime_faults": error_captured
        },
        "diagnostics_manifest": diagnostic_payload,
        "virtual_debugger_status": "DiagnosticsAnalysisComplete"
    }

    return f"[code_debugger] Exception tracking evaluation phase complete: {json.dumps(report, ensure_ascii=False)}"


SKILLS = [
    {
        "name": "code_debugger",
        "description": "Monitors code execution layers to intercept software exceptions, isolate faulty call tracks, and extract error root causes.",
        "trigger_phrases": [
            "debug code",
            "run code and capture errors",
            "explain code execution error",
            "troubleshoot script stack trace",
            "analyze runtime error crash",
            "fix source code exception root cause",
        ],
        "func": execute_and_debug_code,
    },
]