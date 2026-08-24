"""Paired before/after comparison for frozen architecture evaluations."""

from __future__ import annotations

import random
from collections.abc import Callable, Iterable
from statistics import mean
from typing import Any

from .models import EvalRecord


def _bootstrap_delta(
    pairs: list[tuple[float, float]],
    *,
    samples: int = 2000,
    seed: int = 20260824,
) -> tuple[float, float]:
    if not pairs:
        return (0.0, 0.0)
    rng = random.Random(seed)
    deltas: list[float] = []
    for _ in range(samples):
        picked = [pairs[rng.randrange(len(pairs))] for _ in pairs]
        deltas.append(mean(candidate - baseline for baseline, candidate in picked))
    deltas.sort()
    lower = deltas[int(samples * 0.025)]
    upper = deltas[min(samples - 1, int(samples * 0.975))]
    return (round(lower, 6), round(upper, 6))


def compare_records(
    baseline: Iterable[EvalRecord],
    candidate: Iterable[EvalRecord],
) -> dict[str, Any]:
    """Compare paired cases and fail on missing or duplicate case IDs."""

    def index(records: Iterable[EvalRecord], label: str) -> dict[str, EvalRecord]:
        output: dict[str, EvalRecord] = {}
        for record in records:
            if record.case_id in output:
                raise ValueError(f"duplicate {label} case_id: {record.case_id}")
            output[record.case_id] = record
        return output

    left, right = index(baseline, "baseline"), index(candidate, "candidate")
    if left.keys() != right.keys():
        missing_candidate = sorted(left.keys() - right.keys())
        missing_baseline = sorted(right.keys() - left.keys())
        raise ValueError(
            f"case sets differ; missing candidate={missing_candidate}, missing baseline={missing_baseline}"
        )
    case_ids = sorted(left)
    extractors: dict[str, Callable[[EvalRecord], float]] = {
        "success_rate": lambda record: float(record.success),
        "latency_ms": lambda record: record.latency_ms,
        "input_tokens": lambda record: float(record.input_tokens),
        "output_tokens": lambda record: float(record.output_tokens),
        "tool_calls": lambda record: float(record.tool_calls),
    }
    directions = {
        "success_rate": "higher",
        "latency_ms": "lower",
        "input_tokens": "lower",
        "output_tokens": "lower",
        "tool_calls": "lower",
    }
    metrics: dict[str, Any] = {}
    for name, extract in extractors.items():
        pairs = [(extract(left[case_id]), extract(right[case_id])) for case_id in case_ids]
        baseline_mean = mean(pair[0] for pair in pairs) if pairs else 0.0
        candidate_mean = mean(pair[1] for pair in pairs) if pairs else 0.0
        delta = candidate_mean - baseline_mean
        lower, upper = _bootstrap_delta(pairs)
        improved = delta > 0 if directions[name] == "higher" else delta < 0
        metrics[name] = {
            "direction": directions[name],
            "baseline": round(baseline_mean, 6),
            "candidate": round(candidate_mean, 6),
            "delta": round(delta, 6),
            "bootstrap_95pct_delta": [lower, upper],
            "improved": improved,
        }
    return {"paired_cases": len(case_ids), "metrics": metrics}
