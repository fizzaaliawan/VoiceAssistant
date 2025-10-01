from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Callable, List
import importlib
import pkgutil
import time

@dataclass
class Intent:
    name: str
    patterns: list[str]       # regex or simple substrings
    description: str = ""

class Skill:
    name: str = "base"
    def intents(self) -> list[Intent]:
        return []
    def handle(self, intent_name: str, query: str) -> Optional[str]:
        return None

def discover_skills(package: str = "assistant.skills") -> dict[str, Skill]:
    skills: dict[str, Skill] = {}
    pkg = importlib.import_module(package)
    for m in pkgutil.iter_modules(pkg.__path__):
        module_name = f"{package}.{m.name}"
        mod = importlib.import_module(module_name)
        # Expect exactly one Skill subclass per module
        for obj_name in dir(mod):
            obj = getattr(mod, obj_name)
            try:
                if isinstance(obj, type) and issubclass(obj, Skill) and obj is not Skill:
                    instance: Skill = obj()
                    skills[instance.name] = instance
            except Exception:
                continue
    return skills

def timestamp() -> str:
    return time.strftime("%Y-%m-%d %H:%M:%S")
