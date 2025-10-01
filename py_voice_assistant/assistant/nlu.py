from __future__ import annotations
import regex as re
from typing import Optional, Tuple, List
from assistant.core import Intent

def match_intent(intents: List[Intent], query: str) -> Optional[Tuple[str, dict]]:
    q = query.lower().strip()
    for intent in intents:
        for pat in intent.patterns:
            # treat as regex if it contains special chars, else substring
            if re.search(r"[.^$*+?{}\\[\\]|()]", pat):
                m = re.search(pat, q, flags=re.I)
                if m:
                    return intent.name, (m.groupdict() if m else {})
            else:
                if pat in q:
                    return intent.name, {}
    return None
