import sys

def static_code_analysis(file_path: str) -> str:
    """Analyze Python source code files for syntax issues, complexity, and styling standards."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            code = f.read()
    except Exception as e:
        return f"[static_code_analysis] Error opening file: {str(e)}"

    issues = []
    
    # 1. Syntax Check using built-in compile
    try:
        compile(code, file_path, "exec")
    except SyntaxError as se:
        return f"[static_code_analysis] Critical Syntax Error found:\nLine {se.lineno}: {se.msg}\nCode snippet: {se.text.strip() if se.text else ''}"

    lines = code.splitlines()
    for idx, line in enumerate(lines, start=1):
        # 2. Simple Style / Compliance Check (PEP 8 line length limits)
        if len(line) > 79:
            issues.append(f"Line {idx}: Line too long ({len(line)}/79 chars).")
            
        # 3. Security Vulnerability Check: Dangerous built-in evaluations
        if "eval(" in line and not line.strip().startswith("#"):
            issues.append(f"Line {idx}: Security Hazard - Use of 'eval()' detected.")
        if "exec(" in line and not line.strip().startswith("#"):
            issues.append(f"Line {idx}: Security Hazard - Use of 'exec()' detected.")
            
        # 4. Coding Standards Compliance Check: Bare except handlers
        if "except:" in line.replace(" ", "") and not line.strip().startswith("#"):
            issues.append(f"Line {idx}: Coding Standard Warning - Bare 'except:' clause used.")

    if not issues:
        return f"[static_code_analysis] Analysis finished for '{file_path}'. No syntax errors, bare exceptions, dangerous evaluators, or PEP8 line lengths violations detected."
    
    issues_summary = "\n".join(issues)
    return f"[static_code_analysis] Issues found in '{file_path}':\n{issues_summary}"


SKILLS = [
    {
        "name": "static_code_analysis",
        "description": "Analyze code for potential issues, security vulnerabilities, and coding standards compliance.",
        "trigger_phrases": [
            "analyze code",
            "check code quality",
            "static analysis",
            "find code vulnerabilities",
            "pep8 compliance",
            "scan script for bugs"
        ],
        "func": static_code_analysis,
    },
]