# R165 scientific report: exact finite neutral cultural drift, absorption times and innovation stationary law

Date 2026-10-21. Original catalog **P1 / 07-007 Neutral Cultural Drift**. [Precomputation freeze](../../protocols/R165_NEUTRAL_CULTURAL_DRIFT_48_MARKOV_INNOVATION_WORLDS_PRESCORE_FREEZE_2026-10-21.md) committed first at [5963e3a](https://github.com/edwardsage419/Psychohistory-Research/commit/5963e3aa7141c84372636c01be56803b85141c93). **Formal status CLOSED_BOUNDED_E1** for a project-authored, exactly calculated two-symbol cultural neutral-sampling baseline.

## Authors' original research and access limits
* Matthew W. Hahn and R. Alexander Bentley (2003), *Drift as a mechanism for cultural change: an example from baby names*, *Proceedings of the Royal Society B* 270 Suppl 1:S120–S123, DOI [10.1098/rsbl.2003.0045](https://doi.org/10.1098/rsbl.2003.0045), [original NIH full-text record](https://pmc.ncbi.nlm.nih.gov/articles/PMC1698036/) and [PubMed PMID12952655](https://pubmed.ncbi.nlm.nih.gov/12952655). Authors model the emergence and disappearance of names via neutral random copying and **novel name innovation** in a many-variant population.
* R. Alexander Bentley, Matthew W. Hahn and Stephen J. Shennan (2004), *Random drift and culture change*, *Proceedings of the Royal Society B* 271(1547):1443–1450, DOI [10.1098/rspb.2004.2746](https://doi.org/10.1098/rspb.2004.2746), [PubMed PMID15306315](https://pubmed.ncbi.nlm.nih.gov/15306315) and [Durham research record](https://durham-repository.worktribe.com/output/1622925). Authors compare original data involving first names, pottery types and patent classes with neutral-copying power-law-like distributions.
* This R165 does **not** reproduce those multi-category/new-type distributions, author MATLAB code, source population sizes or any of the three historical datasets. A two-token artificial process has no mechanism for generating a long tail of many novel types. The source findings are conceptual motivation and applicability boundary, not empirical validation of R165.

## Frozen 48 artificial finite Markov worlds

Artificial isolated populations of fixed size N∈{4,6,8}, each with two anonymous token types A/B. For each N, four preregistered initial A counts: N4 {0,1,2,4}; N6 {0,1,3,6}; N8 {0,1,4,8}. Four symmetric content-neutral innovation probabilities μ∈{0,1/16,1/8,1/4}. Exactly **3×4×4=48** fully identified worlds, each with 5 entire count-probability distributions for t=0,1,2,3,4.

Given current A count k, the artificial new learner selects token A with probability
\[
q(k;N,\mu)=(1-\mu)k/N+\mu/2;\qquad
K_{t+1}\mid K_t=k\sim\mathrm{Binomial}(N,q).
\]
This represents uniformly random copying plus hypothetical balanced innovation, with no popularity fitness, importance or payoff. It is a finite two-variant Markov model.

Two independently written Fraction methods:
1. Exact binomial combination count-transition kernel and probability row-vector propagation.
2. Enumeration of all \(2^N\) next-generation individual binary configurations (up to 256) and separate nested-loop propagation across all count states.

All **12 complete transition kernels** for three sizes and four innovation rates were strictly identical as exact fractions. All 48×5 complete count-distributions, means and expected diversity values were strictly identical. All transition rows and time distributions sum to one exactly. The entire state-level evidence and conditional kernels are in [full results JSON](R165_EXACT_RESULTS.json).

## Exact expected time to neutral fixation

When μ=0 the all-B and all-A states are absorbing. The eventual all-A fixation probability is k/N, because current A fraction is a martingale in the artificial model. For interior states, the exact expected time τ_k until reaching either endpoint solves
\[
\tau_k=1+\sum_{j=1}^{N-1}T_{kj}\tau_j,\quad \tau_0=\tau_N=0.
\]
The study uses independent Fraction Gaussian elimination on the finite transient matrix, and validates every residual exactly.

For **equal initial frequency p=1/2**, the results are:
* N=4, k0=2: exact τ=132/29 ≈ **4.5517241379 generations**.
* N=8, k0=4: exact τ=738222218968/74653224767 ≈ **9.8886849332 generations**.

Their different neutral absorption times occur despite the same initial composition. In a one-step sample at p=1/2, the variance of the next A fraction is \(p(1-p)/N\), equal to **1/16** for N4 and **1/32** for N8. Smaller finite populations drift faster under the frozen independent-copying assumptions. These are modeled ensemble quantities, not measured times to cultural extinction in societies.

## Expected diversity decline and innovation

Define the artificial pair-diversity index \(H_t=\mathbb{E}[2(K_t/N)(1-K_t/N)]\). For μ=0, the exact expected diversity decays by
\[
H_t=H_0(1-1/N)^t
\]
even while the expected A fraction remains fixed at its starting k/N. This proves that a stable **average** need not imply a stable realized social composition.

When μ>0 the endpoints are no longer absorbing. The exact expectation follows
\[
\mathbb E[K_t/N]=1/2+(1-\mu)^t(k_0/N-1/2).
\]
The finite chain has strictly positive transition probabilities, a unique stationary distribution π for each fixed (N,μ>0), and mean A fraction exactly 1/2. We solved πT=π, ∑π=1 in exact Fraction, verified every stationary equation, and found reflected symmetry π(k)=π(N−k). The no-innovation process instead has **multiple stationary distributions** (including point masses at both endpoints and their mixtures). Therefore a single unique stationary composition cannot be asserted at μ=0.

This deliberate two-token innovation mechanism always replaces with token A or B uniformly. It does **not** produce newly named cultural variants and cannot generate the full tail of distinct names of Hahn/Bentley's original research. Its use is a bounded mathematical baseline for later model comparisons only.

## Verification and provenance

[Source code](r165_neutral_drift_exact.py), [82 genuine unittest methods](test_r165_neutral_drift_exact.py), with 48 uniquely named complete worlds and 34 further independent normalization, exact stationarity, absorption-time, innovation, reflectivity, diversity, negative-type and JSON replay checks.

* [Initial CI 39530110643](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39530110643): Python3.11 and Python3.12 each passed 82 tests, with identical four SHA256 hashes.
* [Pinned CI39530175910](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39530175910): both Python versions again passed 82 tests and verified all four artifact identities.
* [Archive CI39530202133](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39530202133): Python3.11 and 3.12 each passed 82 tests; independent publisher job118994150188 separately re-ran 82 tests and compared all hashes, then permanently archived the complete original JSON and deterministic ZIP in main at [commit9b3d1dd](https://github.com/edwardsage419/Psychohistory-Research/commit/9b3d1dd56a91affa30cebfa825fd2e9352bd5a9b).
* Total **574 real unittest method executions, 82 different methods, zero failures**; seven runs of the same 82 methods support computational reproducibility, not independent historical replication.
* Fixed SHA256: source `33e480abee890329bc93d59877697df97dac577e766452caea63c617cddeea09`; tests `214e0583fc1fff08b69869c3d3883c90322518710c6bb66a5cfd0b4f52d3250b`; JSON `826576f87f5c586e64d3d70861e876e665da90beac5fbd49948a8839639018b8`; [complete ZIP](R165_Neutral_Drift_48_Worlds_82_Tests.zip) `771d60b9a01ad39851bef77382f1d8d7d4b380779d24c5cbaecf74565565b724`.
* Replay from `research/R165`: `python r165_neutral_drift_exact.py > R165_EXACT_RESULTS.json` followed by `python -m unittest -q test_r165_neutral_drift_exact.py`; all standard library.

**Final scientific assessment: R165 CLOSED_BOUNDED_E1** for finite cultural two-token random-copying and symmetric innovation mathematics. No original human or archival artifact measurements were replicated: new E2=0, E3=0. R073 and PESEN v0.1 remain frozen. Continue original R series with next verified catalog **R166 P1 / 07-008**, whose exact name must be confirmed before starting. Only after all planned R studies are complete should unified categorization and fusion begin.
