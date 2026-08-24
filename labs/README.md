# Controlled architecture labs

The labs make one architecture change at a time and store the generated proof.

Every lab includes:

- frozen cases;
- baseline and candidate configuration;
- deterministic runner code;
- committed comparison results;
- SHA-256 input and output manifests;
- a clear statement of what the result does **not** prove.

| Lab | Controlled question | Main result |
|---|---|---|
| [01 — Mega instructions](01-mega-instructions/README.md) | Should all specialist rules be global? | loaded estimate `344 → 84.3` |
| [02 — Tool overload](02-tool-overload/README.md) | Is raw count or overlap the real problem? | routing `0.50 → 1.00` |
| [03 — Mega skill](03-mega-skill/README.md) | When should a skill use references? | loaded estimate `270 → 87.25` |
| [04 — Overlapping skills](04-overlapping-skills/README.md) | What do vague boundaries cost? | routing `0.375 → 0.958` |
| [05 — Premature subagents](05-premature-subagents/README.md) | When is a worker unnecessary? | modelled agents `9.3 → 1.2` |
| [06 — Eager context](06-eager-context/README.md) | What does full preloading cost? | total estimate `46,600 → 3,963` |

## Verify

```bash
agent-guide lab run all --root .
```

The command regenerates results in memory and compares them with the committed files. Any drift fails.

Regenerate only after intentionally changing a case, configuration, or runner:

```bash
agent-guide lab run all --root . --write
```

Review the diff and updated manifest before accepting it.

## Interpretation

These are deterministic structural experiments. They are useful for testing architecture claims, fixtures, and release gates. They are not universal provider benchmarks. Live model claims require fixed model IDs, repeated runs, raw traces, and the [live provider protocol](../docs/evaluation/live-provider-protocol.md).
