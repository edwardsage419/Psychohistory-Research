# R333 S129 prospective freeze: intervention timing and delayed reciprocal effects

Date: 2026-11-01 UTC. Target key (r,R333,S129-v1,intervention_timing_delayed_feedback). New artificial E1 extension; original R333 is unchanged.

## Frozen source
R333 original239 03-002 Social Cognitive Theory, frozen protocol blob f66b8437f63bce079a7f10a0b8b82311dbdc64a4; original code blob c28c82a6a18ababe8da14b0f48c846d940bf32b3; original CSV blob 8a202f773badb8833992ff0df25c3c90f60b3680; original 32-world JSON blob dd82e1f616528742622ebafc844ec66adadf18b5. Bandura 1989 DOI 10.1037/0003-066X.44.9.1175 and Bandura 2001 DOI 10.1146/annurev.psych.52.1.1 are conceptual sources, not equations for this invented model.

## Question
How does shifting the imposed behavior intervention from t=1 to t=2 alter the delay and persistence of its effect on person and environment variables in two invented Boolean mechanisms? The original R333 t=1 intervention is the compatibility anchor.

## Prespecified finite design
Initial (P0,B0,E0) enumerates all eight binary triples. Two mechanisms: cyclic P'=P XOR E, B'=P XOR B, E'=B XOR E; feedforward P'=P XOR E, B'=P XOR B, E'=E. Synchronous transitions use old state. For each mechanism, initial triple, intervention value d in {0,1}, and intervention time tau in {1,2}, compute t=0..4. At the update producing time tau, replace B_tau with d after computing the simultaneous P and E updates; at all other times B'=P XOR B. Original R333 trace at tau=1 must be recovered for all 32 original worlds and all 160 state rows. New universe: 2*8*2*2=64 worlds and 320 rows, ordered cyclic/feedforward, initial P/B/E lexical, d, tau, t. Store full CSV and 64-world JSON, exact deterministic bytes.

## Frozen falsifiers
1. All 64 worlds and 320 rows complete, binary states only, correct time and key uniqueness.
2. For each tau, comparing d=0 and d=1 at fixed mechanism and initial triple changes E_(tau+1) for all eight cyclic initial states and none of the feedforward states.
3. For each tau, the same paired intervention changes P_(tau+2) for all eight cyclic initial states; for feedforward P_(tau+2) is unaffected.
4. At tau=1, full original R333 160-row and 32-world states and final outputs must match, including the original mechanism ordering and source identities.
5. For tau=2, report the t=4 outcome differences between d=0/1 and compare them with tau=1; no post hoc parameter change. The effect at time t<=tau on E is zero because the intervention only overwrites B_tau after the transition. A violation is FAIL.
6. Independent no-import Python exact enumeration and explicit negative controls for missing/duplicate rows, wrong timing, state flip, wrong world summary, and evidence upgrade.

## Scope
Only E1 invented Boolean transitions. The artificial do(B_tau) operation is not a randomized human intervention. No inference of real cognitive agency, social feedback causality, human E2, historical E3, calibration or external replication. No GitHub Actions without verified free billing quota. R073, PESEN v0.1 and original R333 acceptance frozen; R series before classification/fusion; personal product paused.
