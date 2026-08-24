#!/usr/bin/env python3
"""Run deterministic authentication and session policy checks."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def analyze(data: dict[str, Any]) -> dict[str, Any]:
    configuration = data["configuration"]
    policy = data["policy"]
    findings: list[dict[str, str]] = []

    def add(code: str, severity: str, evidence: str, fix: str) -> None:
        findings.append(
            {
                "code": code,
                "severity": severity,
                "evidence": evidence,
                "fix": fix,
            }
        )

    cookie = configuration["session_cookie"]
    if policy["require_secure_cookie"] and not cookie["secure"]:
        add(
            "COOKIE_SECURE",
            "high",
            "session_cookie.secure=false",
            "Set Secure on the session cookie.",
        )
    if policy["require_http_only"] and not cookie["http_only"]:
        add(
            "COOKIE_HTTP_ONLY",
            "high",
            "session_cookie.http_only=false",
            "Set HttpOnly on the session cookie.",
        )
    if cookie["same_site"] not in policy["allowed_same_site"]:
        add(
            "COOKIE_SAMESITE",
            "medium",
            f"session_cookie.same_site={cookie['same_site']}",
            "Use an allowed SameSite value and document the cross-site need.",
        )

    oauth = configuration["oauth"]
    if policy["require_pkce"] and not oauth["pkce"]:
        add(
            "OAUTH_PKCE",
            "high",
            "oauth.pkce=false",
            "Require PKCE for the authorization code flow.",
        )
    bad_redirects = sorted(set(oauth["redirect_uris"]) - set(policy["allowed_redirect_uris"]))
    if bad_redirects:
        add(
            "OAUTH_REDIRECT",
            "high",
            f"unapproved redirect URIs: {', '.join(bad_redirects)}",
            "Use exact approved redirect URIs; do not use wildcard hosts.",
        )
    if configuration["browser_token_storage"] != policy["allowed_browser_token_storage"]:
        add(
            "TOKEN_STORAGE",
            "high",
            f"browser_token_storage={configuration['browser_token_storage']}",
            "Store only an opaque session identifier in an HttpOnly cookie.",
        )

    return {
        "review_id": data["review_id"],
        "passed": not findings,
        "finding_count": len(findings),
        "findings": sorted(findings, key=lambda row: (row["severity"], row["code"])),
        "not_checked": [
            "Identity-provider tenant policy",
            "Runtime secret values",
            "Network-layer controls",
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
