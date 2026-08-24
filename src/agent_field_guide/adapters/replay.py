"""Offline adapter for reproducible CI and frozen trace fixtures."""

from __future__ import annotations

from pathlib import Path

from ..io import read_jsonl
from ..models import AdapterResult, CommandPlan
from .base import HarnessAdapter


class ReplayAdapter(HarnessAdapter):
    name = "replay"

    def __init__(self, trace_path: Path) -> None:
        rows = read_jsonl(trace_path)
        self._rows = {str(row["prompt"]): row for row in rows}

    def build(self, prompt: str, *, schema_path: Path | None = None) -> CommandPlan:
        del schema_path
        return CommandPlan(adapter=self.name, argv=("replay", prompt))

    def parse(self, stdout: str) -> AdapterResult:
        row = self._rows.get(stdout)
        if row is None:
            return AdapterResult(adapter=self.name, text="", success=False, raw={"missing": stdout})
        return AdapterResult(
            adapter=self.name,
            text=str(row.get("response", "")),
            success=bool(row.get("success", True)),
            usage={str(k): v for k, v in dict(row.get("usage", {})).items()},
            raw=row,
        )
