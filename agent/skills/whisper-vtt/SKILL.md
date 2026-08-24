---
name: whisper-vtt
description: Reads dictated text from Whisper VTT's drop box and routes it — tasks to TASKS.md, lessons to pending-lessons, journal entries, status updates to PROGRESS.md, and dictation sessions into note-taking mode. Use when the user says they dictated something with Jarvis ("process my dictations", "read my dictation", "what did I dictate"), or mentions Jarvis/Whisper VTT.
---

# Whisper VTT bridge

Whisper VTT (the user's offline dictation tool) appends every
transcription to `~/.local/whisper-vtt/inbox/dictations.jsonl`. This skill
reads that drop box and routes the entries.

## Register the pi window (handshake)

Whisper uses a handshake state file to know pi is alive and where its
window is — instead of AppleScript title-guessing. Run this at session
start and again after responding to dictations:

```bash
cd ~/projects/whisper-vtt && python3 scripts/pi_handshake.py --title "PI Code — <project>" --host Code
```

(`python3 scripts/pi_handshake.py --check` prints the current state.)
A stale file (>30 min) just means the positive evidence expired —
whisper falls back to its own window detection.

## Read the inbox

```bash
cd ~/projects/whisper-vtt && .venv/bin/python scripts/read_dictations.py            # all unprocessed dictations
cd ~/projects/whisper-vtt && .venv/bin/python scripts/read_dictations.py --latest   # only the newest entry
```

(The scripts import `src.dropbox`, which needs the project venv —
the stock macOS `python3` is 3.9 and can't parse it.)

## Clear after processing

```bash
cd ~/projects/whisper-vtt && .venv/bin/python scripts/clear_dictations.py   # archives the inbox file
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
| `kind: "session_start"` | Enter note-taking mode (below) for that session id/title |
| `kind: "session"` | Commit the session: merge items, file notes, close mode (below) |
| no prefix | Treat the text as the user's message/input — act on it (unless note-taking mode is active, below) |

## Dictation sessions — note-taking mode

A dictation session is the flow where the user kicks off with a spoken
command and Whisper becomes the ears: pi must NOT interpret the kickoff
or its items as commands. Two producers feed this mode:

1. **Whisper's own routing** — a matching kickoff is consumed by whisper
   (never pasted) and journals `{"kind": "session_start", "id", "title"}`
   then delivers "process my dictations". Items accumulate in whisper and
   arrive on commit as `{"kind": "session", "id", "title", "items"}`.
2. **Fallback** — when the user's phrasing escaped whisper's parser, the
   kickoff arrives as a plain message. Recognize it yourself.

### Kickoff patterns (fallback)

A message (dictated or typed) that matches any of these is a session
kickoff, not a command:

- `start (a new) session (for|about|on) <topic>`
- `start and use session (for|about|on) <topic>`
- `session (for|about|on) <topic>` / `session <stuff> for <more>`
- `take notes (for|about|on) <topic>` / `start a session to take notes …`
- `note-taking session (for|about|on) <topic>`

On any of these (or a `session_start` drop-box entry):

```bash
python3 ~/.pi/agent/skills/whisper-vtt/scripts/session_state.py start "<topic or title>"
```

Then reply with exactly one line acknowledging the mode, e.g.
"Note-taking session open: <topic>. Whisper is the ears — dictate notes;
'that's all' commits them." **Do not start work, plans, or files.**

### While the mode is active

- `session_state.py status` shows the open session (age included).
- **A dictated entry** (matches the newest drop-box entry) is a NOTE,
  never a command:
  ```bash
  python3 ~/.pi/agent/skills/whisper-vtt/scripts/session_state.py note "<text>"
  ```
  Reply at most `✓ n` (item count). Do not act on the content.
- **A typed message** (no matching drop-box entry) is still a command —
  the user may need to interrupt ("abort the session").
- A dictated end phrase while mode is active ("that's all", "end session",
  "done", "finish session") → commit immediately (below).

### Committing

On a `kind: "session"` drop-box entry (or a dictated end phrase):

1. Write whisper's items to a temp JSON array file, e.g.
   `~/.pi/agent/dictation-session-items.json` (a JSON list of strings).
2. ```bash
   python3 ~/.pi/agent/skills/whisper-vtt/scripts/session_state.py commit --items-file ~/.pi/agent/dictation-session-items.json
   ```
3. The helper merges whisper's items with pi's buffered notes (deduped,
   order preserved) and files them as numbered notes in a dated markdown
   file — `<project>/.agent/notes/YYYY-MM-DD-<slug>.md` when the topic
   names a project under `~/projects/`, else
   `~/.pi/agent/dictation-sessions/`. It clears the mode state.
4. Recap in one or two lines: where the notes landed and how many items.
   Offer: "say 'make these tasks' to file them into TASKS.md instead."
5. Archive the processed inbox entries (clear command above).

If the user says "make these tasks" after a commit, convert the most
recent session notes file into `- [ ]` items in the project's TASKS.md
under a titled heading.

### Aborting / staleness

- "abort the session" (typed or dictated) →
  `session_state.py abort` — discard, no file written.
- A state file older than 2 hours is stale — `start` replaces it; never
  merge an old buffer into a new session.

## Config commands (no prefix)

Dictations that ask to change whisper's output mode arrive as plain
messages. Act on them with the bridge script:

```bash
cd ~/projects/whisper-vtt && .venv/bin/python scripts/set_mode.py <mode>
```

Valid modes: `clipboard` | `auto_paste` (auto-send off) | `auto_send`
(auto-send on, always Enter) | `protected` (spoken 'Enter' trigger +
pi-window guard). The script validates, rewrites `config.toml`
atomically, and exits 1 on an invalid mode.

Whisper hot-reloads config.toml (~1s poll) — the mode change applies on
the next dictation. **No restart needed.**

## Spoken per-dictation override

"…without sending" / "paste this without sending" / "don't send" / "just
paste" suppress the Enter for that one dictation in every mode, and the
phrase is stripped from the text before pasting/journaling.

After filing, run the clear command and confirm to the user what was
filed where.

For the full command reference with examples, read
`references/jarvis-guide.md` when the user asks how to use Jarvis.
