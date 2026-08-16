---
name: whisper-vtt
description: Reads dictated text from Whisper VTT's drop box and routes it — tasks to TASKS.md, lessons to pending-lessons, journal entries, status updates to PROGRESS.md. Use when the user says they dictated something with Jarvis ("process my dictations", "read my dictation", "what did I dictate"), or mentions Jarvis/Whisper VTT.
---

# Whisper VTT bridge

Whisper VTT (the user's offline dictation tool) appends every
transcription to `~/.local/whisper-vtt/inbox/dictations.jsonl`. This skill
reads that drop box and routes the entries.

## Read the inbox

```bash
./scripts/read-dictation.sh            # all unprocessed dictations
./scripts/read-dictation.sh --latest   # only the newest entry
```

## Clear after processing

```bash
./scripts/clear-dictations.sh          # archives the inbox file
```

## Routing rules

Read the entries, then route each one by its spoken prefix. The keywords
are natural speech — the user doesn't type them, they dictate them:

| Prefix | Route |
|---|---|
| `task:` | Append `- [ ] <text>` to the project's `TASKS.md`. If no TASKS.md exists, tell the user and offer to create it |
| `lesson:` | Append to `.agent/lessons-pending.md` (gardening intakes it later) |
| `journal:` | Append to `.agent/journal.md` with a date heading, or a daily journal file |
| `status:` | Append a timestamped line to `PROGRESS.md` (the same format as other session entries) |
| `note:` | Plain voice note — show it to the user, don't file it anywhere |
| no prefix | Treat the text as the user's message/input — act on it |

After filing, run `./scripts/clear-dictations.sh` and confirm to the user
what was filed where.

For the full command reference with examples, read
`references/jarvis-guide.md` when the user asks how to use Jarvis.
