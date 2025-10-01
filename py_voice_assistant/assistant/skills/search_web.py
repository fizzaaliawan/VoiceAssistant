from __future__ import annotations
import urllib.parse, webbrowser
from typing import Optional
from assistant.core import Skill, Intent

class SearchWebSkill(Skill):
    name = "search_web"
    def intents(self):
        return [
            Intent("search_web", [r"search for (?P<q>.+)", r"google (?P<q>.+)"], "Searches the web"),
        ]

    def handle(self, intent_name: str, query: str) -> Optional[str]:
        if intent_name == "search_web":
            # crude parse
            q = query.lower().split("search for")[-1].strip() if "search for" in query.lower() else query.lower().split("google")[-1].strip()
            if not q:
                return "What should I search for?"
            url = "https://www.google.com/search?q=" + urllib.parse.quote_plus(q)
            webbrowser.open(url)
            return f"Searching for {q}."
        return None
