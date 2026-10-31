# R257 S53 strict receipt validator plan
Goal: reject the six PR #1 false positives without changing archived code or blind-order status.
Design: standard-library validator in research/codex_audit/r257_s53_validator; fixed protocol identities plus exact convex KKT certificates, not an import/copy of either archived optimizer. CLI fails closed with ValueError/exit 1, works under python -O. Successful output explicitly retains blinded-order FAIL and full scientific acceptance PARTIAL.
- [x] Write mutation, malformed-input, CLI and positive receipt tests. Run against no-op skeleton and retain red output.
- [x] Implement fixed sets/schema, exact rational KKT, baseline/derivative/secants and metadata checks; no production assert.
- [x] Run full isolated unittest suite normally and -O, then validate archived receipt and reject corrupted CLI input. Record versions/hashes/commands.
- [x] Re-read main and target paths; publish only new dedicated files and dated Codex handoff on branch/PR. Read back bytes and actual Actions state.
Limits: nonblind E1 algorithm check, not full prescore acceptance, not source CSV re-audit or external team replication; original R073/PESEN/protocol/results remain frozen. No new costs/CI.
