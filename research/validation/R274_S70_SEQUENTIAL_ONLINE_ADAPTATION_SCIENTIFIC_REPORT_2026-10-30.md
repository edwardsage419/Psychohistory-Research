# R274 S70 scientific report: exact legal online one-step update

Date: 2026-10-30 Asia/Singapore. Research ID R274 S70, original catalogue 12-004. Status: COMPLETE finite E1 arithmetic and internal replay, original R274 formal bounded acceptance unchanged. Prescore protocol was committed first at 6783168501b596693ec1b3dae2b215b7174ab3c1. The original R274 results had been read, so this is a nonblind internal complement.

## Research question and design

Does updating a legal forecast after observing Y5 improve the prediction of Y6, while maintaining strict chronological information boundaries? Use exactly the original R274 artificial regimes STABLE_HALF (a,b)=(1/2,1/2), RISING_RATE=(1/4,3/4), FALLING_RATE=(3/4,1/4). At t4 the four past binary observations are known; Y5 is observed only after the t5 forecast and before the t6 forecast; Y6 remains unobserved until scoring.

Three lawful policies: PAST_FIXED q5=q6=(K+1)/6; ONLINE_ONE_STEP q5=(K+1)/6 and q6=(K+Y5+1)/7; PRECOMMITTED_HALF q5=q6=1/2. Brier is (Y-q)^2. Nine regime-policy cells, each with 64 exhaustive ordered six-bit source types, 576 policy-labelled source rows. All probabilities and losses are exact rationals. The original HINDSIGHT_POOLED policy remains an explicitly invalid retrospective leakage counterexample and is excluded from this new prospective comparison.

## Exact results

| Regime | Legal policy | E Brier at t5 | E Brier at t6 | Two-period mean |
| --- | --- | ---: | ---: | ---: |
| STABLE_HALF | PAST_FIXED | 5/18 | 5/18 | 5/18 |
| STABLE_HALF | ONLINE_ONE_STEP | 5/18 | 27/98 | 122/441 |
| STABLE_HALF | PRECOMMITTED_HALF | 1/4 | 1/4 | 1/4 |
| RISING_RATE | PAST_FIXED | 55/144 | 55/144 | 55/144 |
| RISING_RATE | ONLINE_ONE_STEP | 55/144 | 131/392 | 5053/14112 |
| RISING_RATE | PRECOMMITTED_HALF | 1/4 | 1/4 | 1/4 |
| FALLING_RATE | PAST_FIXED | 55/144 | 55/144 | 55/144 |
| FALLING_RATE | ONLINE_ONE_STEP | 55/144 | 131/392 | 5053/14112 |
| FALLING_RATE | PRECOMMITTED_HALF | 1/4 | 1/4 | 1/4 |

Predeclared contrasts:
* ONLINE_ONE_STEP minus PAST_FIXED t6 risk: STABLE_HALF -1/441; RISING_RATE and FALLING_RATE -337/7056. The legal one-step update improves t6 Brier in all three constructed regimes.
* ONLINE_ONE_STEP minus PRECOMMITTED_HALF two-period risk: STABLE_HALF +47/1764; RISING_RATE and FALLING_RATE +1525/14112. The legal adaptive policy remains worse than the simple half-probability baseline in all three regimes.

The t5 risk of the two history-based policies is identical by construction. The gain at t6 arises from the now-observed Y5, with no Y6 leakage. Even after this gain, the fixed half-probability baseline has lower expected risk under these three artificial settings. The result does not justify a universal preference for constant forecasts or a general advantage for online updating.

## Independent arithmetic and source replay

R route: archived JavaScript v2 enumerates all 64 ordered six-bit sources per regime and all three policies, producing 576 weighted source rows and nine complete result objects. V8 re-execution of the archived v2 script regenerated the entire persisted CSV and JSON text exactly.

B route: independently authored exact-moment oracle uses E[K]=4a, Var(K)=4a(1-a), E[Y5]=b, Var(Y5)=b(1-b), and E[(Y-q)^2]=b(1-b)+Var(q)+(E[q]-b)^2. Native Python execution of the exact archived source (Git blob 0f6c37ff108eb1b5aa0630dd9a7654b7df922de3) returned PASS for all 18 per-time scores and nine averages. An independent JavaScript gate compared 27 per-time/average fields, six contrasts and all 576 archived source rows with 3456 numeric source checks. Nine deliberately corrupted receipt variants were all rejected. This is an internal, nonblind methodological check, not an independent external research team.

An R source control defect was found during this run: the first archived script compared the same q6 expression with itself, a tautological leakage check. The original remains as historical evidence. A separate v2 script now compares the q6 values for the 32 distinct (past four bits,Y5) prefixes per regime-policy across paired Y6 values. Its full JSON and CSV outputs are byte-identical to the previously archived outputs. The B gate independently verifies q5/q6 formulas and source identities. No results were silently rewritten.

## Artifacts and evidence boundaries

* Frozen S70 design: `protocols/R274_S70_ONLINE_ONE_STEP_TEMPORAL_ADAPTATION_FREEZE_2026-10-30.md`
* Corrected R source: `research/validation/r274_s70_online_temporal_exact_v2_20261030.js`
* Complete source: `research/validation/R274_S70_ALL_576_ONLINE_SOURCE_ROWS_2026-10-30.csv`
* Exact result: `research/validation/R274_S70_ONLINE_EXACT_RESULTS_2026-10-30.json`
* B native Python moment oracle: `research/evidence_audit/b_r274_s70_independent_moment_20261030.py`
* B strict full-receipt gate: `research/evidence_audit/b_r274_s70_strict_receipt_gate_20261030.js`
* B machine audit: `research/evidence_audit/B_R274_S70_INTERNAL_EXACT_GATE_RECEIPT_2026-10-30.json`

Native Node CLI on the archived R and B scripts: NOT_RUN. New GitHub Actions: NOT_RUN, no runner dispatched. External independent replication: NOT_RUN. No new real human E2 or historical E3 observations. R073 model/scoring and PESEN v0.1 remain frozen. Original R274 bounded E1 scientific acceptance is unaffected; this supplement is separately labelled internal nonblind E1. No paid API, purchased data, rented GPU or charged CI was used.
