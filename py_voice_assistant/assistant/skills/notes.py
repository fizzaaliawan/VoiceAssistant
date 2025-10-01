from __future__ import annotations
import os, json, pathlib
from typing import Optional, List
from assistant.core import Skill, Intent

NOTES_PATH = pathlib.Path.home() / ".nova_notes.json"

def load_notes() -> List[str]:
    if NOTES_PATH.exists():
        try:
            return json.loads(NOTES_PATH.read_text(encoding="utf-8"))
        except Exception:
            return []
    return []

def save_notes(notes: List[str]):
    NOTES_PATH.write_text(json.dumps(notes, ensure_ascii=False, indent=2), encoding="utf-8")

class NotesSkill(Skill):
    name = "notes"
    def intents(self):
        return [
            Intent("add_note", [r"note (?P<text>.+)", r"remember (?P<text>.+)"], "Saves a note"),
            Intent("list_notes", ["list notes", "show notes"], "Lists notes"),
            Intent("clear_notes", ["clear notes", "delete all notes"], "Clears notes"),
        ]

    def handle(self, intent_name: str, query: str) -> Optional[str]:
        if intent_name == "add_note":
            # naive parse
            text = query.split("note",1)[-1].strip() if "note" in query.lower() else query.split("remember",1)[-1].strip()
            if not text:
                return "What should I note?"
            notes = load_notes(); notes.append(text); save_notes(notes)
            return "Saved."
        if intent_name == "list_notes":
            notes = load_notes()
            if not notes:
                return "No notes yet."
            return "Here are your notes: " + "; ".join(notes[:10])
        if intent_name == "clear_notes":
            save_notes([])
            return "All notes cleared."
        return None
