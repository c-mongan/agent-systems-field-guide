# Scripts and tools

Scripts and tools should own exact collection, transformation, calculation, or action.

The model should not spend reasoning tokens on work that ordinary code can perform more reliably.

## Good uses

Use code for:

- parsing logs or structured files;
- filtering and joining records;
- deduplication;
- counting and aggregation;
- graph traversal and ordering;
- schema validation;
- fixed scoring formulas;
- timestamp correlation;
- deterministic API pagination;
- safe, repeatable transformations;
- checks with an objective pass or fail result.

Example: during an incident, code should correlate request IDs across gateway, application, database, and provider events. The model should inspect the compact timeline and judge the likely causal story.

## Direct tool or skill-wrapped tool?

Use the tool directly when:

- the intent maps cleanly to one operation;
- arguments are simple and safe;
- output is already compact and meaningful;
- little interpretation is required.

Wrap it in a skill when:

- the model must decide whether it applies;
- argument choice needs domain judgment;
- several tools form a procedure;
- output must be combined with other evidence;
- missing evidence changes the next step;
- the operation has safety conditions.

## Return compact evidence

A good tool result helps the next reasoning step. It does not dump every raw row.

Prefer:

```json
{
  "matched_requests": 184,
  "first_failure_at": "2026-08-24T09:42:11Z",
  "error_families": [
    {"name": "provider_timeout", "count": 161},
    {"name": "db_lock_wait", "count": 23}
  ],
  "sample_evidence_ids": ["evt-017", "evt-041", "evt-203"]
}
```

Avoid returning 80,000 raw lines when the model only needs the counts, first occurrence, representative samples, and pointers back to source evidence.

## Design for failure

A deterministic tool should make these explicit:

- input schema;
- output schema;
- timeout;
- pagination and truncation;
- retry policy;
- idempotency;
- side effects;
- permission needs;
- error categories;
- provenance of returned evidence.

Do not hide partial results. An empty result must be distinguishable from a failed query.

## Batch repeated operations

A common agent smell is a long sequence of similar calls:

```text
fetch item 1
fetch item 2
fetch item 3
...
fetch item 80
```

Test a batch operation that fetches all needed items, validates them, and returns a compact result. This reduces tool-selection overhead and makes partial failures easier to reason about.

## Verify the boundary

Compare:

- task success;
- tool calls;
- input tokens;
- wall-clock time;
- parsing or calculation errors;
- retry count;
- missing or over-truncated evidence.

The repository examples show this split in production incident correlation, code migration, security review, and release ordering.

**Evidence:** `scripts-for-determinism`, `progressive-disclosure`
