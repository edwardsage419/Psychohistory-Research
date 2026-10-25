# R155 third method scientific report: Bass initial-sales jet structural identification

Date: 2026-10-25 UTC+08. Model: P1/06-013 Bass diffusion. **Status: PASS_BOUNDED_INTERNAL_EXACT_E1**. Original R155 CLOSED_BOUNDED_E1 remains unchanged. This is a new mathematical mechanism audit, not a new real-data fit.

## Frozen inputs and execution
Freeze protocol: [R155 initial-jet freeze](R155_INITIAL_JET_IDENTIFICATION_PROTOCOL_FREEZE_2026-10-25.md), commit `d19dc9a92ff2b099671c03d07c1ef974d0bf5a8c`. Read original R155 code blob `60a296dfdb870c2a49994217d155d0a0387e7e20`, original report and formal acceptance. Exact Fraction implementation: [r155_initial_jet_exact.py](r155_initial_jet_exact.py). [All 75 rational rows](R155_INITIAL_JET_IDENTIFICATION_EXACT_RECEIPT_2026-10-25.json). This is the previously frozen grid of five innovation rates, five imitation rates and three market sizes.

## Derivation
For Bass first-adopter share `F`, `F'=(p+qF)(1-F)`, `F(0)=0`. Let `S=mF'` be instantaneous first-purchase sales. The three initial Taylor-jet components are exactly:

* `S0=mp`
* `S1=mp(q-p)`
* `S2=mp[(q-p)^2-2pq]`

When `p>0`, the ratios `d=S1/S0=q-p` and `h=[d^2-S2/S0]/2=pq` determine `p` as the unique positive root of `p^2+d*p-h=0`. Then `q=p+d`, `m=S0/p`. When `q=0`, the boundary solution is `p=-d`, `q=0`. When `p=0`, sales and every initial derivative vanish in this unseeded model; `q` and `m` cannot be recovered.

## Actual exact results
* 75 synthetic worlds enumerated, with 60 `p>0` and 15 `p=0`.
* 75 exact rows checked; 60 positive-p inverse identities passed.
* All 60 positive-p worlds have distinct three-component jets. The 15 zero-p worlds form one indistinguishable class. Total: **61 exact equivalence classes**, with collision size 15.
* The two-component jets `(S0,S1)` also have 61 equivalence classes **on this finite grid**; their only collision is the same 15 zero-p worlds. This finite-grid observation does not establish identification in the unrestricted parameter space.
* An explicit off-grid two-jet counterexample: `(p,q,m)=(1/50,2/5,1000)` and `(1/100,39/100,2000)` both give `S0=20`, `S1=38/5`, but their third components differ: `321/125` versus `683/250`. Thus two initial sales derivatives are insufficient in the continuous parameter space.

## Independent method and negative controls
B's independent Taylor coefficient-matching implementation uses `F=a1*t+a2*t^2+a3*t^3+...` with `a1=p`, `2a2=(q-p)a1`, `3a3=(q-p)a2-q*a1^2`. All 75 rational rows match the main method, with zero discrepancies; 60 inverse identities and 15 zero-p blocks are independently checked. Removing the nonlinear term `-qF^2` changes `S2` in all **48** grid worlds where both `p` and `q` are positive. B report: [independent scientific audit](../evidence_audit/B_R155_INDEPENDENT_TAYLOR_JET_SCIENTIFIC_AUDIT_2026-10-25.md).

## Scientific limits
Exact continuous-time derivatives at a known adoption origin are idealized observables. Annual shipment counts, sampling error, uncertain time origin, product replacement, multiple purchases, changing addressable market, and finite-difference instability are outside this proof. The original 1969 Bass paper's eleven annual consumer-durable series have not been obtained or refitted. A historical shipments series is not automatically a first-purchase series. This is **E1 internal exact mathematics**, E2=0, E3=0, external independent research-group replication=0. No claim of sample-out prediction or probability calibration. R073 and PESEN v0.1 remain frozen.

## Archive and CI
The original R155 frozen experiment, published-table arithmetic and historical CI receipts are retained. These new scripts were executed locally with Python standard library. No new GitHub Actions were intentionally triggered; new remote CI status is NOT_RUN unless later verified otherwise. No paid data or computation was used. The shared original239 v7.8 crosswalk and 154-item pending scientific queue were read and left unchanged.
