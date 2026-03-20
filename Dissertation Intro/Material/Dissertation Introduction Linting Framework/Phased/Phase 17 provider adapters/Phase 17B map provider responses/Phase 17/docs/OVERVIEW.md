# Phase 17B Overview

This pack maps provider responses into normalized `audit_report` artifacts and
makes them consumable by the pipeline layer.

Main additions:
- provider -> audit mapper
- prompt runner emitting mapped audit artifacts
- provider-backed audit bridge for pipeline usage
- tests for structured and JSON-payload mapping
