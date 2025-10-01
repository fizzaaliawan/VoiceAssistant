from __future__ import annotations
from datetime import datetime, timedelta
import regex as re
from typing import Optional
from assistant.core import Skill, Intent

class RemindersSkill(Skill):
    name = "reminders"
    def intents(self):
        return [
            Intent("add_reminder", [
                r"remind me in (?P<num>\d+) (?P<unit>seconds?|minutes?|hours?) to (?P<task>.+)",
                r"remind me at (?P<hour>\d{1,2}):(?P<minute>\d{2}) to (?P<task>.+)",
            ], "Schedules a reminder"),
        ]

    def on_start(self, scheduler=None, speaker=None):
        self.scheduler = scheduler
        self.speaker = speaker

    def handle(self, intent_name: str, query: str) -> Optional[str]:
        if intent_name != "add_reminder": return None
        q = query.lower()
        m = re.search(r"remind me in (?P<num>\d+) (?P<unit>seconds?|minutes?|hours?) to (?P<task>.+)", q)
        if m:
            num = int(m.group("num")); unit = m.group("unit"); task = m.group("task")
            delta = timedelta(seconds=num) if "second" in unit else timedelta(minutes=num) if "minute" in unit else timedelta(hours=num)
            run_time = datetime.now() + delta
            self.scheduler.add_job(lambda: self._speak(task), 'date', run_date=run_time)
            return f"Okay, I'll remind you in {num} {unit}."
        m = re.search(r"remind me at (?P<hour>\d{1,2}):(?P<minute>\d{2}) to (?P<task>.+)", q)
        if m:
            hour = int(m.group("hour")); minute = int(m.group("minute")); task = m.group("task")
            now = datetime.now()
            run_time = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
            if run_time <= now:
                run_time += timedelta(days=1)
            self.scheduler.add_job(lambda: self._speak(task), 'date', run_date=run_time)
            return f"Got it. I'll remind you at {hour:02d}:{minute:02d}."
        return "I couldn't parse the time. Try: 'remind me in 10 minutes to stretch'."

    def _speak(self, task: str):
        if self.speaker:
            self.speaker.say(f"Reminder: {task}")
