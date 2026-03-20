# Phase 16B Overview

Pipeline execution model:

1. Read pipeline config.
2. Create isolated run directory.
3. Execute configured steps in order.
4. Persist step outputs into the run directory.
5. Validate contract artifacts after each contract-producing step.
6. Return gate-aware exit code.

Current demo stages:
- audit
- gate
- repair-plan
- history-index
- dashboard
