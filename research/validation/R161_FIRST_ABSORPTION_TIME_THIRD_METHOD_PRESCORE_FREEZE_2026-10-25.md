# R161 supplementary prescore freeze: exact first absorption time

Date: 2026-10-25. Scope: retrospective extension of already CLOSED_BOUNDED_E1 R161; this protocol is frozen before any new absorption-time calculations. It does not change the original R161 frozen model, results, source code, acceptance status, R073 or PESEN v0.1.

## Fixed source and sample universe

Use existing original source `research/R161/r161_finite_conformist_markov.py` and original immutable `research/R161/R161_EXACT_RESULTS.json`. Frozen population sizes N=5,7; conformist strengths h=0,1/4,1/2,1. Original six initial states for each N give 48 synthetic cases, with 8 distinct transition kernels. No human data. Fixation is first entry into count 0 or count N; time starts at t=0, so already absorbing starts have expected time 0. No new parameter tuning.

## Independent computation and success criteria

Method R: reconstruct exact binomial transition probabilities with Python standard-library Fraction. For each of 8 kernels solve (I-Q)t=1 on transient counts 1..N-1 by exact rational Gaussian elimination, with t[0]=t[N]=0. Check exact first-step identity for all N+1 states and nonnegative finite solutions. Check exact reflected symmetry t[k]=t[N-k]. For each of the 48 frozen starts record expected first absorption time as a rational string. Record all 8 full-state vectors, plus contrast neutral h=0 with h=1 for each population size and starting state. No prespecified direction of this contrast.

Method B: separate implementation that enumerates all 2^N binary learner configurations to reconstruct each transition row, then computes survival probabilities s_t=P(0<K_t<N) from an independent row-vector recurrence, with 60-digit Decimal arithmetic. Since max transient row retention rho<1, the uncomputed expected-time tail after L terms is bounded by rho^L/(1-rho). Increase L until this theoretical bound is <1e-12, with a hard cap of 10000 steps. Compare independent Decimal survival-sum expectation to exact Fraction result within 1e-10 for each of the 48 initial states. Record actual L, rho and bound; a failed bound is OPEN rather than PASS. Compare all 8 transition kernels against the immutable original JSON using exact rational strings.

Negative controls: deliberately treat k=0 as transient and verify its expected absorption time changes from 0; deliberately omit the first survival term for transient starts and verify a discrepancy of 1. If a mutant is not detected, report FAIL. All executed failures and amendments must remain visible.

## Evidence and stopping

E1 synthetic mathematics only. An internal independently coded method is not an external-team replication. Do not claim human behavioral forecasting, causal identification, calibration, E2 or E3. Preserve original acceptance and 154-item audit queue. Do not trigger billable CI. If computational or source checks fail, archive the exact blocker and leave stage OPEN. New files only under `research/validation/` and `research/evidence_audit/`; recheck main HEAD and destination absence immediately before writes.
