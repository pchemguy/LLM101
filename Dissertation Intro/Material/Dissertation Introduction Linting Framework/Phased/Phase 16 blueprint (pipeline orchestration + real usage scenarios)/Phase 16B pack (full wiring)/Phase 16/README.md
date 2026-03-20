# Phase 16B — Pipeline Wiring Pack

This pack upgrades the Phase 16A orchestrator skeleton into a wired pipeline runner.

Included:
- step registry for pipeline stages
- real artifact passing between steps
- strict validation hook after each step
- gate-based exit-code propagation
- run directory layout with persisted artifacts
- demo step implementations for:
  - audit
  - gate
  - repair-plan
  - history-index
  - dashboard

This is still a local execution pack. It does not call external LLM backends.
