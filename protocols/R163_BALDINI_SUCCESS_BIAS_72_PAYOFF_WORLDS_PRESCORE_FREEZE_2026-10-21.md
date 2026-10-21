# R163 Prescore freeze | Compare Means versus Imitate the Best under artificial observed payoffs

Date 2026-10-21. Original catalog P1 / 07-005 Success Biased Transmission, verified `docs/MODEL_CANDIDATE_CATALOG_v0.1.json`. Prior main `fd920adad53de359127a3f60063ba5257e515092`, R162 formally CLOSED_BOUNDED_E1. Protocol created and committed *before* code and data.

## Primary literature and evidence boundary
Ryan Baldini (2013), *Two success-biased social learning strategies*, *Theoretical Population Biology* 86:43–49, DOI https://doi.org/10.1016/j.tpb.2013.03.005. Original publisher abstract and PubMed PMID23587700 examined; it distinguishes "Compare Means" (select trait with highest mean observed payoff) from "Imitate the Best" (copy single demonstrator with maximum payoff); both can perform worse than indiscriminate imitation in different environments. **Original article full equations, source code and stochastic evolutionary selection analysis have not been read or replayed.**
Ryan Baldini (2012), *Success-biased social learning: Cultural and evolutionary dynamics*, *Theoretical Population Biology* 82(3):222–228, DOI https://doi.org/10.1016/j.tpb.2012.06.005. Publisher original abstract directly checked; warns stochastic payoff-driven bias can be poor when optimal trait is already common.
Alex Mesoudi (2011), *An experimental comparison of human social learning strategies: payoff-biased social learning is adaptive but underused*, *Evolution and Human Behavior* 32(5):334–342, DOI https://doi.org/10.1016/j.evolhumbehav.2010.12.001, [author original published article PDF](https://www.alexmesoudi.com/publication/mesoudi-experimental-2011/Mesoudi_EHB_2011.pdf), publisher original abstract and source full text accessible; reports a mixed social/individual learning strategy in an experimental virtual-arrowhead task. **We have not obtained person-level choice/payoff original data, rerun the experiment, or replicated published regressions and counts.**
Kendal et al. (2018), *Social Learning Strategies: Bridge-Building between Fields*, *Trends in Cognitive Sciences* 22(7):651–665 DOI https://doi.org/10.1016/j.tics.2018.04.003, original publisher abstract reviewed, cautioning that strategies are flexibly combined and population patterns need not uniquely identify cognitive mechanisms.

All following rules are independent, project-authored **finite one-round toy arithmetic**, not exact original Baldini equations, no source empirical reanalysis, no actual human/technical competence measurements, no historical prediction; E1 only.

## Freeze exactly 72 payoff-table worlds
Three anonymous synthetic demonstrators with binary culturally neutral actions A=1 or B=0. Six prespecified observed 3-agent profiles:
- P0 ("A outlier"): actions (1,1,0), observed payoffs (12,0,8). Individual best A, group A mean6 < B mean8.
- P1 ("B outlier"): actions (1,0,0), observed payoffs (8,12,0). Individual best B, group A mean8 > B mean6.
- P2 ("A agreement"): actions (1,1,0), observed payoffs (10,9,2). Both strategies prefer A.
- P3 ("B agreement"): actions (1,0,0), observed payoffs (2,10,9). Both strategies prefer B.
- P4 ("best tie"): actions (1,0,0), observed payoffs (8,8,2). Imitate Best picks A with probability 1/2; Compare Means picks A with probability1.
- P5 ("mean tie"): actions (1,1,0), observed payoffs (8,0,4). Imitate Best picks A with probability1; Compare Means picks A with probability1/2.

Three artificial display transformations T: observed unchanged (raw), reverse displayed scores (12−original), or flatten all scores to 6. Two strategy definitions ("best","means"), two externally assigned objectively correct artificial actions c∈{0,1}. **6×3×2×2=72 distinct worlds**.
Random-copy baseline is unbiased uniform sampling of one of the three demonstrators: p0(A)=#A/3.

"Best": sample uniformly among demonstrators whose displayed score attains maximum (ties at person level). "Means": calculate mean displayed score *within each action*, choose the action with higher mean; equal means choose uniformly between available action types. Every profile contains both actions, so no ambiguous missing group. **Tie conventions are project definitions and must be recorded;** a means tie selects A with probability 1/2, even when #A=2, unlike unbiased demonstrator copying.
For an artificial c, expected correctness S=P(A) when c=1, otherwise 1−P(A). Advantage S−S0 is against baseline random demonstrator, not against original authors' experimental performance. No payoff reliability, random payoff-generating law, time-varying environment, adaptive utility or human cognitive fitting is assumed.

## Two independently coded exact Fraction oracle routes
Route 1: exact direct max/means ranking with normal integer/Fraction scores; tie set cardinality and exact rational output.
Route 2: independent enumerator for max indices, and **cross-product inequality** between total action-payoff sums times the opposing group count to compare group mean scores, independently enumerating the available cultural tokens for exact ties. Avoid calling direct ranking function; both must agree in all 72 worlds for copying probability, neutral baseline, synthetic success and advantage.

## Prespecified negative controls and identification
1. Raw P0 best p(A)=1, means p(A)=0. Raw P1 best p(A)=0, means p(A)=1. Same observations, two success strategies disagree.
2. Raw P4 best p(A)=1/2, means p(A)=1, proving individual tie treatment matters. Raw P5 best p(A)=1, means p(A)=1/2, proving group-mean tie treatment matters.
3. Flat signal P0 has best p(A)=2/3 and means p(A)=1/2, while neutral baseline p0(A)=2/3. Observed displayed payoff equality does not imply strategy equivalence because of tie conventions.
4. Same raw P0 best choice A=1: assigned correct c=1 gives model advantage +1/3 over baseline2/3; c=0 gives model advantage −1/3. Exact reversal when changing unobserved true correctness. Comparison of observed payoff rankings alone does not establish future variant success.
5. Transforming payoffs by a **strictly increasing affine map** does not change either strategy's ranking; reverse transform can change rankings. Flatten destroys relative payoff information. At no point infer that displayed success is a validated signal of actual quality.
6. Strategies are only one-round; no repeated-game histories, interaction, sequence selection or empirical independent forecasts. Identical resulting copying frequency cannot be used to infer true mental strategy without payoff signal variation and explicit tie conditions.

## Acceptance
At least 72 uniquely named world unittest methods plus 25 independent edge tests; archive complete deterministic original JSON and exact source/test ZIP. Verify two Python versions 3.11 and 3.12, independently report all four SHA256, lock by immutable hashes and publish JSON/ZIP permanently on main; check all original artifacts and science report. Scientific status CLOSED_BOUNDED_E1 only upon passing. New E2=0, E3=0. R073 and PESEN v0.1 remain frozen. Next original catalog R164 must be verified before setting priority.
