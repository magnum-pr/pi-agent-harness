---
description: Scout gathers context, planner creates plan. NO implementation - returns the plan for approval.
---
Use the subagent tool with the chain parameter to execute this workflow:

1. First, use the "scout" agent to find all code relevant to: $@
2. Then, use the "planner" agent to create an implementation plan for "$@" using the scout's context (use {previous} placeholder)

Execute as a chain, passing output via {previous}. Do NOT implement - just return the plan for the orchestrator's approval.
