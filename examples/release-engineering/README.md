# Reproducible example — Release engineering

A monorepo release changes a shared core package and an authentication plugin. Dependent packages may need version propagation and a strict publish order.

## Architecture

```text
Package graph + semantic bump decisions
                ↓
Deterministic release planner
                - propagate dependent patch bumps
                - calculate topological order
                - reject dependency cycles
                - list release gates
                ↓
Release workflow
                - verify tests
                - create versions
                - dry-run publish
                - require approval
                - publish in order
                - verify or rollback
```

## What code owns

[`run.py`](run.py) calculates:

- version propagation;
- dependency reasons;
- topological publish order;
- cycle failure;
- a fixed set of release gates.

Those results should not depend on model creativity.

## What an agent should own

A real release skill may assess whether an individual change is patch, minor, or major. A workflow should then control approval, publishing, verification, and rollback because those steps have state and external side effects.

## Run

```bash
python examples/release-engineering/run.py \
  examples/release-engineering/fixtures/input.json
```

Expected output is frozen in [`expected/output.json`](expected/output.json).

## Failure boundary

If the dependency graph contains a cycle, the script raises an error. It does not invent an order. In a production workflow, that error should block publishing and require an explicit graph fix.
