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
- render-report: render audit JSON to Markdown
- render-comparison: render comparison JSON to Markdown
- render-gate: render gate JSON to Markdown
- repair-plan: generate a repair plan Markdown from audit JSON
- pack-prompts: concatenate prompt/standard/taxonomy/input into a single bundle
- export-defects-csv: export defects from one or more audit JSON files to CSV
- trends: summarize trends across multiple audit JSON files
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter
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

DEFAULT_EXTRACTION_SCHEMA = {
    "type": "object",
    "properties": {
        "problem_context": {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "status": {
                    "type": "string",
                    "enum": ["explicit", "implicit_but_clear", "vague", "absent"],
                },
            },
            "required": ["text", "status"],
        },
        "knowledge_state": {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "status": {
                    "type": "string",
                    "enum": ["explicit", "implicit_but_clear", "vague", "absent"],
                },
            },
            "required": ["text", "status"],
        },
        "research_gap": {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "status": {
                    "type": "string",
                    "enum": ["explicit", "implicit_but_clear", "vague", "absent"],
                },
            },
            "required": ["text", "status"],
        },
        "goal": {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "status": {
                    "type": "string",
                    "enum": ["explicit", "implicit_but_clear", "vague", "absent"],
                },
            },
            "required": ["text", "status"],
        },
        "tasks": {"type": "array", "items": {"type": "string"}},
        "object": {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "status": {
                    "type": "string",
                    "enum": ["explicit", "implicit_but_clear", "vague", "absent"],
                },
            },
            "required": ["text", "status"],
        },
        "subject": {
            "type": "object",
            "properties": {
                "text": {"type": "string"},
                "status": {
                    "type": "string",
                    "enum": ["explicit", "implicit_but_clear", "vague", "absent"],
                },
            },
            "required": ["text", "status"],
        },
        "methodology": {"type": "string"},
        "methods": {"type": "array", "items": {"type": "string"}},
        "database": {"type": "string"},
        "scientific_novelty": {"type": "array", "items": {"type": "string"}},
        "propositions_for_defense": {"type": "array", "items": {"type": "string"}},
        "theoretical_significance": {"type": "string"},
        "practical_significance": {"type": "string"},
        "reliability": {"type": "string"},
        "approbation": {"type": "string"},
        "publications": {"type": "string"},
        "dissertation_structure": {"type": "string"},
    },
    "required": [
        "problem_context",
        "knowledge_state",
        "research_gap",
        "goal",
        "tasks",
        "object",
        "subject",
        "methodology",
        "methods",
        "database",
        "scientific_novelty",
        "propositions_for_defense",
        "theoretical_significance",
        "practical_significance",
        "reliability",
        "approbation",
        "publications",
        "dissertation_structure",
    ],
}

DEFAULT_AUDIT_SCHEMA = {
    "type": "object",
    "properties": {
        "metadata": {
            "type": "object",
            "properties": {
                "document_id": {"type": "string"},
                "language": {"type": "string"},
                "audit_mode": {"type": "string"},
                "date": {"type": "string"},
            },
            "required": ["document_id", "language", "audit_mode", "date"],
        },
        "extraction": {"type": "object"},
        "scores": {
            "type": "object",
            "properties": {
                "SC1": {"type": "integer"},
                "SC2": {"type": "integer"},
                "LC1": {"type": "integer"},
                "LC2": {"type": "integer"},
                "LC3": {"type": "integer"},
                "LC4": {"type": "integer"},
                "LC5": {"type": "integer"},
                "LC6": {"type": "integer"},
                "NV": {"type": "integer"},
                "VAL": {"type": "integer"},
            },
            "required": [
                "SC1",
                "SC2",
                "LC1",
                "LC2",
                "LC3",
                "LC4",
                "LC5",
                "LC6",
                "NV",
                "VAL",
            ],
        },
        "defects": {"type": "array"},
        "gost_compliance": {"type": "object"},
        "summary": {"type": "object"},
    },
    "required": [
        "metadata",
        "extraction",
        "scores",
        "defects",
        "gost_compliance",
        "summary",
    ],
}

DEFAULT_COMPARISON_SCHEMA = {
    "type": "object",
    "properties": {
        "from_version": {"type": "string"},
        "to_version": {"type": "string"},
        "resolved_defects": {"type": "array", "items": {"type": "string"}},
        "remaining_defects": {"type": "array", "items": {"type": "string"}},
        "new_defects": {"type": "array", "items": {"type": "string"}},
        "score_diff": {"type": "object"},
        "regression_warnings": {"type": "array", "items": {"type": "string"}},
        "overall_assessment": {"type": "string"},
    },
    "required": [
        "from_version",
        "to_version",
        "resolved_defects",
        "remaining_defects",
        "new_defects",
        "score_diff",
        "regression_warnings",
        "overall_assessment",
    ],
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
- intro-qa render-report
- intro-qa render-comparison
- intro-qa render-gate
- intro-qa repair-plan
- intro-qa pack-prompts
- intro-qa export-defects-csv
- intro-qa trends

The CLI does not call an LLM directly. Instead, it helps you manage:
- project scaffolding
- audit reports
- comparison reports
- acceptance gate checks
- Markdown rendering
- defect exports
- trend summaries across multiple reports
"""

DEFAULT_AUDIT_PROMPT = """# Audit Prompt

Вы выступаете как методологический эксперт, выполняющий строгий аудит введения диссертации.

Отчет должен быть написан полностью на русском языке.

Позиция: аналитическая, критическая, диагностическая.
Любая неясность, расплывчатость, двусмысленность или шаблонность должна трактоваться как дефект.
Не додумывайте отсутствующие элементы за автора.

Требуемые блоки ответа:
1. NORMALIZED EXTRACTION
2. STRUCTURAL ANALYSIS
3. GOST COMPLIANCE CHECK
4. RESEARCH LOGIC ANALYSIS
5. CRITERION SCORES
6. DEFECTS BY SEVERITY
7. FINAL DIAGNOSTIC ASSESSMENT
8. REVISION PRIORITIES
"""

DEFAULT_LINT_PROMPT = """# Lint Prompt

Вы выполняете быстрый строгий lint-анализ введения диссертации.

Язык ответа: русский.
Позиция: критическая.
Любая неясность считается дефектом.
Не восстанавливайте отсутствующие элементы за автора.
"""

DEFAULT_REPAIR_PROMPT = """# Repair Prompt

Вы выполняете адресную методологическую переработку текста.

Язык ответа: русский.
Исправляйте только необходимые фрагменты для устранения указанных defect codes.
Сохраняйте общую структуру, если она не мешает исправлению.
"""

DEFAULT_COMPARE_PROMPT = """# Compare Prompt

Вы сравниваете два аудиторских отчета по двум версиям введения диссертации.

Язык ответа: русский.
Определите устраненные дефекты, оставшиеся дефекты, новые дефекты,
динамику score и возможные регрессии.
"""

DEFAULT_REPORT_TEMPLATE = """# Audit Report Template

## Metadata
- document_id:
- language: ru
- audit_mode:
- date:

## Summary
- overall_verdict:
- critical_count:
- major_count:
- moderate_count:
- minor_count:
- logical_integrity_score:

## Revision Priorities
1.
2.
3.
"""

DEFAULT_REPAIR_PLAN_TEMPLATE = """# Repair Plan Template

## Critical Defects
- 

## Major Defects
- 

## Moderate Defects
- 

## Minor Defects
- 

## Ordered Rewrite Agenda
1.
2.
3.
"""

DEFAULT_COMPARISON_TEMPLATE = """# Comparison Report Template

## Resolved Defects
- 

## Remaining Defects
- 

## New Defects
- 

## Regression Warnings
- 

## Overall Assessment

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
        base_dir / "exports",
        base_dir / "trends",
        base_dir / "templates",
    ]
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)

    _write_text(base_dir / "README.md", DEFAULT_README)
    _write_text(
        base_dir / "configs" / "acceptance_profiles.yaml",
        DEFAULT_ACCEPTANCE_PROFILES,
    )
    _write_json(base_dir / "schemas" / "extraction_schema.json", DEFAULT_EXTRACTION_SCHEMA)
    _write_json(base_dir / "schemas" / "audit_report_schema.json", DEFAULT_AUDIT_SCHEMA)
    _write_json(
        base_dir / "schemas" / "comparison_schema.json", DEFAULT_COMPARISON_SCHEMA
    )
    _write_json(base_dir / "reports" / "audit_report_template.json", DEFAULT_AUDIT_REPORT)
    _write_json(
        base_dir / "comparisons" / "comparison_report_template.json",
        DEFAULT_COMPARISON_REPORT,
    )
    _write_text(base_dir / "prompts" / "audit_prompt.md", DEFAULT_AUDIT_PROMPT)
    _write_text(base_dir / "prompts" / "lint_prompt.md", DEFAULT_LINT_PROMPT)
    _write_text(base_dir / "prompts" / "repair_prompt.md", DEFAULT_REPAIR_PROMPT)
    _write_text(base_dir / "prompts" / "compare_prompt.md", DEFAULT_COMPARE_PROMPT)
    _write_text(base_dir / "templates" / "report_template.md", DEFAULT_REPORT_TEMPLATE)
    _write_text(
        base_dir / "templates" / "repair_plan_template.md",
        DEFAULT_REPAIR_PLAN_TEMPLATE,
    )
    _write_text(
        base_dir / "templates" / "comparison_report_template.md",
        DEFAULT_COMPARISON_TEMPLATE,
    )
    _write_text(
        base_dir / "inputs" / "intro_example.md",
        "# Intro Example\n\nПоместите сюда текст введения для анализа.\n",
    )


def _bullet_lines(items: list[str]) -> str:
    if not items:
        return "- нет"
    return "\n".join(f"- {item}" for item in items)


def _render_report_markdown(report: dict[str, Any]) -> str:
    metadata = report.get("metadata", {})
    summary = report.get("summary", {})
    defects = report.get("defects", [])
    scores = report.get("scores", {})
    gost = report.get("gost_compliance", {})

    lines = [
        f"# Audit Report: {metadata.get('document_id', 'unknown')}",
        "",
        "## Metadata",
        f"- language: {metadata.get('language', '')}",
        f"- audit_mode: {metadata.get('audit_mode', '')}",
        f"- date: {metadata.get('date', '')}",
        "",
        "## Summary",
        f"- overall_verdict: {summary.get('overall_verdict', '')}",
        f"- critical_count: {summary.get('critical_count', 0)}",
        f"- major_count: {summary.get('major_count', 0)}",
        f"- moderate_count: {summary.get('moderate_count', 0)}",
        f"- minor_count: {summary.get('minor_count', 0)}",
        f"- logical_integrity_score: {summary.get('logical_integrity_score', 0)}",
        "",
        "## Scores",
    ]
    for key in sorted(scores):
        lines.append(f"- {key}: {scores[key]}")

    lines.extend(["", "## GOST Compliance"])
    for key in sorted(gost):
        lines.append(f"- {key}: {gost[key]}")

    lines.extend(["", "## Defects"])
    if not defects:
        lines.append("- defects not listed")
    else:
        for idx, defect in enumerate(defects, start=1):
            lines.extend(
                [
                    f"### {idx}. {defect.get('code', 'NO-CODE')} ({defect.get('severity', '')})",
                    f"- section: {defect.get('section', '')}",
                    f"- description: {defect.get('description', '')}",
                    f"- evidence: {defect.get('evidence', '')}",
                    f"- recommendation: {defect.get('recommendation', '')}",
                    "",
                ]
            )
    return "\n".join(lines).strip() + "\n"


def _render_comparison_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# Comparison: {report.get('from_version', '')} → {report.get('to_version', '')}",
        "",
        "## Resolved Defects",
        _bullet_lines(report.get("resolved_defects", [])),
        "",
        "## Remaining Defects",
        _bullet_lines(report.get("remaining_defects", [])),
        "",
        "## New Defects",
        _bullet_lines(report.get("new_defects", [])),
        "",
        "## Score Delta",
    ]
    score_diff = report.get("score_diff", {})
    if score_diff:
        for key in sorted(score_diff):
            lines.append(f"- {key}: {score_diff[key]:+g}")
    else:
        lines.append("- нет")

    lines.extend(
        [
            "",
            "## Regression Warnings",
            _bullet_lines(report.get("regression_warnings", [])),
            "",
            "## Overall Assessment",
            report.get("overall_assessment", ""),
            "",
        ]
    )
    return "\n".join(lines)


def _render_gate_markdown(report: dict[str, Any]) -> str:
    lines = [
        f"# Gate Result: {report.get('profile', '')}",
        "",
        f"- passed: {report.get('passed', False)}",
        "",
        "## Failures",
        _bullet_lines(report.get("failures", [])),
        "",
    ]
    return "\n".join(lines)


def _build_repair_plan(report: dict[str, Any]) -> str:
    grouped: dict[str, list[dict[str, Any]]] = {
        "critical": [],
        "major": [],
        "moderate": [],
        "minor": [],
    }
    for defect in report.get("defects", []):
        severity = str(defect.get("severity", "")).lower()
        if severity in grouped:
            grouped[severity].append(defect)

    lines = [
        f"# Repair Plan: {report.get('metadata', {}).get('document_id', 'unknown')}",
        "",
    ]
    for severity in ["critical", "major", "moderate", "minor"]:
        title = severity.capitalize()
        lines.append(f"## {title} Defects")
        if not grouped[severity]:
            lines.append("- нет")
            lines.append("")
            continue
        for defect in grouped[severity]:
            lines.append(
                f"- {defect.get('code', 'NO-CODE')}: {defect.get('description', '')}"
            )
            recommendation = defect.get("recommendation", "")
            if recommendation:
                lines.append(f"  - recommendation: {recommendation}")
        lines.append("")

    ordered = grouped["critical"] + grouped["major"] + grouped["moderate"] + grouped["minor"]
    lines.append("## Ordered Rewrite Agenda")
    if not ordered:
        lines.append("1. Существенных дефектов для переработки не зафиксировано.")
    else:
        for idx, defect in enumerate(ordered, start=1):
            lines.append(
                f"{idx}. Устранить {defect.get('code', 'NO-CODE')} в разделе "
                f"{defect.get('section', '')}."
            )
    lines.append("")
    return "\n".join(lines)


def _pack_prompts(prompt: Path, standard: Path, taxonomy: Path, intro: Path) -> str:
    parts = [
        "PROMPT\n" + prompt.read_text(encoding="utf-8").strip(),
        "EVALUATION STANDARD\n" + standard.read_text(encoding="utf-8").strip(),
        "DEFECT TAXONOMY\n" + taxonomy.read_text(encoding="utf-8").strip(),
        "TEXT TO EVALUATE\n" + intro.read_text(encoding="utf-8").strip(),
    ]
    return "\n\n---\n\n".join(parts) + "\n"


def _collect_audit_reports(paths: list[str]) -> list[dict[str, Any]]:
    return [_read_json(Path(path)) for path in paths]


def _document_label(report: dict[str, Any], fallback: str) -> str:
    return str(report.get("metadata", {}).get("document_id", fallback))


def _export_defects_csv(reports: list[dict[str, Any]], out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "document_id",
                "date",
                "code",
                "severity",
                "section",
                "description",
                "evidence",
                "recommendation",
            ],
        )
        writer.writeheader()
        for idx, report in enumerate(reports, start=1):
            metadata = report.get("metadata", {})
            for defect in report.get("defects", []):
                writer.writerow(
                    {
                        "document_id": _document_label(report, f"report_{idx}"),
                        "date": metadata.get("date", ""),
                        "code": defect.get("code", ""),
                        "severity": defect.get("severity", ""),
                        "section": defect.get("section", ""),
                        "description": defect.get("description", ""),
                        "evidence": defect.get("evidence", ""),
                        "recommendation": defect.get("recommendation", ""),
                    }
                )


def _trend_summary(reports: list[dict[str, Any]]) -> dict[str, Any]:
    severity_counter: Counter[str] = Counter()
    code_counter: Counter[str] = Counter()
    score_avgs: dict[str, float] = {}
    score_counts: Counter[str] = Counter()
    score_sums: Counter[str] = Counter()
    documents: list[dict[str, Any]] = []

    for idx, report in enumerate(reports, start=1):
        label = _document_label(report, f"report_{idx}")
        summary = report.get("summary", {})
        defects = report.get("defects", [])
        scores = report.get("scores", {})
        documents.append(
            {
                "document_id": label,
                "critical_count": int(summary.get("critical_count", 0)),
                "major_count": int(summary.get("major_count", 0)),
                "moderate_count": int(summary.get("moderate_count", 0)),
                "minor_count": int(summary.get("minor_count", 0)),
                "logical_integrity_score": float(
                    summary.get("logical_integrity_score", 0.0)
                ),
            }
        )
        for defect in defects:
            severity_counter[str(defect.get("severity", "unknown")).lower()] += 1
            code = str(defect.get("code", ""))
            if code:
                code_counter[code] += 1
        for key, value in scores.items():
            score_sums[key] += float(value)
            score_counts[key] += 1

    for key in sorted(score_sums):
        count = score_counts[key]
        score_avgs[key] = round(float(score_sums[key]) / max(count, 1), 3)

    return {
        "report_count": len(reports),
        "documents": documents,
        "severity_totals": dict(sorted(severity_counter.items())),
        "top_defect_codes": [
            {"code": code, "count": count}
            for code, count in code_counter.most_common(10)
        ],
        "average_scores": score_avgs,
    }


def _render_trend_markdown(payload: dict[str, Any]) -> str:
    lines = [
        f"# Trend Summary ({payload.get('report_count', 0)} reports)",
        "",
        "## Severity Totals",
    ]
    severity_totals = payload.get("severity_totals", {})
    if severity_totals:
        for key in sorted(severity_totals):
            lines.append(f"- {key}: {severity_totals[key]}")
    else:
        lines.append("- нет")

    lines.extend(["", "## Average Scores"])
    average_scores = payload.get("average_scores", {})
    if average_scores:
        for key in sorted(average_scores):
            lines.append(f"- {key}: {average_scores[key]}")
    else:
        lines.append("- нет")

    lines.extend(["", "## Top Defect Codes"])
    top_codes = payload.get("top_defect_codes", [])
    if top_codes:
        for item in top_codes:
            lines.append(f"- {item.get('code', '')}: {item.get('count', 0)}")
    else:
        lines.append("- нет")

    lines.extend(["", "## Document Snapshots"])
    for doc in payload.get("documents", []):
        lines.extend(
            [
                f"### {doc.get('document_id', '')}",
                f"- critical_count: {doc.get('critical_count', 0)}",
                f"- major_count: {doc.get('major_count', 0)}",
                f"- moderate_count: {doc.get('moderate_count', 0)}",
                f"- minor_count: {doc.get('minor_count', 0)}",
                f"- logical_integrity_score: {doc.get('logical_integrity_score', 0)}",
                "",
            ]
        )
    return "\n".join(lines).rstrip() + "\n"


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
    _write_text(Path(args.out), _render_report_markdown(report))
    print(f"Wrote Markdown report: {args.out}")
    return 0


def cmd_render_comparison(args: argparse.Namespace) -> int:
    report = _read_json(Path(args.report))
    _write_text(Path(args.out), _render_comparison_markdown(report))
    print(f"Wrote Markdown comparison: {args.out}")
    return 0


def cmd_render_gate(args: argparse.Namespace) -> int:
    report = _read_json(Path(args.report))
    _write_text(Path(args.out), _render_gate_markdown(report))
    print(f"Wrote Markdown gate report: {args.out}")
    return 0


def cmd_repair_plan(args: argparse.Namespace) -> int:
    report = _read_json(Path(args.report))
    _write_text(Path(args.out), _build_repair_plan(report))
    print(f"Wrote repair plan: {args.out}")
    return 0


def cmd_pack_prompts(args: argparse.Namespace) -> int:
    bundle = _pack_prompts(
        Path(args.prompt),
        Path(args.standard),
        Path(args.taxonomy),
        Path(args.intro),
    )
    _write_text(Path(args.out), bundle)
    print(f"Wrote prompt bundle: {args.out}")
    return 0


def cmd_export_defects_csv(args: argparse.Namespace) -> int:
    reports = _collect_audit_reports(args.reports)
    _export_defects_csv(reports, Path(args.out))
    print(f"Wrote defect CSV export: {args.out}")
    return 0


def cmd_trends(args: argparse.Namespace) -> int:
    reports = _collect_audit_reports(args.reports)
    payload = _trend_summary(reports)
    _write_json(Path(args.out_json), payload)
    if args.out_md:
        _write_text(Path(args.out_md), _render_trend_markdown(payload))
    print(f"Wrote trend summary JSON: {args.out_json}")
    if args.out_md:
        print(f"Wrote trend summary Markdown: {args.out_md}")
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
    render_comparison_parser.add_argument(
        "--out", required=True, help="Output Markdown path."
    )
    render_comparison_parser.set_defaults(func=cmd_render_comparison)

    render_gate_parser = subparsers.add_parser(
        "render-gate",
        help="Render gate JSON to Markdown.",
    )
    render_gate_parser.add_argument("report", help="Path to gate JSON report.")
    render_gate_parser.add_argument("--out", required=True, help="Output Markdown path.")
    render_gate_parser.set_defaults(func=cmd_render_gate)

    repair_plan_parser = subparsers.add_parser(
        "repair-plan",
        help="Generate Markdown repair plan from audit JSON.",
    )
    repair_plan_parser.add_argument("report", help="Path to audit JSON report.")
    repair_plan_parser.add_argument("--out", required=True, help="Output Markdown path.")
    repair_plan_parser.set_defaults(func=cmd_repair_plan)

    pack_parser = subparsers.add_parser(
        "pack-prompts",
        help="Bundle prompt, standard, taxonomy, and intro text into one file.",
    )
    pack_parser.add_argument("--prompt", required=True, help="Path to prompt Markdown.")
    pack_parser.add_argument(
        "--standard", required=True, help="Path to evaluation standard Markdown."
    )
    pack_parser.add_argument(
        "--taxonomy", required=True, help="Path to defect taxonomy Markdown."
    )
    pack_parser.add_argument("--intro", required=True, help="Path to introduction text.")
    pack_parser.add_argument("--out", required=True, help="Output bundle path.")
    pack_parser.set_defaults(func=cmd_pack_prompts)

    defects_csv_parser = subparsers.add_parser(
        "export-defects-csv",
        help="Export defects from one or more audit JSON files to CSV.",
    )
    defects_csv_parser.add_argument(
        "reports",
        nargs="+",
        help="One or more audit JSON report paths.",
    )
    defects_csv_parser.add_argument("--out", required=True, help="Output CSV path.")
    defects_csv_parser.set_defaults(func=cmd_export_defects_csv)

    trends_parser = subparsers.add_parser(
        "trends",
        help="Summarize trends across multiple audit JSON files.",
    )
    trends_parser.add_argument(
        "reports",
        nargs="+",
        help="One or more audit JSON report paths.",
    )
    trends_parser.add_argument("--out-json", required=True, help="Output trend JSON path.")
    trends_parser.add_argument("--out-md", help="Optional output Markdown path.")
    trends_parser.set_defaults(func=cmd_trends)

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
