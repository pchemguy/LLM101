# ARCHITECTURE

## 1. Purpose

The system is designed as a layered QA pipeline for dissertation introduction analysis.

Its central object is the dissertation introduction treated as a structured
research specification that can be audited through:
- extraction
- linting
- scoring
- defect coding
- revision planning
- benchmarking

## 2. Main layers

### Layer A — Core audit tools
Primary script:
- `intro_qa.py`

Functions:
- scaffold reports
- compare audits
- gate checks
- render markdown reports
- pack prompt bundles
- export defects
- history and dashboard generation
- defect clustering
- section analytics

### Layer B — Benchmark evaluation
Primary script:
- `benchmark_scorer.py`

Functions:
- compare expected defect targets with actual audit outputs
- compute per-case recall / precision
- generate run summaries
- build simple leaderboards

### Layer C — Benchmark orchestration
Primary script:
- `benchmark_orchestrator.py`

Functions:
- discover benchmark cases
- create manifests
- create workflow plans
- aggregate regression summaries

### Layer D — Registry and project management
Primary script:
- `benchmark_registry.py`

Functions:
- create sessions
- register runs
- build run registry
- build consolidated project dashboard

### Layer E — Packaging and release
Primary script:
- `benchmark_packager.py`

Functions:
- bootstrap new projects
- generate demo plans
- create release bundles

## 3. Artifact model

The system works with the following major artifact classes:

- introduction text
- audit report JSON
- comparison JSON
- gate JSON
- benchmark expected JSON
- benchmark run summary JSON
- session JSON
- registry JSON
- release manifest JSON

Markdown and HTML outputs are treated as renderings of structured artifacts.

## 4. Flow model

Typical flow:

1. Introduction is audited.
2. Audit report is rendered and analyzed.
3. Defects are repaired and re-audited.
4. Reports are compared across versions.
5. Multiple runs can be benchmarked.
6. Benchmark runs can be grouped into sessions.
7. Sessions can be aggregated into registries and dashboards.
8. Entire project can be bundled for release.

## 5. Design philosophy

The stack is intentionally:
- modular
- artifact-first
- machine-readable
- compatible with LLM-in-the-loop workflows
- suitable for iterative refinement

## 6. Current limitation

The stack orchestrates and evaluates artifacts but does not directly call remote LLMs.
LLM execution remains external to preserve portability and model-agnostic use.
