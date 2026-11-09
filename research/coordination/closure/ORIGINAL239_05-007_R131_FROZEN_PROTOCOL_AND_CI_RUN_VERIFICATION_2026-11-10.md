# Original239 05-007 / R131: frozen protocol and historical CI independent metadata audit

Date: 2026-11-10 UTC. Track: closure. Read-only research checks followed by this independent archival note. Baseline main SHA: `7a2e39edf9e35be80b12ac510fa02310c452471a`.

## Directly checked repository records

* Frozen protocol: `protocols/R131_TAYLOR_JONKER_1978_STATIC_ESS_DYNAMIC_COUNTEREXAMPLES_AND_FINITE_DRIFT_FREEZE_2026-10-20.md`, Git blob `d85ab6019dfb82c4254aa98016b81414932c43d1`.
* Historical CI receipt: `research/R131/R131_PHASE_A_1978_63_TEST_504_INVASION_SOURCE_FINITE_DRIFT_CI_ACCEPTANCE.json`, Git blob `4895b340c478165bf9307fa6a97d7fa448a1b88c`.
* Historical R131 status: `research/R131/R131_FINAL_ACCEPTANCE_STATUS.json`, blob `3fa4bc6657ae38ee306e106dbd98f21edd48451b`.
* Earlier closure mathematics note: `research/coordination/closure/ORIGINAL239_05-007_R131_INDEPENDENT_MATH_ITEMWISE_AUDIT_2026-11-10.md`, blob `ccef1b57bb0b04982ddc7166680593b0c0494ccb`.
* Concurrent R-track provenance correction: `research/R131/R131_ORIGINAL_PAPER_MUTANT_WITNESS_PROVENANCE_AUDIT_2026-11-10.md`, blob `07959ae7ae1cfbe21264ccd93506ce051d53ebed`. The original p153 witness q=(18,17,0)/35 and project q=(0,0,1) must be distinguished. This R-track correction already exists; no duplicate source attribution change is made here.

## New verification against live GitHub Actions API

Independently queried historical run `39360828291` and its jobs via GitHub REST GET. Run status `completed`, conclusion `success`, event `push`, head SHA `b71f54b45ada4cc646993130c17fc5bab83a3b18`, attempt 1, created `2026-10-20T02:47:36Z`. One reported job: `original-1978-ESS-stability-contradictions-and-finite-Moran`, job ID `118426358465`, `completed/success`. GitHub's job metadata marks the 63-test step, independent 504-invasion-equalities replay step, and receipt commit step as `success`. This confirms that the historical CI execution record exists and completed successfully. Job logs, exact test stdout, and SHA256 of the three files were **not** independently replayed or validated in this audit. Historical receipt records 63 tests, 0 failures, and three SHA256 digests; these are receipt assertions, not newly reproduced local results.

## Protocol and inference checks

The frozen protocol specifies the 1978 source matrices, two independent invasion calculation paths, a minimum 45 unittest cases, 504 exact comparisons, exact Jacobian cross-checks, and finite Moran N=5 fixation 16/211. The historical receipt reports 63 tests and 504 comparisons, and the live CI job metadata is consistent with the recorded execution. This verifies a narrower A01 protocol existence and A03 historical CI metadata gate; it does not prove all test semantics or reproduce all hashes.

The frozen protocol selects project witness q=(0,0,1) for the second matrix. The R-track original-source note documents the paper's different printed witness. Accordingly the project witness remains mathematically admissible and must be explicitly attributed as project-selected. This audit makes no historical rewrite and no claim of prospective registration for earlier historical research.

A01: PARTIAL, frozen protocol directly inspected; chronology relative to first calculation not independently established. A02: PARTIAL, original source direct inspection was documented in the separate R-track note, not repeated here. A03: PARTIAL, historical GitHub CI run and step statuses directly confirmed, exact logs and file SHA256 verification OPEN. A04: PARTIAL, negative ESS/dynamics cases documented; complete negative test audit OPEN. A05: PASS for E1-only inference boundary. A06: OPEN for full itemwise independent closure.

**Outcome:** one additional historical CI existence and success gate verified using live metadata; frozen protocol content independently checked. Original239 05-007 remains provisional and the original 154-row queue is unchanged. No new E2/E3, no new test execution, no new original-source inspection, no independent external replication. R131 historical CLOSED_BOUNDED remains unchanged. No Actions run was triggered.

Next priority: independently validate the three file SHA256 digests and original test program output against frozen protocol, then decide itemwise gate with explicit A01–A06 outcomes. The container's direct public network request failed with DNS resolution, so no local bytes were obtained from raw.githubusercontent.com in this audit. No extra paid resources used.
