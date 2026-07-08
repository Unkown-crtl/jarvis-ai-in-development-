"""
Jarvis Brain - LLM interface using Ollama (Llama 3.1)
"""
import json
import requests
from typing import Generator


OLLAMA_URL = "http://localhost:11434"
MODEL = "llama3.1"


def chat(messages: list[dict], stream: bool = True) -> str | Generator:
    """Send messages to Llama 3.1 via Ollama."""
    payload = {
        "model": MODEL,
        "messages": messages,
        "stream": stream,
    }
    if stream:
        def _stream():
            with requests.post(f"{OLLAMA_URL}/api/chat", json=payload, stream=True) as r:
                r.raise_for_status()
                for line in r.iter_lines():
                    if line:
                        chunk = json.loads(line)
                        if content := chunk.get("message", {}).get("content"):
                            yield content
                        if chunk.get("done"):
                            break
        return _stream()
    else:
        r = requests.post(f"{OLLAMA_URL}/api/chat", json=payload)
        r.raise_for_status()
        return r.json()["message"]["content"]


def check_ollama() -> bool:
    """Check if Ollama is running and model is available."""
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=3)
        models = [m["name"] for m in r.json().get("models", [])]
        return any(MODEL in m for m in models)
    except Exception:
        return False
