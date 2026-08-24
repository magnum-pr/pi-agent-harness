# Whisper VTT — notes & status

Project: `~/projects/whisper-vtt` (own repo, own PROGRESS/TASKS).

## Behavior (current)
- Idle: wake word "jarvis" only
- Sticky follow-up (20s): onset armed — any speech starts recording
- Compile sessions: each item starts with "note" (configurable compile_trigger)
- Silence auto-stops recording (adaptive VAD + max-duration cap 45s)
- Idle CPU ~5% (was 67–100% — busy-spin fixed)

## Config keys (config.toml)
- `[wake_word] threshold = 1e-10` — stricter "jarvis" (was 1e-20, false triggers)
- `[session] sticky = true`, `onset_enabled = true` (sticky-only onset),
  `compile_trigger = "note"`, `max_duration_s = 45`
- `[output] paste_target` via `scripts/set_target.py`; mode via `scripts/set_mode.py`

## Improvements shipped (WHISPER-004..011)
Adaptive VAD threshold · idle-CPU busy-spin fix · onset scoped to sticky ·
"note" compile trigger · max-duration cap · Calendly-style signature
hardening pattern for webhooks.

## Drop box / skill
`~/.pi/agent/skills/whisper-vtt/` — dictation routing to TASKS/notes/sessions.
