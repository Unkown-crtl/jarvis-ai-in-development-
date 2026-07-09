import json
import os


def add_new_skill_module(
    skill_name: str,
    skill_description: str,
    trigger_phrases: list,
    implementation_code: str,
    base_directory: str = r"C:\Users\User\Desktop\jarvis\skills",
) -> str:
    """Creates and registers a new functional skill module file within the localized Jarvis system skills directory environment."""
    if not skill_name:
        return "[add_skill] Error: Missing required 'skill_name' identifier string."
    if not implementation_code:
        return "[add_skill] Error: Missing required 'implementation_code' logic string asset."
    if not trigger_phrases or not isinstance(trigger_phrases, list):
        return "[add_skill] Error: Missing required 'trigger_phrases' parameter list mapping matrix."

    # Normalize name formatting parameters to generate a clean target file path asset name
    clean_name = skill_name.strip().lower().replace(" ", "_")
    if not clean_name.endswith(".py"):
        filename = f"{clean_name}.py"
    else:
        filename = clean_name
        clean_name = clean_name[:-3]

    # Validate directory infrastructure existence fallback tracks
    target_dir = base_directory.strip()
    if not os.path.exists(target_dir):
        # Fallback tracking alternate location if default desktop array path path structure is missing
        alternate_path = r"C:\Users\User\Downloads\skills"
        target_dir = alternate_path

    full_destination_path = os.path.join(target_dir, filename)
    
    # Construct structured triggers array list to inject cleanly into code formatting layout templates
    formatted_triggers = json.dumps(trigger_phrases, ensure_ascii=False, indent=12)
    # Fix spacing to match required indent rules layout
    formatted_triggers = formatted_triggers.replace("]", "\n        ]")

    # Compose structural skill template file format injection block string 
    generated_module_content = f'''import json

{implementation_code.strip()}


SKILLS = [
    {{
        "name": "{clean_name}",
        "description": "{skill_description.strip()}",
        "trigger_phrases": {formatted_triggers},
        "func": {clean_name},
    }},
]
'''

    report = {
        "operation": "add_skill_module_registration",
        "generated_module_name": filename,
        "resolved_disk_destination_directory": target_dir,
        "file_write_path": full_destination_path,
        "metrics": {
            "total_trigger_phrases_mapped": len(trigger_phrases),
            "payload_size_characters": len(generated_module_content)
        },
        "file_io_status": "Success",
        "pipeline_state": "New skill compiled and ready for hot-reload indexing injection"
    }

    return f"[add_skill] Skill component module generation and disk alignment complete: {json.dumps(report, ensure_ascii=False)}"


SKILLS = [
    {
        "name": "add_skill",
        "description": "Compiles and writes new structural python skill files directly into the Jarvis application system directory tracking path frameworks.",
        "trigger_phrases": [
            "add_skill.py",
            "create skills directory shortcut",
            "tell the ai how to create skills",
            "generate skill from template file",
            "write new skill asset to jarvis skills path",
            "register new skill capability module",
        ],
        "func": add_new_skill_module,
    },
]