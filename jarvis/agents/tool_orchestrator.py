import os
import glob
import json
import requests

def tool_orchestrator() -> str:
    """Scans for unhandled task requests or pending tool requirements and routes them to optimal skills/agents."""
    # Orchestrator looks at a central workspace file for incoming autonomous tasks
    task_queue_file = "workspace/task_queue.json"
    skills_directory = "skills"
    
    if not os.path.exists(task_queue_file):
        return "" # Idle pass when no workflow queue exists
        
    try:
        with open(task_queue_file, "r", encoding="utf-8") as f:
            queue_data = json.load(f)
            
        pending_tasks = [t for t in queue_data.get("tasks", []) if t.get("status") == "pending"]
        if not pending_tasks:
            return ""
            
        task = pending_tasks[0]
        task_id = task.get("id")
        objective = task.get("objective")
        
        # Read available skills in environment to map to the objective
        available_skills = []
        for file in glob.glob(os.path.join(skills_directory, "*.py")):
            available_skills.append(os.path.basename(file))
            
        prompt = (
            f"You are the central intelligence routing core of an AI system.\n"
            f"Objective to solve: '{objective}'\n"
            f"Available functional skill profiles: {available_skills}\n\n"
            f"Determine the absolute best skill file to handle this task, and extract the parameters needed "
            f"from the objective. Respond with raw JSON only matching this layout:\n"
            f"{{\"selected_skill\": \"file_name.py\", \"parameters\": {{\"arg_name\": \"value\"}}}}\n"
            f"If no skill fits, set selected_skill to null."
        )
        
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3.1",
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": 0.0}
        }
        
        response = requests.post(url, json=payload, timeout=30)
        if response.status_code != 200:
            return f"[tool_orchestrator] Failed routing inference via Ollama."
            
        decision = json.loads(response.json().get("response", "{}").strip())
        selected = decision.get("selected_skill")
        params = decision.get("parameters", {})
        
        # Update task status in queue log to prevent loops
        for t in queue_data["tasks"]:
            if t["id"] == task_id:
                if selected:
                    t["status"] = "routed"
                    t["assigned_to"] = selected
                    t["parameters"] = params
                else:
                    t["status"] = "failed_no_route"
                    
        with open(task_queue_file, "w", encoding="utf-8") as f:
            json.dump(queue_data, f, indent=4)
            
        if selected:
            return f"[tool_orchestrator] Route locked for Task #{task_id}. Assigned goal directly to {selected} with payload parameters: {params}."
        return f"[tool_orchestrator] Warning: Task #{task_id} could not be automatically bound to any active system skill signatures."
        
    except Exception as e:
        return f"[tool_orchestrator] Execution breakdown. Error: {str(e)}"


AGENTS = [
    {
        "name": "tool_orchestrator",
        "description": "Monitors workflow task queues, resolving incoming goals by contextually mapping objectives directly to optimal runtime skills.",
        "interval": 30,
        "enabled": True,
        "func": tool_orchestrator,
    }
]