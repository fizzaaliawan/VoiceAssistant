from __future__ import annotations
from datetime import datetime
from typing import Optional
from assistant.core import Skill, Intent

class TimeDateSkill(Skill):
    name = "time_date"
    def intents(self):
        return [
            Intent("ask_time", [r"what(?:'s| is) the time", "current time", "tell me the time"], "Tells the time"),
            Intent("ask_date", [r"what(?:'s| is) the date", "today's date", "tell me the date"], "Tells today's date"),
        ]

    def handle(self, intent_name: str, query: str) -> Optional[str]:
        now = datetime.now()
        if intent_name == "ask_time":
            return f"It is {now.strftime('%I:%M %p')}."
        if intent_name == "ask_date":
            return f"Today is {now.strftime('%A, %B %d, %Y')}."
        return None
