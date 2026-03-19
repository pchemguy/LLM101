#!/usr/bin/env python3
"""CLI for dissertation introduction QA pipeline.

Phase 6 adds:
- defect-cluster: cluster defects by section/severity/category
- section-analytics: section-wise analytics over one or more audit reports
- html-dashboard: render a baseline HTML dashboard from history index or audit files

This tool intentionally keeps dependencies minimal.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Tuple


def read_json(path: Path) -> Dict[str, Any]:
  with path.open("r", encoding="utf-8") as f:
    return json.load(f)


def write_json(path: Path, data: Dict[str, Any]) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  with path.open("w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)


def write_text(path: Path, text: str) -> None:
  path.parent.mkdir(parents=True, exist_ok=True)
  path.write_text(text, encoding="utf-8")


def scaffold_project(target: Path) -> None:
  dirs = [
      "standards", "prompts", "configs", "schemas", "inputs", "reports",
      "comparisons", "repair", "templates", "history", "dashboard",
  ]
  for rel in dirs:
    (target / rel).mkdir(parents=True, exist_ok=True)
  for rel in ["reports", "comparisons", "repair", "history", "dashboard"]:
    (target / rel / ".gitkeep").write_text("", encoding="utf-8")
  (target / "inputs" / "intro_example.md").write_text(
      "# Intro Example\n\nПоместите сюда текст введения диссертации.\n",
      encoding="utf-8",
  )


def scaffold_report(path: Path, document_id: str = "intro_v1") -> None:
  data = {
      "metadata": {
          "document_id": document_id,
          "language": "ru",
          "audit_mode": "full",
          "date": str(date.today()),
      },
      "extraction": {},
      "scores": {
          "SC1": 0, "SC2": 0, "LC1": 0, "LC2": 0, "LC3": 0,
          "LC4": 0, "LC5": 0, "LC6": 0, "NV": 0, "VAL": 0,
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
  write_json(path, data)


def scaffold_comparison(path: Path, from_version: str = "v1", to_version: str = "v2") -> None:
  data = {
      "from_version": from_version,
      "to_version": to_version,
      "resolved_defects": [],
      "remaining_defects": [],
      "new_defects": [],
      "score_diff": {},
      "regression_warnings": [],
      "overall_assessment": "",
  }
  write_json(path, data)


def defect_key(defect: Dict[str, Any]) -> Tuple[str, str]:
  return defect.get("code", ""), defect.get("section", "")


def compare_reports(report1: Dict[str, Any], report2: Dict[str, Any]) -> Dict[str, Any]:
  defects1 = {defect_key(d): d for d in report1.get("defects", [])}
  defects2 = {defect_key(d): d for d in report2.get("defects", [])}
  keys1, keys2 = set(defects1), set(defects2)

  scores1, scores2 = report1.get("scores", {}), report2.get("scores", {})
  score_diff = {k: scores2.get(k, 0) - scores1.get(k, 0) for k in sorted(set(scores1) | set(scores2))}
  regressions = [f"Снижение score по {k}: {d}" for k, d in score_diff.items() if d < 0]

  return {
      "from_version": report1.get("metadata", {}).get("document_id", "v1"),
      "to_version": report2.get("metadata", {}).get("document_id", "v2"),
      "resolved_defects": [k[0] for k in sorted(keys1 - keys2)],
      "remaining_defects": [k[0] for k in sorted(keys1 & keys2)],
      "new_defects": [k[0] for k in sorted(keys2 - keys1)],
      "score_diff": score_diff,
      "regression_warnings": regressions,
      "overall_assessment": "",
  }


def load_yaml_like_profiles(path: Path) -> Dict[str, Any]:
  text = path.read_text(encoding="utf-8").splitlines()
  profiles: Dict[str, Any] = {}
  current_profile = None
  current_block = None
  for raw in text:
    line = raw.rstrip()
    if not line or line.lstrip().startswith("#") or line.startswith("profiles:"):
      continue
    if line.startswith("  ") and not line.startswith("    ") and line.strip().endswith(":"):
      current_profile = line.strip()[:-1]
      profiles[current_profile] = {}
      current_block = None
      continue
    if current_profile is None:
      continue
    stripped = line.strip()
    if stripped.endswith(":") and ":" not in stripped[:-1]:
      current_block = stripped[:-1]
      profiles[current_profile][current_block] = {}
      continue
    if stripped.startswith("- "):
      profiles[current_profile].setdefault(current_block, [])
      profiles[current_profile][current_block].append(stripped[2:].strip())
      continue
    if ":" in stripped:
      key, value = stripped.split(":", 1)
      key, value = key.strip(), value.strip()
      try:
        value_obj = int(value)
      except ValueError:
        try:
          value_obj = float(value)
        except ValueError:
          value_obj = value.lower() == "true" if value.lower() in {"true", "false"} else value
      if current_block and line.startswith("      "):
        profiles[current_profile][current_block][key] = value_obj
      else:
        profiles[current_profile][key] = value_obj
  return {"profiles": profiles}


def run_gate(report: Dict[str, Any], config: Dict[str, Any], profile_name: str) -> Dict[str, Any]:
  profile = config.get("profiles", {}).get(profile_name)
  if profile is None:
    raise ValueError(f"Profile not found: {profile_name}")

  summary = report.get("summary", {})
  scores = report.get("scores", {})
  gost = report.get("gost_compliance", {})
  failed = []

  if summary.get("critical_count", 0) > profile.get("max_critical", 10**9):
    failed.append(f"critical_count={summary.get('critical_count', 0)} > {profile.get('max_critical')}")
  if summary.get("major_count", 0) > profile.get("max_major", 10**9):
    failed.append(f"major_count={summary.get('major_count', 0)} > {profile.get('max_major')}")

  for key, threshold in profile.get("min_scores", {}).items():
    if scores.get(key, 0) < threshold:
      failed.append(f"score {key}={scores.get(key, 0)} < {threshold}")

  for gost_key in profile.get("require_gost", []):
    if not gost.get(gost_key, False):
      failed.append(f"missing_gost_component={gost_key}")

  return {
      "profile": profile_name,
      "passed": not failed,
      "failed_checks": failed,
      "summary": summary,
      "scores": scores,
  }


def render_report_md(report: Dict[str, Any]) -> str:
  lines = ["# Audit Report", ""]
  meta = report.get("metadata", {})
  lines += [
      f"- Document ID: {meta.get('document_id', '')}",
      f"- Language: {meta.get('language', '')}",
      f"- Audit mode: {meta.get('audit_mode', '')}",
      f"- Date: {meta.get('date', '')}",
      "",
      "## Scores",
  ]
  for key, value in report.get("scores", {}).items():
    lines.append(f"- {key}: {value}")
  lines += ["", "## Defects"]
  defects = report.get("defects", [])
  if not defects:
    lines.append("- No defects listed.")
  else:
    for defect in defects:
      lines += [
          f"- [{defect.get('severity', '').upper()}] {defect.get('code', '')}",
          f"  - Section: {defect.get('section', '')}",
          f"  - Description: {defect.get('description', '')}",
          f"  - Evidence: {defect.get('evidence', '')}",
          f"  - Recommendation: {defect.get('recommendation', '')}",
      ]
  lines += ["", "## Summary"]
  for key, value in report.get("summary", {}).items():
    lines.append(f"- {key}: {value}")
  return "\n".join(lines) + "\n"


def render_comparison_md(comp: Dict[str, Any]) -> str:
  lines = [f"# Comparison: {comp.get('from_version', '')} → {comp.get('to_version', '')}", "", "## Resolved defects"]
  for item in comp.get("resolved_defects", []):
    lines.append(f"- {item}")
  lines += ["", "## Remaining defects"]
  for item in comp.get("remaining_defects", []):
    lines.append(f"- {item}")
  lines += ["", "## New defects"]
  for item in comp.get("new_defects", []):
    lines.append(f"- {item}")
  lines += ["", "## Score delta"]
  for key, delta in comp.get("score_diff", {}).items():
    lines.append(f"- {key}: {delta:+}")
  lines += ["", "## Regression warnings"]
  for item in comp.get("regression_warnings", []):
    lines.append(f"- {item}")
  lines += ["", "## Overall assessment", comp.get("overall_assessment", "")]
  return "\n".join(lines) + "\n"


def render_gate_md(gate: Dict[str, Any]) -> str:
  lines = [f"# Gate Result: {gate.get('profile', '')}", "", f"- Passed: {gate.get('passed', False)}", "", "## Failed checks"]
  failed = gate.get("failed_checks", [])
  if failed:
    lines += [f"- {item}" for item in failed]
  else:
    lines.append("- None")
  lines += ["", "## Summary"]
  for key, value in gate.get("summary", {}).items():
    lines.append(f"- {key}: {value}")
  lines += ["", "## Scores"]
  for key, value in gate.get("scores", {}).items():
    lines.append(f"- {key}: {value}")
  return "\n".join(lines) + "\n"


def pack_prompts(prompt: Path, standard: Path, taxonomy: Path, intro: Path, out: Path) -> None:
  text = "\n".join([
      "# PROMPT",
      prompt.read_text(encoding="utf-8"),
      "",
      "# EVALUATION STANDARD",
      standard.read_text(encoding="utf-8"),
      "",
      "# DEFECT TAXONOMY",
      taxonomy.read_text(encoding="utf-8"),
      "",
      "# TEXT TO EVALUATE",
      intro.read_text(encoding="utf-8"),
      "",
  ])
  write_text(out, text)


def generate_repair_plan(report: Dict[str, Any]) -> str:
  grouped = defaultdict(list)
  severity_order = {"critical": 0, "major": 1, "moderate": 2, "minor": 3}
  for defect in report.get("defects", []):
    grouped[defect.get("section", "UNSPECIFIED")].append(defect)

  lines = ["# Repair Plan", ""]
  for section in sorted(grouped):
    lines.append(f"## {section}")
    defects = sorted(grouped[section], key=lambda d: severity_order.get(d.get("severity", ""), 99))
    for defect in defects:
      lines += [
          f"- [{defect.get('severity', '').upper()}] {defect.get('code', '')}",
          f"  - Problem: {defect.get('description', '')}",
          f"  - Evidence: {defect.get('evidence', '')}",
          f"  - Recommendation: {defect.get('recommendation', '')}",
      ]
    lines.append("")
  return "\n".join(lines) + "\n"


def export_defects_csv(reports: List[Path], out: Path) -> None:
  rows = []
  for report_path in reports:
    report = read_json(report_path)
    doc_id = report.get("metadata", {}).get("document_id", report_path.stem)
    for defect in report.get("defects", []):
      rows.append({
          "document_id": doc_id,
          "code": defect.get("code", ""),
          "severity": defect.get("severity", ""),
          "section": defect.get("section", ""),
          "description": defect.get("description", ""),
          "evidence": defect.get("evidence", ""),
          "recommendation": defect.get("recommendation", ""),
      })
  out.parent.mkdir(parents=True, exist_ok=True)
  with out.open("w", encoding="utf-8", newline="") as f:
    writer = csv.DictWriter(
        f,
        fieldnames=["document_id", "code", "severity", "section", "description", "evidence", "recommendation"],
    )
    writer.writeheader()
    writer.writerows(rows)


def trend_summary(reports: List[Path]) -> Dict[str, Any]:
  by_doc = []
  defect_counter = Counter()
  severity_counter = Counter()
  for report_path in reports:
    report = read_json(report_path)
    meta = report.get("metadata", {})
    defects = report.get("defects", [])
    for defect in defects:
      defect_counter[defect.get("code", "")] += 1
      severity_counter[defect.get("severity", "")] += 1
    by_doc.append({
        "document_id": meta.get("document_id", report_path.stem),
        "date": meta.get("date", ""),
        "critical_count": report.get("summary", {}).get("critical_count", 0),
        "major_count": report.get("summary", {}).get("major_count", 0),
        "moderate_count": report.get("summary", {}).get("moderate_count", 0),
        "minor_count": report.get("summary", {}).get("minor_count", 0),
        "scores": report.get("scores", {}),
    })
  return {
      "documents": by_doc,
      "defect_frequency": dict(defect_counter.most_common()),
      "severity_totals": dict(severity_counter),
  }


def trends_markdown(summary: Dict[str, Any]) -> str:
  lines = ["# Trend Summary", "", "## Documents"]
  for doc in summary.get("documents", []):
    lines.append(
        f"- {doc.get('document_id', '')}: critical={doc.get('critical_count', 0)}, "
        f"major={doc.get('major_count', 0)}, moderate={doc.get('moderate_count', 0)}, "
        f"minor={doc.get('minor_count', 0)}"
    )
  lines += ["", "## Defect frequency"]
  for code, count in summary.get("defect_frequency", {}).items():
    lines.append(f"- {code}: {count}")
  lines += ["", "## Severity totals"]
  for sev, count in summary.get("severity_totals", {}).items():
    lines.append(f"- {sev}: {count}")
  return "\n".join(lines) + "\n"


def validate_audit(report: Dict[str, Any]) -> Dict[str, Any]:
  required = ["metadata", "extraction", "scores", "defects", "gost_compliance", "summary"]
  missing = [key for key in required if key not in report]
  return {"valid": not missing, "missing_top_level": missing}


def validate_comparison(comp: Dict[str, Any]) -> Dict[str, Any]:
  required = ["from_version", "to_version", "resolved_defects", "remaining_defects", "new_defects", "score_diff", "regression_warnings", "overall_assessment"]
  missing = [key for key in required if key not in comp]
  return {"valid": not missing, "missing_top_level": missing}


def history_index(reports: List[Path]) -> Dict[str, Any]:
  items = []
  defect_frequency = Counter()
  severity_frequency = Counter()
  for path in reports:
    report = read_json(path)
    meta = report.get("metadata", {})
    defects = report.get("defects", [])
    for defect in defects:
      defect_frequency[defect.get("code", "")] += 1
      severity_frequency[defect.get("severity", "")] += 1
    items.append({
        "document_id": meta.get("document_id", path.stem),
        "date": meta.get("date", ""),
        "summary": report.get("summary", {}),
        "scores": report.get("scores", {}),
    })
  return {
      "reports": items,
      "defect_frequency": dict(defect_frequency.most_common()),
      "severity_frequency": dict(severity_frequency),
  }


def render_dashboard_md(index: Dict[str, Any]) -> str:
  lines = ["# QA Dashboard", "", "## Reports"]
  for item in index.get("reports", []):
    summary = item.get("summary", {})
    lines.append(
        f"- {item.get('document_id', '')}: critical={summary.get('critical_count', 0)}, "
        f"major={summary.get('major_count', 0)}, moderate={summary.get('moderate_count', 0)}, "
        f"minor={summary.get('minor_count', 0)}"
    )
  lines += ["", "## Defect frequency"]
  for code, count in index.get("defect_frequency", {}).items():
    lines.append(f"- {code}: {count}")
  lines += ["", "## Severity frequency"]
  for sev, count in index.get("severity_frequency", {}).items():
    lines.append(f"- {sev}: {count}")
  return "\n".join(lines) + "\n"


def defect_clusters(reports: List[Path]) -> Dict[str, Any]:
  by_section = defaultdict(Counter)
  by_severity = Counter()
  by_category = Counter()
  by_section_severity = defaultdict(Counter)
  for path in reports:
    report = read_json(path)
    for defect in report.get("defects", []):
      section = defect.get("section", "UNSPECIFIED")
      severity = defect.get("severity", "unspecified")
      code = defect.get("code", "")
      category = code.split("-", 1)[0] if "-" in code else code or "UNKNOWN"
      by_section[section][code] += 1
      by_severity[severity] += 1
      by_category[category] += 1
      by_section_severity[section][severity] += 1
  return {
      "by_section": {k: dict(v.most_common()) for k, v in sorted(by_section.items())},
      "by_severity": dict(by_severity),
      "by_category": dict(by_category.most_common()),
      "by_section_severity": {k: dict(v) for k, v in sorted(by_section_severity.items())},
  }


def section_analytics(reports: List[Path]) -> Dict[str, Any]:
  result = defaultdict(lambda: {
      "defect_count": 0, "critical": 0, "major": 0, "moderate": 0, "minor": 0,
      "codes": Counter(), "documents": set(),
  })
  for path in reports:
    report = read_json(path)
    doc_id = report.get("metadata", {}).get("document_id", path.stem)
    for defect in report.get("defects", []):
      section = defect.get("section", "UNSPECIFIED")
      sev = defect.get("severity", "").lower()
      code = defect.get("code", "")
      bucket = result[section]
      bucket["defect_count"] += 1
      if sev in {"critical", "major", "moderate", "minor"}:
        bucket[sev] += 1
      bucket["codes"][code] += 1
      bucket["documents"].add(doc_id)
  normalized = {}
  for section, data in result.items():
    normalized[section] = {
        "defect_count": data["defect_count"],
        "critical": data["critical"],
        "major": data["major"],
        "moderate": data["moderate"],
        "minor": data["minor"],
        "top_codes": dict(data["codes"].most_common(10)),
        "documents": sorted(data["documents"]),
        "document_count": len(data["documents"]),
    }
  return normalized


def render_section_analytics_md(data: Dict[str, Any]) -> str:
  lines = ["# Section-wise Analytics", ""]
  for section, stats in sorted(data.items(), key=lambda kv: (-kv[1].get("defect_count", 0), kv[0])):
    lines += [
        f"## {section}",
        f"- defect_count: {stats.get('defect_count', 0)}",
        f"- critical: {stats.get('critical', 0)}",
        f"- major: {stats.get('major', 0)}",
        f"- moderate: {stats.get('moderate', 0)}",
        f"- minor: {stats.get('minor', 0)}",
        f"- document_count: {stats.get('document_count', 0)}",
        "- top_codes:",
    ]
    for code, count in stats.get("top_codes", {}).items():
      lines.append(f"  - {code}: {count}")
    lines.append("")
  return "\n".join(lines) + "\n"


def render_cluster_md(data: Dict[str, Any]) -> str:
  lines = ["# Defect Clusters", "", "## By category"]
  for cat, count in data.get("by_category", {}).items():
    lines.append(f"- {cat}: {count}")
  lines += ["", "## By severity"]
  for sev, count in data.get("by_severity", {}).items():
    lines.append(f"- {sev}: {count}")
  lines += ["", "## By section"]
  for section, codes in data.get("by_section", {}).items():
    lines.append(f"### {section}")
    for code, count in codes.items():
      lines.append(f"- {code}: {count}")
    sev_stats = data.get("by_section_severity", {}).get(section, {})
    if sev_stats:
      lines.append("- severity_breakdown:")
      for sev, count in sev_stats.items():
        lines.append(f"  - {sev}: {count}")
    lines.append("")
  return "\n".join(lines) + "\n"


def html_escape(text: str) -> str:
  return str(text).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def render_html_dashboard(index: Dict[str, Any], clusters: Dict[str, Any], sections: Dict[str, Any]) -> str:
  report_rows = []
  for item in index.get("reports", []):
    summary = item.get("summary", {})
    report_rows.append(
        "<tr>"
        f"<td>{html_escape(item.get('document_id', ''))}</td>"
        f"<td>{html_escape(item.get('date', ''))}</td>"
        f"<td>{summary.get('critical_count', 0)}</td>"
        f"<td>{summary.get('major_count', 0)}</td>"
        f"<td>{summary.get('moderate_count', 0)}</td>"
        f"<td>{summary.get('minor_count', 0)}</td>"
        "</tr>"
    )
  defect_rows = [f"<tr><td>{html_escape(code)}</td><td>{count}</td></tr>" for code, count in index.get("defect_frequency", {}).items()]
  category_rows = [f"<tr><td>{html_escape(cat)}</td><td>{count}</td></tr>" for cat, count in clusters.get("by_category", {}).items()]
  section_rows = []
  for section, stats in sorted(sections.items(), key=lambda kv: (-kv[1].get("defect_count", 0), kv[0])):
    section_rows.append(
        "<tr>"
        f"<td>{html_escape(section)}</td>"
        f"<td>{stats.get('defect_count', 0)}</td>"
        f"<td>{stats.get('critical', 0)}</td>"
        f"<td>{stats.get('major', 0)}</td>"
        f"<td>{stats.get('moderate', 0)}</td>"
        f"<td>{stats.get('minor', 0)}</td>"
        "</tr>"
    )
  return f"""<!doctype html>
<html lang="ru">
<head>
<meta charset="utf-8">
<title>Dissertation Intro QA Dashboard</title>
<style>
body {{ font-family: Arial, sans-serif; margin: 24px; line-height: 1.4; }}
h1, h2 {{ margin-top: 1.4em; }}
table {{ border-collapse: collapse; width: 100%; margin: 12px 0 24px 0; }}
th, td {{ border: 1px solid #ccc; padding: 8px; text-align: left; vertical-align: top; }}
th {{ background: #f3f3f3; }}
.grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 24px; }}
.card {{ border: 1px solid #ddd; padding: 16px; border-radius: 8px; }}
</style>
</head>
<body>
<h1>Dissertation Intro QA Dashboard</h1>
<div class="grid">
  <div class="card">
    <h2>Severity totals</h2>
    <ul>{''.join(f'<li>{html_escape(k)}: {v}</li>' for k, v in index.get('severity_frequency', {}).items())}</ul>
  </div>
  <div class="card">
    <h2>Defect categories</h2>
    <ul>{''.join(f'<li>{html_escape(k)}: {v}</li>' for k, v in clusters.get('by_category', {}).items())}</ul>
  </div>
</div>
<h2>Reports timeline</h2>
<table><thead><tr><th>Document</th><th>Date</th><th>Critical</th><th>Major</th><th>Moderate</th><th>Minor</th></tr></thead><tbody>{''.join(report_rows)}</tbody></table>
<h2>Top defect codes</h2>
<table><thead><tr><th>Code</th><th>Count</th></tr></thead><tbody>{''.join(defect_rows)}</tbody></table>
<h2>Defect categories</h2>
<table><thead><tr><th>Category</th><th>Count</th></tr></thead><tbody>{''.join(category_rows)}</tbody></table>
<h2>Section-wise analytics</h2>
<table><thead><tr><th>Section</th><th>Total</th><th>Critical</th><th>Major</th><th>Moderate</th><th>Minor</th></tr></thead><tbody>{''.join(section_rows)}</tbody></table>
</body>
</html>
"""


def gather_reports_from_inputs(inputs: List[Path]) -> List[Path]:
  reports = []
  for p in inputs:
    if p.is_dir():
      reports.extend(sorted(p.glob("*.json")))
    else:
      reports.append(p)
  return reports


def build_parser() -> argparse.ArgumentParser:
  parser = argparse.ArgumentParser(prog="intro-qa")
  sub = parser.add_subparsers(dest="cmd", required=True)

  p = sub.add_parser("init"); p.add_argument("target")
  p = sub.add_parser("scaffold-report"); p.add_argument("out"); p.add_argument("--document-id", default="intro_v1")
  p = sub.add_parser("scaffold-comparison"); p.add_argument("out"); p.add_argument("--from-version", default="v1"); p.add_argument("--to-version", default="v2")
  p = sub.add_parser("compare"); p.add_argument("report1"); p.add_argument("report2"); p.add_argument("--out", required=True); p.add_argument("--report-md")
  p = sub.add_parser("gate"); p.add_argument("report"); p.add_argument("--profiles", required=True); p.add_argument("--profile", required=True); p.add_argument("--out"); p.add_argument("--report-md")
  p = sub.add_parser("render-report"); p.add_argument("report"); p.add_argument("--out", required=True)
  p = sub.add_parser("render-comparison"); p.add_argument("comparison"); p.add_argument("--out", required=True)
  p = sub.add_parser("render-gate"); p.add_argument("gate"); p.add_argument("--out", required=True)
  p = sub.add_parser("pack-prompts"); p.add_argument("--prompt", required=True); p.add_argument("--standard", required=True); p.add_argument("--taxonomy", required=True); p.add_argument("--intro", required=True); p.add_argument("--out", required=True)
  p = sub.add_parser("repair-plan"); p.add_argument("report"); p.add_argument("--out", required=True)
  p = sub.add_parser("export-defects-csv"); p.add_argument("inputs", nargs="+"); p.add_argument("--out", required=True)
  p = sub.add_parser("trends"); p.add_argument("inputs", nargs="+"); p.add_argument("--out-json", required=True); p.add_argument("--out-md")
  p = sub.add_parser("validate-audit"); p.add_argument("report"); p.add_argument("--out")
  p = sub.add_parser("validate-comparison"); p.add_argument("comparison"); p.add_argument("--out")
  p = sub.add_parser("history-index"); p.add_argument("inputs", nargs="+"); p.add_argument("--out", required=True)
  p = sub.add_parser("dashboard"); p.add_argument("history_index"); p.add_argument("--out", required=True)
  p = sub.add_parser("defect-cluster"); p.add_argument("inputs", nargs="+"); p.add_argument("--out-json", required=True); p.add_argument("--out-md")
  p = sub.add_parser("section-analytics"); p.add_argument("inputs", nargs="+"); p.add_argument("--out-json", required=True); p.add_argument("--out-md")
  p = sub.add_parser("html-dashboard"); p.add_argument("inputs", nargs="+"); p.add_argument("--out", required=True); p.add_argument("--history-index"); p.add_argument("--clusters-json"); p.add_argument("--sections-json")
  return parser


def main(argv: List[str] | None = None) -> int:
  parser = build_parser()
  args = parser.parse_args(argv)

  if args.cmd == "init":
    scaffold_project(Path(args.target)); return 0
  if args.cmd == "scaffold-report":
    scaffold_report(Path(args.out), document_id=args.document_id); return 0
  if args.cmd == "scaffold-comparison":
    scaffold_comparison(Path(args.out), from_version=args.from_version, to_version=args.to_version); return 0
  if args.cmd == "compare":
    comp = compare_reports(read_json(Path(args.report1)), read_json(Path(args.report2)))
    write_json(Path(args.out), comp)
    if args.report_md: write_text(Path(args.report_md), render_comparison_md(comp))
    return 0
  if args.cmd == "gate":
    gate = run_gate(read_json(Path(args.report)), load_yaml_like_profiles(Path(args.profiles)), args.profile)
    if args.out: write_json(Path(args.out), gate)
    else: print(json.dumps(gate, ensure_ascii=False, indent=2))
    if args.report_md: write_text(Path(args.report_md), render_gate_md(gate))
    return 0
  if args.cmd == "render-report":
    write_text(Path(args.out), render_report_md(read_json(Path(args.report)))); return 0
  if args.cmd == "render-comparison":
    write_text(Path(args.out), render_comparison_md(read_json(Path(args.comparison)))); return 0
  if args.cmd == "render-gate":
    write_text(Path(args.out), render_gate_md(read_json(Path(args.gate)))); return 0
  if args.cmd == "pack-prompts":
    pack_prompts(Path(args.prompt), Path(args.standard), Path(args.taxonomy), Path(args.intro), Path(args.out)); return 0
  if args.cmd == "repair-plan":
    write_text(Path(args.out), generate_repair_plan(read_json(Path(args.report)))); return 0
  if args.cmd == "export-defects-csv":
    export_defects_csv([Path(p) for p in args.inputs], Path(args.out)); return 0
  if args.cmd == "trends":
    reports = gather_reports_from_inputs([Path(p) for p in args.inputs])
    summary = trend_summary(reports)
    write_json(Path(args.out_json), summary)
    if args.out_md: write_text(Path(args.out_md), trends_markdown(summary))
    return 0
  if args.cmd == "validate-audit":
    result = validate_audit(read_json(Path(args.report)))
    if args.out: write_json(Path(args.out), result)
    else: print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0
  if args.cmd == "validate-comparison":
    result = validate_comparison(read_json(Path(args.comparison)))
    if args.out: write_json(Path(args.out), result)
    else: print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0
  if args.cmd == "history-index":
    write_json(Path(args.out), history_index(gather_reports_from_inputs([Path(p) for p in args.inputs]))); return 0
  if args.cmd == "dashboard":
    write_text(Path(args.out), render_dashboard_md(read_json(Path(args.history_index)))); return 0
  if args.cmd == "defect-cluster":
    data = defect_clusters(gather_reports_from_inputs([Path(p) for p in args.inputs]))
    write_json(Path(args.out_json), data)
    if args.out_md: write_text(Path(args.out_md), render_cluster_md(data))
    return 0
  if args.cmd == "section-analytics":
    data = section_analytics(gather_reports_from_inputs([Path(p) for p in args.inputs]))
    write_json(Path(args.out_json), data)
    if args.out_md: write_text(Path(args.out_md), render_section_analytics_md(data))
    return 0
  if args.cmd == "html-dashboard":
    reports = gather_reports_from_inputs([Path(p) for p in args.inputs])
    index = read_json(Path(args.history_index)) if args.history_index else history_index(reports)
    clusters = read_json(Path(args.clusters_json)) if args.clusters_json else defect_clusters(reports)
    sections = read_json(Path(args.sections_json)) if args.sections_json else section_analytics(reports)
    write_text(Path(args.out), render_html_dashboard(index, clusters, sections))
    return 0

  parser.error("Unknown command")
  return 2


if __name__ == "__main__":
  sys.exit(main())
