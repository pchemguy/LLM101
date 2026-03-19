# Phase 15 — Implementation Roadmap

## Contract Completion and Stack Migration

Ниже — уже **execution plan**, а не концепт.
Цель: довести `Phase 14A execution starter` до состояния **stabilization-complete package**.

---

## 1. Цель Phase 15

Phase 15 считается успешным, если система становится:

* **schema-enforced**
* **artifact-contract stable**
* **fully migrated into package layout**
* **testable**
* **config- and taxonomy-aware**

Иначе говоря, после него стек должен перестать быть “starter with direction” и стать **coherent internal package**.

---

## 2. Main workstreams

Phase 15 лучше делать по пяти workstreams.

| Workstream | Goal                            |
| ---------- | ------------------------------- |
| WS1        | Full schema enforcement         |
| WS2        | Full CLI migration              |
| WS3        | Test suite                      |
| WS4        | Config and taxonomy integration |
| WS5        | Docs + migration cleanup        |

---

## 3. WS1 — Full schema enforcement

### 3.1. Add real dependency

В `pyproject.toml` добавить:

```toml
dependencies = ["jsonschema>=4.0"]
```

### 3.2. Extend schema inventory

Сейчас в 14A есть только базовые схемы. Нужно добавить полный набор:

```text
schemas/
  artifact_envelope.schema.json
  audit_report.schema.json
  comparison_report.schema.json
  gate_result.schema.json
  history_index.schema.json
  benchmark_summary.schema.json
  leaderboard.schema.json
  run_manifest.schema.json
  workflow_plan.schema.json
  session.schema.json
  run_registry.schema.json
  project_dashboard.schema.json
  release_manifest.schema.json
```

### 3.3. Replace lightweight validator

Текущий `core/schema.py` должен быть заменен на real validator:

* `load_schema(schema_name)`
* `validate_payload(payload, artifact_type)`
* `validate_enveloped_artifact(data)`
* `assert_valid_artifact(data, expected_type=None, allow_legacy=True)`

### 3.4. Add explicit schema map

```python
SCHEMA_MAP = {
    "audit_report": "audit_report.schema.json",
    "comparison_report": "comparison_report.schema.json",
    "gate_result": "gate_result.schema.json",
    ...
}
```

### 3.5. Enforce on every migrated command

Каждая команда:

* валидирует input artifact
* валидирует output artifact before write

---

## 4. WS2 — Full CLI migration

### 4.1. Current state

В 14A migrated только subset `intro_qa`.

### 4.2. Required migration matrix

| CLI                      | Status in 14A | Phase 15 action |
| ------------------------ | ------------- | --------------- |
| `intro_qa`               | partial       | complete        |
| `benchmark_scorer`       | placeholder   | migrate         |
| `benchmark_orchestrator` | placeholder   | migrate         |
| `benchmark_registry`     | placeholder   | migrate         |
| `benchmark_packager`     | placeholder   | migrate         |

### 4.3. Migration order

Правильный порядок:

1. `benchmark_scorer`
2. `benchmark_orchestrator`
3. `benchmark_registry`
4. `benchmark_packager`
5. finish `intro_qa`

Почему так:

* scorer depends mostly on artifact contracts
* orchestrator depends on benchmark artifacts
* registry depends on scorer/orchestrator artifacts
* packager sits at outer layer

### 4.4. Refactor rule

В каждом CLI:

* parse args only
* call shared core/artifact functions
* no duplicated IO/render/aggregation logic

---

## 5. WS3 — Test suite

### 5.1. Add pytest layout

```text
tests/
  test_envelope.py
  test_schema_validation.py
  test_compare_reports.py
  test_gate_logic.py
  test_history_index.py
  test_benchmark_scorer.py
  test_benchmark_orchestrator.py
  test_benchmark_registry.py
  test_packager.py
  test_cli_smoke.py
```

### 5.2. Test matrix

#### Envelope tests

* wrap creates valid envelope
* unwrap legacy works in Phase 15
* unwrap wrong type fails

#### Schema tests

* valid audit artifact passes
* missing `payload` fails
* missing required payload keys fail
* unknown artifact type fails

#### Compare tests

* resolved defects computed correctly
* new defects computed correctly
* score delta deterministic

#### Gate tests

* strict profile fails on critical defects
* supervisor profile passes expected sample
* missing GOST fields trip correct failure

#### History/dashboard tests

* history index ordering deterministic
* dashboard markdown stable

#### Benchmark scorer tests

* expected vs actual diff correct
* macro recall correct
* severity failure detection correct

#### Registry tests

* session creation correct
* run registration appends deterministically
* consolidated dashboard chooses best/worst correctly

#### Packager tests

* bootstrap creates expected dirs
* demo-plan file shape correct
* release bundle copies expected artifacts

---

## 6. WS4 — Config and taxonomy integration

### 6.1. Real config loader

Replace placeholder `core/config.py` with:

* YAML parser
* defaults
* optional override merge

Need fields like:

```yaml
schema_validation: strict
legacy_input_mode: warn
taxonomy_version: 1.0.0
json_sort_keys: true
reject_unknown_defect_codes: true
```

### 6.2. Real taxonomy loader

`core/taxonomy.py` should:

* load machine-readable taxonomy
* expose lookup by code
* expose severity floor
* validate unknown codes

### 6.3. Artifact propagation

Audit artifacts must explicitly include:

```json
"taxonomy_version": "1.0.0"
```

### 6.4. Optional enforcement

For audit artifacts:

* if defect code not in taxonomy → fail or warn based on config
* if severity below taxonomy floor → warn or fail based on config

---

## 7. WS5 — Docs and migration cleanup

### 7.1. Update docs after actual migration

Need to update:

* `README.md`
* `CHANGELOG.md`
* `docs/ARCHITECTURE.md`
* `docs/reference/COMMAND_REFERENCE.md`

### 7.2. Add migration note

New doc:

```text
docs/MIGRATION_FROM_PHASE14A.md
```

Should explain:

* legacy JSON still readable
* all newly written artifacts are enveloped
* schema enforcement now real
* migrated CLIs list

### 7.3. Mark placeholders removed

Once a CLI is migrated:

* remove “placeholder” docs language
* update examples

---

## 8. Exact file diff

### Add

```text
schemas/comparison_report.schema.json
schemas/gate_result.schema.json
schemas/history_index.schema.json
schemas/benchmark_summary.schema.json
schemas/leaderboard.schema.json
schemas/run_manifest.schema.json
schemas/workflow_plan.schema.json
schemas/session.schema.json
schemas/run_registry.schema.json
schemas/project_dashboard.schema.json
schemas/release_manifest.schema.json

tests/test_envelope.py
tests/test_schema_validation.py
tests/test_compare_reports.py
tests/test_gate_logic.py
tests/test_history_index.py
tests/test_benchmark_scorer.py
tests/test_benchmark_orchestrator.py
tests/test_benchmark_registry.py
tests/test_packager.py
tests/test_cli_smoke.py

docs/MIGRATION_FROM_PHASE14A.md
```

### Replace

```text
src/dissertation_intro_qa/core/schema.py
src/dissertation_intro_qa/core/config.py
src/dissertation_intro_qa/core/taxonomy.py
src/dissertation_intro_qa/cli/benchmark_scorer.py
src/dissertation_intro_qa/cli/benchmark_orchestrator.py
src/dissertation_intro_qa/cli/benchmark_registry.py
src/dissertation_intro_qa/cli/benchmark_packager.py
```

### Expand

```text
src/dissertation_intro_qa/core/render.py
src/dissertation_intro_qa/core/aggregation.py
src/dissertation_intro_qa/cli/intro_qa.py
```

---

## 9. Recommended implementation order

### Step 1

Finish schema inventory.

### Step 2

Replace `core/schema.py` with real `jsonschema` validation.

### Step 3

Implement `core/config.py` and `core/taxonomy.py`.

### Step 4

Migrate `benchmark_scorer.py`.

### Step 5

Migrate `benchmark_orchestrator.py`.

### Step 6

Migrate `benchmark_registry.py`.

### Step 7

Migrate `benchmark_packager.py`.

### Step 8

Finish remaining `intro_qa` commands.

### Step 9

Add tests.

### Step 10

Update docs and changelog.

That is the lowest-risk order.

---

## 10. Acceptance gates for Phase 15

### Gate 15-1 — Schema Complete

Passes if:

* every artifact type has schema
* `assert_valid_artifact()` uses real schema validation
* invalid artifacts fail predictably

### Gate 15-2 — CLI Complete

Passes if:

* all major CLIs are migrated under `src/.../cli`
* no major duplicated business logic remains

### Gate 15-3 — Testable

Passes if:

* pytest suite exists
* unit + contract + regression tests pass

### Gate 15-4 — Configured

Passes if:

* config loader is real
* taxonomy is machine-readable and enforced
* unknown code handling is explicit

### Gate 15-5 — Migration Safe

Passes if:

* legacy artifacts readable
* new artifacts written only as enveloped
* migration doc exists

---

## 11. Command migration matrix

| Command group                     | Phase 14A    | Phase 15 target |
| --------------------------------- | ------------ | --------------- |
| `compare`                         | migrated     | finalize        |
| `gate`                            | migrated     | finalize        |
| `render-*`                        | migrated     | finalize        |
| `repair-plan`                     | migrated     | finalize        |
| `history-index`                   | migrated     | finalize        |
| `dashboard`                       | migrated     | finalize        |
| `benchmark score-run`             | not migrated | migrate         |
| `benchmark leaderboard`           | not migrated | migrate         |
| `orchestrator discover`           | not migrated | migrate         |
| `orchestrator manifest`           | not migrated | migrate         |
| `orchestrator workflow-plan`      | not migrated | migrate         |
| `orchestrator regression-summary` | not migrated | migrate         |
| `registry create-session`         | not migrated | migrate         |
| `registry register-run`           | not migrated | migrate         |
| `registry build-registry`         | not migrated | migrate         |
| `registry project-dashboard`      | not migrated | migrate         |
| `packager bootstrap`              | not migrated | migrate         |
| `packager demo-plan`              | not migrated | migrate         |
| `packager release-bundle`         | not migrated | migrate         |

---

## 12. Risks to watch

### 12.1. Partial schema mismatch

If schemas are too strict too early, legacy samples will explode.

Mitigation:

* keep `allow_legacy=True` in Phase 15
* only new outputs must be enveloped

### 12.2. Taxonomy enforcement too early

Unknown codes in legacy benchmark data may fail.

Mitigation:

* config-driven warn/fail

### 12.3. Hidden duplication remains

If CLI migration is rushed, duplication just moves around.

Mitigation:

* every migrated CLI should shrink to thin wrapper size

---

## 13. Definition of Done

Phase 15 is done when:

* all major artifact types are schema-defined
* all migrated commands validate input/output
* all migrated commands write enveloped artifacts
* benchmark / orchestrator / registry / packager are migrated into package layout
* pytest suite passes
* config and taxonomy are real, not placeholder
* docs reflect stabilized package state

---
