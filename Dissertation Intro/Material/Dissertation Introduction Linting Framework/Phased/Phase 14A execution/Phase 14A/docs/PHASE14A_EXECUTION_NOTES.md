# Phase 14A Execution Notes

This starter intentionally migrates only a subset of functionality.

## Migrated now
- package layout
- shared core
- envelope support
- compare
- gate
- renderers
- repair plan
- history index
- dashboard

## Deferred
- benchmark scorer migration
- benchmark orchestration migration
- registry migration
- release layer migration
- strict jsonschema enforcement
- full test suite

## Immediate next tasks
1. Replace lightweight schema checks with canonical schema validation.
2. Migrate remaining CLIs into package layout.
3. Add transitional warnings for legacy artifacts in CLI output.
4. Add unit tests for compare / gate / envelope behavior.
