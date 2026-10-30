# R290 S86 prospective finite likelihood training and independent heldout risk protocol

Date 2026-10-30 UTC. This file is committed before generating S86 results. It extends the original R290 2026-10-23 finite artificial signal detection protocol at commit 696e86b029581d2b00dc79bdd2219c59427a7980. Original R290, R073, PESEN v0.1, original239 v7.8, and pending154 remain unchanged.

## Scientific question and evidence boundary

In the 12 frozen artificial worlds, how does a likelihood decision rule trained on 1 or 2 labeled observations per class perform on a completely independent future observation? Evaluate exact expectation over every training sample and heldout class/evidence distribution. E1 artificial mathematics only; no human E2, historical E3, external team, or original Tanner/Swets empirical replication. This is a new complementary question, not a reacceptance of original R290.

## Fixed data generating processes and losses

Evidence x=0,1,2,3,4. Conditional noise/signal probabilities:
MONOTONE noise (8,6,4,2,1)/21; signal (1,2,4,6,8)/21.
CENTERED noise (8,2,1,2,8)/21; signal (1,3,13,3,1)/21.
IDENTICAL noise=signal (1,2,3,2,1)/9.
Known heldout signal prior pi in {1/2,3/4}; costs (FP,FN) in {(1,1),(1,3)}. All are fixed before any S86 scoring.

## Fixed training, estimator, policy and scoring

Two sample sizes m=1 and m=2, with exactly m independent noise-labeled draws and m independent signal-labeled draws, conditionally i.i.d. within each class. Training labels are observed. Each draw has five possible bins. Enumerate ordered training samples exhaustively: 5^(2m) training sequences per DGP, hence 25 and 625 per world. Preserve their exact product probabilities, including repeated observations. The independent future heldout observation is sampled afresh using prior pi and original true class-conditional probabilities.

For each class, compute five empirical bin counts k_x. Use fixed add-one categorical smoothing: estimated P(x|class)=(k_x+1)/(m+5). The plug-in rule predicts signal for bin x iff pi * FN * estimated P(x|signal) > (1-pi) * FP * estimated P(x|noise); exact ties predict noise. No model selection or tuning after seeing results. Evaluate each training-dependent rule on the true independent heldout distribution using weighted FP/FN risk. Sum exact probability-weighted risks over all training sequences. Compute exact risk of the known-distribution Bayes rule as oracle, best fixed single cutoff t=0..5 (smallest t in ties), fixed t=3, and the best constant rule as descriptive baselines. The oracle risk is a lower bound. No claim that risk decreases monotonically from m=1 to m=2; report any nonmonotonicity as found.

## Prespecified output and negative controls

R route: Python standard library Fraction, explicit ordered sample enumeration, exact training probability mass and risk, per-world m1/m2 aggregate, 12 worlds and 24 results. Persist machine-readable JSON, source script and scientific report. Exact training probability mass per world/m must be 1. All expected regrets relative to true Bayes must be nonnegative. All rule predictions binary. Preserve exact fractions, not float rounding.

B route: independent implementation without importing R route; for each evidence bin use independent binomial count distributions for the noise and signal training counts and evaluate the expected decision cost for that bin. This 5-bin marginal count route must reproduce all 24 expected risks exactly. Audit the tie-negative convention, source coverage, independent heldout evaluation, and oracle/baseline inequalities. Negative controls must reject at least duplicate/missing training-source identifiers, probability mass corruption, swapped class counts, and E1-to-E2 promotion if implemented; report each actually executed test, never invent it.

No paid API, data, cloud, GPU or Actions. Native local CLI preferred. GitHub Actions only if no cost is confirmed. Any deviation requires an append-only erratum preserving this freeze. Original 239 metadata and existing frozen R290 acceptance remain untouched.
