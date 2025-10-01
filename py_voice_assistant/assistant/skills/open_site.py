from __future__ import annotations
import webbrowser
from typing import Optional
from assistant.core import Skill, Intent

COMMON = {
    "youtube": "https://www.youtube.com",
    "github": "https://github.com",
    "google": "https://www.google.com",
    "gmail": "https://mail.google.com",
}

class OpenSiteSkill(Skill):
    name = "open_site"
    def intents(self):
        return [
            Intent("open_site", [r"open (?P<site>\w+)", "open youtube", "open github", "open google"], "Opens a common website"),
        ]

    def handle(self, intent_name: str, query: str) -> Optional[str]:
        if intent_name == "open_site":
            q = query.lower()
            for key, url in COMMON.items():
                if key in q:
                    webbrowser.open(url)
                    return f"Opening {key}."
            return "Which site? Try 'open YouTube' or 'open GitHub'."
        return None
