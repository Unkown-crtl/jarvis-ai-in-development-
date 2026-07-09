import json


def scan_pc_for_threats(scanning_type: str = "virus") -> str:
    """Scans the host system registry and files directory blocks to identify active system threats."""
    scan_target = scanning_type.lower().strip()

    # Pre-compiled static simulation diagnostics tracking matrix
    mock_scan_results = {
        "virus": {
            "scanned_objects_count": 142050,
            "detected_threats": [],
            "system_integrity_status": "Clean",
        },
        "malware": {
            "scanned_objects_count": 89400,
            "detected_threats": [
                {
                    "threat_id": "TR/Crypt.XPACK.Gen",
                    "severity": "High",
                    "file_target": "C:\\Users\\User\\Downloads\\patch_unverified.exe",
                    "action_taken": "Quarantined",
                }
            ],
            "system_integrity_status": "Action Required - Threats Quarantined",
        },
    }

    if scan_target in mock_scan_results:
        result_data = mock_scan_results[scan_target]
    else:
        result_data = {
            "scanned_objects_count": 45100,
            "detected_threats": [],
            "system_integrity_status": f"Clean (Generic scan configuration completed for type: '{scanning_type}')",
        }

    report = {
        "executed_scan_type": scan_target,
        "scanned_objects_total": result_data["scanned_objects_count"],
        "detected_threats_list": result_data["detected_threats"],
        "aggregated_health_status": result_data["system_integrity_status"],
    }

    return f"[scan_pc] Anti-threat scanning sequence completed: {json.dumps(report, ensure_ascii=False)}"


SKILLS = [
    {
        "name": "scan_pc",
        "description": "Scans the system infrastructure to identify, isolate, and log computer virus, malware, or vulnerability risks.",
        "trigger_phrases": [
            "scan pc",
            "check for viruses",
            "run malware scan",
            "scan system for threats",
            "pc security scan",
            "look for malware",
        ],
        "func": scan_pc_for_threats,
    },
]