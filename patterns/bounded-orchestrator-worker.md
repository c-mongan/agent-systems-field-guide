---
id: bounded-orchestrator-worker
status: recommended
evidence:
  - subagent-isolation
---
# Bounded orchestrator-worker

Use one coordinator and a small number of workers with explicit goals and evidence contracts.

## Orchestrator owns

- task decomposition;
- shared evidence snapshot;
- worker selection;
- conflict resolution;
- final synthesis;
- user-facing result.

## Worker owns

- one independent investigation;
- only the tools and context needed for it;
- a bounded output schema;
- explicit unknowns and evidence IDs.

```text
Coordinator
   ├─ application worker
   ├─ database worker
   └─ provider worker
          ↓
compact evidence results
          ↓
Coordinator synthesis
```

## Guardrails

- do not create a worker for one deterministic call;
- do not let every worker refetch shared evidence;
- cap context, time, and tool permissions;
- require compact output;
- define what happens when one worker fails;
- parallelize only independent work.

## Proof

Compare against the one-agent baseline. Track wall-clock time, total tokens, duplicated calls, contradictory outputs, and final task success.

**Evidence:** `subagent-isolation`, `start-single-agent`
