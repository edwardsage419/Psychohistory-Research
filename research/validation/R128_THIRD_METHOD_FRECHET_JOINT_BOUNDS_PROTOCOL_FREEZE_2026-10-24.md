# R128 third-method Frechet joint-success bounds: prospective protocol freeze

Date: 2026-10-24. State: **FROZEN_BEFORE_NEW_COMPUTATION**. Original239 05-004. Reuse existing R128 unchanged; R127 05-003 still has earlier CI and protocol-archive blockers, so this is a parallel preparation of the next item, not a queue decrement.

## Prior work and primary-source boundary

Existing R128 original source Git blob `4695fb1d03fc9e004f91e993907e9b165f90cc52`, original 70-test bounded acceptance and Skyrms (2004) Cambridge University Press chapter 1 https://assets.cambridge.org/052182/6519/sample/0521826519ws.pdf . The original two-person stag/hare row payoffs are (4,0) for stag and 3 regardless of partner for hare. R128's all-or-nothing n-person extension is project-created; existing R128 already checked iid `p^(n-1)` and three example joint distributions for n=3, p=4/5. This protocol adds a different exact constructive audit of dependence bounds for all n=2..8; it must not be attributed to the original book's empirical study.

## Falsifiable exact finite tests

For n in 2..8, let k=n-1 other players, each with identical marginal stag probability p in the frozen grid `{0,1/4,1/2,3/4,4/5,1}`. Without assuming independence, joint success Q=P(all k other players choose stag) obeys the sharp Frechet bounds
`L=max(0,k*p-(k-1)) <= Q <= U=p`.
There are exactly 42 n,p conditions. For each condition, use an integer uniform sample space of D atoms where D is the denominator of p in lowest terms.

Construct U using identical success sets of size D*p for all k agents. Construct L using cyclic consecutive failure sets: each agent j fails on the `D*(1-p)` atoms indexed `(j*F+t) mod D`, for `t=0,...,F-1`, with F=D*(1-p). Enumerate all D atoms, calculate each player's success marginal and joint success count, and require exact equality with both sharp bounds. No calls to original R128 functions may be used for constructing these laws.

Compare the expected stag payoff `4Q` with hare payoff 3. Classify `S` only if 4Q>3, `H` only if 4Q<3, and `TIE` otherwise. Classify the decision as **identified** if every Q in [L,U] implies the same choice (including exact tie only when L=U=3/4); otherwise **ambiguous**. Require the independently calculated iid `p^k` to lie in [L,U] for every condition. Freeze two diagnostic examples: n=3,p=4/5 gives L=3/5 and U=4/5 with H at L and S at U; n=2,p=4/5 gives L=U=4/5 and S at both. Also require n=3,p=3/4 to give L=1/2 and U=3/4 (H to TIE).

Tamper controls: reject one altered upper joint count and one altered lower marginal count. Archive complete machine-readable 42-case data, deterministic replay source, scientific report and internal audit note. Explicitly report counts of ambiguous cases, exact ties, negative controls and exceptions. Any mismatch fails. No adjustment to the p grid, n range, construction or pass criteria after execution.

## Evidence and operations

E1 synthetic finite exact construction only; no E2 person-level prediction, E3 historical validation, external team replication or real trust estimate. Original R128 code and all R073/PESEN v0.1 files remain frozen. Use existing local compute, no paid API or paid CI. A GitHub Actions run is optional and may be omitted if costs or visibility cannot be verified; absence of CI blocks any claim of new CI-backed formal acceptance.
