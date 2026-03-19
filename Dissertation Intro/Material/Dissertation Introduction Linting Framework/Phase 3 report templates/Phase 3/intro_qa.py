#!/usr/bin/env python3
"""CLI starter for dissertation introduction QA workflows.

This tool does not run an LLM by itself. Instead, it provides the local
scaffolding needed to support a structured QA pipeline around LLM-generated
reports.

Main capabilities:
- init: create a repo-ready starter kit structure
- scaffold-report: generate a blank audit report JSON skeleton
- scaffold-comparison: generate a blank comparison JSON skeleton
- compare: compare two audit JSON reports
- gate: validate an audit JSON report against an acceptance profile YAML
- render-report: render audit JSON to Markdown
- render-comparison: render comparison JSON to Markdown
- pack-prompts: assemble prompt + standard + taxonomy + intro into one bundle
- repair-plan: generate a revision plan from defect codes
- render-gate: render a gate-check JSON result to Markdown
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

Локальный CLI-каркас для QA-пайплайна введений диссертаций.

## Поддерживаемые команды

- `intro-qa init`
- `intro-qa scaffold-report`
- `intro-qa scaffold-comparison`
- `intro-qa compare`
- `intro-qa gate`
- `intro-qa render-report`
- `intro-qa render-comparison`
- `intro-qa render-gate`
- `intro-qa pack-prompts`
- `intro-qa repair-plan`

CLI сам не вызывает LLM. Он обслуживает локальный workflow вокруг LLM-аудита:

- scaffold проекта
- шаблоны JSON-отчетов
- сравнение версий
- gate checks
- рендер Markdown-отчетов
- сборка bundle для следующего прогона
- генерация repair plan по defect codes

## Быстрый старт

### 1. Инициализация структуры проекта

```bash
intro-qa init ./my_intro_qa
```

### 2. Создание шаблона audit report

```bash
intro-qa scaffold-report --out reports/audit_v1.json --document-id intro_v1
```

### 3. Проверка gate

```bash
intro-qa gate reports/audit_v1.json --profiles configs/acceptance_profiles.yaml --profile supervisor --out reports/gate_v1.json
```

### 4. Рендер audit JSON в Markdown

```bash
intro-qa render-report reports/audit_v1.json --out reports/audit_v1.md
```

### 5. Сравнение двух версий

```bash
intro-qa compare reports/audit_v1.json reports/audit_v2.json --out comparisons/v1_v2.json
intro-qa render-comparison comparisons/v1_v2.json --out comparisons/v1_v2.md
```

### 6. Сборка единого prompt bundle

```bash
intro-qa pack-prompts \
  --prompt prompts/audit_prompt.md \
  --standard standards/evaluation_standard.md \
  --taxonomy standards/defect_taxonomy.md \
  --intro inputs/intro_v2.md \
  --out bundles/audit_bundle_v2.md
```

### 7. Генерация repair plan

```bash
intro-qa repair-plan reports/audit_v2.json --out repair/repair_plan_v2.md
```
"""


SECTION_TITLES = {
    "problem_context": "ProblemContext",
    "knowledge_state": "KnowledgeState",
    "research_gap": "ResearchGap",
    "goal": "Goal",
    "tasks": "Tasks",
    "object": "Object",
    "subject": "Subject",
    "methodology": "Methodology",
    "methods": "Methods",
    "database": "DataBase",
    "scientific_novelty": "ScientificNovelty",
    "propositions_for_defense": "PropositionsForDefense",
    "theoretical_significance": "TheoreticalSignificance",
    "practical_significance": "PracticalSignificance",
    "reliability": "Reliability",
    "approbation": "Approbation",
    "publications": "Publications",
    "dissertation_structure": "DissertationStructure",
}


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
        base_dir / "bundles",
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


def _format_extraction_value(value: Any) -> str:
    if isinstance(value, dict):
        text = str(value.get("text", "")).strip()
        status = str(value.get("status", "")).strip()
        if text:
            return f"**Status:** `{status}`\n\n{text}"
        return f"**Status:** `{status}`"
    if isinstance(value, list):
        if not value:
            return "—"
        return "\n".join(f"- {item}" for item in value)
    text = str(value).strip()
    return text or "—"


def render_audit_report(report: dict[str, Any]) -> str:
    metadata = report.get("metadata", {})
    extraction = report.get("extraction", {})
    scores = report.get("scores", {})
    defects = report.get("defects", [])
    gost = report.get("gost_compliance", {})
    summary = report.get("summary", {})

    lines = [
        f"# Audit Report: {metadata.get('document_id', 'unknown')}",
        "",
        "## Metadata",
        f"- Language: {metadata.get('language', '')}",
        f"- Audit mode: {metadata.get('audit_mode', '')}",
        f"- Date: {metadata.get('date', '')}",
        "",
        "## Normalized Extraction",
    ]
    for key in SECTION_TITLES:
        lines.append(f"### {SECTION_TITLES[key]}")
        lines.append(_format_extraction_value(extraction.get(key, "")))
        lines.append("")

    lines.extend(["## GOST Compliance", ""])
    for key, value in gost.items():
        lines.append(f"- {key}: {'yes' if value else 'no'}")
    lines.append("")

    lines.extend(["## Criterion Scores", ""])
    for key, value in sorted(scores.items()):
        lines.append(f"- {key}: {value}")
    lines.append("")

    severity_order = ["critical", "major", "moderate", "minor"]
    grouped: dict[str, list[dict[str, Any]]] = {name: [] for name in severity_order}
    for defect in defects:
        severity = str(defect.get("severity", "moderate")).lower()
        grouped.setdefault(severity, []).append(defect)

    lines.append("## Defects by Severity")
    lines.append("")
    for severity in severity_order:
        lines.append(f"### {severity.title()}")
        bucket = grouped.get(severity, [])
        if not bucket:
            lines.append("- none")
            lines.append("")
            continue
        for item in bucket:
            lines.append(
                f"- **{item.get('code', 'NO-CODE')}** ({item.get('section', 'section not set')}): {item.get('description', '').strip()}"
            )
            evidence = str(item.get("evidence", "")).strip()
            if evidence:
                lines.append(f"  - Evidence: {evidence}")
            recommendation = str(item.get("recommendation", "")).strip()
            if recommendation:
                lines.append(f"  - Recommendation: {recommendation}")
        lines.append("")

    lines.extend([
        "## Summary",
        f"- Critical: {summary.get('critical_count', 0)}",
        f"- Major: {summary.get('major_count', 0)}",
        f"- Moderate: {summary.get('moderate_count', 0)}",
        f"- Minor: {summary.get('minor_count', 0)}",
        f"- Logical integrity score: {summary.get('logical_integrity_score', 0)}",
        "",
        "## Overall Verdict",
        summary.get("overall_verdict", "—") or "—",
        "",
    ])
    return "\n".join(lines)


def render_comparison_report(report: dict[str, Any]) -> str:
    lines = [
        f"# Comparison: {report.get('from_version', 'old')} → {report.get('to_version', 'new')}",
        "",
        "## Resolved Defects",
    ]
    resolved = report.get("resolved_defects", [])
    lines.extend([f"- {item}" for item in resolved] or ["- none"])
    lines.extend(["", "## Remaining Defects"])
    remaining = report.get("remaining_defects", [])
    lines.extend([f"- {item}" for item in remaining] or ["- none"])
    lines.extend(["", "## New Defects"])
    new_defects = report.get("new_defects", [])
    lines.extend([f"- {item}" for item in new_defects] or ["- none"])
    lines.extend(["", "## Score Delta"])
    score_diff = report.get("score_diff", {})
    if score_diff:
        for key, value in sorted(score_diff.items()):
            lines.append(f"- {key}: {value:+g}")
    else:
        lines.append("- none")
    lines.extend(["", "## Regression Warnings"])
    warnings = report.get("regression_warnings", [])
    lines.extend([f"- {item}" for item in warnings] or ["- none"])
    lines.extend(["", "## Overall Assessment", report.get("overall_assessment", "—") or "—", ""])
    return "\n".join(lines)


def render_gate_report(payload: dict[str, Any]) -> str:
    lines = [
        f"# Gate Check: {payload.get('profile', 'unknown')}",
        "",
        f"- Passed: {payload.get('passed', False)}",
        "",
        "## Failures",
    ]
    failures = payload.get("failures", [])
    lines.extend([f"- {item}" for item in failures] or ["- none"])
    lines.append("")
    return "\n".join(lines)


def generate_repair_plan(report: dict[str, Any]) -> str:
    defects = report.get("defects", [])
    if not defects:
        return "# Repair Plan\n\nСущественных дефектов не зафиксировано."

    grouped: dict[str, list[dict[str, Any]]] = {}
    for defect in defects:
        section = str(defect.get("section", "Unspecified section")).strip() or "Unspecified section"
        grouped.setdefault(section, []).append(defect)

    severity_rank = {"critical": 0, "major": 1, "moderate": 2, "minor": 3}
    ordered_sections = sorted(
        grouped,
        key=lambda name: min(
            severity_rank.get(str(item.get("severity", "moderate")).lower(), 99)
            for item in grouped[name]
        ),
    )

    lines = [
        "# Repair Plan",
        "",
        "## Prioritization Logic",
        "Сначала исправляются critical defects, затем major, затем moderate и minor.",
        "",
    ]
    for section in ordered_sections:
        items = sorted(
            grouped[section],
            key=lambda item: severity_rank.get(str(item.get("severity", "moderate")).lower(), 99),
        )
        lines.append(f"## {section}")
        lines.append("")
        for item in items:
            lines.append(
                f"- **{str(item.get('severity', 'moderate')).title()} / {item.get('code', 'NO-CODE')}**: {item.get('description', '').strip()}"
            )
            recommendation = str(item.get("recommendation", "")).strip()
            if recommendation:
                lines.append(f"  - Action: {recommendation}")
            evidence = str(item.get("evidence", "")).strip()
            if evidence:
                lines.append(f"  - Evidence: {evidence}")
        lines.append("")

    lines.extend([
        "## Recommended Order of Work",
        "1. Устранить все critical defects.",
        "2. Устранить разрывы исследовательской логики и major defects.",
        "3. Проверить, не породили ли правки новые LOG-* и NOV-* дефекты.",
        "4. После этого шлифовать moderate и minor issues.",
        "",
    ])
    return "\n".join(lines)


def pack_prompt_bundle(prompt: Path, standard: Path, taxonomy: Path, intro: Path) -> str:
    parts = [
        ("PROMPT", prompt.read_text(encoding="utf-8").strip()),
        ("EVALUATION STANDARD", standard.read_text(encoding="utf-8").strip()),
        ("DEFECT TAXONOMY", taxonomy.read_text(encoding="utf-8").strip()),
        ("TEXT TO EVALUATE", intro.read_text(encoding="utf-8").strip()),
    ]
    return "\n\n---\n\n".join(f"{title}\n\n{content}" for title, content in parts)


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


def cmd_render_report(args: argparse.Namespace) -> int:
    report = _read_json(Path(args.report))
    rendered = render_audit_report(report)
    _write_text(Path(args.out), rendered)
    print(f"Wrote Markdown audit report: {args.out}")
    return 0


def cmd_render_comparison(args: argparse.Namespace) -> int:
    report = _read_json(Path(args.report))
    rendered = render_comparison_report(report)
    _write_text(Path(args.out), rendered)
    print(f"Wrote Markdown comparison report: {args.out}")
    return 0


def cmd_render_gate(args: argparse.Namespace) -> int:
    payload = _read_json(Path(args.report))
    rendered = render_gate_report(payload)
    _write_text(Path(args.out), rendered)
    print(f"Wrote Markdown gate report: {args.out}")
    return 0


def cmd_pack_prompts(args: argparse.Namespace) -> int:
    bundle = pack_prompt_bundle(
        Path(args.prompt), Path(args.standard), Path(args.taxonomy), Path(args.intro)
    )
    _write_text(Path(args.out), bundle)
    print(f"Wrote prompt bundle: {args.out}")
    return 0


def cmd_repair_plan(args: argparse.Namespace) -> int:
    report = _read_json(Path(args.report))
    rendered = generate_repair_plan(report)
    _write_text(Path(args.out), rendered)
    print(f"Wrote repair plan: {args.out}")
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
    gate_parser.add_argument("--profiles", required=True, help="Path to acceptance_profiles.yaml.")
    gate_parser.add_argument("--profile", required=True, help="Profile name.")
    gate_parser.add_argument("--out", help="Optional output JSON path.")
    gate_parser.set_defaults(func=cmd_gate)

    render_report_parser = subparsers.add_parser(
        "render-report",
        help="Render audit JSON to Markdown.",
    )
    render_report_parser.add_argument("report", help="Path to audit JSON report.")
    render_report_parser.add_argument("--out", required=True, help="Output Markdown path.")
    render_report_parser.set_defaults(func=cmd_render_report)

    render_comparison_parser = subparsers.add_parser(
        "render-comparison",
        help="Render comparison JSON to Markdown.",
    )
    render_comparison_parser.add_argument("report", help="Path to comparison JSON report.")
    render_comparison_parser.add_argument("--out", required=True, help="Output Markdown path.")
    render_comparison_parser.set_defaults(func=cmd_render_comparison)

    render_gate_parser = subparsers.add_parser(
        "render-gate",
        help="Render gate JSON to Markdown.",
    )
    render_gate_parser.add_argument("report", help="Path to gate JSON report.")
    render_gate_parser.add_argument("--out", required=True, help="Output Markdown path.")
    render_gate_parser.set_defaults(func=cmd_render_gate)

    pack_prompts_parser = subparsers.add_parser(
        "pack-prompts",
        help="Build a single Markdown bundle for the next LLM run.",
    )
    pack_prompts_parser.add_argument("--prompt", required=True, help="Prompt file path.")
    pack_prompts_parser.add_argument("--standard", required=True, help="Evaluation standard path.")
    pack_prompts_parser.add_argument("--taxonomy", required=True, help="Defect taxonomy path.")
    pack_prompts_parser.add_argument("--intro", required=True, help="Introduction text path.")
    pack_prompts_parser.add_argument("--out", required=True, help="Output bundle path.")
    pack_prompts_parser.set_defaults(func=cmd_pack_prompts)

    repair_plan_parser = subparsers.add_parser(
        "repair-plan",
        help="Generate a Markdown repair plan from an audit JSON report.",
    )
    repair_plan_parser.add_argument("report", help="Path to audit JSON report.")
    repair_plan_parser.add_argument("--out", required=True, help="Output Markdown path.")
    repair_plan_parser.set_defaults(func=cmd_repair_plan)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    sys.exit(main())
