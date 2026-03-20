# Phase 17 — Provider Adapters and Prompt Runner Integration

This pack adds a provider-adapter layer and a prompt runner on top of the
Phase 16 executor bridge.

Included:
- provider adapter interface
- local subprocess provider adapter
- deterministic prompt template loader
- prompt run manifest artifact
- prompt runner service
- CLI for running prompts through a provider adapter
- examples and tests

This pack still avoids direct remote API integration. It is designed to connect
the stabilized pipeline to local wrappers, model runners, or provider bridge
scripts.
