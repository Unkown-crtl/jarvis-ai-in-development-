"""
J.A.R.V.I.S. — Just A Rather Very Intelligent System
Powered by Llama 3.1 via Ollama

Usage:
    python main.py              # Launch GUI
    python main.py --cli        # Launch CLI mode

Requirements:
    pip install requests psutil pyautogui

Llama 3.1 setup:
    1. Install Ollama: https://ollama.com
    2. ollama pull llama3.1
    3. ollama serve  (runs in background)
"""
import sys
import os
import subprocess
import time
import requests

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def ensure_ollama_running():
    try:
        requests.get("http://localhost:11434/api/tags", timeout=2)
    except requests.exceptions.ConnectionError:
        try:
            if sys.platform == "win32":
                subprocess.Popen(["ollama", "serve"], creationflags=subprocess.CREATE_NO_WINDOW)
            else:
                subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            for _ in range(10):
                time.sleep(1)
                try:
                    requests.get("http://localhost:11434/api/tags", timeout=1)
                    break
                except requests.exceptions.ConnectionError:
                    continue
        except FileNotFoundError:
            print("Error: 'ollama' command not found. Please install Ollama.", file=sys.stderr)


def run_gui():
    from ui.app import JarvisApp
    app = JarvisApp()
    app.mainloop()


def run_cli():
    from core.jarvis import Jarvis
    j = Jarvis(base_dir=os.path.dirname(os.path.abspath(__file__)))
    j.start()
    print("J.A.R.V.I.S. CLI — type 'exit' to quit\n")
    while True:
        try:
            user_input = input("YOU: ").strip()
            if user_input.lower() in ("exit", "quit"):
                break
            if not user_input:
                continue
            print("JARVIS: ", end="", flush=True)
            for chunk in j.chat_stream(user_input):
                print(chunk, end="", flush=True)
            print()
        except (KeyboardInterrupt, EOFError):
            break


if __name__ == "__main__":
    ensure_ollama_running()
    if "--cli" in sys.argv:
        run_cli()
    else:
        run_gui()