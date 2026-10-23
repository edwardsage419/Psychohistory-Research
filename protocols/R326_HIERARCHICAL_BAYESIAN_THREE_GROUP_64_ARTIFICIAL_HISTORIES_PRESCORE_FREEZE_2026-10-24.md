# R326 prescore freeze: exact finite hierarchical Bayesian cross-group learning

Date 2026-10-24. Original239 **02-007 Hierarchical Bayesian Learning**, P2. Frozen before source generation, exact results, or scoring.

## English source and existing R reuse
Tenenbaum, Kemp, Griffiths & Goodman (2011), *How to Grow a Mind: Statistics, Structure, and Abstraction*, Science 331:1279-1285, DOI 10.1126/science.1192788, reviews probabilistic inference over hierarchies. Perfors, Tenenbaum, Griffiths & Xu (2011), *A Tutorial Introduction to Bayesian Models of Cognitive Development*, Cognition 120:302-321, DOI 10.1016/j.cognition.2010.11.015.
Existing R112 Beta-Bernoulli learning and R179 posterior arithmetic are reusable only for single-group Bayes mechanics; R301 changepoint inference concerns a different latent structure. No verified primary hierarchical cross-group learning R in original239 v4.3. Historical early ZIP content scan remains open.

## Frozen finite generative model
One global latent regime Z in {L,H}, prior P(Z=H)=1/2. Three groups g=1,2,3. Conditional on Z, independent group-specific binary theta_g in {1/4,3/4}. Conditional P(theta_g=3/4|Z=H)=3/4; conditional P(theta_g=3/4|Z=L)=1/4. Given theta_g, group g has two conditionally iid Bernoulli observations. Enumerate all 2^6=64 ordered artificial histories, lexicographic order. Compute exact posterior P(Z=H|six bits), and three posterior predictive success probabilities for each group using all groups' observations. Comparator is three separate group posteriors with marginal P(theta_g=3/4)=1/2 and no cross-group pooling. All calculations exact rational Fraction. Each source history gets enumeration weight 1/64, which is NOT a generative likelihood.

## Falsifiable predictions
P1: For group1 fixed observations (0,1), group2 and group3 both (1,1) versus both (0,0) must yield different hierarchical predictive success for group1, higher in all-success other groups. Independent group1 prediction is 1/2 in both.
P2: Under any group permutation, global posterior Z remains equal and the three hierarchical predictive probabilities permute accordingly.
P3: Under complementing all six bits, P(Z=H) transforms to 1-P(Z=H) and all three hierarchical and independent predictions transform to 1-prediction.
P4: Every history has positive evidence likelihood, posterior and predictive probabilities strictly between 0 and 1, and exactly 64 unique histories.
P5: An independent auditor must recompute all 64 histories by enumerating 2 global regimes x 2^3 group theta assignments, without importing the generator. It must compare exact CSV source and JSON results and reject mutation.
P6: CI Python 3.11 and 3.12 unit tests plus an independent no-import audit job must pass before bounded E1 acceptance.

## Evidence scope
The exact two-level finite mixture is project-defined, not a replication of any author's cognitive participant data or their full representation-learning model. This is artificial mathematical E1 only. No evidence of actual human hierarchical learning E2, historical E3, fitted population priors or external prediction. R073/PESEN v0.1 remain frozen. Finish R-series before classification and fusion; personal decision system deferred.
