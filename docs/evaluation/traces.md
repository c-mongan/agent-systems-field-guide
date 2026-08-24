# Trace contract

A trace should let another engineer understand and reproduce a run without exposing unnecessary secrets.

## Minimum record

```json
{
  "case_id": "stable-id",
  "architecture": "baseline-or-candidate",
  "adapter": "claude-code-or-codex",
  "model": "exact-model-id",
  "model_settings": {},
  "tool_policy": {},
  "input_snapshot": "sha256",
  "started_at": "ISO-8601",
  "success": true,
  "latency_ms": 0,
  "input_tokens": 0,
  "output_tokens": 0,
  "tool_calls": 0,
  "evidence_ids": [],
  "error": null
}
```

The JSON Schema is stored at [`evals/schema/trace.schema.json`](../../evals/schema/trace.schema.json).

## Store raw artifacts separately

Keep:

- stdout and stderr;
- structured provider events;
- tool-call arguments and results, with sensitive fields removed;
- grader output;
- execution record;
- architecture files used for the run;
- data snapshot or immutable reference.

The adapter runner stores the prompt hash rather than the prompt in `execution.json`. Raw prompts and provider output may still contain sensitive data, so store them under the same access policy as the source task.

## Record failure honestly

Do not drop:

- timeouts;
- parse errors;
- provider errors;
- permission denials;
- empty outputs;
- missing cases;
- interrupted runs.

A missing candidate output is not a successful zero-cost run. It is a failed or incomplete case.

## Preserve comparability

Do not combine results when these changed without a separate analysis:

- model identifier;
- model settings;
- tool permissions;
- source-data snapshot;
- system or repository instructions;
- acceptance policy;
- grader version;
- timeout;
- retry policy.

## Privacy and security

- hash prompts in summary records;
- redact secrets and personal data from published traces;
- avoid storing the full ambient environment;
- store allowed tools and permissions explicitly;
- record side-effect identifiers for audit and deduplication;
- keep provenance for every evidence item.

**Evidence:** `headless-adapter-controls`, `skill-lift-eval`, `skill-security-review`
