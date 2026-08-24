"""Deterministic architecture labs with frozen inputs and generated results."""

from __future__ import annotations

import json
from collections.abc import Callable
from pathlib import Path
from statistics import mean
from typing import Any

from . import __version__
from .io import read_json, read_jsonl, sha256_file, stable_json
from .models import CatalogItem, RouteCase
from .routing import evaluate_routes
from .text import estimate_tokens

LAB_NAMES = (
    "01-mega-instructions",
    "02-tool-overload",
    "03-mega-skill",
    "04-overlapping-skills",
    "05-premature-subagents",
    "06-eager-context",
)


def _load_catalog(path: Path) -> list[CatalogItem]:
    data = read_json(path)
    return [CatalogItem(name=str(row["name"]), description=str(row["description"])) for row in data["items"]]


def _load_route_cases(path: Path) -> list[RouteCase]:
    return [
        RouteCase(case_id=str(row["case_id"]), prompt=str(row["prompt"]), expected=str(row["expected"]))
        for row in read_jsonl(path)
    ]


def _context_variant(cases: list[dict[str, Any]], config: dict[str, Any], variant: str) -> dict[str, Any]:
    blocks: dict[str, str] = {str(k): str(v) for k, v in config["blocks"].items()}
    core = str(config.get("core", ""))
    all_block_names = sorted(blocks)
    rows: list[dict[str, Any]] = []
    for case in cases:
        required = {str(value) for value in case["required"]}
        conflicts = {str(value) for value in case.get("conflicts", [])}
        if config["mode"] == "eager":
            loaded = set(all_block_names)
        else:
            loaded = {str(value) for value in case["selected"]}
        loaded_text = "\n".join([core] + [blocks[name] for name in sorted(loaded)])
        relevant_text = "\n".join([core] + [blocks[name] for name in sorted(required)])
        loaded_tokens = estimate_tokens(loaded_text)
        relevant_tokens = estimate_tokens(relevant_text)
        conflict_hits = sorted(loaded & conflicts)
        success = required.issubset(loaded) and not conflict_hits
        rows.append(
            {
                "case_id": case["case_id"],
                "success": success,
                "loaded": sorted(loaded),
                "required": sorted(required),
                "conflict_hits": conflict_hits,
                "loaded_tokens": loaded_tokens,
                "relevant_tokens": relevant_tokens,
                "irrelevant_tokens": max(0, loaded_tokens - relevant_tokens),
            }
        )
    return {
        "variant": variant,
        "metrics": {
            "success_rate": round(mean(float(row["success"]) for row in rows), 6),
            "mean_loaded_tokens": round(mean(row["loaded_tokens"] for row in rows), 6),
            "mean_irrelevant_tokens": round(mean(row["irrelevant_tokens"] for row in rows), 6),
            "mean_conflict_hits": round(mean(len(row["conflict_hits"]) for row in rows), 6),
        },
        "cases": rows,
    }


def _run_context(lab_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    cases = read_jsonl(lab_dir / "cases.jsonl")
    return (
        _context_variant(cases, read_json(lab_dir / "baseline.json"), "baseline"),
        _context_variant(cases, read_json(lab_dir / "candidate.json"), "candidate"),
    )


def _route_variant(lab_dir: Path, filename: str, variant: str) -> dict[str, Any]:
    result = evaluate_routes(_load_route_cases(lab_dir / "cases.jsonl"), _load_catalog(lab_dir / filename))
    return {"variant": variant, **result}


def _run_route(lab_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    return (
        _route_variant(lab_dir, "baseline.json", "baseline"),
        _route_variant(lab_dir, "candidate.json", "candidate"),
    )


def _knowledge_variant(cases: list[dict[str, Any]], config: dict[str, Any], variant: str) -> dict[str, Any]:
    core = str(config["core"])
    references: dict[str, dict[str, str]] = {
        str(name): {str(k): str(v) for k, v in facts.items()} for name, facts in config["references"].items()
    }
    order = [str(value) for value in config["order"]]
    rows: list[dict[str, Any]] = []
    for case in cases:
        domain = str(case["domain"])
        key = str(case["key"])
        expected = str(case["expected"])
        if config["mode"] == "monolith":
            loaded_names = order
            # A monolith with repeated generic keys resolves by document order.
            answer = next((references[name][key] for name in order if key in references[name]), "")
        else:
            loaded_names = [domain]
            answer = references.get(domain, {}).get(key, "")
        loaded_text = (
            core
            + "\n"
            + "\n".join(f"{name}:" + json.dumps(references[name], sort_keys=True) for name in loaded_names)
        )
        relevant_text = core + "\n" + json.dumps(references[domain], sort_keys=True)
        loaded_tokens = estimate_tokens(loaded_text)
        relevant_tokens = estimate_tokens(relevant_text)
        rows.append(
            {
                "case_id": case["case_id"],
                "domain": domain,
                "key": key,
                "answer": answer,
                "expected": expected,
                "success": answer == expected,
                "loaded_references": loaded_names,
                "loaded_tokens": loaded_tokens,
                "irrelevant_tokens": max(0, loaded_tokens - relevant_tokens),
            }
        )
    return {
        "variant": variant,
        "metrics": {
            "success_rate": round(mean(float(row["success"]) for row in rows), 6),
            "mean_loaded_tokens": round(mean(row["loaded_tokens"] for row in rows), 6),
            "mean_irrelevant_tokens": round(mean(row["irrelevant_tokens"] for row in rows), 6),
        },
        "cases": rows,
    }


def _run_knowledge(lab_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    cases = read_jsonl(lab_dir / "cases.jsonl")
    return (
        _knowledge_variant(cases, read_json(lab_dir / "baseline.json"), "baseline"),
        _knowledge_variant(cases, read_json(lab_dir / "candidate.json"), "candidate"),
    )


def _subagent_variant(cases: list[dict[str, Any]], config: dict[str, Any], variant: str) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    spawn_ms = float(config["agent_spawn_ms"])
    agent_tokens = int(config["agent_tokens"])
    agent_failure = float(config["agent_failure_probability"])
    script_ms = float(config["script_ms"])
    script_tokens = int(config["script_tokens"])
    for case in cases:
        branches = int(case["branches"])
        kind = str(case["kind"])
        work_ms = float(case["work_ms"])
        if config["strategy"] == "always-agents" or kind == "independent-reasoning":
            agent_count = branches
            deterministic_count = 0
            latency = spawn_ms + work_ms + (agent_count * float(config["coordination_ms_per_agent"]))
            tokens = agent_count * agent_tokens
            success_probability = (1.0 - agent_failure) ** agent_count
        else:
            agent_count = 0
            deterministic_count = branches
            latency = script_ms * branches
            tokens = script_tokens * branches
            success_probability = 1.0
        rows.append(
            {
                "case_id": case["case_id"],
                "kind": kind,
                "agent_count": agent_count,
                "deterministic_count": deterministic_count,
                "latency_ms": round(latency, 6),
                "input_tokens": tokens,
                "expected_success_probability": round(success_probability, 8),
            }
        )
    return {
        "variant": variant,
        "metrics": {
            "mean_agent_count": round(mean(row["agent_count"] for row in rows), 6),
            "mean_latency_ms": round(mean(row["latency_ms"] for row in rows), 6),
            "mean_input_tokens": round(mean(row["input_tokens"] for row in rows), 6),
            "mean_expected_success_probability": round(
                mean(row["expected_success_probability"] for row in rows), 8
            ),
        },
        "cases": rows,
    }


def _run_subagents(lab_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    cases = read_jsonl(lab_dir / "cases.jsonl")
    return (
        _subagent_variant(cases, read_json(lab_dir / "baseline.json"), "baseline"),
        _subagent_variant(cases, read_json(lab_dir / "candidate.json"), "candidate"),
    )


def _eager_variant(cases: list[dict[str, Any]], config: dict[str, Any], variant: str) -> dict[str, Any]:
    skills: dict[str, dict[str, int]] = {
        str(name): {str(k): int(v) for k, v in values.items()} for name, values in config["skills"].items()
    }
    budget = int(config["context_budget"])
    rows: list[dict[str, Any]] = []
    for case in cases:
        active = str(case["active_skill"])
        references_needed = int(case["references_needed"])
        if config["mode"] == "eager":
            initial = sum(value["body_tokens"] for value in skills.values())
            reference_tokens = sum(value["reference_tokens"] for value in skills.values())
            total = initial + reference_tokens
            relevant = skills[active]["body_tokens"] + min(
                skills[active]["reference_tokens"], references_needed
            )
        else:
            initial = sum(value["catalog_tokens"] for value in skills.values())
            active_body = skills[active]["body_tokens"]
            reference_tokens = min(skills[active]["reference_tokens"], references_needed)
            total = initial + active_body + reference_tokens
            relevant = active_body + reference_tokens
        rows.append(
            {
                "case_id": case["case_id"],
                "active_skill": active,
                "initial_tokens": initial,
                "total_tokens": total,
                "relevant_tokens": relevant,
                "irrelevant_tokens": max(0, total - relevant),
                "budget_overflow": total > budget,
            }
        )
    return {
        "variant": variant,
        "metrics": {
            "mean_initial_tokens": round(mean(row["initial_tokens"] for row in rows), 6),
            "mean_total_tokens": round(mean(row["total_tokens"] for row in rows), 6),
            "mean_irrelevant_tokens": round(mean(row["irrelevant_tokens"] for row in rows), 6),
            "budget_overflow_rate": round(mean(float(row["budget_overflow"]) for row in rows), 6),
        },
        "cases": rows,
    }


def _run_eager(lab_dir: Path) -> tuple[dict[str, Any], dict[str, Any]]:
    cases = read_jsonl(lab_dir / "cases.jsonl")
    return (
        _eager_variant(cases, read_json(lab_dir / "baseline.json"), "baseline"),
        _eager_variant(cases, read_json(lab_dir / "candidate.json"), "candidate"),
    )


_RUNNERS: dict[str, Callable[[Path], tuple[dict[str, Any], dict[str, Any]]]] = {
    "01-mega-instructions": _run_context,
    "02-tool-overload": _run_route,
    "03-mega-skill": _run_knowledge,
    "04-overlapping-skills": _run_route,
    "05-premature-subagents": _run_subagents,
    "06-eager-context": _run_eager,
}


def _metric_direction(name: str) -> str:
    higher = {"accuracy", "mean_margin", "success_rate", "mean_expected_success_probability"}
    return "higher" if name in higher else "lower"


def _compare_metrics(baseline: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    output: dict[str, Any] = {}
    common = sorted(set(baseline["metrics"]) & set(candidate["metrics"]))
    for name in common:
        left = baseline["metrics"][name]
        right = candidate["metrics"][name]
        if not isinstance(left, (int, float)) or not isinstance(right, (int, float)):
            continue
        direction = _metric_direction(name)
        delta = right - left
        improved = delta > 0 if direction == "higher" else delta < 0
        output[name] = {
            "baseline": left,
            "candidate": right,
            "delta": round(delta, 6),
            "direction": direction,
            "improved": improved,
        }
    return output


def build_lab(labs_root: Path, name: str) -> dict[str, Any]:
    if name not in _RUNNERS:
        raise ValueError(f"unknown lab: {name}")
    lab_dir = labs_root / name
    baseline, candidate = _RUNNERS[name](lab_dir)
    comparison = {
        "lab": name,
        "runner_version": __version__,
        "result_type": "deterministic-structural-experiment",
        "model_benchmark": False,
        "metrics": _compare_metrics(baseline, candidate),
    }
    return {"baseline": baseline, "candidate": candidate, "comparison": comparison}


def _expected_files(lab_dir: Path, built: dict[str, Any]) -> dict[Path, str]:
    results_dir = lab_dir / "results"
    outputs = {
        results_dir / "baseline.json": stable_json(built["baseline"]) + "\n",
        results_dir / "candidate.json": stable_json(built["candidate"]) + "\n",
        results_dir / "comparison.json": stable_json(built["comparison"]) + "\n",
    }
    input_paths = [lab_dir / "cases.jsonl", lab_dir / "baseline.json", lab_dir / "candidate.json"]
    manifest = {
        "format_version": 1,
        "lab": lab_dir.name,
        "runner_version": __version__,
        "review_date": "2026-08-24",
        "result_type": "deterministic-structural-experiment",
        "model_benchmark": False,
        "inputs": {path.name: sha256_file(path) for path in input_paths},
        "outputs": {
            path.name: __import__("hashlib").sha256(content.encode("utf-8")).hexdigest()
            for path, content in outputs.items()
        },
    }
    outputs[results_dir / "manifest.json"] = stable_json(manifest) + "\n"
    return outputs


def run_lab(labs_root: Path, name: str, *, write: bool = False) -> dict[str, Any]:
    lab_dir = labs_root / name
    built = build_lab(labs_root, name)
    expected = _expected_files(lab_dir, built)
    drift: list[str] = []
    for path, content in expected.items():
        if write:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        elif not path.exists() or path.read_text(encoding="utf-8") != content:
            drift.append(path.relative_to(labs_root.parent).as_posix())
    return {"lab": name, "drift": drift, "built": built}


def run_all_labs(labs_root: Path, *, write: bool = False) -> list[dict[str, Any]]:
    return [run_lab(labs_root, name, write=write) for name in LAB_NAMES]
