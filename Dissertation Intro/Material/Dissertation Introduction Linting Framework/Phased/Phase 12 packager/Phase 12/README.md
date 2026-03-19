# Dissertation Intro QA CLI — Phase 12

Phase 12 adds a packager / release layer.

## New script

- `benchmark_packager.py`

## What it adds

Phase 12 introduces:
- full project scaffold generator
- one-command bootstrap
- demo pipeline plan generator
- release bundle generator for handoff / publishing

## Main commands

### 1. Bootstrap empty project scaffold
```bash
python benchmark_packager.py bootstrap   --target /path/to/new_project   --out-json bootstrap/bootstrap_result.json
```

### 2. Generate demo pipeline plan
```bash
python benchmark_packager.py demo-plan   --project-root .   --out-json demo_runner/demo_plan.json   --out-md demo_runner/demo_plan.md
```

### 3. Build release bundle
```bash
python benchmark_packager.py release-bundle   --project-root .   --out-dir release/dissertation_intro_qa_release   --out-json release/release_bundle.json   --out-md release/release_bundle.md
```

## Why this matters

Phase 12 makes the stack handoff-ready:

- a new project scaffold can be created automatically;
- a demo workflow can be documented in one command;
- a releasable bundle can be assembled for GitHub or direct transfer.
