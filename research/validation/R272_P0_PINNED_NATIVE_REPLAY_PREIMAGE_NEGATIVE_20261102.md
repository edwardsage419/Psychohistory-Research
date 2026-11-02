# R272 P0 pinned native source replay, read-only preimage rejection and original-generator masking counterexample

track: R+B
subflow: original239 12-002 scientific integrity
run_date_utc: 2026-11-02
starting_main_head: 608cff4116fc8a5996f2802dd733075fc871a84a
code_commit: 05bad52fc63463140e45391d7823351bb480810e
target_key: (R+B,R272,2026-10-23 prescore freeze,pinned native source replay and preimage masking)
status: COMPLETE_LOCAL_PINNED_SOURCE_REPLAY / PARTIAL_PRODUCTION_ACCEPTANCE / P0_OPEN
evidence_scope: INTERNAL_NONBLIND_FINITE_ARTIFICIAL_E1
ci_status: NOT_RUN
billing_checked: ACCOUNT_BILLING_AND_FREE_QUOTA_NOT_VERIFIED

## 1. Research question and fixed input identity

Question: Can the exact archived R272 original generator, frozen protocol, independent receipt checker and preimage-first wrapper be executed together under normal and optimized CPython, and can the real generator mask preexisting archive corruption when called before verification?

Fetched the authentic original generator and prescore freeze from main through the connected GitHub repository interface. Materialized their full text into an isolated local directory and independently computed Git blob SHA1 over the exact bytes. Both matched main:

* `research/R272/r272_exact_train_test_prediction.py`: `13843eecf2f9f05c19ee5545bdb224f58313f367`
* `protocols/R272_OUT_OF_SAMPLE_9_BERNOULLI_WORLDS_576_FULL_SOURCE_PRESCORE_FREEZE_2026-10-23.md`: `9fbdb0078a58c4a9c0a548643227e30da5731119`

The wrapper was the unchanged main blob `8722fd4388421e3b1f77c6648b4ed1b38088c4b0`. The locally supplied independent checker matched SHA256 `f7109f8f815d166128ca3429fb42ff3e7cac780d03fb78f8243aeabbd6fbb786`. The checker is distributed in the prior R272 candidate ZIP. No generator, freeze, original archive or production workflow was edited on GitHub.

## 2. Actual native execution

Environment: Linux local container, CPython 3.13.5, standard library only. All computation deterministic, seed N/A. Original generator `--emit` executed inside a disposable directory containing the authenticated generator and freeze. The three emitted artifacts exactly matched the documented Git blobs and byte counts:

| Generated artifact | Bytes | Git blob SHA1 | Result |
| --- | ---: | --- | --- |
| R272_ALL_576_ORIGINAL_TRAIN_AND_TEST_SOURCES.csv | 61489 | `8fbbc73d239765f5c66395af1bcf9cf7a8df1f41` | PASS |
| R272_EXACT_RESULTS.json | 4402 | `db3ca11ae224af52c2caf385c898e24aaa0cc54b` | PASS |
| R272_MACHINE_RECEIPT.json | 413 | `85d36858911a7eb79c73c607cddf45ea88852a60` | PASS |

A new standalone regression, `research/validation/r272_pinned_native_replay_and_preimage_negative_20261102.py`, executed all of the following in **each** of Python normal, `-O` and `-OO` modes:

1. The actual archived generator `--test`, exactly **83 tests**, exit 0.
2. The pinned independent receipt gate CLI `--root`, PASS for 576 sources, nine worlds and 8640 fields.
3. The unchanged read-only wrapper `--root --regenerate`, PASS with `checked_archived_preimage=true`, `isolated_regeneration_compared=true`, and `original_archives_untouched=true`.
4. Appending one newline separately to the original generator, prescore freeze, source CSV, result JSON and machine receipt. All **five** corrupted-input runs exited nonzero with explicit `FAIL:`, preserving the corrupted input bytes.

Totals: 249 native unittest executions across three modes, three positive independent gate calls, three positive wrapper runs and 15 correctly rejected corrupted-input calls. Counts are repeated execution checks, not independent experiments.

A further negative used the actual pinned generator. A corrupted source CSV was rejected by the wrapper before any regeneration. Running the original generator `--emit` first then restored the exact historical bytes, and the wrapper subsequently returned PASS. This is an **executed original-generator masking counterexample**, stronger than the prior synthetic-only order-of-operations demonstration. It confirms a workflow ordering hazard; it does not show that historical CI ever encountered a corrupted archive.

The regression script itself was run locally and returned PASS. Its local and remote Git blob is `9b8a5a566b7f48c7e72ba34505d49eebe3a94b44`. The script only reads the supplied root and uses temporary directories for generation, mutation and comparison.

## 3. Exact limits and production decision

This was a **byte-authenticated local reconstruction of the source and freeze**, with generated archive bytes matching GitHub history. The three historical archive preimage files were **not independently downloaded from the remote checkout**, and the complete remote repository was **not cloned**. Thus this run verifies native generator reproducibility and checker behavior on byte-identical reconstructed artifacts, not an independently captured historical preimage in a full checkout.

The current production workflow `.github/workflows/r272-exact-train-test-oos-e1.yml` remains Git blob `3132b08cf4ee64b55f5112d2249894ea0ec9d42d`. Its original `--emit` before audit, archive-path trigger omissions, `assert` checks, write permission and missing mandatory independent gate were previously confirmed and are still unmodified. No GitHub Actions execution was initiated. The successful candidate wrapper is **not** a production P0 closure.

Acceptance still requires an independently reviewed mandatory production caller that authenticates checked-out preimages before mutation, runs the pinned independent checker, regenerates in isolation, propagates failure under optimized Python, covers relevant paths and never silently overwrites original archives. Separate review of write permissions and verified free CI eligibility is required before any Actions run.

## 4. Original239, A public data and B scientific evidence

Re-read original239 v7.8 crosswalk Git blob `36f24235901172642c46853298aebb421f1a3552` and pending queue Git blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f`. Pending count remains 154: P0=27, P1=82, P2=45. R272 12-002 remains provisional and P0. Net formal closure=0.

Twelve Codex PRs were open when checked; #1 and #3 concern R257 S53 and remain unmerged. The R257 blind-order failure remains historical; no R272 competing PR was identified. Latest theory/market commits were inspected and do not claim adoption of this production caller.

A data scout checked the English original deposit record for Kim (2023), *The Effects of Time Preferences on Cooperation: Experimental Evidence from Infinitely Repeated Games*, ICPSR/AEA data DOI `10.3886/E152261V1` (https://doi.org/10.3886/E152261V1). The record describes an original human repeated prisoner's dilemma experiment, three treatments, four sessions per treatment and 14–20 participants per session. Candidate only: data files, participant/session IDs, license, existing-R duplication and frozen R073 compatibility were not verified. DF2011 was already decoded and identified as the same study as R074; it is excluded as a newly independent R073 experiment. New qualified dataset=0; new R E2=0; E3=0; external-team reproduction=0.

R073 and PESEN v0.1 remain frozen. No R classification, fusion or personal decision product work was performed.

## 5. Archive, cost and next action

Output code: `research/validation/r272_pinned_native_replay_and_preimage_negative_20261102.py`
Output report: this document.
Original source, freeze, archived CSV/JSON/receipt and workflow: untouched.
No paid papers, APIs, GPU, cloud service or CI runs. Actual account billing and GitHub free quota remain unverified. The only external data access was read-only public sources and existing GitHub repository content.

Next action: review and implement a **mandatory preimage-first caller** through the authorized integration route, with failure propagation and path coverage; then validate against an independently obtained complete remote checkout. Maintain R272 P0 OPEN until production caller acceptance. Continue R333–R340 composite caller review and R257 S53 blind failure independently.
