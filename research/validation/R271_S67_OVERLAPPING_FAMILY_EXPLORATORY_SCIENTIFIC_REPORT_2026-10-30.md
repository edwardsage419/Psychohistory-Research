# R271 S67 overlapping candidate tests: exploratory finite null risk

Date: 2026-10-30 UTC. Baseline HEAD 38f714a2860fe4ff0e21776453e3f765068d05b0. Design boundary: protocols/R271_S67_OVERLAPPING_TEST_FAMILY_DESIGN_FREEZE_2026-10-30.md, committed as e37481377bbde97d019293581d547b4e5768f373.

## Question and scope

Original R271 (12-001) is already bounded E1 accepted. This is a separate complementary S67 mathematical extension: how does reuse of primitive observations across candidate tests change the exact false-positive probability when the analyst reports any unadjusted positive test? It is an **exploratory, nonblind, artificial E1** calculation. The researcher worked out possible rolling-window results while choosing the design; the new protocol was archived before script execution, yet **strict blind prescore timing is not claimed**. Original R271 acceptance and its files are unchanged.

All primitive bits are independent fair Bernoulli; each candidate uses four bits and exact one-sided Binomial p values. Family m=1,2,3; designs IDENTICAL (same four bits), ROLLING (one-bit-shifted four-bit windows), DISJOINT (independent four-bit windows). Policies FROZEN_FIRST, FLEXIBLE_ANY, BONFERRONI_ANY. Nominal alpha=1/8.

## Exact finite source results

| m | design | frozen first | flexible any | Bonferroni any |
| --- | --- | --- | --- | --- |
| 1 | all three | 1/16 | 1/16 | 1/16 |
| 2 | identical | 1/16 | 1/16 | 1/16 |
| 2 | rolling | 1/16 | 3/32 | 3/32 |
| 2 | disjoint | 1/16 | 31/256 | 31/256 |
| 3 | identical | 1/16 | 1/16 | 0 |
| 3 | rolling | 1/16 | 1/8 | 0 |
| 3 | disjoint | 1/16 | 721/4096 | 0 |

For m=3, the flexible reporting risk is 6.25% when all tests reuse the same four bits, 12.5% for shifted windows, and approximately 17.60% for disjoint tests. The disjoint versus rolling gap is 209/4096, approximately 5.10 percentage points. Correlation induced by shared observations changes the probability of reporting at least one positive test, even with identical individual exact p values.

For m=2, the Bonferroni threshold is 1/16 and still allows four successes. For m=3 the threshold is 1/24, below the minimum attainable raw p=1/16, hence zero reports in all designs. Fixed-first reporting is 1/16 regardless of overlap.

## Computation and provenance

The R enumeration evaluated 27 policy/design/family worlds and 13,584 policy-labelled primitive configurations. These are mathematical types, not 13,584 independent experiments. R's native Python program ran eight unit tests successfully and emitted the full CSV and exact JSON. The GitHub-archived standalone JavaScript generator reproduced the same CSV Git blob 4bfed50d9df756d537d239868771181e07a2c216 and JSON Git blob 6b56bd2b82790e531a938106db5eada7da416a18, matching locally generated Python bytes.

Source SHA256: 9a72624ebcfc77e3eb65cdfe44696efc0d85a282f695a5ad77029753f75db9cb.
Results SHA256: 0f6268f76b705fb69b9aa806ba9551f7eb109dfda8a93eddeceaa4476fc89379.

Independent B route: inclusion-exclusion on unions of observed bit positions, with no import of the R enumeration, checked all 27 exact Fraction risks. The independent local Python CLI rechecked all 13,584 persisted source rows and passed seven tests including six mutations. The archived JS B implementation executed in a V8 runtime, rechecked all 13,584 source rows and rejected six mutations. The JS Node native CLI entry points remain NOT_RUN; no GitHub Actions were triggered.

## Scientific boundaries

The overlap contrast is a controlled comparison of mathematical source designs, not a real-world causal evaluation of preregistration or registered reports. No real research submission, empirical calibration, human E2, historical E3, or external independent replication was conducted. Code execution and persisted checks establish internal computational consistency, not real-world prediction. R073 model/scoring and PESEN v0.1 remain frozen.

Next: independently review the assumptions about repeated identical tests, preserve the exploratory timing caveat, and seek real observational evidence only under a separately frozen, appropriately grouped protocol.
