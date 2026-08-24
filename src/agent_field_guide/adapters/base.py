"""Adapter contracts for live harnesses and frozen replays."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from ..models import AdapterResult, CommandPlan


class HarnessAdapter(ABC):
    """Build a bounded command and parse one provider result."""

    name: str

    @abstractmethod
    def build(self, prompt: str, *, schema_path: Path | None = None) -> CommandPlan:
        raise NotImplementedError

    @abstractmethod
    def parse(self, stdout: str) -> AdapterResult:
        raise NotImplementedError
