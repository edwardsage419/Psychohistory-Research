# C034: joint weight and score uncertainty in two-objective choice

Date: 2026-11-20 Asia/Singapore. Status: SYNTHETIC_ANALYTIC_CANDIDATE. Independent acceptance NOT_RUN. Scope: personal decision workbench, weight-change thresholds and measurement-gap prioritization. This extends C004 E1/E3 without modifying C004, C028–C033, R073, PESEN v0.1 or frozen protocols.

## Decision question and inputs

After confirmed hard-constraint filtering (C028), can option A be certified strictly preferable to B when the decision-maker's first-objective weight is only known to lie in [p,q], and both options' objective scores have bounded errors? Both objective scores are higher-is-better, commensurable cardinal numbers on a declared common scale. The second-objective weight is 1-w, with 0<=p<=q<=1. Score uncertainty is epistemic, not probabilistic.

Let nominal A=(0.8,0.4), B=(0.5,0.8), matching C004 E1. Each of four score cells can independently vary within nominal ±e, e>=0. These are synthetic scores, with no personal calibration. Define U_w(a)=w x_1(a)+(1-w)x_2(a), and D(w)=U_w(A)-U_w(B).

## Derivation and exact certificate

The nominal difference is D_0(w)=0.7w-0.4. Because each score cell has an independent symmetric ±e range, the first-objective difference is [0.3-2e,0.3+2e] and the second-objective difference is [-0.4-2e,-0.4+2e]. For any fixed w in [0,1], D(w) lies exactly in [0.7w-0.4-2e,0.7w-0.4+2e]. The same corner assignment simultaneously attains each bound for all w. Thus over w in [p,q]:

min D = 0.7p-0.4-2e; max D = 0.7q-0.4+2e.

A is strictly preferred to B in EVERY allowed joint realization iff 0.7p-0.4-2e>0. B is strictly preferred in EVERY realization iff 0.7q-0.4+2e<0. Otherwise the evidence permits a tie or a reversal, so the system reports UNRESOLVED for strict universal preference. Equality yields a feasible tie and cannot certify strict superiority. This is a necessary-and-sufficient statement for the stated rectangular uncertainty set, not a general multiattribute theorem.

## Minimal examples and exact boundary

Case 1: w in [0.60,0.65], e=0.005. min D=0.42-0.4-0.01=0.01; max D=0.455-0.4+0.01=0.065. A is universally strictly preferred within this artificial set.

Case 2: same weights, e=0.01. min D=0, so strict preference cannot be certified. A feasible witness for the tie is w=0.60, A=(0.79,0.39), B=(0.51,0.81), giving U(A)=0.63 and U(B)=0.63. For e>0.01, the same adverse corner at w=0.60 makes B better. Thus e<0.01 is an exact sharp threshold for this weight interval.

Case 3: w in [0.55,0.65], even e=0 gives min D=-0.015 and max D=0.055. Better measurement of scores alone cannot establish universal preference: the elicited weight interval straddles 4/7. A decision-maker may revise or confirm their weight bounds, but the system cannot change them automatically.

## Baselines, information gaps and acceptance

Baseline 1: nominal point scores at w=0.625 give D=0.0375 and rank A; this does not certify robust preference under arbitrary wider weight or score intervals. Baseline 2: Pareto comparison leaves A and B incomparable because each excels on one objective. A useful information request must specify which uncertainty prevents a certificate. At [0.60,0.65], the score error radius needs to be below 0.01; at [0.55,0.65], reducing e alone cannot suffice. These thresholds are mathematical conditions, not promises that measurement can attain them.

Independent acceptance properties: (1) exact p/q extrema; (2) e=0 reduces to C004 E1; (3) strict equality remains UNRESOLVED; (4) score-error expansion cannot create a new universal certificate; (5) widening [p,q] cannot create a new universal certificate; (6) witness tie at e=0.01; (7) B symmetric certificate; (8) unknown score bounds return UNKNOWN, not e=0; (9) C028 REJECT cannot be reinstated by utility; (10) known cross-cell dependence must use a joint feasible set instead of rectangular corners.

Failure and evidence boundaries: additive utility requires user-confirmed comparability, cardinal scaling, compensation and weight semantics; score uncertainty may be asymmetric or dependent; feasibility can be unresolved; time horizons and units may differ; preferences may change. No elicitation, human data, software tests, independent replication, empirical calibration or scientific acceptance was performed. This is a project-local algebraic derivation with a reproducible synthetic witness, not a reproduction of Keeney (1971) or Greco et al. (2008). C004 lists their original bibliographic sources and reading limitations. Model track recommends a candidate interface with weight interval, per-score bounds, exact comparison certificate, reversal witness and requested clarification. Independent acceptance track owns separate implementation and holdout tests; data track owns provenance of real score intervals. Formal development requires separate owner authorization.
