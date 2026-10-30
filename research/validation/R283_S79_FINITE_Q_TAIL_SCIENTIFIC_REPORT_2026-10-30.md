# R283 S79 scientific report: exact finite-sample Q alert distribution
Date UTC: 2026-10-30. Track: r. Status: PARTIAL_BOUNDED_INTERNAL_E1_EXPLORATORY. Prior results read: original R283 frozen protocol, report, results and acceptance status. This is explicitly NONBLIND; R283 original CLOSED_BOUNDED E1 state is unchanged.

## Question and frozen design
Can an observed Cochran-style Q statistic trigger a high-heterogeneity alert in the original R283 artificial three-study registry even when all three true effects are identical? How do the same alert and zero-Q rates change under the two pre-existing heterogeneous artificial DGPs? Freeze commit: d6a072305ed28a12d987cf148f5f53b3eaeb3262, committed before S79 scores were calculated. Fixed descriptive threshold Q >= 6; no chi-square p-value or nominal 5% test claim. Original R283 study rates, oracle inverse-variance weights and complete six-bit source universe preserved.

## Exact results
| Original artificial DGP | P(Q=0) | P(Q>=6) | E(Q) | Exact Q support size |
| --- | ---: | ---: | ---: | ---: |
| HOMOGENEOUS | 473/2048 (23.0957%) | 135/2048 (6.5918%) | 2 | 4 |
| BALANCED_HETEROGENEITY | 45/512 (8.7891%) | 41/256 (16.0156%) | 10/3 | 7 |
| ONE_REVERSAL | 153/2048 (7.4707%) | 455/2048 (22.2168%) | 34/9 | 4 |

The full rational PMF and all 192 source rows are archived separately. In HOMOGENEOUS the true study effects are all 1/2, yet 135/2048 of artificial repeated datasets trigger Q>=6. The alert rate rises with the two chosen heterogeneous DGPs. These are model-specific exact probabilities, not empirically estimated detection rates. The oracle weights require true arm probabilities and are unavailable from one treatment and one control observation in real studies. Q=0 is a finite-sample event, not proof of equal true study effects. The original E(Q) values (2, 10/3, 34/9) are exactly recovered.

## Actual execution and verification
1. Before scoring, freeze protocol committed separately.
2. Local Python 3 standard-library six-bit route ran and wrote 192-row CSV and complete JSON. The local generated Git blob identities match the actual remote persisted CSV and JSON exactly: CSV `9e087a230ab8085dfae28a12c9e0017f95062092`; JSON `94e615904aaafac1ad47127da26783c3e52fddf3`. Local SHA256: CSV `69211312827a201bcfca56204a87cf1f7a05563cf99ed39b0a7e4824818acea3`, JSON `9dd5163e55ef51c81651704ea28f875068d55777586ba12d715958b1c4e9ea60`.
3. Independent local Python B route enumerated 27 study-level effect categories, without importing the six-bit generator. All three full PMFs and summaries agree. 192 source identities and all row-level probabilities/Q values checked; six deliberate mutations rejected (duplicate, missing, mass, Q, evidence grade, tail).
4. Archived source `R283_S79_EXACT_Q_REPLAY.py` and independent `B_R283_S79_INDEPENDENT_27_CELL_AUDIT.py` are new files. Their exact remote bytes have not been executed with native Python in this run; the independently authored local equivalents were executed. Do not equate local-equivalent execution with archived-exact CLI replay.
5. New GitHub Actions and external independent-team replication: NOT_RUN. Billing quota NOT_VERIFIED; no Actions dispatched.

## Unified acceptance
A01 PASS bounded artificial question and exclusion; A02 PASS original R283 frozen DGP and new prescore S79 protocol; A03 PARTIAL local execution, remote receipt byte identity, archived exact native CLI open; A04 PASS six deliberate negative controls and all outcomes preserved; A05 PASS E1/nonblind/oracle/threshold limits; A06 PARTIAL additive remote archive and handoff, no external reproduction. S79 exploratory scientific acceptance remains PARTIAL. Original R283 closed-bounded status is unaffected. No real systematic review, real paper effect sizes, E2/E3 prediction or external replication. R073 and PESEN v0.1 FROZEN.

Sources: original R283 https://github.com/edwardsage419/Psychohistory-Research/tree/main/research/R283 ; PRISMA 2020 https://doi.org/10.1136/bmj.n71 ; Higgins et al. 2003 https://doi.org/10.1136/bmj.327.7414.557 .
Next: exact native CLI replay on archived Python files; then R284 complementary audit without duplicating its existing publication selection model.
