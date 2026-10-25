# B independent scientific audit: R170 third-method naming-game observation ladder

Date: 2026-10-26 Asia/Singapore. Target: the append-only R170 third-method protocol frozen at commit 6bba9f855b470ecbc7fe1a8a373468083a874c0c and main scientific result at commit c6e9296ac369db35ed5fd28cde15c9d9ef1120f2.

## Independent execution

A Python 3 Fraction program was written and executed locally using undirected-edge selection, explicit speaker/hearer orientation, explicit uttered word and flip/no-flip branches. It independently constructs and propagates each full inventory-state distribution for 72 worlds over t0..t3. It does not import the main JavaScript code. Python execution produced 288 normalized snapshots, 36 stratum-time observations, all 12 aggregate class counts and all 12 unique/ambiguous/pairwise counts. The 12 aggregate records matched the main JavaScript route exactly. The first witness (path, split, nu=1/4, both-confirm versus listener-only, t1) matched O1 TV=0 and O4 TV=1/12. The out-of-grid noise perturbation matched TV=1/24. Eight monolingual-start/noiseless first-step feedback equalities passed.

Executed Python source: `research/evidence_audit/r170_b_edge_utterance_20261026.py`. Python source local SHA256 `134cfee8510606fef8f94eb3d9975f1045006bf17360444aeaa1b588d0080423`. Local full execution JSON receipt SHA256 `8cdf817c0e32cd48ea1a70dd1f9d0c5fc55022c8d355981157d0181934ab2565` (23004 bytes). A compact independent summary is archived here. The full local receipt has not been uploaded to the repository, so its digest is an execution provenance record rather than remote-archive completeness proof.

## Evidence validity checklist

* Data leakage: none in this artificial no-fit calculation; all 72 grid points are specified before the extension code, and all control comparisons are within the same graph and initial inventory.
* Baselines: equality of full rational probability laws, coarsened O1/O2/O3/O4 observation laws, and a known mutated control. There is no learned predictive baseline on empirical data.
* Held-out prediction and probability calibration: not applicable to the current E1 exercise; no E2 or E3 acceptance is earned.
* Uncertainty: the finite probability laws are exactly enumerated. They do not provide empirical confidence intervals for parameter inference from a finite sample. A real experiment would need participant/session separation and repeated independent experimental units.
* Negative controls: eight nu=0 monolingual equality checks, normalization and valid-mask invariants, and an executed nu=1/3 mutation against nu=1/4 with O4 TV=1/24.
* Scope: class counts refer to exact distributions under six known controls per fixed initial graph. A single t3 observation does not identify a control; repeated experiments would be required to estimate the law. No general arbitrary-parameter identifiability is established.

## Independence and limitations

The main JavaScript script includes two event kernels and checks 288 complete state-distribution equalities, but those kernels share a common state-update helper. The independently executed Python B route agrees with the JavaScript on all aggregate class counts and named controls. A byte-level or rational term-by-term Python-versus-JavaScript comparison of all 288 snapshots has not been performed. This is internal method-level cross-checking by the same project, not an external team's independent replication.

The original R170 result remains CLOSED_BOUNDED_E1. New E1 bounded information study=1, new E2 human forecast=0, new E3 historical validation=0. R073 and PESEN v0.1 remain frozen. No GitHub Actions triggered; no billing or free-quota assertion is made.
