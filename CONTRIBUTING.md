# Contributing

## Content change

1. State whether the claim is official, specification, research, heuristic, or measure.
2. Prefer a first-party source.
3. Add or update `sources/sources.json` and `sources/claims.json`.
4. Keep examples realistic and reproducible.
5. Do not add benchmark numbers without frozen cases, raw traces, exact model details, and a run date.

## Code change

```bash
python -m pip install -e .
python -m pip install -r requirements-dev.lock
agent-guide check .
agent-guide lab run all --root .
coverage run -m pytest
coverage report --fail-under=90
```

If a fixture or runner changes intentionally, regenerate lab results and review the diff:

```bash
agent-guide lab run all --root . --write
```
