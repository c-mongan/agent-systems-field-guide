#!/usr/bin/env python3
"""Correlate a frozen incident event set into an evidence-first diagnosis."""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from datetime import datetime
from pathlib import Path
from typing import Any


def parse_time(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def analyze(data: dict[str, Any]) -> dict[str, Any]:
    events = sorted(
        data["events"],
        key=lambda row: (parse_time(row["timestamp"]), row["event_id"]),
    )
    by_request: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in events:
        if event.get("request_id"):
            by_request[str(event["request_id"])].append(event)

    failed_requests: list[str] = []
    provider_timeout_requests: list[str] = []
    database_error_requests: list[str] = []
    for request_id, rows in sorted(by_request.items()):
        if any(row["severity"] == "error" for row in rows):
            failed_requests.append(request_id)
        if any(row["component"] == "payment-provider" and row["code"] == "UPSTREAM_TIMEOUT" for row in rows):
            provider_timeout_requests.append(request_id)
        if any(row["component"] == "database" and row["severity"] == "error" for row in rows):
            database_error_requests.append(request_id)

    component_errors = Counter(row["component"] for row in events if row["severity"] == "error")
    leading_boundary = "unknown"
    confidence = "low"
    reasons: list[str] = []
    if provider_timeout_requests and not database_error_requests:
        leading_boundary = "payment-provider"
        confidence = "high" if len(provider_timeout_requests) >= 2 else "medium"
        reasons.extend(
            [
                "Repeated upstream timeout events occur at the payment-provider boundary.",
                "Database events remain successful for the same requests.",
            ]
        )
    elif database_error_requests:
        leading_boundary = "database"
        confidence = "medium"
        reasons.append("Database errors occur in failed request chains.")

    failed_set = set(failed_requests)
    evidence_ids = [
        row["event_id"]
        for row in events
        if row["request_id"] in failed_set
        and (row["severity"] == "error" or row["component"] in {"database", "payment-provider"})
    ]
    if leading_boundary == "payment-provider":
        containment = "Disable automatic payment retries and route failed requests to a manual retry queue."
    else:
        containment = "Collect more evidence before changing production behaviour."

    return {
        "incident_id": data["incident_id"],
        "failed_requests": failed_requests,
        "leading_boundary": leading_boundary,
        "confidence": confidence,
        "reasons": reasons,
        "component_error_counts": dict(sorted(component_errors.items())),
        "evidence_event_ids": evidence_ids,
        "containment": containment,
        "unknowns": ["The provider's internal root cause is not present in this dataset."],
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
