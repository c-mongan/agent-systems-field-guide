# Reproducible example — Large code migration

A team is replacing `LegacyCheckoutClient` with `CheckoutClientV2` across shared and leaf packages.

The migration contains both safe mechanical edits and semantic rewrites that change control flow.

## Architecture

```text
Static findings
   ↓
Deterministic classifier
   - sort findings
   - classify known mechanical patterns
   - isolate custom control flow
   - group semantic work by package
   - build rollout batches
   ↓
Migration skill
   - verify classification evidence
   - load framework-specific references
   - inspect semantic call sites
   - choose tests, canary, and rollback plan
```

## What code owns

[`run.py`](run.py) treats direct method renames, static import renames, and named-argument renames as mechanical only when custom control flow is absent.

It creates three possible batches:

1. mechanical codemod;
2. semantic changes in leaf packages;
3. semantic changes in shared core.

The classification rules are visible and testable.

## What an agent should own

A real migration agent should:

- confirm that the detected pattern is safe in the current code;
- inspect callback-to-async changes for error and cancellation behaviour;
- load version-specific migration guidance;
- identify public API and compatibility risks;
- decide which tests and canary signals are required;
- stop when evidence is insufficient.

## Run

```bash
python examples/code-migration/run.py \
  examples/code-migration/fixtures/input.json
```

Expected output is frozen in [`expected/output.json`](expected/output.json).

## Why this is not a toy codemod

The example keeps the important boundary visible: code can classify known patterns and produce rollout groups, but it cannot safely decide every semantic rewrite. The agent uses the deterministic result as evidence rather than replacing it with free-form scanning.
