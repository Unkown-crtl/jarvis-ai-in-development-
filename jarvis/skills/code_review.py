import json


def review_code_for_issues(
    code_to_review: str,
    programming_language: str = "python",
    check_security: bool = True,
) -> str:
    """Reviews code structures for logical bugs, structural anti-patterns, and baseline security threat vectors."""
    if not code_to_review:
        return "[code_reviewer] Error: Missing required 'code_to_review' input parameter string."

    lang = programming_language.lower().strip()
    code_clean = code_to_review.strip()
    findings = []

    # Emulate localized abstract syntax tree checking patterns
    if lang == "python":
        if "except:" in code_clean or "except Exception:" in code_clean:
            if "pass" in code_clean:
                findings.append({
                    "severity": "Warning",
                    "category": "Anti-Pattern",
                    "description": "Silent exception handling detected via raw 'except: pass' sequence block."
                })
        if "eval(" in code_clean or "exec(" in code_clean:
            if check_security:
                findings.append({
                    "severity": "Critical",
                    "category": "Security Vulnerability",
                    "description": "Arbitrary code execution risk identified through primitive 'eval' or 'exec' invocation matrices."
                })
        if "input(" in code_clean and "int(" not in code_clean and check_security:
            findings.append({
                "severity": "Low",
                "category": "Input Sanitization",
                "description": "Unsanitized user-facing dynamic prompt execution risk found."
            })
    elif lang in ["javascript", "typescript"]:
        if "eval(" in code_clean and check_security:
            findings.append({
                "severity": "Critical",
                "category": "Security Vulnerability",
                "description": "Dynamic evaluation wrapper risk exposed via raw runtime 'eval()' function."
            })
        if "==" in code_clean and "===" not in code_clean:
            findings.append({
                "severity": "Medium",
                "category": "Type Coercion",
                "description": "Loose comparison operator '==' found. Prefer strict equality operator '===' matrix tracking."
            })

    # Fallback response profile if no deterministic violations triggered match vectors
    if not findings:
        findings.append({
            "severity": "Info",
            "category": "Static Analysis",
            "description": "No immediate critical validation errors or architectural design flaws matched standard heuristic matrices."
        })

    report = {
        "target_language_evaluated": lang,
        "security_deep_scan_enabled": check_security,
        "total_violations_flagged": len(findings) if findings[0]["severity"] != "Info" else 0,
        "review_findings_manifest": findings,
        "analysis_completion_status": "Success"
    }

    return f"[code_reviewer] Code review lifecycle processing complete: {json.dumps(report, ensure_ascii=False)}"


SKILLS = [
    {
        "name": "code_reviewer",
        "description": "Performs static syntax analysis scans to flag software bugs, security weaknesses, and structural code violations.",
        "trigger_phrases": [
            "review code",
            "check code for bugs",
            "find security issues in code",
            "audit script for bad practices",
            "analyze code quality patterns",
            "run code reviewer engine",
        ],
        "func": review_code_for_issues,
    },
]