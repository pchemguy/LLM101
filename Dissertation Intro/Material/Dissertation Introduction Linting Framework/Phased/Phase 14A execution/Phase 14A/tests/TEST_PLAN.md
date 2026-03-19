# Test Plan

## Unit tests
- test_envelope_wrap_unwrap.py
- test_legacy_and_enveloped_audit_validation.py
- test_compare_reports.py
- test_gate_logic.py
- test_history_index.py

## Contract tests
- legacy audit artifact accepted in Phase 14A
- enveloped audit artifact accepted
- malformed envelope rejected
- wrong artifact_type rejected

## Migration tests
- compare writes enveloped comparison artifact
- gate writes enveloped gate artifact
- history-index writes enveloped history artifact
