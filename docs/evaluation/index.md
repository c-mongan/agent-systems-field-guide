# Evaluation method

An architecture eval asks whether a boundary improves the system. It does not ask whether one answer looks impressive.

## Freeze the comparison

Before the first run, store:

- stable case IDs;
- input and data snapshot hashes;
- expected behaviour or acceptance rubric;
- model identifier and settings;
- tool and permission policy;
- timeout and retry policy;
- architecture version;
- grader version;
- number of repeated runs.

Use the same controls for baseline and candidate. Reject mismatched case sets.

## Change one architecture variable

Examples:

- global procedure versus on-demand skill;
- monolithic skill versus core skill plus references;
- repeated direct calls versus one batch script;
- overlapping descriptions versus distinct boundaries;
- single context versus one isolated worker;
- prose-only process versus explicit workflow.

If the model, tools, and data also change, you no longer know which change caused the result.

## Evaluation stack

1. **Static checks** — schema, missing files, links, unsafe scripts, unpinned validators.
2. **Routing checks** — correct activation, missed activation, false activation, overlap.
3. **Component lift** — skill or tool enabled versus a baseline.
4. **System quality** — end-to-end task success, cost, latency, recovery, and safety.
5. **Regression** — frozen representative cases on every accepted architecture change.
6. **Production monitoring** — drift, new failure families, and changes in real traffic.

## Quality first, then cost

Define a task-specific success policy before running the eval. Examples:

- the migration plan identifies every semantic rewrite and does not modify generated files;
- the incident report separates observed evidence from inferred causes;
- the security review finds all seeded control failures and avoids unsupported findings;
- the release plan produces a valid dependency order and blocks cycles.

Then track:

- success rate;
- false positives and false negatives;
- input and output tokens;
- tool calls;
- wall-clock latency;
- subagent count;
- retries;
- human intervention;
- side-effect errors;
- safety or policy violations.

## Repeat nondeterministic runs

One run per case is not enough for a live model comparison. Repeat cases and report the distribution, not only the best output.

At minimum record:

- number of attempts;
- mean and median success;
- variance or confidence interval;
- timeout and error counts;
- model and date.

## Grade without leaking the answer

Use deterministic graders when the result is objective. Use rubric or model graders only when necessary. Blind the grader to baseline versus candidate where practical.

Keep raw outputs so a human can audit grader errors.

## Interpretation rules

A result supports only the workload tested.

- A structural simulation proves that the repository's deterministic code is reproducible.
- A live provider run supports a claim about the exact model, harness, settings, data, and date used.
- Neither proves universal behaviour across all models and future versions.

## Run the portable comparison

The repository CLI pairs cases by `case_id` and rejects mismatched inputs.

```bash
agent-guide eval compare baseline.jsonl candidate.jsonl
```

Read the [trace contract](traces.md), [lab results](lab-results.md), and [live provider protocol](live-provider-protocol.md).

**Evidence:** `skill-lift-eval`, `blind-comparison`, `microsoft-agent-evaluation`
