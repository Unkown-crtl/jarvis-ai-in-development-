"""
Skill Manager - Load, register, and run skills dynamically.
Skills are Python files in the /skills directory.
"""
import importlib.util
import inspect
import os
from dataclasses import dataclass, field
from typing import Callable, Any


@dataclass
class Skill:
    name: str
    description: str
    trigger_phrases: list[str]
    func: Callable
    params: list[str] = field(default_factory=list)

    def run(self, **kwargs) -> Any:
        return self.func(**kwargs)


class SkillManager:
    def __init__(self, skills_dir: str = "skills"):
        self.skills: dict[str, Skill] = {}
        self.skills_dir = skills_dir
        os.makedirs(skills_dir, exist_ok=True)
        self._load_all()

    def _load_all(self):
        for fname in os.listdir(self.skills_dir):
            if fname.endswith(".py") and not fname.startswith("_"):
                self._load_skill_file(os.path.join(self.skills_dir, fname))

    def _load_skill_file(self, path: str):
        spec = importlib.util.spec_from_file_location("skill_module", path)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
        except Exception as e:
            print(f"[SkillManager] Failed to load {path}: {e}")
            return

        # Each skill file should define SKILLS: list of dict
        if not hasattr(mod, "SKILLS"):
            return

        for s in mod.SKILLS:
            skill = Skill(
                name=s["name"],
                description=s["description"],
                trigger_phrases=s.get("trigger_phrases", []),
                func=s["func"],
                params=list(inspect.signature(s["func"]).parameters.keys()),
            )
            self.skills[skill.name] = skill
            print(f"[SkillManager] Loaded skill: {skill.name}")

    def reload(self):
        self.skills.clear()
        self._load_all()

    def get_skill_descriptions(self) -> str:
        if not self.skills:
            return "No skills loaded."
        lines = []
        for name, skill in self.skills.items():
            lines.append(f"- **{name}**: {skill.description}")
            if skill.params:
                lines.append(f"  params: {', '.join(skill.params)}")
        return "\n".join(lines)

    def find_skill(self, name: str) -> Skill | None:
        return self.skills.get(name)

    def all_names(self) -> list[str]:
        return list(self.skills.keys())
