# Live adapter evaluation

A command that runs successfully is not an evaluation. A live eval needs frozen cases, repeat runs, a grader, and stored traces.

## Recommended directory

```text
runs/
└── 2026-08-24-routing-v1/
    ├── run-spec.json
    ├── baseline/
    │   └── case-001-attempt-01/
    │       ├── stdout.txt
    │       ├── stderr.txt
    │       ├── execution.json
    │       └── grade.json
    ├── candidate/
    └── summary.json
```

`run-spec.json` should record every comparison control. Do not rely on the operator's memory.

## Provider output contracts

### Claude Code

Use non-interactive mode and structured output. Record the exact model, output schema, permission mode, turn limit, session persistence policy, and any configuration discovery that remains enabled.

### Codex

Use `codex exec` with JSON events and an explicit sandbox. Record whether user configuration and repository rules were ignored. Treat stderr progress and stdout events according to the current CLI contract.

### Gemini CLI

Use headless JSON or streaming JSON. Record response statistics, exit code, model, and any tools enabled by the environment.

## Parse failures are failures

If the provider returned text that did not match the required schema, store the raw output and mark the case failed. Do not repair only the candidate output by hand.

## Repeat policy

Choose the number of attempts before running. Apply it equally to both variants. A common starting point is several attempts per case, then more for borderline results.

Report all attempts, including:

- success;
- timeout;
- provider error;
- parse error;
- policy denial;
- empty output.

## Reproducibility limit

Providers, model weights, and harness versions can change. A live result is a dated measurement, not a permanent truth. Store version details and rerun important gates after upgrades.

**Evidence:** `headless-adapter-controls`, `microsoft-agent-evaluation`
