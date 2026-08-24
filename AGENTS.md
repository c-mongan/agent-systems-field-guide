# Repository instructions

## Project

This is a Python 3.11+ executable field guide for designing and evaluating agent systems. It combines vendor-neutral Markdown guidance with deterministic labs, examples, adapters, validators, and a CLI.

## Instruction precedence

`AGENTS.md` is the canonical repository instruction file. Harness-specific files such as `CLAUDE.md` and `.github/copilot-instructions.md` defer to it and may only add harness-specific guidance. The closest scoped `AGENTS.md` takes precedence if one is added below the repository root.

## Working rules

- Use simple technical English.
- Keep portable guidance separate from vendor-specific syntax.
- Label claims as official, specification, research, heuristic, or measure.
- Describe structural lab results as deterministic structural evidence. Reserve live benchmark language for runs with raw traces, exact model IDs, configuration, and dates.
- Add evidence IDs for factual architecture claims.
- Use deterministic scripts for generated results and diagrams.
- Run `agent-guide check .`, all labs, examples, and tests before committing.
- Pin validation tools and GitHub Actions. Do not add silent skips.
