# 30-second demo

Tenant messages arrive as a mixed dump; the CLI turns them into a ranked triage list.

From a clean checkout of `main`, at the repo root, run these commands in order:

```sh
python3 -m triage samples/monday.txt
python3 -m triage samples/monday.txt --json | python3 -m json.tool
```

| Time | Say and show |
|---|---|
| 0–5s | “This is a morning's email, SMS and voicemail in one file.” |
| 5–18s | Run the first command. Point to row 1: Priya's burst pipe is **emergency / leak** and the **REASON** column says `burst`. The gas smell and sparking switch also rise above routine messages. |
| 18–30s | Run the second command. Point to the same first message's `urgency`, `category`, and `reason` fields in the formatted JSON. |
