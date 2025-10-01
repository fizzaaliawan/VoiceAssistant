from __future__ import annotations
import platform, sys
from typing import Optional
from assistant.core import Skill, Intent

class SystemSkill(Skill):
    name = "system"
    def intents(self):
        return [
            Intent("about", ["who are you", "what can you do"], "Describes the assistant"),
            Intent("quit", ["quit", "exit", "goodbye"], "Quits the assistant"),
            Intent("os_info", ["system info", "what is my os"], "Shows basic system info"),
        ]

    def handle(self, intent_name: str, query: str) -> Optional[str]:
        if intent_name == "about":
            return "I'm a local voice assistant with modular skills. Ask me for time, notes, reminders, or to open websites."
        if intent_name == "os_info":
            return f"You are on {platform.system()} {platform.release()}."
        if intent_name == "quit":
            print("Goodbye!"); sys.exit(0)
        return None
