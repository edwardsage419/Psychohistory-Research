# R295 S91 prospective protocol freeze: noisy context cue and heldout Brier information

Date: 2026-10-30 UTC. Track: r. Baseline main HEAD 40abc616f8d670ac344de6db03d161c957fa1ffd. Original R295 source CSV blob c8400ce907e2f09734bbdf5f018074ce73d0b130, original program blob 146662201e92848f6fd6dad012fdbe2f5df3cad3. Original 239 v7.8 crosswalk blob 36f24235901172642c46853298aebb421f1a3552; pending154 blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f. Existing R295 closed bounded E1 unchanged.

## Fixed scientific question and original mechanism

How much can a noisy binary measurement of the context cue improve prediction of a fixed artificial habit/goal controller? Preserve R295 exactly: alpha in {0,1/2,1}, habit share lambda in {0,1/2,1}, valuation V in {0,1}, repetitions n in {0,1,2,3,4}, H=1-(1-alpha)^n, score A=(1-lambda)V+lambda*c*H, B score 1/2, ties select B. No new learning or fitting.

## Prespecified new observation mechanism

For each of 90 fixed (alpha,lambda,V,n) settings, draw true cue C independently with P(C=0)=P(C=1)=1/2. Independently flip cue observation Z with error e in {0,1/4,1/2}, P(Z != C)=e. Y=1 iff the original R295 action is A. Enumerate all (C,Z) in {0,1} squared, including zero probability atoms. Expected exactly 90*3*4=1080 fully labelled atoms and 270 settings, probability sum one per setting. No training/test leakage: no model is fit; evaluate the true conditional probabilities for an independent future draw under the same known synthetic mechanism.

Three fixed Bayes predictors: q0=P(Y=1) ignoring cue, qZ=P(Y=1|Z) observing noisy cue, qC=Y(C) oracle with true cue. For e=0,1/4,1/2 each Z has mass 1/2, so all conditionals defined. Compute exact Brier E[(Y-q)^2] by source enumeration, separately for q0, qZ, qC. Report delta=R(q0)-R(qZ). Negative controls: settings with Y(0)=Y(1) have all risks and delta zero. In cue-sensitive settings: R(q0)=1/4, R(qZ)=e(1-e), R(qC)=0, delta=(1/2-e)^2. Count cue-sensitive settings by lambda and total; no predetermined count claimed. Confirm R(q0)>=R(qZ)>=R(qC), delta nonincreasing in e and zero at e=1/2. Record exact fractions in source and results, avoid floating point.

## Independent B audit and scope

B route must read the persisted source atoms and independently reconstruct the complete 270 setting universe, verify 1080 unique atoms, all labels and probability masses, recompute Y from original formula without importing R generator, and derive the analytical conditional variance using the two cue actions and e. Check the full persisted result against this independent calculation and include adversarial malformed-source controls (duplicate, missing, wrong probability, wrong action, wrong prediction, summary alteration, evidence label inflation) with observed outcomes. Mark all such tests internal nonblind procedural replication. Original R295 frozen E1 acceptance and R073/PESEN v0.1 remain unchanged. New S91 evidence E1 only; E2=0, E3=0, external independent team=NOT_RUN. No fee, no Actions without cost verification. Source metadata and current main must be rechecked before writing. All artifacts add-only in research/validation and research/evidence_audit, coordination only in research/coordination/r. This freeze precedes any S91 result calculation.
