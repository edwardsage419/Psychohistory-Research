# R148 additive scientific report: first irreversible resource extinction
Date: 2026-10-25. Scientific scope: project-generated synthetic E1, no new E2 or E3.

## Precommit and frozen equations
Protocol was committed first at `671ff0228ed5961b7fbb3a71c63a8b29629a8995`, before producing the new executable and scores. The original R148 prescore protocol and original 2026-10-20 accepted research remain unchanged. The 2009 Ostrom SES diagnostic framework and 2004 Anderies/Janssen/Ostrom robustness paper supply theoretical motivation, not the project's numeric nine-stock eight-year model.

## Executed computation
At q=f=1/4, independently enumerate 256 weather histories crossed with 256 infrastructure-failure histories for each of OPEN, QUOTA and ADAPT. Exactly 65,536 event histories per policy, 196,608 in total. Each event sequence has exact integer weight under common denominator `4^16=4294967296`. For each history, record first hitting year of absorbing S=0, or survival after year 8, and weighted cumulative harvest. An independently coded state-mass recursion checks all 24 first-ruin bins, three terminal survivals and three weighted harvest totals. The distinct Python B audit separately recomputes them.

| Policy | First ruin in year 2 numerator | First ruin in year 3 numerator | First ruin in year 8 numerator | Survival after year 8 numerator |
| --- | ---: | ---: | ---: | ---: |
| OPEN | 268435456 | 2214592512 | 0 | 0 |
| QUOTA | 117440512 | 327155712 | 426156633 | 1330196823 |
| ADAPT | 117440512 | 327155712 | 404505333 | 1499549355 |

All table entries are integer numerators divided by 4294967296. The full t1..t8 distributions are in the exact CSV receipt. Each policy's ruin mass plus survival mass equals the common denominator. The original R148 exact terminal survival and net harvest values are independently reproduced. The executed Node source blob is `aac9200fe9bd724fba9130c11df8ad4c7698d4e1`, locally verified equal to the committed blob; SHA256 of the locally executed source is `daf6b4181b737c7f593473d58eb8a41c9020a42a48aaab1a43f1c0bc2c594a48`.

## New bounded within-model finding
At the frozen q=f=1/4 parameter point, ADAPT has a weakly lower cumulative extinction probability than QUOTA at each year 1..8. Both have equal cumulative first-ruin probabilities through year 3. Starting in year 4, the cumulative QUOTA minus ADAPT ruin numerator is respectively `26542080, 68677632, 112534272, 147701232, 169352532` for years 4..8. The year-8 survival probability difference is exactly `42338133/1073741824`, approximately 0.03943 in favor of ADAPT. This is a within-model stochastic ordering at ONE frozen parameter point. It is not a general theorem for all climate/failure parameters and says nothing about observed ecological performance.

## Original fee contract and sensitivity
R148's frozen net metric pays annual governance maintenance fees for all eight years, including years after ecological collapse. The path enumeration confirms this ledger exactly. As a deliberately distinct hypothetical alternative, if fees stopped only after the first collapse year, QUOTA's expected net would increase by `472050117/2147483648` approximately 0.21982, and ADAPT's by `224917083/536870912` approximately 0.41894. These alternative values are sensitivity diagnostics, NOT replacement scores and not empirical welfare estimates.

## Audit and acceptance
Local Node direct path enumeration and independent state-mass DP completed without errors; archived survival and net exact checks pass. A separate Python implementation in `research/evidence_audit/r148_b_independent_first_ruin.py` passed 40 checks and a deliberate resurrection mutant rejection. Original R148 CI `39412337646` is historical and does not certify these new scripts. New remote CI: `NOT_RUN`; billing exposure was not independently verified. E1 internal bounded verification only, E2=0, E3=0, external independent replication=0. The R073 and PESEN v0.1 freezes and original239 crosswalk are untouched.

Reproduce with `node research/validation/r148_first_ruin_event_paths.js receipt.json` and `python research/evidence_audit/r148_b_independent_first_ruin.py research/validation/R148_FIRST_RUIN_65536_EXACT_RECEIPT_2026-10-25.csv`. No paid dependency or third-party library.
