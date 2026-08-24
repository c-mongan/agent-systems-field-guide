---
id: eager-context-loading
status: avoid
evidence:
  - progressive-disclosure
---
# Eager context loading

Every skill, reference, or specialist manual is loaded before the task is known.

## Symptoms

- startup context grows with the library;
- most loaded tokens are never used;
- conflicting specialist rules appear;
- latency rises before the first useful action;
- adding a skill affects unrelated tasks.

## Better boundary

Advertise concise catalogue metadata. Load the chosen procedure, then only the references and scripts needed for that branch. Filter catalogues for specialist agents.

## Exception

A small, tightly scoped eager skill set can be valid. Measure it in the actual harness because some SDK custom-agent configurations preload assigned skills by design.

## Proof required

Track initial tokens, total loaded tokens, relevant-token ratio, overflow or compaction, and task success. See [Lab 06](../labs/06-eager-context/README.md).

**Evidence:** `progressive-disclosure`, `copilot-eager-skills`
