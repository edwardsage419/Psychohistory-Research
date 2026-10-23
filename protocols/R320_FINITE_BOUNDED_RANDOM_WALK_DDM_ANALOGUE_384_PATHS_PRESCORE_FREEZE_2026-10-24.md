# R320 prescore freeze: finite bounded random walk as a DDM analogue

Date 2026-10-24. Original239 01-009 Drift Diffusion Model, P2. **PRESCORE FREEZE ONLY**. This protocol is committed before any R320 path source, calculation or report.

## Primary references and strict reuse gate

Ratcliff (1978), *A theory of memory retrieval*, Psychological Review 85(2):59–108; Ratcliff and McKoon (2008), *The Diffusion Decision Model: Theory and Data for Two-Choice Decision Tasks*, Neural Computation 20(4):873–922, DOI 10.1162/neco.2008.12-06-420, full author manuscript https://pmc.ncbi.nlm.nih.gov/articles/PMC2474742/ . The published DDM uses continuous noisy evidence accumulation with two absorbing thresholds and nondecision time, with strong accuracy/RT distribution predictions. **R320 studies only an exactly enumerated discrete-time, discrete-space absorbing random walk analogue**. It does not implement the continuous-time Wiener first-passage distribution, original subject fits, or original 1978 model replication.

Repository-wide file-name tree search at 2026-10-24 found R131 evolutionary finite drift, R165 neutral cultural drift, R174 diffusion/invention, R147 policy diffusion and R289 sequential offers. These do not contain the same two-threshold evidence-accumulation decision-time mechanism. GitHub code searches for drift diffusion / first passage / sequential sampling returned zero results, which is insufficient to exclude all historical ZIP content. Reuse their general finite Markov arithmetic where useful; do not relabel these studies as R320 empirical evidence.

## Frozen source universe

For upper absorbing boundary a in {4,6}, start z=a/2 in {2,3}; probability of +1 step p in {1/4,1/2,3/4}; lower boundary 0; maximum decision steps T=6. The artificial sample space is **all 2^6=64 ordered six-bit exogenous increment sequences per world**, 0=step -1, 1=step +1, with exact independent Bernoulli mass p^u(1-p)^(6-u). The first boundary hit terminates the actual decision; subsequent bits are merely exogenous *mathematical continuation labels* for exhaustive probability accounting and must never be called observed post-decision behavior. The first hit time/side is determined only from the prefix until absorption. Paths without a hit by t=6 are right-censored.

Exactly **2*3=6 artificial worlds and 384 complete original path-source rows**, no exclusions. Fixed CSV fields: world_id, upper_bound, start, p_up, path_bits, up_steps, down_steps, full_path_probability, first_hit_time, first_hit_side, censored. Time empty and side=none for censored. Store a JSON summary per world of first-hit probability by each t=1..6 and side=lower/upper, survival probability, total hit probability, conditional mean decision steps among hits, and expected truncated steps E[min(tau,6)]. Fractions only, no Monte Carlo or random seeds.

## Prespecified falsifiable checks

1. Each world sums all 64 source path probabilities to exactly 1. First-hit joint distribution plus right-censor mass sums exactly 1. No path hits both boundaries. Absorbing time is first hit, and no non-censored time exceeds 6.
2. For a=4,z=2,p=1/2, total probability of a hit by t=6 is **7/8**, survival **1/8**, upper/lower probability each **7/16**. For a=6,z=3,p=1/2, the upper/lower hit probabilities are equal by path complement symmetry.
3. For each boundary a, p=1/4 versus p=3/4 swaps upper and lower first-hit probabilities at each t and preserves survival. For p=1/2, the two sides are symmetric at each t.
4. For p=1/2, survival at t=6 with a=6 is strictly greater than with a=4. All 384 original paths and all time-side cells must match a **separate no-import independent dynamic-programming audit**, which propagates only surviving interior mass rather than enumerating full six-bit strings.
5. Distinguish total choice probability by t=6 from eventual absorption probability, and conditional mean observed decision steps from nondecision time; no claim of full RT model.

## Reproduction and acceptance

Provide complete source CSV, summary JSON, stdlib generator with >=25 tests, independent dynamic-programming audit, source blob receipt and scientific report. GitHub Actions Python 3.11 and 3.12 tests plus separate independent audit must all succeed. Formal scientific acceptance is only **PASS_BOUNDED_E1_DISCRETE_ANALOGUE_ONLY** after 3 green jobs and Git blob verification; otherwise PENDING. No human E2, historical E3, original diffusion likelihood, drift-parameter fit, real RT validation or external prediction. Change only original239 01-009 after formal verification. R073 and PESEN v0.1 frozen; complete R series before taxonomy/fusion.
