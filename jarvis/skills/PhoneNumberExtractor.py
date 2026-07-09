import re
import json


def extract_phone_numbers(text_data: str) -> str:
    """Extracts phone numbers from text fields, unstructured logs, or email data bodies."""
    if not text_data:
        return "[phone_number_extractor] Error: Missing required text_data input string."

    # Regular expression configuration matching varied international and local standard formats
    # Handles: +1-555-555-5555, (555) 555-5555, 555.555.5555, +49 1234 567890, etc.
    phone_pattern = re.compile(
        r'(?:(?:\+?([1-9]\d{0,3})[\s.-]?)?\(?(\d{2,4})\)?[\s.-]?)?(\d{3,4})[\s.-]?(\d{3,4})(?:[\s.-]?(\d{1,4}))?'
    )

    found_matches = phone_pattern.finditer(text_data)
    extracted_numbers = []

    for match in found_matches:
        full_number = match.group(0).strip()
        
        # Enforce minimum digit density constraints to filter out unrelated stray scalar strings
        digit_count = sum(c.isdigit() for c in full_number)
        if digit_count >= 7 and digit_count <= 15:
            # Clean trailing formatting noise artifacts from bounds boundaries
            clean_num = full_number.strip(".,:- ")
            if clean_num not in extracted_numbers:
                extracted_numbers.append(clean_num)

    report = {
        "source_text_length": len(text_data),
        "total_extractions_found": len(extracted_numbers),
        "extracted_phone_numbers": extracted_numbers
    }

    return f"[phone_number_extractor] Pattern matching phase complete: {json.dumps(report, ensure_ascii=False)}"


SKILLS = [
    {
        "name": "phone_number_extractor",
        "description": "Extracts telephone and phone numbers from unstructured text streams, documents, and email payloads.",
        "trigger_phrases": [
            "extract phone numbers",
            "find phone number in text",
            "get phone numbers from email",
            "phone number extractor",
            "scrape telephone numbers",
            "pull phone listings",
        ],
        "func": extract_phone_numbers,
    },
]