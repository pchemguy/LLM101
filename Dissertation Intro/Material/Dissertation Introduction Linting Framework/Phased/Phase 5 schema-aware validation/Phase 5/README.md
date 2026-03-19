# Dissertation Introduction QA CLI Starter

This starter provides a lightweight local CLI for the dissertation introduction QA workflow.

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
- intro-qa validate-audit
- intro-qa validate-comparison
- intro-qa history-index
- intro-qa dashboard

The CLI does not call an LLM directly. It helps you manage:
- project scaffolding
- audit reports
- comparison reports
- acceptance gate checks
- Markdown rendering
- defect exports
- trend summaries across multiple reports
- schema-aware validation of audit/comparison JSON
- history indexing across many report versions
- dashboard scaffolding for defect frequency review

## Quick examples

Initialize a starter project:

```bash
intro-qa init ./dissertation_intro_qa_project
```

Create an empty audit JSON:

```bash
intro-qa scaffold-report --out reports/audit_v1.json --document-id intro_v1
```

Compare two audit reports:

```bash
intro-qa compare reports/audit_v1.json reports/audit_v2.json --out comparisons/v1_v2.json
```

Check an acceptance gate:

```bash
intro-qa gate reports/audit_v2.json \
  --profiles configs/acceptance_profiles.yaml \
  --profile strict \
  --out reports/gate_v2.json
```

Render Markdown outputs:

```bash
intro-qa render-report reports/audit_v2.json --out reports/audit_v2.md
intro-qa render-comparison comparisons/v1_v2.json --out comparisons/v1_v2.md
intro-qa render-gate reports/gate_v2.json --out reports/gate_v2.md
```

Build a repair plan:

```bash
intro-qa repair-plan reports/audit_v2.json --out repair/repair_plan_v2.md
```

Bundle prompt artifacts for the next LLM run:

```bash
intro-qa pack-prompts \
  --prompt prompts/audit_prompt.md \
  --standard standards/evaluation_standard.md \
  --taxonomy standards/defect_taxonomy.md \
  --intro inputs/intro_v2.md \
  --out bundles/audit_bundle_v2.md
```

Export defects to CSV and summarize trends:

```bash
intro-qa export-defects-csv reports/audit_v1.json reports/audit_v2.json --out exports/defects.csv
intro-qa trends reports/audit_v1.json reports/audit_v2.json --out-json trends/summary.json --out-md trends/summary.md
```

Phase 5 additions:

```bash
intro-qa validate-audit reports/audit_v2.json --out reports/validate_audit_v2.json
intro-qa validate-comparison comparisons/v1_v2.json --out comparisons/validate_v1_v2.json
intro-qa history-index reports/audit_v1.json reports/audit_v2.json --out-json history/index.json --out-md dashboards/history_dashboard.md
intro-qa dashboard history/index.json --out dashboards/dashboard.md
```
