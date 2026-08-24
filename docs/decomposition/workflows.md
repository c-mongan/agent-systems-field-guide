# Skill or workflow?

Use a skill when the model should decide the method. Use a workflow when the system must control the path.

```text
Flexible expert method            Required operational control
          ↓                                  ↓
        Skill                            Workflow
```

## Choose a skill when

- one agent can complete the task in a bounded run;
- steps can adapt to evidence;
- actions are read-only, idempotent, or low risk;
- restarting the task is acceptable;
- there is no required approval boundary;
- the output is mainly analysis or a recommendation.

Example: assess whether a library upgrade contains breaking changes and propose a rollout plan.

## Choose a workflow when

- steps must run in a fixed or validated order;
- work may pause and resume;
- human approval is required;
- retries could repeat side effects;
- several systems or agents coordinate;
- state and audit history must survive process failure;
- rollback or compensation must be available.

Example: calculate release order, obtain approval, publish packages, verify registry state, announce, and open a rollback window.

## Use both

Most useful systems combine them:

```text
Workflow step: assess change risk
             ↓
Skill chooses evidence and method
             ↓
Structured risk result
             ↓
Workflow applies approval policy
```

The workflow owns state. The skill owns flexible expert judgment.

## Warning signs that prose is acting as a workflow

- “always do A, then B, then C” appears in a long system prompt;
- retries are described but not persisted;
- the model decides whether a payment or publish action already happened;
- approvals exist only as conversational text;
- a crash forces the process to restart from the beginning;
- different agents disagree about which step is current.

## Evaluation

Inject failures at each state transition. Verify that the process resumes correctly, avoids duplicate side effects, preserves approvals, and records the evidence used by model-driven steps.

**Evidence:** `skill-v-workflow`, `microsoft-agent-evaluation`
