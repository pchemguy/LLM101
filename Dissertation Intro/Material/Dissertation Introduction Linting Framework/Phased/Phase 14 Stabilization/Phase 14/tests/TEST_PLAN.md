# Test Plan Skeleton

## Unit tests
- test_io_roundtrip.py
- test_envelope_helpers.py
- test_compare_logic.py
- test_benchmark_summary.py
- test_registry_logic.py

## Contract tests
- valid enveloped audit artifact passes
- invalid envelope fails
- invalid payload fails
- unknown artifact type fails

## Regression tests
- strict benchmark summary remains stable
- soft benchmark summary remains stable
- leaderboard ordering remains deterministic
