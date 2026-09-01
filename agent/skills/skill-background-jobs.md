---
name: background-jobs
description: Orchestrator background dispatch — offer to run long-running, self-contained tasks in a background session once the plan is solidified, with a mandatory parameter gate. Use when a task is background-eligible (long-running, multi-step, independent of the live conversation) or when dispatching work to an orchestrator / tiered agent pipeline. Complements grill (extract params) and edit-gate (checkpoint).
---

# Skill: Background Jobs (Orchestrator Dispatch)

The loop for turning an idea into executed work, with a guardrail that
prevents a runaway queue.

## The loop

```
① IDEA   ──▶  you have a proposition
② GRILL  ──▶  I interrogate it → assumptions, scope, failure modes, done-when
              → solidified plan (saved to .agent/grill/<topic>.md)
③ OFFER  ──▶  once the plan is solid, IF long-running / self-contained:
              "want me to run this in the background?" (mandatory params if yes)
④ EXEC   ──▶  synchronous (in-turn) or background, per your choice
```

## When to load
- A task is long-running, multi-step, or self-contained (doesn't need live
  back-and-forth to finish).
- You describe something you'd like to keep talking while it runs.
- Dispatching work to an orchestrator / tiered pipeline (scout→planner→
  worker→reviewer) or any background session.

## Hard rules

1. **Background is an OFFER, never the default.** I propose it; you decide.
   Normal chatter never auto-queues work.
2. **Default is synchronous.** Background only happens when you opt in.
3. **No dispatch without parameters.** I don't fire a background job on a
   vague or half-formed request. I list what's missing and wait.
4. **Offer only AFTER the plan is solidified** (grill first, then offer).
   A vague idea never gets the background pitch.
5. **One background job at a time.** If one is running and you opt into
   another, I tell you it queues before adding it — the queue is visible,
   never silent.

## Mandatory parameter gate (for background dispatch)

These are all required before dispatch — NOT the edit-gate's 2-of-3. You
can't interrupt a background pipeline mid-flight, so the plan must be
concrete:

1. **Scope** — what the job does AND what it explicitly does NOT touch.
2. **Done-when** — a verifiable success condition (non-negotiable).
3. **Deliverable** — where/how the result lands (file · summary · format).
4. **Capacity** — confirmed one-at-a-time; if a job is already running,
   surface the queue.

Missing any → tell the user exactly what's missing and wait. Never
dispatch on guesses.

## The offer language

When a background-eligible task has a solid plan:

> "This one could run in the background while we keep talking — it's
> [long-running / multi-step / self-contained]. Want me to run it that
> way? If so, I'll need: scope, done-when, and where you want the result."

## Triage (reconcile with grill + edit-gate)

Pick ONE interrogation path per request — never run both:

- **Trivial / mechanical** → no gate, just do it.
- **Ambiguous but simple** → flat edit-gate 2-of-3 (batch questions,
  restate, wait).
- **Genuinely complex / risky** → GRILL (offer it first: "this has hidden
  assumptions — mind if I grill you on it?"). Grill is the question engine
  that fills the parameters; edit-gate is the checkpoint; this skill is the
  router.

## Anti-patterns
- Don't offer background for short/synchronous tasks (context overhead
  with no benefit).
- Don't dispatch a background job without the mandatory gate, even if
  the user seems eager — confirm the plan first.
- Don't let multiple background jobs pile up silently — always surface
  the queue.

## Related skills
- `grill` — upstream: extracts the parameters / solidified plan.
- `edit-gate` — the checkpoint (2-of-3) for synchronous edits and dispatch.
- `plan-then-implement` — when the solidified plan moves into execution.
