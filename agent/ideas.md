
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

## 2026-09-13 — Two voice modes: Awake (wake word) and Sleep (pseudo-sleep)

**Idea:** an explicit "sleep" state for the voice interface, so the agent can be
silenced without the user having to fight the reply loop. (Pivoted from the
earlier "mute / stop-replies" note — this is the concrete design, not a lesson.)

**Triggers → Sleep:** phrases such as _"Oracle, take a break"_, _"just listen"_,
or _"standby"_. The agent acknowledges with a short token — e.g. **"Yes
master."** — mirroring how the wake word already gets "yes?". Then it enters
**Sleep mode**.

**In Sleep mode:** the agent does not reply to, or act on, incoming audio /
transcription. It stays "listening" only. Open question: does it keep
transcribing to the VTT log (probably yes) but suppress all replies, or go fully
dark?

**Wake:** saying _"Wake up"_ returns it to normal **Awake / wake-word mode**.

**Why:** observed live — ambient audio arrived as messages and each one forced a
reply; telling the agent "do not respond" could not stop it, because a reply is
emitted per incoming message. A real mode toggle owned by the runtime is the only
reliable fix (a prompt instruction is not a state).

**Status:** idea / scaffold — belongs in the tech-stack improvement bucket.
Depends on the voice pipeline (PiWeb + Whisper VTT) supporting a global
input-gating state.
