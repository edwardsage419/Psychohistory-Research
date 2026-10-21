# R168 precode freeze | finite three-level cumulative cultural learning under sampling versus individual fidelity

Date 2026-10-21. Catalog **P1 / 07-010 Cumulative Cultural Evolution**. This protocol is frozen before R168 model implementation. **Previous Derex2013 human source file access unsuccessful**, recorded in [original-study access and disagreement audit](../research/R168/R168_EMPIRICAL_ACCESS_AND_2014_DISPUTE_AUDIT_2026-10-21.md): Nature 2013 publisher challenge and missing XLS, separate 2015 Dryad CC0 metadata but protected bytes, Social Sciences Replication Project protocol has no results. Do not claim original human predictions or replication. Primary motivations from Derex et al. 2013 DOI https://doi.org/10.1038/nature12774, Andersson & Read 2014 critique DOI https://doi.org/10.1038/nature13411, Derex et al. 2014 reply DOI https://doi.org/10.1038/nature13412, Henrich 2004 DOI https://doi.org/10.2307/4128416, and Tennie et al. 2009 DOI https://doi.org/10.1098/rstb.2009.0052. The equations below are entirely *project-authored*, are **not** reproductions of original Derex or Henrich models, and are a restricted E1 sampling/confounding mechanism test.

## 64 frozen exact artificial worlds
One fictional socially shared cultural-skill frontier level L_t ∈ {0,1,2}; labels stand for increasing abstract complexity and are not measured technique quality. Artificial population N∈{2,4,8,16}. Independent attempt fidelity f∈{1/2,3/4}. Innovation probability u∈{0,1/8}. Two observation-access modes:
* **full_pool**: there are N independent cultural trials each next generation and the group records the maximum level across them.
* **single_channel**: exactly one effective cultural trial each generation, regardless of N, and the group records its outcome.

Initial shared frontier L0 ∈{0,2}. Exactly 4 population sizes ×2 fidelity ×2 innovation ×2 modes ×2 initial levels =**64 cases**, each stored as five complete probability vectors t=0,...,4 over L={0,1,2}. For current level k, one artificially trained trial produces:

* k=0: (Pr(0),Pr(1),Pr(2))=(1−u,u,0).
* k=1: ((1−u)(1−f),(1−u)f,u). Here a successful innovation directly reaches 2; otherwise copying succeeds with probability f or regresses to 0.
* k=2: (0,1−f,f). Failure to faithfully reproduce 2 regresses to 1; innovation already capped at 2.

Independent child trials use exactly this distribution. The group skill frontier is the **maximum** of m=N or m=1 child levels according to the frozen mode. This maximum is a deliberately strong form of full within-group knowledge pooling with no interaction costs. No human teacher, true fidelity parameter, innovation payoff, skill use rate, cumulative technological artifact or actual lifetime data is represented.

## Independent complete probability oracles
1. Derive exact rational CDF of maximum: for j=0,1,2, P(next frontier ≤j)= (Σ_{r≤j} Pr(child=r))^m; subtract adjacent CDF to get 3-state transition row, and propagate probability row vectors exactly via Fraction.
2. Independently compute maximum of m independent trials by sequential dynamic programming over current maximum states and the full 3-category child distribution, without using powered CDF or calling oracle 1, then independently propagate with nested loops.
All 32 full 3×3 transition matrices and all 64×5 complete distributions must exactly match, remain nonnegative and normalize to 1, with no rounded numerical comparison.

## Prespecified sampling and identifiability counterexamples
1. Starting at level2, group retaining frontier2 on next step is **1−(1−f)^m**, and individual copying fidelity remains f regardless of N. Thus in full_pool larger N raises group maximum retention even if the individual's f is identical. In single_channel, group retention is exactly f regardless of nominal N. This is the Andersson/Read type group-level sampling baseline, **not** a new empirical claim about Derex2013 results.
2. At N=2 full_pool with f=1/2, level2 group maintenance =3/4. At any nominal N single_channel with f=3/4, group maintenance also =3/4. Observing group maintenance alone cannot identify per-person fidelity separately from effective sample size.
3. For starting level0 and u=0, there is no means to create higher levels and state0 is absorbing; for starting level0 and u=1/8, first step creates at most level1, and level2 can first appear at t=2 when innovations and copying opportunities allow. This is a conditional toy multistage cultural innovation path, not proof of a human ratchet.
4. For u=0 and 0<f<1, eventual complete frontier loss is certain from any initial L≤2, regardless of finite N; full_pool can make it extremely slow. Exact mean hitting times are E[T_hit0|L=1]=1/(1−f)^m and E[T_hit0|L=2]=2/(1−f)^m. This proves high short-run maintenance does not guarantee permanent cumulative culture.
5. When u>0, all three frontier states communicate (under 0<f<1). Each fixed 3-state transition matrix has a unique strictly positive stationary distribution, solved with independent exact Fraction linear elimination, with zero stationarity residual.
6. If full_pool is replaced by a single_channel, n does not affect any one-step or long-run distribution conditional on f,u,start. Consequently population size alone never determines a ratchet.
7. Every expected group maximum is a statistic of a *fully shared group knowledge pool*; individual skill, knowledge-use frequency, selection of information and learning cost are distinct estimands. No group/individual causal mechanism can be identified by group maximum alone.
8. Exact input/negative controls: invalid n, f, u, mode, start, time and malformed probability rows must raise, and no floats/bools allowed. The original Nature figure XLS was not accessed. All results explicitly labeled E1.

## Acceptance
At least 64 separately named complete-world tests, plus at least 25 distinct exact mechanism, group-vs-individual identification, nonabsorbing, stationary, protocol boundary and negative tests. Deterministic full JSON and standard-library source/test/JSON ZIP with four pinned SHA256. GitHub Actions under Python3.11 and Python3.12, independent publisher archive step and permanent main readback. Close only **CLOSED_BOUNDED_E1**, with new E2=0, E3=0; R073/PESEN v0.1 frozen. Keep the Derex2013 empirical case as **BLOCKED_SOURCE_ACCESS**; do not overwrite or imply R168 has resolved the 2014 controversy. Next original R series item R169 must be checked separately.
