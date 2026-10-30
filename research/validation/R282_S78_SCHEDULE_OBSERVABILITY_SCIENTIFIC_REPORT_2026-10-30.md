# R282 S78: Identifiability of update schedules from observed trajectories
Date UTC: 2026-10-30. Baseline before freeze: 2b543b4a0593dacfff9c7f8078676f45678ec088.
Research key: (r,R282,original-5447354b+S78-v1,schedule-identification-from-observations)
Freeze committed BEFORE S78 scoring: def580607b81df0873fd54cd73ceff991f19e863.
Prior information read: original R282 full 192 source model, its terminal marginals and same-source schedule differences; this is **internal nonblind exploratory E1**. Original R282 formal bounded acceptance unchanged.

## Question
Can an observer distinguish which of the three activation schedules generated the two-agent XOR simulation when some perturbation inputs are unrecorded? All schedules use the same complete 64 six-bit source space, and each of the 192 schedule-labelled source cases has mass 1/192 under equal schedule prior. The source index is an enumeration key, never a human subject or PRNG seed.

## Frozen methods and exact results
The frozen classifier chooses the schedule with the largest observation count, ties in order SYNC, A_THEN_B, B_THEN_A. Total variation is computed from exact source counts. The four nested observation regimes are exactly those specified in the S78 freeze.

| Observed fields | Distinct observations | Bayes accuracy | Probability mass with a top-likelihood tie | TV(SYNC,A_THEN_B) | TV(A_THEN_B,B_THEN_A) |
| --- | ---: | ---: | ---: | ---: | ---: |
| t2 only | 4 | 1/3 | 1 | 0 | 0 |
| t0,t1,t2 | 64 | 1/3 | 1 | 0 | 0 |
| t0,t1,t2 and first-step eA0,eB0 | 128 | 2/3 | 7/12 | 1/2 | 3/4 |
| t0,t1,t2 and both steps' four e bits | 160 | 5/6 | 5/16 | 3/4 | 15/16 |

TV(SYNC,B_THEN_A) is also 0, 0, 1/2, 3/4 across these regimes. All 12 self-pair TV distances are zero. The remaining directed pairs are symmetric.

Confusion counts with rows true schedule (SYNC, A_THEN_B, B_THEN_A) and columns chosen schedule in the same order:
* TERMINAL and TRACE: [[64,0,0],[64,0,0],[64,0,0]].
* TRACE_E0: [[64,0,0],[32,32,0],[32,0,32]].
* TRACE_EALL: [[64,0,0],[16,48,0],[16,0,48]].

## Independent analytical explanation
For any given complete state triple (t0,t1,t2), each schedule has **exactly one** compatible sequence of four perturbation bits. Under independent fair perturbations, every such triple therefore has probability 1/64 under every schedule. Even observing the full state trajectory cannot identify the schedule if the innovations are unobserved.

The inverse disturbance map for a transition (a,b)->(x,y) is:
* SYNC: (eA,eB)=(x XOR b, y XOR a).
* A_THEN_B: (eA,eB)=(x XOR b, y XOR x).
* B_THEN_A: (eA,eB)=(x XOR y, y XOR a).

Revealing first-step innovations rules out some schedules. Revealing both steps increases discrimination further. Residual ties remain because multiple schedules can generate the same observed states with the same recorded innovations.

This result is compatible with original R282's 48/64 **same-source** t2 disagreements. Paired-source counterfactual trajectories differ while unpaired observational state distributions can coincide. The distinction is conditional on the artificial fair innovation distribution and fixed two-step horizon.

## Evidence and execution
R source: `research/validation/r282_s78_schedule_observability_20261030.js`, complete 192 rows: `research/validation/R282_S78_ALL_192_SOURCE_OBSERVATIONS.csv`, exact result: `research/validation/R282_S78_EXACT_RESULTS.json`.
Independent B: `research/evidence_audit/b_r282_s78_inverse_schedule_oracle_20261030.js` enumerates 64 state triples per schedule, inverts perturbations and independently reproduces every regime's confusion, observation support, tie mass and TV values.
Persisted remote receipts were re-read and checked by `research/evidence_audit/b_r282_s78_strict_remote_receipt_gate_20261030.js`: 192 full rows, all 4 summaries and 36 TV cells PASS, seven corruptions rejected. Details in `research/evidence_audit/B_R282_S78_INVERSE_ORACLE_REMOTE_RECEIPT_AND_MUTATIONS_2026-10-30.md`.
Executed inside isolated V8 and an independent Python Fraction exploratory cross-check; archived native Node CLI NOT_RUN, GitHub Actions NOT_RUN, external independent replication NOT_RUN. New formal scientific acceptance: PARTIAL exploratory. The original R282 bounded E1 acceptance remains unchanged.

## Limits and next
No empirical human decision rule, no observational noise, no missing states, no fitted probabilities, no true external independent validation. An alternative perturbation distribution may make trajectories informative without recording perturbations; this is a **new untested hypothesis** requiring a new frozen protocol.
New human E2 prediction=0, historical E3=0. R073 model and scoring rules and PESEN v0.1 remain frozen. No paid data, API, cloud, or CI started; billing/free quota NOT_VERIFIED.
