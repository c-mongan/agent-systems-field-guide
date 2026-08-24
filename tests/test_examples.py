from __future__ import annotations

import importlib.util
import json
from pathlib import Path
from types import ModuleType

ROOT = Path(__file__).resolve().parents[1]


def load_module(name: str) -> ModuleType:
    path = ROOT / "examples" / name / "run.py"
    spec = importlib.util.spec_from_file_location(f"example_{name.replace('-', '_')}", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_examples_match_frozen_output() -> None:
    for name in ("incident-response", "code-migration", "security-review", "release-engineering"):
        module = load_module(name)
        data = json.loads((ROOT / "examples" / name / "fixtures" / "input.json").read_text())
        expected = json.loads((ROOT / "examples" / name / "expected" / "output.json").read_text())
        assert module.analyze(data) == expected


def test_incident_unknown_boundary() -> None:
    module = load_module("incident-response")
    result = module.analyze({"incident_id": "x", "events": []})
    assert result["leading_boundary"] == "unknown"
    assert result["containment"].startswith("Collect")


def test_incident_database_boundary() -> None:
    module = load_module("incident-response")
    data = {
        "incident_id": "x",
        "events": [
            {
                "event_id": "e",
                "timestamp": "2026-01-01T00:00:00Z",
                "request_id": "r",
                "component": "database",
                "severity": "error",
                "code": "DB_ERROR",
            }
        ],
    }
    assert module.analyze(data)["leading_boundary"] == "database"


def test_release_cycle_rejected() -> None:
    module = load_module("release-engineering")
    data = {
        "release_id": "x",
        "packages": [
            {"name": "a", "dependencies": ["b"]},
            {"name": "b", "dependencies": ["a"]},
        ],
        "changes": [],
    }
    try:
        module.analyze(data)
    except ValueError as exc:
        assert "cycle" in str(exc)
    else:
        raise AssertionError("expected dependency cycle")
