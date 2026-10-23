# R329 scientific report: finite binary expected-free-energy policy scoring
Date 2026-10-24. Original239 02-011 Active Inference (P2). Formal grade: **PASS_BOUNDED_E1_CONSTRUCTED_BINARY_EFE_ONLY**.

## English primary sources and reuse
Friston et al. (2015), *Active inference and epistemic value*, Cognitive Neuroscience 6(4):187–214, DOI 10.1080/17588928.2015.1020053. Friston et al. (2016), *Active inference and learning*, Neuroscience & Biobehavioral Reviews 68:862–879, DOI 10.1016/j.neubiorev.2016.06.022. These articles describe policy choice with pragmatic preferences and epistemic information value. R327 one-sense POMDP, R328 scalar predictive-error, R300 HMM and R326 hierarchical Bayesian reports were inspected before the freeze. They do not establish the exact policy score identity tested here. Reuse is mathematical context only. Historical ZIP itemwise content audit remains open.

## Prospective protocol and raw artificial source
Prescore protocol committed first as [15cb8ddaf57295ea3a2b6ad16f20cab4483187cb](https://github.com/edwardsage419/Psychohistory-Research/commit/15cb8ddaf57295ea3a2b6ad16f20cab4483187cb). Source and reproducible code committed later as [596012c7822ee2f555842a7d42b7e9793f2abae0](https://github.com/edwardsage419/Psychohistory-Research/commit/596012c7822ee2f555842a7d42b7e9793f2abae0).

Three prior beliefs P(S=1) in {1/4,1/2,3/4}, two outcome preference distributions C(O=1) in {1/2,3/4}, three costs for a precise sensor {0,1/8,1/4} yield 18 artificial worlds. Two policies, two hidden states and two observation labels yield **144 complete artificial joint probability source atoms**. Precise accuracy is 3/4, noisy accuracy 1/2. All source atoms have positive rational masses and are exhaustively enumerated. There are zero real participants.

## Exact mechanism and falsifiers
The direct score is G(a)=-E[ln C(O)]-I(S;O|a)+cost(a). The independent alternative is G(a)=KL(q(O|a)||C(O))+E_{q(S)}H[P(O|S,a)]+cost(a). Lower score wins; NOISY on ties. All 18 worlds passed both score identities within 1e-12. The uninformative NOISY policy has zero mutual information in all worlds.

For b=1/2,c=1/2 and precise cost 0, PRECISE G=0.562335145 versus NOISY G=0.693147181, so PRECISE is selected. At cost 1/8, PRECISE G=0.687335145 and remains selected. At cost 1/4, PRECISE G=0.812335145 and NOISY wins. Across 18 constructed worlds, PRECISE wins 8 and NOISY wins 10. This demonstrates a bounded preference/information/cost tradeoff in this project's scoring scheme.

## Reproducibility, independent audit, CI
Python source regenerates the CSV and JSON byte for byte, with tests for normalization, decomposition, zero information, two counterexamples, and replay. An independent standard-library Python auditor imports no production module, reconstructs all 144 rational joint masses and independently computes risk-plus-ambiguity scores, checks 18 world records, and rejects a deliberately tampered CSV source.

[GitHub Actions run 40035516146](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40035516146) completed **success**: Python 3.11 unit job, Python 3.12 unit job, and independent audit job all succeeded. Machine receipt pins Git blob identities. Formal E1 acceptance is scoped to these finite constructed arithmetic claims.

## Scientific limitations
This is a binary one-step constructed analogue, with project-specified observation preferences and exogenous sensor costs. It does not reproduce the original authors' neuronal or multi-step simulations, policy precision updates, neural signals, human behavior, learning, parameter recovery or external prediction. Human E2 and historical E3 remain NOT_ESTABLISHED. The directory association establishes provenance only. R073 and PESEN v0.1 unchanged. Classification, model fusion and personal decision system deferred.
