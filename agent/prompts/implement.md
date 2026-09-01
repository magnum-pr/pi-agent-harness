---
description: Full tiered implementation - scout gathers context once (cheap), planner creates plan (cheap, gated), worker executes (expensive, once), reviewer verifies (cheap)
---
Use the subagent tool with the chain parameter to execute this workflow:

1. First, use the "scout" agent to find all code relevant to: $@
2. Then, use the "planner" agent to create an implementation plan for "$@" using the scout's context (use {previous} placeholder)
3. Return the plan to the orchestrator for APPROVAL before proceeding - do NOT implement yet
4. After approval, use the "worker" agent to implement the approved plan (use {previous} placeholder)
5. Finally, use the "reviewer" agent to review the implementation and run the acceptance gates (use {previous} placeholder)

Execute as a chain, passing output between steps via {previous}. STOP after step 2 and await approval.
