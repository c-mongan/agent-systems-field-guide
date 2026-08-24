---
id: unpinned-agent-tooling
status: avoid
evidence:
  - pinned-validation
---
# Unpinned agent tooling

CI uses `latest`, a mutable action tag, or an unconstrained validator version.

## Risk

The same commit can produce a different result tomorrow. A compromised or breaking upstream release can alter the gate without repository review.

## Better boundary

- pin Python packages exactly;
- pin Node.js and npm packages used by validation;
- pin GitHub Actions by full commit SHA;
- update through reviewed dependency pull requests;
- record tool versions in verification reports;
- keep version checks fail closed.

## Limits

Pinning improves reproducibility. It does not prove the validator is correct or secure. Continue to review updates and run behavioural evals.

## Proof required

Run the release profile twice from a clean environment and compare tool versions and results.

**Evidence:** `pinned-validation`
