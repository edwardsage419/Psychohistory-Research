# R135 Supplementary mathematical result: exact cooperation-ESS disappearance threshold

Date: 2026-11-13. Track: manual R-series bounded post-freeze E1 mathematics. Scientific status: `COMPLETE_INTERNAL_EXACT_THEOREM_WITH_REEXECUTABLE_CERTIFICATES`. This is an entirely new sensitivity statement, with **no change to the historical frozen R135 test, original accepted result, original paper, or evidence grade**.

## Starting state, source, and independence limits

Observed GitHub main at selection: `d57cfdc9efac9c66c861f2c34abec70c96c83569`. Nine open Codex A/B engineering PRs #30–33 and #35–39 were checked and do not address this post-freeze R135 mathematical threshold. Five scheduled workflows remained enabled. Avoided active R131, R132, R133 closure and R257 engineering verification, as well as previously archived R134/R136/R137 sensitivities.

Primary source: H. Ohtsuki and Y. Iwasa (2004), *How should we define goodness? Reputation dynamics in indirect reciprocity*, *Journal of Theoretical Biology* 231:107–120, DOI: 10.1016/j.jtbi.2004.06.005. Author/institution-hosted original: https://brainmind.umin.jp/public/Ohtsuki%26Iwasa%20JTB04.pdf. Newly inspected original printed page 111 (the indirect-observation model and noise definitions), page 112 (Eq. 2–10) and page 113 (original 4096-case ESS count and Fig. 2). Date of inspection: 2026-11-13. The authors' original parameter estimates, any original source code, and actual individual human or animal decisions were **not** newly acquired.

The research reimplements the same discrete 8-bit public reputation norm `d`, 4-bit behavioral strategy `p`, independent binary public H-scores, infinitely large randomly rematched population, **indirect observation**, one-way execution noise, assignment noise, and rare mutant ESS criterion. All 256 norms, all 16 strategies and 15 distinct mutant strategies per resident are within scope. Only the new assignment-error variable `a=mu_a` is varied over **`[1/50,1/2]`**, with `b=2`, `c=1` and execution error `mu_e=1/50` fixed throughout. Assignment error larger than 1/2 is outside the theorem. An executed help has common positive factor `49/50`, so intentional payoff ordering is unchanged.

Original 2026-10-20 freeze: `protocols/R135_OHTSUKI_IWASA_2004_FULL_4096_NORMS_MUTANT_INVASION_PRESCORE_FREEZE_2026-10-20.md`; historical result: `research/R135/R135_FINAL_ACCEPTANCE_STATUS.json`. The 2026-11-12 supplementary **complete-erasure endpoint** and earlier sufficient disappearance bound `sqrt(6)-2` are left untouched. This new result tightens the bound **only for the fixed model family above**, using a distinct proof.

## Exact mathematical statement

Define

`a_star = 2401/8502 = 0.282404140202305...`.

Under the model and fixed parameters just stated:

1. For each `a in [1/50,a_star)`, there exists a cooperative strict ESS, for example norm `d=10011000` (integer 152, JUDGE) with strategy `p=1010` (integer 10, helps recipients with good H-score). All fifteen alternative mutant behavioral rules have strictly smaller payoff.
2. For each `a in [a_star,1/2]`, all 256 norms combined with any of the 15 strategies containing at least one intended cooperation bit fail the **strict ESS** condition. At `a=a_star`, some residents are tied by a mutant; for `a>a_star`, the AllD behavioral mutant earns strictly more against every cooperative resident.
3. For every `a in [1/50,1/2]`, all 256 norm/AllD pairs are strict ESS: they neither pay cooperation costs nor can be successfully invaded by a distinct strategy with a strictly positive intended helping probability. Hence from `a_star` onward there are precisely **256 raw ESS**, or **136 mirror-equivalent ESS**, all AllD; there are zero cooperative strict ESS.

This is a **fixed-parameter internal mathematical theorem**, not a parameter estimated from the data and not a universal threshold for all indirect reciprocity theories.

## Derivation of the witness equality

For `d=10011000`, `p=1010`, write `h` for stationary resident H-score. From the first-party Eq. (3)–(4) with `mu_e=1/50`, the resident fixed point is the unique root `h in (0,1)` of

`100*a*h^2 - 198*a*h + 50*a - 50*h^2 + 49*h = 0`.

Against the AllD mutant, Eq. (3)–(4) gives the mutant's stationary H-score

`h_m = a / [2*a+(1-2*a)*h]`.

For the `p=1010` resident, `theta(p,h,h)=h` and `theta(p,h,h_m)=h_m`. Hence the payoff advantage of resident over AllD is `h-2*h_m`, with equality exactly when `h=2*h_m`. Eliminate `h` from these two equations. The exact resultant, computed with SymPy rational polynomials, factors as

`a*(2*a-1)^2*(8502*a-2401)/1250`.

Only `a_star` can be a genuine equality in the interior `(1/50,1/2)`. At `a_star`, the physically admissible resident root is **`h=49/74`**, the other algebraic root `-49/50` being invalid. Direct rational substitution gives `h_m=49/148`, hence a **true equality**. At `a=0.3` the resident advantage is strictly negative; by continuity and lack of further admissible zeros, it remains negative throughout `(a_star,1/2)`. At the endpoint `a=1/2` the gap is exactly `-1/2` (the `2*a-1` resultant factor is spurious at this endpoint). The same conclusion applies to the eight boundary norm/strategy pairs below, by unused norm bits and exact reputation relabeling.

## Proving the witness persists below the threshold

The witness's fifteen distinct mutant payoff differences were independently constructed from first-party Eq. (3)–(10). For each, SymPy polynomial resultants were factored and exact real-root counts checked on the **open interval `(1/50,a_star)`**. There are **zero** such roots across the fifteen comparisons. At `a=1/50`, every mutant is shown to lose by a **strictly positive certified rational lower bound** obtained by 24-step rational stationary-root bracketing and a conservative derivative bound `100`. Thus all 15 inequalities remain strictly positive for all `a in [1/50,a_star)`. At `a_star`, the exact tie mutant IDs are 0 (AllD), 2 and 8, confirming strictness ceases there.

Machine source and complete symbolic factor list: `r135_threshold_symbolic.py`, `R135_THRESHOLD_SYMBOLIC_CERTIFICATE_20261113.json`. SymPy 1.14.0 was **actually executed** under Python 3.13.5. SymPy is a free open-source dependency for this secondary symbolic proof; the global interval certificate uses **only Python standard-library Fraction**.

## Excluding *all* cooperative residents above the threshold

For arbitrary norm d and strategy p, the resident H-score satisfies

`h = a + (1-2*a)*F_d,p(h)`, where `F_d,p` is a quadratic Bernoulli-mixing polynomial with corner coefficients in `[0,1]`.

Over `a in [a_star,1/2]`, `h in [a,1-a]` and

`|F'_d,p(h)| <= 2*max(h,1-h) <= 2*(1-a)`.

This yields the uniform exact implicit differentiation bound

`|dh/da| <= 1/[1-2*(1-2*a)*(1-a)] <= 2.664`.

The stationary AllD mutant H-score has affine-in-resident-H-score numerator and denominator `h_m=g_0/(1-g_1+g_0)`. Because `g_0 >= a`, `g_1 <= 1-a`, its denominator is at least `2*a`. Consequently

`|partial h_m/partial a| <= 1/(2*a)`, `|partial h_m/partial h| <= (1-2*a)/(2*a)`.

For every resident cooperation strategy define the source-payoff difference

`G_d,p(a) = theta(p,h,h) - 2*theta(p,h,h_m)`.

The four binary help cells imply each partial derivative of `theta` with respect to either H-score has absolute value at most 1. Combining these bounds yields

`|dG_d,p/da| <= (2+1/a)*[1-2*(1-2*a)*(1-a)]^-1 + 1/a < 19`,

and at fixed `a`, `|partial G_d,p/partial h| <= 2+1/a < 6` over the audited interval.

Of the `256*15=3840` cooperative residents, the following **eight** norm/behavior pairs can reach `G=0` at `a_star`:

`(81,5), (89,5), (152,10), (154,10), (184,10), (186,10), (209,5), (217,5)`.

The four norm variants for strategy 10 have identical source-payoff response against AllD because the varied norm bits concern actions never used by either resident or AllD. Their strategy-5 mirrors are identical under good/bad relabeling. The same explicit resultant and boundary sign proof applies, so all eight have `G<0` for `a>a_star` and `G=0` at `a_star`.

**All 3832 remaining cases** were covered using **48 closed rational intervals** spanning the entire continuous parameter range `[a_star,1/2]`. For each interval's exact rational midpoint a, ten steps of rational bisection enclose the unique resident root h within width `2^-10`. The payoff `G` at the rational midpoint of that bracket was evaluated **exactly** with `fractions.Fraction` and is extended to *every parameter in the interval* by adding conservative errors

`(6 / 2^11) + (19 * (1/2 - a_star)/(2*48)) = 3/1024 + 17575/408096`.

There were `48*3832 = 183936` independent exact-Fraction midpoint evaluations. Across all of them, the **largest certified upper bound on resident minus AllD payoff** was

`-801049/26118144 ≈ -0.0306702114821 < 0`.

This is a uniform *strict* negative certificate over the **entire continuous interval** for all 3832 nonexception pairs, not a claim based only on a discrete grid. Machine certificate, cases, derivative-bound constants and complete executable auditor: `R135_THRESHOLD_INTERVAL_CERTIFICATE_20261113.json`, `r135_threshold_interval.py`. The 8 exceptions are handled analytically and separately, which closes the endpoint equality issue.

## Independent baseline parity, numerical diagnostics and testing

A separate float64 implementation reconstructed the 256 x 16 full strategy ESS scan from first-party Eq. (3)–(10) under the original published conditions (`mu_a=mu_e=0.02`, `c=1`). The **five** reported nontrivial mirror-ESS counts for benefits `b=(4,3,2,1.2,1.1)` were reproduced exactly: **(73,59,25,15,13)**, as in the paper's original Fig. 2. The new scanned error-rate sequence was stored as a numerical **diagnostic** and was never used for the rational interval proof.

Exploratory fixed `b=2` count examples:

| Assignment-error a | Nontrivial mirror ESS |
|---:|---:|
| 0.02 | 25 |
| 0.12 | 23 |
| 0.20 | 9 |
| 0.24 | 7 |
| 0.25 | 2 |
| 0.28 | 2 |
| 0.282 | 2 |
| 0.283 | 0 |
| 0.50 | 0 |

`test_r135_threshold.py` ran **7 actual standard-library tests** successfully in normal Python and **7 in Python -O**, total 14, both with zero failures. These tests verify baseline five-count parity, extra grid checks, exact root/equalities, symbolic receipt completeness, exception-mirror invariance and the derivative bounds. The interval certificate and symbolic certificate themselves were *actually generated*, using exact arithmetic. Their execution is separate from simply checking stored files.

No GitHub Actions or external paid compute was run. The fresh scripts have no use of removable bare `assert` for acceptance logic; internal failures use explicit exceptions. All results are calculated by the project's own operator, so this is **independent internal algorithmic cross-validation**, not an outside-laboratory replication.

## Program, outputs, and status

* `r135_threshold_scan.py`: independent full original-equation and new-error numerical model.
* `r135_threshold_interval.py`: reproducible exact rational global interval certificate; Python standard library only.
* `r135_threshold_symbolic.py`: exact fifteen-mutant symbolic/resultant witness proof; free SymPy.
* `test_r135_threshold.py`: normal/optimized 7-test acceptance checks.
* `R135_THRESHOLD_GRID_20261113.json`: exploratory grid and published five-benefit parity.
* `R135_THRESHOLD_INTERVAL_CERTIFICATE_20261113.json`: actual 183936 rational midpoint and derivative-cover receipt.
* `R135_THRESHOLD_SYMBOLIC_CERTIFICATE_20261113.json`: exact resultants and interval root counts.

As of this report: mathematical theorem for the stated model is **COMPLETE_INTERNAL_E1**. Scientific closure of the *full original239 catalogue item*, external animal/human E2 transfer and independent historical E3 remain **not established**. R073, PESEN v0.1, original R135 freeze and all historical receipts remain unchanged. No new costs, no workflow prompt adjustments, no Codex task reassignment, no production scoring.
