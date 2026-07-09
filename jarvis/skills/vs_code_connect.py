import os

def path_finder(target_name: str) -> str:
    """
    Scans the workspace directory structure to find the absolute path 
    of a specified project folder or file configuration target.
    """
    root_dir = os.getcwd()
    for root, dirs, files in os.walk(root_dir):
        if target_name in dirs or target_name in files:
            return os.path.abspath(os.path.join(root, target_name))
            
    # Fallback simulation if exact node isn't matched right away
    return os.path.abspath(os.path.join(root_dir, target_name))


def vs_code_connect(action: str = "status", file_path: str = "", content: str = "", **kwargs) -> str:
    """
    Establishes a synchronization channel directly to VS Code. Accepts arbitrary keyword 
    arguments dynamically (like project_path) to prevent unexpected keyword argument crashes,
    utilizing path_finder internally when explicit routing parameters match structural queries.
    """
    host = "127.0.0.1"
    port = 54321  
    
    # Safely unpack potential keyword deviations or routing variants safely from kwargs
    project_path = kwargs.get("project_path", "")
    resolved_path = file_path
    
    if project_path and not resolved_path:
        resolved_path = path_finder(project_path)
    elif not resolved_path:
        resolved_path = os.getcwd()

    import json
    import socket

    payload = {
        "action": action,
        "filePath": resolved_path,
        "content": content
    }
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(3.0)
            s.connect((host, port))
            s.sendall(json.dumps(payload).encode("utf-8"))
            
            response = s.recv(4096).decode("utf-8")
            res_data = json.loads(response)
            
            if res_data.get("success"):
                return f"[vs_code_connect] Success: {res_data.get('message', 'Operation completed.')}"
            else:
                return f"[vs_code_connect] Editor Refusal: {res_data.get('error', 'Unknown editor error.')}"
                
    except ConnectionRefusedError:
        return f"[vs_code_connect] Connection Failed: Could not connect to VS Code on port {port}. Please verify your helper extension is active."
    except Exception as e:
        return f"[vs_code_connect] Workspace Execution Error: {str(e)}"


SKILLS = [
    {
        "name": "vs_code_connect",
        "description": "Establishes a synchronization channel directly to VS Code to view, edit, or write code files locally. Safely handles dynamic path arguments.",
        "trigger_phrases": ["connect to vs code", "open in vs code", "write to vs code", "edit file in vscode", "send code to vscode"],
        "func": vs_code_connect,
    },
]