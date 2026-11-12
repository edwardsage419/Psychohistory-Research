# R135: Exact boundary when public reputation loses information

**Date:** 2026-11-12, manual R-series research. **Status:** COMPLETE for bounded independent E1 mathematics, not a replacement for the frozen R135 phase A. **Pre-run main:** `d4e3357b91265cad16d0672c71111de941766c5c`.

## Primary source and precise scope

Ohtsuki H., Iwasa Y. (2004). *How should we define goodness? Reputation dynamics in indirect reciprocity.* J. Theor. Biol. 231:107–120. DOI `10.1016/j.jtbi.2004.06.005`. First-party paper: https://brainmind.umin.jp/public/Ohtsuki%26Iwasa%20JTB04.pdf . Read visually, printed pp.109–116, especially Eq. (3)–(10), Fig. 2, Fig. 3 and Table 4.

The original R135 frozen `mu_a=0.02`, `mu_e=0.02`, `b=2`, `c=1` analysis remains unchanged: 4096 (norm, strategy) combinations, 61440 mutant evaluations, 161 strict ESS mirror orbits, of which 25 are non-AllD. Original R135 freeze: `protocols/R135_OHTSUKI_IWASA_2004_FULL_4096_NORMS_MUTANT_INVASION_PRESCORE_FREEZE_2026-10-20.md`. Original final acceptance: `research/R135/R135_FINAL_ACCEPTANCE_STATUS.json`. Neither artifact has been edited. New results are **post-freeze artificial parameter sensitivity** and cannot be added to its historical preregistered pass count.

Only the original homogeneous infinite-population, shared public binary H-score, indirect-observation, binary intentional action, and independent noise model of the cited paper is studied. It is a mathematical investigation, not a claim about human reputation systems or empirical social history. For strict ESS conclusions from Eq. (10), assume `b>0`, `c>0`, `0 <= mu_e < 1`, `0 < mu_a <= 1/2`.

## Analytic theorem A: complete reputation erasure

From Eq. (3), for either intended action and any old own/recipient H-scores, the assignment probability becomes `t_ij = mu_a + (1-2 mu_a) * weighted_norm_output`. At **mu_a=1/2**, `t_ij=1/2` for every strategy and every eight-bit norm. Thus the Eq. (4) reputation dynamics are `d h / dt = 1/2 - h`, with unique stationary resident and rare-mutant reputation `h_r=h_m=1/2`. All four own/recipient reputation cells have probability exactly `1/4`.

Let `K(p)` be the number of intended C bits in a four-bit resident strategy, `K(p')` that of the mutant. Original Eq. (5)–(9) reduce to

`W(p|p) = (b-c) K(p)/4`,  `W(p'|p) = b K(p)/4 - c K(p')/4`.

The resident advantage is exactly `W(p|p)-W(p'|p)=c [K(p')-K(p)]/4`, independently of the norm and benefit `b`. Any resident with `K(p)>0` is beaten by the mutant `AllD`, whose `K(p')=0`; an `AllD` resident strictly beats every different mutant, as `c K(p')/4>0`. Hence **exactly 256 of the 4096 raw norm/strategy pairs are strictly stable**, all with `p=AllD`. There are **zero cooperative strict ESS**. If the action execution failure probability is positive, all payoff expressions acquire a common positive factor `(1-mu_e)`, so the ordering remains. At `mu_e=1`, all executed actions are D and strict behavioral ESS is lost; this degenerate endpoint is excluded.

For reputation mirror relabeling, the eight-bit norm involution has 16 fixed points, and the four-bit strategy involution has 4 fixed points. Burnside gives `(4096+16*4)/2=2080` total norm/strategy orbits. Among 256 AllD stable pairs, the fixed norms are still 16, giving `(256+16)/2=136` stable mirror orbits. The original frozen `mu_a=0.02` also had 136 AllD orbits, but **25 additional cooperative orbits**; the present endpoint has none.

## Analytic theorem B: a universal sufficient noncooperation region

For `0<mu_a<=1/2`, each Eq. (3) assignment transition falls in `[mu_a,1-mu_a]`; taking any stationary convex mixture of these transitions forces both resident and rare-mutant stationary H-scores `h_r,h_m` into the same interval. Hence `|h_r-h_m| <= 1-2 mu_a`.

For a fixed resident action rule p, its intended helping probability when meeting a recipient with H-score h is affine in h and has slope in `[-1,1]`. Therefore the resident's help received difference between resident and AllD mutant recipients obeys `|theta(p,p)-theta(p,AllD)| <= 1-2 mu_a`.

When the resident has at least one intended C bit, every own/recipient reputation-cell probability is at least `mu_a^2`, so the resident's intended helping rate is at least `mu_a^2`. Original Eq. (8)–(9), when the mutant is AllD, then imply

`W(AllD | p) - W(p | p) >= c mu_a^2 - b(1-2mu_a)`.

Thus if **`c mu_a^2 > b(1-2mu_a)`**, AllD strictly invades *every cooperative resident for every one of the 256 norms*, irrespective of the execution error as long as its positive common factor is respected. This is a **sufficient bound**, not the exact bifurcation threshold for the 4096 candidates.

For the original `b=2,c=1`, solving `mu_a^2+4mu_a-2>0` gives `mu_a > sqrt(6)-2 = 0.44948974278...`. At `mu_a=9/20`, the exact lower bound on AllD's intentional payoff advantage is `1/400` for every cooperative resident and every norm. At `mu_a=11/25`, the bound is negative (`-29/625`), which supplies **no conclusion** about actual ESS survival there. At `mu_a=1/2`, the bound is `1/4`, attained by one-bit resident strategies against AllD.

This sufficiency proof is global within the specified model; it does not depend on finite-grid sampling. Its limitation is intentional conservatism, especially for error rates below 0.44949. The paper's Fig. 3 studies `mu_e,mu_a` values around 0.005–0.08 and does not claim a numeric test at the information-erasure endpoint. This report does **not** attribute the new upper-error theorem to the original authors.

## Executed independent reproduction and diagnostics

Original-author algorithm/code was not rerun. A separate Python standard-library `Fraction` implementation computed the **actual** source Eq. (3) conditional assignment expectations and Eq. (5)–(9) original four-cell intentional payoffs and independently compared them with a count-only closed form at the erasure endpoint. Results:

* `256` distinct norm bit strings, `16` strategies, `4096` candidate residents, `61440` directed resident/mutant comparisons; **all exactly equal** to the separate four-bit cardinality formula.
* `36864` explicit conditional reputation-update checks at own/recipient H-scores `0`, `1/2`, `1`: all equal `1/2`.
* Raw strict ESS `256`, all sixteen strategy IDs except `0000` have zero winners. Mirror fixed norms `16`, total fixed pairs `64`, total orbits `2080`, erasure-ESS orbits `136`.
* Minimum AllD resident strict winning margin in the paper's **intended-payoff units**: `1/4`; actual executed helping rates multiply every payoff comparison by `49/50` for `mu_e=1/50`.
* Explicit source-payoff comparisons with equality: `13824` directed comparisons, many from different rules with identical count `K`; these do not create a strictly ESS resident.
* Seven Python `unittest` functions passed on the corrected local program with no failure, 4.674s. Test cases include exact Eq. (3) at five arbitrary old H-score values; Eq. (5)–(9) pairwise checks; whole `4096 x 15` enumeration; mirror Burnside counts; rational bound sign changes; zero-cost exclusion; and non-erasure controls.
* During development a **newly written mirror-index transform** was initially reversed and produced 0 rather than 16 fixed norms, causing one local unit test to fail. It was corrected to swap `11<->00`, `10<->01` while complementing output. Subsequent full tests passed. This failure occurred **only in this new exploratory code** and does not establish a defect in frozen R135.

Program: `research/R135/r135_assignment_noise_boundary_20261112.py`  
Machine result: `research/R135/R135_ASSIGNMENT_NOISE_ERASURE_RESULTS_20261112.json`.

Local program SHA256: `c17713a42aa4feb063751d5a2ba5734832e266bc6deb7c4250e78f2ed35e1158`.  
Local JSON SHA256: `5ad4a8a2eda8e286f7c0bd6eeb95461fcd1e1336c195e6e0789dfa7560f507b3`.

Reproduce with Python 3.11+:

```sh
python research/R135/r135_assignment_noise_boundary_20261112.py --test
python research/R135/r135_assignment_noise_boundary_20261112.py > erasure-result.json
```

## Evidence and governance limits

Evidence class: new **mathematical/synthetic E1**. No real person/animal decisions were used, no observational sample, no out-of-population prediction, no historical event, and no independent external laboratory replication. Frozen R073 and PESEN v0.1 remain untouched. No CI was triggered, GitHub billing was not independently verified, and no additional paid resource was used. The proof is independent mathematical reasoning and the code is an internal second implementation, with `mu_a=1/2` outside the paper's published small-error figure range.

**Next:** If valuable, inspect intermediate error rates with a separate preregistered exploratory parameter grid and robust interval root solver to estimate rather than mislabel the exact cooperative ESS failure threshold. For the R-series queue, choose an *unreviewed* item based on the current actual index instead of redoing the completed original R135 4096-case scan.