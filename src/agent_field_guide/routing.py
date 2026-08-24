"""Deterministic catalogue routing used by controlled overlap labs."""

from __future__ import annotations

import math
from collections import Counter
from collections.abc import Iterable
from itertools import combinations

from .models import CatalogItem, RouteCase, RouteDecision
from .text import jaccard, token_counts, tokens


def _inverse_document_frequency(items: list[CatalogItem]) -> dict[str, float]:
    document_count = max(1, len(items))
    frequencies: Counter[str] = Counter()
    for item in items:
        frequencies.update(set(tokens(item.description)))
    return {token: math.log((document_count + 1) / (count + 1)) + 1.0 for token, count in frequencies.items()}


def score_catalog(prompt: str, items: list[CatalogItem]) -> dict[str, float]:
    """Score a prompt against item descriptions using deterministic weighted overlap."""
    prompt_counts = token_counts(prompt)
    idf = _inverse_document_frequency(items)
    scores: dict[str, float] = {}
    prompt_lower = prompt.lower()
    for item in items:
        description_counts = token_counts(item.description)
        score = 0.0
        for token, prompt_count in prompt_counts.items():
            if token in description_counts:
                score += min(prompt_count, description_counts[token]) * idf.get(token, 1.0)
        # Exact multi-word fragments receive a small tie-breaking bonus.
        phrases = [part.strip() for part in item.description.lower().split(",") if len(part.split()) >= 2]
        score += sum(0.35 for phrase in phrases if phrase in prompt_lower)
        scores[item.name] = round(score, 6)
    return scores


def route_case(case: RouteCase, items: list[CatalogItem]) -> RouteDecision:
    if not items:
        raise ValueError("catalogue must contain at least one item")
    scores = score_catalog(case.prompt, items)
    ranked = sorted(scores.items(), key=lambda pair: (-pair[1], pair[0]))
    selected, score = ranked[0]
    runner_up = ranked[1][1] if len(ranked) > 1 else 0.0
    return RouteDecision(
        case_id=case.case_id,
        expected=case.expected,
        selected=selected,
        score=score,
        runner_up_score=runner_up,
        margin=round(score - runner_up, 6),
        correct=selected == case.expected,
        scores=scores,
    )


def evaluate_routes(cases: Iterable[RouteCase], items: list[CatalogItem]) -> dict[str, object]:
    decisions = [route_case(case, items) for case in cases]
    count = len(decisions)
    accuracy = sum(decision.correct for decision in decisions) / count if count else 0.0
    # A margin <= 0.5 is deliberately treated as an ambiguous structural route.
    ambiguous = sum(decision.margin <= 0.5 for decision in decisions)
    pairwise: list[dict[str, str | float]] = []
    overlaps: list[float] = []
    for left, right in combinations(items, 2):
        overlap = round(jaccard(left.description, right.description), 6)
        overlaps.append(overlap)
        pairwise.append({"left": left.name, "right": right.name, "jaccard": overlap})
    mean_overlap = sum(overlaps) / len(overlaps) if overlaps else 0.0
    max_overlap = max(overlaps, default=0.0)
    return {
        "metrics": {
            "accuracy": round(accuracy, 6),
            "ambiguity_rate": round(ambiguous / count, 6) if count else 0.0,
            "mean_margin": round(sum(d.margin for d in decisions) / count, 6) if count else 0.0,
            "mean_pairwise_overlap": round(mean_overlap, 6),
            "max_pairwise_overlap": round(max_overlap, 6),
            "catalog_items": len(items),
        },
        "decisions": [decision.to_dict() for decision in decisions],
        "pairwise_overlap": pairwise,
    }
