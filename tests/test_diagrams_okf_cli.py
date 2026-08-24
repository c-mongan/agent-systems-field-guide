from __future__ import annotations

import json
from pathlib import Path

from agent_field_guide.cli import main
from agent_field_guide.diagrams import build_diagrams, check_diagrams
from agent_field_guide.okf import export_knowledge

ROOT = Path(__file__).resolve().parents[1]


def test_diagrams_are_current(tmp_path: Path) -> None:
    assert check_diagrams(ROOT / "diagrams") == []
    built = build_diagrams(tmp_path)
    assert "hero.svg" in built
    assert "routing-proof.svg" in built
    assert 'role="img"' in (tmp_path / "hero.svg").read_text()


def test_diagram_drift(tmp_path: Path) -> None:
    build_diagrams(tmp_path)
    (tmp_path / "hero.svg").write_text("broken")
    assert "hero.svg" in check_diagrams(tmp_path)


def test_okf_export(tmp_path: Path) -> None:
    output = tmp_path / "knowledge.json"
    payload = export_knowledge(ROOT, output)
    assert output.exists()
    assert len(payload["records"]) >= 16
    assert {record["type"] for record in payload["records"]} == {"Pattern", "AntiPattern"}


def test_cli_adapter_and_eval(capsys, tmp_path: Path) -> None:
    assert main(["adapter", "render", "codex", "route"]) == 0
    rendered = json.loads(capsys.readouterr().out)
    assert rendered["adapter"] == "codex"
    output = tmp_path / "comparison.json"
    assert (
        main(
            [
                "eval",
                "compare",
                str(ROOT / "evals/fixtures/baseline.jsonl"),
                str(ROOT / "evals/fixtures/candidate.jsonl"),
                "--output",
                str(output),
            ]
        )
        == 0
    )
    result = json.loads(capsys.readouterr().out)
    assert result["paired_cases"] == 6
    assert output.exists()


def test_cli_skill_check_and_lab(capsys) -> None:
    assert main(["check-skills", str(ROOT)]) == 0
    assert json.loads(capsys.readouterr().out)["ok"] is True
    assert main(["lab", "run", "04-overlapping-skills", "--root", str(ROOT)]) == 0
    assert json.loads(capsys.readouterr().out)["ok"] is True


def test_cli_diagrams_and_okf(capsys, tmp_path: Path) -> None:
    assert main(["diagrams", "check", "--root", str(ROOT)]) == 0
    assert json.loads(capsys.readouterr().out)["ok"] is True
    relative = tmp_path.name + "/knowledge.json"
    # export path is relative to the repository root, so use a temporary folder inside it
    target_dir = ROOT / tmp_path.name
    try:
        assert main(["okf", "export", "--root", str(ROOT), "--output", relative]) == 0
        assert json.loads(capsys.readouterr().out)["records"] >= 16
        assert (ROOT / relative).exists()
    finally:
        if target_dir.exists():
            import shutil

            shutil.rmtree(target_dir)


def test_cli_live_adapter_requires_explicit_acknowledgement(capsys, tmp_path: Path) -> None:
    code = main(
        [
            "adapter",
            "run",
            "codex",
            "route",
            "--output-dir",
            str(tmp_path),
        ]
    )
    assert code == 2
    payload = json.loads(capsys.readouterr().err)
    assert payload["error"] == "refusing live execution without --execute"
