---
id: subagent-theatre
status: avoid
evidence:
  - subagent-isolation
---
# Subagent theatre

A workflow creates workers without useful context, permission, model, or responsibility separation.

## Symptoms

- a worker returns one boolean or count;
- every worker refetches the same evidence;
- parent and worker prompts are nearly identical;
- workers need constant back-and-forth;
- total latency and tokens rise without quality gain;
- the agent tree looks sophisticated but the task remains serial.

## Better boundary

Use a script or direct tool for exact work. Keep reasoning in the parent unless a separate context, tool policy, or independent parallel job has measured value.

## Proof required

Compare against one agent. Track total and wall-clock latency, token cost, duplicated calls, worker failures, and task success.

See [Lab 05](../labs/05-premature-subagents/README.md).

**Evidence:** `subagent-isolation`, `start-single-agent`
