# Phase 14 — Implementation Plan + Concrete Refactoring Diff

Ниже — уже не концепт, а **практический план стабилизации**, ориентированный на превращение текущего Phase 13 stack в **контрактно-стабильный package**.

Я разделю это на пять частей:

1. **Что именно надо изменить**
2. **Что удалить / заморозить**
3. **Как должна выглядеть новая структура**
4. **Пошаговый migration plan**
5. **Definition of Done для stabilization pass**

---

## 1. Главные цели Phase 14

Phase 14 должен решить четыре системные проблемы:

### 1.1. Разрозненные контракты артефактов

Сейчас JSON-артефакты существуют, но как семейство слабо связанных форматов.
Нужно сделать их **формальной системой типов**.

### 1.2. Копипастная логика по нескольким скриптам

Сейчас есть повторяющиеся куски:

* `read_json`
* `write_json`
* markdown renderers
* aggregation helpers
* simple validation logic

Это нужно централизовать.

### 1.3. Отсутствие жесткого enforcement

Validation есть, но не встроен как обязательный барьер.
Нужно сделать:

> invalid artifact ⇒ fail-fast

### 1.4. Отсутствие единого production-style layout

Сейчас проект still phase-driven.
Нужно перейти от “слоя артефактов по фазам” к **устойчивому package layout**.

---

## 2. High-level refactoring diff

### Сейчас условно

```text
project/
  intro_qa.py
  benchmark_scorer.py
  benchmark_orchestrator.py
  benchmark_registry.py
  benchmark_packager.py
  ...
```

### После Phase 14

```text
project/
  pyproject.toml
  README.md
  CHANGELOG.md

  src/
    dissertation_intro_qa/
      __init__.py
      version.py

      core/
        io.py
        schema.py
        envelope.py
        taxonomy.py
        errors.py
        render.py
        aggregation.py
        paths.py

      cli/
        intro_qa.py
        benchmark_scorer.py
        benchmark_orchestrator.py
        benchmark_registry.py
        benchmark_packager.py

      artifacts/
        audit.py
        comparison.py
        gate.py
        benchmark.py
        registry.py
        release.py

  schemas/
    audit_report.schema.json
    comparison_report.schema.json
    gate_result.schema.json
    benchmark_summary.schema.json
    run_manifest.schema.json
    session.schema.json
    registry.schema.json
    release_manifest.schema.json
    artifact_envelope.schema.json

  configs/
    default.yaml

  docs/
  tests/
  benchmark/
```

Это уже production-like layout.

---

## 3. Concrete changes by subsystem

### 3.1. Artifact envelope

#### Добавить

Файл:

```text
src/dissertation_intro_qa/core/envelope.py
```

#### С функциями:

* `wrap_artifact(artifact_type, payload, schema_version, producer)`
* `unwrap_artifact(data, expected_type=None)`
* `is_enveloped(data)`

#### Целевой формат

```json
{
  "artifact_type": "audit_report",
  "schema_version": "1.0.0",
  "generated_at": "2026-03-19T12:00:00Z",
  "producer": {
    "tool": "intro_qa",
    "version": "0.14.0"
  },
  "payload": { ... }
}
```

#### Что изменить

Все JSON outputs должны перейти с flat structure на:

* envelope
* payload inside envelope

#### Что сломается

Да, это **breaking change**.
Но если делать stabilization, это как раз последний допустимый момент.

---

### 3.2. Canonical schemas

#### Добавить

Все схемы в `schemas/`.

Обязательный набор:

* `artifact_envelope.schema.json`
* `audit_report.schema.json`
* `comparison_report.schema.json`
* `gate_result.schema.json`
* `benchmark_summary.schema.json`
* `leaderboard.schema.json`
* `run_manifest.schema.json`
* `workflow_plan.schema.json`
* `session.schema.json`
* `run_registry.schema.json`
* `project_dashboard.schema.json`
* `release_manifest.schema.json`

#### Что изменить

Validation helpers больше не должны быть ad hoc.
Они должны использовать canonical mapping:

```python
SCHEMA_MAP = {
    "audit_report": "schemas/audit_report.schema.json",
    ...
}
```

---

### 3.3. Strict validation layer

#### Добавить

```text
src/dissertation_intro_qa/core/schema.py
```

#### Функции:

* `load_schema(schema_name)`
* `validate_payload(payload, schema_name)`
* `validate_artifact(artifact)`
* `assert_valid_artifact(...)`

#### Важное решение

Если не хочешь пока тащить `jsonschema`, можно сделать Phase 14A и 14B:

#### Phase 14A

* strict custom validator

#### Phase 14B

* migrate to `jsonschema`

Но лучше сразу перейти на `jsonschema`.

---

### 3.4. Core error model

#### Добавить

```text
src/dissertation_intro_qa/core/errors.py
```

#### Минимум классов:

```python
class IntroQAError(Exception): ...
class SchemaError(IntroQAError): ...
class ArtifactTypeError(IntroQAError): ...
class MissingArtifactError(IntroQAError): ...
class ContractViolation(IntroQAError): ...
class ConfigurationError(IntroQAError): ...
```

#### Зачем

Чтобы CLI не разваливался на “random ValueError + print”.

---

### 3.5. Core IO layer

#### Добавить

```text
src/dissertation_intro_qa/core/io.py
```

#### Вынести туда:

* `read_json`
* `write_json`
* `write_text`
* deterministic JSON dumping
* safe directory creation

#### Правило

Любой файл пишется через один и тот же IO слой.

---

### 3.6. Deterministic serialization

#### Изменить

Все JSON dump делать через единый helper:

```python
json.dump(..., ensure_ascii=False, indent=2, sort_keys=True)
```

#### И дополнительно

Перед записью:

* сортировать defect lists
* сортировать sections
* сортировать runs
* сортировать leaderboard rows по фиксированному ключу

#### Причина

Нужна стабильность для:

* git diff
* regression
* benchmark comparison

---

### 3.7. Taxonomy freeze

#### Добавить

Machine-readable taxonomy:

```text
configs/defect_taxonomy.json
```

или

```text
schemas/defect_taxonomy.json
```

#### Формат

```json
{
  "taxonomy_version": "1.0.0",
  "groups": {
    "GAP": {
      "GAP-01": {
        "title": "...",
        "default_severity_floor": "critical"
      }
    }
  }
}
```

#### Изменить

Все audit artifacts должны указывать:

```json
"taxonomy_version": "1.0.0"
```

---

### 3.8. CLI normalization

#### Сейчас проблема

Аргументы немного разношерстны.

#### Нужно ввести единый convention

Для всех команд:

* input path args максимально явные
* `--out-json`
* `--out-md`
* `--schema-check {strict,warn,off}`
* `--config ...`

#### Пример

Вместо полу-случайного сочетания:

```bash
compare report1 report2 --out ...
```

можно оставить positional, но строго документировать как canonical.

Главное — чтобы все команды:

* имели одинаковую модель output
* уважали schema validation policy

---

### 3.9. Config layer

#### Добавить

```text
configs/default.yaml
```

#### Пример

```yaml
schema_validation: strict
taxonomy_version: 1.0.0
json_sort_keys: true
markdown_render_style: standard
fail_on_unknown_artifact_type: true
```

#### Плюс helper

```text
src/dissertation_intro_qa/core/config.py
```

---

### 3.10. Render layer centralization

#### Сейчас

Renderer functions раскиданы.

#### Нужно

```text
src/dissertation_intro_qa/core/render.py
```

#### Вынести туда:

* `render_audit_md`
* `render_comparison_md`
* `render_gate_md`
* `render_summary_md`
* `render_registry_md`
* `render_dashboard_md`

---

### 3.11. Aggregation layer centralization

#### Сейчас

Aggregation логика частично в разных скриптах.

#### Нужно

```text
src/dissertation_intro_qa/core/aggregation.py
```

#### Вынести туда:

* report compare
* trend summary
* defect clustering
* section analytics
* benchmark aggregate
* leaderboard build
* registry aggregate

---

## 4. What to delete or freeze

### 4.1. Удалить phase-narrative from active package

Phase-numbering полезен для conversation/history, но в package это шум.

#### Нужно:

* сохранить `CHANGELOG.md`
* убрать phase-logic из runtime структуры

---

### 4.2. Заморозить CLI names

После stabilization:

* не переименовывать команды без крайней необходимости
* не ломать JSON field names

---

### 4.3. Удалить ad hoc validation duplication

Все отдельные мини-validator helpers должны либо:

* стать thin wrappers над `core/schema.py`
* либо быть удалены

---

### 4.4. Удалить implicit contract assumptions

Например:

* “это summary похоже на benchmark summary”
* “если есть поле X, то probably Y”

Нужно явное определение типа артефакта.

---

## 5. Concrete migration plan

### Step 1 — Freeze baseline

Перед началом:

* сохранить current Phase 13 as baseline archive
* объявить его pre-stabilization snapshot

Это нужно, чтобы было куда откатиться.

---

### Step 2 — Introduce package layout

Создать:

```text
src/dissertation_intro_qa/
```

И перенести код в модули.

Это structural migration, еще без behavior changes.

---

### Step 3 — Extract shared core

Вынести в core:

* IO
* errors
* render
* aggregation
* config
* schema
* envelope

---

### Step 4 — Introduce artifact envelope

Сначала:

* уметь читать both legacy + enveloped

Затем:

* все новые outputs писать только enveloped

#### Это лучший transitional режим:

* backward read compatibility
* forward write normalization

---

### Step 5 — Add canonical schemas

Сделать реальные schema files.

---

### Step 6 — Turn validation on by default

Все CLI commands должны:

* валидировать input
* валидировать output

---

### Step 7 — Lock taxonomy and schema versions

Добавить:

* `taxonomy_version`
* `schema_version`

во все релевантные артефакты.

---

### Step 8 — Add real tests

Минимально:

#### Unit tests

* io
* compare logic
* scorer logic
* registry logic
* manifest logic

#### Contract tests

* sample artifacts validate successfully
* broken artifacts fail

#### Regression tests

* benchmark scorer on sample strict/soft runs

---

### Step 9 — Cleanup docs

Документацию после refactor обновить так, чтобы:

* README отражал final structure
* COMMAND_REFERENCE отражал stabilized CLI
* ARCHITECTURE отражал layered modules, not only scripts

---

## 6. Concrete file-level diff

### Add

```text
src/dissertation_intro_qa/core/io.py
src/dissertation_intro_qa/core/errors.py
src/dissertation_intro_qa/core/schema.py
src/dissertation_intro_qa/core/envelope.py
src/dissertation_intro_qa/core/render.py
src/dissertation_intro_qa/core/aggregation.py
src/dissertation_intro_qa/core/config.py
src/dissertation_intro_qa/core/taxonomy.py
src/dissertation_intro_qa/version.py
configs/default.yaml
schemas/*.schema.json
tests/*.py
```

### Move

```text
intro_qa.py -> src/dissertation_intro_qa/cli/intro_qa.py
benchmark_scorer.py -> src/dissertation_intro_qa/cli/benchmark_scorer.py
benchmark_orchestrator.py -> src/dissertation_intro_qa/cli/benchmark_orchestrator.py
benchmark_registry.py -> src/dissertation_intro_qa/cli/benchmark_registry.py
benchmark_packager.py -> src/dissertation_intro_qa/cli/benchmark_packager.py
```

### Freeze

* defect code namespace
* command names
* benchmark case IDs
* summary metric names

### Remove or deprecate

* duplicated read/write/render helpers in each script
* any legacy JSON without version info after migration window ends

---

## 7. Transitional compatibility strategy

Это важный момент.

Не надо делать “жесткий слом сразу” без перехода.

### Recommended transition

#### Phase 14A

* read legacy + read new envelope
* write new envelope only
* emit warning for legacy input

#### Phase 14B

* fail on legacy input unless `--legacy-ok`

Так ты не убьешь старые артефакты мгновенно.

---

## 8. Definition of Done

Phase 14 считается завершенным, если выполнены все условия ниже.

### Contract / artifacts

* все JSON artifacts enveloped
* все artifacts versioned
* taxonomy version is explicit

### Validation

* every CLI command validates input/output
* invalid artifact fails predictably

### Code structure

* shared logic moved to core modules
* no obvious copy-paste renderer/IO duplication remains

### Determinism

* repeated run on same inputs gives byte-stable JSON output

### Tests

* unit tests pass
* contract tests pass
* benchmark smoke regression passes

### Docs

* architecture updated
* command reference updated
* migration note added to changelog

---

## 9. Recommended execution order in one sentence

Самый безопасный порядок такой:

> **package layout → shared core → envelope → schemas → validation enforcement → tests → docs cleanup**

---

## 10. Hard recommendation

Если делать это всерьез, я бы **не шел в Integration pass до завершения Phase 14**.

Потому что иначе ты подключишь реальный backend к системе, у которой:

* не зафиксирован artifact contract
* не зафиксирован error model
* нет строгой validation discipline

Это почти гарантированно создаст технический долг.

---
