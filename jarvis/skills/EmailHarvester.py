import re
import json


def harvest_email_addresses(text_data: str) -> str:
    """Harvests email addresses from websites, documents, or unstructured raw text streams."""
    if not text_data:
        return "[email_harvester] Error: Missing required text_data input string."

    # Regular expression matching standard email structures conforming to common address constraints
    email_pattern = re.compile(
        r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    )

    found_matches = email_pattern.findall(text_data)
    
    # Deduplicate entries while keeping preservation ordering sequences intact
    harvested_emails = []
    for email in found_matches:
        email_clean = email.strip().lower()
        if email_clean not in harvested_emails:
            harvested_emails.append(email_clean)

    report = {
        "source_text_length": len(text_data),
        "total_harvested_count": len(harvested_emails),
        "harvested_email_addresses": harvested_emails
    }

    return f"[email_harvester] Harvesting sequence completed: {json.dumps(report, ensure_ascii=False)}"


SKILLS = [
    {
        "name": "email_harvester",
        "description": "Harvests and extracts email addresses from unstructured web contents, documents, and textual inputs.",
        "trigger_phrases": [
            "harvest emails",
            "extract email addresses",
            "scrape emails from text",
            "email harvester",
            "collect emails from document",
            "find email addresses",
        ],
        "func": harvest_email_addresses,
    },
]