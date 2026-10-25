# R170 third method: exact observation ladder for artificial two-word naming games

Date: 2026-10-26 Asia/Singapore. Catalogue P2 / 07-012 Language Evolution Models. Protocol frozen first at commit `6bba9f855b470ecbc7fe1a8a373468083a874c0c`. Prior R170 `CLOSED_BOUNDED_E1` unchanged. Status of this extension: `PASS_BOUNDED_INTERNAL_E1`.

## Research question and design

For each of the 12 frozen graph and initial-inventory strata, compare six known controls (noise 0, 1/4, 1/2 crossed with both-confirm and listener-only feedback). Propagate the complete exact probability distribution of all four labeled agents at t=0,1,2,3, and compare control equivalence under O1 total bilingual speakers, O2 complete inventory histogram, O3 histogram plus disjoint-contact-edge count, O4 full labeled inventory state. All comparisons use exact rational equality of **probability laws**, with 180 within-stratum unordered control pairs. This is a model-identification calculation assuming access to exact probability distributions, **not** a claim that a single observed 3-event trajectory can identify controls.

## Results

| time | observation | classes summed over 12 strata | uniquely identified worlds / 72 | ambiguous worlds | distinguishable control pairs / 180 |
| --- | --- | ---: | ---: | ---: | ---: |
| t1 | O1 bilingual count | 38 | 12 | 60 | 132 |
| t1 | O2 inventory histogram | 60 | 51 | 21 | 164 |
| t1 | O3 histogram plus disjoint edges | 60 | 51 | 21 | 164 |
| t1 | O4 labeled inventories | 60 | 51 | 21 | 164 |
| t2 | O1 | 65 | 61 | 11 | 170 |
| t2 | O2 | 72 | 72 | 0 | 180 |
| t2 | O3 | 72 | 72 | 0 | 180 |
| t2 | O4 | 72 | 72 | 0 | 180 |
| t3 | O1 | 72 | 72 | 0 | 180 |
| t3 | O2 | 72 | 72 | 0 | 180 |
| t3 | O3 | 72 | 72 | 0 | 180 |
| t3 | O4 | 72 | 72 | 0 | 180 |

The frozen grid has finite-time observational equivalences at t1, with the count-only observation losing more distinctions than the inventory histogram. O3 and O4 add no **control-class** distinctions beyond O2 in this grid, despite containing more information about individual states. At t3 the exact distribution of the bilingual count distinguishes all six controls within every fixed stratum. This finite-grid result does not extend to unknown initial conditions, unknown graphs, arbitrary noise values or finite empirical samples. Additional real observations would require sampling-error assessment, held-out predictive scoring and calibration.

Prespecified first witness: path graph, split initial inventories, t1, nu=1/4. `both_confirm` and `listener_only` have identical O1 laws, TV=0, while the complete labeled-state distributions differ with TV=1/12. This is an exact counterexample to inferring feedback from bilingual counts alone at t1.

## Execution and controls

Executed JavaScript BigInt exact rational program with two separately coded event kernels. Directed-pair delivered-token mixture and undirected-edge speaker-utterance-flip enumeration agree on all **288 complete four-agent state-distribution snapshots** (72 worlds times four timepoints); all 288 are normalized. For all eight graph/monolingual-start combinations, the two feedback rules agree at t1 when nu=0. Out-of-grid nu=1/3 mutation against frozen nu=1/4 for path/bilingual/both-confirm at t1 changes the O4 law with TV=1/24. All 36 stratum-time refinement checks pass.

A separately implemented Python Fraction B route was locally executed and reproduced all 12 aggregate class/unique/ambiguity/pair counts, the first witness TV=1/12, the mutation TV=1/24 and eight monolingual controls. This cross-language comparison is of aggregate results and named witnesses; the JavaScript's exact 288 full-state equality uses its two event kernels sharing the same state-update helper. Do not upgrade the Python check to independent full-state equality without comparing all Python state masses. The original R170 already had two exact Fraction oracles and 111 tests; the extension is a new observation-information question, not a new original-author replication.

## Science scope, source and next gate

Evidence `E1_INTERNAL_FINITE_ONLY`. New E2 human prediction=0; new E3 historical validation=0; external team replication=0. Original naming-game inspiration: Baronchelli et al. (2006), DOI https://doi.org/10.1088/1742-5468/2006/06/P06014. The project-specific two-word cap and channel mutation are outside that paper's original model. No original author human data, grammar, large-population scaling or empirical calibration is established.

See `research/validation/r170_observation_ladder_20261026.js`, `research/validation/R170_OBSERVATION_LADDER_EXACT_RECEIPT_2026-10-26.json` and frozen protocol. CI intentionally not triggered because free quota and billing risk have not been independently confirmed. Preserve R073 and PESEN v0.1 frozen. Original239 v7.8 and the 154-item evidence queue remain unchanged.
