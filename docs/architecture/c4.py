# /// script
# requires-python = ">=3.11"
# dependencies = ["diagrams"]
# ///
"""C4 diagrams for <SYSTEM>. Copy this file, replace the example nodes, run it.

    uv run c4.py            # writes c4_context.png ... c4_code.png beside this file
    uv run c4.py context    # just one level

While planning it lives at ~/hub/projects/<repo>/c4.py and draws the PLANNED system,
levels 1-3 only. After the build it moves to docs/architecture/c4.py in the repo and
draws the REAL code, level 4 included. The inline dependency above means nothing is
added to the repo's pyproject.
"""

import shutil
import sys
from pathlib import Path

from diagrams import Cluster, Diagram, Edge
from diagrams.c4 import Container, Database, Person, Relationship, System, SystemBoundary
from functools import partial

# diagrams.c4 wraps text at 40 characters but draws 2.6in boxes, which fit about 34:
# lines of 35-40 characters were cut off, silently. 3.3in fits the full wrap width.
Container, Database, Person, System = (partial(f, width="3.3") for f in (Container, Database, Person, System))
from diagrams.programming.language import Python

SYSTEM = "triage"  # <- the system's name
# Look at every PNG before showing it to anyone.
OUT = Path(__file__).parent
GRAPH = {"splines": "spline", "nodesep": "0.8", "ranksep": "1.1"}


def draw(level, title):
    return Diagram(f"{SYSTEM} - {title}", filename=str(OUT / f"c4_{level}"), outformat="png",
                   show=False, direction="TB", graph_attr=GRAPH)


def context():
    """Level 1: who uses it and what it depends on. The system is ONE box."""
    with draw("context", "System Context"):
        user = Person("Letting agent", "Needs the urgent tenant messages first")
        system = System(SYSTEM, "Turns a dump of tenant messages into a triage list")
        src = System("Message dump", "Emails, SMS, transcripts pasted into one file", external=True)
        user >> Relationship("runs on a file") >> system
        system >> Relationship("reads") >> src


def container():
    """Level 2: the separately running or deployed pieces, and how they talk."""
    with draw("container", "Containers"):
        user = Person("Letting agent", "")
        with SystemBoundary(SYSTEM):
            cli = Container("triage CLI", "Python 3 stdlib", "python3 -m triage FILE [--json]")
        dump = System("Message dump", "Text file: samples/monday.txt or any dump", external=True)
        user >> Relationship("runs") >> cli
        cli >> Relationship("reads") >> dump


def component():
    """Level 3: inside ONE container. Name the container in the title."""
    with draw("component", "Components of the triage CLI"):
        with SystemBoundary("triage CLI"):
            main = Container("CLI", "triage/__main__.py (core)", "Args, sort, table or JSON")
            model = Container("Message model", "triage/model.py (core)", "Message, Triage dataclasses")
            ingest = Container("Ingest", "triage/ingest/", "Splits messy text into Messages")
            classify = Container("Classify", "triage/classify/", "Keyword rules: urgency, category, reason")
        main >> Relationship("split(text)") >> ingest
        main >> Relationship("classify(msg)") >> classify
        ingest >> Relationship("builds") >> model
        classify >> Relationship("returns Triage") >> model


def code():
    """Level 4: classes and key signatures, from the real code."""
    with draw("code", "Code"):
        with Cluster("triage/"):
            main = Python("__main__.py\n——\n+ main(argv) → int\n+ rank(items) → list[Triage]\n+ render_table(items) → str\n+ render_json(items) → str")
            model = Python("model.py\n——\nMessage(id, text, sender, received)\nTriage(message, urgency, category, reason)\nURGENCIES, CATEGORIES")
            ingest = Python("ingest/__init__.py\n——\n+ split(text)\n  → list[Message]")
            classify = Python("classify/__init__.py\n——\n+ classify(msg)\n  → Triage")
        main >> Edge(label="split") >> ingest
        main >> Edge(label="classify") >> classify
        ingest >> Edge(label="builds") >> model
        classify >> Edge(label="returns") >> model


# Only the levels defined above: while planning, code() is deleted, not stubbed.
LEVELS = {n: globals()[n] for n in ("context", "container", "component", "code") if n in globals()}

if __name__ == "__main__":
    if not shutil.which("dot"):
        sys.exit("c4: Graphviz is not installed (no `dot` on PATH). Run: sudo apt install -y graphviz")
    for name in sys.argv[1:] or LEVELS:
        LEVELS[name]()
        print(OUT / f"c4_{name}.png")
