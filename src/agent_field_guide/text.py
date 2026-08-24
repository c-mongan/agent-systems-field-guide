"""Small deterministic text functions. These are not model tokenizers."""

from __future__ import annotations

import math
import re
from collections import Counter

_TOKEN_RE = re.compile(r"[a-z0-9][a-z0-9+.#/_-]*", re.IGNORECASE)
_STOP_WORDS = {
    "a",
    "an",
    "and",
    "are",
    "as",
    "at",
    "be",
    "by",
    "for",
    "from",
    "in",
    "is",
    "it",
    "of",
    "on",
    "or",
    "that",
    "the",
    "this",
    "to",
    "use",
    "when",
    "with",
    "you",
    "your",
}


def tokens(text: str) -> list[str]:
    return [token.lower() for token in _TOKEN_RE.findall(text) if token.lower() not in _STOP_WORDS]


def token_counts(text: str) -> Counter[str]:
    return Counter(tokens(text))


def estimate_tokens(text: str) -> int:
    """Estimate model tokens using ceil(UTF-8 characters / 4).

    The estimate is intentionally simple and is used only for controlled comparisons.
    It must not be presented as a provider billing count.
    """
    return max(1, math.ceil(len(text.encode("utf-8")) / 4)) if text else 0


def jaccard(left: str, right: str) -> float:
    a, b = set(tokens(left)), set(tokens(right))
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)
