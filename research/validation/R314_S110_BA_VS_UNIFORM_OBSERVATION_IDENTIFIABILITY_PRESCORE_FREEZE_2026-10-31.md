# R314 S110 pre-score freeze: preferential versus uniform attachment under observation coarsening

Date: 2026-10-31 UTC. Track r. Status: PRESCORE_FROZEN. Baseline main HEAD 6eeb7b2f76cdd3992bdab24bea7c8f0a896dba8c.

## Provenance and scope
Read R314 original prescore protocol `protocols/R314_BARABASI_ALBERT_THREE_SEED_TWO_ARRIVAL_54_TARGET_SOURCE_PRESCORE_FREEZE_2026-10-24.md` (blob a9cf305df9fb24ca5fa84b0768fe2c179c847273), original 54 source atoms (blob 063fd8b52f3aa425ccb9d61f26496d2db8365b9a), 44 two-arrival paths (blob e49b94e282fde0b2772af3a8d42b8ed84b000564), original acceptance (bounded E1 only), original239 crosswalk v7.8 (blob 36f24235901172642c46853298aebb421f1a3552), pending 154 queue (blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f). Original R314 model, acceptance and source bytes are immutable. This is an **additional finite artificial E1 question**, not an empirical network or scale-free exponent test.

## Fixed model comparison
For each of exactly three frozen labeled seed graphs P3, K3, S4, use exactly two sequential arrivals, one undirected edge per arrival, new vertex ID equal to old vertex count. Two hypotheses with equal prior probability 1/2:
* H_BA: existing vertex i chosen with probability degree(i)/sum_old_degrees. Use original R314 44 paths as fixed BA source and verify every path probability.
* H_U: existing vertex i chosen with probability 1/n_old. This is a prespecified negative-control mechanism, with the same seeds, arrivals and support.
For each seed, enumerate all n(n+1) ordered target pairs. No fitting or sampling. All arithmetic exact Fraction.

## Prespecified observations
O0: full ordered target pair (first_target, second_target).
O1: final **labeled** degree vector (vertex IDs in order, including both arrivals).
O2: sorted final degree multiset (nondecreasing; labels removed).
O3: final maximum degree alone.
For each observation, push forward each hypothesis' complete path probabilities into observation cells. Compute total variation TV(P,Q)=sum_cells |P(cell)-Q(cell)|/2; equal-prior Bayes-optimal classification accuracy (1+TV)/2; error (1-TV)/2; cell count; and explicit likelihood-ratio diagnostic for each O0 path. For O0, also compute BA versus U likelihood ratio P_BA(path)/P_U(path) and expected BA log-likelihood ratio is **excluded** (irrational logs). Verify probability mass 1 under each hypothesis at each observation, TV nonincrease O0>=O1>=O2>=O3, and accuracy in [1/2,1]. Report any equalities as found, never presuppose strictness.

## Controls and negative examples
K3 first arrival alone must have TV=0, since initial degrees equal; second arrival can distinguish the hypotheses. Check original BA source probabilities for all 44 paths exactly, not merely aggregate counts. Check no path omitted/duplicated, original edge structure, degree conservation, and correct update of target degrees before second arrival. Mutations to test: duplicate path, omitted path, BA probability corruption, uniform probability corruption, labeled degree corruption, observation coarsening corruption, TV summary corruption, E1-to-E2 grade escalation. Mutation checks must be explicit exceptions and work under Python -O. Retain any failed checks as evidence.

## Scientific boundary
Outputs: immutable freeze, complete path table CSV (44 rows), observation summary JSON (3 seeds x 4 observations), deterministic generator script, separate independent non-importing Python audit, scientific report and A public data gate. Internal independent implementation is **nonblind procedural verification**, not external replication. E1 only; human E2 and historical E3 zero. No empirical fitting, sample-out evaluation or calibration claims. R073 scoring/model and PESEN v0.1 remain frozen. No changes to original239 crosswalk, queue, historical files, other tracks. No paid services or CI dispatch without independently verified free billing.
