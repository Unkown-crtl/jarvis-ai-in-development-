import json


def format_code_snippet(
    code_content: str,
    formatter_standard: str = "pep8",
    line_length_limit: int = 79,
) -> str:
    """Standardizes code syntax blocks according to styling specifications like PEP 8 or Prettier layout constraints."""
    if not code_content:
        return "[code_formatter] Error: Missing required 'code_content' input snippet text."

    standard = formatter_standard.lower().strip()
    
    if standard not in ["pep8", "prettier"]:
        return f"[code_formatter] Error: Styling framework standard '{formatter_standard}' is unsupported."

    lines = code_content.splitlines()
    formatted_lines = []

    for line in lines:
        stripped = line.strip()
        if not stripped:
            formatted_lines.append("")
            continue
        
        # Simulate mechanical layout adjustments matching selected standards
        if standard == "pep8":
            # Ensure Python stylistic spaces around binary assignment maps
            if "=" in stripped and "==" not in stripped and " =" not in stripped and "= " not in stripped:
                stripped = stripped.replace("=", " = ")
            # Emulate maximum horizontal print character bounds enforcement
            if len(stripped) > line_length_limit:
                stripped = f"{stripped[:line_length_limit-4]}..."
        
        elif standard == "prettier":
            # Ensure JS statements consistently terminate with explicit semicolons
            if not stripped.endswith(";") and not stripped.endswith("{") and not stripped.endswith("}"):
                if any(keyword in stripped for keyword in ["const", "let", "var", "return", "console"]):
                    stripped = f"{stripped};"

        # Preserve structural block indentation offsets
        indent_count = len(line) - len(line.lstrip())
        formatted_lines.append(" " * indent_count + stripped)

    final_formatted_code = "\n".join(formatted_lines)

    report = {
        "applied_styling_standard": standard,
        "configured_max_line_length": line_length_limit,
        "metrics": {
            "initial_line_count": len(lines),
            "final_line_count": len(formatted_lines),
            "character_delta_count": len(final_formatted_code) - len(code_content)
        },
        "formatting_engine_status": "Clean",
        "formatted_code_output": final_formatted_code
    }

    return f"[code_formatter] Code style normalization execution complete: {json.dumps(report, ensure_ascii=False)}"


SKILLS = [
    {
        "name": "code_formatter",
        "description": "Standardizes structural code snippets against specific stylistic conventions and line metrics constraints.",
        "trigger_phrases": [
            "automated code formatting",
            "format code snippet style",
            "standardize source code layout",
            "apply pep8 formatting",
            "prettier code style enforcement",
            "fix script layout spacing",
        ],
        "func": format_code_snippet,
    },
]