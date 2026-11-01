# R331 S127 scientific report: heterogeneous retention and declining conditional hazard
Date 2026-11-01 UTC. Status PARTIAL_E1_EXTENSION, original R331 bounded E1 acceptance unchanged.

## Freeze and source
Original R331 protocol `protocols/R331_HETEROGENEOUS_RETENTION_81_ATOMS_PRESCORE_FREEZE_2026-10-24.md`, Git blob `f25b23480d40e6bf2334777ddbe7a4b493331534`; original 81-atom source blob `7abe55e5454b9d76e8032224455470d5610d87cf`; original nine-world summary blob `30317b2e16269d89286c8a75cedb3c483b72c725`. Extension frozen before calculation at commit `200bca2798aa45245f97f7383604415d54d3ec94`. Prior S(t)>Q(t) finding known before this follow-on; this is not blind.

Original English theory sources: Ebbinghaus (1885/1913), *Memory: A Contribution to Experimental Psychology*, and Wixted & Ebbesen (1991), *On the Form of Forgetting*. This study uses only constructed finite exponential mixtures, no author human data.

## Exact design
Keep all original nine artificial worlds: three retention-rate pairs (a,b)=(1/4,1/2),(1/4,3/4),(1/2,3/4), three fast weights w=1/4,1/2,3/4. At t=0..7 compute 72 exact records:
S(t)=w*a^t+(1-w)*b^t;
conditional retention R_t=S(t+1)/S(t);
conditional forgetting hazard H_t=1-R_t;
fast component share among surviving traces W_t=w*a^t/S(t).
The single exponential matched at t=1 has constant hazard H0=1-[w*a+(1-w)*b].

## Findings
All nine artificial worlds have strictly decreasing H_t for t=0..7 and strictly decreasing fast-component share W_t. At t=0, the mixture hazard equals the homogeneous comparator exactly in all nine worlds. Later hazards fall below that comparator. All 72 hazard values are strictly between 0 and 1.

Frozen counterexample a=1/4,b=3/4,w=1/2: H0=1/2, H1=3/8, H2=3/10; fast share W0=1/2,W1=1/4,W2=1/10. A declining aggregate hazard emerges from changing mixture composition even though each component has a fixed rate. The mechanism is selection among surviving artificial traces. This result does not identify actual memory interference, cognitive retrieval failure or human forgetting.

## Reproducibility and boundaries
Primary exact BigInt JavaScript: `research/validation/r331_s127_conditional_hazard.js`. Full 72-row receipt: `research/validation/R331_S127_EXACT_72_HAZARD_ATOMS.json`, 13,960 bytes, Git blob `b74142527d87e458fe363c40e50bbc6d8c2eadba`. Actual persisted JS re-executed in V8 with exact byte equality. Each of 72 new rows looked up original archived S(t) and S(t+1), yielding 144 original-source comparisons, all equal.

Independent Python Fraction oracle: `research/evidence_audit/b_r331_s127_fraction_oracle.py`, blob `75510c805bee8eb330a37f2eb865959fce0010b2`. The exact archived Python source was executed locally in normal and -O modes; three unit tests each mode PASS, six active mutations each mode rejected. Independent Python-generated 13,960-byte JSON had exact Git blob `b74142527d87e458fe363c40e50bbc6d8c2eadba`, identical to the persisted JS receipt. Internal nonblind computational verification only. Native Node CLI NOT_RUN. External independent team NOT_RUN. No GitHub Actions launched because free quota was not independently verified.

A01 PASS_BOUNDED, A02 PASS for original artificial-source provenance, A03 PASS for exact arithmetic and local Python, A04 PASS for prespecified monotonicity and six negative controls, A05 PASS for E1-only boundaries, A06 PASS for archived source/receipt/report and pending coordination handoff. No human E2, historical E3, empirical calibration, out-of-sample prediction, or causal mechanism claim. R073 and PESEN v0.1 remain frozen.
