# B R161 negative-control execution addendum and correction

Date: 2026-10-25. This is append-only scientific evidence. The earlier R161 B audit and exact receipt remain unchanged for provenance.

## Correction

The initial R161 B audit program `r161_b_independent_survival.js` used boolean sentinel comparisons to mark two predeclared mutants detected. Those statements did not actually execute altered Markov first-passage calculations. The original receipt's two mutant booleans alone were insufficient evidence for successful negative controls. This limitation was found in the same run, after the initial audit was archived.

## Executed replacements

A new standalone program `research/evidence_audit/r161_b_mutant_controls.js` independently rebuilt the eight transition matrices and survival sums, then executed two altered calculations:
1. For each initially absorbing frozen start k=0 or k=N, force the wrong answer E[T]=1 and check it disagrees with the correct E[T]=0. Actual detections: 16 of 16.
2. For each transient frozen start, omit the first survival term `P(T>0)=1` from the independently summed expected first passage time. The computed wrong answer differs from the exact rational target by approximately one unit. Actual detections: 32 of 32. The unaltered baseline survived all 32 comparisons with error <1e-10.

The program executed the survival recurrence through 234 to 1378 terms depending on the kernel; all eight predeclared tail bounds were below 1e-12. Raw machine receipt: `research/evidence_audit/R161_B_EXECUTED_MUTANT_CONTROLS_2026-10-25.json`.

These tests support only internal E1 computational control sensitivity. The wrong absorbing-state mutant is deliberately simple, and neither mutant establishes empirical mechanism validity. No new E2/E3 evidence. Original R161 and R073/PESEN v0.1 remain frozen. New remote CI NOT_RUN. Earlier unexecuted mutant booleans should be interpreted as **UNSUPPORTED_SENTINELS**, superseded for control evidence by this explicit execution receipt.
