# R127 Table 2: exact identification bounds from published marginal counts

Date: 2026-11-10. Track: closure. Subflow: independent bounded scientific audit. Starting main: `c955f6e6c5d6cbcfd124ca9184cab3ee77de2e7d`. Source: frozen `protocols/R127_VAN_HUYCK_1990_MINIMUM_EFFORT_ORIGINAL_TABLE2_AND_2X2_RISK_SELECTION_FREEZE_2026-10-20.md` (Git blob `4734ede5133701d622acfda76c4f9474bf660b21`), originally transcribed from Van Huyck, Battalio & Beil (1990), AER 80(1), Table 2, printed pp. 240–241. This run independently derives mathematical bounds from the archived transcription; it did not re-open the publisher scan or obtain individual-level observations.

## Exact bounded calculation

For each session, let `a_j` and `b_j` be published period 1 and period 10 counts for effort j=7,...,1, and `n=sum(a)=sum(b)`. The minimum possible number of persons whose effort changed is `n - sum_j min(a_j,b_j)` (integer transport coupling maximizing diagonal matches). The maximum possible number changed is `n - max(0, max_j(a_j+b_j-n))` (integer transport coupling minimizing diagonal matches). These bounds are attainable given only the two marginals and preserved session membership; they say nothing about actual individual transitions. For entry into effort 1, the minimum is `max(0,b_1-a_1)`, the maximum is `min(b_1,n-a_1)`.

| Session | n | min changed | max changed | min newly effort 1 | max newly effort 1 |
| --- | ---: | ---: | ---: | ---: | ---: |
| 1 | 16 | 13 | 16 | 13 | 13 |
| 2 | 16 | 13 | 16 | 13 | 13 |
| 3 | 14 | 11 | 14 | 9 | 9 |
| 4 | 15 | 15 | 15 | 13 | 13 |
| 5 | 16 | 14 | 16 | 11 | 11 |
| 6 | 16 | 12 | 16 | 7 | 8 |
| 7 | 14 | 11 | 14 | 9 | 10 |
| **Sum** | **107** | **89** | **107** | **75** | **77** |

Independently checkable calculation: `sum(n - sum(min(x,y) for x,y in zip(a,b)) for a,b,n in sessions) == 89`. Session 4 has disjoint support at the two times, forcing all 15 individuals to have different effort choices. The published aggregate first-round effort-1 count is 2 and last-round count is 77. At least 75 individuals must therefore have entered effort 1, with the session-preserving sharp upper bound 77. No exact transition count or transition matrix is identified.

## Scientific scope and acceptance

Evidence: E1 exact mathematical partial identification **conditional on archived published marginals**; original article contains human experimental aggregates, but this calculation is not new person-level E2 prediction or E3 historical forecasting. The prior R127 `CLOSED_BOUNDED` state and frozen protocol remain unchanged. This is a newly derived, bounded property of the existing Table 2 marginals and does not upgrade the original catalogue item `05-003` from `PROVISIONAL_PRIMARY_README_LINK`.

Method is a direct transportation/counting identity independent of R127's original Python implementation. No Actions/CI invoked, no paid service, no sensitive data. Limitations: matching identities between period 1 and period 10 are unavailable; coupling feasibility assumes the same n persons within each published session, and imposes no extra restrictions on paths through intermediate periods. A stronger claim would require individual linked sequences and separate source verification.

Next action: inspect the actual original Table 2 scan against all fourteen transcribed marginal vectors and source version, then audit machine receipt identities and catalogue-specific closure requirements before changing the itemwise queue.