# R120 original239 04-003: third-method exact integer-grid re-audit

Date: 2026-10-24. Evidence status: **PASS_BOUNDED_INTERNAL_THIRD_METHOD_EXACT_E1**. The R120 2026-10-19 study and frozen protocol are reused unchanged. No new R identifier.

## First-party source and original scope

Kempe, Kleinberg and Tardos (2003), *Maximizing the Spread of Influence through a Social Network*, DOI 10.1145/956750.956769. Original author-hosted paper: https://www.cs.cornell.edu/home/kleinber/kdd03-inf.pdf . Theorem 2.5 concerns expected influence submodularity; Claim 2.6 establishes equal full terminal activated-set distributions for independent, once-drawn uniform thresholds and one incoming live edge per target. The claim does not establish empirical human adoption or independently measured influence weights.

The new pre-execution protocol was committed as `5be1c64271e6ef1152e4b2e3059f307b211d5bfc` before any new auditor source or data was committed.

## Actual third-method implementation and raw evidence

New auditor: `research/validation/verify_r120_independent_integer_grid.py`.
Complete independently enumerated raw terminal-set distribution:
`research/validation/R120_INTEGER_GRID_530_CASE_TERMINAL_DISTRIBUTIONS_2026-10-24.csv`.
Raw CSV SHA256: `189a7a857cfa59e318e254c88ec3c7edb1d89f6caf6d197945ac1c3d00ad4fea`.

For rational edge weights with common denominator L, every possible incoming-subset influence is a multiple of 1/L. The auditor uses all L equally likely threshold cell midpoints for each node, holds each threshold fixed for the entire progressive cascade, and counts terminal node masks with exact rational probabilities. This procedure does not call the original breakpoint-interval or live-edge algorithms to compute its own results.

The finite exhaustive family consists of all 1, 4, 64 loop-free labeled directed graphs with n=1,2,3, each edge weighted 1/target-indegree and every seed subset. It yields 69 graph instances, 530 graph-seed cases, 590 nonzero terminal-set CSV rows. All 530 independent full distributions equal both original R120 implementations exactly, with normalized mass 1. Five additional nonuniform seed/chain/cycle fixtures match, including 3/2, 5/4, 11/4, 25/12, 7/4 expected activation counts.

The independent-Bernoulli-inbound negative control yields target activation 5/8 versus correct 3/4. The program rejects modified CSV bytes and a deliberately wrong source Git blob SHA. All three original R120 file identities were verified with Git blob hashing.

## GitHub Actions execution and failure retention

Initial run https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40083352028 completed **failure**. Both Python jobs raised a local auditor iteration error: iterating a dictionary without calling `.items()`. The error occurred before the 530-case test. This failure is retained.

A single-line source repair was committed as `124c18bae7bd9fe94f2855b92e8d1b70a9f25779`. Subsequent run https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40083392282 completed **success**. The Python 3.11 and 3.12 jobs each printed the exact same receipt: 69 graphs, 530 cases, 590 distribution rows, five nonuniform fixtures, three source identity checks, one negative control and two tamper rejections. Both jobs then ran the original 45 unit tests, each with zero failures. Original R120 run https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39254086771 also completed success on 2026-10-19.

This is method-independent **within the same project**, using constructed mathematics and the original author's theoretical model. It is not an independent external research-team reproduction. Exact fractions require no confidence interval or calibration; no human sample was evaluated.

## Scientific boundaries and next gate

Only the finite exact mathematical scope receives E1 acceptance. Human E2 prediction added: 0. Historical E3 evidence added: 0. Original large coauthorship network experiments, inferred edge weights, original greedy optimization benchmarks, individual causal adoption and out-of-sample probability calibration remain unreplicated. Early R001 to R064 ZIP content reuse audit remains open. R073 and PESEN v0.1 remain frozen. This acceptance may support strict reattribution of original239 item 04-003 only; it does not imply all original239 science is complete.
