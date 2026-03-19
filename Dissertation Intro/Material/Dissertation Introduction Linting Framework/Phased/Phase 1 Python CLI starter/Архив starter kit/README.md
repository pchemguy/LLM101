# Dissertation Introduction QA CLI Starter

This package provides a lightweight local CLI for the dissertation introduction
QA workflow.

## Install

```bash
pip install -e .
```

## Commands

### Initialize starter repo

```bash
intro-qa init ./dissertation_intro_qa_project
```

### Create blank audit report scaffold

```bash
intro-qa scaffold-report --out reports/audit_v1.json --document-id intro_v1
```

### Compare two audit reports

```bash
intro-qa compare reports/audit_v1.json reports/audit_v2.json --out comparisons/v1_v2.json
```

### Check acceptance gate

```bash
intro-qa gate reports/audit_v2.json \
  --profiles configs/acceptance_profiles.yaml \
  --profile strict \
  --out reports/gate_v2.json
```

## Scope

This CLI does **not** call an LLM directly. It is a local orchestration and
artifact-management starter for:

- audit scaffolding
- comparison scaffolding
- acceptance gate checks
- repo initialization

It is intended as Phase 1 infrastructure for a larger dissertation intro QA
pipeline.
