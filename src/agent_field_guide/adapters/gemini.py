"""Gemini CLI headless adapter, included as an additional portability example."""

from __future__ import annotations

import json
from pathlib import Path

from ..models import AdapterResult, CommandPlan
from .base import HarnessAdapter


class GeminiAdapter(HarnessAdapter):
    name = "gemini"

    def __init__(self, *, model: str | None = None) -> None:
        self.model = model

    def build(self, prompt: str, *, schema_path: Path | None = None) -> CommandPlan:
        if schema_path is not None:
            raise ValueError("Gemini adapter does not map a local JSON schema flag in this guide")
        argv = ["gemini", "-p", prompt, "--output-format", "json"]
        if self.model:
            argv.extend(["--model", self.model])
        return CommandPlan(adapter=self.name, argv=tuple(argv))

    def parse(self, stdout: str) -> AdapterResult:
        payload = json.loads(stdout)
        text = str(payload.get("response", payload.get("result", "")))
        stats = payload.get("stats")
        usage: dict[str, float | int] = {}
        if isinstance(stats, dict):
            for key, value in stats.items():
                if isinstance(value, (int, float)):
                    usage[str(key)] = value
        success = not bool(payload.get("error"))
        return AdapterResult(adapter=self.name, text=text, success=success, usage=usage, raw=payload)
