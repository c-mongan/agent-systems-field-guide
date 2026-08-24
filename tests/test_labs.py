from __future__ import annotations

from pathlib import Path

import pytest

from agent_field_guide.labs import LAB_NAMES, build_lab, run_all_labs, run_lab

ROOT = Path(__file__).resolve().parents[1]
LABS = ROOT / "labs"


def test_all_frozen_labs_have_no_drift() -> None:
    results = run_all_labs(LABS)
    assert [result["lab"] for result in results] == list(LAB_NAMES)
    assert all(not result["drift"] for result in results)


def test_flagship_lab_changes_boundary_not_count() -> None:
    built = build_lab(LABS, "04-overlapping-skills")
    before = built["baseline"]["metrics"]
    after = built["candidate"]["metrics"]
    assert before["catalog_items"] == after["catalog_items"] == 6
    assert before["accuracy"] == 0.375
    assert after["accuracy"] == 0.958333
    assert after["max_pairwise_overlap"] < before["max_pairwise_overlap"]


def test_tool_lab_is_comparable() -> None:
    built = build_lab(LABS, "02-tool-overload")
    assert built["baseline"]["metrics"]["catalog_items"] == built["candidate"]["metrics"]["catalog_items"]
    assert built["candidate"]["metrics"]["accuracy"] == 1.0


def test_context_and_reference_labs() -> None:
    mega = build_lab(LABS, "01-mega-instructions")
    skill = build_lab(LABS, "03-mega-skill")
    assert (
        mega["candidate"]["metrics"]["mean_loaded_tokens"] < mega["baseline"]["metrics"]["mean_loaded_tokens"]
    )
    assert skill["candidate"]["metrics"]["success_rate"] == 1.0
    assert (
        skill["candidate"]["metrics"]["mean_irrelevant_tokens"]
        < skill["baseline"]["metrics"]["mean_irrelevant_tokens"]
    )


def test_subagent_and_eager_labs() -> None:
    sub = build_lab(LABS, "05-premature-subagents")
    eager = build_lab(LABS, "06-eager-context")
    assert sub["candidate"]["metrics"]["mean_agent_count"] < sub["baseline"]["metrics"]["mean_agent_count"]
    assert eager["baseline"]["metrics"]["budget_overflow_rate"] == 1.0
    assert eager["candidate"]["metrics"]["budget_overflow_rate"] == 0.0


def test_unknown_lab_rejected() -> None:
    with pytest.raises(ValueError, match="unknown lab"):
        build_lab(LABS, "unknown")


def test_write_to_temporary_copy(tmp_path: Path) -> None:
    import shutil

    target = tmp_path / "labs"
    shutil.copytree(LABS, target)
    for path in (target / "01-mega-instructions" / "results").glob("*.json"):
        path.unlink()
    result = run_lab(target, "01-mega-instructions", write=True)
    assert not result["drift"]
    assert (target / "01-mega-instructions" / "results" / "manifest.json").exists()
