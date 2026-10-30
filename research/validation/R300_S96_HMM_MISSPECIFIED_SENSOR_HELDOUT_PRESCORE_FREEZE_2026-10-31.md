# R300 S96 prescore freeze: finite HMM forecast under transition and emission misspecification

UTC date: 2026-10-30. Status: FROZEN_BEFORE_S96_SCORING. Target key: (r,R300,S96-v1,misspecified transition and emission one-step Brier risk).

## Existing scope
Original R300 is CLOSED_BOUNDED_E1 for a two-state known-parameter HMM; original protocol ef56b01c3c2b5da98e433f9d2fefdd61fd9028c3, original sources and acceptance remain unchanged. Original Rabiner (1989), DOI 10.1109/5.18626. This extension examines misspecification of a known candidate model and does not fit parameters. No human E2, historical E3, Viterbi, Baum-Welch, or psychological latent identification. R073 and PESEN v0.1 remain frozen.

## Frozen complete artificial design
True worlds W: (stay, emission match) = (1/2,3/4) and (3/4,3/4), each with hidden H1 prior 1/2. Every length-four observed binary prefix y1..y4 is enumerated once per true world, 16 prefixes per world. For each true world, evaluate nine fixed candidate filters with assumed stay a in {1/4,1/2,3/4} and assumed emission match q in {1/2,3/4,1}. Each candidate has a positive prefix likelihood for every prefix. Source count = 2 true worlds * 16 prefixes * 9 candidate pairs = 288 distinct (world,prefix,a,q) records. The 288 records reuse the same 32 distinct true-world prefixes, so they are not independent samples.

## Frozen evaluation
True joint prefix probability w(y)=P_true(Y1:4=y). True conditional next observation probability p(y)=P_true(Y5=1|y). Candidate next prediction f_a,q(y) uses the candidate filter and candidate transition/emission parameters on the same observed prefix. Conditional Brier risk = p(y)*(1-f)^2 + (1-p(y))*f^2. Aggregate expected risk for a candidate = sum over all 16 prefixes w(y)*conditional Brier. Oracle uses the true a,q. Baseline always forecasts 1/2 and has expected Brier 1/4. Excess over oracle = sum w(y)*(f-p)^2. Compare all 18 true-world/candidate cells; record source-level w,p,f,risk and group expected risk, oracle, excess, baseline. Do not select candidate after seeing risk, do not treat this as learned parameter estimation or empirical holdout.

## Mandatory tests
All exact rational arithmetic, no float comparisons. Sum true prefix masses=1 per world; 288 unique keys and 18 complete groups; every candidate likelihood positive; oracle excess=0; all excess>=0; IID true world next p=1/2 for every prefix; candidate a=1/2 next prediction=1/2 for every prefix irrespective q; candidate q=1/2 next prediction=1/2 irrespective a; true persistent oracle risk <=1/4. Explicitly record misspecification penalty and negative controls. Independent B method must use full latent-path enumeration for true joint probabilities and independently calculate candidate predictions, then run deliberate source and summary mutations; B plan must be frozen before B outcomes.

## Files and acceptance
New files only in research/validation for R outputs, research/data_scout for A, research/evidence_audit for B; no modification of original R300, R073, PESEN, original239 v7.8 or pending154. Original R300 acceptance unchanged; S96 limited E1 internal review is PARTIAL pending external independent replication and empirical transfer. GitHub Actions must not run until zero cost verified. Failure evidence is retained. No fabricated CI or fee confirmation.
