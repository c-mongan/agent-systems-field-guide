#!/usr/bin/env python3
"""Run the repository's core or release verification profile.

The core profile is fully local after Python dependencies are installed. The
release profile adds the pinned third-party static gates and fails when any of
them is unavailable. Nothing is skipped implicitly.
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import subprocess
import sys
import tempfile
import time
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
AGNIX_VERSION = "0.49.0"


def _redact_local_paths(text: str) -> str:
    """Remove checkout and temporary paths from publication reports."""
    redacted = text.replace(str(ROOT), "<repo>")
    temp_root = Path(tempfile.gettempdir())
    for variant in {str(temp_root), str(temp_root.resolve())}:
        redacted = redacted.replace(variant, "<temp>")
    return redacted


@dataclass(frozen=True)
class Step:
    name: str
    argv: list[str]
    ok: bool
    returncode: int
    duration_ms: float
    stdout: str
    stderr: str

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["argv"] = [_redact_local_paths(argument) for argument in self.argv]
        return payload


def _run(
    name: str,
    argv: list[str],
    *,
    env: dict[str, str],
    timeout_seconds: float = 180.0,
) -> Step:
    started = time.monotonic()
    try:
        completed = subprocess.run(
            argv,
            cwd=ROOT,
            env=env,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            check=False,
            timeout=timeout_seconds,
        )
        return Step(
            name=name,
            argv=argv,
            ok=completed.returncode == 0,
            returncode=completed.returncode,
            duration_ms=round((time.monotonic() - started) * 1000, 3),
            stdout=_redact_local_paths(completed.stdout),
            stderr=_redact_local_paths(completed.stderr),
        )
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, str) else ""
        stderr = exc.stderr if isinstance(exc.stderr, str) else ""
        detail = f"timed out after {timeout_seconds:g} seconds"
        if stderr:
            detail = f"{detail}\n{stderr}"
        return Step(
            name=name,
            argv=argv,
            ok=False,
            returncode=124,
            duration_ms=round((time.monotonic() - started) * 1000, 3),
            stdout=_redact_local_paths(stdout),
            stderr=_redact_local_paths(detail),
        )
    except OSError as exc:
        return Step(
            name=name,
            argv=argv,
            ok=False,
            returncode=127,
            duration_ms=round((time.monotonic() - started) * 1000, 3),
            stdout="",
            stderr=_redact_local_paths(str(exc)),
        )


def _example_step(name: str, *, env: dict[str, str], work_dir: Path) -> Step:
    output = work_dir / f"{name}.json"
    step = _run(
        f"example:{name}",
        [
            PYTHON,
            f"examples/{name}/run.py",
            f"examples/{name}/fixtures/input.json",
            "--output",
            str(output),
        ],
        env=env,
    )
    if not step.ok:
        return step
    expected = ROOT / "examples" / name / "expected" / "output.json"
    if output.read_bytes() == expected.read_bytes():
        return step
    return Step(
        name=step.name,
        argv=step.argv,
        ok=False,
        returncode=1,
        duration_ms=step.duration_ms,
        stdout=step.stdout,
        stderr="generated output does not match the frozen expected file",
    )


def _markdown(report: dict[str, Any]) -> str:
    lines = [
        "# Verification report",
        "",
        f"- Profile: `{report['profile']}`",
        f"- Generated: `{report['generated_at']}`",
        f"- Source commit: `{report['source_commit']}`",
        f"- Python: `{report['python']}`",
        f"- Platform: `{report['platform']}`",
        f"- Result: **{'PASS' if report['ok'] else 'FAIL'}**",
        "",
        "| Check | Result | Time |",
        "|---|---:|---:|",
    ]
    for step in report["steps"]:
        lines.append(
            f"| `{step['name']}` | {'PASS' if step['ok'] else 'FAIL'} | {step['duration_ms']:.0f} ms |"
        )
    lines.extend(
        [
            "",
            "## Scope",
            "",
            (
                "`core` verifies code compilation, tests, branch coverage, repository "
                "invariants, frozen labs, diagrams, examples, and the optional "
                "knowledge export."
            ),
            "",
            (
                "`release` runs the same checks plus pinned Ruff, Mypy, and `agnix` "
                "gates. Missing release tools are failures, not skips."
            ),
            "",
            (
                "This report does not claim a live Claude, Codex, Gemini, or Copilot "
                "benchmark. Those require provider credentials, fixed model IDs, and "
                "separately published raw traces."
            ),
            "",
        ]
    )
    failures = [step for step in report["steps"] if not step["ok"]]
    if failures:
        lines.extend(["## Failures", ""])
        for step in failures:
            lines.extend(
                [
                    f"### {step['name']}",
                    "",
                    "```text",
                    (step["stderr"] or step["stdout"] or "No output").strip()[-4000:],
                    "```",
                    "",
                ]
            )
    return "\n".join(lines)


def _git_commit(env: dict[str, str]) -> str:
    step = _run("git-head", ["git", "rev-parse", "HEAD"], env=env)
    return step.stdout.strip() if step.ok else "uncommitted"


def run(profile: str, report_dir: Path) -> int:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT / "src")
    steps: list[Step] = []

    if profile == "release":
        steps.extend(
            [
                _run("ruff-check", ["ruff", "check", "."], env=env),
                _run("ruff-format", ["ruff", "format", "--check", "."], env=env),
                _run("mypy", ["mypy"], env=env),
                _run(
                    "agnix-version",
                    ["npx", "--yes", f"agnix@{AGNIX_VERSION}", "--version"],
                    env=env,
                    timeout_seconds=60.0,
                ),
                _run(
                    "agnix-strict",
                    ["npx", "--yes", f"agnix@{AGNIX_VERSION}", "--strict", "."],
                    env=env,
                    timeout_seconds=120.0,
                ),
            ]
        )
        version_step = next(step for step in steps if step.name == "agnix-version")
        if version_step.ok and AGNIX_VERSION not in version_step.stdout:
            index = steps.index(version_step)
            steps[index] = Step(
                name=version_step.name,
                argv=version_step.argv,
                ok=False,
                returncode=1,
                duration_ms=version_step.duration_ms,
                stdout=version_step.stdout,
                stderr=f"expected agnix {AGNIX_VERSION}",
            )

    steps.append(
        _run(
            "compileall",
            [PYTHON, "-m", "compileall", "-q", "src", "tests", "examples", "scripts"],
            env=env,
        )
    )
    steps.append(_run("coverage-erase", [PYTHON, "-m", "coverage", "erase"], env=env))
    steps.append(_run("tests", [PYTHON, "-m", "coverage", "run", "-m", "pytest", "-q"], env=env))
    steps.append(
        _run(
            "branch-coverage",
            [PYTHON, "-m", "coverage", "report", "--fail-under=90"],
            env=env,
        )
    )
    cli = [PYTHON, "-m", "agent_field_guide.cli"]
    steps.extend(
        [
            _run("skill-spec", [*cli, "check-skills", "."], env=env),
            _run("repository", [*cli, "check", "."], env=env),
            _run("frozen-labs", [*cli, "lab", "run", "all", "--root", "."], env=env),
            _run("diagram-drift", [*cli, "diagrams", "check", "--root", "."], env=env),
        ]
    )

    with tempfile.TemporaryDirectory(prefix="agent-guide-verify-") as temporary:
        work_dir = Path(temporary)
        for example in (
            "incident-response",
            "code-migration",
            "security-review",
            "release-engineering",
        ):
            steps.append(_example_step(example, env=env, work_dir=work_dir))
        steps.append(
            _run(
                "knowledge-export",
                [
                    *cli,
                    "okf",
                    "export",
                    "--root",
                    ".",
                    "--output",
                    str(work_dir / "knowledge.json"),
                ],
                env=env,
            )
        )

    report = {
        "profile": profile,
        "generated_at": datetime.now(UTC).isoformat(),
        "source_commit": _git_commit(env),
        "python": platform.python_version(),
        "platform": platform.platform(),
        "ok": all(step.ok for step in steps),
        "steps": [step.to_dict() for step in steps],
    }
    report_dir.mkdir(parents=True, exist_ok=True)
    (report_dir / "verification.json").write_text(
        json.dumps(report, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    (report_dir / "verification.md").write_text(_markdown(report), encoding="utf-8")
    print(json.dumps({"ok": report["ok"], "profile": profile, "report_dir": str(report_dir)}, indent=2))
    return 0 if report["ok"] else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", choices=("core", "release"), default="core")
    parser.add_argument("--report-dir", type=Path, default=ROOT / "reports")
    args = parser.parse_args()
    return run(args.profile, args.report_dir.resolve())


if __name__ == "__main__":
    raise SystemExit(main())
