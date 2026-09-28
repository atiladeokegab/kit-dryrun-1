"""The shared contract. Only the core changes this file."""
from dataclasses import dataclass

URGENCIES = ("emergency", "urgent", "routine")  # sort order, most urgent first
CATEGORIES = ("leak", "heating", "electrical", "pest", "noise", "admin", "other")


@dataclass(frozen=True)
class Message:
    id: int  # 1-based position in the dump
    text: str  # body, stripped, never empty
    sender: str = ""
    received: str = ""


@dataclass(frozen=True)
class Triage:
    message: Message
    urgency: str  # one of URGENCIES
    category: str  # one of CATEGORIES
    reason: str  # matched keywords, comma-separated; "" if none
