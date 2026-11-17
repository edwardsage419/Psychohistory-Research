# R127 / original239 05-003: Ten-round published aggregate sharp transition bounds

Date: 2026-11-17. Track: R mainline P0 / 05-003. Evidence: secondary nonblind partial identification from published 1990 human group aggregates, together with new internal exact mathematics. New individual held-out E2 scores = 0; new historical E3 scores = 0.

## 1. Research baseline, primary source and deduplication

Start main: cd2d1e9bfa02089c7261252604be4c8d197b42c7.

Primary publication: Van Huyck, Battalio & Beil (1990), Tacit Coordination Games, Strategic Uncertainty, and Coordination Failure, American Economic Review 80(1):234–248. Original scan hosted at https://econweb.ucsd.edu/~jandreoni/Econ264/papers/Van%20Huyck%20et%20al%20AER%201990.pdf , printed pages 240–241 Table 2.

The sole numeric source is the previously transcribed 490 published cells in research/validation/r127_primary_table2_70_periods_source_audit_20261103.js, authenticated against Git blob SHA1 aa575a803e5547afe24eabc1f232f2b539ef1709. Existing original-source reports R127_05_003_PRIMARY_1990_TABLE2_ALL_PERIODS_SOURCE_CHECK_20261102.md and R127_05_003_TABLE2_SECOND_PASS_490_CELL_CONCORDANCE_AND_BALANCED_MUTATION_20261102T2140Z.md document two nonblind readings by the same project research agent.

The 2026-11-02 report R127_05_003_TABLE2_SHARP_TRANSITION_BOUNDS_20261102.md already established the sharp minimum 89 / maximum 107 subjects whose actions differed between period 1 and period 10. This new analysis uses all ten periods to identify bounds on 63 adjacent-session-period transition tables, total repeated action changes, summed absolute effort movement, and minimum exits from effort 1. It does not duplicate endpoint-only bounds.

No PDF pages were reread during this run; no new blind transcriber or original individual-level trajectories were obtained. Original numerical transcription could contain same-agent errors.

## 2. Partial identification assumptions and exact bounds

Seven stable experimental groups contain 16,16,14,15,16,16,14 participants (total 107). Assume a fixed roster within each session and exactly one effort choice per subject per period. For a given session and two adjacent periods, let a_i and b_i be the published action counts (i=1..7), both summing to group size n. The unknown integer transition matrix X_ij must have row sums a_i and column sums b_j.

The sharp lower and upper counts of people whose efforts differ across these two adjacent periods are:

L = n - SUM_i min(a_i,b_i) = (SUM_i |a_i-b_i|)/2.

U = n - max(0, max_i(a_i+b_i-n)).

The sharp minimum sum of individual absolute effort differences for adjacent periods equals the one-dimensional earth-mover value:

W = SUM_{k=1}^{6} |SUM_{i=1}^{k} (a_i-b_i)|.

These are algebraic bounds on feasible unpublished transition matrices, not estimates of actual participant transition identities.

## 3. Exact results for nine consecutive period transitions

The 107 subjects over nine adjacent pairs yield 963 subject-transition opportunities and 63 group-period transportation problems.

| Periods | Sharp lower changed | Sharp upper changed | Sharp minimum absolute effort distance |
|:--|--:|--:|--:|
| 1 to 2 | 45 | 107 | 110 |
| 2 to 3 | 40 | 107 | 93 |
| 3 to 4 | 30 | 105 | 75 |
| 4 to 5 | 31 | 105 | 72 |
| 5 to 6 | 31 | 103 | 53 |
| 6 to 7 | 26 | 103 | 30 |
| 7 to 8 | 26 | 91 | 52 |
| 8 to 9 | 16 | 72 | 22 |
| 9 to 10 | 17 | 64 | 45 |
| **All adjacent periods** | **262** | **857** | **552** |

Session-specific cumulative lower/upper changed event ranges:
1 = 36 to 130, 2 = 42 to 122, 3 = 41 to 109, 4 = 46 to 122, 5 = 43 to 129, 6 = 33 to 139, 7 = 21 to 106.

The quantity 262 to 857 counts **repeated change events across nine transitions**, not distinct persons. A subject may contribute multiple events. In contrast the prior 89 to 107 result counts subject endpoints that differ, once per subject.

The numerical sharpness of the global sums was not presumed. Independently optimized 7-by-7 nonnegative integer flows attain the pairwise minima and maxima, and deterministic flow decomposition constructs separate complete ten-round **synthetic** participant paths matching every published group-period-cell count while jointly attaining 262 minimum changes, 857 maximum changes, and 552 minimum summed absolute effort units, respectively. These are three separate witness path populations and must never be presented as the real participants.

## 4. Observed aggregate constraints on irreversible convergence

Published count at effort 1, pooled across seven groups for each period:
2, 5, 15, 25, 37, 50, 47, 70, 72, 77.

Summing required positive and negative changes of the effort-1 count **within each individual session and transition** gives at least 98 entrances into effort 1 and at least 23 exits from effort 1 across the nine transitions. The net change is 77−2=75 and the lower bounds satisfy 98−23=75.

The strong absorbing-action hypothesis "a person never leaves effort 1 after first selecting it" is logically incompatible with these published marginals, conditional on fixed within-session membership: total choosing effort 1 drops from 50 in period 6 to 47 in period 7; the groupwise flow audit strengthens the forced-exit count to 23 over all periods. This does not identify which individuals switched or which mechanisms generated the changes. Absorbing convergence, noisy learning, shocks, errors, heterogeneity, and other mechanisms must be kept distinct.

## 5. Executed independent program and validation

New code: research/validation/r127_table2_full_ten_period_sharp_transitions_20261117.js.

The program reads the archival source read-only and first authenticates its whole Git blob SHA1. It uses standard Node.js built-in libraries, with no external dependencies. It implements:

1. All 63 closed-form changed-action bounds L and U, with nonnegative integer margin checks and 490-cell coverage.
2. A separate 7-by-7 integer min-cost-flow algorithm under zero diagonal cost, plus negative off-diagonal costs for maximal switches; row and column sums are checked for every integer transition matrix.
3. Independent earth-mover calculations by cumulative differences and ascending quantile matching.
4. Synthetic complete ten-round path decomposition for lower changed, upper changed, and lower absolute effort objectives; every constructed path population reproduces each source cell exactly.
5. A nonconserving count mutation deliberately rejected; source bytes are pinned fail-closed.

The computation was first executed against actually fetched archive bytes in the isolated JavaScript V8 environment. All 63 flow problems and all path certificates passed. Then a native GitHub Actions run on standard ubuntu-24.04 / Node v22.23.4 actually executed the saved Node CLI and an explicit Python output-gate. CI run https://github.com/edwardsage419/Psychohistory-Research/actions/runs/44024706230 returned **completed / success**, with log signal R127_ADJACENT_SHARP_BOUNDS_VERIFIED 262 857.

The GitHub repository is PUBLIC and the job used a STANDARD GitHub-hosted runner with read-only permissions, no artifact upload, and no large runner. GitHub official billing guidance states standard public-repository runners are free: https://docs.github.com/en/actions/concepts/billing-and-usage. Account invoice was not accessed. No other paid services, external API, private datasets, or new subscriptions were used.

## 6. Evidence classification and next scientific gates

COMPLETE_BOUNDED_INTERNAL: exact published-group-marginal transportation bounds, exhaustive 63-pair checks, three constructive longitudinal sharpness certificates, GitHub Node execution, and mutation rejection.

PARTIAL: old source Table 2 transcription was verified by the same research agent, not an external blinded second reader; PDF source bytes and identities were not reauthenticated this round.

NOT_RUN: fitting actual subject-specific adaptive learning coefficients, a new human E2 held-out prediction, an E3 historical event forecast, or genuinely independent external-team replication.

UNCHANGED: R127 original CLOSED_BOUNDED acceptance, original239 05-003 pending P0 formal disposition, R073, PESEN v0.1 and every frozen research protocol. No scientific grade upgrade; no new E2 or E3.

Next action: perform independent original239/05-003 formal itemwise adjudication with historical protocol deviation retained, or advance R272 mandatory production gate review. Avoid redoing the 490-cell manual transcription unless an actually independent source reader becomes available.
