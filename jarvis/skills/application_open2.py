import json


def open_designated_application(
    application_name: str,
    execution_context: str = "native",
) -> str:
    """Simulates initializing, spawning, and opening a designated local application or website profile."""
    if not application_name:
        return "[open_application] Error: Missing required 'application_name' target string parameter."

    target_clean = application_name.strip()
    context_mode = execution_context.lower().strip()

    # Pre-compiled common path allocations and uniform resource identifiers
    application_registry = {
        "browser": {"type": "application", "path": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"},
        "editor": {"type": "application", "path": "C:\\Users\\User\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe"},
        "player": {"type": "application", "path": "C:\\Program Files\\VideoLAN\\VLC\\vlc.exe"},
        "github": {"type": "website", "path": "https://github.com"},
        "stackoverflow": {"type": "website", "path": "https://stackoverflow.com"},
    }

    lookup_key = target_clean.lower()
    if lookup_key in application_registry:
        resolved_entity = application_registry[lookup_key]
        resolved_path = resolved_entity["path"]
        deployment_type = resolved_entity["type"]
    else:
        # Fallback handling routing raw domain links or generic execution targets safely
        if lookup_key.startswith("http://") or lookup_key.startswith("https://") or lookup_key.endswith(".com") or lookup_key.endswith(".org"):
            resolved_path = target_clean if lookup_key.startswith("http") else f"https://{target_clean}"
            deployment_type = "website"
        else:
            resolved_path = target_clean
            deployment_type = "generic_executable"

    report = {
        "requested_target": target_clean,
        "resolved_deployment_type": deployment_type,
        "execution_path_or_uri": resolved_path,
        "environment_context": context_mode,
        "process_spawn_status": "Success",
        "window_state": "MaximizedFocus"
    }

    return f"[open_application] Execution string dispatched to shell layer: {json.dumps(report, ensure_ascii=False)}"


SKILLS = [
    {
        "name": "open_application",
        "description": "Opens, launches, or navigates to designated system software processes, binaries, or website endpoints.",
        "trigger_phrases": [
            "open application",
            "launch application or website",
            "open designated program",
            "start application shortcut",
            "run local program",
            "navigate to website link",
        ],
        "func": open_designated_application,
    },
]