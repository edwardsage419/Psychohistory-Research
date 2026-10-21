# R161 scientific report: finite-population conformist copying, stochastic drift and exact cultural fixation

Date: 2026-10-21. Original candidate **P1/07-003 Conformist Transmission**. All experiments frozen in [precode protocol](../../protocols/R161_FINITE_CONFORMITY_48_MARKOV_WORLDS_PRESCORE_FREEZE_2026-10-21.md), [commit e0d590f](https://github.com/edwardsage419/Psychohistory-Research/commit/e0d590fc3946847a588d9b111808612ae0384d79). The scientific status is **CLOSED_BOUNDED_E1**, meaning *project-authored, synthetic finite-population stochastic mathematics* only.

## Original sources and competing empirical observations
* Robert Boyd and Peter J. Richerson, *Culture and the Evolutionary Process* (1985), [University of Chicago Press original book contents](https://press.uchicago.edu/ucp/books/book/chicago/C/bo5970597.html), explicitly includes chapter 7 "Frequency-dependent Bias and the Evolution of Cooperation", with sections on adaptive conformity and empirical conformity research. The complete book's source algorithms and data were not reproduced.
* Joseph Henrich and Robert Boyd (1998), *The Evolution of Conformist Transmission and the Emergence of Between-Group Differences*, *Evolution and Human Behavior* 19(4):215–241, DOI [10.1016/S1090-5138(98)00018-X](https://www.sciencedirect.com/science/article/pii/S109051389800018X). The original Elsevier full abstract and online section excerpts were read. The authors address why conformity may evolve under spatiotemporal environmental change and how it may sustain cultural differentiation. **No original author environmental dynamics, behavioral data or experimental choices were duplicated**.
* Charles Efferson, Rafael Lalive, Peter J. Richerson, Richard McElreath, Mark Lubell (2008), *Conformists and mavericks: the empirics of frequency-dependent cultural transmission*, *Evolution and Human Behavior* 29(1):56–64, DOI [10.1016/j.evolhumbehav.2007.08.003](https://www.sciencedirect.com/science/article/pii/S1090513807000876). Original publisher abstract read: the authors caution that ordinary majority-following must be distinguished from **exaggerated** frequency dependence and report heterogeneous learning styles. Original person-level payoff/choice data and estimates were not acquired. This source demonstrates why observing a modal behavior alone does not validate our project parameter \(h\).

The model below consists solely of independent artificial A/B cultural labels in small mathematically isolated groups, not identifiable human communities. Source models are wider than this simple binomial copying process. No real-life conformity estimate, policy effect, actual institutional persistence or group selection mechanism is claimed.

## Frozen exact Markov construction
Each artificial population has size N=5 or N=7. Start count \(K_0\) in six frozen choices: for N=5, k=0,1,2,3,4,5; for N=7, k=0,1,2,5,6,7. Conformist strength h∈{0,1/4,1/2,1}. Hence **2×6×4=48 independent synthetic worlds**, all with entire count-distribution trajectory for t=0,1,2,3,4. Conditional on current count k, a learner's theoretical A-choice probability is
\[
q(k;h)=(1-h)\frac{k}{N}
+h\left[3\left(\frac{k}{N}\right)^2-2\left(\frac{k}{N}\right)^3\right].
\]
Next-generation N learner choices are mutually independent by project assumption, so \(K_{t+1}\mid K_t=k\sim Binomial(N,q(k;h))\). There is no mutation, immigration, fitness or family structure. Neither this binomial sampling equation nor its exact fixation solutions are claimed from the original authors.

The exact transition matrix is \(T_{kj}=\binom Nj q(k;h)^j(1-q(k;h))^{N-j}\). Two independent Fraction implementations were executed:
1. Combinatorial binomial coefficients followed by row-vector matrix evolution.
2. Full enumeration of all 2^N possible next-generation binary configurations (32/128 sequences for N=5/7) with independent summing by A count, then separate distribution propagation.
All 48×5 full count distributions are **identical by strict Fraction equality**, all transition rows strictly normalize, and all entries are nonnegative. Eight canonical transition matrices (2 population sizes × 4 h values) are preserved in [143,483-byte complete JSON](R161_EXACT_RESULTS.json).

## Exact eventual absorbing probabilities
Count k=0 and k=N are absorbing, and every other count has positive probability of immediate absorption at either endpoint. The exact probability of eventual all-A fixation \(u_k\) is solved by Fraction Gaussian elimination for the transient states, \((I-Q)u=R_N\), with u_0=0 and u_N=1. We then check **every harmonic identity** \(u_k=\sum_j T_{kj}u_j\) as an exact rational equality, independently of the solver's elimination steps.

For neutral copying h=0, all N and all k have \(u_k=k/N\), a standard exact martingale result. For **N=5,h=1**, probabilities include
\[
u_1=\frac{41690187205771}{928107300091355}\approx 0.044919,\quad
u_4=\frac{886417112885584}{928107300091355}\approx 0.955081.
\]
The purely mathematical majority-bias scheme suppresses fixation of an initial minority relative to neutral values 0.2 and enhances fixation of the initial majority relative to 0.8. These are *eventual* absorbing probabilities, **not** a prediction about a finite generation or any real culture.

## Finite population mean versus deterministic limit
The finite Markov model has one-generation conditional mean \(\mathbb E[K_{t+1}/N\mid K_t=k]=q(k;h)\). Thus at N=5, k=2 and full conformity h=1, first next-generation expected A frequency is 44/125=0.352. Starting from k=3, it is 81/125=0.648; the gap 37/125=0.296 exceeds the original prevalence gap 1/5=0.2.

The **frozen divergence counterexample** occurs after two generations when N=5, k=2,h=1:
\[
\mathbb E[K_2/N]=\frac{15605084}{48828125}=0.31959212032;
\quad
q(q(2/5))=\frac{555632}{1953125}=0.284483584.
\]
Their difference is \(1714284/48828125=0.03510853632\). The deterministic recurrence applied to its own mean ignores the variance in the first-generation distribution; with nonlinear conformity, \(\mathbb E[q(K_1/N)]\ne q(\mathbb E[K_1/N])\). R159 explored a deterministic culture-frequency update; R161 establishes a **distinct finite-population mechanism and exact case**, with no historical generalization beyond the toy assumptions.

In contrast, for h=0 neutral copying, the *unconditional expected fraction* is exactly constant k/N for all generations, while the **distribution** spreads to both absorbing endpoints with positive probability. An unchanged expectation alone is not evidence of a stationary or certain cultural composition. Mirrored initial states have complementary fixation probabilities and reflected transition rows.

## Reproduction, tests and boundary of acceptance
[Source implementation](r161_finite_conformist_markov.py), [78 real unittest methods](test_r161_finite_conformist_markov.py): 48 individually named full scenarios plus 30 distinct conditional-distribution, normalization, exact absorption, source-scope, negative-input and deterministic-versus-stochastic controls.
* First [GitHub Actions run39525830737](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39525830737) succeeded: Python3.11 and 3.12 each executed all 78 tests and generated identical SHA256 across source, tests, JSON and ZIP.
* Second [pinned run39525915174](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39525915174) succeeded in both Python versions with 78 tests each, and an independent publishing job118980461164 reran all 78 before verifying all four fixed hashes and permanently publishing [complete JSON](R161_EXACT_RESULTS.json) and [ZIP](R161_Conformity_48_Finite_Worlds_78_Tests.zip) on main in [archive commit e13324a](https://github.com/edwardsage419/Psychohistory-Research/commit/e13324aa0f82bbd39f8370b1b4a4e55f9cf8edcf).
* Total **390 actually executed unit tests in five test invocations, 78 distinct methods, 0 failures**. These repetitions support computational reproducibility, not causal empirical generalizability.
* Immutable source SHA256 `744026427340efd9addba636d36fdefd65e94604f40678563e5b9995eccb2f21`; tests `ee6b29e5bd404fde7cdd692ce2b348f0fe056cdaf839f24b9a0740c39971f699`; original JSON `8cba0edf39013a0bb8dd694e00b00f38cae20fd5473e46c7f0b0a6474232d5af`; canonical ZIP `dfd9483ca9f98f9fd07f671918b2074a846642d13e8dc17e4366fd35397ee766`.
* Replay from `research/R161` via `python r161_finite_conformist_markov.py > R161_EXACT_RESULTS.json`, then `python -m unittest -q test_r161_finite_conformist_markov.py`. Python standard library only.

The stage is **CLOSED_BOUNDED_E1 for the frozen synthetic finite-state stochastic test**. No original 1998/2008 person-level empirical results are re-estimated, no natural selection/migration/actual cultural identity observations, and no E2/E3 evidence added. R073 and PESEN v0.1 continue FROZEN. According to the original candidate catalog, the next stage must be checked as **R162 P1/07-004 Prestige Biased Transmission**, followed by remaining R items before classification or fusion.
