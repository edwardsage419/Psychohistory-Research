# Platform v0.2 implementation plan

The current main inspected before implementation is `7ea6eab94433e3669b6f492d802bb35316dc90d6`. The existing cloud checkout is isolated and the feature branch starts from this revision. All edits are scoped to this platform directory.

1. Add typed curated source capture and verification for R123, R132 and R233. Persist immutable identities and classify sources outside pinned main as candidates.
2. Use DeGroot's discrete row-stochastic recursion from R123. This version uses exact synthetic inputs and compares a fixed forecast rule with a training-only prevalence baseline on separate synthetic studies. R132 remains a provenance profile while Phase A PR #44 is open. R272 informs the isolated execution design.
3. Build hash-bound protocol drafts, approvals and durable holdout-use accounting on existing SQLite. Add v2 execution beside v1, passing only approved synthetic specs to a subprocess that compiles fixed platform source bytes under isolated Python. Recheck provenance at dispatch and result acceptance.
4. Provide the same workflows through API, CLI and Chinese Web. Verify cancellation, failed run records, retry, history lookup and hash-checked results.
5. Run v0.1 and v0.2 tests, ordinary and optimized guards, browser flows, review, backup/restore and fresh checkout installation. Push scoped commits and one Draft PR with evidence.

Review focus includes duplicate holdout access under concurrent requests, candidate source leakage into approval, run restart and drift, exact executed bytes independent of cache/import paths, and reading existing v0.1 backups.
