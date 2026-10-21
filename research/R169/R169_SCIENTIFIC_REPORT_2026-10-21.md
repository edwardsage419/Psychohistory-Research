# R169 scientific report | exact labeled adaptive culture-network dynamics

Date 2026-10-21. Original catalog **P2 / 07-011 Coevolving Networks**. Research acceptance **CLOSED_BOUNDED_E1**, restricted to an original four-node project-defined graph/opinion stochastic process. No observed human opinions or network ties, no original author implementation replay, no empirical causal identification and no phase-transition verification.

## Source inspection and scope

* Holme and Newman (2006), *Nonequilibrium phase transition in the coevolution of networks and opinions*, *Physical Review E* 74, 056108, DOI [10.1103/PhysRevE.74.056108](https://doi.org/10.1103/PhysRevE.74.056108). The [American Physical Society original abstract](https://journals.aps.org/pre/abstract/10.1103/PhysRevE.74.056108) and [author arXiv paper](https://arxiv.org/abs/physics/0603023) were consulted. Their original model couples acquaintance rewiring with neighbor-mediated opinion updating. Their node-oriented event clock is not identical to R169's discordant-edge clock; do **not** claim exact reproduction or reproduce their reported large-network continuous transition.
* Vázquez, Eguíluz and San Miguel (2008), *Generic Absorbing Transition in Coevolution Dynamics*, *Physical Review Letters* 100, 108702, DOI [10.1103/PhysRevLett.100.108702](https://doi.org/10.1103/PhysRevLett.100.108702), [original APS abstract](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.100.108702) and [author preprint](https://arxiv.org/abs/0710.4910). Models rewiring an active discordant link versus copying its neighboring node. Its mean-field critical expression p_c=(mu−2)/(mu−1) assumes a different asymptotic approximation, which the four-node R169 calculations **do not establish or test**.
* Gross and Blasius (2008), *Adaptive coevolutionary networks: a review*, *Journal of the Royal Society Interface* 5:259–271, DOI [10.1098/rsif.2007.1229](https://doi.org/10.1098/rsif.2007.1229), [open author/publication record](https://pmc.ncbi.nlm.nih.gov/articles/PMC2405905/). This provides background on jointly changing network structure and local states, not validation of our specific finite model.

All 72 artificial worlds use only four **labeled, entirely fictional nodes** (0,1,2,3), binary abstract state 0/1, and simple undirected graphs. There is no measurement of polarization, social identity, friendship, belief, transmission success, social welfare, group selection, or genuine time-series history. The graph labels are not persons in the real world.

## Pre-scored 72 complete factorial worlds and precise event clock

[Prescoring protocol](../../protocols/R169_FINITE_ADAPTIVE_NETWORK_72_LABELED_GRAPH_WORLDS_PRESCORE_FREEZE_2026-10-21.md) was committed **before any model or test source** at [e991aec](https://github.com/edwardsage419/Psychohistory-Research/commit/e991aecee0def3adb051d9e4f9590a9a74ad545c).

Four graph templates: four-node path with three links, three-leaf star with three links, four-cycle with four links, and four-link triangle-plus-tail. Three independent initial binary-node-state patterns: block (0,0,1,1), alternate (0,1,0,1), singleton (0,0,0,1). Three rewiring probabilities alpha∈{0,1/2,1}. Two target policies: 'same' only eligible same-state nonneighbors; 'any' any eligible nonneighbors. **4×3×3×2=72 worlds**, each storing the **complete joint distribution over labeled adjacency matrix and all four node states** for t=0,1,2,3.

At each step, if no discordant edge exists, the graph-opinion configuration is absorbing. Otherwise choose one discordant undirected edge uniformly and one endpoint as oriented anchor uniformly. With probability 1−alpha, anchor copies the other endpoint's node-state and the graph does not change. With probability alpha, anchor tries to drop that edge and connect to a uniformly sampled eligible nonneighbor other than the old neighbor. In 'same' mode the new target must have the anchor's current opinion. If **no eligible target exists the entire attempted rewiring is a true no-op**; the probability mass is not reassigned to adoption or redistributed to an available edge. Successful rewiring preserves total graph edges, with no self-loops or multiedges.

This **project-specific active-link clock and target-policy/no-op convention** is essential to interpreting the numbers. It is not a claim that any original paper used identical rules.

## Independent full-state Fraction verification

Oracle A directly enumerates active undirected edges and oriented anchors, combines exact adoption and rewire branches with target probabilities, and propagates the full labeled state probability distribution for three generations.

Oracle B independently enumerates the complete oriented discordant-edge event space, recomputes eligible targets from the original graph and node states without calling Oracle A's helper functions, independently constructs graph-state successor sets, and separately propagates their probability masses. Both use exact Python Fraction, no float approximations, third-party packages or stochastic RNG.

All **72×4 complete joint distributions match exactly**, including zero-eligible-target no-op paths. Every distribution sums to precisely one, all state probabilities are nonnegative, and edge counts remain invariant for all sampled paths. The [full 1,512,645-byte JSON archive](R169_EXACT_RESULTS.json) contains every graph edge list, node-state vector and exact rational probability. It also stores expected discordant links, A-node counts and connected components by time. The [compressed code/tests/results ZIP](R169_Adaptive_Network_72_Worlds_111_Tests.zip) preserves the entire original data and reusable algorithms.

## Frozen controls and independent two-time-state result

1. **alpha=0**: network edges never change; node states may update. Rewiring target policy is completely observationally irrelevant, as confirmed by equality of whole four-snapshot paths.
2. **alpha=1**: node states never change; network links may rewire. A-count is invariant, so an opinion proportion alone cannot reveal network evolution.
3. **No active disagreement or no eligible target**: absorbing/no-op branch behavior explicitly tested, including a complete six-link graph where all rewiring attempts fail and must remain no-ops.
4. For successful 'same'-opinion rewiring, exactly one discordant edge disappears and an agreeing link takes its place; no-op branches retain discordance. Under alpha=1 the whole path cannot increase discordant link count. With 'any' targets a discordant link can be replaced with another discordant link, preserving disagreement while changing topology.
5. For all 12 (four graphs × three starting opinion patterns) when alpha=1, the **complete path distribution under 'same' differs from 'any'**. This is an exact finite-model distinction independent of real data.
6. **Aggregate-measure non-identification counterexample**: start at four-node *path* edges {(0,1),(1,2),(2,3)}, opinions (0,0,1,1), and alpha=1. After two steps, the entire labeled state distributions under 'same' versus 'any' have exact total variation distance
\[
TV_2(P_{same},P_{any})=\tfrac12\sum_s|P_{same}(s)-P_{any}(s)|=\frac12.
\]
Yet the **expected discordant-edge count is exactly 1 under both modes** at the same t=2. Thus one common network statistic does not identify the actual distribution of labeled graph configurations, let alone the learning/reconnection mechanism. This numerical witness was separately computed by the final publisher CI job after the original 72-case source was frozen.
7. The expected count of connected components, edge discordance and node-state distribution are separate quantities. Neither a high aggregate agreement rate nor fragmentation alone can justify psychological, historical or causal social-polarization conclusions.

R169 adds an explicit evolving adjacency structure relative to R166's all-to-all cultural copying and R167's aggregate two-group weights. These are mathematical alternatives, not empirical model comparison wins.

## Real GitHub Actions verification and immutable source archive

The original [Python implementation](r169_adaptive_network_exact.py), [111 genuinely different unittest methods](test_r169_adaptive_network_exact.py), 72 individually named worlds and 39 graph invariant/absorbing/method identification/invalid-input/JSON controls, plus archived result JSON and ZIP have been independently audited.

* [First GitHub Actions run39540425684](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39540425684) **success** in Python3.11 and Python3.12: each executed 111 genuine methods, both generated identical original source/test/JSON/ZIP hashes.
* [SHA256-locked archive run39540516277](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39540516277) **success**: each of Python3.11 and 3.12 reran 111, independently validated all four fixed SHA256. The third archival job119026989146 reran 111, rebuilt the JSON and deterministic ZIP, validated all four hashes, computed the two-step TV=1/2 counterexample, and permanently committed the original full JSON and ZIP on main at [archive commit c27bb03](https://github.com/edwardsage419/Psychohistory-Research/commit/c27bb0329bbfa8daecf142846719086840287e0c).
* This totals **555 actual unittest executions over five runs of 111 different test methods, zero failures**. Repeated execution is reproducibility, *not* five independent human datasets.

Four fixed SHA256:
* source: `6f60b15ebbde33502ec660f4c7602960368eb6bbd8243d94483d7243f4005a3a`
* tests: `2f40e938e9b90c2099f7545707ae205c7ff130477d4e7d9d769b8c2f2368ba74`
* exact full JSON: `171c529917d8cdd3443b13883681cf4b020522f6ba0a807d1cb685c70cfd31e1`
* [ZIP](R169_Adaptive_Network_72_Worlds_111_Tests.zip): `64b02b3ccd90f31548fde255ca2e9da14fa2d949fb92b0b7e73d0dbd7119a518`.

Reproduce under `research/R169`: `python r169_adaptive_network_exact.py > R169_EXACT_RESULTS.json`, then `python -m unittest -q test_r169_adaptive_network_exact.py`, using Python standard library only. Source and stored artifact files are byte-identity pinned in CI.

**Formal acceptance: CLOSED_BOUNDED_E1** for the fixed finite state graph/opinion process and original-publication concept audit. New E2 independently validated human network predictions =0; E3 external historical event forecasts=0. R073 and PESEN v0.1 remain frozen. Next verified original catalog entry **R170 P2/07-012 Language Evolution Models**. Complete all R-series before classification, then model fusion.
