"""Explicit, bounded execution for live harness adapters.

The command is run only when a caller invokes this module directly. It never
uses a shell, never records the full ambient environment, and does not persist
the prompt in the execution record by default.
"""

from __future__ import annotations

import hashlib
import os
import shutil
import subprocess
import time
from dataclasses import asdict, dataclass, replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from ..io import stable_json
from ..models import AdapterResult
from .base import HarnessAdapter


@dataclass(frozen=True)
class ExecutionRecord:
    """One explicit adapter execution and its parsed result."""

    adapter: str
    success: bool
    returncode: int | None
    timed_out: bool
    started_at: str
    duration_ms: float
    prompt_sha256: str
    command: tuple[str, ...]
    stdout_path: str | None
    stderr_path: str | None
    result: dict[str, Any] | None
    error: str | None

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        payload["command"] = list(self.command)
        return payload


def _safe_command(argv: tuple[str, ...], prompt: str) -> tuple[str, ...]:
    digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    marker = f"<prompt sha256:{digest}>"
    return tuple(marker if value == prompt else value for value in argv)


def _write_artifacts(
    output_dir: Path | None,
    stdout: str,
    stderr: str,
    record: ExecutionRecord,
) -> ExecutionRecord:
    if output_dir is None:
        return record
    output_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = output_dir / "stdout.txt"
    stderr_path = output_dir / "stderr.txt"
    stdout_path.write_text(stdout, encoding="utf-8")
    stderr_path.write_text(stderr, encoding="utf-8")
    updated = replace(
        record,
        stdout_path=stdout_path.name,
        stderr_path=stderr_path.name,
    )
    (output_dir / "execution.json").write_text(
        stable_json(updated.to_dict()) + "\n",
        encoding="utf-8",
    )
    return updated


def run_adapter(
    adapter: HarnessAdapter,
    prompt: str,
    *,
    schema_path: Path | None = None,
    timeout_seconds: float = 120.0,
    cwd: Path | None = None,
    output_dir: Path | None = None,
) -> ExecutionRecord:
    """Run one explicitly selected harness command without a shell.

    Raw stdout and stderr are saved only when ``output_dir`` is provided. The
    record stores a prompt hash instead of the prompt itself.
    """

    if timeout_seconds <= 0:
        raise ValueError("timeout_seconds must be greater than zero")

    plan = adapter.build(prompt, schema_path=schema_path)
    if not plan.argv:
        raise ValueError("adapter returned an empty command")

    digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()
    safe_command = _safe_command(plan.argv, prompt)
    started_at = datetime.now(UTC).isoformat()
    started = time.monotonic()
    stdout = ""
    stderr = ""

    executable = shutil.which(plan.argv[0])
    if executable is None:
        record = ExecutionRecord(
            adapter=adapter.name,
            success=False,
            returncode=None,
            timed_out=False,
            started_at=started_at,
            duration_ms=round((time.monotonic() - started) * 1000, 3),
            prompt_sha256=digest,
            command=safe_command,
            stdout_path=None,
            stderr_path=None,
            result=None,
            error=f"executable not found: {plan.argv[0]}",
        )
        return _write_artifacts(output_dir, stdout, stderr, record)

    env = os.environ.copy()
    env.update(plan.env)
    try:
        completed = subprocess.run(
            [executable, *plan.argv[1:]],
            input=plan.stdin,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout_seconds,
            cwd=cwd,
            env=env,
            check=False,
        )
        stdout = completed.stdout
        stderr = completed.stderr
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout if isinstance(exc.stdout, str) else ""
        stderr = exc.stderr if isinstance(exc.stderr, str) else ""
        record = ExecutionRecord(
            adapter=adapter.name,
            success=False,
            returncode=None,
            timed_out=True,
            started_at=started_at,
            duration_ms=round((time.monotonic() - started) * 1000, 3),
            prompt_sha256=digest,
            command=safe_command,
            stdout_path=None,
            stderr_path=None,
            result=None,
            error=f"execution exceeded {timeout_seconds:g} seconds",
        )
        return _write_artifacts(output_dir, stdout, stderr, record)

    parsed: AdapterResult | None = None
    parse_error: str | None = None
    try:
        parsed = adapter.parse(stdout)
    except (KeyError, TypeError, ValueError) as exc:
        parse_error = f"could not parse adapter output: {exc}"

    success = completed.returncode == 0 and parsed is not None and parsed.success
    error = parse_error
    if completed.returncode != 0:
        error = f"command exited with code {completed.returncode}"
    elif parsed is not None and not parsed.success:
        error = "adapter reported an unsuccessful result"

    record = ExecutionRecord(
        adapter=adapter.name,
        success=success,
        returncode=completed.returncode,
        timed_out=False,
        started_at=started_at,
        duration_ms=round((time.monotonic() - started) * 1000, 3),
        prompt_sha256=digest,
        command=safe_command,
        stdout_path=None,
        stderr_path=None,
        result=parsed.to_dict() if parsed is not None else None,
        error=error,
    )
    return _write_artifacts(output_dir, stdout, stderr, record)
