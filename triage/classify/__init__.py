"""Keyword triage for tenant messages."""

import re

from triage.model import CATEGORIES, Message, Triage


_EMERGENCY = ("burst", "flood", "flooding", "gas smell", "smell of gas",
              "sparks", "sparking", "fire", "smoke")
_URGENT = ("leak", "leaking", "drip", "no hot water", "boiler",
           "broken lock", "mould", "rats", "mice")
_CATEGORY = {
    "leak": ("burst", "flood", "flooding", "leak", "leaking", "drip", "mould"),
    "heating": ("gas smell", "smell of gas", "no heating", "no hot water", "boiler"),
    "electrical": ("sparks", "sparking", "fire", "smoke"),
    "pest": ("rats", "mice"),
    "noise": ("noise", "noisy", "loud"),
    "admin": ("rent", "parking", "deposit", "invoice", "broken lock"),
}


def _hits(text: str, terms: tuple[str, ...]) -> list[str]:
    return [term for term in terms if re.search(
        r"\b" + re.escape(term).replace(r"\ ", r"\s+") + r"\b", text, re.I)]


def classify(msg: Message) -> Triage:
    emergency = _hits(msg.text, _EMERGENCY)
    if _hits(msg.text, ("no heating",)):
        vulnerable = _hits(msg.text, ("baby", "elderly", "newborn"))
        if vulnerable:
            emergency.extend(("no heating", *vulnerable))
    urgent = _hits(msg.text, _URGENT)
    urgency = "emergency" if emergency else "urgent" if urgent else "routine"

    category, category_hits = "other", []
    for name in CATEGORIES:
        hits = _hits(msg.text, _CATEGORY.get(name, ()))
        if hits:
            category, category_hits = name, hits
            break
    reason = ", ".join(dict.fromkeys((*emergency, *urgent, *category_hits)))
    return Triage(msg, urgency, category, reason)
