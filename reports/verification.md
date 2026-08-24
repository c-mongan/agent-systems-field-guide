# Verification report

- Profile: `release`
- Generated: `2026-08-24T20:33:23.049052+00:00`
- Source commit: `796c0ba265eeea1a7c0759998e26de511a1f11f5`
- Python: `3.13.1`
- Platform: `macOS-26.5.2-arm64-arm-64bit-Mach-O`
- Result: **PASS**

| Check | Result | Time |
|---|---:|---:|
| `ruff-check` | PASS | 56 ms |
| `ruff-format` | PASS | 13 ms |
| `mypy` | PASS | 219 ms |
| `agnix-version` | PASS | 675 ms |
| `agnix-strict` | PASS | 452 ms |
| `compileall` | PASS | 32 ms |
| `coverage-erase` | PASS | 67 ms |
| `tests` | PASS | 825 ms |
| `branch-coverage` | PASS | 113 ms |
| `skill-spec` | PASS | 52 ms |
| `repository` | PASS | 80 ms |
| `frozen-labs` | PASS | 48 ms |
| `diagram-drift` | PASS | 42 ms |
| `example:incident-response` | PASS | 24 ms |
| `example:code-migration` | PASS | 23 ms |
| `example:security-review` | PASS | 23 ms |
| `example:release-engineering` | PASS | 23 ms |
| `knowledge-export` | PASS | 42 ms |

## Scope

`core` verifies code compilation, tests, branch coverage, repository invariants, frozen labs, diagrams, examples, and the optional knowledge export.

`release` runs the same checks plus pinned Ruff, Mypy, and `agnix` gates. Missing release tools are failures, not skips.

This report does not claim a live Claude, Codex, Gemini, or Copilot benchmark. Those require provider credentials, fixed model IDs, and separately published raw traces.
