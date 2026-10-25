# R157 third-method scientific report: pressure-product scaling and parameter nonidentifiability

Date: 2026-10-25. Research grade: **E1 internal bounded exact computation**. Protocol frozen at commit `408fe2301031361a99e47e90bd17b77bea06a94a`. Original R157 report and acceptance remain unchanged.

## Frozen system and exact identity
Original synthetic zero-initial-state model: M[t+1]=(1-a)M[t]+aH; E[t+1]=(1-b)E[t]+bM[t]; F[t+1]=(1-c)F[t]+c(1-r)E[t]; P[t]=M[t]E[t]F[t].

By linearity and zero initial conditions, for fixed (a,b,c), M[t]=H m[t], E[t]=H e[t], F[t]=H(1-r)f[t], where m,e,f are the normalized H=1,r=0 paths. Hence for **every nonnegative integer t**,

**P[t] = H^3 (1-r) K[t;a,b,c]**, where K[t]=m[t]e[t]f[t].

This identity is exact for the synthetic model. It implies a structural confounding ridge for observing the product alone. Distinct pairs (H,r) sharing H^3(1-r) produce the same entire P time series when lag parameters are fixed. Observing separate M, E, F components can break this particular ambiguity.

## Independent archived replay
Main third-method script `r157_product_scaling_convolution.js` uses finite convolution and exact BigInt rational arithmetic. It reads the existing original R157_EXACT_RESULTS.json (Git blob `27621615444dcb76489232236dfa528fabd2d3c6`), which was produced before this addendum. It independently reconstructs 8 normalized lag triples and compares all 72 original worlds at 13 time points.

Results: **2,808 exact state cells matched**, **936 exact product cells matched**, **216 early zero-product checks**, **48 positive time-three checks**. No floating-point tolerance. All three frozen negative controls were rejected: incorrect H squared scaling, incorrect buffer sign, and inferring zero H from zero P.

## Explicit counterexample
With a=b=c=1/4, pair A (H=1/2,r=0) and pair B (H=1,r=7/8) share H^3(1-r)=1/8. Their P[t] values coincide at every t, including P[3]=185/1048576 and P[12]=2345008149288796188925/37778931862957161709568. Yet M[1] is 1/8 in A and 1/4 in B. The second pair extends beyond the original discrete r grid; it is an analytical parameter counterexample within the original model's admissible [0,1] domain.

## Limitations and acceptance
The conclusion concerns the constructed pressure-product index. It does **not** identify real mass, elite, or fiscal pressure; it does not predict unrest; and it does not reproduce Turchin's historical equations or calibrate a real political stress index. No human E2 or historical E3 observation is introduced. No external replication, calibration, sample split, or predictive baseline is claimed. Existing R073 and PESEN v0.1 freeze remains unchanged.

Source: Peter Turchin (2013), *Modeling Social Pressures Toward Political Instability*, DOI 10.21237/C7clio4221333. This report studies the project-defined synthetic lag model, not the source's historical estimation.

**Acceptance: PASS_BOUNDED_LOCAL_INTERNAL_E1**, additive to the original R157 finite acceptance; original239 itemwise primary evidence queue is unchanged.
