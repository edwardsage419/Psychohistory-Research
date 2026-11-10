# R127 candidate-action count semantics: independent audit (2026-11-10)

Scope: R127 original-source minimum-effort exact enumeration, read-only interpretation of frozen implementation at main 558ef502ed2e06e76bb35bffdde785075b04f71e. No change to frozen protocol, tests, evidence tier or acceptance status.

## Independently derived arithmetic

The source function `exhaustive_original_min_effort_payoff_audit()` enumerates all seven actions for each player at every profile, including the unchanged action `trial == own`. The loop increments `deviation_total` for every trial. Thus its reported 75,117 is the number of candidate-action payoff comparisons, **not** the number of strictly changed unilateral actions.

| n | Profiles 7^n | Candidate-action comparisons n * 7^(n+1) | Genuine changed-action comparisons n * 6 * 7^n |
|---|---:|---:|---:|
| 2 | 49 | 686 | 588 |
| 3 | 343 | 7,203 | 6,174 |
| 4 | 2,401 | 67,228 | 57,624 |
| Total | 2,793 | 75,117 | 64,386 |

Difference: 10,731 unchanged-action comparisons, equal to sum(n * 7^n). The 75,117 source receipt is numerically consistent with the implementation and is valid as a count of exhaustive candidate-action checks. The code also separately evaluates other actions when testing unique best replies. No numerical discrepancy or P0 bypass is established by this terminology distinction.

## Scientific boundary

This is E1 arithmetic and static-source interpretation only. It does not establish a new human E2 score, historical E3 result, independent external replication, or closure of original catalogue 05-003. R127 remains CLOSED_BOUNDED; original itemwise status stays provisional pending the established acceptance criteria and historical CI source-commit identity review.

## Reproduction

For n in {2,3,4}, compute `profiles=7**n`, `candidate=n*7*profiles`, `changed=n*6*profiles`; sum each column. Inspect source lines containing `for trial in range(1,8)` and `deviation_total+=1`. This audit does not import the R127 implementation.
