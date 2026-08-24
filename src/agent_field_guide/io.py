"""Stable file IO helpers used by the guide, labs, and tests."""

from __future__ import annotations

import hashlib
import json
from collections.abc import Iterable
from pathlib import Path
from typing import Any


def read_json(path: Path) -> Any:
    """Read a UTF-8 JSON file."""
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    """Write deterministic, human-readable JSON."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(stable_json(value) + "\n", encoding="utf-8")


def stable_json(value: Any) -> str:
    """Return JSON with stable key ordering and no platform-specific output."""
    return json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    """Read JSON Lines, ignoring blank lines."""
    rows: list[dict[str, Any]] = []
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = raw.strip()
        if not line:
            continue
        value = json.loads(line)
        if not isinstance(value, dict):
            raise ValueError(f"{path}:{line_number}: expected a JSON object")
        rows.append(value)
    return rows


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    """Write JSON Lines with stable object key ordering."""
    path.parent.mkdir(parents=True, exist_ok=True)
    content = "\n".join(json.dumps(row, sort_keys=True, ensure_ascii=False) for row in rows)
    path.write_text(content + ("\n" if content else ""), encoding="utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def sha256_paths(paths: Iterable[Path], *, base: Path) -> dict[str, str]:
    """Return path-to-digest entries in stable order."""
    output: dict[str, str] = {}
    for path in sorted(paths):
        output[path.relative_to(base).as_posix()] = sha256_file(path)
    return output
