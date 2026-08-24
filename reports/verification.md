# Verification report

- Profile: `release`
- Generated: `2026-08-24T20:36:03.088132+00:00`
- Source commit: `0b8d155b38f5c8c90c628e5f2c1534e99a8220af`
- Python: `3.13.1`
- Platform: `macOS-26.5.2-arm64-arm-64bit-Mach-O`
- Result: **PASS**

| Check | Result | Time |
|---|---:|---:|
| `ruff-check` | PASS | 12 ms |
| `ruff-format` | PASS | 11 ms |
| `mypy` | PASS | 216 ms |
| `agnix-version` | PASS | 459 ms |
| `agnix-strict` | PASS | 424 ms |
| `compileall` | PASS | 33 ms |
| `coverage-erase` | PASS | 72 ms |
| `tests` | PASS | 805 ms |
| `branch-coverage` | PASS | 109 ms |
| `skill-spec` | PASS | 51 ms |
| `repository` | PASS | 78 ms |
| `frozen-labs` | PASS | 46 ms |
| `diagram-drift` | PASS | 42 ms |
| `example:incident-response` | PASS | 24 ms |
| `example:code-migration` | PASS | 23 ms |
| `example:security-review` | PASS | 23 ms |
| `example:release-engineering` | PASS | 24 ms |
| `knowledge-export` | PASS | 41 ms |

## Scope

`core` verifies code compilation, tests, branch coverage, repository invariants, frozen labs, diagrams, examples, and the optional knowledge export.

`release` runs the same checks plus pinned Ruff, Mypy, and `agnix` gates. Missing release tools are failures, not skips.

This report does not claim a live Claude, Codex, Gemini, or Copilot benchmark. Those require provider credentials, fixed model IDs, and separately published raw traces.
