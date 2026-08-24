from __future__ import annotations

from pathlib import Path

from agent_field_guide.validation import (
    findings_as_text,
    parse_frontmatter,
    validate_ci,
    validate_evidence,
    validate_links,
    validate_repository,
    validate_skill,
)

ROOT = Path(__file__).resolve().parents[1]


def test_repository_validation_passes() -> None:
    report = validate_repository(ROOT)
    assert report["ok"], findings_as_text(report)
    assert report["errors"] == 0


def test_frontmatter_parser() -> None:
    metadata, body = parse_frontmatter(ROOT / ".agents" / "skills" / "architecture-review" / "SKILL.md")
    assert metadata["name"] == "architecture-review"
    assert "Architecture review" in body


def test_skill_validator_catches_name_and_link(tmp_path: Path) -> None:
    skill = tmp_path / "bad-skill"
    skill.mkdir()
    (skill / "SKILL.md").write_text("---\nname: Wrong\ndescription: Tiny\n---\n[missing](references/no.md)\n")
    findings = validate_skill(skill, tmp_path)
    codes = {item.code for item in findings}
    assert {"SKILL-003", "SKILL-004", "SKILL-007", "SKILL-009"}.issubset(codes)


def test_skill_validator_missing_file(tmp_path: Path) -> None:
    findings = validate_skill(tmp_path / "absent", tmp_path)
    assert findings[0].code == "SKILL-001"


def test_parse_frontmatter_errors(tmp_path: Path) -> None:
    path = tmp_path / "x.md"
    path.write_text("no frontmatter")
    try:
        parse_frontmatter(path)
    except ValueError as exc:
        assert "opening" in str(exc)
    else:
        raise AssertionError("expected ValueError")
    path.write_text("---\nname: x\n")
    try:
        parse_frontmatter(path)
    except ValueError as exc:
        assert "closing" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_link_validator_finds_missing(tmp_path: Path) -> None:
    (tmp_path / "a.md").write_text("[bad](missing.md)\n[external](https://example.com)\n")
    findings = validate_links(tmp_path)
    assert len(findings) == 1 and findings[0].code == "LINK-001"


def test_ci_validator_rejects_latest(tmp_path: Path) -> None:
    workflow = tmp_path / ".github" / "workflows"
    workflow.mkdir(parents=True)
    (workflow / "validate.yml").write_text("uses: actions/checkout@v6\nrun: npx agnix@latest || true\n")
    codes = {item.code for item in validate_ci(tmp_path)}
    assert {"CI-002", "CI-003", "CI-004", "CI-005", "CI-006"}.issubset(codes)


def test_evidence_validator_checks_every_claim_id(tmp_path: Path) -> None:
    sources = tmp_path / "sources"
    docs = tmp_path / "docs"
    sources.mkdir()
    docs.mkdir()
    (sources / "sources.json").write_text('[{"id": "source-a"}]\n')
    (sources / "claims.json").write_text('[{"id": "known", "sources": ["source-a"]}]\n')
    (docs / "guide.md").write_text("**Evidence:** `known`, `unknown-second`\n", encoding="utf-8")

    findings = validate_evidence(tmp_path)

    assert [(item.code, item.message) for item in findings] == [
        ("EVID-003", "unknown claim ID: unknown-second"),
    ]
