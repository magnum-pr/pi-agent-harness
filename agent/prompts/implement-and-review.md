---
description: Worker executes an approved plan, reviewer verifies + runs gates, worker applies feedback. For already-planned work.
---
Use the subagent tool with the chain parameter to execute this workflow:

1. First, use the "worker" agent to implement: $@
2. Then, use the "reviewer" agent to review the implementation and run the acceptance gates (use {previous} placeholder)
3. Then, use the "worker" agent to apply the reviewer's feedback and re-run gates (use {previous} placeholder)

Execute as a chain, passing output via {previous}. Only use after a plan is already approved.
