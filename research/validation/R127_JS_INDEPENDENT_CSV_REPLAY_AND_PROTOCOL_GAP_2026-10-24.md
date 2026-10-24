# R127: additional independent CSV replay and frozen-protocol discrepancy

Date: 2026-10-24. Track: R-series main / B internal method audit. Original239: 05-003. Status: **ADDITIONAL_FINITE_E1_REPLAY_PASS_WITH_OPEN_ACCEPTANCE_BLOCKERS**. This note supplements the interim report and does not supersede it.

## Concurrent-write preflight and provenance

Before writing, read latest main commits, original239 crosswalk v7.6, pending 157 queue, existing R127 frozen protocol, original Python source and tests, archived third-method verifier, workflow, CSV and interim report. Other concurrent tracks had added `theory/TH012_...` and `research/market/MKT009_...` at HEAD `17a9dfa0a889869e398c40addc68a3b990962e2f`. This is a new path and does not alter their files. Original R127 source Git blob `6964fa57e291e719e8cc071cc3a70d73836363e4`; archived CSV blob `2a6706dcb047a5bf64f91651a8217d1d8009aa2c`.

## Actually executed independent calculation

A separate JavaScript enumeration in the connected execution environment fetched the complete archived CSV from GitHub and rebuilt each row without invoking the Python verifier or R127 model helpers. The enumerator used mixed-radix enumeration of every ordered profile in `{1,...,7}^n` for n=2,3,4, and separately calculated `6 + 2*min(profile) - own_effort` for every individual.

Observed: CSV 54,783 characters, 2,793 data rows, by n: 49, 343, 2,401; 10,731 person payoff cells. Every archived CSV row matched the independently constructed expected row in the original order; **zero row mismatches**. An independent exhaustive enumeration of opponent profiles of lengths 1,2,3 covered 399 profiles and 2,793 own-action alternatives; all 399 had the unique best action equal to the minimum opponent action, with zero exceptions. A one-row synthetic mutation was detected by direct byte-string inequality. The frozen CSV's existing SHA256 `821f785bf21a96eae5b65d1200389a5a2baa45ad63e5a115e48505051a2e9df4` was inherited from the earlier report; this JavaScript replay checked the retrieved bytes against the exact regenerated text, **not** an independently recomputed cryptographic SHA256.

These results establish a second computational check of the finite constructed dataset and analytic best-response formula. They do not establish that the archived Python verifier executed successfully, that the original Python model produced matching outputs in a new runtime, or that 60 historical tests reran in CI.

## Discovered frozen-protocol discrepancy

The precommitted `R127_THIRD_METHOD_INTEGER_TENT_BEST_RESPONSE_PROTOCOL_FREEZE_2026-10-24.md` explicitly requires the archived row to contain `n, efforts, integer payoff numerators, minimum and exact comparison flag`. The archived CSV header is exactly `group_size,efforts,minimum,payoff_numerators`: **no per-row exact comparison flag is present**. The Python verifier compares outputs at runtime, but that is a separate artifact from the required row-level archived flag. This is a documented **PROTOCOL_ARCHIVE_NONCONFORMANCE**, not silently accepted as equivalent.

Acceptable next action: preserve original frozen protocol and raw CSV; after independently executing the unchanged original source, write a separate supplementary, uniquely named row-level comparison receipt with each row's comparison result and source identity, or record a transparent deviation with explicit reduced acceptance scope. Do not rewrite the frozen protocol or relabel the existing CSV as compliant.

## CI and scientific acceptance gate

The GitHub connector's commit-run lookup filters pull-request runs and returned no matching run for the push commit `d58f71bceacc08fba2ae8b0ce478dc51e54900e3`. Combined commit statuses also returned an empty list. No accessible run ID, job conclusion or log was independently verified. **CI_VERIFICATION_PENDING; R127_FORMAL_ACCEPTANCE_PENDING; original239 pending count remains 157.**

New E1: internal constructed-data replay only. New E2 human out-of-sample evaluation: zero. New E3 historical evaluation: zero. The source's printed 107 participant aggregates are not individual microdata. No external research-team replication. R073 and PESEN v0.1 files were not edited. No new paid resources, CI jobs or external computation were initiated for this supplementary replay.
