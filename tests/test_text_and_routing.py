from __future__ import annotations

from agent_field_guide.models import CatalogItem, RouteCase
from agent_field_guide.routing import evaluate_routes, route_case, score_catalog
from agent_field_guide.text import estimate_tokens, jaccard, tokens


def test_tokens_and_estimate() -> None:
    assert tokens("Use OAuth and PKCE for the browser") == ["oauth", "pkce", "browser"]
    assert estimate_tokens("") == 0
    assert estimate_tokens("abcd") == 1
    assert estimate_tokens("abcde") == 2


def test_jaccard_edges() -> None:
    assert jaccard("", "") == 1.0
    assert jaccard("one", "") == 0.0
    assert jaccard("alpha beta", "beta gamma") == 1 / 3


def test_route_prefers_specific_description() -> None:
    items = [
        CatalogItem("incident", "Investigate production outage latency trace IDs and provider failures."),
        CatalogItem("release", "Plan versions package publish order and changelog."),
    ]
    case = RouteCase("1", "Investigate outage latency using a trace ID", "incident")
    decision = route_case(case, items)
    assert decision.correct
    assert decision.margin > 0
    assert decision.scores["incident"] > decision.scores["release"]


def test_route_rejects_empty_catalogue() -> None:
    case = RouteCase("1", "anything", "x")
    try:
        route_case(case, [])
    except ValueError as exc:
        assert "at least one" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_route_tie_is_stable() -> None:
    items = [CatalogItem("b", "same words"), CatalogItem("a", "same words")]
    decision = route_case(RouteCase("1", "same words", "a"), items)
    assert decision.selected == "a"
    assert decision.margin == 0


def test_evaluate_routes_reports_overlap() -> None:
    items = [CatalogItem("a", "alpha beta"), CatalogItem("b", "alpha gamma")]
    result = evaluate_routes([RouteCase("1", "alpha beta", "a")], items)
    assert result["metrics"]["accuracy"] == 1.0
    assert result["metrics"]["catalog_items"] == 2
    assert len(result["pairwise_overlap"]) == 1
    assert score_catalog("alpha", items)["a"] == score_catalog("alpha", items)["b"]
