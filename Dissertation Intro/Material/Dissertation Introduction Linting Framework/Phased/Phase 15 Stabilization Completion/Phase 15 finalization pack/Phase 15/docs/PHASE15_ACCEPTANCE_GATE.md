# Phase 15 Acceptance Gate

Phase 15 is considered complete only if all conditions below are satisfied.

## Gate 15-1 — Schema complete
- [x] Main migrated artifact types have schemas
- [x] Input/output validation exists for migrated commands
- [x] Invalid artifacts fail predictably

## Gate 15-2 — CLI complete
- [x] `intro_qa` migrated
- [x] `benchmark_scorer` migrated
- [x] `benchmark_orchestrator` migrated
- [x] `benchmark_registry` migrated
- [x] `benchmark_packager` migrated

## Gate 15-3 — Testable
- [x] Pytest suite fragments exist for core flows
- [x] Contract tests exist
- [x] CLI smoke fragments exist

## Gate 15-4 — Configured
- [x] Config loader exists
- [x] Taxonomy loader exists
- [x] Taxonomy-aware validation hooks exist

## Gate 15-5 — Migration safe
- [x] Legacy artifacts remain readable when explicitly allowed
- [x] New outputs are written as enveloped artifacts
- [x] Migration notes exist

## Remaining non-gate improvements
- stronger full-stack exit-code coverage
- stricter default taxonomy enforcement
- more exhaustive integration tests
