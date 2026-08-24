# Limits

This repository is designed to be useful without overstating what it proves.

## What is verified locally

The core profile verifies:

- Python compilation;
- tests and branch coverage;
- internal Markdown links;
- evidence IDs;
- Agent Skills structure;
- CI pinning rules;
- six frozen structural labs;
- four deterministic examples;
- diagram drift;
- knowledge export.

## What the structural labs prove

They prove that:

- the fixture inputs are frozen;
- baseline and candidate use the same deterministic runner;
- committed outputs can be regenerated;
- changed architecture variables are documented;
- result manifests detect drift.

They do not prove that every model will show the same improvement.

## What is not included

This release does not include:

- a universal model benchmark;
- live Claude, Codex, Gemini, or Copilot performance claims;
- provider billing counts for structural token estimates;
- proof that the suggested heuristics fit every workload;
- a production-grade workflow engine;
- a production MCP server;
- automatic security approval for third-party skills;
- guaranteed future compatibility with vendor CLIs.

## Release verification in this environment

The repository defines a fail-closed release profile for Ruff, Mypy, and pinned `agnix`. Those third-party tools require their installed binaries. The final artifact records which checks were actually executed locally and which remain CI gates.

## Heuristics are not standards

Review points such as 150–200 lines for global instructions, 300 lines for a skill review, an 80% reference-load rate, or three repeated mechanical operations are practical prompts. Only the Agent Skills 500-line and approximately 5,000-token guidance is presented as specification guidance.

Even official product behaviour can change. Every source has a review date.

## Use the guide safely

Adopt the method, then test it on your own cases:

1. freeze representative tasks;
2. record the current baseline;
3. change one boundary;
4. measure quality, cost, and safety;
5. keep or revert;
6. expand the case set after every new failure.
