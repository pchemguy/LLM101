# Dissertation Introduction QA CLI Starter

Локальный CLI-каркас для QA-пайплайна введений диссертаций.

## Команды

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

## Что уже умеет

### Phase 1
- scaffold структуры проекта
- шаблоны audit/comparison JSON
- compare двух audit reports
- gate checks по acceptance profile

### Phase 2
- render audit JSON → Markdown
- render comparison JSON → Markdown
- pack prompt + standard + taxonomy + intro в единый bundle

### Phase 3
- render gate JSON → Markdown
- generate repair plan from defect codes and severities

## Примеры

### Инициализация

```bash
intro-qa init ./my_intro_qa
```

### Создание шаблона audit report

```bash
intro-qa scaffold-report --out reports/audit_v1.json --document-id intro_v1
```

### Gate check

```bash
intro-qa gate \
  reports/audit_v1.json \
  --profiles configs/acceptance_profiles.yaml \
  --profile supervisor \
  --out reports/gate_v1.json
```

### Рендер audit report

```bash
intro-qa render-report reports/audit_v1.json --out reports/audit_v1.md
```

### Рендер comparison report

```bash
intro-qa compare reports/audit_v1.json reports/audit_v2.json --out comparisons/v1_v2.json
intro-qa render-comparison comparisons/v1_v2.json --out comparisons/v1_v2.md
```

### Рендер gate report

```bash
intro-qa render-gate reports/gate_v1.json --out reports/gate_v1.md
```

### Сборка bundle для LLM

```bash
intro-qa pack-prompts \
  --prompt prompts/audit_prompt.md \
  --standard standards/evaluation_standard.md \
  --taxonomy standards/defect_taxonomy.md \
  --intro inputs/intro_v2.md \
  --out bundles/audit_bundle_v2.md
```

### Генерация repair plan

```bash
intro-qa repair-plan reports/audit_v2.json --out repair/repair_plan_v2.md
```

## Важное ограничение

CLI не вызывает LLM автоматически. Он обслуживает workflow вокруг результатов,
которые вы получаете от LLM-аудита.
