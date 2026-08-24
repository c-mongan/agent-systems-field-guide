"""Fail-closed repository and Agent Skills validation."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .io import read_json
from .labs import LAB_NAMES, run_all_labs

_LINK_RE = re.compile(r"(?<!!)\[[^\]]+\]\(([^)]+)\)")
_NAME_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
_ACTION_RE = re.compile(r"^\s*uses:\s*([^\s#]+)", re.MULTILINE)
_FULL_SHA_RE = re.compile(r"^[^@]+@[0-9a-f]{40}$")


@dataclass(frozen=True)
class Finding:
    level: str
    code: str
    path: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {
            "level": self.level,
            "code": self.code,
            "path": self.path,
            "message": self.message,
        }


def parse_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening YAML frontmatter delimiter")
    try:
        end = lines[1:].index("---") + 1
    except ValueError as exc:
        raise ValueError("missing closing YAML frontmatter delimiter") from exc
    metadata: dict[str, Any] = {}
    current_list: str | None = None
    for raw in lines[1:end]:
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        if raw.startswith("  - ") and current_list:
            metadata.setdefault(current_list, []).append(raw[4:].strip())
            continue
        if ":" not in raw:
            raise ValueError(f"unsupported frontmatter line: {raw}")
        key, value = raw.split(":", 1)
        key, value = key.strip(), value.strip()
        if not value:
            metadata[key] = []
            current_list = key
        else:
            metadata[key] = value.strip("\"'")
            current_list = None
    return metadata, "\n".join(lines[end + 1 :])


def validate_skill(skill_dir: Path, root: Path) -> list[Finding]:
    findings: list[Finding] = []
    skill_file = skill_dir / "SKILL.md"
    relative = skill_file.relative_to(root).as_posix()
    if not skill_file.exists():
        return [Finding("error", "SKILL-001", relative, "SKILL.md is missing")]
    try:
        metadata, body = parse_frontmatter(skill_file)
    except ValueError as exc:
        return [Finding("error", "SKILL-002", relative, str(exc))]
    name = str(metadata.get("name", ""))
    description = str(metadata.get("description", ""))
    if not name or not _NAME_RE.fullmatch(name) or len(name) > 64:
        findings.append(
            Finding(
                "error",
                "SKILL-003",
                relative,
                "name must match the Agent Skills naming rule",
            )
        )
    if name != skill_dir.name:
        findings.append(Finding("error", "SKILL-004", relative, "name must match the parent directory"))
    if not description or len(description) > 1024:
        findings.append(Finding("error", "SKILL-005", relative, "description must contain 1-1024 characters"))
    line_count = len(skill_file.read_text(encoding="utf-8").splitlines())
    if line_count >= 500:
        findings.append(Finding("error", "SKILL-006", relative, "SKILL.md must stay under 500 lines"))
    if "when" not in description.lower() and "use" not in description.lower():
        findings.append(
            Finding(
                "warning",
                "SKILL-007",
                relative,
                "description should state when to use the skill",
            )
        )
    for link in _LINK_RE.findall(body):
        target = link.split("#", 1)[0].strip()
        if not target or "://" in target or target.startswith("mailto:"):
            continue
        destination = (skill_dir / target).resolve()
        try:
            destination.relative_to(skill_dir.resolve())
        except ValueError:
            findings.append(Finding("error", "SKILL-008", relative, f"reference leaves skill root: {target}"))
            continue
        if not destination.exists():
            findings.append(Finding("error", "SKILL-009", relative, f"missing referenced file: {target}"))
        if target.count("/") > 1:
            findings.append(
                Finding(
                    "warning",
                    "SKILL-010",
                    relative,
                    f"keep references one level deep: {target}",
                )
            )
    return findings


def validate_links(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for path in sorted(root.rglob("*.md")):
        if any(part in {".git", ".venv", "site"} for part in path.parts):
            continue
        text = path.read_text(encoding="utf-8")
        for target in _LINK_RE.findall(text):
            target = target.strip().split(" ", 1)[0].strip("<>")
            if not target or target.startswith("#") or "://" in target or target.startswith("mailto:"):
                continue
            raw = target.split("#", 1)[0]
            destination = (path.parent / raw).resolve()
            if not destination.exists():
                findings.append(
                    Finding(
                        "error",
                        "LINK-001",
                        path.relative_to(root).as_posix(),
                        f"missing local target: {target}",
                    )
                )
    return findings


def validate_evidence(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    claims_path = root / "sources" / "claims.json"
    sources_path = root / "sources" / "sources.json"
    if not claims_path.exists() or not sources_path.exists():
        return [Finding("error", "EVID-001", "sources", "sources.json and claims.json are required")]
    claims = read_json(claims_path)
    sources = read_json(sources_path)
    source_ids = {str(item["id"]) for item in sources}
    claim_ids = {str(item["id"]) for item in claims}
    for claim in claims:
        for source_id in claim.get("sources", []):
            if source_id not in source_ids:
                findings.append(
                    Finding(
                        "error",
                        "EVID-002",
                        "sources/claims.json",
                        f"unknown source: {source_id}",
                    )
                )
    evidence_paths = [
        *root.glob("patterns/*.md"),
        *root.glob("anti-patterns/*.md"),
        *root.glob("docs/**/*.md"),
    ]
    for path in sorted(evidence_paths):
        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            if "Evidence:" not in line:
                continue
            suffix = line.split("Evidence:", 1)[1]
            for claim_id in re.findall(r"`([^`]+)`", suffix):
                if claim_id not in claim_ids:
                    findings.append(
                        Finding(
                            "error",
                            "EVID-003",
                            path.relative_to(root).as_posix(),
                            f"unknown claim ID: {claim_id}",
                        )
                    )
    return findings


def validate_labs(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    labs_root = root / "labs"
    for name in LAB_NAMES:
        lab = labs_root / name
        for required in ("README.md", "cases.jsonl", "baseline.json", "candidate.json"):
            if not (lab / required).exists():
                findings.append(Finding("error", "LAB-001", f"labs/{name}", f"missing {required}"))
    for result in run_all_labs(labs_root, write=False):
        for path in result["drift"]:
            findings.append(Finding("error", "LAB-002", path, "generated lab result drift"))
    return findings


def validate_ci(root: Path) -> list[Finding]:
    workflow = root / ".github" / "workflows" / "validate.yml"
    if not workflow.exists():
        return [Finding("error", "CI-001", str(workflow), "validation workflow is missing")]
    text = workflow.read_text(encoding="utf-8")
    findings: list[Finding] = []
    if "@latest" in text:
        findings.append(
            Finding(
                "error",
                "CI-002",
                ".github/workflows/validate.yml",
                "floating @latest is forbidden",
            )
        )
    verify_script = root / "scripts" / "verify.py"
    verify_text = verify_script.read_text(encoding="utf-8") if verify_script.exists() else ""
    if 'AGNIX_VERSION = "0.49.0"' not in verify_text:
        findings.append(
            Finding(
                "error",
                "CI-003",
                "scripts/verify.py",
                "agnix must be pinned to 0.49.0",
            )
        )
    if "scripts/verify.py --profile release" not in text:
        findings.append(
            Finding(
                "error",
                "CI-004",
                ".github/workflows/validate.yml",
                "the fail-closed release verification profile must run",
            )
        )
    if 'node-version: "24.19.0"' not in text:
        findings.append(
            Finding(
                "error",
                "CI-007",
                ".github/workflows/validate.yml",
                "Node.js must be pinned for the agnix gate",
            )
        )
    for action in _ACTION_RE.findall(text):
        if action.startswith("./"):
            continue
        if not _FULL_SHA_RE.fullmatch(action):
            findings.append(
                Finding(
                    "error",
                    "CI-005",
                    ".github/workflows/validate.yml",
                    f"action is not SHA-pinned: {action}",
                )
            )
    forbidden = ("|| true", "continue-on-error: true", "command -v skills-ref")
    for phrase in forbidden:
        if phrase in text:
            findings.append(
                Finding(
                    "error",
                    "CI-006",
                    ".github/workflows/validate.yml",
                    f"silent/optional gate found: {phrase}",
                )
            )
    return findings


def validate_examples(root: Path) -> list[Finding]:
    findings: list[Finding] = []
    for name in ("incident-response", "code-migration", "security-review", "release-engineering"):
        directory = root / "examples" / name
        for required in ("README.md", "run.py", "fixtures/input.json", "expected/output.json"):
            if not (directory / required).exists():
                findings.append(Finding("error", "EX-001", f"examples/{name}", f"missing {required}"))
    return findings


def validate_repository(root: Path) -> dict[str, Any]:
    findings: list[Finding] = []
    findings.extend(validate_links(root))
    findings.extend(validate_evidence(root))
    findings.extend(validate_labs(root))
    findings.extend(validate_ci(root))
    findings.extend(validate_examples(root))
    skills = sorted({path.parent for path in root.rglob("SKILL.md") if ".git" not in path.parts})
    for skill in skills:
        findings.extend(validate_skill(skill, root))
    errors = [finding for finding in findings if finding.level == "error"]
    warnings = [finding for finding in findings if finding.level == "warning"]
    return {
        "ok": not errors,
        "errors": len(errors),
        "warnings": len(warnings),
        "findings": [finding.to_dict() for finding in findings],
    }


def findings_as_text(report: dict[str, Any]) -> str:
    lines = [f"errors={report['errors']} warnings={report['warnings']}"]
    for finding in report["findings"]:
        lines.append(f"{finding['level'].upper()} {finding['code']} {finding['path']}: {finding['message']}")
    return "\n".join(lines)
