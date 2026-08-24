"""Codex non-interactive adapter with a read-only default."""

from __future__ import annotations

import json
from pathlib import Path

from ..models import AdapterResult, CommandPlan
from .base import HarnessAdapter


class CodexAdapter(HarnessAdapter):
    name = "codex"

    def __init__(self, *, model: str | None = None, sandbox: str = "read-only") -> None:
        self.model = model
        self.sandbox = sandbox

    def build(self, prompt: str, *, schema_path: Path | None = None) -> CommandPlan:
        argv = [
            "codex",
            "exec",
            "--ephemeral",
            "--json",
            "--sandbox",
            self.sandbox,
            "--ignore-user-config",
            "--ignore-rules",
        ]
        if self.model:
            argv.extend(["--model", self.model])
        if schema_path:
            argv.extend(["--output-schema", str(schema_path)])
        argv.append(prompt)
        return CommandPlan(adapter=self.name, argv=tuple(argv))

    def parse(self, stdout: str) -> AdapterResult:
        events = [json.loads(line) for line in stdout.splitlines() if line.strip()]
        text_parts: list[str] = []
        usage: dict[str, float | int] = {}
        success = True
        for event in events:
            event_type = str(event.get("type", ""))
            if event_type in {"error", "turn.failed"}:
                success = False
            item = event.get("item")
            if isinstance(item, dict) and item.get("type") == "agent_message":
                text = item.get("text")
                if isinstance(text, str):
                    text_parts.append(text)
            event_usage = event.get("usage")
            if isinstance(event_usage, dict):
                for key, value in event_usage.items():
                    if isinstance(value, (int, float)):
                        usage[str(key)] = value
        return AdapterResult(
            adapter=self.name,
            text="\n".join(text_parts),
            success=success,
            usage=usage,
            raw={"events": events},
        )
