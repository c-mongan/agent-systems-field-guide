"""Claude Code headless adapter. It renders commands; it never runs them implicitly."""

from __future__ import annotations

import json
from pathlib import Path

from ..models import AdapterResult, CommandPlan
from .base import HarnessAdapter


class ClaudeCodeAdapter(HarnessAdapter):
    name = "claude-code"

    def __init__(
        self,
        *,
        model: str | None = None,
        max_turns: int = 8,
        permission_mode: str = "plan",
    ) -> None:
        self.model = model
        self.max_turns = max_turns
        self.permission_mode = permission_mode

    def build(self, prompt: str, *, schema_path: Path | None = None) -> CommandPlan:
        argv = [
            "claude",
            "-p",
            "--output-format",
            "json",
            "--no-session-persistence",
            "--max-turns",
            str(self.max_turns),
            "--permission-mode",
            self.permission_mode,
        ]
        if self.model:
            argv.extend(["--model", self.model])
        if schema_path:
            argv.extend(["--json-schema", schema_path.read_text(encoding="utf-8")])
        argv.append(prompt)
        return CommandPlan(adapter=self.name, argv=tuple(argv))

    def parse(self, stdout: str) -> AdapterResult:
        payload = json.loads(stdout)
        structured = payload.get("structured_output")
        if structured is not None:
            text = json.dumps(structured, sort_keys=True)
        else:
            text = str(payload.get("result", payload.get("text", "")))
        success = not bool(payload.get("is_error", False)) and payload.get("subtype") != "error"
        usage: dict[str, float | int] = {}
        for key in ("duration_ms", "duration_api_ms", "num_turns", "total_cost_usd"):
            value = payload.get(key)
            if isinstance(value, (int, float)):
                usage[key] = value
        return AdapterResult(adapter=self.name, text=text, success=success, usage=usage, raw=payload)
