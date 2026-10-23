# R293 prescore freeze: ten basic values, response style and centering identifiability

Date 2026-10-23 Asia/Taipei. Original 239 model id 01-016 (P1), Schwartz Basic Human Values. Precommitted before any R293 executable or scores. This is a **methodologically bounded synthetic E1 counterexample**, neither an original Schwartz 1992 empirical replication nor ESS human PVQ21 or SVS measurement validation. R013 recovered original ZIP is independently being scanned for historical overlap; do not equate an old paper card to replicated statistics.

## First-party sources and scope

Schwartz (1992), *Universals in the Content and Structure of Values: Theoretical Advances and Empirical Tests in 20 Countries*, AESP 25:1-65, DOI https://doi.org/10.1016/S0065-2601(08)60281-6. Schwartz (2012), *An Overview of the Schwartz Theory of Basic Values*, https://doi.org/10.9707/2307-0919.1116. Schwartz (2021), *Repository of Schwartz Value Scales with Instructions and an Introduction*, https://scholarworks.gvsu.edu/orpc/vol2/iss2/9/ . GESIS English ESS Human Values Scale guide https://zis.gesis.org/s/skala/Schwartz-Breyer-Danner-Human-Values-Scale-%28ESS%29?lang=en recommends centering for individual priority comparisons but cautions regarding choosing raw uncentered values for some structural measurement analyses. R293 quantifies the elementary algebraic implication; its source values are **not real PVQ21 questionnaire answers**, and numerical artificial covariances cannot validate the ten actual motivational value types or quasi-circumplex.

## Two DGPs and 2112 full original sources

Use ten **synthetic dimension slots** numbered i=0..9; theoretical circular labels retained for interpretive reference only, **not** fitted angles or validated measurement scales. Slot labels in fixed illustrative order: Self-Direction, Stimulation, Hedonism, Achievement, Power, Security, Conformity, Tradition, Benevolence, Universalism. Positions with index difference five are called illustrative opposite-slot pairs; there is no claim that each exact one-to-one correspondence reproduces the original Schwartz circular geometry.

* DGP INDEPENDENT: 10 independent, fair Bernoulli latent slot scores b_0 ... b_9, each in {0,1}. Exhaust all 2^10=1024 latent profiles.
* DGP OPPOSED_PAIRS: five independent fair Bernoulli latent scores b_0 ... b_4; slots i=0..4 get b_i and slots i+5 get 1-b_i. Exhaust all 2^5=32 latent profiles.
* Each latent profile crosses a shared respondent response-style shift S∈{0,2}, each with probability 1/2 and independent of all bits. Observed raw artificial slot score X_i=V_i+S, respondent-centered score C_i=X_i - (sum_j X_j)/10. The two shift levels are **fictional** and not a claimed 1-6 ESS survey coding. Every source row has exact joint mass 1/(2*2^10)=1/2048 or 1/(2*2^5)=1/64. Total 2048+64=2112 labeled original full ten-dimensional source rows.

Distinct row labels: DGP, latent profile bits, response style, 10 latent slot scores, 10 observed raw scores and 10 centered scores, common source weight. Full source probability per DGP integrates exactly 1. All moments use Fraction.

## Frozen exact analytic moments, counterexamples and negative controls

Calculate population means, variance, covariance and Pearson correlation across the complete weighted source distributions, separately for raw and centered slots.

For INDEPENDENT, for every i:
Var(X_i)=5/4; Cov(X_i,X_j)=1 for i≠j, giving raw correlation 4/5. Var(C_i)=9/40; Cov(C_i,C_j)=-1/40 for every i≠j, giving centered correlation **-1/9**. Latent independent V_i and V_j had covariance 0. Both raw +4/5 and centered -1/9 are induced here by the common response-style factor and by subtracting the individual's average, respectively.

For OPPOSED_PAIRS, Var(X_i)=5/4; Cov(X_i,X_{i+5})=3/4 and raw correlation 3/5. The centered covariance of each opposite slot pair is -1/4 (correlation -1); covariance between nonpaired centered distinct slots is 0. Sum_i C_i=0 for every source; a shared additive shift is unrecoverable from the centered profile. For each i,j, X_i-X_j = C_i-C_j = V_i-V_j, demonstrating precisely what respondent mean subtraction retains.

* REQUIRED: all 2112 rows generated and fully hashed, each world probability mass exactly 1; numerically identical exact moments produced by two routes: source summation and independent closed-form constants.
* REQUIRED: all 10x10 covariance matrices raw and centered (for each world), exactly represented in JSON and checked by third-party code which never imports production module.
* REQUIRED: raw/centered correlations and the independent latent control; opposition patterns in artificial OPPOSED_PAIRS are source assumptions and cannot be evidence for Schwarz original 1992 empirical universal circle.
* REQUIRED: no original 239 catalogue change, no R013 reclassification from mere mention, E2/E3=0.
* REQUIRED: tamper detection of CSV row, source weight, latent vector, incorrect centering, moment output; SHA256 archival.

## Acceptance

Ship Python >=3.11 standalone --test and --emit, full 2112-row CSV, exact JSON result including 10x10 moments, SHA256 receipt, independently implemented CSV audit, scientific report explicitly reviewing R013 scan and source/manual boundaries, formal machine acceptance only on observed successful GitHub Actions Python3.11+3.12 unit suites plus independent third job, and 239 row crosswalk v0.7 changing only 01-016 from v0.6 after the true E1 acceptance. Keep correct next P1 gap 01-018, no claims of E2, real PVQ sample, historical E3, or final original catalogue scientific completion. User research sequencing: complete R-series first, then categorize, finally model fusion. R073 and PESEN v0.1 remain frozen.
