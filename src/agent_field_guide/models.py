"""Typed records shared by routing, adapters, and evaluation."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class CatalogItem:
    name: str
    description: str


@dataclass(frozen=True)
class RouteCase:
    case_id: str
    prompt: str
    expected: str


@dataclass(frozen=True)
class RouteDecision:
    case_id: str
    expected: str
    selected: str
    score: float
    runner_up_score: float
    margin: float
    correct: bool
    scores: dict[str, float]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class EvalRecord:
    case_id: str
    success: bool
    latency_ms: float = 0.0
    input_tokens: int = 0
    output_tokens: int = 0
    tool_calls: int = 0
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass(frozen=True)
class CommandPlan:
    adapter: str
    argv: tuple[str, ...]
    stdin: str | None = None
    env: dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "adapter": self.adapter,
            "argv": list(self.argv),
            "stdin": self.stdin,
            "env": dict(self.env),
        }


@dataclass(frozen=True)
class AdapterResult:
    adapter: str
    text: str
    success: bool
    usage: dict[str, float | int] = field(default_factory=dict)
    raw: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)
