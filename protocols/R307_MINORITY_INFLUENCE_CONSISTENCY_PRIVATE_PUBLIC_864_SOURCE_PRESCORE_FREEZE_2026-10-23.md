# R307 prescore freeze: minority consistency/credibility evidence and public normative suppression in bounded Bayesian toy

2026-10-23 Asia/Taipei. Original-239 **03-016 Minority Influence Models**, P1. FROZEN BEFORE MODEL SOURCE, GENERATED DATA OR RESULTS. Bounded original-to-project **E1 synthetic mathematical demonstration**. No 1969 child/student human perceptual response replication, no reproduction of 1994 meta-analytic effect sizes, no new E2 or E3. R073 and PESEN v0.1 frozen; complete R series before taxonomy/model fusion.

## Scientific original papers and carefully limited theory attribution

Moscovici, S., Lage, E. & Naffrechoux, M. (1969), *Influence of a consistent minority on the responses of a majority in a color perception task*, *Sociometry* 32(4):365–380, DOI https://doi.org/10.2307/2786541, [PubMed original bibliography](https://pubmed.ncbi.nlm.nih.gov/5373094/). Original experimental blue/green minority disagreement study investigates consistent versus inconsistent minority behavioral styles with real participants; our toy does **not** reproduce any actual observers, slides or conditions.

Wood, W., Lundgren, S., Ouellette, J. A., Busceme, S. & Blackstone, T. (1994), *Minority influence: a meta-analytic review of social influence processes*, *Psychological Bulletin* 115(3):323–345, DOI https://doi.org/10.1037/0033-2909.115.3.323; [original-author-hosted 1994 manuscript](https://dornsife.usc.edu/wendy-wood/wp-content/uploads/sites/183/2023/10/Wood.Lundgren.Ouellette.Busceme.Blackstone.1994_Minority_influence_a_meta-analytics.pdf), [PubMed PMID8016284](https://pubmed.ncbi.nlm.nih.gov/8016284/). Meta-analysis of 97 real experiments reports influence relatively stronger in private and indirect vs public/direct outcomes, and association with consistent minority source style. This paper does NOT provide fit/calibration for the numerical evidence/suppression coefficients below.

Prior R115 Informational Social Influence studied Bayesian action cascades and R116 Normative Social Influence studied public/private pressure; **R307 is distinct a minority-versus-majority source analysis** in which source behavioral consistency/credibility gates create a Bayesian *hypothetical* information increment and group numerical majority suppresses its public expression. Prior R303 observational learning, R304 identity allocation, R305 categorization, R306 polarization are separate. These separate conceptual overlaps do not constitute independent empirical replication.

## Exact finite artificial source universe

Six abstract agents in every artificial group, minority size m∈{1,2}, majority size 6−m. No genuine people. Two prior minority-proposal endorsement probabilities p0∈{1/4,1/2}. Hypothetical evidence exposure horizon t∈{0,1,2,3} (at t=0 no minority information). Minority advocacy behavioral-consistency gate c∈{0,1/2,1}; independent perceived credibility gate k∈{0,1/2,1}; public normative pressure n∈{0,1/2,1}. Two **distinct observation channels** PRIVATE_BELIEF and PUBLIC_EXPRESSION. **2 prior×4 horizons×3 consistency×3 credibility×3 normative pressure×2 minority sizes=432 original synthetic worlds**, each with two channels, hence **864 complete labeled original artificial source rows**. Every row records all inputs, each of six actors' minority/majority membership counts (no IDs), t exposed hypothetical identical minority advocacy evidence, prior odds, frozen per-signal likelihood multiplier, successive posterior odds sequence and exact private/public probabilities, private and public increment vs prior, suppression gap and label.

## Newly INVENTED project math; not Moscovici/Wood original parameters

Let prior odds O0=p0/(1−p0). Each minority advocacy exposure supplies assumed **likelihood multiplier** L=1+c·k. This is a deliberately invented evidence likelihood ratio parameterization: under c=0 or k=0, evidence has LR1 (uninformative); under c=k=1, each exposure LR2. Freeze t repeated identical exposures; posterior odds O_t=O0*L^t and PRIVATE belief probability b_t=O_t/(1+O_t). This *does not model physical perceptual truth*, nor an identifiable source agreement process; it only shows possible Bayesian odds accumulation conditioned on invented L.

Public pressure suppression factor z=1−n*(6−m)/6. PUBLIC expression probability e_t=p0+z*(b_t−p0). As n increases or majority share increases, expressed incremental endorsement is reduced; **PRIVATE posterior b_t independent of n/m**, by assumption. Public expression is merely stipulated a probabilistic expression gate, not a real person's observed speech or hidden cognition. No stochastic sampling, simulation, identity inference or real majority behavioral data.

All Fraction exact. The main model uses odds powers and data export; independent audit uses a sequential normalized binary Bayes likelihood update at each exposure with hypothetical P(E|alternative)=L/(L+1), P(E|nonalternative)=1/(L+1); this normalizes evidence and gives Bayes factor L. Also independently verifies PUBLIC suppression and exact source bytes.

## Frozen comparisons and negative controls

- With p0=1/4, t=3,c=k=1: O0=1/3; L^3=8; O3=8/3 => PRIVATE b3=8/11, increment 21/44. m=2 (majority4), n=1 => z=1/3, PUBLIC=9/22 (private>public>prior). m=1 (majority5), n=1 => z=1/6, PUBLIC=29/88, smaller than with 2 minority sources at same evidence. **This minority-size dependence is deliberately only through public majority-pressure weight**, not evidential influence, to make the design's assumption explicit.
- Same first-world but n=0: PUBLIC=PRIVATE=8/11.
- p0=1/4,t=3,c=1/2,k=1 -> L3/2, posterior 9/17; c=1,k=1/2 produces SAME 9/17: **product-confounding/nonidentifiability**. The artificial model cannot distinguish perceived source credibility from consistency from observed p alone. Even observed private/public outcome cannot independently identify c and k.
- c=0 OR k=0 OR t=0: posterior/private and public remain p0 for all n/m, so false positive minority persuasion forbidden.
- At p0=1/2, c=k=1,t=3 posterior8/9, no human meaning.
- For every world PRIVATE>=PUBLIC>=prior; n=0 channels identical; at higher n PUBLIC cannot increase, at higher m PUBLIC cannot decrease for same p0,c,k,t,n. Every hypothetical result in [0,1].
- A strong minority effect on private modeled judgment **does not mean greater observed public compliance or vice versa**, and no observation in these sources supports causal conversion of real humans.

No calibration, sensitivity study with actual behavior, social network feedback, independence verification of 3 exposures in original paper, psychological or historical validity. Model is an explicit illustration linking source consistency to information strength and public conformity.

## Acceptance gates

Native exact executable model for Python3.11+3.12, exhaustive original 864 synthetic rows CSV, full 432-world private/public results JSON, SHA256 machine receipt. Source-level independent no-import sequential Bayesian audit, 17+ adversarial falsification tests for row duplication, swapped channels, source count, altered c/k, posterior, pressure, hash and scope. Real GitHub Actions 2 Python jobs + third independent archive job all completed/success and permanently archive originals in main. Report and machine E1 acceptance only after passing.

Then crosswalk v2.2 **only change original 03-016**: v2.1 195 primary→196 primary, 41 pending→40 (P1 14→13, P2 27 stays). 03-012 R306, 03-010 R072 source-level E2 blocker and R115/R116 original provenance all preserved. R073/PESEN v0.1 frozen; no taxonomy/fusion before all R.
