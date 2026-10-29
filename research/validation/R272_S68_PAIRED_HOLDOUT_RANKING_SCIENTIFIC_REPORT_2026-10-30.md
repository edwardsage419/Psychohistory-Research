# R272 S68 scientific report: finite paired holdout ranking reversal

Date: 2026-10-30 Asia/Singapore. Design freeze: edacaa60498e9a53043db14dd7eb0531d995062b. Original R272 freeze: 52f84dbfbe8563cf5c9a491e67d5e320223e0a56. Baseline before freeze: 3d5349f5505679492ee324f8b47d028476b1fc7b.

## Question and source
For three frozen R272 Bernoulli p values (1/4,1/2,3/4), four training bits and two truly independent test bits, compare the *same two heldout labels* for each of three frozen predictor pairs. Nine p/pair comparisons, 64 ordered six-bit sources each, 576 comparison-labelled rows. Within p all pairs reuse the same primitive 64 sources, so these are not 576 independent trials.

D = first predictor's mean test Brier minus second predictor's mean test Brier. D>0 means first is worse on the observed two-bit test. A strict wrong ranking means D and E[D] have opposite signs. Ties D=0 are kept separate.

## Exact results
| p | first vs second | E[D] | P(first wins) | P(tie) | P(first loses) | P(strict wrong ranking) |
|---|---|---:|---:|---:|---:|---:|
| 1/4 | MLE vs Laplace | 11/576 | 857/2048 | 27/128 | 759/2048 | 857/2048 |
| 1/4 | MLE vs half | -1/64 | 857/2048 | 27/128 | 759/2048 | 759/2048 |
| 1/4 | Laplace vs half | -5/144 | 857/2048 | 27/128 | 759/2048 | 759/2048 |
| 1/2 | MLE vs Laplace | 5/144 | 5/32 | 3/8 | 15/32 | 5/32 |
| 1/2 | MLE vs half | 1/16 | 5/32 | 3/8 | 15/32 | 5/32 |
| 1/2 | Laplace vs half | 1/36 | 5/32 | 3/8 | 15/32 | 5/32 |
| 3/4 | MLE vs Laplace | 11/576 | 857/2048 | 27/128 | 759/2048 | 857/2048 |
| 3/4 | MLE vs half | -1/64 | 857/2048 | 27/128 | 759/2048 | 759/2048 |
| 3/4 | Laplace vs half | -5/144 | 857/2048 | 27/128 | 759/2048 | 759/2048 |

At p=1/4, MLE has a higher population future Brier than Laplace, yet the observed two-bit test prefers MLE with probability 857/2048 (41.8457%). At p=1/4, MLE is better in population than the constant-half predictor, yet the two-bit test prefers the constant with probability 759/2048 (37.0605%). At p=1/2, MLE is worse in population than constant-half, but a two-bit test incorrectly prefers MLE with probability 5/32 (15.625%) and ties with probability 3/8 (37.5%). A paired finite test can therefore produce a directionally misleading model ranking even when the test labels were strictly held out.

All nine exact variances, second moments and directional probabilities are in the persisted JSON. Exact enumeration route R and independent 15-cell Binomial(4,p)×Binomial(2,p) route B agree on 63 exact metrics. Source mass sums to 1 for each p/pair. Identity forecast and reversed sign controls pass.

## Evidence and acceptance
The new question was frozen before this run's paired sign results were calculated. The researcher had already read original R272 population risks and model definitions. Therefore the S68 analysis is **nonblind internal E1**. The original R272 CLOSED_BOUNDED E1 acceptance is unchanged. This result does not establish the empirical probability of misranking in any real human or historical population.

A01 PASS bounded finite question; A02 PASS original pinned R272 sources and frozen protocol; A03 PARTIAL R script V8 executed and remote CSV/JSON replay checked, independent Python selftest native PASS, but archived Python native CLI on the actual remote persisted files NOT_RUN; A04 PASS ties and negative controls preserved; A05 PASS E1 only, E2/E3 zero; A06 OPEN full independent native persisted-file CLI and external replication. S68 final status: PARTIAL_EXPLORATORY_E1.

Sources: protocols/R272_S68_PAIRED_HOLDOUT_RANKING_FREEZE_2026-10-30.md; research/R272/r272_exact_train_test_prediction.py; research/validation/r272_s68_paired_holdout_ranking_20261030.js; research/validation/R272_S68_ALL_576_COMPARISON_SOURCE_ROWS_2026-10-30.csv; research/validation/R272_S68_PAIRED_HOLDOUT_EXACT_RESULTS_2026-10-30.json; research/evidence_audit/b_r272_s68_independent_binomial_oracle_20261030.py.

No GitHub Actions launched, no new paid service or data access. R073 and PESEN v0.1 remain frozen.
