# R272 P0: read-only wrapper self-test mutation sensitivity audit

track: R+B
subflow: original239 12-002 scientific acceptance integrity
run_date_utc: 2026-11-02
initial_main_head: bed9c793fbdbacaa10fbe17204a52683e8dcd9a1
main_after_test_script_commit: 704dcb4574313bd29e4f95639e2adc49464e5500
target_key: (R+B,R272,2026-10-23-frozen-12-002,read-only-wrapper-self-test-mutation-sensitivity)
status: COMPLETE_LOCAL_MUTATION_AUDIT / P0_OPEN / PRODUCTION_NATIVE_NOT_RUN

## Actual evidence and question

The earlier read-only wrapper `research/validation/r272_preimage_first_readonly_gate_20261102.py` (Git blob `8722fd4388421e3b1f77c6648b4ed1b38088c4b0`) checks the archived generator source, prescore freeze and archived machine receipt Git blob before running a separate scientific checker. Its `--self-test` directly checks the mathematical checker and compares the mutated receipt blob to a constant. It does not invoke `verify_preimage` to establish that the three mandatory input-identity guards are actually executed. This run asked whether the existing self-test would detect removal of one guard.

The independent scientific checker source was taken from the existing local conversation attachment `r272_failclosed_independent_receipt_gate_20261102.py` and its SHA256 verified as `f7109f8f815d166128ca3429fb42ff3e7cac780d03fb78f8243aeabbd6fbb786`. The wrapper's source bytes were checked against the live main Git blob. The audit program is `research/validation/r272_wrapper_selftest_mutation_sensitivity_20261102.py`, Git blob `3e4e71f675421534429aefba375d7d563ad65c15`, SHA256 `4eca085d7b0559988f4409ec4de85d7362700b5bbfb1f08779f2642329029169`.

## Executed test

Environment: local CPython 3.13.5 standard library; temporary directories; deterministic six-bit artificial fixture; no random seed. The fixture's scientific checker validated the original CSV and results SHA256 pins, and the reconstructed receipt reproduced Git blob `85d36858911a7eb79c73c607cddf45ea88852a60`. The test uses synthetic stand-in source and freeze bytes, with their expected Git blobs set in memory to exercise the wrapper's `verify_preimage` path. It never represents these stand-ins as the original repository files.

Positive control: the unchanged wrapper accepted the intact synthetic fixture. Negative controls: the unchanged wrapper rejected a one-byte append to each of the synthetic source, freeze and archived machine receipt inputs, 3/3.

Mutation controls: create three separate disposable copies of the wrapper, each deleting exactly one mandatory `require` line. Each modified wrapper accepted the corresponding corrupted input. All three modified wrappers still reported `--self-test` PASS with exit code zero under ordinary Python, `python -O` and `python -OO`. Total: 3 removed guards, 3 direct wrong acceptances in the constructed `verify_preimage` scenario, 9 false-pass self-test executions. No historical source, freeze, archived result or workflow was modified.

Reproduction after obtaining the two pinned Python sources:

```sh
python research/validation/r272_wrapper_selftest_mutation_sensitivity_20261102.py \
  --wrapper research/validation/r272_preimage_first_readonly_gate_20261102.py \
  --gate /path/to/verified/r272_failclosed_independent_receipt_gate_20261102.py
```

The checker is currently stored in `research/validation/R272_P0_FAILCLOSED_CANDIDATE_20261102.zip`; the extracted member must have the pinned SHA256 before use. The code does not execute untrusted third-party code or call the original generator.

## Scientific interpretation and P0 disposition

Confirmed: **self-test mutation-sensitivity coverage defect**. The current wrapper's mandatory guards worked for the tested corruption cases. A future regression deleting one of them would pass the existing self-test. The test label `new_receipt_byte_guard_rejected=1` in the earlier self-test demonstrates a blob inequality, not a full rejection by `verify_preimage`.

This is a narrower claim than an actual false acceptance by the unmodified wrapper. No authentic full-checkout `--root` execution, isolated original-generator `--emit`, Actions run, or historical false CI result was observed. The original R272 optimized-mode assertion vulnerability and the production workflow's regeneration-before-preimage check and missing mandatory independent gate remain OPEN.

Required remediation: include a mutation-sensitive, actual `verify_preimage` negative test for source, freeze, CSV, results and receipt; retain ordinary/-O/-OO checks; test that removing each identity guard makes the regression suite fail; then run native `--root` and isolated regeneration on a trustworthy complete checkout. Review a mandatory production caller and trigger coverage before any workflow adoption. Do not edit the frozen generator or historical evidence.

## Original239, A data, coordination and cost

Read the live main ref, latest commits, original239 v7.8 crosswalk blob `36f24235901172642c46853298aebb421f1a3552`, and pending queue blob `3b96d46b3d88ccafd779a08509c3cfd0e435772f`. Parsed 154 pending rows: P0 27, P1 82, P2 45. R272 12-002 remains P0; formal queue net closure zero. All 12 Codex PRs remained open, including #1 and #3 for R257 S53; no competing R272 PR was found.

A scout reviewed the existing DF2011 source reconciliation `research/data_scout/A_DF2011_R074_PRIOR_DECODE_AND_SOURCE_DUPLICATE_STATUS_RECONCILIATION_2026-11-01.md`. Earlier fixed-source decoding already established 7,358 records; DF2011 belongs to the same Dal Bó and Fréchette 2011 original experiment as R074 (DOI 10.1257/aer.101.1.411), so it cannot count as a newly independent R073 experiment. Its row-level identity with R074 is still unknown. No new dataset was acquired, qualified or scored. R073 and PESEN v0.1 remain frozen.

Evidence level: internal nonblind synthetic E1 program audit. New real-human E2 = 0, historical E3 = 0, external-team replication = NOT_RUN. No paid data, API, cloud compute or Actions were invoked. Actual GitHub billing/free quota = NOT_VERIFIED. CI = NOT_RUN. The source audit and report were archived separately without changing other tracks or historical results.
