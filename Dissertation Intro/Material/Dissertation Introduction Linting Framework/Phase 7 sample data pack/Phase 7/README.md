# Dissertation Intro QA CLI — Phase 7

Phase 7 adds:

- sample data pack
- demo audit reports
- end-to-end smoke test workflow
- ready-made example commands for the full QA cycle

## Included sample assets

- `sample_data/inputs/intro_demo_v1.md`
- `sample_data/inputs/intro_demo_v2.md`
- `sample_data/reports/audit_demo_v1.json`
- `sample_data/reports/audit_demo_v2.json`
- `sample_data/comparisons/compare_demo_v1_v2.json`
- `tests/smoke_test_workflow.md`

## End-to-end smoke test

### 1. Render reports
```bash
python intro_qa.py render-report sample_data/reports/audit_demo_v1.json --out sample_data/reports/audit_demo_v1.md
python intro_qa.py render-report sample_data/reports/audit_demo_v2.json --out sample_data/reports/audit_demo_v2.md
```

### 2. Compare demo versions
```bash
python intro_qa.py compare   sample_data/reports/audit_demo_v1.json   sample_data/reports/audit_demo_v2.json   --out sample_data/comparisons/compare_demo_v1_v2.generated.json   --report-md sample_data/comparisons/compare_demo_v1_v2.generated.md
```

### 3. Trends / history
```bash
python intro_qa.py trends sample_data/reports/   --out-json sample_data/history/trends.json   --out-md sample_data/history/trends.md

python intro_qa.py history-index sample_data/reports/   --out sample_data/history/index.json
```

### 4. Clusters / sections
```bash
python intro_qa.py defect-cluster sample_data/reports/   --out-json sample_data/history/defect_clusters.json   --out-md sample_data/history/defect_clusters.md

python intro_qa.py section-analytics sample_data/reports/   --out-json sample_data/history/section_analytics.json   --out-md sample_data/history/section_analytics.md
```

### 5. HTML dashboard
```bash
python intro_qa.py html-dashboard sample_data/reports/   --out sample_data/dashboard/dashboard.html
```
