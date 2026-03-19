# Dissertation Introduction QA CLI Starter

Локальный CLI-каркас для QA-пайплайна введений диссертаций.

## Что уже умеет

- `intro-qa init` — создать starter-структуру проекта
- `intro-qa scaffold-report` — создать шаблон audit JSON
- `intro-qa scaffold-comparison` — создать шаблон comparison JSON
- `intro-qa compare` — сравнить два audit JSON отчета
- `intro-qa gate` — проверить audit report по acceptance profile YAML
- `intro-qa render-report` — рендер audit JSON → Markdown
- `intro-qa render-comparison` — рендер comparison JSON → Markdown
- `intro-qa render-gate` — рендер gate JSON → Markdown
- `intro-qa repair-plan` — построить Markdown-план переработки из audit JSON
- `intro-qa pack-prompts` — собрать единый LLM input bundle
- `intro-qa export-defects-csv` — выгрузить defect rows из одного или нескольких audit JSON в CSV
- `intro-qa trends` — собрать сводку трендов по нескольким audit JSON

## Phase 4 additions

В этой версии добавлены:

- JSON schemas в `schemas/`
- sample Markdown templates в `templates/`
- CSV export дефектов
- trend summary across multiple reports

## Быстрый старт

### 1. Инициализация starter-репозитория

```bash
python intro_qa.py init ./my_intro_qa
```

### 2. Создание шаблона audit report

```bash
python intro_qa.py scaffold-report --out ./my_intro_qa/reports/audit_v1.json --document-id intro_v1
```

### 3. Gate check

```bash
python intro_qa.py gate \
  ./my_intro_qa/reports/audit_v1.json \
  --profiles ./my_intro_qa/configs/acceptance_profiles.yaml \
  --profile strict \
  --out ./my_intro_qa/reports/gate_v1.json
```

### 4. Render audit report to Markdown

```bash
python intro_qa.py render-report \
  ./my_intro_qa/reports/audit_v1.json \
  --out ./my_intro_qa/reports/audit_v1.md
```

### 5. Compare two versions

```bash
python intro_qa.py compare \
  ./my_intro_qa/reports/audit_v1.json \
  ./my_intro_qa/reports/audit_v2.json \
  --out ./my_intro_qa/comparisons/v1_v2.json
```

### 6. Render comparison to Markdown

```bash
python intro_qa.py render-comparison \
  ./my_intro_qa/comparisons/v1_v2.json \
  --out ./my_intro_qa/comparisons/v1_v2.md
```

### 7. Build repair plan

```bash
python intro_qa.py repair-plan \
  ./my_intro_qa/reports/audit_v2.json \
  --out ./my_intro_qa/repair/repair_plan_v2.md
```

### 8. Pack prompt bundle for next LLM run

```bash
python intro_qa.py pack-prompts \
  --prompt ./my_intro_qa/prompts/audit_prompt.md \
  --standard ./my_intro_qa/standards/evaluation_standard.md \
  --taxonomy ./my_intro_qa/standards/defect_taxonomy.md \
  --intro ./my_intro_qa/inputs/intro_example.md \
  --out ./my_intro_qa/reports/audit_bundle_v1.md
```

### 9. Export defects to CSV

```bash
python intro_qa.py export-defects-csv \
  ./my_intro_qa/reports/audit_v1.json \
  ./my_intro_qa/reports/audit_v2.json \
  --out ./my_intro_qa/exports/defects.csv
```

### 10. Build trend summary

```bash
python intro_qa.py trends \
  ./my_intro_qa/reports/audit_v1.json \
  ./my_intro_qa/reports/audit_v2.json \
  --out-json ./my_intro_qa/trends/summary.json \
  --out-md ./my_intro_qa/trends/summary.md
```

## Рекомендуемый workflow

1. LLM делает audit.
2. Вы сохраняете audit JSON.
3. `render-report` делает читаемый Markdown.
4. `gate` проверяет версию по профилю.
5. `repair-plan` превращает defect map в agenda переработки.
6. После новой версии `compare` и `trends` показывают динамику.
7. `export-defects-csv` позволяет агрегировать дефекты и анализировать их вне CLI.

## Ограничения

CLI не вызывает LLM сам по себе. Он управляет артефактами вокруг LLM-аудита:

- scaffolding
- JSON/Markdown reports
- comparison
- gate checks
- CSV export
- trend summaries

## Suggested next step

Следующий логичный слой — Phase 5:

- semi-structured validation helpers
- stronger schema-aware report validation
- defect frequency dashboards
- optional JSON merge / history index
