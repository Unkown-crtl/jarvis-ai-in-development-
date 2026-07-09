import os
import requests

def code_completion(path: str, line_number: int = -1) -> str:
    """Uses Llama 3.1 via Ollama to provide context-aware code completion suggestions for a given file."""
    clean_path = path.strip("'\"")
    
    if not os.path.exists(clean_path):
        return f"[code_completion] Error: File '{clean_path}' does not exist."
        
    try:
        with open(clean_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
        file_extension = os.path.splitext(clean_path)[1]
        
        # If line_number is default or out of bounds, complete from the end of the file
        if line_number <= 0 or line_number > len(lines):
            context_code = "".join(lines)
            position_desc = "the end of the file"
        else:
            context_code = "".join(lines[:line_number])
            position_desc = f"line {line_number}"
            
        prompt = (
            f"Act as an intelligent IDE code completion engine. Analyze the following code context from '{clean_path}' "
            f"up to {position_desc}. Based on this context, provide the most logical, syntactically correct code completion block "
            f"to continue or finish the current logic block. Return ONLY the code completion block itself within a code fence, "
            f"with no filler conversational text.\n\n"
            f"Code Context:\n```{file_extension}\n{context_code}\n```"
        )
        
        url = "http://localhost:11434/api/generate"
        payload = {
            "model": "llama3.1",
            "prompt": prompt,
            "stream": False
        }
        
        response = requests.post(url, json=payload, timeout=30)
        
        if response.status_code == 200:
            result_json = response.json()
            completion_suggestion = result_json.get("response", "No completion suggestions could be generated.")
            return f"[code_completion] Suggestions generated relative to context:\n\n{completion_suggestion}"
        else:
            return f"[code_completion] Ollama server replied with error status: {response.status_code}"
            
    except requests.exceptions.ConnectionError:
        return "[code_completion] Error: Connection refused by local Ollama instance. Run 'ollama serve'."
    except Exception as e:
        return f"[code_completion] Failure inside script handler. Error: {str(e)}"


SKILLS = [
    {
        "name": "code_completion",
        "description": "Provides intelligent code completion suggestions based on the context of the code.",
        "trigger_phrases": ["code completion", "complete code", "suggest code lines", "predict next code lines", "fill in code"],
        "func": code_completion,
    },
]