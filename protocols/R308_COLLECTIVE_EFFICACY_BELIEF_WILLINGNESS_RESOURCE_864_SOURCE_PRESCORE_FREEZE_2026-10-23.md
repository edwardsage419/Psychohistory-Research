# R308 pre-score freeze: perceived collective efficacy vs cohesion/willingness/resource-limited action, 864 original synthetic source rows

2026-10-23 Asia/Taipei. Original239 **03-018 Collective Efficacy**, P1. Freeze this complete finite grid & all mathematical comparisons **BEFORE** native source model and generated results. Grade **E1 new project-invented artificial construct-separation mechanism only**; no human/animal E2 or historical E3. R073 and PESEN v0.1 remain frozen; all R-series studies before taxonomy/fusion.

## Primary sources and construct-level boundaries

Bandura, A. (2000), *Exercise of Human Agency Through Collective Efficacy*, *Current Directions in Psychological Science* 9(3):75–78, https://doi.org/10.1111/1467-8721.00064, [author/publisher article](https://www.psychologicalscience.org/journals/current-directions/1467-8721.00064/). Bandura's perceived collective efficacy is group members' shared beliefs about capabilities for coordinated collective effects; it is NOT directly the same as externally proven ability/resources nor observed social action.

Sampson, R. J., Raudenbush, S. W. & Earls, F. (1997), *Neighborhoods and Violent Crime: A Multilevel Study of Collective Efficacy*, *Science* 277(5328):918–924, https://doi.org/10.1126/science.277.5328.918, [PubMed](https://pubmed.ncbi.nlm.nih.gov/9252316/). Study surveys **8,782 real residents in 343 Chicago neighborhoods**, measures social cohesion among neighbors and willingness to intervene for the common good as collective efficacy; reports adjusted negative *association* with violence. Study is NOT a universal randomized causal proof; this R study neither accesses actual respondent records nor reproduces multilevel model or crime outcome.

Goddard, R. D., Hoy, W. K. & Woolfolk Hoy, A. (2000), *Collective Teacher Efficacy: Its Meaning, Measure, and Impact on Student Achievement*, *American Educational Research Journal* 37(2):479–507, DOI https://doi.org/10.3102/00028312037002479, [publisher source](https://journals.sagepub.com/doi/10.3102/00028312037002479). School collective teacher efficacy measurement was studied and associated with school outcomes, but we do not recreate school questionnaires, schools or reading scores. Do not infer teacher causal effects.

Existing R303 imitation acquisition/expression, R304 social identity allocation, R305 self-categorization, R306 polarization, R307 minority public/private, R072 public reputation are **distinct**. Aggregate beliefs about joint action and willingness to intervene require independent mechanism checks.

## Pre-frozen eight artificial three-agent belief patterns and controls

Exactly eight **synthetic unordered patterns with a fixed presentation order**, each triple b1,b2,b3 represents fictional members' *beliefs* about their group's capability, not objective skills or outcomes:
- NONE (0,0,0)
- LOW_UNIFORM (1/2,1/2,1/2)
- HIGH_UNIFORM (1,1,1)
- ONE_STRONG_TWO_ZERO (1,0,0)
- ONE_WEAK_LINK (1,1,0)
- SAME_MEAN_NO_ZERO (1,1/2,1/2)
- HETEROGENEOUS (1,1/2,0)
- HALF_HALF_ZERO (1/2,1/2,0)

These are deliberately chosen **8 distinct toy patterns**, not an exhaustive sample of all 3^3 ordered triples, and cannot estimate a population distribution.

Two invented competing aggregation rules g∈{MEAN, BOTTLENECK_MIN}, measuring perceived shared efficacy B_mean=(b1+b2+b3)/3 or B_min=min(b1,b2,b3). Neither aggregator is supplied by Bandura or validated as a true latent scale. Three independent social gate controls cohesion c∈{0,1/2,1}, willingness to intervene w∈{0,1/2,1}, availability of material/action resources r∈{0,1/2,1}. Define Sampson-inspired **toy cohesion-willingness conjunction** C=c*w, but not his empirical survey estimator.

Define further an **explicitly invented** action-capacity propensity proxy A=B_g*C*r. This factorization is an illustrative logical bound: high shared belief cannot guarantee actionable intervention if willingness or resources are zero. The word 'proxy' must always accompany A; it is NOT observed intervention, criminal victimization probability, neighborhood violence or school performance. One binary reported source channel is PERCEIVED_COLLECTIVE_BELIEF (probability B_g), another is RESOURCE_GATED_ACTION_PROXY (probability A). Both represent artificial model expectations, not 2 people or 2 real treatments.

Universe: 8 belief triples ×2 aggregation rules ×3 cohesion ×3 willingness ×3 resource levels = **432 artificial worlds**, each with exactly2 channel rows = **864 fully labeled artificial source rows**. Each source contains all three member belief levels, mean, bottleneck, selected aggregator, cohesion/willingness/resource, capacity B, collective-action conjunction C, hypothetical proxy A, individual actor belief breakdown, each gate product and the selected channel response.

## Frozen comparisons and causal-identification negative controls

- HIGH_UNIFORM beliefs (1,1,1), g=MEAN or MIN, c=w=r=1 -> B=1,C=1,A=1; if w=0 even with c=r=1, **B remains1, A=0**, showing collective belief is not action; if r=0 then A=0 despite belief and willingness.
- Group ONE_WEAK_LINK=(1,1,0) versus SAME_MEAN_NO_ZERO=(1,1/2,1/2): **mean belief2/3 in both**, but bottleneck min is0 vs1/2. At c=w=r=1, MEAN aggregator yields proxy2/3 for both, BOTTLENECK_MIN yields0 vs1/2 respectively. This proves output depends on the *assumed aggregator* and individual heterogeneity despite same group mean.
- Zero cohesion or zero willingness: conjunction C=0, A=0 even if high B and r; zero resources: A=0 with no effect on B or C.
- If any c,w,r increased with fixed belief pattern and aggregator, A cannot decrease. If individual belief changes but pattern outside original8 is not one of this study's experimental sources; do not extrapolate monotonicity outside grid or to real people.
- For every world, 0≤A≤B≤1 and 0≤C≤1. The two reported channels should differ whenever C*r<1 and B>0.
- Because model assumes a multiplicative proxy, it does **not establish** true causal effects of survey cohesion, individual beliefs or resource scarcity. These dimensions could be correlated or jointly caused by external structural factors in actual neighborhoods. No original data for regression or causal identification.

## Independent audit and release rules

Must create native Python3.11/3.12 Fraction model --test/--emit, all 864 source CSV, complete 432-world full original source JSON, machine SHA256. Independent auditor imports NO primary model, reconstructs B by separate mean/min and proxy by **full enumeration of four artificial independent binary gates**: efficacy chance B, cohesion c, willingness w, resources r, product event "all gates 1"; cross-check every row/JSON, missing/duplicates/altered actor beliefs, false violence interpretation, SHA and required counterexamples.

Three actual GitHub Actions green jobs (dual interpreter+independent source archive), permanent complete original sources and SHA on main, formal scientific E1 report and machine acceptance; then original239 v2.3 crosswalk **changes only 03-018** (primary196→197, pending40→39, P1 13→12, P2 27 fixed). Original R307 03-016, R306 03-012, existing R072 03-010 codebook E2 blocker intact. All R series first, then taxonomy, finally original fusion.
