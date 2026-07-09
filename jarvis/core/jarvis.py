"""
Jarvis Orchestrator - Main controller.
"""
import json
from typing import Generator
from core.brain import chat, check_ollama
from core.skill_manager import SkillManager
from core.agent_runner import AgentRunner


SYSTEM_PROMPT = """You are Jarvis, an advanced AI desktop assistant powered by Llama 3.1.
You are sharp, precise, and professional — like Tony Stark's AI.
You help the user control their desktop, run tasks, manage workflows, debug code, and test MCP servers.

You have access to the following skills (Python functions you can invoke):
{skills}

When a user asks you to DO something (open an app, search, screenshot, run a script, etc.),
respond with a JSON action block inside triple backticks like this:

```json
{{"action": "skill_name", "params": {{"param1": "value1"}}}}
```

Otherwise, respond naturally in conversation.
Never invent skill names. Only call skills listed above.
If a skill isn't available for a request, say so and suggest the user add it."""


class Jarvis:
    def __init__(self, base_dir: str = "."):
        self.skill_manager = SkillManager(skills_dir=f"{base_dir}/skills")
        self.agent_runner = AgentRunner(agents_dir=f"{base_dir}/agents")
        self.history: list[dict] = []
        self.log_lines: list[str] = []
        self.ollama_ok = False

    def log(self, msg: str):
        self.log_lines.append(msg)
        if len(self.log_lines) > 200:
            self.log_lines = self.log_lines[-200:]

    def start(self):
        self.ollama_ok = check_ollama()
        self.agent_runner.start(log_cb=self.log)
        self.log("[Jarvis] Started.")
        if not self.ollama_ok:
            self.log("[Jarvis] WARNING: Ollama not running or llama3.1 not pulled.")

    def _build_system(self) -> str:
        return SYSTEM_PROMPT.format(skills=self.skill_manager.get_skill_descriptions())

    def _try_extract_action(self, text: str) -> dict | None:
        import re
        m = re.search(r"```json\s*(\{.*?\})\s*```", text, re.DOTALL)
        if m:
            try:
                return json.loads(m.group(1))
            except Exception:
                pass
        return None

    def chat_stream(self, user_input: str) -> Generator[str, None, None]:
        """Stream a response, execute any skill actions."""
        self.history.append({"role": "user", "content": user_input})
        messages = [{"role": "system", "content": self._build_system()}] + self.history

        full_response = ""
        if self.ollama_ok:
            for chunk in chat(messages, stream=True):
                full_response += chunk
                yield chunk
        else:
            full_response = self._fallback(user_input)
            yield full_response

        self.history.append({"role": "assistant", "content": full_response})

        # Execute action if present
        action = self._try_extract_action(full_response)
        if action:
            result = self._execute_action(action)
            if result:
                yield f"\n\n> **Action result:** {result}"
                self.log(f"[Skill:{action.get('action')}] {result}")

    def _execute_action(self, action: dict) -> str:
        skill_name = action.get("action")
        params = action.get("params", {})
        skill = self.skill_manager.find_skill(skill_name)
        if not skill:
            return f"Skill '{skill_name}' not found."
        try:
            return str(skill.run(**params))
        except Exception as e:
            return f"Skill error: {e}"

    def _fallback(self, text: str) -> str:
        text_l = text.lower()
        for name, skill in self.skill_manager.skills.items():
            if any(p in text_l for p in skill.trigger_phrases):
                try:
                    result = skill.run()
                    return f"[Skill:{name}] {result}"
                except Exception as e:
                    return f"[Skill:{name}] Error: {e}"
        return ("Ollama is not running. Start it with `ollama serve` and pull "
                "llama3.1 with `ollama pull llama3.1`. I can still run skills if "
                "you mention them by name.")

    def reload_skills(self):
        self.skill_manager.reload()
        self.log("[Jarvis] Skills reloaded.")

    def reload_agents(self):
        self.agent_runner.reload()
        self.log("[Jarvis] Agents reloaded.")

    def clear_history(self):
        self.history.clear()
