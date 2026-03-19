# Phase 14 Migration Checklist

## 1. Freeze baseline
- [ ] Preserve pre-stabilization snapshot
- [ ] Record migration target version in CHANGELOG

## 2. Package layout
- [ ] Create `src/dissertation_intro_qa/`
- [ ] Move standalone scripts into `src/dissertation_intro_qa/cli/`
- [ ] Add `version.py`

## 3. Shared core extraction
- [ ] Move JSON IO helpers into `core/io.py`
- [ ] Move validation logic into `core/schema.py`
- [ ] Move renderer functions into `core/render.py`
- [ ] Move aggregation logic into `core/aggregation.py`
- [ ] Add `core/errors.py`
- [ ] Add `core/config.py`
- [ ] Add `core/taxonomy.py`

## 4. Artifact envelope
- [ ] Introduce `artifact_type`
- [ ] Introduce `schema_version`
- [ ] Introduce `generated_at`
- [ ] Introduce `producer`
- [ ] Move old payload into `payload`

## 5. Canonical schemas
- [ ] Add all schema files under `schemas/`
- [ ] Ensure every artifact type has a schema
- [ ] Ensure schema names are mapped centrally

## 6. Validation enforcement
- [ ] Input validation is on by default
- [ ] Output validation is on by default
- [ ] Invalid artifacts fail fast
- [ ] Exit codes are normalized

## 7. Determinism
- [ ] JSON uses stable ordering
- [ ] Output lists are sorted deterministically
- [ ] Dashboard / registry ordering is deterministic

## 8. Taxonomy lock
- [ ] Add machine-readable taxonomy file
- [ ] Add explicit `taxonomy_version` to audit artifacts
- [ ] Freeze defect code namespace

## 9. Tests
- [ ] Add unit tests for IO / compare / scorer / registry
- [ ] Add schema contract tests
- [ ] Add regression tests for benchmark summaries

## 10. Transition strategy
- [ ] Read legacy artifacts
- [ ] Write enveloped artifacts only
- [ ] Emit warnings on legacy input
- [ ] Plan hard cutover after migration window
