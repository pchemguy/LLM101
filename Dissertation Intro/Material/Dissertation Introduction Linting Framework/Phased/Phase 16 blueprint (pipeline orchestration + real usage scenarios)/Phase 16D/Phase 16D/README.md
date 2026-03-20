# Phase 16D — Local Executor Bridge Pack

This pack upgrades the Phase 16 pipeline by replacing the demo audit step with a
real local executor bridge.

Included:
- executor interface
- demo built-in executor
- subprocess bridge executor
- executor selection via pipeline config
- audit step wired to executor bridge
- basic CLI for running a local audit executor
- tests for executor selection and subprocess bridge

This pack still does not call remote APIs directly. It is designed to connect the
pipeline to a locally available audit command or script.
