# The idea

Zeus writes this once the lead has agreed the idea, and no issue is created before it is
complete. If your task doesn't fit this page, open a change-request (AGENTS.md §7).

## Problem

A letting agent opens Monday to a pile of tenant messages: emails, SMS, voicemail
transcripts, pasted together. A burst pipe sits under a parking complaint, and nobody sees
it until the ceiling comes down.

## The idea

`triage` is a command-line tool: give it a messy text dump of tenant messages and it splits
them apart, tags each with an urgency (emergency, urgent, routine) and a category (leak,
heating, electrical, pest, noise, admin, other) by keyword rules, and prints them
most-urgent-first.

## What we build

- Split a messy dump into messages: blank lines, `---` separators, email headers, SMS timestamps
- Urgency and category by keyword rules, with the matched words as the reason
- `python3 -m triage FILE` prints a table, most urgent first; `--json` prints JSON
- A sample dump in `samples/` covering the messy cases

## What we don't build

- An LLM classifier (needs a key and makes the smoke non-deterministic)
- A web UI, a database, email or SMS integration
- Any dependency outside the Python standard library

## The demo, in one line

`python3 -m triage samples/monday.txt` turns 12 tangled messages into a list with the burst pipe on top.

## Areas and owners

Each person owns their area's directories outright (AGENTS.md §6). The core is the shared
contracts; only the lead changes it.

| Area | Directories | Owner | Issues |
|---|---|---|---|
| core | `triage/__init__.py`, `triage/__main__.py`, `triage/model.py`, `tests/__init__.py`, `tests/test_cli.py` | @atiladeokegab (Zeus) | #1 |
| ingest | `triage/ingest/`, `tests/ingest/` | @Atilmatrix | #2 |
| classify | `triage/classify/`, `tests/classify/` | @Atilmatrix (Prometheus, the lead's builder agent) | #3 |
| pool | `samples/`, `docs/demo.md` | pool | #4, #5 |
