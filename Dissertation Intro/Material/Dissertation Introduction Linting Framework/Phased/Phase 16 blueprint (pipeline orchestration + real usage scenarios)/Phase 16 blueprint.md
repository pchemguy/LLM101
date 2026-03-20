# Phase 16 — Integration Layer Blueprint

## 0. Цель фазы (строго)

Перевести систему из:

```text
CLI utilities → связанный инструмент
```

в:

```text
pipeline system → воспроизводимый QA workflow
```

---

# 1. Архитектурная модель

## 1.1 Основная идея

Вводим **pipeline orchestration layer**, который управляет:

* последовательностью стадий
* контрактами между ними
* хранением артефактов

---

## 1.2 Канонический pipeline

```text
INPUT
  ↓
AUDIT
  ↓
VALIDATION (schema + taxonomy)
  ↓
GATE
  ↓
REPAIR PLAN (optional)
  ↓
COMPARISON (optional)
  ↓
HISTORY UPDATE
  ↓
DASHBOARD
```

---

## 1.3 Формализация стадий

| Stage         | Input         | Output            | Contract-critical |
| ------------- | ------------- | ----------------- | ----------------- |
| audit         | raw text      | audit_report      | YES               |
| validate      | audit_report  | validated_report  | YES               |
| gate          | audit_report  | gate_result       | YES               |
| repair-plan   | audit_report  | repair_plan_md    | NO (presentation) |
| compare       | 2 reports     | comparison_report | YES               |
| history-index | N reports     | history_index     | YES               |
| dashboard     | history_index | dashboard_md      | NO                |

---

# 2. Новый слой: Orchestrator

## 2.1 Новый модуль

```text
src/dissertation_intro_qa/pipeline/orchestrator.py
```

---

## 2.2 Интерфейс (ядро)

```python
class PipelineRunner:
  def run(self, config: PipelineConfig) -> PipelineResult:
    ...
```

---

## 2.3 PipelineConfig

```yaml
input:
  path: intro.txt
  document_id: intro_v3

pipeline:
  steps:
    - audit
    - validate
    - gate
    - repair-plan
    - history-index
    - dashboard

settings:
  strict_mode: true
  taxonomy: configs/defect_taxonomy.json
  profiles: configs/gate_profiles.yaml

outputs:
  base_dir: ./runs/
```

---

## 3. Execution Model

## 3.1 Run = isolated execution unit

Каждый запуск:

```text
runs/
  run_2026-03-20_001/
    audit.json
    gate.json
    comparison.json
    repair_plan.md
    history.json
    dashboard.md
    metadata.json
```

---

## 3.2 Metadata (обязательно)

```json
{
  "run_id": "run_2026-03-20_001",
  "document_id": "intro_v3",
  "timestamp": "...",
  "pipeline_steps": [...],
  "strict_mode": true,
  "taxonomy_version": "1.0.0"
}
```

---

# 4. CLI верхнего уровня

## 4.1 Новый CLI

```bash
intro-pipeline run config.yaml
```

---

## 4.2 Поведение

* выполняет ВСЕ стадии
* валидирует каждый переход
* сохраняет ВСЕ артефакты
* возвращает exit code по итогам gate

---

## 4.3 Exit logic

```text
если gate passed → exit 0
если gate failed → exit 1
если ошибка → exit 3
```

---

# 5. Контракт между стадиями

## 5.1 Жёсткое правило

```text
Каждый шаг принимает ТОЛЬКО валидированный artifact
```

---

## 5.2 Enforcement

После каждого шага:

```python
assert_valid_artifact(...)
validate_taxonomy(...)
```

---

# 6. Реальные сценарии использования

## 6.1 Scenario A — одиночная проверка

```bash
intro-pipeline run single.yaml
```

→ выход:

* audit
* gate
* repair plan

---

## 6.2 Scenario B — итеративное улучшение

```text
v1 → audit → fix → v2 → audit → compare
```

Pipeline:

```yaml
steps:
  - audit
  - compare
  - gate
```

---

## 6.3 Scenario C — мониторинг кафедры

```text
N диссертаций → history → dashboard
```

---

## 6.4 Scenario D — CI/CD

```bash
intro-pipeline run ci.yaml
```

→ fail build if:

* critical defects > 0
* GOST incomplete
* score < threshold

---

# 7. Storage Strategy

## 7.1 Immutable runs

```text
runs/ — append-only
```

НИКОГДА не перезаписывать.

---

## 7.2 Aggregation

```text
history_index = computed, not stored manually
```

---

# 8. Расширение (но не сейчас)

Заложить точки расширения:

* parallel execution (future)
* remote storage (S3 / DB)
* UI layer

Но не реализовывать в Phase 16.

---

# 9. Основные риски (и как ты их избегаешь)

### Риск 1 — “CLI spaghetti”

→ решается orchestrator

### Риск 2 — “artifact drift”

→ strict validation after each stage

### Риск 3 — “non reproducibility”

→ deterministic sorting + immutable runs

### Риск 4 — “manual misuse”

→ pipeline config + single entrypoint

---

# 10. Definition of Done (Phase 16)

Система считается интегрированной, если:

* [ ] можно выполнить полный pipeline одной командой
* [ ] все артефакты сохраняются
* [ ] exit code отражает результат gate
* [ ] результаты воспроизводимы
* [ ] история строится автоматически

---

# Итог

Ты переходишь из:

```text
набор CLI инструментов
```

в:

```text
систему контроля качества научных текстов
```

---
