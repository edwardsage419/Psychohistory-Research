# A2 — R077 fail-closed integration preflight

track: Codex A engineering
subflow: A2 reversible independent-validator entrypoint
run_date: 2026-11-10 UTC (exact execution records in archive)
observed_head: 3221a84fba91731071b8931447837e07578210be
status: COMPLETE for the standalone engineering preflight; PARTIAL for A2 production integration
evidence_scope: fixed-version synthetic regression and source identity only
ci_status: NOT_RUN
billing_checked: existing local environment only; no paid API/resource/install/dispatch; CI quota NOT_VERIFIED
output_paths: research/codex_a/r077_integration/
commit_sha: actual delivery commit recorded in the independent PR
source_links: B18 commit 9de51508daa160d33d0d05b13ba1454f8333f21d, its HANDOFF.md/replay.py/exact_pair.py, R077 Rev002 protocol and original scorer

## Obstacle and completed interface

The original R077 floating-point scorer has the already-established artificial
exact-tie ordering regression. Codex B's existing supplement and replay correctly
report a bounded diagnostic PASS while retaining that original failure. Their
exit 0 is not a defect in the bounded replay, but it must not be used as a
production-readiness gate. Human rescoring and mathematical repair stay with B
and the scientific protocol owners.

This package adds a small independent preflight entrypoint. It authenticates all
40 source fingerprints from B18's fixed Git receipt, checks live bytes and the
captured checkout tree, exports one immutable temporary snapshot and invokes the
**unchanged existing B18 DIAGNOSTICS string** in isolated Python. The existing
original scorer, exact kernel, case generator and integer witness do all numerical
work. No model probabilities, score formulas or repair algorithm are recreated.

The adapter checks complete identities for all 35 cases and consistency of vote
counts, flags and histograms. The result has an explicit production veto:

| Condition | Status | Exit |
|---|---|---:|
| Authentic current diagnostic, original 11 failures retained | BLOCKED_ORIGINAL_R077_UNREPAIRED; engineering_preflight COMPLETE; production_ready false | 2 |
| Missing/changed source, bad identity/schema, failed child or invalid diagnostic | BLOCKED_INVALID_PREFLIGHT | 1 |

There is no success/exit-0 production promotion in this preflight version. The
`--artificial-preflight` flag is mandatory. It accepts no human-data file or
untrusted expected-value argument and writes no original file or result receipt.
Only temporary snapshots and stdout are produced. The source manifest is fetched
from already-present Git objects, not the network. Own adapter bytes are recorded
before execution and checked again before returning.

`classify()` is an engineering consistency check for the trusted pinned child
output, not a standalone mathematical verifier for arbitrary submitted JSON.
The new entrypoint can now be invoked by a caller as a fail-closed readiness
precondition; the frozen original scorer and production research workflow do
not yet invoke it.

## Actual tests and preserved failures

Both normal and optimized Python 3.12.14 CLI runs authenticated 40 sources,
executed the existing 35-case diagnostic and returned the expected exit **2**,
with 11 original failure cases and `production_ready: false`. The diagnostic
stdout hashes were independently recomputed from retained raw data. All 40
source blobs still match latest main and source SHA256 values remain unchanged.

The 12 new unit methods pass in each mode. Coverage includes duplicate/missing
cases, bool/float counts, vote/flag/histogram inconsistency, fake success fields,
human-scope promotion, duplicate JSON and nonfinite values. Actual CLI tests on
disposable source copies reject altered worktree bytes and a mismatching tracked
checkout, even when live source bytes remain correct. No original source was
edited by the tests.

Test-first RED had 13 assertion/subtest failures across 9 methods against a
permissive classification stub. A separate temporary mutant omitted only the
current-worktree/current-checkout guards: both invalid-source CLI tests then
failed, because the wrong copy returned diagnostic-blocked exit 2 rather than
invalid-source exit 1. That is an identity/failure-attribution control, not a
new mathematical bug or a claim that the mutant gave production approval.

A fresh read-only reviewer independently ran both 12-method suites and both real
CLIs, finding no important issue. The original 59-method baseline suite was not
rerun here: it is unchanged and is not needed to exercise this new boundary.
Repeated artificial diagnostics are not new independent scientific evidence.

## Reproduction, provenance and rollback

From a clone already containing the fixed B18 Git objects:

```sh
python3 -B -m unittest discover -s research/codex_a/r077_integration -v
python3 -O -B -m unittest discover -s research/codex_a/r077_integration -v
python3 -B research/codex_a/r077_integration/preflight.py . --artificial-preflight
python3 -O -B research/codex_a/r077_integration/preflight.py . --artificial-preflight
```

The last two commands intentionally return 2; callers must honor the exit code
and production_ready field. Do not append shell success overrides or reinterpret
the diagnostic completion as repaired production behavior. Exact commands,
stdout/stderr, RED/GREEN controls and source-preservation checks are archived in
`evidence.tar.gz`; member hashes are in `evidence_members.json`. Delivered source
SHA256 and Git blobs are in `artifact_hashes.json`. Full fixed source identities,
checkout, runtime/mode and diagnostic digest are present in each CLI sidecar.

Rollback is simply to stop invoking this optional entrypoint; no historical
code/data/result or default workflow has been patched. A future mathematical
repair requires reviewed explicit repinning, not an automatic fallback to newer
or arbitrary source bytes.

## Blockers and next action

Original mathematical repair remains B-owned and **not completed by this
package**. Qualified exact human-probability export, source qualification,
protocol-authorized rescoring, formal production binding, Python3.11/other
platforms, the full repository suite and scientific reacceptance are NOT_RUN.
Historical 14/15 votes, scientific status and results are not reinterpreted.
No human/E2/E3/external-team evidence or formal research queue closure is added.
R073/PESEN v0.1 stay frozen. No GitHub workflow, merge or paid computation ran.

next_action: B to provide a reviewed exact source-probability interface/repair;
A to bind that interface behind source qualification and this explicit veto,
then verify actual production-caller behavior under corresponding authorization.
The A1-reviewed candidate PRs remain open until their specific merge approval.
