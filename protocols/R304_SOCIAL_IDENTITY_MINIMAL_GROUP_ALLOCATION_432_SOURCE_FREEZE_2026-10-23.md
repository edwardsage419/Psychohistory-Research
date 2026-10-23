# R304 prospective freeze — social identity, minimum category salience, relative differentiation and efficient allocation

2026-10-23 Asia/Taipei. Original239 item **03-003 Social Identity Theory** P1. This is a PROSPECTIVE protocol: commit before R304 source code/output. Status sought: **bounded artificial E1 only**. No original human participant files, no new E2/E3. R073 and PESEN v0.1 frozen; finish all R research before cross-model taxonomy, then only after that fusion.

## First-party original literature and itemwise separation

Tajfel, H., Billig, M. G., Bundy, R. P., and Flament, C. (1971), *Social categorization and intergroup behaviour*, *European Journal of Social Psychology* 1:149–178, DOI https://doi.org/10.1002/ejsp.2420010202, [original publisher metadata and abstract](https://onlinelibrary.wiley.com/doi/10.1002/ejsp.2420010202). The author's original minimal group experiments isolated categorical grouping without preexisting hostility or direct participant gain, distinguishing maximizing own group gain, maximizing aggregate gain and intergroup difference. Authors reported group favoritism and, in some original allocation choices, prioritization of positive relative group difference over other material advantages. This is a genuine historical **original human experiment**, but **R304 does not import or reconstruct a single original allocation row**. It neither reproduces that experiment nor estimates its effect sizes. Tajfel & Turner (1979), *An Integrative Theory of Intergroup Conflict*, motivates self-categorization/identity social dimensions but is distinct from the next original catalogue **03-004 Self Categorization Theory**; that candidate remains unlinked until independent research.

R303 Bandura1965 observational acquisition/performance is *not* an ingroup allocation utility theory; R063 Najar social pseudo-reward imitation also not. R304 creates **novel project toy algebra**, no attribution of its numerical coefficients, social identity salience probabilities or utility scores to Tajfel 1971 humans.

## Frozen decision environment: no actor personal reward

One synthetic allocator chooses an allocation for **two other recipients** A and B. The allocator receives zero personal reward in every menu, mirroring the original minimal-group design's intent to distinguish direct individual self-interest but NOT recreating its actual incentives. Group label L∈{A_INGROUP,B_INGROUP} identifies which recipient shares the allocator's assigned group; there is no actual social category, child/participant, hostility or measured identity.

Three separate project-created scalar preference controls:
* categorical salience s∈{0,1/2,1},
* relative ingroup differentiation weight d∈{0,1/2,1},
* independent inequality aversion e∈{0,1/2,1}.

For allocation x=(points_A,points_B), total T=x_A+x_B, inequality D=|x_A−x_B|, assigned group difference G=(x_A−x_B) if L=A_INGROUP else (x_B−x_A). Define **entirely invented exact project utility** U(x|s,d,e,L)=T+s*d*G−e*D. The group difference is about group recipients, never allocator's reward. Under no salient identity s=0 or no differentiation d=0, swapping group labels cannot change U or selected option; with e>0, identical-total inegalitarian allocations are dominated.

Four menus, each offers same BASE allocation (8,8) and one ALTERNATIVE:
* EQUAL_TOTAL_A_FAVORED (10,6), total16 same as base16, recipient A gains more;
* EQUAL_TOTAL_B_FAVORED (6,10), total16, recipient B gains more;
* LOWER_TOTAL_A_FAVORED (9,3), total12, recipient A favored at aggregate loss4;
* LOWER_TOTAL_B_FAVORED (3,9), total12, recipient B favored at aggregate loss4.
No causal manipulation or real choice is run. For exact ties always choose BASE and record tie. This conservative deterministic tie break prevents misleading tie-as-favoritism.

Full factorial 3 salience ×3 difference weight ×3 inequity ×2 labels ×4 menus = **216 entirely synthetic decision worlds**. Each world has precisely **two originally labeled option source rows** = **432 complete artificial source rows**. Every source row records three exact weights, L, menu, alternative identity, both allocations, in/out recipients, actor reward0, total points, group difference, inequality, group-identity term, penalty, exact utility, chosen option, whether chosen alternative maximizes total and whether lower total was knowingly selected. Number of worlds / rows is NOT a number of participants or observed decisions.

## Frozen complete comparisons and mathematical counterexamples

For any world BASE score16. Alternative score equals:
EQUAL_TOTAL favoring assigned ingroup: 16+4s*d−4e; favoring outgroup: 16−4s*d−4e.
LOWER_TOTAL favoring assigned ingroup: 12+6s*d−6e; favoring outgroup: 12−6s*d−6e.
ALTERNATIVE chosen iff score>16, otherwise BASE including tie.

Negative controls: s=0 or d=0 ⇒ never select asymmetric ALTERNATIVE for any of 4 menus; group-label swap cannot change any score. For s=1,d=1,e=0 and A_INGROUP, EQUAL_TOTAL_A_FAVORED chooses ALT with U=20 vs16, while EQUAL_TOTAL_B_FAVORED chooses BASE; reversing group label exchanges the results. At s=1,d=1,e=1, favorable equal-total ALT score16 ties, BASE retained. At s=1,d=1,e=0 and A_INGROUP, LOWER_TOTAL_A_FAVORED ALT U=18 vsBASE16 despite total points12 rather than16; this shows group difference can override efficiency *in this invented utility*, not that actual study participants did so for the same weights. At s=0,d=1,e=0, all group labels and menus choose BASE (for equal-total alternatives tie, for lower-total alternatives lose).

Exact expected **12 out of 216** toy worlds select the alternative: 10 equal-total worlds (5 favorable weight tuples per menu) and 2 lower-total worlds (only s=d=1,e=0 and matching group); the ratio is a count over a chosen finite synthetic grid, **not real discrimination rate**. Independent reviewer shall derive the exact score delta directly from allocation totals and group difference (without calling the primary model) and verify all 432 source rows, 216 menus, group-label swaps, no-salience control and all alternate counts. Must check full 239 source model identity unaffected before indexing.

## Final evidence gates

Main Python 3.11+3.12 source --test/--emit, fully labeled 432-option synthetic CSV, 216-world both-allocation JSON and SHA256 receipt, wholly separate no-import independent source audit with negative/perturbation tests. Three real completed/success GitHub Actions jobs (dual Python plus independent source archivist), original CSV/JSON/SHA permanently committed to main, scientific report and E1 machine acceptance. Only then original239 v1.8 provenance **one changed candidate 03-003**, primary191→192 pending45→44; original 03-004 Self Categorization remains separate pending. No real human E2, new animal E2 or historical E3; R073/PESEN v0.1 remain frozen.
