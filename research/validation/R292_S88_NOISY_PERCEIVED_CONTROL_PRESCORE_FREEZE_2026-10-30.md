# R292 S88 prescore protocol: noisy perceived control and forecast information loss

UTC date: 2026-10-30. Research track r. Baseline main HEAD: 6392a8921f7142865a0993f8cc169fb3d4032fd8.
Target key: (r,R292,S88-v1,noisy perceived control proxy and out-of-sample Brier).
Status: PRE-SCORE FREEZE. This file must be committed before the first S88 result is computed.

## Original frozen model

Read R292 original prescore protocol and original Python implementation from main, R292 original E1 status CLOSED_BOUNDED_E1. Preserve all eight original synthetic worlds: profiles BALANCED=(1,1,1), CONTROL_HEAVY=(1,1,2), CONTROL_NULL=(1,1,0), NORM_HEAVY=(1,2,1); kappa in {0,1}. A,N,C independent fair signs, I Bernoulli(1/2+(a*A+n*N+c*C)/16), F Bernoulli(1/2+kappa*C/4) conditionally independent, B=I*F. No change to original protocol, original source or R073/PESEN.

## New S88 observation design, fixed before scoring

An observed binary control score Z equals latent perceived control C with probability 1-epsilon and -C with probability epsilon, conditionally independent of I,F,A,N given C. Epsilon is exactly 0, 1/4 or 1/2. Z is observed at prediction time, while I,F,C are hidden. Compare:
1. FULL_ANZ = P(B=1 | A,N,Z), exact marginal over C.
2. TRA_AN = P(B=1 | A,N), exact marginal over C,Z.
3. CONSTANT = P(B=1).
4. ORACLE_ANC = P(B=1 | A,N,C), informational upper benchmark unavailable to noisy-score predictor.

Use Brier score on fresh independent action B drawn from the same fixed artificial distribution, evaluated as complete population expectation, never train on heldout outcomes. Enumerate all 2^6=64 tuples (A,N,C,I,F,Z) for each of 8 worlds x 3 epsilon settings, including zero-mass cells at epsilon 0 and 1/2 if any. Total 1536 complete labelled cells; mass 1 within each world. Exact rational arithmetic. The source key must include all six binary variables, profile, kappa, epsilon. Export CSV, JSON with per-world risk, strict source checker and scientific report. No synthetic dataset may be relabelled E2 or E3.

## Independent mathematical check, fixed before scoring

Let mu=1/4+c*kappa/64, D=(a*A+n*N)/32, H=(c+4*kappa)/32+kappa*(a*A+n*N)/64 and t=1-2*epsilon.
Then ORACLE_ANC=mu+D+C*H, FULL_ANZ=mu+D+t*Z*H and TRA_AN=mu+D.
Set V=(c+4*kappa)^2/1024 + kappa^2*(a^2+n^2)/4096.
Expected risk improvements: R_TRA - R_FULL_ANZ=t^2*V, R_FULL_ANZ - R_ORACLE_ANC=(1-t^2)*V. R_TRA-R_ORACLE_ANC=V.
R_CONSTANT-R_TRA=(a^2+n^2)/1024. Negative control CONTROL_NULL kappa0 has V=0 at every epsilon; at epsilon=1/2 Z has no information in any profile. Check all 24 worlds and original R292 risk parity at epsilon0. Independent B auditor must reconstruct probabilities from source fields or use a different conditional aggregation algorithm and must not import R program.

## Acceptance and adverse checks

Freeze before execution. Verify 1536 unique cells, all masses, all conditional probabilities, zero-mass handling, all four risk columns, exact 24 risk vectors and monotonic information ordering. Reject duplicate/missing source keys, probability edits, outcome edits, forecast edits, wrong epsilon and summary edits using explicit exceptions rather than assertions alone. Distinguish internal nonblind independent-method check from external-team independent replication. Preserve any failed attempts and report them. No claim of full scientific acceptance without complete required gates. No paid services, no Actions dispatch until free entitlement verified. Original R292 E1 closure remains unchanged; S88 remains bounded supplementary E1, pending external replication and empirical E2/E3.

A track must independently check a free public dataset candidate and record actual access/identity/license limitations. B track audit stays separate. No overwrites. Codex PRs remain unmerged evidence.
