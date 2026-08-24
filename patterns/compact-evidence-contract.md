---
id: compact-evidence-contract
status: recommended
evidence:
  - scripts-for-determinism
---
# Compact evidence contract

Pass conclusions with traceable evidence, not raw context dumps.

## Contract fields

A useful result usually contains:

```json
{
  "conclusion": "...",
  "confidence": "low|medium|high",
  "evidence_ids": ["..."],
  "unknowns": ["..."],
  "actions_taken": ["..."],
  "next_step": "..."
}
```

Add domain-specific fields, but keep provenance and uncertainty.

## Use between

- scripts and skills;
- MCP tools and agents;
- subagents and orchestrators;
- workflow steps;
- graders and result summaries.

## Benefits

- less context duplication;
- easier audits;
- clearer missing evidence;
- stable schemas for evals;
- simpler retries and handoffs.

## Avoid

Do not remove details needed to verify the conclusion. Store raw artifacts outside the active context and keep evidence IDs that point back to them.

## Proof

Track context saved, handoff errors, missing-evidence rate, and human audit time.

**Evidence:** `scripts-for-determinism`, `headless-adapter-controls`
