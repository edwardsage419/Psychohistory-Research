# R333 to R340 historical claims and mandatory acceptance coverage audit

Date: 2026-11-01 UTC. Track: R with B scientific evidence audit. Status: PARTIAL. Initial observed main: `0278556e1c0a34aac0d69e7c2c4805acd1b1ae27`. All work is read-only except additive audit artifacts.

## Question and evidence

The existing candidate entrypoint `research/evidence_audit/r333_r340_acceptance_entry_20261101.py` pins four strict validators and executes eight model checks in normal and optimized Python. Its four authenticated validators check each model's original source, CSV, and mathematical JSON. This audit asks whether the archived **historical machine receipts and final scientific status documents** are covered by that gate, and independently checks their recorded historical CI identities.

Read the exact entrypoint Git blob `9822418253c6a2888119c2a823ffee62dd945d7c`, the four validator blobs `fce37d846c96598f491a155be684c3b009f7d7a0`, `bc025931c6bfaf3489ba3dcf91054a1e32fdaa29`, `8c42c0e7f53a6ac855d295d0ee72c5618dc664d9`, `bdd44dbc0422b1e4bd33b6bc5281e00227cce865`, all 16 archived `Rxxx_MACHINE_RECEIPT.json` and `Rxxx_FINAL_ACCEPTANCE_STATUS.json` files, and eight historical GitHub Actions run objects and their job collections. Exact 16 JSON Git blobs, CI head commits, and run IDs are preserved in `research/evidence_audit/B_R333_R340_HISTORICAL_CLAIMS_CI_AUDIT_2026-11-01.json`.

## Confirmed results

All eight historical run objects report `completed/success`. Each has exactly three completed successful jobs named `independent`, `python311`, `python312`: **8 runs, 24 successful jobs**. Their `head_sha` matches the archived source commit in the corresponding final acceptance status, and the machine receipt records the same run ID, bounded E1 grade, and source/protocol lineage. R334 uses the distinct `verified_source_commit` field, which was handled explicitly. The historical files state that real-human E2 and historical E3 are unestablished. No claim of independently rerunning those old jobs is made.

Historical run IDs: R333 40047349488; R334 40051279908; R335 40051490899; R336 40055738338; R337 40055959491; R338 40059210892; R339 40059401269; R340 40063363405. Official run links follow the pattern `https://github.com/edwardsage419/Psychohistory-Research/actions/runs/<run_id>`. Read-only run and job metadata were checked on 2026-11-01.

**Additional acceptance coverage gap:** the current unified candidate and its four validators never read or pin the eight `MACHINE_RECEIPT.json` or eight `FINAL_ACCEPTANCE_STATUS.json` files. Their 16 Git blobs are outside the input dependency set. Altering one of these historical claim files while keeping the three pinned source/CSV/JSON inputs unchanged therefore cannot change the gate's checks through its documented code paths. This is a **static input nondependence result**. An actual native mutated-checkout control was **NOT_RUN**. It is a metadata and scientific-claim coverage gap, with no evidence of real archived data tampering and no newly demonstrated numerical error.

The eight historical CI success records confirm what GitHub reported at those commits. They do not establish original optimized-mode safety, blind validation, empirical predictive performance, external independent reproduction, or that a later candidate gate is mandatory. The original optimized-mode false-accept issue remains **OPEN**. The unified gate's complete native 16-child checkout execution remains **NOT_RUN**. Production caller integration and a trusted entrypoint pin remain **NOT_ESTABLISHED**.

## Recommended acceptance contract

Keep historical machine and final status files immutable. Add a separate, source-pinned claim-receipt gate requiring all 16 exact historical Git blobs and checking their model IDs, protocol/source commits, CI run identity, E1 grade, and E2/E3 boundaries. It should fail on a changed or missing historical claim file and on duplicated or mismatched identity fields. Keep mathematical source/CSV/JSON validation as an independent mandatory dependency. Pre-freeze a negative test that changes only a machine receipt's CI conclusion or a final status's evidence grade while leaving source/CSV/JSON untouched. It must fail at the claim gate, even when the old mathematical gate still passes. Review actual production caller wiring before any P0 closure.

This audit supplies source inspection and GitHub run/job metadata, not a new runnable claim gate or an executed native mutation test. It does not alter original files or frozen protocols.

## Other work and priority

Original239 latest crosswalk v7.8 blob `36f24235901172642c46853298aebb421f1a3552` and itemwise pending queue blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f` were rechecked. Queue remains 154 items: P0 27, P1 82, P2 45; net closure 0. Codex PR #1 and PR #3 were checked as open/unmerged; PR #3 covers R257 S53 mathematical receipts and remains separate. No duplicated repair or PR merge.

A-track candidate: University of Portsmouth, Chugunova, Luhan and Nicklisch (2020), DOI `10.17029/0414a771-06a4-4df3-b694-72f4907ab426`. Official metadata confirms a 21.5 KB CC BY README and a 4.66 MB CC BY Stata .dta dataset for migration between sanctioning institutions. The README download returned HTTP 403 during this run, so actual columns, subject/session/time keys, file checksum, and R073 eligibility are **BLOCKED/UNKNOWN**. The study addresses public-goods institution choice; it has not been shown to meet the frozen continuous dyadic repeated-game criterion. No raw participant data were fetched or committed.

Environment: GitHub read-only connector, public English-language institutional data page; no new CI or Actions dispatch, no paid API, no purchased data, no GPU or cloud rental. GitHub billing and free quota **NOT_VERIFIED**. New E2=0, new E3=0, external team reproduction=0. R073 and PESEN v0.1 remain frozen. Next highest-value work: native complete checkout execution of the existing eight-model gate, followed by an explicitly mandatory claim-receipt dependency and source-first original239 itemwise scientific disposition.
