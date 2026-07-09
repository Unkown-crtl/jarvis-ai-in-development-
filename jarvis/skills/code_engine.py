"""
Code Engine Skill — Debug → Review → Fix → Upgrade pipeline.

Stages:
  1. REVIEW   — read the code, identify all issues (bugs, smells, security)
  2. DEBUG    — trace runtime errors, explain root causes
  3. FIX      — produce corrected code
  4. UPGRADE  — apply modern patterns, improve performance/readability

Each stage is streamed so the user sees reasoning as it happens.
"""
import subprocess
import sys
import tempfile
import os
import ast
import re
from typing import Generator


# ─── Static analysis helpers ─────────────────────────────────────────────────

def _syntax_check(code: str, lang: str = "python") -> list[str]:
    errors = []
    if lang == "python":
        try:
            ast.parse(code)
        except SyntaxError as e:
            errors.append(f"SyntaxError line {e.lineno}: {e.msg}")
    return errors


def _run_python(code: str, timeout: int = 8) -> dict:
    """Run Python code in a subprocess, capture stdout/stderr."""
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
        f.write(code)
        path = f.name
    try:
        result = subprocess.run(
            [sys.executable, path],
            capture_output=True, text=True, timeout=timeout
        )
        return {
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"stdout": "", "stderr": "Execution timed out.", "returncode": -1}
    except Exception as e:
        return {"stdout": "", "stderr": str(e), "returncode": -1}
    finally:
        os.unlink(path)


def _lint_python(code: str) -> list[str]:
    """Run flake8 or pyflakes if available."""
    issues = []
    with tempfile.NamedTemporaryFile(suffix=".py", mode="w", delete=False) as f:
        f.write(code)
        path = f.name
    try:
        r = subprocess.run(["flake8", "--max-line-length=100", path],
                           capture_output=True, text=True, timeout=5)
        for line in r.stdout.strip().split("\n"):
            if line.strip():
                # strip temp path prefix
                issues.append(line.replace(path + ":", "line "))
    except FileNotFoundError:
        try:
            r = subprocess.run([sys.executable, "-m", "py_compile", path],
                               capture_output=True, text=True, timeout=5)
            if r.stderr:
                issues.append(r.stderr.strip())
        except Exception:
            pass
    except Exception:
        pass
    finally:
        os.unlink(path)
    return issues


# ─── LLM-powered stages ──────────────────────────────────────────────────────

def _llm_stage(code: str, stage: str, extra: str = "") -> str:
    """Call Ollama synchronously for a code stage."""
    from core.brain import chat
    prompts = {
        "review": f"""You are a senior code reviewer. Review this code thoroughly.
Identify: bugs, logic errors, security issues, bad practices, missing error handling.
Be specific about line numbers. Format as a numbered list.

Code:
```
{code}
```
{extra}""",
        "debug": f"""You are an expert debugger. Trace the root cause of errors in this code.
For each issue: explain WHY it fails, what the actual vs expected behavior is.
Runtime info: {extra}

Code:
```
{code}
```""",
        "fix": f"""You are an expert programmer. Fix ALL issues found in this code.
Previous review: {extra}

Return ONLY the fixed code, no explanations, wrapped in triple backticks.""",
        "upgrade": f"""You are a senior engineer. Upgrade this code with:
- Modern language patterns (type hints, dataclasses, f-strings, etc.)
- Performance improvements
- Better error handling
- Cleaner structure and naming
- Docstrings

Return ONLY the upgraded code wrapped in triple backticks, then a short "Changes:" section.""",
    }
    messages = [
        {"role": "system", "content": "You are Jarvis's code engine. Be precise and thorough."},
        {"role": "user", "content": prompts[stage]},
    ]
    return chat(messages, stream=False)


# ─── Public skill functions ──────────────────────────────────────────────────

def review_code(code: str) -> str:
    """Stage 1: Static analysis + LLM review."""
    syntax_errors = _syntax_check(code)
    lint_issues = _lint_python(code)

    static = ""
    if syntax_errors:
        static += "SYNTAX ERRORS:\n" + "\n".join(syntax_errors) + "\n\n"
    if lint_issues:
        static += "LINT ISSUES:\n" + "\n".join(lint_issues[:20]) + "\n\n"

    llm_review = _llm_stage(code, "review", static)
    return f"── STATIC ANALYSIS ──\n{static or 'No static issues found.'}\n\n── LLM REVIEW ──\n{llm_review}"


def debug_code(code: str) -> str:
    """Stage 2: Run the code, capture errors, explain them."""
    run_result = _run_python(code)
    extra = f"stdout: {run_result['stdout']}\nstderr: {run_result['stderr']}\nexitcode: {run_result['returncode']}"

    if run_result["returncode"] == 0 and not run_result["stderr"]:
        runtime_info = f"✓ Code ran successfully.\nOutput: {run_result['stdout']}"
        debug_out = "No runtime errors detected. Code executed cleanly."
    else:
        debug_out = _llm_stage(code, "debug", extra)
        runtime_info = extra

    return f"── RUNTIME OUTPUT ──\n{runtime_info}\n\n── DEBUG ANALYSIS ──\n{debug_out}"


def fix_code(code: str, review: str = "") -> str:
    """Stage 3: Produce fixed code."""
    result = _llm_stage(code, "fix", review)
    # Extract code block
    m = re.search(r"```(?:\w+)?\n(.*?)```", result, re.DOTALL)
    if m:
        return f"── FIXED CODE ──\n```\n{m.group(1).strip()}\n```"
    return f"── FIXED CODE ──\n{result}"


def upgrade_code(code: str) -> str:
    """Stage 4: Upgrade to modern patterns."""
    result = _llm_stage(code, "upgrade")
    return f"── UPGRADED CODE ──\n{result}"


def full_pipeline(code: str) -> str:
    """Run all 4 stages sequentially and return combined report."""
    out = []
    out.append("═══ Jarvis CODE ENGINE ═══\n")

    out.append("▶ STAGE 1: REVIEW")
    review = review_code(code)
    out.append(review)

    out.append("\n▶ STAGE 2: DEBUG")
    debug = debug_code(code)
    out.append(debug)

    out.append("\n▶ STAGE 3: FIX")
    fix = fix_code(code, review)
    out.append(fix)

    out.append("\n▶ STAGE 4: UPGRADE")
    upgrade = upgrade_code(fix)
    out.append(upgrade)

    return "\n".join(out)


SKILLS = [
    {
        "name": "review_code",
        "description": "Review code for bugs, security issues, and bad practices (stage 1).",
        "trigger_phrases": ["review code", "check code", "code review"],
        "func": review_code,
    },
    {
        "name": "debug_code",
        "description": "Run code, capture errors, explain root causes (stage 2).",
        "trigger_phrases": ["debug", "trace error", "why does this fail"],
        "func": debug_code,
    },
    {
        "name": "fix_code",
        "description": "Fix all bugs and issues in code (stage 3).",
        "trigger_phrases": ["fix code", "fix the bug", "fix this"],
        "func": fix_code,
    },
    {
        "name": "upgrade_code",
        "description": "Upgrade code to modern patterns and improve quality (stage 4).",
        "trigger_phrases": ["upgrade code", "refactor", "modernize", "improve code"],
        "func": upgrade_code,
    },
    {
        "name": "full_pipeline",
        "description": "Run full Review→Debug→Fix→Upgrade pipeline on code.",
        "trigger_phrases": ["full pipeline", "analyze and fix", "debug and fix"],
        "func": full_pipeline,
    },
]
