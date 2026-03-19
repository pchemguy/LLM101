#!/usr/bin/env python3
"""CLI starter for dissertation introduction QA workflows.

This tool does not run an LLM by itself. Instead, it provides the local
scaffolding needed to support a structured QA pipeline around LLM-generated
reports.

Main capabilities:
- init: create a repo-ready starter kit structure
- compare: compare two audit JSON reports
- gate: validate an audit JSON report against an acceptance profile YAML
- scaffold-report: generate a blank audit report JSON skeleton
- scaffold-comparison: generate a blank comparison JSON skeleton
"""

from __future__ import annotations

import argparse
import json
import sys
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path
from typing import Any


DEFAULT_ACCEPTANCE_PROFILES = """profiles:
  draft:
    max_critical: 99
    max_major: 99

  supervisor:
    max_critical: 0
    max_major: 5
    require_gost:
      - relevance
      - degree_of_development
      - goals_tasks
      - novelty
      - methods

  pre_defense:
    max_critical: 0
    max_major: 2
    min_scores:
      LC1: 2
      LC2: 2
      LC3: 2
      LC4: 2
      LC5: 2
      LC6: 2
      NV: 2
      VAL: 1
    require_gost:
      - relevance
      - degree_of_development
      - goals_tasks
      - novelty
      - significance
      - methods
      - defense_propositions
      - reliability
      - approbation

  strict:
    max_critical: 0
    max_major: 1
    min_scores:
      SC1: 3
      SC2: 2
      LC1: 2
      LC2: 2
      LC3: 2
      LC4: 2
      LC5: 2
      LC6: 2
      NV: 2
      VAL: 2
"""

DEFAULT_AUDIT_REPORT = {
    "metadata": {
        "document_id": "intro_v1",
        "language": "ru",
        "audit_mode": "full",
        "date": "YYYY-MM-DD",
    },
    "extraction": {
        "problem_context": {"text": "", "status": "absent"},
        "knowledge_state": {"text": "", "status": "absent"},
        "research_gap": {"text": "", "status": "absent"},
        "goal": {"text": "", "status": "absent"},
        "tasks": [],
        "object": {"text": "", "status": "absent"},
        "subject": {"text": "", "status": "absent"},
        "methodology": "",
        "methods": [],
        "database": "",
        "scientific_novelty": [],
        "propositions_for_defense": [],
        "theoretical_significance": "",
        "practical_significance": "",
        "reliability": "",
        "approbation": "",
        "publications": "",
        "dissertation_structure": "",
    },
    "scores": {
        "SC1": 0,
        "SC2": 0,
        "LC1": 0,
        "LC2": 0,
        "LC3": 0,
        "LC4": 0,
        "LC5": 0,
        "LC6": 0,
        "NV": 0,
        "VAL": 0,
    },
    "defects": [],
    "gost_compliance": {
        "relevance": False,
        "degree_of_development": False,
        "goals_tasks": False,
        "novelty": False,
        "significance": False,
        "methods": False,
        "defense_propositions": False,
        "reliability": False,
        "approbation": False,
    },
    "summary": {
        "critical_count": 0,
        "major_count": 0,
        "moderate_count": 0,
        "minor_count": 0,
        "logical_integrity_score": 0.0,
        "overall_verdict": "",
    },
}

DEFAULT_COMPARISON_REPORT = {
    "from_version": "intro_v1",
    "to_version": "intro_v2",
    "resolved_defects": [],
    "remaining_defects": [],
    "new_defects": [],
    "score_diff": {},
    "regression_warnings": [],
    "overall_assessment": "",
}

DEFAULT_README = """# Dissertation Introduction QA CLI Starter

This starter provides a lightweight local CLI for the dissertation introduction
QA workflow.

Supported commands:
- intro-qa init
- intro-qa scaffold-report
- intro-qa scaffold-comparison
- intro-qa compare
- intro-qa gate

The CLI does not call an LLM directly. Instead, it helps you manage:
- project scaffolding
- audit reports
- comparison reports
- acceptance gate checks
"""


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _parse_scalar(raw: str) -> Any:
    raw = raw.strip()
    if raw.lower() == "true":
        return True
    if raw.lower() == "false":
        return False
    try:
        if "." in raw:
            return float(raw)
        return int(raw)
    except ValueError:
        return raw


@dataclass
class GateResult:
    passed: bool
    failures: list[str]
    profile_name: str


class YamlSubsetError(RuntimeError):
    """Raised when the minimal YAML subset parser cannot parse the file."""


# This parser intentionally supports only the limited YAML shapes used by the
# acceptance profile file in this starter. It avoids external dependencies.
def _parse_simple_yaml(text: str) -> dict[str, Any]:
    root: dict[str, Any] = {}
    stack: list[tuple[int, Any]] = [(-1, root)]

    lines = text.splitlines()
    i = 0
    while i < len(lines):
        line = lines[i]
        i += 1
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        indent = len(line) - len(line.lstrip(" "))
        stripped = line.strip()

        while stack and indent <= stack[-1][0]:
            stack.pop()
        if not stack:
            raise YamlSubsetError("Invalid indentation structure in YAML file.")
        container = stack[-1][1]

        if stripped.startswith("- "):
            if not isinstance(container, list):
                raise YamlSubsetError("List item found outside list context.")
            container.append(_parse_scalar(stripped[2:]))
            continue

        if ":" not in stripped:
            raise YamlSubsetError(f"Unsupported YAML line: {stripped}")

        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()

        if value:
            if not isinstance(container, dict):
                raise YamlSubsetError("Key-value pair found outside dict context.")
            container[key] = _parse_scalar(value)
            continue

        # Need to infer dict or list by looking ahead to the next significant line.
        next_significant = None
        for j in range(i, len(lines)):
            candidate = lines[j]
            if candidate.strip() and not candidate.lstrip().startswith("#"):
                next_significant = candidate
                break

        if next_significant is None:
            inferred: Any = {}
        else:
            next_indent = len(next_significant) - len(next_significant.lstrip(" "))
            next_stripped = next_significant.strip()
            if next_indent <= indent:
                inferred = {}
            elif next_stripped.startswith("- "):
                inferred = []
            else:
                inferred = {}

        if not isinstance(container, dict):
            raise YamlSubsetError("Nested mapping found outside dict context.")
        container[key] = inferred
        stack.append((indent, inferred))

    return root


def _load_profiles(path: Path) -> dict[str, Any]:
    parsed = _parse_simple_yaml(path.read_text(encoding="utf-8"))
    profiles = parsed.get("profiles")
    if not isinstance(profiles, dict):
        raise YamlSubsetError("Top-level 'profiles' mapping not found.")
    return profiles


def _compute_score_diff(
    old_scores: dict[str, Any], new_scores: dict[str, Any]
) -> dict[str, float]:
    keys = set(old_scores) | set(new_scores)
    diff: dict[str, float] = {}
    for key in sorted(keys):
        old_value = float(old_scores.get(key, 0))
        new_value = float(new_scores.get(key, 0))
        diff[key] = new_value - old_value
    return diff


def _comparison_assessment(payload: dict[str, Any]) -> str:
    resolved = len(payload["resolved_defects"])
    new = len(payload["new_defects"])
    regressions = len(payload["regression_warnings"])
    if new == 0 and regressions == 0 and resolved > 0:
        return "Новая версия улучшена без очевидных регрессий."
    if new > 0 or regressions > 0:
        return (
            "Новая версия улучшена частично: часть дефектов устранена, но есть новые "
            "риски или регрессии."
        )
    return "Существенных изменений по набору дефектов не выявлено."


def compare_reports(old_report: dict[str, Any], new_report: dict[str, Any]) -> dict[str, Any]:
    old_codes = {item["code"] for item in old_report.get("defects", []) if "code" in item}
    new_codes = {item["code"] for item in new_report.get("defects", []) if "code" in item}

    resolved = sorted(old_codes - new_codes)
    remaining = sorted(old_codes & new_codes)
    new = sorted(new_codes - old_codes)

    old_summary = old_report.get("summary", {})
    new_summary = new_report.get("summary", {})
    warnings: list[str] = []

    if new_summary.get("critical_count", 0) > old_summary.get("critical_count", 0):
        warnings.append("Увеличилось количество critical defects.")
    if new_summary.get("major_count", 0) > old_summary.get("major_count", 0):
        warnings.append("Увеличилось количество major defects.")

    score_diff = _compute_score_diff(
        old_report.get("scores", {}), new_report.get("scores", {})
    )
    for score_name, delta in score_diff.items():
        if delta < 0:
            warnings.append(f"Снизился score {score_name}: {delta}.")

    payload = deepcopy(DEFAULT_COMPARISON_REPORT)
    payload["from_version"] = old_report.get("metadata", {}).get("document_id", "old")
    payload["to_version"] = new_report.get("metadata", {}).get("document_id", "new")
    payload["resolved_defects"] = resolved
    payload["remaining_defects"] = remaining
    payload["new_defects"] = new
    payload["score_diff"] = score_diff
    payload["regression_warnings"] = warnings
    payload["overall_assessment"] = _comparison_assessment(payload)
    return payload


def check_gate(report: dict[str, Any], profiles: dict[str, Any], profile_name: str) -> GateResult:
    if profile_name not in profiles:
        available = ", ".join(sorted(profiles))
        raise KeyError(f"Unknown profile '{profile_name}'. Available profiles: {available}")

    profile = profiles[profile_name]
    failures: list[str] = []
    summary = report.get("summary", {})
    scores = report.get("scores", {})
    gost = report.get("gost_compliance", {})

    max_critical = int(profile.get("max_critical", 999))
    max_major = int(profile.get("max_major", 999))

    critical_count = int(summary.get("critical_count", 0))
    major_count = int(summary.get("major_count", 0))

    if critical_count > max_critical:
        failures.append(
            f"Critical defects exceed threshold: {critical_count} > {max_critical}."
        )
    if major_count > max_major:
        failures.append(f"Major defects exceed threshold: {major_count} > {max_major}.")

    min_scores = profile.get("min_scores", {})
    if isinstance(min_scores, dict):
        for name, expected in min_scores.items():
            actual = scores.get(name)
            if actual is None:
                failures.append(f"Missing score '{name}' required by profile.")
                continue
            if float(actual) < float(expected):
                failures.append(f"Score {name} below threshold: {actual} < {expected}.")

    require_gost = profile.get("require_gost", [])
    if isinstance(require_gost, list):
        for key in require_gost:
            if gost.get(str(key)) is not True:
                failures.append(f"Required GOST component not satisfied: {key}.")

    return GateResult(passed=not failures, failures=failures, profile_name=profile_name)


def _make_repo_tree(base_dir: Path) -> None:
    dirs = [
        base_dir / "standards",
        base_dir / "prompts",
        base_dir / "configs",
        base_dir / "schemas",
        base_dir / "inputs",
        base_dir / "reports",
        base_dir / "comparisons",
        base_dir / "repair",
    ]
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)

    (base_dir / "README.md").write_text(DEFAULT_README, encoding="utf-8")
    (base_dir / "configs" / "acceptance_profiles.yaml").write_text(
        DEFAULT_ACCEPTANCE_PROFILES,
        encoding="utf-8",
    )
    _write_json(base_dir / "schemas" / "audit_report_schema.example.json", DEFAULT_AUDIT_REPORT)
    _write_json(
        base_dir / "schemas" / "comparison_report_schema.example.json",
        DEFAULT_COMPARISON_REPORT,
    )
    _write_json(base_dir / "reports" / "audit_report_template.json", DEFAULT_AUDIT_REPORT)
    _write_json(
        base_dir / "comparisons" / "comparison_report_template.json",
        DEFAULT_COMPARISON_REPORT,
    )
    (base_dir / "inputs" / "intro_example.md").write_text(
        "# Intro Example\n\nПоместите сюда текст введения для анализа.\n",
        encoding="utf-8",
    )


def cmd_init(args: argparse.Namespace) -> int:
    target = Path(args.path).resolve()
    target.mkdir(parents=True, exist_ok=True)
    _make_repo_tree(target)
    print(f"Initialized dissertation intro QA scaffold at: {target}")
    return 0


def cmd_scaffold_report(args: argparse.Namespace) -> int:
    payload = deepcopy(DEFAULT_AUDIT_REPORT)
    if args.document_id:
        payload["metadata"]["document_id"] = args.document_id
    if args.date:
        payload["metadata"]["date"] = args.date
    _write_json(Path(args.out), payload)
    print(f"Wrote audit report scaffold: {args.out}")
    return 0


def cmd_scaffold_comparison(args: argparse.Namespace) -> int:
    payload = deepcopy(DEFAULT_COMPARISON_REPORT)
    if args.from_version:
        payload["from_version"] = args.from_version
    if args.to_version:
        payload["to_version"] = args.to_version
    _write_json(Path(args.out), payload)
    print(f"Wrote comparison scaffold: {args.out}")
    return 0


def cmd_compare(args: argparse.Namespace) -> int:
    old_report = _read_json(Path(args.old_report))
    new_report = _read_json(Path(args.new_report))
    payload = compare_reports(old_report, new_report)
    _write_json(Path(args.out), payload)
    print(f"Wrote comparison report: {args.out}")
    return 0


def cmd_gate(args: argparse.Namespace) -> int:
    report = _read_json(Path(args.report))
    profiles = _load_profiles(Path(args.profiles))
    result = check_gate(report, profiles, args.profile)

    output = {
        "profile": result.profile_name,
        "passed": result.passed,
        "failures": result.failures,
    }

    if args.out:
        _write_json(Path(args.out), output)

    print(f"Profile: {result.profile_name}")
    print(f"Passed: {result.passed}")
    if result.failures:
        print("Failures:")
        for failure in result.failures:
            print(f"- {failure}")
        return 1
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="intro-qa",
        description="CLI starter for dissertation introduction QA workflows.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Create starter repo structure.")
    init_parser.add_argument("path", help="Target directory for the scaffold.")
    init_parser.set_defaults(func=cmd_init)

    scaffold_parser = subparsers.add_parser(
        "scaffold-report",
        help="Generate an empty audit report JSON scaffold.",
    )
    scaffold_parser.add_argument("--out", required=True, help="Output JSON path.")
    scaffold_parser.add_argument("--document-id", help="Document identifier.")
    scaffold_parser.add_argument("--date", help="Audit date.")
    scaffold_parser.set_defaults(func=cmd_scaffold_report)

    scaffold_comparison = subparsers.add_parser(
        "scaffold-comparison",
        help="Generate an empty comparison report JSON scaffold.",
    )
    scaffold_comparison.add_argument("--out", required=True, help="Output JSON path.")
    scaffold_comparison.add_argument("--from-version", help="Old version label.")
    scaffold_comparison.add_argument("--to-version", help="New version label.")
    scaffold_comparison.set_defaults(func=cmd_scaffold_comparison)

    compare_parser = subparsers.add_parser(
        "compare",
        help="Compare two audit report JSON files.",
    )
    compare_parser.add_argument("old_report", help="Path to old audit JSON.")
    compare_parser.add_argument("new_report", help="Path to new audit JSON.")
    compare_parser.add_argument("--out", required=True, help="Output comparison JSON path.")
    compare_parser.set_defaults(func=cmd_compare)

    gate_parser = subparsers.add_parser(
        "gate",
        help="Check an audit report against an acceptance profile.",
    )
    gate_parser.add_argument("report", help="Path to audit JSON report.")
    gate_parser.add_argument(
        "--profiles",
        required=True,
        help="Path to acceptance_profiles.yaml.",
    )
    gate_parser.add_argument("--profile", required=True, help="Profile name to apply.")
    gate_parser.add_argument("--out", help="Optional output JSON path.")
    gate_parser.set_defaults(func=cmd_gate)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except FileNotFoundError as exc:
        print(f"File not found: {exc}", file=sys.stderr)
        return 2
    except (json.JSONDecodeError, YamlSubsetError, KeyError, ValueError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
