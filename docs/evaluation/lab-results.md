# Committed lab results

The result files under `labs/*/results/` are generated from frozen fixtures. The core verification profile fails if they drift.

## Summary

| Lab | Controlled change | Main committed result |
|---|---|---|
| 01 — Mega instructions | always-loaded specialist rules → on-demand procedures | mean loaded estimate `344 → 84.3`; structural success `0.30 → 1.00` |
| 02 — Tool overload | six overlapping tools → six distinct tools | routing accuracy `0.50 → 1.00`; ambiguity `0.583 → 0.000` |
| 03 — Mega skill | monolith → core procedure + focused references | mean loaded estimate `270 → 87.25`; structural success `0.25 → 1.00` |
| 04 — Overlapping skills | same six jobs, rewritten boundaries | routing accuracy `0.375 → 0.958`; ambiguity `0.708 → 0.125` |
| 05 — Premature subagents | worker per step → one agent + code + selective worker | modelled agents `9.3 → 1.2`; expected success `0.807 → 0.971` |
| 06 — Eager context | full preload → catalogue + on-demand loading | mean total estimate `46,600 → 3,963`; overflow `1.00 → 0.00` |

## What these numbers mean

They are **deterministic structural experiments**:

- token values are fixed estimates or fixture parameters;
- routing uses a documented weighted-overlap algorithm;
- subagent costs use a frozen discrete-event model;
- all inputs and outputs have SHA-256 manifests;
- the same repository code regenerates the results.

They prove that the examples and comparison machinery are reproducible.

## What they do not mean

They are not:

- universal Claude, Codex, Gemini, or Copilot benchmarks;
- provider billing measurements;
- proof that every workload will improve by the same amount;
- evidence that deterministic routing should replace model routing in production.

Use the [live provider protocol](live-provider-protocol.md) before making provider-specific claims.
