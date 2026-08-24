# Verification report

- Profile: `release`
- Generated: `2026-08-24T20:21:45.739043+00:00`
- Source commit: `uncommitted`
- Python: `3.13.1`
- Platform: `macOS-26.5.2-arm64-arm-64bit-Mach-O`
- Result: **PASS**

| Check | Result | Time |
|---|---:|---:|
| `ruff-check` | PASS | 52 ms |
| `ruff-format` | PASS | 11 ms |
| `mypy` | PASS | 331 ms |
| `agnix-version` | PASS | 1220 ms |
| `agnix-strict` | PASS | 572 ms |
| `compileall` | PASS | 36 ms |
| `coverage-erase` | PASS | 77 ms |
| `tests` | PASS | 1415 ms |
| `branch-coverage` | PASS | 113 ms |
| `skill-spec` | PASS | 54 ms |
| `repository` | PASS | 78 ms |
| `frozen-labs` | PASS | 48 ms |
| `diagram-drift` | PASS | 43 ms |
| `example:incident-response` | PASS | 25 ms |
| `example:code-migration` | PASS | 24 ms |
| `example:security-review` | PASS | 23 ms |
| `example:release-engineering` | PASS | 24 ms |
| `knowledge-export` | PASS | 43 ms |

## Scope

`core` verifies code compilation, tests, branch coverage, repository invariants, frozen labs, diagrams, examples, and the optional knowledge export.

`release` runs the same checks plus pinned Ruff, Mypy, and `agnix` gates. Missing release tools are failures, not skips.

This report does not claim a live Claude, Codex, Gemini, or Copilot benchmark. Those require provider credentials, fixed model IDs, and separately published raw traces.
