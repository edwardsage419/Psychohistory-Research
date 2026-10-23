# R304 Scientific Report — Social identity, minimal-group allocation, efficiency and label-swap controls

2026-10-23 Asia/Taipei. Original 239 item **03-003 Social Identity Theory**, priority P1. Final scientific scope **CLOSED_BOUNDED_E1_ARTIFICIAL_R304_MINIMAL_GROUP_ALLOCATION** only. Real human or animal E2 newly added 0; historical E3 0.

## Verified original 1971 experiment versus project toy formalization

Tajfel, H., Billig, M. G., Bundy, R. P. & Flament, C. (1971), *Social categorization and intergroup behaviour*, *European Journal of Social Psychology*, 1:149–178, https://doi.org/10.1002/ejsp.2420010202 (original publisher abstract). Original authors studied human minimal-group allocation choices in situations designed to avoid actor's direct individual material gain or pre-existing hostility. Publisher reports favoritism, own-group gain and relative-group difference, including cases of maximizing group differentiation at the expense of other advantages. Tajfel & Turner (1979), *An Integrative Theory of Intergroup Conflict*, extends the social identity analysis. The next original catalogue **03-004 Self Categorization Theory** is a separate independent model to study, and R304 is not its scientific acceptance.

**R304 does not obtain or reconstruct Tajfel1971 raw participant choices**, original randomization, actual assignment mechanisms, statistical tests, effect size or the authors' quantitative allocator payoff matrices. The score equation and finite parameters below were newly invented by this project's authors for mechanistic exploration. R303 Bandura1965 imitation and R063 Najar2020 social pseudo-reward imitation do not implement these allocation-choice utilities and are not recycled as Social Identity E2.

## Prescore-frozen synthetic allocation micro-world

[Protocol freeze](../../protocols/R304_SOCIAL_IDENTITY_MINIMAL_GROUP_ALLOCATION_432_SOURCE_FREEZE_2026-10-23.md) committed [60f6406c](https://github.com/edwardsage419/Psychohistory-Research/commit/60f6406cede7eb5bb7cea9dc622835d8fe3f4c41) **before any R304 model code or generated results**.

The artificial allocator earns **zero self reward in every choice**; all point outcomes go to distinct synthetic recipients A and B. Frozen grid: identity salience s∈{0,1/2,1}, intergroup differentiation preference d∈{0,1/2,1}, inequality aversion e∈{0,1/2,1}; identify A or B recipient as ingroup. Choices always contain BASE=(8,8), plus exactly one alternative in four menus:
* EQUAL_TOTAL_A_FAVORED=(10,6)
* EQUAL_TOTAL_B_FAVORED=(6,10)
* LOWER_TOTAL_A_FAVORED=(9,3)
* LOWER_TOTAL_B_FAVORED=(3,9).

**Invented, not author-fitted** decision score U=T+s·d·(ingroup_points−outgroup_points)−e·|ingroup_points−outgroup_points|. BASE score16. The alternative scores 16±4s·d−4e for equal-total menus and 12±6s·d−6e for lower-total menus, with sign + only if chosen ingroup is the favored recipient. Strict option score improvement required to choose alternative; all exact ties choose BASE.

There are **3³×2×4=216 entirely artificial allocation worlds**, each with **two fully labeled originally generated option rows**, **432 complete synthetic source rows**. No real participants, observed choices or real group membership. Every original CSV row contains all preference factors, label, option allocations, total, relative ingroup difference, inequality, identity score, inequality penalty, total score, chosen option, and total points forgone.

## Frozen exact results: categorical bias, label reversal and equity/efficiency trade-offs

At s=d=1,e=0 and A_INGROUP, A-favoring equal-total alternate(10,6) has score20 versus baseline(8,8)=16, so the toy chooses alternate; relabel B_INGROUP on the identical raw allocations changes alternate score12 versus baseline16 and choice reverses to BASE. At s=d=e=1, favoring alternate score16 ties baseline, so BASE is chosen. If s=0 or d=0, no menu ever leads to an asymmetric choice (equal-total ties under e=0, otherwise baseline score strictly higher); group-label switch cannot affect any scores. These are controlled mathematical comparators that **do not show categorization caused real people to discriminate**.

At s=d=1,e=0 with A ingroup, the alternative(9,3) yields lower **total reward12 versus16** but model utility18 versus baseline16. Thus the synthetic agent sacrifices four aggregate points for the assumed group gap weight. Actual Tajfel1971 paper motivates studying relative differentiation, but this particular U=... and every number s,d,e are our own imposed utility function, **not measured social identity effect sizes**.

Of 216 predetermined artificial worlds, 12 choose ALTERNATIVE: 10 are equal-total favored-group cases, two are lower-total favored-group cases; 204 choose BASE. These are **counts over the artificial grid**, not percentages of biased persons or general empirical estimates. Identity salience0 and differentiation weight0 always prevent alternative choice in this prescribed menu list. No real randomized identity intervention, individual preferences, societal norm change, group membership duration, historical predictions or out-of-sample validation is present.

## Independent verification and archival proof

[Exact project allocation model and 1,310 true unittests](r304_exact_social_identity_allocation.py); [complete 432 original synthetic source rows](R304_ALL_432_ORIGINAL_MINIMAL_GROUP_ALLOCATION_OPTIONS.csv); [216-world decision+both source option result JSON](R304_EXACT_SOCIAL_IDENTITY_ALLOCATION_RESULTS.json); [original CSV/JSON SHA256 receipt](R304_MACHINE_RECEIPT.json); [independent no-import direct-score-delta audit and 17 adversarial tests](../catalogue_audit/independent_r304_source_audit.py).

[GitHub Actions scientific run39934709217](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39934709217) observed **3 jobs completed/success**: Python3.11 and3.12 each executed1310 actual model tests plus17 independent original-source/tamper tests, third job reconstructed all432 original source allocations, all216 world decisions, negative controls and SHA256 before committing original CSV/JSON and receipt permanently to main [commit52e09ce5](https://github.com/edwardsage419/Psychohistory-Research/commit/52e09ce525958221447cb88c76996ea570e7f505).

Formal E1 success **does not establish Tajfel's original human effect size or generality**. R303 03-001 Social Learning Theory remains separately scoped; R305 candidate03-004 Self Categorization Theory needs its own experiment/protocol and cannot be promoted via overlapping social terminology. R073 and PESEN v0.1 stay frozen; full R-series research before cross-model taxonomy and fusion.
