---
id: workflow-for-control
status: recommended
evidence:
  - skill-v-workflow
---
# Workflow for control

Use a workflow when the system must guarantee order, state, approval, retry, or side effects.

## Pattern

```text
Explicit state
    ↓
Bounded step
    ↓
Persist result
    ↓
Approval or transition check
    ↓
Next step or compensation
```

A step may call a skill for flexible reasoning. The workflow remains responsible for state and allowed transitions.

## Use for

- releases;
- payments and refunds;
- messages or notifications;
- infrastructure changes;
- incident lifecycle;
- human approval processes.

## Required controls

- persistent step state;
- idempotency keys;
- timeout and retry rules;
- approval record;
- side-effect identifiers;
- rollback or compensation;
- audit log.

## Avoid

Do not encode the whole reasoning method into fixed workflow code. Let a skill own bounded expert judgment and return structured evidence.

## Proof

Inject a failure after every step. Verify resume, no duplicate side effects, preserved approvals, and correct rollback.

**Evidence:** `skill-v-workflow`, `microsoft-agent-evaluation`
