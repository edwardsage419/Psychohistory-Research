# R273 S69: two-target-bit paired ranking under source to target transfer

Date 2026-10-30 Asia/Singapore. Track r. Original R273 is CLOSED_BOUNDED_E1; this is an exploratory, internally nonblind E1 extension. New design frozen before new S69 score computation at commit 9051d6e27c1ef17ceff3b49883cbb274d7510871. Prior R273 expected risks and code were read before S69 design. No blind confirmatory claim.

## Question, unchanged mechanism and source

Original R273 protocol: protocols/R273_CROSS_POPULATION_27_WORLDS_1728_COMPLETE_SOURCES_PRESCORE_FREEZE_2026-10-23.md; original frozen commit 91abafbaf627dbf67f86208a82008a5be419e507. Source a and target b in {1/4,1/2,3/4}; four source Bernoulli(a) training bits followed by two independent target Bernoulli(b) test bits. SOURCE_ORACLE q=a, SOURCE_LAPLACE q=(K+1)/6, TARGET_ORACLE q=b. All three predictors and the Brier rule are unchanged.

Nine population pairs, 64 ordered six-bit source types each, 576 paired comparison rows. The original 1728 source rows were labelled separately for three models, so 576 paired states are reused across the two compared predictors and must not be interpreted as 576 independent real people or studies. Exact source weights use integer numerator over 4096. Each paired two-target score uses an integer numerator over 288. Strict paired score outcomes are L_BETTER, S_BETTER, TIE.

## Exact results

| Source a | Target b | Laplace minus source oracle population Brier risk | Probability finite paired test favors the higher-risk model | Ties |
| --- | --- | --- | --- | --- |
| 1/4 | 1/4 | +1/36 | 487/1024 | 0 |
| 1/4 | 1/2 | -1/72 | 105/256 | 0 |
| 1/4 | 3/4 | -1/18 | 349/1024 | 0 |
| 1/2 | 1/4 | +1/36 | 25/128 | 3/8 |
| 1/2 | 1/2 | +1/36 | 5/32 | 3/8 |
| 1/2 | 3/4 | +1/36 | 25/128 | 3/8 |
| 3/4 | 1/4 | -1/18 | 349/1024 | 0 |
| 3/4 | 1/2 | -1/72 | 105/256 | 0 |
| 3/4 | 3/4 | +1/36 | 487/1024 | 0 |

Same population a=b=1/4: source oracle population risk 3/16 versus Laplace 31/144. Even so, a two-label paired test favors the worse Laplace model with probability 487/1024, about 47.56%. For shifted a=1/4,b=1/2, Laplace has lower population risk by 1/72 but the two-label test favors the worse source oracle with probability 105/256, about 41.02%. At a=b=1/2, 3/8 of paired comparisons tie; a tie is neither correct nor wrong.

This is an exact finite artificial ranking error, conditional on the original Bernoulli generator and candidate pair. It does not estimate real human prediction uncertainty. The oracle source and target true probabilities are externally known to the mathematical evaluator and unavailable to an ordinary trained model.

## Execution and evidence

R route enumerated all 576 ordered six-bit states, exact integer weights and paired squared losses. Nine source weights each summed to 4096. Source and Laplace exact risk numerators matched original R273 closed forms in all nine worlds. A separate B route enumerated 15 grouped (K,J) cells per world, 135 total, using binomial multiplicities and independently derived risk expressions. All 158 persisted receipt fields matched; 8 deliberate mutation controls were rejected. A separate read of persisted CSV verified 576 unique labelled rows, all weights, both forecasts, both scores and strict outcome labels, with zero discrepancies. These checks ran in the tool's V8 runtime. Archived Node native CLI was NOT_RUN; CI NOT_RUN. External independent replication NOT_RUN.

Artifacts:
* protocols/R273_S69_PAIRED_TARGET_SCORE_RANKING_FREEZE_2026-10-30.md
* research/validation/r273_s69_paired_target_rank_20261030.js
* research/validation/R273_S69_PAIRED_TARGET_RANK_EXACT_RESULTS_2026-10-30.json
* research/validation/R273_S69_ALL_576_PAIRED_SOURCE_ROWS_2026-10-30.csv
* research/evidence_audit/b_r273_s69_grouped_oracle_20261030.js
* research/evidence_audit/B_R273_S69_GROUPED_ORACLE_AND_RECEIPT_AUDIT_2026-10-30.md

## A01 to A06 acceptance and limits

A01 PASS for finite question and fixed nine-world scope. A02 PASS for original fixed protocol, original model code and current frozen design, while original 1728 CSV byte identity was not rechecked. A03 PASS for V8 enumeration and independent grouped oracle; OPEN for native Node execution and full remote byte replay. A04 PASS for retained negative controls, tie outcomes and eight rejected mutations. A05 PASS for explicit artificial E1 and nonblind limits; real E2 and historical E3 are zero. A06 OPEN for broader scientific acceptance, while bounded incremental report and remote artifacts are archived.

R273 original CLOSED_BOUNDED unchanged. S69 is exploratory E1, not an upgrade to full R273 validation. No empirical probability calibration, external human data, or causal transferability claim. R073 frozen; PESEN v0.1 frozen. No paid compute or Actions invoked. Account billing and free quota not verified. Next: native Node source and receipt replay, then inspect R274 existing evidence before a new complementary finite question.
