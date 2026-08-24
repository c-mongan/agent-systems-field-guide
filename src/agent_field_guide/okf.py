"""Optional OKF-like export from human-first Markdown metadata."""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from .io import stable_json
from .validation import parse_frontmatter


def export_knowledge(root: Path, output: Path) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    for directory, kind in (("patterns", "Pattern"), ("anti-patterns", "AntiPattern")):
        for path in sorted((root / directory).glob("*.md")):
            metadata, body = parse_frontmatter(path)
            title_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
            records.append(
                {
                    "type": kind,
                    "id": metadata.get("id", path.stem),
                    "title": title_match.group(1) if title_match else path.stem,
                    "status": metadata.get("status", "draft"),
                    "evidence": metadata.get("evidence", []),
                    "source_path": path.relative_to(root).as_posix(),
                    "content": body.strip(),
                }
            )
    payload = {
        "format": "agent-systems-field-guide-knowledge",
        "format_version": "1.0",
        "okf_alignment": "optional-export; human Markdown remains canonical",
        "records": records,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(stable_json(payload) + "\n", encoding="utf-8")
    return payload
