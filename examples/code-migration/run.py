#!/usr/bin/env python3
"""Classify migration findings into safe transforms and semantic work."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path
from typing import Any

MECHANICAL = {
    "direct-method-rename",
    "static-import-rename",
    "named-argument-rename",
}


def analyze(data: dict[str, Any]) -> dict[str, Any]:
    findings = sorted(
        data["findings"],
        key=lambda row: (row["package"], row["path"], row["line"]),
    )
    mechanical: list[dict[str, Any]] = []
    semantic: list[dict[str, Any]] = []

    for row in findings:
        is_mechanical = row["pattern"] in MECHANICAL and not row.get("custom_control_flow")
        target = mechanical if is_mechanical else semantic
        target.append(
            {
                "finding_id": row["finding_id"],
                "package": row["package"],
                "path": row["path"],
                "pattern": row["pattern"],
            }
        )

    by_package: dict[str, list[str]] = defaultdict(list)
    for row in semantic:
        by_package[str(row["package"])].append(str(row["finding_id"]))

    leaf_findings = sorted(by_package.get("web-checkout", []) + by_package.get("worker", []))
    batches = [
        {
            "batch": 1,
            "name": "mechanical-codemod",
            "finding_ids": [row["finding_id"] for row in mechanical],
            "gate": "compile + focused tests",
        },
        {
            "batch": 2,
            "name": "semantic-leaf-packages",
            "finding_ids": leaf_findings,
            "gate": "contract + integration tests",
        },
        {
            "batch": 3,
            "name": "semantic-shared-core",
            "finding_ids": sorted(by_package.get("checkout-core", [])),
            "gate": "full regression + canary",
        },
    ]

    return {
        "migration": data["migration"],
        "total_findings": len(findings),
        "mechanical_count": len(mechanical),
        "semantic_count": len(semantic),
        "mechanical": mechanical,
        "semantic": semantic,
        "batches": [batch for batch in batches if batch["finding_ids"]],
        "rollback_boundary": (
            "Keep the compatibility adapter until batch 3 has passed canary and rollback checks."
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    result = analyze(json.loads(args.input.read_text(encoding="utf-8")))
    text = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(text, encoding="utf-8")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
