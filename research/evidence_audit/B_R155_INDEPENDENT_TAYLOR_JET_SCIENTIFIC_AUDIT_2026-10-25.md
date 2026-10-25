# B scientific audit: independent Taylor expansion of R155 Bass initial sales

Date: 2026-10-25 UTC+08. Target: the new R155 synthetic initial-jet identification conclusion. This is an independent **method and implementation inside the same project**, not an external team replication. Prescore scope fixed in [R155 protocol](../validation/R155_INITIAL_JET_IDENTIFICATION_PROTOCOL_FREEZE_2026-10-25.md), freeze commit `d19dc9a92ff2b099671c03d07c1ef974d0bf5a8c`.

## Independent reconstruction
Main method differentiates the Riccati right-hand side directly. B method instead solves the Taylor coefficient equations of `F'=p+(q-p)F-qF^2`, with `F=a1 t+a2 t^2+a3 t^3+...`:

`a1=p`, `a2=(q-p)*a1/2`, `a3=((q-p)*a2-q*a1^2)/3`.

The independently derived jet is `(m*a1,2*m*a2,6*m*a3)`. B reads the archived 75-row JSON solely as the target for exact row-by-row comparison and never imports the main research script.

Actual standard-library Fraction replay: **75/75 exact row matches, 60/60 positive-p inverse identities, 15/15 zero-p degeneracy blocks**. The predeclared nonlinear-term deletion mutant omits `-qF^2`, causing a detectable third-derivative mismatch in **48/48 worlds with p>0 and q>0**. Source: [independent audit script](r155_b_independent_series_audit.py); [machine receipt](R155_B_INDEPENDENT_SERIES_AUDIT_RECEIPT_2026-10-25.json).

## Scientific validity and acceptance gates
The first derivative pair `S0,S1` identifies the 60 positive-p worlds on the chosen finite parameter grid. The continuous parameter space still admits different `p,q,m` with identical `S0,S1`; the main report gives an explicit exact-rational pair. The third component resolves this pair. The `p=0` boundary is unidentifiable even with all derivatives because the zero-seed adoption path is identically zero.

This is an algebraic mechanism proof with known start time and noise-free instantaneous derivatives. There are no empirical participants, independent sessions, calibration curves, resampling confidence intervals, observational data leakage checks, or heldout prediction scores to compute. These missing gates are **NOT_APPLICABLE_TO_E1** and remain required before any E2/E3 claims. No postscore tuning occurred. The original R155 acceptance is unchanged.

Evidence classification: E1 bounded internal pass. New E2=0, new E3=0, external replication=0. No paid resources and no newly requested Actions run. R073 and PESEN v0.1 remain frozen.
