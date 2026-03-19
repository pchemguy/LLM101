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
- render-report: convert an audit JSON report into a readable Markdown report
- render-comparison: convert a comparison JSON report into Markdown
- pack-prompts: generate a single Markdown bundle with prompt + standard + taxonomy
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

DEFAULT_EVALUATION_STANDARD = """# Standard for LLM-Based Evaluation of Dissertation Introductions

См. repo starter kit: этот файл должен содержать ваш нормативный стандарт.
"""

DEFAULT_DEFECT_TAXONOMY = """# Defect Taxonomy / Codebook for Dissertation Introductions

См. repo starter kit: этот файл должен содержать классификатор дефектов.
"""

DEFAULT_AUDIT_PROMPT = """# Audit Prompt

См. repo starter kit: этот файл должен содержать основной prompt для аудита.
"""

DEFAULT_LINT_PROMPT = """# Lint Prompt

См. repo starter kit: этот файл должен содержать быстрый lint prompt.
"""

DEFAULT_REPAIR_PROMPT = """# Repair Prompt

См. repo starter kit: этот файл должен содержать prompt для targeted repair.
"""

DEFAULT_COMPARE_PROMPT = """# Compare Prompt

См. repo starter kit: этот файл должен содержать prompt для comparison mode.
"""

DEFAULT_README = """# Dissertation Introduction QA CLI Starter

This starter provides a lightweight local CLI for the dissertation introduction
QA workflow.

Supported commands:
- intro-qa init
- intro-qa scaffold-report
- intro-qa scaffold-comparison
- intro-qa compare
- intro-qa gate
- intro-qa render-report
- intro-qa render-comparison
- intro-qa pack-prompts
"""


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def _write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


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
            raise YamlSubsetError("Invalid indentation structure.")
        parent = stack[-1][1]

        if stripped.startswith("- "):
            item_value = _parse_scalar(stripped[2:])
            if not isinstance(parent, list):
                raise YamlSubsetError("List item found without list parent.")
            parent.append(item_value)
            continue

        if ":" not in stripped:
            raise YamlSubsetError(f"Unsupported YAML line: {line}")

        key, value = stripped.split(":", 1)
        key = key.strip()
        value = value.strip()

        if value:
            if not isinstance(parent, dict):
                raise YamlSubsetError("Key-value found without dict parent.")
            parent[key] = _parse_scalar(value)
            continue

        # Look ahead to determine whether nested structure is dict or list.
        nested: Any = {}
        j = i
        while j < len(lines):
            probe = lines[j]
            if not probe.strip() or probe.lstrip().startswith("#"):
                j += 1
                continue
            probe_indent = len(probe) - len(probe.lstrip(" "))
            probe_stripped = probe.strip()
            if probe_indent <= indent:
                nested = {}
                break
            nested = [] if probe_stripped.startswith("- ") else {}
            break

        if not isinstance(parent, dict):
            raise YamlSubsetError("Nested key found without dict parent.")
        parent[key] = nested
        stack.append((indent, nested))

    return root


def _load_profiles(path: Path) -> dict[str, Any]:
    data = _parse_simple_yaml(path.read_text(encoding="utf-8"))
    profiles = data.get("profiles")
    if not isinstance(profiles, dict):
        raise YamlSubsetError("Top-level 'profiles' mapping is required.")
    return profiles


def _compute_score_diff(old_scores: dict[str, Any], new_scores: dict[str, Any]) -> dict[str, float]:
    keys = sorted(set(old_scores) | set(new_scores))
    diff: dict[str, float] = {}
    for key in keys:
        old = float(old_scores.get(key, 0))
        new = float(new_scores.get(key, 0))
        delta = new - old
        if delta != 0:
            diff[key] = delta
    return diff


def _defect_code_set(report: dict[str, Any]) -> set[str]:
    return {str(item.get("code", "")).strip() for item in report.get("defects", []) if item.get("code")}


def _compare_reports(old_report: dict[str, Any], new_report: dict[str, Any]) -> dict[str, Any]:
    old_codes = _defect_code_set(old_report)
    new_codes = _defect_code_set(new_report)
    score_diff = _compute_score_diff(old_report.get("scores", {}), new_report.get("scores", {}))

    regression_warnings: list[str] = []
    critical_old = int(old_report.get("summary", {}).get("critical_count", 0))
    critical_new = int(new_report.get("summary", {}).get("critical_count", 0))
    major_old = int(old_report.get("summary", {}).get("major_count", 0))
    major_new = int(new_report.get("summary", {}).get("major_count", 0))

    if critical_new > critical_old:
        regression_warnings.append(
            "Количество critical defects увеличилось. Это сильная регрессия."
        )
    if major_new > major_old:
        regression_warnings.append(
            "Количество major defects увеличилось. Проверьте, не сломала ли правка логику текста."
        )
    if float(new_report.get("scores", {}).get("NV", 0)) < float(old_report.get("scores", {}).get("NV", 0)):
        regression_warnings.append(
            "Снизилась оценка научной новизны. Возможно, правка ослабила формулировку вклада."
        )
    if float(new_report.get("scores", {}).get("LC2", 0)) < float(old_report.get("scores", {}).get("LC2", 0)):
        regression_warnings.append(
            "Снизилась связка gap → goal. Возможно, цель хуже соотносится с выявленным пробелом."
        )

    return {
        "from_version": old_report.get("metadata", {}).get("document_id", "old"),
        "to_version": new_report.get("metadata", {}).get("document_id", "new"),
        "resolved_defects": sorted(old_codes - new_codes),
        "remaining_defects": sorted(old_codes & new_codes),
        "new_defects": sorted(new_codes - old_codes),
        "score_diff": score_diff,
        "regression_warnings": regression_warnings,
        "overall_assessment": "",
    }


def _run_gate(report: dict[str, Any], profile_name: str, profiles: dict[str, Any]) -> GateResult:
    if profile_name not in profiles:
        raise KeyError(f"Profile '{profile_name}' not found.")

    profile = profiles[profile_name]
    summary = report.get("summary", {})
    scores = report.get("scores", {})
    gost = report.get("gost_compliance", {})

    failures: list[str] = []

    max_critical = int(profile.get("max_critical", 999999))
    max_major = int(profile.get("max_major", 999999))

    critical_count = int(summary.get("critical_count", 0))
    major_count = int(summary.get("major_count", 0))

    if critical_count > max_critical:
        failures.append(
            f"critical_count={critical_count} exceeds max_critical={max_critical}"
        )
    if major_count > max_major:
        failures.append(f"major_count={major_count} exceeds max_major={max_major}")

    min_scores = profile.get("min_scores", {})
    if isinstance(min_scores, dict):
        for key, expected in min_scores.items():
            actual = float(scores.get(key, 0))
            expected_value = float(expected)
            if actual < expected_value:
                failures.append(f"score[{key}]={actual} is below required {expected_value}")

    required_gost = profile.get("require_gost", [])
    if isinstance(required_gost, list):
        for field in required_gost:
            if not bool(gost.get(field, False)):
                failures.append(f"gost[{field}] is required but false")

    return GateResult(
        passed=not failures,
        failures=failures,
        profile_name=profile_name,
    )


def _markdown_escape(text: str) -> str:
    return text.replace("\n", " ").strip()


def _format_extraction_value(value: Any) -> str:
    if isinstance(value, dict):
        text = str(value.get("text", "")).strip()
        status = str(value.get("status", "")).strip()
        if not text and status:
            return f"*status:* `{status}`"
        if status:
            return f"*status:* `{status}`; {text}"
        return text or "—"
    if isinstance(value, list):
        if not value:
            return "—"
        return "\n".join(f"- {_markdown_escape(str(item))}" for item in value)
    return str(value).strip() or "—"


def _render_audit_report_markdown(report: dict[str, Any]) -> str:
    md = []
    meta = report.get("metadata", {})
    summary = report.get("summary", {})
    md.append(f"# Audit Report: {meta.get('document_id', 'unknown')}\n")
    md.append("## Metadata\n")
    md.append(f"- Language: {meta.get('language', '')}")
    md.append(f"- Audit mode: {meta.get('audit_mode', '')}")
    md.append(f"- Date: {meta.get('date', '')}\n")

    md.append("## Normalized Extraction\n")
    extraction = report.get("extraction", {})
    for key, value in extraction.items():
        md.append(f"### {key}")
        md.append(_format_extraction_value(value))
        md.append("")

    md.append("## Criterion Scores\n")
    scores = report.get("scores", {})
    for key in sorted(scores):
        md.append(f"- **{key}**: {scores[key]}")
    md.append("")

    md.append("## GOST Compliance\n")
    gost = report.get("gost_compliance", {})
    for key in sorted(gost):
        md.append(f"- **{key}**: {'yes' if gost[key] else 'no'}")
    md.append("")

    defects = report.get("defects", [])
    severity_order = ["critical", "major", "moderate", "minor"]
    md.append("## Defects by Severity\n")
    for severity in severity_order:
        subset = [d for d in defects if str(d.get("severity", "")).lower() == severity]
        md.append(f"### {severity.title()}")
        if not subset:
            md.append("- None")
            md.append("")
            continue
        for idx, defect in enumerate(subset, start=1):
            md.append(
                f"{idx}. **{defect.get('code', '')}** — {defect.get('description', '').strip() or 'No description.'}"
            )
            if defect.get("section"):
                md.append(f"   - Section: {defect.get('section')}")
            if defect.get("evidence"):
                md.append(f"   - Evidence: {defect.get('evidence')}")
            if defect.get("recommendation"):
                md.append(f"   - Recommendation: {defect.get('recommendation')}")
        md.append("")

    md.append("## Summary\n")
    md.append(f"- Critical defects: {summary.get('critical_count', 0)}")
    md.append(f"- Major defects: {summary.get('major_count', 0)}")
    md.append(f"- Moderate defects: {summary.get('moderate_count', 0)}")
    md.append(f"- Minor defects: {summary.get('minor_count', 0)}")
    md.append(
        f"- Logical integrity score: {summary.get('logical_integrity_score', 0)}"
    )
    md.append(f"- Overall verdict: {summary.get('overall_verdict', '')}")
    md.append("")
    return "\n".join(md).strip() + "\n"


def _render_comparison_markdown(report: dict[str, Any]) -> str:
    md = []
    md.append(
        f"# Comparison Report: {report.get('from_version', 'old')} → {report.get('to_version', 'new')}\n"
    )
    for title, key in [
        ("Resolved Defects", "resolved_defects"),
        ("Remaining Defects", "remaining_defects"),
        ("New Defects", "new_defects"),
    ]:
        md.append(f"## {title}\n")
        items = report.get(key, [])
        if not items:
            md.append("- None\n")
            continue
        for item in items:
            md.append(f"- {item}")
        md.append("")

    md.append("## Score Delta\n")
    score_diff = report.get("score_diff", {})
    if not score_diff:
        md.append("- No score changes\n")
    else:
        for key in sorted(score_diff):
            delta = score_diff[key]
            sign = "+" if float(delta) > 0 else ""
            md.append(f"- **{key}**: {sign}{delta}")
        md.append("")

    md.append("## Regression Warnings\n")
    warnings = report.get("regression_warnings", [])
    if not warnings:
        md.append("- None\n")
    else:
        for item in warnings:
            md.append(f"- {item}")
        md.append("")

    md.append("## Overall Assessment\n")
    md.append(report.get("overall_assessment", ""))
    md.append("")
    return "\n".join(md).strip() + "\n"


def _pack_prompts(prompt: Path, standard: Path, taxonomy: Path, intro: Path) -> str:
    parts = [
        ("PROMPT", prompt.read_text(encoding="utf-8")),
        ("EVALUATION STANDARD", standard.read_text(encoding="utf-8")),
        ("DEFECT TAXONOMY", taxonomy.read_text(encoding="utf-8")),
        ("TEXT TO EVALUATE", intro.read_text(encoding="utf-8")),
    ]
    lines: list[str] = []
    for title, body in parts:
        lines.append(f"# {title}\n")
        lines.append(body.strip())
        lines.append("\n")
    return "\n".join(lines).rstrip() + "\n"


def cmd_init(args: argparse.Namespace) -> int:
    root = Path(args.path)
    directories = [
        root / "standards",
        root / "prompts",
        root / "configs",
        root / "schemas",
        root / "inputs",
        root / "reports",
        root / "comparisons",
        root / "repair",
    ]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

    _write_text(root / "README.md", DEFAULT_README)
    _write_text(root / "standards" / "evaluation_standard.md", DEFAULT_EVALUATION_STANDARD)
    _write_text(root / "standards" / "defect_taxonomy.md", DEFAULT_DEFECT_TAXONOMY)
    _write_text(root / "prompts" / "audit_prompt.md", DEFAULT_AUDIT_PROMPT)
    _write_text(root / "prompts" / "lint_prompt.md", DEFAULT_LINT_PROMPT)
    _write_text(root / "prompts" / "repair_prompt.md", DEFAULT_REPAIR_PROMPT)
    _write_text(root / "prompts" / "compare_prompt.md", DEFAULT_COMPARE_PROMPT)
    _write_text(root / "configs" / "acceptance_profiles.yaml", DEFAULT_ACCEPTANCE_PROFILES)
    _write_json(root / "reports" / "audit_report_template.json", deepcopy(DEFAULT_AUDIT_REPORT))
    _write_json(
        root / "comparisons" / "comparison_report_template.json",
        deepcopy(DEFAULT_COMPARISON_REPORT),
    )

    print(f"Initialized dissertation intro QA starter at: {root}")
    return 0


def cmd_scaffold_report(args: argparse.Namespace) -> int:
    payload = deepcopy(DEFAULT_AUDIT_REPORT)
    payload["metadata"]["document_id"] = args.document_id
    if args.date:
        payload["metadata"]["date"] = args.date
    _write_json(Path(args.out), payload)
    print(f"Wrote audit report scaffold: {args.out}")
    return 0


def cmd_scaffold_comparison(args: argparse.Namespace) -> int:
    payload = deepcopy(DEFAULT_COMPARISON_REPORT)
    payload["from_version"] = args.from_version
    payload["to_version"] = args.to_version
    _write_json(Path(args.out), payload)
    print(f"Wrote comparison report scaffold: {args.out}")
    return 0


def cmd_compare(args: argparse.Namespace) -> int:
    old_report = _read_json(Path(args.old_report))
    new_report = _read_json(Path(args.new_report))
    comparison = _compare_reports(old_report, new_report)
    _write_json(Path(args.out), comparison)
    print(f"Wrote comparison report: {args.out}")
    if args.report_md:
        _write_text(Path(args.report_md), _render_comparison_markdown(comparison))
        print(f"Wrote Markdown comparison report: {args.report_md}")
    return 0


def cmd_gate(args: argparse.Namespace) -> int:
    report = _read_json(Path(args.report))
    profiles = _load_profiles(Path(args.profiles))
    result = _run_gate(report, args.profile, profiles)
    payload = {
        "profile": result.profile_name,
        "passed": result.passed,
        "failures": result.failures,
    }
    if args.out:
        _write_json(Path(args.out), payload)
        print(f"Wrote gate result: {args.out}")
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    return 0 if result.passed else 2


def cmd_render_report(args: argparse.Namespace) -> int:
    report = _read_json(Path(args.report))
    rendered = _render_audit_report_markdown(report)
    _write_text(Path(args.out), rendered)
    print(f"Wrote Markdown audit report: {args.out}")
    return 0


def cmd_render_comparison(args: argparse.Namespace) -> int:
    report = _read_json(Path(args.report))
    rendered = _render_comparison_markdown(report)
    _write_text(Path(args.out), rendered)
    print(f"Wrote Markdown comparison report: {args.out}")
    return 0


def cmd_pack_prompts(args: argparse.Namespace) -> int:
    bundled = _pack_prompts(
        Path(args.prompt), Path(args.standard), Path(args.taxonomy), Path(args.intro)
    )
    _write_text(Path(args.out), bundled)
    print(f"Wrote LLM input bundle: {args.out}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="intro-qa",
        description="CLI starter for dissertation introduction QA workflows.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser("init", help="Initialize a starter repo structure.")
    init_parser.add_argument("path", help="Target directory for the starter repo.")
    init_parser.set_defaults(func=cmd_init)

    scaffold_report = subparsers.add_parser(
        "scaffold-report", help="Write a blank audit report JSON scaffold."
    )
    scaffold_report.add_argument("--out", required=True, help="Output JSON path.")
    scaffold_report.add_argument(
        "--document-id", default="intro_v1", help="Document identifier."
    )
    scaffold_report.add_argument("--date", default=None, help="Optional date string.")
    scaffold_report.set_defaults(func=cmd_scaffold_report)

    scaffold_comparison = subparsers.add_parser(
        "scaffold-comparison", help="Write a blank comparison report JSON scaffold."
    )
    scaffold_comparison.add_argument("--out", required=True, help="Output JSON path.")
    scaffold_comparison.add_argument(
        "--from-version", default="intro_v1", help="Source version identifier."
    )
    scaffold_comparison.add_argument(
        "--to-version", default="intro_v2", help="Target version identifier."
    )
    scaffold_comparison.set_defaults(func=cmd_scaffold_comparison)

    compare_parser = subparsers.add_parser(
        "compare", help="Compare two audit JSON reports."
    )
    compare_parser.add_argument("old_report", help="Path to the older audit JSON report.")
    compare_parser.add_argument("new_report", help="Path to the newer audit JSON report.")
    compare_parser.add_argument("--out", required=True, help="Output comparison JSON path.")
    compare_parser.add_argument(
        "--report-md", default=None, help="Optional Markdown report output path."
    )
    compare_parser.set_defaults(func=cmd_compare)

    gate_parser = subparsers.add_parser(
        "gate", help="Check an audit report against an acceptance profile."
    )
    gate_parser.add_argument("report", help="Path to the audit JSON report.")
    gate_parser.add_argument(
        "--profiles", required=True, help="Path to the acceptance profile YAML file."
    )
    gate_parser.add_argument(
        "--profile", required=True, help="Profile name to validate against."
    )
    gate_parser.add_argument(
        "--out", default=None, help="Optional output JSON file for gate results."
    )
    gate_parser.set_defaults(func=cmd_gate)

    render_report_parser = subparsers.add_parser(
        "render-report", help="Render an audit JSON report to Markdown."
    )
    render_report_parser.add_argument("report", help="Path to audit JSON report.")
    render_report_parser.add_argument("--out", required=True, help="Output Markdown path.")
    render_report_parser.set_defaults(func=cmd_render_report)

    render_comparison_parser = subparsers.add_parser(
        "render-comparison", help="Render a comparison JSON report to Markdown."
    )
    render_comparison_parser.add_argument("report", help="Path to comparison JSON report.")
    render_comparison_parser.add_argument(
        "--out", required=True, help="Output Markdown path."
    )
    render_comparison_parser.set_defaults(func=cmd_render_comparison)

    pack_parser = subparsers.add_parser(
        "pack-prompts",
        help="Bundle prompt + standard + taxonomy + intro text into one Markdown file.",
    )
    pack_parser.add_argument("--prompt", required=True, help="Prompt Markdown path.")
    pack_parser.add_argument("--standard", required=True, help="Evaluation standard path.")
    pack_parser.add_argument("--taxonomy", required=True, help="Defect taxonomy path.")
    pack_parser.add_argument("--intro", required=True, help="Introduction text path.")
    pack_parser.add_argument("--out", required=True, help="Output bundle Markdown path.")
    pack_parser.set_defaults(func=cmd_pack_prompts)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except FileNotFoundError as exc:
        print(f"File not found: {exc}", file=sys.stderr)
        return 1
    except KeyError as exc:
        print(str(exc), file=sys.stderr)
        return 1
    except YamlSubsetError as exc:
        print(f"YAML parse error: {exc}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print(f"JSON parse error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
