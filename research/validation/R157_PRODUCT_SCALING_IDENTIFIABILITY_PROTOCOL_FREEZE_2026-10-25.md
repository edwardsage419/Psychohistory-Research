# R157 additional E1 protocol freeze: pressure-product scaling and observational nonidentifiability

Date: 2026-10-25. Baseline main HEAD before freeze: b4eea4fafe900fde476f0edfbd1e691f41d0ee66.
Parent: research/R157/R157_SCIENTIFIC_REPORT_2026-10-21.md and protocols/R157_TURCHIN2013_GOLDSTONE1991_THREE_PRESSURE_72_WORLDS_PRESCORE_FREEZE_2026-10-21.md.

## Frozen model and question
Reuse the project's exact synthetic lag system without changing any R157 parameters or original tests:
M[t+1]=(1-a)M[t]+a H;
E[t+1]=(1-b)E[t]+b M[t];
F[t+1]=(1-c)F[t]+c(1-r)E[t].
All initial states zero. Observable P[t]=M[t] E[t] F[t] is a constructed product index, never a measured risk or probability.

## Predeclared tests and acceptance
1. For every original 72-world grid H in {1/4,1/2,1}, a,b,c in {1/4,1/2}, r in {0,1/2,1}, t=0..12, derive normalized base paths with H=1,r=0 by finite convolution and verify exact factorization P[t]=H^3(1-r)K[t]. Compare 936 product cells and all 2808 state cells with original archived R157_EXACT_RESULTS.json. Exact Fraction equality required, no tolerance.
2. Construct an exact non-grid counterexample holding a=b=c=1/4: (H,r)=(1/2,0) and (1,7/8) have identical P[t] for all t>=0, while M[1] differs. Confirm at t=3,12, and with an exact general identity.
3. Negative controls: replace H^3 with H^2 in factorization (must fail in a positive world); replace 1-r with 1+r (must fail in a buffered world); claim all-zero product identifies H=0 (must fail at r=1,H>0).
4. Check t<=2 products are zero and t=3 is positive for all 48 grid worlds with r<1. Verify no external human/historical data used.
5. B audit: independent derivation using polynomial generating functions or a second implementation, plus explicit observability and confounding scope review. Same-researcher implementation independence is NOT external replication.

## Interpretation
E1 finite exact mechanism and structural nonidentifiability only. No fit, no out-of-sample scoring, no probability calibration, no E2/E3. Existing R073 and PESEN v0.1 frozen. The protocol must precede new script/results; any failed assertion stays visible. Do not modify existing frozen artifacts or shared original239 queue.
