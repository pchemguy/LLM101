# Phase 17 Overview

## Objective
Introduce a provider abstraction above the local executor bridge.

## Main concepts
- ProviderAdapter: execution backend abstraction
- PromptTemplate: deterministic prompt loading and rendering
- PromptRunner: runs one prompt against one provider and persists outputs
- Run manifest: structured metadata describing provider execution

## Supported provider modes
- demo
- subprocess

## Intended next use
Plug a local wrapper script that calls a model backend and returns a JSON result.
