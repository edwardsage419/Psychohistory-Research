# R316 S112: Exact information loss under known-block SBM observation coarsening

Date: 2026-10-31 UTC. Scientific status: **PARTIAL_E1_EXTENSION**. Original R316 bounded E1 acceptance remains unchanged.

## Pre-score freeze and provenance
Freeze commit: `af948405bc682f10cdf6f3add73ab2f35e10c0b4`. Main baseline before freeze: `b5749b94bcc7685bfbaee6ccfd0266d8f4d21335`. Original R316 source is `research/R316/R316_EXACT_128_GRAPH_LIKELIHOODS.json`, Git blob `36da587adbc6e1d92824a5fd39516e506569166c`. The original R316 source contains two regimes and 64 graph outcomes per regime, with six dyads and fixed blocks (0,0,1,1). A has within probability 3/4 and cross probability 1/4; D reverses these. All 128 original graph likelihoods are artificial exact probabilities. No original R316 file or prior acceptance was changed.

Question: Given one fully observed graph and a 1/2 prior on each of two fixed regimes, how much optimal classification information remains after six predefined observation maps? The zero-one Bayes accuracy is (1/2) sum over observation bins of max(P_A(bin),P_D(bin)). The source graph is exactly enumerated; there is no training, sample splitting, estimated parameter or empirical holdout.

## Exact results
| Observation | Distinct bins | Exact Bayes accuracy | Total variation |
| --- | ---: | ---: | ---: |
| Full labeled six-edge graph | 64 | 459/512 (89.6484%) | 203/256 |
| Pair of within/cross edge counts (w,c) | 15 | 459/512 (89.6484%) | 203/256 |
| Signed edge-count contrast w-c | 7 | 459/512 (89.6484%) | 203/256 |
| Within edge count w only | 3 | 3/4 (75%) | 1/2 |
| Cross edge count c only | 5 | 27/32 (84.375%) | 11/16 |
| Total edge count w+c only | 7 | 345/512 (67.3828%) | 89/256 |

All six distributions normalize to one under each regime. Accuracy equals (1+TV)/2 in each case. The full graph TV exactly reproduces the original R316 value 203/256.

## Analytical explanation
For a graph with w within-block edges among two possible within dyads and c cross-block edges among four possible cross dyads, the exact likelihood ratio is

`P(graph|A)/P(graph|D) = 3^(2(w-c+1))`.

Thus the signed contrast w-c retains all information needed for optimal binary discrimination between these **two specified regimes**. A full graph contains additional edge identities but those identities cannot improve this particular fixed-prior classification decision. A deterministic optimal rule selects A when w-c+1>0, selects D when w-c+1<0, and uses a fixed tie choice when w-c+1=0.

The total edge count discards whether ties lie within or across blocks, reducing the exact best accuracy to 345/512. Observing only cross-block edges retains more discrimination (27/32) than observing only within-block edges (3/4) in this specific artificial design, because there are four cross-block opportunities and only two within-block opportunities. These are design-dependent mathematical results.

## Independent verification and limits
R scorer `research/validation/r316_s112_observation_coarsening.js` reads the original archived graph probabilities, verifies source Git blob identity and computes the six exact observation distributions. Its archived receipt is `research/validation/R316_S112_OBSERVATION_COARSENING_EXACT.json`.

Independent B program `research/evidence_audit/b_r316_s112_independent_binomial_oracle.py` reconstructs every Bernoulli graph likelihood and independently groups the binomial counts with combinatorial coefficients, without importing the R scorer. On a local byte-identical reconstruction of the original Git blob, the native Node `--check` passed. Python normal and optimized execution passed the independent oracle and rejected all eight deliberate mutations. The local reconstruction matches the GitHub original source Git blob exactly; the archived R/B scripts and receipt were then uploaded and their remote Git blobs compared with the locally executed copies. This is **internal nonblind programmatic verification**, with no external-team replication or remote Actions run.

A development failure occurred: the first local Python audit script contained an invalid generator expression and raised SyntaxError. The expression was corrected before final B verification; both successful executions were rerun. This failure is preserved in this report.

## Evidence boundary
All results are E1 artificial exact decision theory. There are no human network observations, unknown community inference, observed predictive calibration, empirical out-of-sample assessment, bootstrap intervals, external independent replication, or historical forecasts. This finite result does not establish sufficiency for general stochastic block models, unknown block assignments or other parameter values. New E2=0, E3=0. R073 and PESEN v0.1 remain frozen. No GitHub Actions dispatched and no new paid services used.

## Replay
```sh
node research/validation/r316_s112_observation_coarsening.js --check
python research/evidence_audit/b_r316_s112_independent_binomial_oracle.py
python -O research/evidence_audit/b_r316_s112_independent_binomial_oracle.py
```
