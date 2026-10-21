# R161 prescore freeze: finite-population conformity, binomial transition kernels and absorbing-state probabilities

2026-10-21. Original catalog **P1/07-003 Conformist Transmission**. Previous main HEAD `d66b67d363ed18f545a49be876df74990d54022e` after R160 CLOSED_BOUNDED_E1.

## Primary paper and research-scope boundary
Robert Boyd and Peter J. Richerson (1985), *Culture and the Evolutionary Process*, University of Chicago Press, [publisher table of contents](https://press.uchicago.edu/ucp/books/book/chicago/C/bo5970597.html) chapter 7 on frequency-dependent bias and conformist transmission. Joseph Henrich and Robert Boyd (1998), *The Evolution of Conformist Transmission and the Emergence of Between-Group Differences*, *Evolution and Human Behavior* 19(4):215–241, DOI [10.1016/S1090-5138(98)00018-X](https://www.sciencedirect.com/science/article/pii/S109051389800018X), original Elsevier publisher abstract and section snippets inspected. Charles Efferson, Rafael Lalive, Peter J. Richerson, Richard McElreath, Mark Lubell (2008), *Conformists and mavericks: the empirics of frequency-dependent cultural transmission*, *Evolution and Human Behavior* 29(1):56–64, DOI [10.1016/j.evolhumbehav.2007.08.003](https://www.sciencedirect.com/science/article/pii/S1090513807000876), original publisher abstract inspected: empirical individual learning types are heterogeneous, majority-following is distinguishable from *exaggerated* majority following. We have NOT obtained/reproduced original experimental choices or fitted original model coefficients and have NOT recreated complete author's spatial-temporal fitness mechanisms. The finite N model below is **project-authored** E1 only, with culturally neutral labels A/B, no protected-group or actual human observations.

## 48 frozen finite-population worlds
Artificial homogeneous isolated population N∈{5,7}, current A count k, initial k in six frozen presets:
N=5: {0,1,2,3,4,5};
N=7: {0,1,2,5,6,7}.
Conformist strength h∈{0,1/4,1/2,1}. Exactly **2×6×4=48 different scenarios**. For count k, p=k/N. Synthetic three independent demonstrator majority C(p)=3p²−2p³, independent social-copying mixture q(k;h)=(1−h)p+hC(p). Each next-generation new A indicator independent Bernoulli(q), so \(K_{t+1}|K_t=k\sim Binomial(N,q(k;h))\). No mutation/innovation. Record conditional transition matrix T[k,j] for all k,j=0..N, and the entire probability distribution of K at times t=0..4 inclusive starting as point mass K0=k, plus expected next-period frequency and fixation outcomes. All arithmetic pure Fraction.

Method A: independent binomial coefficient kernel T[k,j]=comb(N,j)*q^j*(1−q)^(N−j); row-vector matrix multiplication for evolving distribution.
Method B: enumerate all 2^N binary next-generation indicator configurations and sum probabilities for exactly j A, then evolve distribution using independently coded loops (not call method A). Both must generate exactly same all 48 worlds×5 time distributions; all rows sum to one and remain nonnegative. Every preserved row and distribution element is exact Fraction (not float).

## Absorbing states and exact fixation test
Because q(0)=0,q(N)=1, states 0 and N are absorbing. For 0<k<N, 0<q(k;h)<1, finite Markov chain eventually hits one of the two absorbing states with probability one. Compute exact ultimate probability of all A by solving \((I-Q)u=R_N\) over transient states 1..N−1 by pure Fraction Gaussian elimination (up to 6×6); verify each solution's exact harmonic residual u[k]=sum_j T[k,j]*u[j] with u[0]=0,u[N]=1. Do not claim convergence at any fixed finite time.
Frozen checks:
1. Neutral h=0: fixation probability exactly k/N for all states and N, with first-generation mean exactly p.
2. For all h>0 and k/N<1/2, conditional expected next frequency q<p; if k/N>1/2, q>p.
3. N=5,h=1,k=1: all A fixation probability <1/5; for k=4 >4/5. At k=0,1 extremes stay absorbing.
4. At N=5 k=2 versus k=3 h=1, one-generation expected A frequencies are C(2/5)=44/125 and C(3/5)=81/125; their difference 37/125 > 1/5 neutral difference.
5. Symmetry: T[k,j]=T[N−k,N−j] and fixation probability u[k]=1−u[N−k] for each N,h.
6. Conformity is positive *frequency dependence*, not automatically selection of fitness-maximizing variant; nothing in synthetic model links A/B to external payoff.
7. With N=5,k=2,h=0, expected proportion of A remains 2/5 for all t but finite-generation distribution spreads to k=0 and k=N at positive probability. Avoid confusing unchanged expectation with deterministically constant frequency.
8. Contrast R159 deterministic \(p_{t+1}=q(p_t)\) to the finite-population stochastic chain; one-step *conditional expectation* agrees, but subsequent unconditional mean need not equal repeated deterministic frequency iterations because q is nonlinear (Jensen). Predeclared example N=5,h=1,k=2 at t=2, compare E[K2/N] against q(q(2/5)) and record difference; do not prespecify sign until validated.

## Acceptance and archival requirements
At least 48 individually named full scenarios plus ≥20 independently named boundary methods; exact binary enumerated and binomial computations, full JSON states and fixation solutions, author-source caveat and complete source/test/JSON ZIP; Python3.11 and 3.12 CI, four immutable SHA256, permanent GitHub main archive and readback. No E2 independent human learning choice data, no E3 historical behavioral predictions. R073 and PESEN v0.1 frozen. Next R series candidate only after original catalog verification. Complete all original R models then classify then fuse.
