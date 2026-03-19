# Dissertation Introduction QA CLI Starter

This package provides a lightweight local CLI for the dissertation introduction QA workflow.

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
intro-qa gate reports/audit_v2.json   --profiles configs/acceptance_profiles.yaml   --profile strict   --out reports/gate_v2.json
```

### Render audit JSON to Markdown

```bash
intro-qa render-report reports/audit_v2.json --out reports/audit_v2.md
```

### Render comparison JSON to Markdown

```bash
intro-qa render-comparison comparisons/v1_v2.json --out comparisons/v1_v2.md
```

### Bundle LLM input pack

```bash
intro-qa pack-prompts   --prompt prompts/audit_prompt.md   --standard standards/evaluation_standard.md   --taxonomy standards/defect_taxonomy.md   --intro inputs/intro_v2.md   --out llm_bundle_v2.md
```

## Scope

This CLI does **not** call an LLM directly. It is a local orchestration and artifact-management starter for:

- audit scaffolding
- comparison scaffolding
- acceptance gate checks
- JSON -> Markdown rendering
- packed LLM input bundles
- repo initialization

It is intended as Phase 2 infrastructure for a larger dissertation intro QA pipeline.
