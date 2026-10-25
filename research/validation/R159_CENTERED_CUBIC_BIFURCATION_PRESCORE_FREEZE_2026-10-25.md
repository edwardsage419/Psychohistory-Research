# R159 centered cubic bifurcation: precomputation protocol freeze

Date: 2026-10-25. Evidence tier: E1 only. This supplement is separate from the immutable R159 original 48-world archive and from original author equations.

## Frozen source identity and boundary
Source code `research/R159/r159_cultural_transmission_exact.py` Git blob `440b2aa3a1b8f46248af31252b0ba60b0a0fe77e`; original R159 report `research/R159/R159_SCIENTIFIC_REPORT_2026-10-21.md` blob `a28d6442617a6e9c5a9de09ba74b71df50e872df`.
Original project-authored map: `p'=(1-u)[p+h*p*(1-p)*(2*p-1)]+u/2`. Fixed parameter grid: `h in {0,1/4,1/2,1}`, `u in {0,1/10,1/4}`. The 48 original trajectories have initial `p0 in {1/4,2/5,3/5,3/4}` and seven observations. No modifications to original source, R073 or PESEN v0.1.

## Predeclared new question and exact method
Analyze all fixed points in the continuous state interval `p in [0,1]` and local stability, including regimes not observable within seven generations. Define `x=p-1/2`, derive `x'=a*x-b*x^3` with `a=(1-u)*(1+h/2)`, `b=2*(1-u)*h`. Derive the critical reset rate `u_c=h/(h+2)` for positive h. For each of 12 parameter pairs, output exact rational `a,b,a-1`, equilibrium `x_*^2` when positive, center derivative, outer derivative and regime. Verify full original 48 x 7 archive transitions without fitting or parameter changes.

## Prespecified gates
1. Exact polynomial identity for rational grid p=k/100, k=0..100, each h/u pair.
2. Exactly 12 unique h/u pairs, partition into neutral continuum, central-only and bistable; check fixed points in [0,1], derivative absolute value <=1 at stable outer equilibria and center instability for bistable worlds.
3. Exact original archive verification: 48 worlds x 7 p observations and 48 x 6 transition equations, preserving the frozen parameter labels.
4. Negative control 1: replace reset-to-half with reset-to-current-p, which should fail in applicable worlds.
5. Negative control 2: replace majority-of-three with unbiased copying, which should fail in applicable worlds.
6. Explicit evidence limits: E1 synthetic, no original-author reproduction, no E2/E3 claim, no externally independent replication.

## Independent B audit design
B will use a separate JavaScript BigInt rational enumerator of the eight independent three-demonstrator outcomes and check archived exact frequencies and next-step predictions, plus the two mutated mechanisms. B will not call the main polynomial function. If implementation access or file integrity blocks a gate, report a failure or blocker; do not adjust tolerances after seeing results.

## A data scout design
Check a newly located original human cultural-transmission source by publisher DOI, original file availability, schema, participant/generation/chain structure, license, prior-source overlap, and suitability for independent held-out scoring. No post-hoc mapping to R073 dyadic prediction or changing its frozen protocol.

## Operational safeguards
Use distinct new files in research/validation, research/data_scout, research/evidence_audit. Before branch mutation reread HEAD and destination absence; create new Git objects and advance main only with expected-HEAD lease, without force. Do not run GitHub Actions or paid services. Record local checks separately from CI.
