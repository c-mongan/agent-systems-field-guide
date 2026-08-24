"""Command-line interface for the executable field guide."""

from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path

from .adapters import ClaudeCodeAdapter, CodexAdapter, GeminiAdapter, HarnessAdapter, run_adapter
from .compare import compare_records
from .diagrams import build_diagrams, check_diagrams
from .io import read_jsonl, stable_json, write_json
from .labs import LAB_NAMES, run_all_labs, run_lab
from .models import EvalRecord
from .okf import export_knowledge
from .validation import findings_as_text, validate_repository, validate_skill


def _root(value: str) -> Path:
    return Path(value).resolve()


def _adapter(name: str, *, model: str | None = None) -> HarnessAdapter:
    if name == "claude-code":
        return ClaudeCodeAdapter(model=model)
    if name == "codex":
        return CodexAdapter(model=model)
    if name == "gemini":
        return GeminiAdapter(model=model)
    raise ValueError(name)


def _records(path: Path) -> list[EvalRecord]:
    output: list[EvalRecord] = []
    for row in read_jsonl(path):
        output.append(
            EvalRecord(
                case_id=str(row["case_id"]),
                success=bool(row["success"]),
                latency_ms=float(row.get("latency_ms", 0.0)),
                input_tokens=int(row.get("input_tokens", 0)),
                output_tokens=int(row.get("output_tokens", 0)),
                tool_calls=int(row.get("tool_calls", 0)),
                metadata=dict(row.get("metadata", {})),
            )
        )
    return output


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agent-guide",
        description="Evaluate agent-system architecture with frozen evidence.",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    check = sub.add_parser("check", help="Run all local fail-closed repository checks")
    check.add_argument("root", nargs="?", default=".")
    check.add_argument("--json", action="store_true")

    skills = sub.add_parser("check-skills", help="Validate every Agent Skills directory")
    skills.add_argument("root", nargs="?", default=".")

    lab = sub.add_parser("lab", help="Run or verify controlled labs")
    lab_sub = lab.add_subparsers(dest="lab_command", required=True)
    lab_run = lab_sub.add_parser("run")
    lab_run.add_argument("name", choices=["all", *LAB_NAMES])
    lab_run.add_argument("--root", default=".")
    lab_run.add_argument("--write", action="store_true", help="Regenerate committed result files")

    evaluate = sub.add_parser("eval", help="Compare paired JSONL evaluation records")
    evaluate_sub = evaluate.add_subparsers(dest="eval_command", required=True)
    compare = evaluate_sub.add_parser("compare")
    compare.add_argument("baseline")
    compare.add_argument("candidate")
    compare.add_argument("--output")

    adapter = sub.add_parser("adapter", help="Render or parse live harness commands")
    adapter_sub = adapter.add_subparsers(dest="adapter_command", required=True)
    render = adapter_sub.add_parser("render")
    render.add_argument("name", choices=["claude-code", "codex", "gemini"])
    render.add_argument("prompt")
    render.add_argument("--schema")
    render.add_argument("--model")
    run = adapter_sub.add_parser("run", help="Execute one live harness command explicitly")
    run.add_argument("name", choices=["claude-code", "codex", "gemini"])
    run.add_argument("prompt")
    run.add_argument("--schema")
    run.add_argument("--model")
    run.add_argument("--timeout-seconds", type=float, default=120.0)
    run.add_argument("--cwd")
    run.add_argument("--output-dir", required=True)
    run.add_argument(
        "--execute",
        action="store_true",
        help="Required acknowledgement that this starts a live external process",
    )
    parse = adapter_sub.add_parser("parse")
    parse.add_argument("name", choices=["claude-code", "codex", "gemini"])
    parse.add_argument("file")

    diagrams = sub.add_parser("diagrams", help="Build or check deterministic SVG diagrams")
    diagrams_sub = diagrams.add_subparsers(dest="diagrams_command", required=True)
    diagrams_build = diagrams_sub.add_parser("build")
    diagrams_build.add_argument("--root", default=".")
    diagrams_check = diagrams_sub.add_parser("check")
    diagrams_check.add_argument("--root", default=".")

    okf = sub.add_parser("okf", help="Export optional machine-readable knowledge")
    okf_sub = okf.add_subparsers(dest="okf_command", required=True)
    okf_export = okf_sub.add_parser("export")
    okf_export.add_argument("--root", default=".")
    okf_export.add_argument("--output", default="dist/knowledge.json")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "check":
        report = validate_repository(_root(args.root))
        print(stable_json(report) if args.json else findings_as_text(report))
        return 0 if report["ok"] else 1

    if args.command == "check-skills":
        root = _root(args.root)
        findings = []
        for skill_file in sorted(root.rglob("SKILL.md")):
            if ".git" not in skill_file.parts:
                findings.extend(validate_skill(skill_file.parent, root))
        report = {
            "ok": not any(item.level == "error" for item in findings),
            "findings": [item.to_dict() for item in findings],
        }
        print(stable_json(report))
        return 0 if report["ok"] else 1

    if args.command == "lab":
        labs_root = _root(args.root) / "labs"
        results = (
            run_all_labs(labs_root, write=args.write)
            if args.name == "all"
            else [run_lab(labs_root, args.name, write=args.write)]
        )
        drift = [path for result in results for path in result["drift"]]
        summary = {
            "labs": [result["lab"] for result in results],
            "write": args.write,
            "drift": drift,
            "ok": not drift,
        }
        print(stable_json(summary))
        return 0 if not drift else 1

    if args.command == "eval":
        result = compare_records(_records(Path(args.baseline)), _records(Path(args.candidate)))
        if args.output:
            write_json(Path(args.output), result)
        print(stable_json(result))
        return 0

    if args.command == "adapter":
        model = getattr(args, "model", None)
        harness = _adapter(args.name, model=model)
        if args.adapter_command == "render":
            schema = Path(args.schema) if args.schema else None
            plan = harness.build(args.prompt, schema_path=schema)
            print(stable_json({**plan.to_dict(), "shell_preview": shlex.join(plan.argv)}))
            return 0
        if args.adapter_command == "run":
            if not args.execute:
                print(
                    stable_json(
                        {
                            "ok": False,
                            "error": "refusing live execution without --execute",
                        }
                    ),
                    file=sys.stderr,
                )
                return 2
            record = run_adapter(
                harness,
                args.prompt,
                schema_path=Path(args.schema) if args.schema else None,
                timeout_seconds=args.timeout_seconds,
                cwd=Path(args.cwd).resolve() if args.cwd else None,
                output_dir=Path(args.output_dir).resolve(),
            )
            print(stable_json(record.to_dict()))
            return 0 if record.success else 1
        adapter_result = harness.parse(Path(args.file).read_text(encoding="utf-8"))
        print(stable_json(adapter_result.to_dict()))
        return 0 if adapter_result.success else 1

    if args.command == "diagrams":
        root = _root(args.root)
        if args.diagrams_command == "build":
            names = sorted(build_diagrams(root / "diagrams"))
            print(json.dumps({"built": names}, indent=2))
            return 0
        drift = check_diagrams(root / "diagrams")
        print(json.dumps({"drift": drift, "ok": not drift}, indent=2))
        return 0 if not drift else 1

    if args.command == "okf":
        root = _root(args.root)
        payload = export_knowledge(root, root / args.output)
        print(json.dumps({"records": len(payload["records"]), "output": args.output}, indent=2))
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
