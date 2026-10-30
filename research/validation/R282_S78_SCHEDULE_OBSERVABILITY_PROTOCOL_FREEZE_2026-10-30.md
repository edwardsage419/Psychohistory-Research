# R282 S78 schedule identifiability under hidden versus recorded perturbations
Date UTC: 2026-10-30. Baseline main: 2b543b4a0593dacfff9c7f8078676f45678ec088
Research key: (r,R282,original-5447354b + S78-v1, schedule-identification-from-observations)
Evidence: planned E1 artificial, internal nonblind exploratory. Prior R282 results and complete 192-source archive have been read. No claim of prospective blindness.

## Immutable original mechanism
Three equiprobable schedules SYNC, A_THEN_B, B_THEN_A, each paired with exactly 64 equiprobable six-bit primitive sources `a0 b0 eA0 eB0 eA1 eB1`, indexed 0..63. Original two-agent XOR transitions at t0->t1 and t1->t2 are unchanged. The 192 labelled cases have prior mass 1/192. No source is a human subject.

## Frozen observation regimes and estimand
Evaluate exactly four regimes:
1. TERMINAL: t2 joint two-bit state only.
2. TRACE: ordered joint states t0,t1,t2, no innovation bits.
3. TRACE_E0: ordered joint states plus eA0,eB0, but not second-period innovations.
4. TRACE_EALL: ordered joint states plus eA0,eB0,eA1,eB1.
Each observed field is an exact string/bit, no observation noise. Observers know the candidate schedule mechanisms and equal schedule prior, and do not observe source index except through stated fields.

For each regime, compute integer `n[s,o]` as count of source indexes yielding observation o under schedule s. Require each schedule's sum of counts =64. The posterior schedule probability given o is `n[s,o]/sum_s n[s,o]`. Classifier selects the maximum-count schedule with deterministic tie order SYNC, A_THEN_B, B_THEN_A. The exact unconditional classification accuracy is `sum_o max_s n[s,o]/192`. For every ordered pair of schedules compute total variation `sum_o abs(n[s,o]-n[t,o])/128`. Record full 3x3 confusion counts (true schedule rows, selected schedule columns), number of distinct observations, posterior tie mass, and exact rational accuracies. A tie is counted when at least two schedules share maximum count; report its total joint probability mass. No post-hoc change of tie rule.

## Falsification and acceptance
The new research must retain any failed expectations and all zero-probability observation cells. No guaranteed positive identification claim is preregistered. Verify source completeness, masses, t0/t1/t2 via the original frozen transition definitions, monotonic Bayes accuracy under nested observation regimes (TERMINAL <= TRACE <= TRACE_E0 <= TRACE_EALL), and independent second-route calculation that does not import the R enumerator. Preserve any discrepancy. R and B independently compare 4 accuracies, 4 confusion matrices, 24 pairwise TV values (including self pairs if generated), all schedule observation counts, and tie masses. Mutations must reject duplicate source, dropped source, wrong schedule, altered observation and false evidence-grade upgrade. Do not call GitHub Actions until verified no new billing; default NOT_RUN. No retroactive modification to original R282 formal acceptance or original S77 failed assertion.

## Scope
This study examines identifiability from artificial observations, not social behavior, empirical calibration, external blind replication, or the Grimm et al. ODD standard's certification. R073 and PESEN v0.1 remain FROZEN. E2=0, E3=0. Write only new research/validation, research/evidence_audit, research/data_scout and research/coordination/r paths after rechecking HEAD and target absence.
