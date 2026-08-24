from __future__ import annotations

import json
import os
from pathlib import Path

import pytest

from agent_field_guide.adapters import (
    ClaudeCodeAdapter,
    CodexAdapter,
    GeminiAdapter,
    ReplayAdapter,
)

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "labs" / "04-overlapping-skills" / "adapter-contracts"


def test_claude_command_is_bounded() -> None:
    plan = ClaudeCodeAdapter(model="claude-test", max_turns=4).build("route this")
    assert plan.argv[:2] == ("claude", "-p")
    assert "--no-session-persistence" in plan.argv
    position = plan.argv.index("--max-turns")
    assert (
        plan.argv[position],
        plan.argv[position + 1],
    ) == ("--max-turns", "4")
    assert "claude-test" in plan.argv


def test_claude_schema_and_parser() -> None:
    schema = CONTRACTS / "output-schema.json"
    plan = ClaudeCodeAdapter().build("route", schema_path=schema)
    assert "--json-schema" in plan.argv
    result = ClaudeCodeAdapter().parse((CONTRACTS / "claude-code-result.json").read_text())
    assert result.success
    assert "production-incident" in result.text
    assert result.usage["num_turns"] == 1


def test_claude_error_parser() -> None:
    result = ClaudeCodeAdapter().parse(json.dumps({"is_error": True, "result": "bad"}))
    assert not result.success


def test_claude_structured_output_parser() -> None:
    result = ClaudeCodeAdapter().parse(json.dumps({"structured_output": {"skill": "production-incident"}}))
    assert result.success
    assert json.loads(result.text)["skill"] == "production-incident"


def test_codex_command_uses_read_only_and_clean_config() -> None:
    plan = CodexAdapter(model="gpt-test").build("route", schema_path=CONTRACTS / "output-schema.json")
    assert plan.argv[:2] == ("codex", "exec")
    assert "--ephemeral" in plan.argv
    assert "read-only" in plan.argv
    assert "--ignore-user-config" in plan.argv
    assert "--ignore-rules" in plan.argv
    assert "--output-schema" in plan.argv


def test_codex_parser() -> None:
    result = CodexAdapter().parse((CONTRACTS / "codex-events.jsonl").read_text())
    assert result.success
    assert "production-incident" in result.text
    assert result.usage["input_tokens"] == 412


def test_codex_parser_marks_error() -> None:
    result = CodexAdapter().parse('{"type":"turn.failed"}\n')
    assert not result.success


def test_gemini_adapter() -> None:
    plan = GeminiAdapter(model="gemini-test").build("route")
    assert plan.argv[0] == "gemini"
    assert "--output-format" in plan.argv
    result = GeminiAdapter().parse(json.dumps({"response": "ok", "stats": {"input_tokens": 10}}))
    assert result.success and result.text == "ok"
    assert result.usage["input_tokens"] == 10
    with pytest.raises(ValueError):
        GeminiAdapter().build("route", schema_path=CONTRACTS / "output-schema.json")


def test_gemini_adapter_marks_error_and_filters_usage() -> None:
    result = GeminiAdapter().parse(
        json.dumps(
            {
                "response": "",
                "error": {"message": "failed"},
                "stats": {"input_tokens": 3, "model": "x"},
            }
        )
    )
    assert not result.success
    assert result.usage == {"input_tokens": 3}


def test_replay_adapter(tmp_path: Path) -> None:
    trace = tmp_path / "trace.jsonl"
    trace.write_text('{"prompt":"p","response":"r","success":true,"usage":{"input_tokens":4}}\n')
    adapter = ReplayAdapter(trace)
    assert adapter.build("p").argv == ("replay", "p")
    found = adapter.parse("p")
    missing = adapter.parse("missing")
    assert found.success and found.text == "r"
    assert not missing.success


def _fake_executable(path: Path, body: str) -> Path:
    path.write_text("#!/usr/bin/env python3\n" + body, encoding="utf-8")
    path.chmod(0o755)
    return path


def test_explicit_runner_records_artifacts_without_prompt(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from agent_field_guide.adapters import run_adapter

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    _fake_executable(
        bin_dir / "claude",
        'import json\nprint(json.dumps({"result":"production-incident","num_turns":1}))\n',
    )
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}")
    output = tmp_path / "run"
    prompt = "private routing prompt"
    record = run_adapter(ClaudeCodeAdapter(), prompt, output_dir=output)
    assert record.success
    assert record.result is not None
    assert record.result["text"] == "production-incident"
    saved = (output / "execution.json").read_text(encoding="utf-8")
    assert prompt not in saved
    assert "<prompt sha256:" in saved
    assert (output / "stdout.txt").exists()
    assert (output / "stderr.txt").exists()


def test_explicit_runner_fails_closed_for_missing_binary(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from agent_field_guide.adapters import run_adapter

    monkeypatch.setenv("PATH", str(tmp_path))
    record = run_adapter(CodexAdapter(), "prompt", output_dir=tmp_path / "run")
    assert not record.success
    assert record.error == "executable not found: codex"
    assert (tmp_path / "run" / "execution.json").exists()


def test_explicit_runner_times_out(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    from agent_field_guide.adapters import run_adapter

    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    _fake_executable(bin_dir / "claude", "import time\ntime.sleep(2)\n")
    monkeypatch.setenv("PATH", f"{bin_dir}{os.pathsep}{os.environ.get('PATH', '')}")
    record = run_adapter(ClaudeCodeAdapter(), "prompt", timeout_seconds=0.01)
    assert not record.success
    assert record.timed_out


def test_explicit_runner_rejects_bad_timeout() -> None:
    from agent_field_guide.adapters import run_adapter

    with pytest.raises(ValueError):
        run_adapter(ClaudeCodeAdapter(), "prompt", timeout_seconds=0)
