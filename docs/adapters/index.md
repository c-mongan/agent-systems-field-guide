# Harness adapters

The repository includes provider-neutral interfaces and bounded adapters for:

- Claude Code;
- OpenAI Codex;
- Gemini CLI;
- frozen replay fixtures.

The adapters serve two different purposes.

## Command rendering

Rendering builds the exact argument list without starting an external process.

```bash
agent-guide adapter render claude-code "Route this task" --model EXACT_MODEL_ID
agent-guide adapter render codex "Route this task" --model EXACT_MODEL_ID
agent-guide adapter render gemini "Route this task" --model EXACT_MODEL_ID
```

The output includes an argument array and a shell preview. The array is the source of truth; the runner does not use a shell.

## Explicit execution

A live provider process starts only when `--execute` is supplied.

```bash
agent-guide adapter run codex "Route this task" \
  --model EXACT_MODEL_ID \
  --output-dir runs/codex-case-001 \
  --execute
```

The runner:

- resolves the executable explicitly;
- uses no shell;
- applies a hard timeout;
- records exit status and timing;
- stores raw stdout and stderr when an output directory is supplied;
- parses structured output;
- stores a prompt SHA-256 rather than the prompt in `execution.json`;
- reports missing executables, timeouts, parse failures, and provider failures.

## Safe defaults

The included command builders prefer bounded modes:

- Claude Code: non-interactive JSON, no session persistence, turn cap, plan-style permissions;
- Codex: ephemeral session, JSON events, read-only sandbox, ignored user configuration and rules;
- Gemini: headless JSON output and explicit model support.

These defaults reduce hidden state. They do not guarantee full isolation. Each harness can still have version-specific behaviour, credentials, environment variables, or workspace access.

## Why no Copilot live adapter?

The repository maps Copilot concepts in the vendor guide but does not pretend to support a live adapter that was not implemented and tested. Contributions should add a provider only when command, output, permission, and error contracts can be frozen and verified.

## Read next

- [Live evaluations](live-evals.md)
- [Live provider protocol](../evaluation/live-provider-protocol.md)
- [Trace contract](../evaluation/traces.md)

**Evidence:** `headless-adapter-controls`, `adapter-bounds`
