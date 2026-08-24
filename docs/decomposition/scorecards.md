# Decomposition scorecards

These scorecards are structured review aids. They are not standards and they do not replace an eval.

## Move instructions into a skill

Add one point for each true statement:

- the section applies to fewer than half of normal tasks;
- it describes a repeatable multi-step method;
- it names task-specific tools;
- it has its own output format;
- changing it has broken unrelated tasks;
- it contains conditional branches or specialist examples.

**0–1:** keep it in instructions for now.<br>
**2–3:** test moving it into a skill.<br>
**4–6:** the boundary is probably overdue.

## Move skill content into references

Add one point for each true statement:

- the section is needed only for one framework or case family;
- the skill can state a clear read condition;
- the section is mostly facts, schemas, examples, or policy detail;
- loading it does not change the main procedure;
- it adds substantial context on unrelated runs;
- separate sections activate independently.

**0–1:** keep it in `SKILL.md`.<br>
**2–3:** create a focused reference and compare.<br>
**4–6:** split the conditional material before adding more.

## Replace model work with code

Add one point for each true statement:

- the operation has one objectively correct result;
- the model repeats it across many items;
- it is filtering, joining, sorting, parsing, counting, or validating;
- errors are easy to test with fixtures;
- the raw input is much larger than the useful output;
- the operation does not need open-ended semantic judgment.

**0–1:** direct model reasoning may be fine.<br>
**2–3:** prototype a script.<br>
**4–6:** code should probably own the operation.

## Add a workflow

Add one point for each true statement:

- order must be guaranteed;
- a step has an external side effect;
- retries could repeat a completed action;
- human approval is required;
- the process may pause and resume;
- compensation or rollback is needed;
- several systems or agents must coordinate.

**0–1:** a skill may be enough.<br>
**2–3:** test a small explicit workflow.<br>
**4–7:** do not rely on prose-only control.

## Add a subagent

Add one benefit point for each true statement:

- the work has a large independent context;
- it can run in parallel without another worker's result;
- it needs different tools or permissions;
- it needs a different model policy;
- the parent needs only a compact result;
- intermediate reasoning would pollute the parent.

Subtract one point for each cost:

- the worker repeats parent retrieval;
- the handoff cannot be expressed clearly;
- the task returns one deterministic value;
- the worker needs frequent back-and-forth with the parent;
- the task is faster as one direct tool call.

**Score ≤0:** keep it local.<br>
**Score 1–2:** test only if traces show a real problem.<br>
**Score ≥3:** a subagent is a reasonable candidate.

## Split into a specialist agent

Use a specialist agent only when the domain has a durable boundary. Require at least two of:

- distinct permissions;
- distinct data access;
- distinct tool catalogue;
- distinct model or reasoning policy;
- stable repeated responsibility;
- independent governance or audit owner.

A different name or tone does not count.

## Acceptance rule

Every scorecard ends with the same gate:

```text
Candidate boundary
       ↓
Paired frozen eval
       ↓
Quality + cost + safety comparison
       ↓
Keep or revert
```

**Evidence:** `scripts-for-determinism`, `skill-v-workflow`, `subagent-isolation`, `skill-lift-eval`
