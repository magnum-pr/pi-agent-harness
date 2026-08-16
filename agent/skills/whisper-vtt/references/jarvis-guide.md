# Talking to Jarvis — command reference

Jarvis is the wake word for Whisper VTT, the offline dictation tool. Say
**"jarvis"**, speak, pause ~3 seconds, and the transcription lands in pi
(auto-paste) or in the drop box. A prefix keyword tells pi what to do
with it — the keywords are just natural speech.

## task — capture work for later

Say it while driving, walking, or mid-thought; pi files it into
`TASKS.md` when you next say "process my dictations".

> "Jarvis, task: reorder the schedule section on the homepage"
> "Jarvis, task: write tests for the carousel wrap-around"
> "Jarvis, task: ask Sharon about private-session pricing"

## lesson — things you never want to relearn

Goes to `.agent/lessons-pending.md`; the gardening flow promotes it into
LESSONS.md so future sessions carry the warning.

> "Jarvis, lesson: never close an audio stream from inside its own callback"
> "Jarvis, lesson: Vercel needs Node 22 — local Node 18 won't build"
> "Jarvis, lesson: the client prefers terracotta, not green"

## journal — context and decisions worth keeping

Decisions, meeting notes, client feedback — anything that should survive
the session.

> "Jarvis, journal: Sharon confirmed Dance $65, Kinetic $35"
> "Jarvis, journal: the deploy timeout is a Vercel function limit"
> "Jarvis, journal: client meeting — wants the booking form first"

## status — track your work

One line into PROGRESS.md; pi boots with it next session. Narrate as you
work and you'll never lose the thread.

> "Jarvis, status: merged testimonials, starting the mic meter"
> "Jarvis, status: blocked on Stripe keys, waiting on client"
> "Jarvis, status: RED test written for goTo, implementing now"

## note — plain voice note

Shown to you, not filed.

> "Jarvis, note: pick up milk on the way home"

## plain dictation — just talk to pi

No prefix → pi treats it as your message and acts on it. End with the
word "Enter" and auto-send will submit it for you.

> "Jarvis, fix the bug on the homepage, Enter"
> "Jarvis, explain why the build is slow"

## In pi, after dictating

Say **"process my dictations"** — pi reads the drop box, files every
entry, and tells you where each one went.
