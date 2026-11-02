# R272 P0: preimage-first read-only audit candidate and machine receipt identity

track: R+B
subflow: original239 P0 scientific integrity
run_date_utc: 2026-11-02T05:40Z
observed_main_head_at_start: 6e40ac752af3e30de73cd79fae1c52122acb4049
original239_target: 12-002 Out of Sample Prediction / R272
freeze_commit: 52f84dbfbe8563cf5c9a491e67d5e320223e0a56
status: COMPLETE_LOCAL_CANDIDATE_TESTS / PARTIAL_NATIVE_ARCHIVE / PRODUCTION_P0_OPEN

## Inputs and identity

Read main branch API, recent commits, all 12 open PR summaries, original239 crosswalk blob 36f24235901172642c46853298aebb421f1a3552 and pending CSV blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f. The CSV contains 154 pending entries, P0=27, P1=82, P2=45. PR #1 and #3 remain open and concern R257 S53, not this R272 implementation. R272 original generator Git blob 13843eecf2f9f05c19ee5545bdb224f58313f367, prescore freeze Git blob 9fbdb0078a58c4a9c0a548643227e30da5731119 and workflow Git blob 3132b08cf4ee64b55f5112d2249894ea0ec9d42d were fetched on main. No production caller changes observed.

The locally available independent checker is r272_failclosed_independent_receipt_gate_20261102.py with SHA256 f7109f8f815d166128ca3429fb42ff3e7cac780d03fb78f8243aeabbd6fbb786. Its identity relative to the binary GitHub ZIP member has not been independently rechecked in this run. The new candidate pins that exact local checker SHA256 and requires original generator/freeze blob identity, CSV and result JSON byte hashes, scientific content and full machine receipt Git blob 85d36858911a7eb79c73c607cddf45ea88852a60.

## New bounded finding

The earlier independent candidate checks source CSV and result JSON against fixed SHA256 pins. Its receipt validation checks semantic JSON fields and hashes but does not pin the receipt's original serialized bytes. A receipt with one appended newline is accepted by its verify(..., pins=True), even though the Git blob changes. This is an archived machine-receipt **byte-identity coverage gap**, not evidence that a false scientific claim can pass. The new wrapper adds a mandatory fixed receipt Git blob check.

## New candidate

The R-owned standalone read-only wrapper research/validation/r272_preimage_first_readonly_gate_20261102.py first authenticates checked-out original source, frozen protocol and three archived preimages, then calls the pinned independent checker and checks for file mutation. Optional --regenerate copies the pinned generator into a disposable temporary directory, executes it there, independently checks the regenerated artifacts, and requires exact byte equality to the authenticated preimages. It never writes to original archived files and does not change the production workflow. The --root and --regenerate paths require a complete trusted checkout and the extracted checker source.

Local environment: CPython 3.13.5 standard library; no random seed. Reconstructed 61,489-byte CSV, 4,402-byte result JSON and 413-byte receipt reproduce the three documented Git blob identities 8fbbc73d239765f5c66395af1bcf9cf7a8df1f41, db3ca11ae224af52c2caf385c898e24aaa0cc54b and 85d36858911a7eb79c73c607cddf45ea88852a60. The pinned scientific checker returned PASS for 576 finite artificial sources and nine worlds. The new wrapper self-test passed under python, python -O and python -OO. Each mode: one positive, one original receipt whitespace acceptance counterexample, one new receipt byte-guard rejection, one scientific corruption rejection with updated receipt hash. Three modes yielded 3 positive and 6 new rejection executions; do not equate counts with independent empirical validation.

Actual native --root against a full remote checkout: NOT_RUN. Actual isolated generator --emit from pinned original source: NOT_RUN. GitHub Actions: NOT_RUN. No frozen source/protocol/receipt/workflow changes; no production P0 closure.

## A public data scout

English source scan of Romero and Rosokha (2023) Econometrica DOI 10.3982/ECTA17482 (publisher supplement lists 197 MB data/programs), and Dal Bó and Fréchette (2011) DF2011 panel data as distributed by datafsm (documented 7,358 rows; fields treatment, id, game, period, choice, other.choice). DF2011 is a promising independently identifiable participant/game/period source, but original data bytes, ID uniqueness semantics, opponent pairing, licence terms and R073 frozen compatibility were not checked. Candidate only; new qualified R073 dataset=0; new E2/E3 scores=0.

## Scope and next

Evidence: INTERNAL_NONBLIND_FINITE_ARTIFICIAL_E1 program audit only. No external-team replication. Pending original239 queue net closure 0. R257 S53 blind-order failure remains recorded; R333 to R340 composite caller remains open. R073 and PESEN v0.1 frozen. No classification, fusion or personal decision product development.

Next: obtain complete trusted checkout and verify candidate ZIP member identity, execute both independent --root and read-only wrapper --root --regenerate in ordinary and optimized Python, and preserve actual stdout, stderr and return codes. Independently review a mandatory preimage-first production caller with archive and checker path trigger coverage before any workflow modification. No Actions triggered because free billing quota was not independently verified. No purchases or paid APIs; account billing status NOT_VERIFIED.
