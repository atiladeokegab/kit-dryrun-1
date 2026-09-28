# Tiny Hack (kit dry run #1)

Build a small command-line tool that turns a pile of tenant messages into a triage list.
One track. This is a rehearsal event: the brief, data and deadlines are fake.

Official rules: none (rehearsal). The idea and the areas: [IDEA.md](IDEA.md).

Smoke: `python3 -m unittest discover -s tests -t .`

(Once `samples/monday.txt` and both areas have landed, the smoke becomes
`python3 -m unittest discover -s tests -t . && python3 -m triage samples/monday.txt`.)

The product that ships is `main`: the last commit that passed the smoke check.

## Deadlines

Your agent checks these every session against the UTC column.

| Deadline | Event time | UTC |
|---|---|---|
| build start | 2026-09-28T15:22+01:00 | 2026-09-28T14:22Z |
| code freeze | 2026-09-28T16:22+01:00 | 2026-09-28T15:22Z |
| reality test | 2026-09-28T16:32+01:00 | 2026-09-28T15:32Z |
| submit | 2026-09-28T16:47+01:00 | 2026-09-28T15:47Z |

## Judging criteria

- Correct triage: 50%
- Handles messy input: 30%
- Engineering: 20%

## Team

| Name | GitHub | Role |
|---|---|---|
| Atilade | @atiladeokegab | Lead; core (via Zeus), classify (via Prometheus), reviews and merges |
| Matrix | @Atilmatrix | Ingest area |
