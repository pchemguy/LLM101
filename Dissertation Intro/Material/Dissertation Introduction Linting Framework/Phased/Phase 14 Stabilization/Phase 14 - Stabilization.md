# Phase 14 — Stabilization / Cleanup Pass (Design)

## 0. Главный принцип

Цель не «добавить», а:

> **сократить энтропию системы и зафиксировать контракт**

Если коротко:

* меньше вариативности
* меньше implicit поведения
* больше формализации

---

## 1. Жёсткая нормализация artifact model

### Проблема сейчас

У тебя уже есть:

* audit JSON
* comparison JSON
* gate JSON
* benchmark summary JSON
* registry JSON
* manifest JSON

Но:

* нет строгого единого meta-слоя
* нет versioning на уровне схем
* нет guarantee совместимости

---

### Решение: ввести `artifact envelope`

#### Стандартная оболочка (обязательно для всех JSON)

```json
{
  "artifact_type": "audit_report",
  "schema_version": "1.0.0",
  "generated_at": "...",
  "producer": {
    "tool": "intro_qa",
    "version": "0.14.0"
  },
  "payload": { ... }
}
```

---

### Что это даёт

* единый контракт для всех CLI-утилит
* возможность миграций
* возможность cross-tool validation

---

## 2. Schema enforcement (не “optional”)

### Сейчас

* есть «validation helpers»
* но они не являются обязательными

### Должно быть

Любая команда:

```bash
render / compare / gate / scorer / registry
```

должна:

> ❗ падать при несоответствии schema

---

### Минимум:

* `schemas/` → canonical JSON schemas
* `validate-*` → используется внутри всех команд
* fail-fast поведение

---

## 3. Удаление дублирования логики

### Симптом

У тебя сейчас:

* render функции
* json IO
* aggregation
* markdown generation

— размазаны по разным скриптам

---

### Решение: internal core module

Ввести:

```
core/
  io.py
  render.py
  schema.py
  aggregation.py
```

---

### Эффект

* исчезает copy-paste логика
* легче изменять формат отчётов
* единая точка контроля

---

## 4. Canonical defect taxonomy locking

### Сейчас

taxonomy есть, но:

* не зафиксирован как immutable reference
* может «поплыть» между версиями

---

### Нужно

```json
{
  "taxonomy_version": "1.0.0",
  "codes": {
    "GAP-01": {...},
    "NOV-03": {...}
  }
}
```

---

### И правило:

> audit JSON всегда указывает taxonomy_version

---

## 5. Deterministic outputs

### Проблема

LLM-пайплайн inherently stochastic, но:

* твои CLI outputs должны быть deterministic

---

### Требование:

* сортировка:

  * defect codes
  * sections
  * runs
* фиксированный порядок полей
* отсутствие случайных UUID

---

### Это критично для:

* regression testing
* diff analysis
* Git history

---

## 6. CLI contract stabilization

### Сейчас

CLI вырос organically:

* много команд
* не всегда единый стиль аргументов

---

### Нужно унифицировать:

#### Общие флаги:

```bash
--in-json
--out-json
--out-md
--schema-check strict|warn|off
```

---

### И правило:

> каждая команда:

* принимает input явно
* пишет output явно
* не имеет скрытых side effects

---

## 7. Error model (сейчас отсутствует)

### Сейчас

ошибки:

* print + exit
* без типизации

---

### Нужно:

#### Классы ошибок:

* `SchemaError`
* `IOError`
* `ContractViolation`
* `MissingArtifactError`

---

### И поведение:

```bash
exit codes:
0 = ok
1 = user error
2 = schema error
3 = internal error
```

---

## 8. Test layer (не smoke, а real)

### Сейчас

есть:

* smoke tests (документы)

нет:

* автоматических тестов

---

### Минимум:

* pytest
* tests/

  * test_schema_validation.py
  * test_compare_logic.py
  * test_scorer.py
  * test_registry.py

---

### Критично:

> regression scorer должен быть тестируемым без LLM

---

## 9. Config layer

### Сейчас

параметры размазаны по CLI

---

### Нужно:

```yaml
config/default.yaml
```

```yaml
schema_validation: strict
sorting: deterministic
taxonomy_version: 1.0.0
```

---

### CLI:

```bash
--config config/default.yaml
```

---

## 10. Repository cleanup

### У тебя сейчас

* phase artifacts
* дублирование README
* тесты как markdown

---

### Нужно:

#### Финальная структура:

```
src/
  intro_qa/
    core/
    cli/

schemas/
configs/
docs/
tests/
benchmark/
```

---

## 11. Breaking change freeze

После Phase 14:

> ❗ заморозка контрактов

* JSON formats
* CLI commands
* taxonomy

---

## 12. Что НЕ делать на этом этапе

Критично:

❌ не добавлять:

* новые команды
* новые типы отчётов
* новые уровни abstraction

---

## 13. Результат Phase 14

Если сделать правильно, ты получаешь:

### До:

* мощный, но “живой” прототип

### После:

* **контрактно-стабильную систему**

---

## 14. Ключевой инсайт

Сейчас у тебя система:

> feature-complete, но не invariant-safe

Phase 14 делает:

> invariant-safe → foundation для production или публикации

---

## Если продолжать дальше

После stabilization есть два осмысленных направления:

### A. Integration

* реальный LLM backend
* batch execution
* async runs

### B. Productization

* UI
* API
* web dashboard

---
