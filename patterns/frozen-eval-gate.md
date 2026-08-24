---
id: frozen-eval-gate
status: recommended
evidence:
  - skill-lift-eval
---
# Frozen eval gate

Accept architecture complexity only after a fair baseline-versus-candidate comparison.

## Freeze

- cases and stable IDs;
- data snapshot;
- model and settings;
- tools and permissions;
- timeout and retry policy;
- acceptance rubric;
- grader version.

## Run

1. execute baseline and candidate;
2. store every result, timeout, and error;
3. repeat live model cases;
4. grade blindly where practical;
5. compare quality and cost;
6. inspect regressions;
7. keep or revert.

## Why it matters

Architecture changes often look cleaner while moving failures elsewhere. Frozen cases prevent the team from changing the test after seeing the answer.

## Repository example

All six labs store baseline, candidate, cases, results, and SHA-256 manifests. CI rejects drift.

## Proof

The gate itself should fail closed when cases are missing, IDs differ, validators are unavailable, or committed results no longer match generation code.

**Evidence:** `skill-lift-eval`, `blind-comparison`, `microsoft-agent-evaluation`
