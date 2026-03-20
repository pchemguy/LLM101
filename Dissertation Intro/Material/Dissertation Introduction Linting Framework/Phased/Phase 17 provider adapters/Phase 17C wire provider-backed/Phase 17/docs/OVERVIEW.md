# Phase 17C Overview

This pack wires provider-backed audit directly into the pipeline runner as an
alternate audit path.

Main additions:
- pipeline audit step supports two modes:
  - executor-backed audit
  - provider-backed audit
- audit mode selection via pipeline config
- end-to-end pipeline run using provider-backed mapped audit artifacts
- tests for demo provider and subprocess JSON-payload provider paths

This closes the loop between:
provider adapter -> provider response mapping -> normalized audit artifact ->
gate/history/dashboard pipeline stages.
