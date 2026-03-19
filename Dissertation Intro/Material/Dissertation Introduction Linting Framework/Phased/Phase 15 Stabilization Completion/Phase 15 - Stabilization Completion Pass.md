# Phase 15 — Stabilization Completion Pass

Его задача — закрыть именно те четыре незавершенных блока, которые сейчас остались после 14A:

1. **полноценный `jsonschema` enforcement**
2. **миграция benchmark/scorer/orchestrator/registry/packager слоев**
3. **реальная test suite**
4. **полная config/taxonomy integration**

То есть 14A сделал:

* package layout
* shared core
* envelope
* partial CLI migration

А 15 должен сделать:

* **contract enforcement real**
* **stack-wide migration complete**
* **regression-safe execution**
* **configuration discipline fixed**

---

## Как я бы сформулировал Phase 15

### Phase 15A — Contract enforcement

Это самый критичный блок.

Нужно:

* заменить lightweight validation на реальный `jsonschema`
* сделать schema validation обязательным для всех migrated commands
* ввести единый `artifact_type -> schema` resolver
* добавить strict/warn/off policy через config/CLI

#### Deliverables

* `core/schema.py` на `jsonschema`
* canonical schemas for all artifact types
* fail-fast validation everywhere
* normalized exit codes

---

### Phase 15B — Full CLI migration

Сейчас migrated только часть `intro_qa`.

Нужно перенести в stabilized layout:

* `benchmark_scorer`
* `benchmark_orchestrator`
* `benchmark_registry`
* `benchmark_packager`

И убрать логику из standalone-style scripts в:

* `core/aggregation.py`
* `core/render.py`
* `artifacts/*.py`

#### Deliverables

* all CLIs under `src/dissertation_intro_qa/cli/`
* shared helpers reused instead of copy-paste
* envelope write path everywhere
* legacy read compatibility preserved temporarily

---

### Phase 15C — Real test suite

Это уже не markdown smoke docs, а настоящие тесты.

Минимально нужны:

#### Unit tests

* envelope wrap/unwrap
* schema validation
* compare logic
* gate logic
* scorer logic
* registry logic

#### Contract tests

* valid enveloped artifact passes
* malformed envelope fails
* wrong artifact type fails
* missing required payload keys fail

#### Regression tests

* benchmark summary on sample strict run
* benchmark summary on sample soft run
* leaderboard ordering deterministic
* dashboard / registry outputs deterministic

#### CLI tests

* migrated commands produce expected files
* invalid input exits with correct code

---

### Phase 15D — Config and taxonomy integration

Сейчас config/taxonomy mostly placeholder.

Нужно:

* real config loader
* config precedence model
* machine-readable taxonomy loader
* explicit taxonomy version propagation
* severity floor lookup from taxonomy
* optional validation that unknown defect codes are rejected

#### Deliverables

* `core/config.py`
* `core/taxonomy.py`
* `configs/default.yaml`
* `configs/defect_taxonomy.json`
* `taxonomy_version` present in audit artifacts
* defect code validation

---

## Самая правильная структура Phase 15

Я бы разбил не по “фазам внутри фазы”, а по **acceptance gates**.

### Gate 15-1 — Schema-complete

Считается пройденным, если:

* every artifact type has schema
* every migrated command validates input/output
* schema errors fail predictably

### Gate 15-2 — CLI-complete

Считается пройденным, если:

* all major scripts are migrated into package layout
* no major business logic remains duplicated across CLIs

### Gate 15-3 — Testable

Считается пройденным, если:

* pytest suite exists
* unit + contract + regression tests pass

### Gate 15-4 — Configured and taxonomy-locked

Считается пройденным, если:

* config loader is real
* taxonomy is machine-readable and versioned
* unknown defect code handling is explicit

---

## Что Phase 15 даст practically

После него система станет не просто “stabilized in direction”, а уже **operationally coherent**.

То есть ты получишь:

### До Phase 15

* правильная архитектурная траектория
* частичная стабилизация
* рабочий starter

### После Phase 15

* **единый контракт артефактов**
* **единый runtime discipline**
* **тестируемый package**
* **почти production-grade internal tool**

---

## Что я бы НЕ делал в Phase 15

Важно не сорваться обратно в feature creep.

Не надо в Phase 15:

* UI
* API
* real LLM backend
* charts / fancy dashboards
* auto-repair orchestration

Сначала нужно закончить stabilization completion.

---

## Самый рациональный итоговый смысл

Если Phase 14A был:

> “начало переноса в стабильную архитектуру”

то Phase 15 должен быть:

> “закрытие архитектурного долга и фиксация инвариантов”

---

## Suggested official name

Я бы назвал его так:

**Phase 15 — Contract Completion and Stack Migration**

или, если короче:

**Phase 15 — Stabilization Completion**

---

