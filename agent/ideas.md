
## 2026-08-20 — LLM on a Raspberry Pi / smart watch

**Idea:** run a small LLM/AI model on a Raspberry Pi (or Arduino-class
board) and potentially incorporate it into a smart-watch form factor.

**Technical reality check for later:**
- Raspberry Pi (4/5, 8GB) runs quantized 1–3B models via llama.cpp /
  llama_cpp_python at a few tokens/sec — usable for small assistants.
  A Coral USB/Edge TPU or Hailo-8 accelerates inference further.
- Arduino-class MCUs (ESP32 etc.) can't run LLMs — no RAM/MMU. Their
  role in a watch is UI/sensors/mic, with the LLM on a companion
  (Pi, phone, or cloud endpoint).
- Watch form factor: battery + thermals are the real constraints;
  a realistic v1 is watch-MCU streaming audio to a Pi/phone running
  the model.

**Status:** idea — not planned. No repo, no hardware assumptions yet.

## 2026-08-20 — Media scanner → Plex library app

**Idea:** an app that scans a catalog (e.g., DC Animated Movies),
finds media, organizes by shows/movies/titles, and downloads into an
external drive / Plex server.

**Boundary note:** the auto-search-and-download-torrents-of-copyrighted-
media version I can't help build (copyright infringement — that's not a
technical gray area). The legitimate core IS buildable and useful:
- a media-library manager: scan an existing drive, match files to
  metadata (TMDB API), rename/organize shows → seasons → episodes,
  sync with a Plex server, report missing episodes
- Radarr/Sonarr already do most of the "download + organize for Plex"
  workflow if the user sources content legally — a project could be a
  cleaner custom front-end/scheduler on top of them
- the catalog-scanning part (title lists, what's released vs owned)
  is a fine standalone tool

**Status:** idea — buildable parts: library organizer, metadata
matcher, Plex sync, catalog tracker. Off-limits parts: torrent
search/auto-download of copyrighted media.

## 2026-08-20 — AlignMe online classes (future)

Owner intent: studio is local-Central for now (Calendly timezone locked
to Central); online/virtual classes planned for the future.

Thinking notes for later:
- Calendly supports Zoom/Google Meet "locations" per event type — an
  online offering is mostly new event types with a video location,
  not new code
- Site side: a "Book online" variant of the service cards + copy
  ("in-studio or from anywhere"), and the booking panel embeds those
  event types
- Pricing/availability may differ for virtual (shorter sessions,
  different rates) — worth a separate event type per service
- Zoho messaging unchanged; the review engine works for virtual too

## 2026-08-21 — Phone ⇄ Pi connection (deferred — follow up)

Owner wants to interact with pi from the phone AND receive pings
(gardening completion, alerts).

Plan:
- pings: **ntfy.sh** free push — launchd jobs end with a curl to a
  topic; phone app shows it. Needs: owner installs ntfy + gives a topic.
  (Gardening job currently runs Sun 8:00 AM — wire the ping when topic is set.)
- interactive: **Tailscale** on Mac + iPhone, then **Blink/Termius** SSH
  → run pi in a session from anywhere.
- bigger/later: route **phone dictation into pi** + replies back to
  phone (natural evolution of the existing Whisper VTT dictation loop).

## 2026-09-13 — Mute / stop-replies control (PiWeb + Whisper VTT)

**Idea:** a way to silence the agent while the user is listening to something
else (a phone call, a conversation, ambient audio) — without the agent
replying to transcribed speech it wasn't meant to hear.

**Problem observed:** ambient audio kept arriving as messages, and each one
triggered a reply. Telling the agent "do not respond" did NOT stop the reply
loop, because every incoming message still produces a turn. The agent's own
acknowledgements were themselves interruptions.

**Proposed functionality:**
- **PiWeb:** a mute / hard-pause control that stops the agent generating
  replies to incoming messages until unmuted — a real state, not a prompt
  instruction. Ideally also a "listen-only" mode that transcribes but never
  responds.
- **Whisper VTT:** a hotkey and/or voice command ("stop", "mute") that halts
  forwarding transcription into the agent, plus ambient-noise suppression so
  background conversation isn't captured as input.
- **Both:** suppress auto-replies to messages flagged as ambient/inaudible, and
  make "stop responding" a first-class command rather than a suggestion.

**Status:** feature request — not planned. No repo/design yet.
