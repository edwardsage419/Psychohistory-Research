# R165 preregistered neutral cultural drift, fixation time and symmetric innovation

Date 2026-10-21. Original model catalog **P1 / 07-007 Neutral Cultural Drift**. Last closed baseline main commit `e0dd8853defe9afeef935e47cb78ba233011a52b` includes formally closed R164. This experiment is frozen in GitHub **before any code**.

## Primary author literature and dimensional caution
Hahn and Bentley (2003), *Drift as a mechanism for cultural change: an example from baby names*, *Proceedings of the Royal Society B* 270 (Supplement 1):S120–S123, DOI [10.1098/rsbl.2003.0045](https://doi.org/10.1098/rsbl.2003.0045), [PubMed original record PMID12952655](https://pubmed.ncbi.nlm.nih.gov/12952655), [open original article](https://pmc.ncbi.nlm.nih.gov/articles/PMC1698036/) checked. The authors modeled many baby names as a random neutral copying baseline with *novel types* added over time, aiming to explain observed skewed frequency distributions.
Bentley, Hahn and Shennan (2004), *Random drift and culture change*, *Proceedings of the Royal Society B* 271(1547):1443–1450, DOI [10.1098/rspb.2004.2746](https://doi.org/10.1098/rspb.2004.2746), [PubMed record PMID15306315](https://pubmed.ncbi.nlm.nih.gov/15306315) and [Durham research record](https://durham-repository.worktribe.com/output/1622925) checked. Authors compare empirical distributions of names, pottery styles and patents against simple neutral drift models.
Original 2003 author's model is **multi-allele with unbounded novelty** and 2004 paper considers several real application-specific power-law distributions. This experiment uses only **TWO abstract cultural tokens A and B and symmetric innovation toward 1/2**. It cannot reproduce the author's name-rank power laws, real baby-name time series, pottery distributions, patent counts, real population size or original MATLAB simulation. No historical data acquired/replayed; this E1 exercise is a bounded *comparison to a neutral cultural baseline*, not empirical author replication. R161 used a neutral h=0 special case mainly to contrast conformity; R165 adds mean time to absorption and a unique stationary law under innovation.

## Frozen finite count chain and exact 48 cases
Isolated artificial population N∈{4,6,8} with A count Kt, current p=k/N. Artificial symmetric innovation probability μ∈{0,1/16,1/8,1/4}, all choices independently sample A with
q(k;N,μ)=(1−μ)k/N+μ/2.
Then K(t+1)|K(t)=k is Binomial(N,q); finite transition matrix T[k,j]=C(N,j)q^j(1−q)^(N−j).

Six? Exactly four initial counts for each N:
N=4: k0∈{0,1,2,4};
N=6: k0∈{0,1,3,6};
N=8: k0∈{0,1,4,8}.
Thus 3 population sizes × 4 initial counts × 4 innovation rates = **48 separately identified frozen scenarios**, all with five complete count-probability vectors t=0,...,4 and exact mean A prevalence and diversity \(H_t=E[2(K_t/N)(1−K_t/N)]\). Store exact Fraction strings.

Independent algorithms:
1. Direct Fraction binomial-coefficient rows and matrix-vector propagation.
2. Independently enumerate all 2^N possible binary outcomes per parent count and add their Bernoulli probability to resulting count, then independently propagate with nested loops; must agree on all three N, four μ, 48×5 distributions by *strict Fraction*.

## Frozen exact long-horizon quantities and negative controls
A. At μ=0, states k=0 and N are absorbing. Exact eventual fixation probability at all-A is k/N. Compute transient expected time to absorption \(\tau=(I−Q)^{-1}1\) on k=1,...,N−1 with independent exact Fraction Gaussian elimination; verify exact residual \(\tau_k=1+\sum_j T[k,j]\tau_j\) for all interior states, and \(\tau_0=\tau_N=0\).
B. At μ=0, mean frequency is a martingale E[Kt/N]=k0/N for every t and diversity declines by \(H_t=H_0(1−1/N)^t\) for each initial point mass k0. Smaller N loses diversity faster per step. This is *ensemble expectation*, not deterministic trajectory: even if the mean stays constant, random realization can become homogeneous.
C. At μ>0, neither boundary is absorbing, and one-step mean obeys E[p(t+1)]=(1−μ)E[p(t)]+μ/2, yielding \(m_t=1/2+(1−μ)^t(p0−1/2)\). No meaningful all-A fixation time exists as an absorbing event; do not solve zero-innovation absorption time for such cases.
D. At μ>0, exact unique stationary distribution π over counts 0..N is solved using \(πT=π\) and \(Σπ=1\) with exact Fraction Gaussian elimination, verified by full residual. By symmetry, π(k)=π(N−k) and Eπ[K/N]=1/2. Both boundaries have positive stationary mass, but are not absorbing.
E. At μ=0, there are at least two absorbing stationary distributions (delta_0 and delta_N and mixtures); do not report a *unique* stationary distribution.
F. Same initial frequency p=1/2 in N=4,6,8 exhibits distinct one-step variances q(1−q)/N and distinct time-to-absorption distributions; initial prevalence alone does not identify drift noise intensity N.
G. No fitness/payoff superiority is assigned. A cultural variant may fix purely through finite-sample neutral copying. This is a conditional mathematical mechanism, not evidence that observed modern cultural patterns are actually neutral.
H. Reject invalid k, N, μ, booleans, non-Fraction floats, negative times. All outputs stay rational and normalize exactly.

## Acceptance
>=48 individually named world tests plus >=25 independently named mechanism/stationary/fixation controls; full JSON and canonical standard-library source/tests/results ZIP with four fixed SHA256; Python3.11 and 3.12 GitHub CI; permanent main archival and readback; report original source boundaries. Only CLOSED_BOUNDED_E1 upon success. E2=0, E3=0. R073 and PESEN v0.1 remain frozen. Next catalog R166 must be independently checked.
