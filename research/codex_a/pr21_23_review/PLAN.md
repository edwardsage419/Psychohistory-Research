# Independent PR 21–23 review and CLI regression plan

Goal/spec: extend the user's A2/A3 engineering verification with real native
replays and CLI identity/schema regressions, without changing research sources,
frozen protocols or Codex B implementations. Three fixed proposed heads are
review inputs, not adopted main capabilities. Main starts at `25bcd51d`.

Architecture: use existing replay CLIs for the full numerical work. A small
unittest file exports #22/#23 CLI modules and original artifacts from fixed Git
objects into temporary roots, invokes real Python/Node processes and checks
structured exit/status contracts. No new scientific algorithm or framework.
Original files are never written. No packages, network, CI or merge is required
by the tests. Missing fixed Git objects are errors, never skips or downloads.

Review focus: independently permuted records must retain identity; duplicate
identities must reject; duplicate JSON keys at multiple depths must reject;
bool/float confusion must reject; an altered original B executable must reject.

- [x] Capture current main/open PRs, inspect sources/dependencies, run all three
  complete replays in normal/-O, verify every stream/source hash (six exits 0).
- [x] Add `test_cli_contracts.py`: archived and permuted positives; duplicate
  identities/keys; nonfinite JSON; metadata and declaration types; CSV coverage;
  missing/extra success-shaped metadata; original B executable pin.
- [x] Prove test sensitivity against a disposable duplicate-key-parser mutant;
  retain the expected assertion failure and unchanged real sources.
- [x] Run the clean fixed CLI tests in normal/-O, retain raw logs/commands and
  source hashes, inspect the review diff and prepare an independent draft PR.

Execution: inline, as authorized by the user's continuing engineering scope.
Only the new Codex A directory may be committed. The full repository has no
single established test command; scope claims explicitly to these replays and
CLI regressions. Original R077 failures and scientific limits remain unchanged.
No merging #21–#23 is included in this work package.

Final review: one fresh read-only reviewer found a P2 synchronized-permutation
blind spot. Fixed in one pass: independent schedule rotations and collection
reversals. Positional mutants pass the synchronized-only control; the final
tests produce five expected assertion failures against those temporary copies.
The duplicate-parser mutant produces four failures. Clean snapshots pass both
modes, 10 methods and 35 real CLI calls per mode, no skips. No Codex B fix was
needed; this is test coverage, not a discovered scientific discrepancy.
