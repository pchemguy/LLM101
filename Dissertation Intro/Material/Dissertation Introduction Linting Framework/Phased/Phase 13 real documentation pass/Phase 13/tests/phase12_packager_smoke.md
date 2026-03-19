# Phase 12 Packager Smoke Test

## Goal

Проверить packager/release layer.

## Commands

### Bootstrap
```bash
python benchmark_packager.py bootstrap   --target /tmp/dissertation_intro_qa_bootstrap   --out-json bootstrap/bootstrap_result.json
```

### Demo plan
```bash
python benchmark_packager.py demo-plan   --project-root .   --out-json demo_runner/demo_plan.json   --out-md demo_runner/demo_plan.md
```

### Release bundle
```bash
python benchmark_packager.py release-bundle   --project-root .   --out-dir release/dissertation_intro_qa_release   --out-json release/release_bundle.json   --out-md release/release_bundle.md
```

## Expected result

- scaffold directories are created
- demo plan is generated
- release bundle copies core scripts and benchmark assets
- release manifest is produced
