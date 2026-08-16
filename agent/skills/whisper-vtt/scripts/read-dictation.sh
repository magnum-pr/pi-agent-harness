#!/bin/bash
# Read Whisper VTT's dictation drop box.
# Usage: read-dictation.sh [--latest]
set -euo pipefail

INBOX="$HOME/.local/whisper-vtt/inbox/dictations.jsonl"

if [ ! -f "$INBOX" ]; then
  echo "(no dictations in the inbox)"
  exit 0
fi

if [ "${1:-}" = "--latest" ]; then
  tail -n 1 "$INBOX" | python3 -c '
import sys, json
try:
    entry = json.loads(sys.stdin.read())
    print(entry["text"])
except Exception:
    print("(inbox empty or unreadable)")
'
else
  python3 -c '
import sys, json, datetime
for line in sys.stdin:
    line = line.strip()
    if not line:
        continue
    try:
        entry = json.loads(line)
        ts = datetime.datetime.fromtimestamp(entry["ts"]).strftime("%Y-%m-%d %H:%M")
        text = entry["text"]
        print(f"[{ts}] {text}")
    except Exception:
        print(f"(unreadable) {line[:80]}")
' < "$INBOX"
fi
