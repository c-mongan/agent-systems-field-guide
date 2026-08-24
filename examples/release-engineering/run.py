#!/usr/bin/env python3
"""Calculate version propagation and publish order for a small monorepo."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict, deque
from pathlib import Path
from typing import Any

RANK = {"none": 0, "patch": 1, "minor": 2, "major": 3}


def analyze(data: dict[str, Any]) -> dict[str, Any]:
    packages = {package["name"]: package for package in data["packages"]}
    bumps = {name: "none" for name in packages}
    reasons: dict[str, list[str]] = defaultdict(list)

    for change in data["changes"]:
        name = str(change["package"])
        bump = str(change["bump"])
        if RANK[bump] > RANK[bumps[name]]:
            bumps[name] = bump
        reasons[name].append(str(change["change_id"]))

    changed = True
    while changed:
        changed = False
        for name, package in packages.items():
            for dependency in package["dependencies"]:
                if bumps[dependency] != "none" and bumps[name] == "none":
                    bumps[name] = "patch"
                    reasons[name].append(f"dependency:{dependency}")
                    changed = True

    indegree = {name: 0 for name in packages}
    outgoing: dict[str, list[str]] = defaultdict(list)
    for name, package in packages.items():
        for dependency in package["dependencies"]:
            outgoing[dependency].append(name)
            indegree[name] += 1

    queue = deque(sorted(name for name, value in indegree.items() if value == 0))
    order: list[str] = []
    while queue:
        name = queue.popleft()
        order.append(name)
        for child in sorted(outgoing[name]):
            indegree[child] -= 1
            if indegree[child] == 0:
                queue.append(child)

    if len(order) != len(packages):
        raise ValueError("package dependency cycle")

    release = [
        {
            "package": name,
            "bump": bumps[name],
            "reasons": sorted(reasons[name]),
        }
        for name in order
        if bumps[name] != "none"
    ]
    return {
        "release_id": data["release_id"],
        "publish_order": [row["package"] for row in release],
        "packages": release,
        "gates": [
            "all package tests pass",
            "generated versions match plan",
            "dry-run publish succeeds",
            "rollback artefacts exist",
        ],
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
