---
name: edit-gate
description: Pre-edit checkpoint for every substantive request — before editing code, confirm at least 2 of 3 core signals (done-when / questions batched / proposal-no-edit), then check the secondary parameters and surface what happens next plus any missing inputs. Use on any non-trivial task.
---

# Edit Gate

Before touching files for a non-trivial request, run a 3-second checkpoint.

## Core gate — the 2-of-3 rule (hard)

Proceed only if at least 2 of these are already true:

1. **Done-when given** — a verifiable success condition exists
   ("done when X passes / Y is visible")
2. **Questions batched** — scope questions were asked/answered in one
   message, not discovered piecemeal
3. **Proposal / no-edit** — the user said "propose only" / "don't edit"
   (then do NO edits, just the proposal)

If fewer than 2 are met, stop and reply with:
- one line: what I understand the request to be
- the missing inputs / questions, batched in one block
- **what happens next** — the next 1–2 steps in the flow

Then wait for the go (trivial single-file mechanical changes are exempt).

## Secondary parameters (default when obvious, ask only when ambiguous)

| Parameter | Default | Ask when |
|---|---|---|
| Scope boundary (what NOT to touch) | smallest related files | change could ripple beyond the obvious |
| Underlying goal ("the why") | the literal ask | literal ask seems like the wrong path |
| Constraints (browser, tz, brand, budget) | current project conventions | request implies new platform/audience |
| Surgical vs free-rein | surgical | user says "improve/polish however" |
| Conventions: follow vs introduce | follow existing | a new pattern/abstraction is tempting |
| Review cadence | autonomous end-to-end | user says "check in" / risky change |
| Risk tolerance (branch vs main) | stable on main | experimental / "try variations" |
| Decision authority | local decisions mine | long-term/architectural choice |
| Deliverable shape | code change | "think about", "plan", "spike", "doc" |
| Assets/keys availability | assume present | integration needs credentials |
| Time budget | a reasonable session | "quick" vs "spend hours on it" |
| Output verbosity | terse recap | user asks for detail |

When 2+ of these are genuinely uncertain, fold the questions into the
same batched block as the core gate — never a second round-trip.

## Tell them what comes next

I know the arc; they know their next step. State briefly:
- "I'll do X first, then Y"
- what I'll need from them later (keys, decisions, assets, approvals)

Keep the whole reply to a few lines. Wait for the go unless the task is
trivial.

## Thinking escalation

Assume low thinking by default. When a task needs deeper reasoning
(architecture, root-cause debugging, wide ripple), tell the user
upfront — "bump thinking to high for this one" — and pause for them to
Shift+Tab before proceeding. Never silently brute-force a high-effort
problem on low.
