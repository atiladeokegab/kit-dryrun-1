"""python3 -m triage FILE [--json]"""
import argparse
import json
import sys

from triage.model import URGENCIES, Triage


def rank(items):
    return sorted(items, key=lambda t: (URGENCIES.index(t.urgency), t.message.id))


def as_dict(t: Triage):
    m = t.message
    return {"id": m.id, "urgency": t.urgency, "category": t.category, "sender": m.sender,
            "received": m.received, "text": m.text, "reason": t.reason}


def render_json(items):
    return json.dumps([as_dict(t) for t in items], indent=2, ensure_ascii=False)


def render_table(items):
    rows = [("#", "URGENCY", "CATEGORY", "SENDER", "TEXT", "REASON")]
    for t in items:
        text = " ".join(t.message.text.split())
        rows.append((str(t.message.id), t.urgency.upper(), t.category, t.message.sender[:20],
                     text[:57] + "..." if len(text) > 60 else text, t.reason))
    widths = [max(len(r[i]) for r in rows) for i in range(len(rows[0]))]
    return "\n".join(" | ".join(c.ljust(w) for c, w in zip(r, widths)).rstrip() for r in rows)


def main(argv=None):
    ap = argparse.ArgumentParser(prog="triage", description=__doc__)
    ap.add_argument("file")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        with open(args.file, encoding="utf-8", errors="replace") as f:
            text = f.read()
    except OSError as e:
        print(f"triage: cannot read {args.file}: {e.strerror}", file=sys.stderr)
        return 2
    # The areas are imported here so the core works before they exist.
    from triage.classify import classify
    from triage.ingest import split

    items = rank(classify(m) for m in split(text))
    print(render_json(items) if args.json else render_table(items))
    return 0


if __name__ == "__main__":
    sys.exit(main())
