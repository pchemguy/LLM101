# Phase 16D Overview

## Objective
Replace the hardcoded demo audit step with an executor bridge.

## Supported executor modes
- `demo` — built-in deterministic audit stub
- `subprocess` — calls a local command which returns an audit artifact JSON file

## Executor contract
The executor must produce an enveloped `audit_report` artifact JSON.

## Why this matters
This is the first real bridge between the stabilized QA stack and an external
execution backend, while keeping the integration local and testable.
