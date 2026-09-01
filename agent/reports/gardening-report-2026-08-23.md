# Gardening Report — 2026-08-23

## Context
Trees cleaned first (committed pending `~/.pi` whisper/settings work and
`alignme` copy/doc/gitignore work). Gardening run on clean trees.

## Passes

- **Pass 1 — Intake (executed):** Reviewed `alignme/.agent/lessons-pending.md`
  (~30 candidates). Most were already folded into global LESSONS.md (Zoho
  OAuth cluster, usage/cost habits, Stripe-integration decision, pkill
  danger). Accepted:
  - **AlignMe `LESSONS.md` (created)** — L-001 (DNS cutover mail-safety),
    L-002 (no hardcoded prices).
  - **Global** — GL-001 (don't paste file contents back; reference by path).
  - Archived reviewed pending → `.agent/archive/lessons-pending-2026-08-23.md`;
    fresh stub.
- **Pass 2 — Merge:** No near-duplicates. No-op.
- **Pass 3 — Demote:** No `lesson-stats.json` telemetry → skipped.
- **Pass 4 — Compress:** Observe-only; global LESSONS ~1.4k tokens, under
  3670 budget. Nothing to compress.
- **Pass 5 — Progress horizon:** All entries <30 days; nothing to archive.
  Active project; narrative kept intact.
- **Pass 6 — Sweeps:** `.agent/grill` files 8 days old (<45-day max). No-op.
- **Passive re-run:** Confirmed lesson files present, budget under, no
  further action.

## Changes made
- New `alignme/LESSONS.md` (L-001, L-002).
- Global `~/.pi/agent/LESSONS.md` + GL-001.
- Archived reviewed pending lessons.
- Commits: `alignme 1678621`; `~/.pi` whisper/config commit `fbf1df4`.

## Tokens/budget
Global LESSONS.md 5552 bytes (~1.4k tokens) — under 3670 budget.
