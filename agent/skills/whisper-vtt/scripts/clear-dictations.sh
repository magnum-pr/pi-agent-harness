#!/bin/bash
# Archive Whisper VTT's dictation inbox (call AFTER filing the entries).
set -euo pipefail

INBOX_DIR="$HOME/.local/whisper-vtt/inbox"
INBOX="$INBOX_DIR/dictations.jsonl"

if [ ! -f "$INBOX" ]; then
  echo "(nothing to clear)"
  exit 0
fi

STAMP="$(date +%Y%m%d-%H%M%S)"
ARCHIVE="$INBOX_DIR/processed-$STAMP.jsonl"
mv "$INBOX" "$ARCHIVE"
echo "archived inbox → $ARCHIVE"
