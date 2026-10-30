# R288 S84: six-draw preference sign error under frozen reference-dependent loss model

Date: 2026-10-30 UTC. Track R. Status: PRESCORE_FREEZE, no results examined for S84.
Target key: (r,R288,original-2026-10-23-freeze,S84-six-draw-sign-error).
Original R288 closed bounded E1 is preserved. S84 is an additional artificial E1 sub-study.

## Fixed sources and design
Use exactly the archived R288 six-bit fair gamble source table at research/R288/R288_ALL_576_ORIGINAL_REFERENCE_LOSS_SOURCES.csv, original nine worlds r in {-2,0,2}, L in {1,2,3}, 64 equiprobable ordered six-bit sequences per world, and the original prospect-value rule. Original prescore freeze is protocols/R288_PROSPECT_REFERENCE_LOSS_AVERSION_9_WORLDS_576_SOURCES_PRESCORE_FREEZE_2026-10-23.md. All source atoms, including ties and adverse results, must remain in the analysis. No new data, fit, loss parameter, or probability distortion.

For each source compute six-draw realized mean gamble reference value minus the fixed sure-zero reference value, using the original CSV. Compute the exact population preference difference from the two equally probable gamble outcomes. Classify the observed six-draw sign as CORRECT, WRONG, or TIE relative to the population sign. A sample TIE has realized difference exactly zero. The population sign is nonzero in all nine worlds under the frozen mechanism. Report unconditional P(CORRECT), P(WRONG), P(TIE) and conditional P(WRONG | non-tie), with a separate tie denominator. Report all nine worlds; a directional example may be highlighted only after full tabulation.

## Precommitted checks
R route must parse every persisted CSV row and independently recompute the original per-source realized difference from the six-bit string and piecewise loss value; require all 576 unique (r,L,bits), six bits, 64 rows per world, probability 1/64, and exact rational equality to the archived realized difference. Recompute exact total probability 1 for each world.
B route must use only independent binomial counts k=0..6 and C(6,k)/64 to calculate classification probabilities and compare all nine worlds with R. Include explicit negative controls for missing, duplicated, altered probability, altered realized difference, and altered class. Preserve failures.
The result must report E1_ONLY, original R288 status unchanged, R073/PESEN frozen, E2/E3=0, and no external team replication. A01-A06 acceptance must be assessed separately, and CLI execution cannot be equated with external scientific validation.

## Stop conditions
Any original-source identity mismatch, source coverage failure, or R/B disagreement => S84 FAIL/OPEN with evidence retained; do not modify this freeze to accommodate results. No CI invocation without verifying zero billing risk. Do not modify original R288 files.
