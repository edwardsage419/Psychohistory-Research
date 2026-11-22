# Joint causal transport intervals with a dependent feasible set

Date: 2026-11-23. Track: decision model learning. Status: synthetic mathematical counterexample, pending independent acceptance.

## Purpose and provenance
This addendum qualifies the existing `CAUSAL_TRANSPORT_JOINT_MODIFIER_EFFECT_INTERVAL_2026-11-23.md` method card. Its rectangular parameter bounds can be conservative if target composition and subgroup effects are constrained jointly. The algebra here is a new illustrative construction, not an empirical finding or a claim attributed to Bareinboim and Pearl (2016), *Causal inference and the data-fusion problem*, PNAS, DOI 10.1073/pnas.1510507113. Transport identification, effect modification and outcome comparability remain separate prerequisites.

## Inputs and exact calculation
Use D=q*d1+(1-q)*d0 with q in [2/5,3/5], d1 in [3/20,1/4], d0 in [-3/20,-1/20]. The prior rectangular outer bounds are [-3/100,13/100], spanning zero.

Now posit the *synthetic joint constraint* d1=9/20-q/2. This is an assumed perfect negative dependence, **not** supported by real evidence. It respects the same marginal intervals. Keep d0 independently free in [-3/20,-1/20]. For each q, D increases in d0 because 1-q>0. Hence the lower envelope is
D_low(q) = (3/5)*q - q^2/2 - 3/20.
Its derivative is 3/5-q, nonnegative over [2/5,3/5], so the minimum is D_low(2/5)=1/100.

The upper envelope is
D_high(q) = q/2-q^2/2-1/20.
Its maximum occurs at q=1/2 and equals 3/40.

The *sharp* range over this constrained feasible set is therefore [1/100,3/40] = [+0.010,+0.075]. The rectangular outer bounds [-0.030,+0.130] remain valid but are not sharp. The conclusion changes from unknown sign to positive sign only under the additional joint restriction.

## Baseline and failure cases
Baseline: use eight corners of the marginal rectangle, preserving a safe outer bound without dependence evidence. Enhanced calculation: optimize over a justified joint feasible set. Do not infer the dependence restriction from a convenient narrative, a single observation, or the desired decision. If the restriction is estimated, include its uncertainty; otherwise a positive sign certificate may be false. Statistical interval coverage, causal identification, and applicability to a person are still unresolved. The value of D alone does not establish net utility once costs, harms, or user preferences are included.

## Acceptance preparation
1. Independently verify the derivative signs and endpoint/interior extrema with rational arithmetic or symbolic polynomial optimization.
2. Verify [0.010,0.075] is contained in [-0.030,0.130] and that d1 stays inside [0.15,0.25].
3. Remove the joint constraint and recover the rectangular outer bound.
4. Perturb the joint constraint to include an uncertainty band and find the threshold at which the lower bound crosses zero.
5. Ensure the interface distinguishes an evidence-backed joint feasible set from a hypothetical sensitivity scenario.

Recommendation: when dependence information is absent, retain rectangular conservative bounds and report sign uncertainty. Allow constrained-set analysis only with explicit, traceable justification. Data track owns any real dependence evidence. Independent acceptance track owns exact extrema and adversarial tests. Engineering integration requires separate authorization.

Evidence: algebraic synthetic derivation only. No real-data validation, scientific acceptance, paid APIs, CI, or private records. R073, PESEN v0.1 and frozen protocols unchanged.
