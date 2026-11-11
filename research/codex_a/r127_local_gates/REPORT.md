# R127 standalone fail-closed engineering gate

This implements the local candidate gate requested by main's R127 P0 handoff.
It does not edit the R-owned production workflow or historical research files.
Base: `b8b0ea2e2a45a6fb9c99e9a51302ab0f07e8c613`.

## Problem and resulting behavior

The workflow at Git blob `4b22f653dc7516bb31ead23e45dcf7f62261d79d`
uses assertions to validate test logs and upstream scientific aggregates. Its
log parser accepts FAILED followed by OK, and optimization removes its integrity
assertions. Its literal zero E2 receipt field can mask a synthetic upstream 7.
These are existing documented defects, not new discoveries or claims about the
actual historical result. Original unittest execution uses pipefail; our controls
do not demonstrate a full production CI bypass.

`gate.py` now supplies a standalone, stdout-only local replay:

- Authenticate five fixed workflow/code/test/report/historical-receipt snapshots
  using SHA256, Git blob and one captured checkout commit. All computation uses
  those snapshots in a temporary tree; the original files are not executed in
  place or changed. This reuses the adopted S53/R170 byte-identity pattern and
  the original R127 algorithms and tests, without a new scientific algorithm.
- Run the original 60 unittest methods in isolated Python, explicitly propagating
  `-O`. Require exit 0, exactly one 60-test summary and one final plain OK; reject
  failure markers, duplicate/nested summaries, skips and expected failures.
- Reexecute the original six stage-two functions. Compare all 138 returned leaf
  values and exact types/schema with the authenticated historical receipt's
  corresponding sections. Reject E2=7, bool/float confusion, missing fields and
  altered enumeration totals. The sidecar E2 field derives from validated
  upstream E2 and is explicitly bound to the historical receipt's outer field.
- Emit a new local provenance record containing the source checkout, workflow
  reference identity, gate identity, exact commands/exits and raw-stream hashes.
  The workflow hash identifies the referenced target; the original YAML workflow
  is not executed. Local run/job IDs remain null; past CI/run/time identity is
  explicitly NOT_REAUTHENTICATED / NOT_ESTABLISHED.

The fixed workflow pin must be deliberately refreshed in a separately reviewed
mainline integration after the workflow is edited. Silently accepting a changed
workflow or baseline is not supported. The standalone helper's expected receipt
argument is trusted only after the outer CLI authenticates it.

## Actual tests and review

Final normal and optimized runs each passed **16 new unittest methods** and an
independent native replay of the **60 original methods**. Each real replay
matched all 138 stage-two fields. Raw output stream hashes were rechecked. The
new provenance regression also invokes the real original children internally;
these repeated tests are not new scientific evidence.

Test-first RED against a temporary permissive stub ran 15 methods and produced
167 assertion/subtest failures, with no unittest errors. The exact historical
log parser was extracted from the pinned workflow; only its logfile path was
redirected to disposable inputs. Its eight normal/optimized cases and the
candidate's corresponding eight cases reproduced all expected outcomes:

| Parser/mode | valid | 59 tests | FAILED then OK | duplicate summary |
|---|---:|---:|---:|---:|
| Historical normal | 0 | 1 | 0 | 1 |
| Historical optimized | 0 | 0 | 0 | 0 |
| Candidate normal | 0 | 1 | 1 | 1 |
| Candidate optimized | 0 | 1 | 1 | 1 |

One fresh read-only review found a P2 flaw in the initial candidate's provenance:
it read its own source hash after execution, potentially reporting a different
revision. A regression altered only a disposable gate copy after a real child
completed; it initially failed (`0 != 1`). In one fix pass, gate bytes were
captured before replay, checked again before success, and that captured identity
was recorded. The final 16-method suites pass, including this real-child
concurrency rejection. No other important finding remained. No second review
was substituted for the covering RED/GREEN checks.

## Reproduce and inspect

```sh
python3 -B -m unittest discover -s research/codex_a/r127_local_gates -v
python3 -O -B -m unittest discover -s research/codex_a/r127_local_gates -v
python3 -B research/codex_a/r127_local_gates/gate.py .
python3 -O -B research/codex_a/r127_local_gates/gate.py .
```

No package installation, network or Git write is performed by the gate. Missing
objects/files, changed identities or validation failures return BLOCKED/exit 1,
with no successful sidecar. `evidence.tar.gz` contains original RED logs, review
regression RED, final commands/raw logs/sidecars, historical/candidate log matrix,
five-source preservation checks and current queue inventory. Member SHA256 values
are in `evidence_members.json`; delivered source SHA256/Git blobs are in
`artifact_hashes.json`. `pins.json` records all five original source identities.

## Ownership, status and remaining work

Main's `R127_CI_P0_FAIL_CLOSED_HANDOFF_MATRIX_2026-11-10.md` explicitly states
that R mainline owns the workflow edit and scientific conclusion. All new files
therefore stay under this Codex A directory on an independent draft PR.
**The production workflow remains vulnerable and unchanged.** Mainline still
needs reviewed wiring/pin refresh, publish no-op/conflict handling, trusted CI
run/job identity, and optimized end-to-end workflow validation after free-quota
confirmation. Historical receipts must remain immutable.

No CI was dispatched and no billing/free quota is asserted. Python 3.12.14 was
used; the production workflow's Python 3.11, other environments, the full
repository and publication stage were NOT_RUN. Formal research reacceptance,
catalogue 05-003 closure, new human E2/E3 and external-team replication: zero.
R127 remains CLOSED_BOUNDED; R073/PESEN v0.1 remain unchanged. Numerical agreement
with a fixed receipt is engineering regression evidence, not new source-document
review, historical execution authentication or independent scientific prediction.

The open queue was rechecked with main's existing `audit_queue.py`; details are
in the archive. #21–#24 remain drafts, and new #25 is inventoried but its native
replay is NOT_RUN this round because the mainline R127 P0 handoff took priority.
Next: mainline disposition of this integration candidate and independent review
of #25, while preserving the existing #21–#24 evidence and merge boundaries.
