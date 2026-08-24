# Workflows

A workflow controls required order, state, checkpointing, retry, approval, and side effects.

A workflow answers: **what must happen, in what order, and what state is safe to resume from?**

A skill answers: **how should an expert perform this flexible task?**

## Use a workflow when

- a process has required stages;
- steps produce side effects;
- work may pause and resume;
- human approval is required;
- retries must not repeat completed actions;
- several agents or systems must coordinate;
- rollback or compensation is needed;
- auditability requires explicit state.

Examples:

- publish a software release;
- process a refund;
- approve and apply an infrastructure change;
- open, communicate, and close a major incident;
- prepare, review, sign, and send a legal document.

## Skill versus workflow

| Question | Skill | Workflow |
|---|---|---|
| Who chooses the method? | model | model inside bounded steps |
| Who controls order? | model | system |
| Can it checkpoint? | usually one run | yes |
| Are repeated side effects safe? | only when idempotent or low risk | controlled through state and retry rules |
| Best for | focused expert method | operational process |

A workflow can call a skill inside a step:

```text
Collect evidence
      ↓
Skill: assess release risk
      ↓
Human approval
      ↓
Deterministic publish action
      ↓
Verification
      ↓
Close or rollback
```

## State must be explicit

Record:

- current step;
- completed steps;
- inputs and evidence snapshot;
- approvals;
- side-effect identifiers;
- retry count;
- timeout state;
- next allowed transitions;
- rollback or compensation status.

Do not rely on conversation memory as the only workflow state for high-impact processes.

## Design retries around side effects

A retry should not send a second email, charge a second payment, or publish the same package twice.

Use:

- idempotency keys;
- persisted step status;
- read-before-write checks;
- compensating actions;
- manual review for ambiguous outcomes.

## Avoid over-specifying reasoning

The workflow should control the path without turning every expert decision into fixed code. Use a skill inside a step when the correct method depends on evidence.

## Evaluate workflows

Track:

- completion rate;
- recovery from injected failures;
- repeated side effects;
- time spent waiting for approval;
- checkpoint resume accuracy;
- manual intervention;
- rollback success;
- end-to-end task quality.

**Evidence:** `skill-v-workflow`, `microsoft-agent-evaluation`
