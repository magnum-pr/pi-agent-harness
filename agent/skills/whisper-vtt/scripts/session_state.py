#!/usr/bin/env python3
"""Pi-side dictation-session state helper (whisper-vtt skill support).

Manages ~/.pi/agent/dictation-session.json — the note-taking-mode state
pi uses while a Whisper VTT dictation session is open — and files
committed sessions as dated markdown notes.

Subcommands:
    start <topic...>            Open note-taking mode (topic = rest of argv)
    note <text...>              Append one note to the open session
    status                      Print the state as JSON (age included)
    commit [--items-file PATH]  Merge whisper items + buffered notes,
                                dedupe, write the notes file, clear state
    abort                       Discard the open session

Works on Python 3.9+ (macOS stock interpreter included).

Notes destination: <project>/.agent/notes/ when the topic names a
project under ~/projects/ (normalized substring match on the dir name),
else ~/.pi/agent/dictation-sessions/. Filenames are collision-safe
(-2, -3 suffixes).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Optional

AGENT_DIR = Path(os.path.expanduser("~/.pi/agent"))
STATE_FILE = AGENT_DIR / "dictation-session.json"
SESSIONS_DIR = AGENT_DIR / "dictation-sessions"
PROJECTS_DIR = Path(os.path.expanduser("~/projects"))
STALE_AFTER_S = 2 * 60 * 60  # sessions older than this are treated as stale


def _now() -> float:
    return time.time()


def _slug(topic: str, max_len: int = 48) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", topic.lower()).strip("-")
    return slug[:max_len].strip("-") or "session"


def _normalize(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def _detect_project(topic: str) -> Optional[Path]:
    """Project whose dir name appears in the topic, most specific wins."""
    if not PROJECTS_DIR.is_dir():
        return None
    normalized_topic = _normalize(topic)
    best: Optional[Path] = None
    for entry in PROJECTS_DIR.iterdir():
        if not entry.is_dir() or entry.name.startswith("."):
            continue
        name = _normalize(entry.name)
        if name and name in normalized_topic:
            if best is None or len(name) > len(_normalize(best.name)):
                best = entry
    return best


def _read_state() -> Optional[dict]:
    try:
        with open(STATE_FILE, encoding="utf-8") as f:
            return json.load(f)
    except (OSError, ValueError):
        return None


def _write_state(state: dict) -> None:
    AGENT_DIR.mkdir(parents=True, exist_ok=True)
    tmp = STATE_FILE.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp, STATE_FILE)


def cmd_start(topic: str) -> int:
    existing = _read_state()
    if existing is not None:
        age = _now() - existing.get("started_at", 0)
        if age < STALE_AFTER_S:
            print(
                "error: session already open "
                f"({age / 60:.1f}m old, topic '{existing.get('topic')}') — "
                "run 'abort' first"
            )
            return 1
        # Stale — discard silently and start fresh.
        STATE_FILE.unlink(missing_ok=True)

    project = _detect_project(topic)
    state = {
        "topic": topic,
        "started_at": _now(),
        "project": str(project) if project else None,
        "notes": [],
    }
    _write_state(state)
    dest = project or SESSIONS_DIR
    print(f"session started: {topic!r} -> {dest}")
    return 0


def cmd_note(text: str) -> int:
    state = _read_state()
    if state is None:
        print("error: no open session — run 'start' first")
        return 1
    state.setdefault("notes", []).append(text)
    _write_state(state)
    print(f"noted ({len(state['notes'])}): {text}")
    return 0


def cmd_status() -> int:
    state = _read_state()
    if state is None:
        print("no open session")
        return 0
    age = _now() - state.get("started_at", 0)
    state["age_seconds"] = round(age, 1)
    state["stale"] = age >= STALE_AFTER_S
    print(json.dumps(state, ensure_ascii=False, indent=2))
    return 0


def _load_items_file(path: Optional[str]) -> List[str]:
    """Whisper items from a JSON-array file, or [] when not given.

    Stdin is deliberately not read — shells/harnesses pipe stdin in
    ways that make isatty() unreliable.
    """
    if not path:
        return []
    try:
        with open(path, encoding="utf-8") as f:
            payload = json.load(f)
    except (OSError, ValueError) as e:
        print(f"error: could not read items file: {e}")
        return []
    if not isinstance(payload, list):
        print("error: items file must contain a JSON array")
        return []
    return [str(i) for i in payload if str(i).strip()]


def _dedupe(ordered: List[str]) -> List[str]:
    seen = set()
    out = []
    for item in ordered:
        key = item.strip().lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(item.strip())
    return out


def _destination(state: dict) -> Path:
    project = state.get("project")
    if project:
        return Path(project) / ".agent" / "notes"
    return SESSIONS_DIR


def _notes_path(state: dict) -> Path:
    base = _destination(state)
    today = datetime.now().strftime("%Y-%m-%d")
    name = f"{today}-{_slug(state.get('topic', ''))}.md"
    path = base / name
    n = 2
    while path.exists():
        path = base / f"{today}-{_slug(state.get('topic', ''))}-{n}.md"
        n += 1
    return path


def cmd_commit(items_file: Optional[str]) -> int:
    state = _read_state()
    if state is None:
        print("error: no open session — nothing to commit")
        return 1
    whisper_items = _load_items_file(items_file)
    merged = _dedupe(state.get("notes", []) + whisper_items)
    if not merged:
        print("session has no notes — nothing filed; state cleared")
        STATE_FILE.unlink(missing_ok=True)
        return 0

    path = _notes_path(state)
    path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now()
    lines = [
        f"# {state.get('topic', 'Dictation session')} — {now.strftime('%Y-%m-%d')}",
        "",
        f"> Whisper VTT dictation session · {len(merged)} item(s) · "
        f"committed {now.strftime('%H:%M')}",
        "",
    ]
    for i, item in enumerate(merged, 1):
        lines.append(f"{i}. {item}")
    lines.append("")
    tmp = path.with_suffix(".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    os.replace(tmp, path)

    STATE_FILE.unlink(missing_ok=True)
    print(f"filed {len(merged)} item(s) -> {path}")
    return 0


def cmd_abort() -> int:
    if STATE_FILE.exists():
        STATE_FILE.unlink()
        print("session aborted")
    else:
        print("no open session")
    return 0


def main(argv: List[str]) -> int:
    parser = argparse.ArgumentParser(
        prog="session_state.py",
        description="Pi-side dictation-session state helper (whisper-vtt skill)",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_start = sub.add_parser("start", help="open note-taking mode")
    p_start.add_argument("topic", nargs="+")

    p_note = sub.add_parser("note", help="append a note")
    p_note.add_argument("text", nargs="+")

    sub.add_parser("status", help="print state as JSON")
    sub.add_parser("abort", help="discard the open session")

    p_commit = sub.add_parser("commit", help="file notes and close")
    p_commit.add_argument("--items-file", default=None)

    args = parser.parse_args(argv)
    if args.command == "start":
        return cmd_start(" ".join(args.topic))
    if args.command == "note":
        return cmd_note(" ".join(args.text))
    if args.command == "status":
        return cmd_status()
    if args.command == "commit":
        return cmd_commit(args.items_file)
    if args.command == "abort":
        return cmd_abort()
    parser.error("unknown command")
    return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
