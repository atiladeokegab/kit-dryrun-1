"""Split a raw tenant-message dump into messages."""

import re

from triage.model import Message


_SEPARATOR = re.compile(r"(?:-{3,}|\*{3}|—)\Z")
_SMS_TIME = re.compile(r"\[(\d{2}:\d{2})\]\s+([^:]+):\s*(.*)\Z")
_SMS_DATE = re.compile(r"(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2})\s+-\s+([^:]+):\s*(.*)\Z")
_VOICEMAIL = re.compile(r"(Voicemail\s+\d{2}:\d{2}):\s*(.*)\Z", re.I)
_HEADER = re.compile(r"(From|To|Subject|Date):\s*(.*)\Z", re.I)


def split(text: str) -> list[Message]:
    messages: list[Message] = []
    body: list[str] = []
    sender = received = ""
    email = pending_blank = False

    def flush() -> None:
        nonlocal sender, received, email
        content = "\n".join(body).strip()
        if content:
            messages.append(Message(len(messages) + 1, content, sender, received))
        body.clear()
        sender = received = ""
        email = False

    for raw in text.splitlines():
        line = raw.strip()
        if _SEPARATOR.fullmatch(line):
            flush()
            pending_blank = False
            continue
        if not line:
            pending_blank = True
            continue

        header = _HEADER.fullmatch(line)
        sms = _SMS_TIME.fullmatch(line) or _SMS_DATE.fullmatch(line)
        voicemail = _VOICEMAIL.fullmatch(line)
        signoff = email and body and sender and line.casefold() == sender.split()[0].casefold()
        if (header and header[1].lower() == "from") or sms or voicemail or (pending_blank and body and not signoff):
            flush()
        pending_blank = False

        if header and (email or header[1].lower() == "from") and not body:
            email = True
            if header[1].lower() == "from":
                sender = header[2].strip()
            elif header[1].lower() == "date":
                received = header[2].strip()
        elif sms:
            received, sender = sms[1].strip(), sms[2].strip()
            body.append(sms[3].strip())
        elif voicemail:
            received = voicemail[1].strip()
            body.append(voicemail[2].strip())
        else:
            body.append(line)

    flush()
    return messages
