# Dissertation Intro QA CLI

Phase 6 starter for QA/audit workflow of dissertation introductions.

## New in Phase 6

- `defect-cluster` — clustering defects by section, severity, and taxonomy category
- `section-analytics` — section-wise analytics across one or more audit reports
- `html-dashboard` — baseline HTML dashboard scaffold from audit reports or precomputed JSON

## Example commands

### Defect clustering
```bash
python intro_qa.py defect-cluster reports/ \
  --out-json history/defect_clusters.json \
  --out-md history/defect_clusters.md
```

### Section-wise analytics
```bash
python intro_qa.py section-analytics reports/ \
  --out-json history/section_analytics.json \
  --out-md history/section_analytics.md
```

### Baseline HTML dashboard
```bash
python intro_qa.py html-dashboard reports/ --out dashboard/dashboard.html
```

Or with precomputed sources:
```bash
python intro_qa.py html-dashboard reports/ \
  --history-index history/index.json \
  --clusters-json history/defect_clusters.json \
  --sections-json history/section_analytics.json \
  --out dashboard/dashboard.html
```
