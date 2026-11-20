# C034 addendum: perfectly correlated offsets under clipping

Date: 2026-11-20. Status: SYNTHETIC_ANALYTIC_CANDIDATE. Independent acceptance NOT_RUN. Scope: decision hub dispatch under explicit calibration dependence.

## Decision gap and relation to prior work

The prior C034 exact clipped-offset analysis assumes c1 and c2 can vary independently in [-0.30,0.30] and obtains D in [-0.04,0.09]. This supplement tests a different *joint feasible set*: c1=c2=c, c in [-0.30,0.30]. This equality is a hypothetical assumption, not an empirical finding. Nominal scores A=(0.8,0.4), B=(0.5,0.8), first-objective weight w in [0.60,0.65], and T(x)=min(1,max(0,x)) are unchanged.

## Exact calculation

Define D(w,c)=w[T(0.8+c)-T(0.5+c)]+(1-w)[T(0.4+c)-T(0.8+c)].

For -0.30<=c<=0.20, neither score difference is clipped: D=0.7w-0.4.

For 0.20<=c<=0.30, D=w(0.5-c)+(1-w)(c-0.6)=1.1w-0.6+(1-2w)c.

Because w>=0.60, D decreases with c on the second segment. Both segments increase with w throughout the specified domain. Consequently the global minimum is at w=0.60,c=0.30: D=0.5(0.60)-0.30=0. The global maximum is at w=0.65,c<=0.20: D=0.7(0.65)-0.4=0.055. By continuity, **the exact attainable range is [0,0.055]**. A is weakly preferred in every permitted realization, with a feasible tie. Universal *strict* preference is not certified.

Under independent offsets the attainable range was [-0.04,0.09]. Imposing c1=c2 eliminates the negative witness, but it would be unsafe to impose this equality without source evidence.

## Sharp threshold in a generalized weight interval

For any w in [0,1] with the same common-offset range, the minimum over c is min(0.7w-0.4,0.5w-0.3), and the maximum is 0.7w-0.4 for w>=0.5; for w<=0.5 the second segment increases with c and the maximum is max(0.7w-0.4,0.5w-0.3). Thus for the target weight interval [p,q] subset [0.5,1], the lower bound is min(0.7p-0.4,0.5p-0.3) and the upper bound is 0.7q-0.4. In this range a universal strict A certificate requires p>0.60. At p=0.60 a tie is attainable.

## Minimal checks and baseline

At w=0.60,c=0.30: A transformed scores (1.0,0.7), B transformed scores (0.8,1.0), hence D=0.60(0.2)+0.40(-0.3)=0.

At w=0.65,c=0: nominal difference D=0.65(0.3)+0.35(-0.4)=0.055.

The simple nominal baseline c=0 yields D in [0.02,0.055], and misses the tie. An independent-offset baseline produces a negative lower bound that is impossible under this equality constraint.

## Dispatch, failure and acceptance

Use a correlated-offset certificate only when the source establishes the common offset across *both objectives* on the same cardinal scale. Shared offsets within each objective alone do not establish c1=c2. If dependency is unknown, use the larger admissible set and retain uncertainty. Clipping-aware optimization is required. Check hard constraints before utility calculations; preserve user-owned weights.

Independent acceptance candidates: verify both endpoints and witnesses; both clipping breakpoints; equality at w=0.60,c=0.30; perturb w above/below 0.60; compare independent and common-offset feasible sets; ensure a dependent model never widens the attainable range; check UNKNOWN when dependence is unverified; compare a brute-force grid with analytic extrema; test change of clipping bounds; reject claims of probability or empirical calibration.

Evidence: exact algebra on a synthetic case, not a reproduction of an external paper. No empirical evidence establishes common offsets; no formal independent implementation, real-data verification or scientific acceptance is claimed. Independent acceptance track owns isolation tests. Data track owns calibration dependency evidence. Version integration requires owner authorization. R073, PESEN v0.1 and frozen protocols remain unchanged.
