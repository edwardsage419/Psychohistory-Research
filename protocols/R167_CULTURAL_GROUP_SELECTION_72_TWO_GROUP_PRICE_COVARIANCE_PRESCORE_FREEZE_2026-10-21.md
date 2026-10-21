# R167 prescore freeze: synthetic two-group cultural frequency dynamics and exact within-between decomposition

Date 2026-10-21. Original catalog **P2 / 07-009 Cultural Group Selection**, following formally closed R166 (main indexed at `0ef63032e9a7976e8d20e12da67ce397ec402cd3`). This file freezes all input conditions, formulas, tests and evidence boundaries **before code**.

## Sources and disputed/limited scope
Boyd & Richerson (2002), *Group beneficial norms can spread rapidly in a structured population*, *Journal of Theoretical Biology* 215(3):287–296, DOI [10.1006/jtbi.2001.2515](https://doi.org/10.1006/jtbi.2001.2515), original Elsevier abstract and PMID12054837 directly checked. This original models imitation in **structured populations**, with within-group and between-group consequences, and is much richer than two artificial group weights.
Joseph Henrich (2004), *Cultural group selection, coevolutionary processes and large-scale cooperation*, *Journal of Economic Behavior & Organization* 53(1):3–35, DOI [10.1016/S0167-2681(03)00094-5](https://doi.org/10.1016/S0167-2681%2803%2900094-5), original Elsevier abstract checked; the article argues that culturally generated behavioral equilibria and group structure can change the evolution of cooperative behavior, in a coevolutionary framework. Exact author models and human data not reconstructed. George R. Price (1970), *Selection and covariance*, *Nature* 227:520–521, DOI [10.1038/227520a0](https://doi.org/10.1038/227520a0), verified original Nature issue listing and PubMed bibliography; this project uses an elementary two-group covariance identity as **independent algebra check**, not a historical reproduction of Price's derivation or an empirical estimate. Do not claim that mathematical covariance terms prove actual group-level causal selection, adaptation, cooperation, group welfare or preference value.

## Frozen 72 three-transition worlds
Two entirely fictional unlabeled A/B culture groups indexed low/high (only refers to relative mathematical A frequency, no actual community).
Initial ordered A fractions:
P0=(1/4,3/4), P1=(1/3,2/3), P2=(1/5,4/5), P3=(1/2,1/2).
Initial weight of high group h∈{1/2,3/4}, weight of low group 1−h.
Artificial within-group A **disadvantage** delta ∈{-1/4,0,1/4}, under \(p'_g=p_g-\delta p_g(1-p_g)\). Negative delta favors A within each group, positive delta suppresses A within each group.
Artificial between-group reweighting coefficient kappa∈{0,1,2}, determined by *pre-within* A fraction in each group: \(R_g=1+\kappa p_g\), and \(w'_g=w_g R_g/\sum_i w_i R_i\).
Project next overall A frequency \(P'=\sum_g w'_g p'_g\), versus previous \(P=\sum_g w_gp_g\).
Exactly **4 pairs ×2 initial group weights ×3 delta ×3 kappa =72 worlds**, each with 4 complete snapshots t=0,1,2,3 (three within/between transitions) of group A fractions, group weights, and overall P. Save every one-step within, between and total change as exact Fraction.

## Two independent arithmetic identities, full paths
(1) Direct Fraction sequential within update and weighted group reproduction.
(2) Independently derive two-group covariance change:
\[
W=\sum_g w_g(p'_g-p_g),\quad
B=\frac{w_0w_1(R_1-R_0)(p'_1-p'_0)}
         {w_0R_0+w_1R_1},\quad
\Delta P=W+B.
\]
Compute B from covariance factorization **without** using direct new weights; separately verify P+W+B equals direct P'. For each next step also derive total overall P from normalized group masses independently, and assert exact equality. This is an exact mathematical identity for the frozen two-group process, not a statistical causal decomposition or a universal Price equation proof.

## Prespecified controls and important scientific boundaries
1. Simpson-style reversal: P0=(1/4,3/4), high initial group weight1/2, delta=+1/4 (A loses within both groups), kappa=2 (higher-A group grows faster). Within-group new fractions p'_0=13/64 and p'_1=45/64; previous P=1/2. Exact within contribution W=−3/64. Exact between contribution B=+1/16=+4/64. Hence next P=33/64 and total change +1/64, even though both groups decreased their own A fraction. **This is a synthetic aggregation reversal, not measured group selection in humans**.
2. When kappa=0, all group weights remain constant and B=0 (for every delta, all timepoints).
3. When delta=0, each individual group's p stays fixed; aggregate P can change due to group reweighting when kappa>0 and p0<p1.
4. For equal initial fractions P3=(1/2,1/2), changing kappa cannot change group weight (same R). All timepoints retain identical group p and hence B=0; within delta may still change p.
5. For delta=+1/4 and 0<p<1, local p strictly decreases. For delta=-1/4, p strictly increases. If kappa=0, aggregate change equals within contribution. Bounds p,w in [0,1], sum group weights exactly 1.
6. For kappa>0 and p_high>p_low, B>0 when resulting p_high'>p_low', assuming positive group weights; only with additional conditions is net overall change guaranteed positive. Larger group weights can mask within-group deterioration.
7. Group mean frequency alone hides within changes; macro frequency change cannot uniquely establish micro adaptation, migration or selection. No true human group welfare payoff measured, no migration, social network, institutional enforcement, conflict, demographics, genetic or historic selection evidence.
8. Reject invalid groups, missing or float parameters, negative/out-of-unit p and group weights, invalid horizon; preserve exactness.

## Formal closure gates
72 distinct named worlds plus ≥25 separate negative/identity tests, full source, result JSON and tests ZIP with four immutable SHA256, Python3.11/3.12 GitHub CI, independent archive publication on main, post-commit readback, author-source limitation report. Only E1 mathematically bounded status if all pass. No E2 human independent behavior prediction, E3 external historical prediction. R073 and PESEN v0.1 remain FROZEN. Next original catalog entry R168 to verify after closure. Finish all R studies first, then classification, then fusion.
