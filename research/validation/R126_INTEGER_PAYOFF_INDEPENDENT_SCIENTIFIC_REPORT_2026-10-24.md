# R126 independent exact integer payoff audit: scientific report

Date: 2026-10-24. Original239 05-002 Public Goods Game. Strict reuse of existing R126. Maximum evidence grade `PASS_BOUNDED_INTERNAL_INTEGER_PAYOFF_E1`.

## Primary source and prior study

Fehr and Gächter (2000), *Cooperation and Punishment in Public Goods Experiments*, American Economic Review 90(4):980–994, DOI 10.1257/aer.90.4.980. The existing R126 scientific report directly reviewed original printed pp. 981–985, Eq.(1)/(2), Table 2 and Table 3, and the original R126 source had already passed 57 unit tests, 52,500 artificial contribution deviations, and source aggregate checks in GitHub Actions 39347160953. Original R126 report: `research/R126/R126_FEHR_GAECHTER_2000_ORIGINAL_PGG_COSTLY_PUNISHMENT_TABLE3_SCIENTIFIC_REPORT_2026-10-20.md`.

The frozen third-method protocol `research/validation/R126_THIRD_METHOD_INTEGER_PAYOFF_PROTOCOL_FREEZE_2026-10-24.md`, Git blob `8a957b11a761786e08706867a53689fec3b4d124`, predates all new R126 code and data.

## Independent method and exact result

For each four-player contribution vector from `{0,5,10,15,20}^4`, enumerate eight previously frozen punishment matrices. Calculate each player's final payoff as the exact integer numerator `(100-5g_i+2G)(10-P_i)-50C_i` over denominator 50, with capped received punishment `P_i` and nonlinear sender cost `C_i` from original Table 2. The third method does not call original payoff functions to construct the numerator. It subsequently compares every exact result with unchanged R126 original individual and independent group payoff methods.

**5000 complete constructed worlds, 20,000 exact individual payoff comparisons and 5000 group sum comparisons passed.** The original 57 tests passed on each of Python 3.11 and 3.12. Frozen controls: no contribution/no punishment gives four payoffs 20; full contribution/no punishment gives four 32; the combined one-point and two-point punishment illustration gives [23,22,24,154/5], total 499/5; saturated 6/7/10 points gives group total 14, punished target zero, one sender negative. Wrong source Git blob and mutated CSV are rejected.

Raw CSV: `research/validation/R126_INTEGER_PAYOFF_5000_CONSTRUCTED_WORLDS_2026-10-24.csv`; SHA256 `6cd4dfb8cf257980aef805bad3bdf9cd54f9666b5b900fd08f0c601b8808f333`. Independent script: `research/validation/verify_r126_integer_payoff.py`. Original source, test and report Git blobs are pinned and verified.

GitHub Actions https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40095282746 completed successfully. Both Python 3.11 and 3.12 jobs passed the exact CSV regeneration, source identity and mutation rejection checks and all 57 unchanged tests. Both logs printed the same SHA256. Standard public repository hosted Ubuntu runners were used.

## Scientific limitations and B review

The real 2000 experiment involved 112 participants as reported by its authors; the current audit accessed no original individual behavior records. Published Table 3 Stranger session display values of 9.8, 14.3, 13.1 average to 12.4 while the printed Mean row is 12.3. The discrepancy remains explicitly unresolved without unrounded source values. It is not silently corrected. No original Wilcoxon p value, individual-level confidence interval, treatment effect, predictive calibration, sample-out prediction or session-resampled uncertainty was independently estimated.

The exact payoffs prove consistency of the frozen institutional incentive formula in 5000 artificial worlds. They do not establish real participants' behavioral mechanisms or the causal efficacy of punishment. This is internal independent-method checking, not external research team replication. New E2=0, historical E3=0. R073 and PESEN v0.1 unchanged. Catalogue linkage and scientific validity are separate.

## A scout status

Montero-Porras 2022 has been deduplicated against existing R096's same original experiment. The current round does not add a new independent human dataset or frozen R073 external score.
