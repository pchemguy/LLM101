# Migration from Phase 14A

This starter advances the stabilization process beyond Phase 14A.

## What changed

- lightweight validation is replaced with `jsonschema`-based validation
- schema inventory is expanded
- `benchmark_scorer` is migrated into package layout
- minimal pytest suite is added

## Transitional compatibility

- legacy flat artifacts are still readable when `allow_legacy=True`
- new benchmark summary and leaderboard outputs are written as enveloped artifacts

## Recommended next migrations

1. migrate `benchmark_orchestrator`
2. migrate `benchmark_registry`
3. migrate `benchmark_packager`
4. extend tests
5. integrate real config and taxonomy enforcement
