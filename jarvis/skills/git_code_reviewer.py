import json


def review_code(
    file_path: str,
    code_content: str,
    programming_language: str = "python",
) -> str:
    """Reviews code files for quality, security vulnerabilities, performance optimization, and maintainability metrics."""
    if not file_path or not code_content:
        return "[code_reviewer] Error: Both 'file_path' and 'code_content' are required parameters."

    lang_clean = programming_language.lower().strip()
    code_lower = code_content.lower()

    # Diagnostic state tracking collections
    issues = []
    security_flags = 0
    performance_flags = 0
    maintainability_flags = 0

    # 1. Security Evaluation Layer
    security_checks = {
        "eval(": "Critical: Avoid using the 'eval()' function pattern as it permits dangerous arbitrary code execution injectors.",
        "exec(": "Critical: Avoid using 'exec()' statements due to severe shell injection vulnerability surface vulnerabilities.",
        "password =": "Warning: Hardcoded string credential assignment detected. Migrate sensitive keys to protected environmental variables.",
        "secret =": "Warning: Potential hardcoded secret exposure. Keep security configuration files decoupled from open version control.",
    }
    for marker, description in security_checks.items():
        if marker in code_lower:
            issues.append({"category": "Security", "severity": "High", "description": description})
            security_flags += 1

    # 2. Performance Evaluation Layer
    if lang_clean == "python":
        if "for" in code_lower and ".append(" in code_lower:
            issues.append({
                "category": "Performance",
                "severity": "Low",
                "description": "Optimization: Consider refactoring manual iterative element assignment patterns into structured list comprehensions for faster execution loops."
            })
            performance_flags += 1
        if "global " in code_lower:
            issues.append({
                "category": "Performance",
                "severity": "Medium",
                "description": "Optimization: Reduce namespace binding tracking overheads by avoiding global variable reference calls inside functional execution steps."
            })
            performance_flags += 1

    # 3. Maintainability / Style Verification
    if "except:" in code_lower or "except Exception:" in code_lower:
        issues.append({
            "category": "Maintainability",
            "severity": "Medium",
            "description": "Best Practice: Catching broad top-level exceptions masks unexpected functional faults. Declare narrow explicit handling targets."
        })
        maintainability_flags += 1
    if len(code_content.splitlines()) > 150:
        issues.append({
            "category": "Maintainability",
            "severity": "Low",
            "description": "Structure: File exceeds target modular length guidelines. Deconstruct complex components into separate individual modules."
        })
        maintainability_flags += 1

    # Synthesize diagnostic health weights
    total_issues = len(issues)
    health_score = max(10, 100 - (security_flags * 25) - (performance_flags * 10) - (maintainability_flags * 15))

    report = {
        "reviewed_target": file_path,
        "detected_language": lang_clean,
        "computed_health_score": f"{health_score}/100",
        "total_violations_found": total_issues,
        "detailed_findings": issues if issues else "No critical architectural violations detected. File adheres safely to operational quality standards."
    }

    return f"[code_reviewer] Static analytical code review complete: {json.dumps(report, ensure_ascii=False)}"


SKILLS = [
    {
        "name": "code_reviewer",
        "description": "Reviews code file payloads for architectural quality issues, security vulnerabilities, and code performance optimization.",
        "trigger_phrases": [
            "review code",
            "code review",
            "check code quality",
            "security audit code",
            "analyze repository file",
            "code static analysis",
            "reviewer tool",
        ],
        "func": review_code,
    },
]