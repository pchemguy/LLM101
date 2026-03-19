# CONTRIBUTING AND EXTENSION GUIDE

## 1. Extension philosophy

New functionality should preserve the core principles of the project:

- artifact-first design
- machine-readable outputs
- compatibility with manual and LLM-assisted workflows
- explicit documentation of new commands and outputs

## 2. Safe extension points

### Add a new renderer
Recommended when introducing:
- new markdown reports
- new HTML dashboards
- new summary views

### Add a new artifact schema
Recommended when introducing:
- new JSON outputs
- new benchmark summary structures
- new registry or dashboard artifacts

### Add a new benchmark layer
Recommended when introducing:
- new benchmark metrics
- alternative scoring methods
- case families or domain-specific corpora

## 3. Documentation requirements for new features

Any new feature should update:

- `README.md`
- `CHANGELOG.md`
- `docs/reference/COMMAND_REFERENCE.md`
- relevant smoke test in `tests/`

## 4. Backward-compatibility guidance

Try to preserve:
- existing command names
- existing JSON field names
- existing basic directory structure

If a breaking change is unavoidable:
- record it in `CHANGELOG.md`
- document migration implications

## 5. Recommended next engineering directions

Possible future extensions:

- direct JSON schema validation using `jsonschema`
- richer HTML dashboard with charts
- prompt registry and evaluation matrix
- domain-specific benchmark families
- integration wrappers for external LLM APIs
- semi-automated repair execution pipeline

## 6. Minimal contribution checklist

Before accepting a new feature, verify:

1. Does it have a clear artifact model?
2. Does it preserve or document compatibility?
3. Does it include at least one usage example?
4. Does it include or update a smoke test?
5. Does it fit the layered architecture?
