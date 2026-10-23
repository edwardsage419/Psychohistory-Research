# R321 prescore freeze: finite Bernoulli sequential likelihood ratio stopping

Date: 2026-10-24. Original239 01-010 Sequential Sampling Models (P2). **PRESCORE ONLY**. This protocol must be committed to main before any R321 generated source, test outcomes or report.

## Sources and reuse boundary

Wald (1945), *Sequential Tests of Statistical Hypotheses*, Annals of Mathematical Statistics 16(2), 117–186, DOI 10.1214/aoms/1177731118. Ratcliff (1978), *A theory of memory retrieval*, Psychological Review 85(2), 59–108. For modern family scope see Forstmann, Ratcliff & Wagenmakers (2016), *Sequential Sampling Models in Cognitive Neuroscience*, Annual Review of Psychology 67:641–666, DOI 10.1146/annurev-psych-122414-033645. The original Sequential Sampling Models catalogue entry is a broad family, not a single uniquely identifiable original mathematical model.

R320 has already verified a two-boundary discrete absorbing random walk over 384 artificial paths. Its first-hit combinatorics can be **reused only as a mathematical submechanism**. R320 did not specify rival Bernoulli likelihoods, likelihood-ratio stopping, type-I/type-II errors or fixed-sample comparison. R289 sequential offers is a satisficing rule, not a likelihood-ratio test. Repository code search for SPRT, Wald and sequential probability ratio returned no itemwise matching source; historical ZIP audit remains incomplete. This R321 study adds a separate finite **Wald-inspired SPRT E1** with explicitly defined hypothesis testing semantics; it does not validate the general family or any human RT model.

## Frozen finite universe

Two pairs of simple Bernoulli hypotheses: (p0,p1)=(1/4,3/4) and (1/3,2/3). For each pair, log-likelihood-ratio step has base c=p1/p0=(1-p0)/(1-p1), so the integer score S_t=2*ones-t represents LR=c^S_t. Threshold K in {2,3}; stop at the first t <=7 with S_t>=K (accept H1) or S_t<=-K (accept H0). Otherwise right-censor at T=7, **without assigning a forced decision**. This is a finite-horizon truncation of an ideal sequential test, and LR thresholds c^K are exact fixed choices, not Wald's approximate alpha/beta boundary prescriptions.

For each (pair,K,true hypothesis H0/H1), enumerate every binary exogenous 7-bit string in lexicographic order, with exact Bernoulli mass p_true^ones*(1-p_true)^zeros. The full sample is 2 pairs * 2 K * 2 truths * 128 paths = **8 worlds, 1024 original artificial source rows**. Suffix bits after stopping are mathematical labels only. Source CSV fields: world_id,p0,p1,K,true_hypothesis,p_true,path_bits,ones,full_path_probability,stop_time,decision,censored. Result JSON stores per-world P(accept H0), P(accept H1), P(censor), E[min(tau,7)], all t-by-decision first-stop probabilities, and fixed-seven majority comparator P(choose H1) with threshold ones>=4. All fractions exact, no random seeds.

## Prespecified falsification gates

1. All 1024 rows unique by (world_id,path_bits), 128 per world, exact probability mass 1 per world. Stop time is the **first** threshold crossing, no post-stop behavior inferred. All outcome masses sum to 1.
2. Under the first pair, K=2, H1: P(accept H1)=873/1024, P(accept H0)=97/1024, P(censor)=27/512, E[min(tau,7)]=1579/512. Under H0 swap the two decision masses, with identical censoring and expected truncated samples.
3. Under first pair K=3 H1: P(accept H1)=12987/16384, P(accept H0)=481/16384, P(censor)=729/4096, E[min(tau,7)]=609/128. For both pairs and either truth, K=3 yields strictly higher censor probability and expected truncated sample count than K=2.
4. For each pair and K, H0/H1 complement symmetry swaps H0/H1 decision masses and preserves censor and truncated expected sample count. The fixed-seven comparator must equal independent binomial summation.
5. Independent audit must read source CSV **without importing generator**, recompute every row's mass/decision and all world aggregates via a separate state-mass dynamic program that only propagates still-active score states. Corrupt mass or first-hit row must fail. At least 25 stdlib unit tests, Python 3.11 and 3.12, independent CI audit job, Git blob receipt.
6. Report unconditional error mass, censoring, and conditional-on-decision error distinctly. No claim of infinite-horizon Wald optimality, achieved target alpha/beta, continuous-time diffusion, real participant E2, historical E3 or out-of-sample prediction. Index may add one **bounded E1 provenance primary link** only after all CI and source identity checks; do not call a broad model family validated.

## Acceptance and safeguards

Prescore commit SHA must precede every R321 outcome source commit. Formal gate: PASS_BOUNDED_E1_FINITE_WALD_INSPIRED_ONLY if all above checks and CI succeed, otherwise PENDING. R073 and PESEN v0.1 remain frozen. Complete all R studies before classification or fusion.
