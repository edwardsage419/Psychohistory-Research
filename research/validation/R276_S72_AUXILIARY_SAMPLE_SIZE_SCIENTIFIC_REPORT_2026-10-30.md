# R276 S72: auxiliary measurement sample size and finite MAP classification

Date: 2026-10-30 Asia/Singapore. Original catalogue 12-006. Original R276 remains CLOSED_BOUNDED_E1_THREE_PARAMETER_STRUCTURAL_IDENTIFIABILITY. This extension is EXPLORATORY_E1_NONBLIND, not a new formal acceptance.

## Freeze, provenance and methods

Read original R276 protocol, source, results, acceptance and R275 handoff before design. Original freeze commit 58e192c523cc87b4fd4f6b9758af118d620a1951. New S72 protocol was committed first as 8e3eb673efa5daeddf1c5defe03ae205a2aa9429. The earlier m=2 result 11/16 was known before this freeze. The fixed new grid m=0..8 and descriptive 9/10 threshold were specified before new S72 scores.

The three original parameter points are A theta1=1/2, B theta1=1/4, C theta1=1, all with theta1*theta2=1/4. Four Y observations carry identical likelihood under the three points. For each m, observe m ordered independent Z Bernoulli(theta1), use equal prior and MAP with first-index tie break A,B,C. The exact source route enumerates all 3*sum(m=0..8)2^m=1533 ordered source types. There are 1031 positive-probability source types; C has one positive source at each m. A separate Python standard-library count route sums Binomial(m,theta1) by success count, without using the R ordered-source program.

## Exact results

| Z sample size m | Mean MAP correct | A correct | B correct | C correct |
| ---: | ---: | ---: | ---: | ---: |
| 0 | 1/3 | 1 | 0 | 0 |
| 1 | 7/12 | 0 | 3/4 | 1 |
| 2 | 11/16 | 1/2 | 9/16 | 1 |
| 3 | 71/96 | 3/8 | 27/32 | 1 |
| 4 | 605/768 | 5/8 | 189/256 | 1 |
| 5 | 103/128 | 25/32 | 81/128 | 1 |
| 6 | 1687/2048 | 41/64 | 1701/2048 | 1 |
| 7 | 41321/49152 | 49/64 | 12393/16384 | 1 |
| 8 | 55271/65536 | 109/128 | 44469/65536 | 1 |

The equal-prior macro accuracy rises monotonically over the frozen grid. No m<=8 reaches the prespecified 9/10 threshold; the largest grid value is 55271/65536, approximately 84.34%. Individual parameter accuracies need not increase at every m: A falls from 1/2 at m=2 to 3/8 at m=3, even while macro accuracy rises from 11/16 to 71/96. C is perfectly recognized for m>=1 under the artificial assumption theta1=1. At m=0, the fixed tie rule always selects A, so its conditional accuracy is 1.

The m=2 row exactly reproduces the frozen original R276 conditional accuracies A=1/2, B=9/16, C=1 and macro 11/16. These finite classification rates do not change the original result that the three full YZ distributions are pairwise distinguishable. They do not establish global identifiability over continuous parameter spaces.

## Execution and evidence

R-route full CSV (1533 rows) and full JSON were constructed by exact BigInt rational arithmetic in the V8 execution environment and persisted on main. Git blobs: CSV 08dbd0c57ea2f18749d05fe953b2ed907de9cbdd; JSON 51eb669c9150b6c90ac81c3ab8cf5f91030f9d0b. The remote persisted bytes were reread and a separate V8 source-level verifier checked 1533 unique keys, source probabilities, MAP labels, all three posteriors, 81 confusion cells, nine macro values and evidence tags. Six deliberately altered inputs were rejected: duplicate row, missing row, changed source mass, changed posterior, E3 evidence upgrade, changed macro accuracy.

B-route independent Python source was executed locally and independently compared ordered enumeration with binomial-count aggregation for all nine m. The local replay JSON matched byte for byte. Archived B Python source blob f3a41ce21d132a0985590f67410ef017f7c10e13 matches the locally executed file's Git blob. The archived R Python source is a reproducible program and was uploaded; its native Python CLI has NOT_RUN in this round. GitHub Actions NOT_RUN because free billing quota was not verified. No external-team or blind replication was performed. No E2 predictions, no E3 evidence.

## Interpretation and remaining work

An extra measurement channel can separate finite parameter distributions while classification error remains substantial at small sample sizes. The overall Bayes-optimal accuracy can improve even as one candidate's conditional accuracy worsens. This is a model-specific E1 result relying on independent Z, known parameter candidates, equal prior, known measurement channel and fixed MAP rule. It is not a recommendation for the number of observations in a real experiment.

Next: native CLI execution of archived R program and byte comparison to persisted CSV/JSON; independent external replication and real measurement-model checks remain open. Keep R073 and PESEN v0.1 frozen. Continue R277 only after fresh queue and concurrent-work recheck. No fusion or personal decision product development.
