"""
Agent Runner - Manages and runs autonomous agents.
Agents are Python files in the /agents directory, each implementing a run() coroutine.
"""
import importlib.util
import os
import threading
import time
from dataclasses import dataclass, field
from typing import Callable


@dataclass
class Agent:
    name: str
    description: str
    interval: float          # seconds between runs (0 = run once)
    func: Callable
    enabled: bool = True
    last_run: float = 0.0
    status: str = "idle"
    last_output: str = ""
    _thread: threading.Thread | None = field(default=None, repr=False)

    def run_once(self, log_cb=None):
        try:
            self.status = "running"
            result = self.func()
            self.last_output = str(result) if result else ""
            self.last_run = time.time()
            self.status = "idle"
            if log_cb:
                log_cb(f"[Agent:{self.name}] {self.last_output}")
        except Exception as e:
            self.status = "error"
            self.last_output = str(e)
            if log_cb:
                log_cb(f"[Agent:{self.name}] ERROR: {e}")


class AgentRunner:
    def __init__(self, agents_dir: str = "agents"):
        self.agents: dict[str, Agent] = {}
        self.agents_dir = agents_dir
        self.log_cb = None
        self._running = False
        self._ticker: threading.Thread | None = None
        os.makedirs(agents_dir, exist_ok=True)
        self._load_all()

    def _load_all(self):
        for fname in os.listdir(self.agents_dir):
            if fname.endswith(".py") and not fname.startswith("_"):
                self._load_agent_file(os.path.join(self.agents_dir, fname))

    def _load_agent_file(self, path: str):
        spec = importlib.util.spec_from_file_location("agent_module", path)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            print(f"[AgentRunner] Failed to load {path}: {e}")
            return

        if not hasattr(mod, "AGENTS"):
            return

        for a in mod.AGENTS:
            agent = Agent(
                name=a["name"],
                description=a["description"],
                interval=a.get("interval", 0),
                func=a["func"],
                enabled=a.get("enabled", True),
            )
            self.agents[agent.name] = agent
            print(f"[AgentRunner] Loaded agent: {agent.name}")

    def reload(self):
        self.agents.clear()
        self._load_all()

    def start(self, log_cb=None):
        self.log_cb = log_cb
        self._running = True
        self._ticker = threading.Thread(target=self._loop, daemon=True)
        self._ticker.start()

    def stop(self):
        self._running = False

    def _loop(self):
        while self._running:
            now = time.time()
            for agent in self.agents.values():
                if not agent.enabled:
                    continue
                if agent.interval > 0 and (now - agent.last_run) >= agent.interval:
                    t = threading.Thread(target=agent.run_once, args=(self.log_cb,), daemon=True)
                    t.start()
            time.sleep(1)

    def run_agent_now(self, name: str) -> str:
        agent = self.agents.get(name)
        if not agent:
            return f"Agent '{name}' not found."
        agent.run_once(self.log_cb)
        return agent.last_output

    def toggle(self, name: str) -> str:
        agent = self.agents.get(name)
        if not agent:
            return f"Agent '{name}' not found."
        agent.enabled = not agent.enabled
        return f"Agent '{name}' {'enabled' if agent.enabled else 'disabled'}."

    def status_all(self) -> list[dict]:
        return [
            {
                "name": a.name,
                "description": a.description,
                "enabled": a.enabled,
                "status": a.status,
                "interval": a.interval,
                "last_output": a.last_output,
            }
            for a in self.agents.values()
        ]
