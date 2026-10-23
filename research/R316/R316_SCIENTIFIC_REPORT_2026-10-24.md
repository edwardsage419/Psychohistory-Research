# R316: exact known-block Bernoulli stochastic block model E1

Date 2026-10-24 Asia/Taipei. Original239 candidate **04-019 Stochastic Block Model**, P1.

## First party paper and explicit limited rule

Holland, Laskey and Leinhardt (1983), *Stochastic blockmodels: First steps*, *Social Networks* 5(2):109–137, https://doi.org/10.1016/0378-8733(83)90021-7 . Original paper introduced stochastic block model approaches including more elaborate relation settings. Here only a clearly specified fixed-known-membership, undirected independent Bernoulli planted-partition special case is implemented. The mechanism is *not* an inference algorithm for unknown groups and does not model reciprocated directed ties.

The [R316 freeze](../../protocols/R316_SBM_KNOWN_BLOCK_FOUR_NODE_768_DYAD_SOURCE_PRESCORE_FREEZE_2026-10-24.md) was committed at `8a9730882203dffbf46e1ef843bb8f52b2b9674d` strictly before source scoring. Four nodes 0,1,2,3 in blocks (0,0,1,1), six unordered candidate edges, two within and four cross. Fixed A regime: within p=3/4 and cross p=1/4; fixed D: within p=1/4 and cross p=3/4. All edges independent conditional on fixed block labels and regime.

## Finite exhaustive result

Each regime has **64 full undirected graphs**. Exactly 2×64×6=**768 graph-dyad source factors** and **128 full graph probabilities** are recorded as rational values, without sampling or fitting. All graph likelihoods are products of six independent Bernoulli factors. The total mass of each 64 graph distribution equals 1 exactly, independently also established via the 2-within × 4-cross binomial grouping.

* Assortative expected within and cross edge counts: 3/2 and 1, giving expected total 5/2.
* Disassortative expected within and cross edge counts: 1/2 and 3, giving expected total 7/2.
* Within-only graph mask 33 (`100001`) has exact likelihood A=729/4096 versus D=1/4096, for conditional likelihood ratio 729 in favor of A. This uses the chosen fixed likelihoods and known group identities. It is not empirical posterior evidence for actual human group segregation.
* Empty graph likelihood A=81/4096, D=9/4096. Complete graph A=9/4096, D=81/4096.
* Full known-parameter A versus D total variation distance across all 64 graph outcomes is **203/256**. This is mathematical distinguishability under frozen synthetic parameters, not cross-population prediction, classifier accuracy on people, or latent-group identifiability.

Each CSV atom records its original source world, the dyad, same/different block, observed counterfactual graph edge bit, parametric edge chance, Bernoulli factor and full graph product. It is an enumerated artificial graph configuration, not a real observed person-to-person tie.

## Reproducibility gate

* [768 complete dyad source atoms](R316_ALL_768_ORIGINAL_GRAPH_DYAD_PROBABILITY_ATOMS.csv), [128 exact graphs and total variation](R316_EXACT_128_GRAPH_LIKELIHOODS.json).
* [Main rational model and explicit unit tests](r316_exact_sbm.py). [Independent no-import audit](../catalogue_audit/independent_r316_sbm_source_audit.py) verifies every atom, reconstructs 128 likelihoods, and separately checks binomial combinatorial normalization.
* [CI workflow](../../.github/workflows/r316-sbm-two-block-exact-e1.yml) must finish 3 jobs success (Python 3.11, Python 3.12 and independent source audit) before formal bounded E1 acceptance. Otherwise report remains pending and no main original239 linkage is promoted.

Real human E2=0, historical E3=0. No parameter recovery, observed network analysis, community identification or causal mechanism demonstration. R073 and PESEN v0.1 remain frozen. Finish R studies first, then categorize, finally model fusion.
