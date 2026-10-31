# B track: R314 S110 independent nonblind exact oracle and mutation audit

Date: 2026-10-31 UTC. Target key: (B,R314,S110_frozen_c1708f29,BA_uniform_TV_observation_coarsening). Baseline main `6eeb7b2f76cdd3992bdab24bea7c8f0a896dba8c`. Original frozen R314 data were read. Independent checker does not import the R S110 generator.

## Evidence and methods
* Main R script: `research/validation/r314_s110_exact.py` (Git blob `6956f687f13182c87a8fc29f324ad2527613c07a`).
* Independent B script: `research/evidence_audit/b_r314_s110_nonblind_exact_oracle.py` (Git blob `efc5f39680d3bbff6da22e4fc51079d8733ab649`).
* Exact 44-row path CSV blob `0ed3ed60fe409cae514d96099f050ded497eb686`; 12-observation JSON blob `6e873ed38a1a8c62389420af7ecb0d529ab2cefb`.
* B oracle derives the second-arrival target degree algebraically: `d_j+1{j=i}` for old seed nodes, 1 for first new node. Independently reconstructs final labeled degree vectors, path edges and BA/Uniform probabilities. 44/44 path rows and 12/12 summary rows agree exactly.
* Remote original R314 54 conditional source atoms rechecked with independent JavaScript integer cross-products, edge lists, target degrees and denominators: 54/54 PASS. Remote original 44 path probabilities and edges: 44/44 PASS. These source checks are nonblind and do not replace the original R314 CI.

## Mutation controls and actual executions
Local Python 3.13.5 ordinary and `-O` both executed checker on the same persisted CSV/JSON byte contents. Eight deliberate changes rejected in **each** mode: duplicate path, missing path, BA probability, uniform probability, labeled degrees, sorted-degree observation, TV summary, and false E2 grade. Total 16 rejection executions. Positive unmodified control PASS in both modes. Explicit ValueError guards remain active under `-O`.

## Scientific evidence gate
Data leakage: no empirical training/holdout is used, so no empirical leakage claim can be tested. Baseline: uniform attachment fixed in pre-score protocol; all paths scored under both models. Out-of-sample prediction and probability calibration: NOT_RUN on humans. Independence: R and B programs use different mathematical constructions but share protocol and observed output; **internal nonblind**, external independent replication NOT_RUN. Uncertainty: exact enumerated finite distribution, no sampling CI. Negative controls: K3 first-arrival TV=0; eight mutations rejected. Claims limited to three artificial seeds, two arrivals, equal-prior 0-1 discrimination. E1 only, E2=0, E3=0. Original R314 acceptance unchanged, S110 PARTIAL_E1_EXTENSION.

No Actions dispatched, no billing or free-minute balance independently checked. Original R314 historical CI success cannot be represented as new S110 CI success.
