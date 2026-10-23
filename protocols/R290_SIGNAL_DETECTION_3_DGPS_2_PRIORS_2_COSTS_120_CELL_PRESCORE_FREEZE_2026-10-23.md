# R290: Signal Detection Theory finite Bayes decision and ROC prescore freeze

Date: 2026-10-23 Asia/Taipei. Original 239 catalogue ID 01-011, P1. This is a prospective *artificial, exact mathematical* E1 learning study; it is neither an empirical replication of Tanner & Swets (1954) nor an E2 human or E3 historical test. R073 and PESEN v0.1 stay frozen. Complete R studies before taxonomy and fusion.

## First-party bibliographic anchor and scientific limitation

Tanner, W. P., Jr. & Swets, J. A. (1954). A decision-making theory of visual detection. Psychological Review 61(6):401-409. DOI: https://doi.org/10.1037/h0058700; PubMed https://pubmed.ncbi.nlm.nih.gov/13215690/. This protocol borrows the signal-versus-noise likelihood decision framing. It does NOT fit human ratings, calculate Gaussian d-prime, establish perceptual normality, or claim to reproduce the original paper's experiments.

## Frozen 3 x 2 x 2 mathematical worlds

All outcomes on ordered evidence x in {0,1,2,3,4} and true class y in {0 noise,1 signal}. Conditional probabilities are exact rational vectors in that order:

* MONOTONE: noise=(8,6,4,2,1)/21, signal=(1,2,4,6,8)/21.
* CENTERED: noise=(8,2,1,2,8)/21, signal=(1,3,13,3,1)/21. Non-monotone likelihood ratios.
* IDENTICAL: noise=signal=(1,2,3,2,1)/9. Chance-level discrimination.

Signal prior pi in {1/2,3/4}, noise prior 1-pi. Two loss contracts: (false-positive cost, false-negative cost) in {(1,1),(1,3)}. True-positive and true-negative costs fixed at zero. This yields 12 named worlds, 10 outcome-label source cells per world, exactly 120 labeled artificial joint probability cells. No sampling/random seed, no subject observations.

## Predefined competing policies and tie conventions

1. Full discrete likelihood-ratio Bayes decision: at evidence x predict signal iff pi * C_FN * P(x|signal) > (1-pi)*C_FP*P(x|noise). EXACT TIES predict noise. It may select a disconnected set of x.
2. Single evidence-cutoff policies: predict signal iff x >= t, t in {0,1,2,3,4,5}. Pick minimum weighted risk; EXACT ties choose the smallest t.
3. Fixed reference single cutoff t=3 (not tuned).

Weighted risk R= (1-pi)*C_FP*Pr(predict signal|noise) + pi*C_FN*Pr(predict noise|signal). Signal hit rate and noise false-alarm rate are conditional quantities and MUST be separated from prior-weighted risk. All probabilities and risks use Fraction, preserving exact rational arithmetic.

## Primary fixed claims, independent route and negative controls

A. For every world, full-policy risk computed by exhaustively looping the 10 joint cells equals the independently derived sum over 5 bins of min{(1-pi) C_FP P(x|noise), pi C_FN P(x|signal)}. This also independently certifies global optimality among *all* 2^5 deterministic rules.
B. Full-policy risk never exceeds best single-cutoff risk; best cutoff never exceeds fixed t=3.
C. In CENTERED, with pi=1/2 and equal costs, the strictly Bayes-optimal signal bins equal {1,2,3} (non-contiguous in threshold direction) and risk is strictly lower than every single-threshold policy.
D. In IDENTICAL, conditional hit rate equals false alarm rate for every rule; the best constant rule depends on weighted priors/costs; discriminability is zero in this artificial sense even though classification risk changes with priors.
E. Increasing miss cost or signal prior cannot turn any positive Bayes bin into a negative bin for fixed conditional distributions under strict tie-negative rule; check exact nesting for the fixed policies.
F. Validate every conditional distribution sums to 1, every source joint mass is nonnegative, and every world sums to 1; preserve all 120 source rows and per-world 6 ROC cutoff points.

Third-party independent audit must read exported CSV and recompute numerator-based Bayes scores, brute-force all 32 subset rules and six threshold risks WITHOUT importing production functions. Verify CSV and JSON SHA256. No claim of E2/E3 or cross-study prediction.

## Frozen delivery and acceptance gates

Deliver standalone Python >=3.11 executable with --test and --emit; complete 120 source-cell CSV; 12-world exact results JSON with per-world thresholds, ROC and comparisons; SHA256 receipt; independent audit script; scientific report and bounded acceptance JSON. Run local Python tests plus independent source audit and, if available, GitHub Actions for Python 3.11/3.12 and separate independent audit. Only mark CLOSED_BOUNDED_E1 after successful test/CI evidence and immutable source audit. Any source changes after protocol require explicit documented erratum instead of silently altering this freeze. Do not modify original 239-candidate catalogue or expand the 239 denominator.
