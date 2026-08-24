from __future__ import annotations

import pytest

from agent_field_guide.compare import compare_records
from agent_field_guide.models import EvalRecord


def test_compare_records_pairs_cases_and_directions() -> None:
    baseline = [EvalRecord("a", False, 100, 1000, 20, 4), EvalRecord("b", True, 200, 800, 30, 3)]
    candidate = [EvalRecord("a", True, 80, 600, 15, 2), EvalRecord("b", True, 150, 700, 25, 2)]
    result = compare_records(baseline, candidate)
    assert result["paired_cases"] == 2
    assert result["metrics"]["success_rate"]["candidate"] == 1.0
    assert result["metrics"]["latency_ms"]["improved"] is True
    assert result["metrics"]["input_tokens"]["delta"] < 0
    assert len(result["metrics"]["tool_calls"]["bootstrap_95pct_delta"]) == 2


def test_compare_rejects_duplicate_ids() -> None:
    with pytest.raises(ValueError, match="duplicate baseline"):
        compare_records([EvalRecord("a", True), EvalRecord("a", False)], [EvalRecord("a", True)])


def test_compare_rejects_different_case_sets() -> None:
    with pytest.raises(ValueError, match="case sets differ"):
        compare_records([EvalRecord("a", True)], [EvalRecord("b", True)])


def test_compare_empty_sets() -> None:
    result = compare_records([], [])
    assert result["paired_cases"] == 0
    assert result["metrics"]["success_rate"]["baseline"] == 0
