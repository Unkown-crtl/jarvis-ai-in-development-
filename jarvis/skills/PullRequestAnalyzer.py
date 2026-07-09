import json


def analyze_pull_request(
    repo_name: str,
    pr_id: int,
    diff_content: str = "",
    title: str = "",
) -> str:
    """Analyzes pull request diffs, titles, and structural data to find bugs, issues, and optimizations."""
    if not repo_name or not pr_id:
        return "[pr_analyzer] Error: Parameters 'repo_name' and 'pr_id' are required."

    findings = []
    has_bugs = False
    has_tests = False

    # Check for context validation markers in the title or diff contents
    combined_context = f"{title} {diff_content}".lower()

    if "fix" in combined_context or "bug" in combined_context:
        findings.append({
            "type": "Context Match",
            "severity": "Info",
            "message": "PR explicitly targets an issue or bug fix. Cross-reference linked issue IDs."
        })

    # Run static pattern parsing on code diff strings
    if diff_content:
        diff_lines = diff_content.splitlines()
        
        # Track if verification test definitions are included in the change vectors
        if any(
            "test_" in line or "import pytest" in line or "unittest" in line 
            for line in diff_lines if line.startswith("+")
        ):
            has_tests = True

        for line_num, line in enumerate(diff_lines, start=1):
            if not line.startswith("+"):
                continue
            
            # Catch raw print logs left behind
            if "print(" in line and "logger." not in line:
                findings.append({
                    "type": "Code Quality",
                    "severity": "Warning",
                    "message": f"Line {line_num}: Stray print statement found. Use production logging frameworks instead."
                })

            # Catch common raw equality comparisons against None variables
            if "== None" in line:
                findings.append({
                    "type": "Style / Best Practice",
                    "severity": "Low",
                    "message": f"Line {line_num}: Style mismatch. Use 'is None' instead of '== None' for identity comparisons."
                })

            # Check for generic exception catching blocks
            if "except:" in line or "except Exception:" in line:
                findings.append({
                    "type": "Robustness / Bug Risk",
                    "severity": "Medium",
                    "message": f"Line {line_num}: Broad exception handling block can mask silent control flow errors."
                })
                has_bugs = True

    # Enforce unit verification best practices if structural modules were touched
    if diff_content and not has_tests:
        findings.append({
            "type": "Verification Coverage",
            "severity": "Medium",
            "message": "No accompanying unit testing files or assertions detected within the diff modifications."
        })

    analysis_report = {
        "repository": repo_name,
        "pull_request_number": pr_id,
        "title_context": title if title else "Untitled PR Context",
        "potential_risk_detected": has_bugs,
        "automated_findings": findings if findings else ["No immediate functional risks or regressions found. Branch is clean."]
    }

    return f"[pr_analyzer] Pull Request evaluation complete: {json.dumps(analysis_report, ensure_ascii=False)}"


SKILLS = [
    {
        "name": "pr_analyzer",
        "description": "Analyzes pull request parameters and code diffs to isolate risks, structural bugs, and quality improvements.",
        "trigger_phrases": [
            "analyze pull request",
            "review pr",
            "pull request analysis",
            "check pr diff",
            "find bugs in pr",
            "pr reviewer tool",
            "analyze pr code changes",
        ],
        "func": analyze_pull_request,
    },
]