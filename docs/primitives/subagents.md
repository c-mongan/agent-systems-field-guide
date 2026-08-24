# Subagents

A subagent is a separate context used for a large independent reasoning task.

The main value is isolation. Parallelism is useful only when the work is actually independent.

## Use a subagent when

At least one benefit should be material:

- the worker needs a large context that would pollute the parent;
- independent work can run in parallel;
- the worker needs a restricted or different tool set;
- the worker needs a different model or reasoning policy;
- the parent should receive only a compact specialist result;
- the task needs an explicit responsibility boundary.

Examples:

- investigate database evidence during an incident while another worker inspects application traces;
- review a large migration batch independently from the planner;
- perform an adversarial security review with restricted write access;
- inspect a separate repository without loading it into the main context.

## Do not delegate trivial work

A subagent is usually wrong for:

- reading one file;
- calculating one value;
- running one exact command;
- checking one regular expression;
- returning one boolean;
- restating evidence the parent already loaded.

Use a function, script, or direct tool call instead.

## Define a handoff contract

The parent should send:

- one clear goal;
- the minimum evidence needed;
- allowed tools and permissions;
- stop conditions;
- the required output schema;
- an evidence budget.

The worker should return:

- conclusion;
- confidence or uncertainty;
- evidence IDs;
- missing evidence;
- actions taken;
- recommended next step.

Avoid returning a full raw transcript unless the parent truly needs it.

## Parallel only when independent

Parallel work is useful when workers do not need each other's output to start. Otherwise, parallelism creates duplicated retrieval and conflicting conclusions.

Good parallel split:

```text
application evidence
      +
database evidence
      +
provider evidence
```

Poor split:

```text
worker 1 chooses hypothesis
worker 2 needs that hypothesis
worker 3 needs worker 2's result
```

That is a sequence, not a parallel fan-out.

## Measure the isolation benefit

Track:

- parent context saved;
- worker startup tokens;
- duplicated tool calls;
- wall-clock latency;
- total token cost;
- worker failure rate;
- handoff errors;
- contradictory results;
- task success versus one-agent baseline.

Lab 05 models the cost of creating workers for work that code can perform: [premature subagents](../../labs/05-premature-subagents/README.md).

**Evidence:** `subagent-isolation`, `start-single-agent`
