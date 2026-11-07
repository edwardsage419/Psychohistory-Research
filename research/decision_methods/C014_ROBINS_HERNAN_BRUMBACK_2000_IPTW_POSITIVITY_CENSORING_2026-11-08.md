# C014 Robins, Hernán与Brumback（2000）：动态干预权重、删失和正值性边界

track: theory
subflow: C
run_date: 2026-11-08 (Asia/Singapore)
target_key: (theory-C,Robins-Hernan-Brumback-2000,original-published,IPTW_longitudinal_positivity_censoring_and_personal_decision_identification)
observed_head: 707f898ae4cdbaea04502623d95a6181746ad050
status: PRIMARY_TEXT_BOUNDED; CONSTRUCTIVE_ARITHMETIC; NO_EMPIRICAL_CAUSAL_VALIDATION
source: James M. Robins, Miguel Ángel Hernán, Babette Brumback (2000), *Marginal Structural Models and Causal Inference in Epidemiology*, Epidemiology 11(5):550–560. DOI 10.1097/00001648-200009000-00011. Author/university-hosted original-layout PDF: https://www.stat.ubc.ca/~john/papers/RobinsEpi2000.pdf ; alternative institutional copy https://content.sph.harvard.edu/wwwhsph/sites/1268/2014/11/Marginal_Structural_Models_and_Causal_Inference_in.11.pdf .
reading_scope: Original published text pp.555–560, sections 7.1–12, Appendix 1 and Tables A1–A5, plus p.554 longitudinal equation (14). Text and formula transcription checked; full scan visual formula-by-formula verification remains NOT_RUN.

## 原著独立增量

1. p.555 equation (14): longitudinal stabilized treatment weight is the product across time of the observed treatment's conditional probability given past treatment divided by the corresponding probability given past treatment AND measured covariate history. For binary treatment, p.556 equations (15)–(17) explicitly use p^a(1-p)^(1-a) for each observed treatment, so untreated observations must use 1-p. The earlier single-treatment expression is insufficient for repeated decisions.
2. p.556 section 8: numerator and denominator treatment models are distinct. Under the stated causal and denominator model assumptions, numerator misspecification does not necessarily destroy consistency, although weight stability may change. This is a model-specific theoretical statement, not a finite-sample guarantee.
3. p.557 section 9: effect modification by PRE-treatment covariates may enter the MSM, whereas treating post-treatment covariates as effect modifiers in that specification is invalid; structural nested models are suggested for treatment interaction with time-varying covariates. The relevant estimand must be chosen before fitting.
4. pp.557–558 section 10: loss to follow-up requires inverse probability of censoring weights multiplied by treatment weights. Treating only observed outcomes as a random sample can induce selection bias. Both treatment and censoring mechanisms require identifying assumptions.
5. p.558 section 11: deterministic treatment within a measured covariate stratum violates positivity for the specified treatment comparison. For example, off-work employees cannot receive occupational exposure at work. No amount of repeated observation of the same support pattern identifies the counterfactual for an impossible treatment. One must revise the intervention/eligible population or use a different identifiable estimand. The paper discusses structural nested models as an alternative, but their suitability still depends on assumptions.
6. Appendix 1, pp.559–560 Tables A1–A5: published one-time treatment example has 500 observed persons. In L=1, treated 360 with 108 outcomes and untreated 40 with 24 outcomes; L=0, treated 50 with 20 outcomes and untreated 50 with 40 outcomes. L=1 share 400/500=.8 and L=0 share .2. Standardized treated risk .8*(108/360)+.2*(20/50)=.32; untreated risk .8*(24/40)+.2*(40/50)=.64. Risk difference -.32 and risk ratio .5. Crude risks 128/410 and 64/90 yield a different association. Weighting by 1/P(A|L) gives pseudo treated 160/500=.32, untreated 320/500=.64, reproducing the standardized comparison. These are calculations on the author's pedagogical table, not independent empirical replication.

## C候选可观测设计与证伪标准

Candidate longitudinal variables: time-stamped decision A_k, pre-decision state L_k, prior decisions, recorded intervention eligibility, outcome Y, loss-to-follow-up C_k, data-collection context and changes in measurement. Record no actual user's sensitive information. A future predeclared study would need to specify the intervention regimes and estimand, temporal ordering, treatment/censoring model, weight distribution and positivity by history, measurement error and sensitivity to unmeasured confounding. If any clinically/physically/institutionally possible action has zero conditional probability in a required history, the corresponding full-population comparison fails the proposed IPTW identification gate. Near-zero probabilities imply unstable weights and require reporting, not automatic causal claims.

Constructive counterexample: A_k=1 whenever L_k=1 and A_k=0 whenever L_k=0. Observed (A,L,Y) cannot reveal Y under A=0 for L=1, regardless of sample size. Two potential-outcome worlds can agree on all observed data and disagree on this missing counterfactual. This is logical nonidentification, not a measured effect.

Competition: g-computation and structural nested models target different modeling/identification strategies; randomized sequential interventions could reduce treatment-confounding assumptions but can still face adherence, censoring and interference. Measurement reactivity, latent state, self-selection and policy changes are alternative explanations. Original clinical cohort results and historical events were NOT analyzed.

Evidence limits: the source is a published methodological argument and illustrative table. Original empirical companion study (Hernán et al. 2000, pp.561–570) NOT_READ. Appendix 2 in this PDF beyond the inspected ranges NOT_VERIFIED. No individual experimental results, historical prediction, R-series evidence upgrade, personal utility weights, or product implementation.

Local arithmetic assertions verified in exact fractions conceptually: 108/360=3/10; 20/50=2/5; 24/40=3/5; 40/50=4/5; weighted risks 8/25 and 16/25; RD=-8/25; RR=1/2; pseudo outcome counts 160 and 320. Programmatic automated test NOT_RUN. GitHub Actions NOT_RUN; account billing NOT_VERIFIED. No paid operation requested. D003 2026-W45 completed 2026-11-02, read-only; R073/PESEN v0.1 frozen, R E1/E2/E3 and MARKET unchanged.

Next: check original p.555–558 equations against page images, then rotate to weak-covered historical/institutional sources; no repeated C014 identifier for minor details.
