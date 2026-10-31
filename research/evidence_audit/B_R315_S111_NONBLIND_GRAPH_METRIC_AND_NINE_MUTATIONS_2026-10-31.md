# B track R315 S111: independent nonblind graph metric and probability audit

Date: 2026-10-31 UTC. Target key: (B,R315,S111_ec4fb603,independent_event_graph_BFS_and_nine_mutations). Frozen R protocol commit `ec4fb603e3dccb1f35e8cf6b9d31f0c6e1ae5c40`. The B route was implemented after reading the frozen R315 original model and after seeing the S111 R result, so it is explicitly **NONBLIND**. Same agent and execution context; not external independent replication.

## Read scope and methods
Read original R315 finite protocol (blob `8d37595d39fa15c8c9d0915bbabac0754b83ff2b`), original 180-path JSON (blob `5abbcdbf01e8b31e54671e83d033ab0f1985bd78`), 210-row original source CSV (blob `29f2774cfd56ad4ebd65beca9980900e250675af`), original report and acceptance, S111 frozen protocol and R machine result. Original239 v7.8 crosswalk and 154-row pending queue were checked unchanged. Existing original R315 independent auditor already used Floyd-Warshall, so this new B route instead rebuilds every rewiring event and checks each final graph using independent BFS plus BigInt rational arithmetic. It does not import the R S111 scoring script.

B independently checked all 180 original path action pairs and exact conditional branch probabilities, final labeled graph edges, 180 recomputed clustering and shortest-path metrics, six p-specific world summaries, 10 three-class classification cells and all probability masses. Every cell agreed exactly with the frozen R result. Original CSV 210 source rows were fetched and counted, but original R315 source audit CLI was not rerun in this round.

## Real negative controls
Nine nonempty injected corruptions were actually passed to the direct JS audit function, and all nine were rejected: duplicate path, omitted path, corrupted probability, corrupted clustering, corrupted distance, corrupted component count, corrupted final graph, false E2 source scope and corrupted optimal classification accuracy. Each rejection raised a concrete error; the test was not satisfied by a no-op mutation.

A third local Python 3 interpreter route independently reconstructed the two-step graph events, calculated exact Fraction graph metrics via BFS, and agreed on all 10 classification cells and six expected-metric worlds. Local script file `/mnt/data/r315_s111_local_crosscheck.py` was executed with exit 0. A reproducible equivalent script was archived at `research/evidence_audit/r315_s111_local_fraction_third_route.py`, but the exact archived copy's CLI was not rerun in a clean checkout. The JS audit direct function executed; its archived Node CLI also remains NOT_RUN.

## Retained engineering failure
The first uploaded JS audit script incorrectly escaped the NUL separator for the Git blob SHA1 calculation. A subsequent read-back exposed the issue before any native CLI replay claim. Commit `1567e645c82161002a30317e6430f57a08e0530b` corrected the code to append `Buffer.from([0])` explicitly. The original faulty commit `09ce9bc70b2a7e1c9b168781330c7fc268dc0bad` remains in Git history. This is a genuine development defect and the archived CLI has not yet been independently executed.

## Scientific scope and open gates
E1 mathematical checks PASS within the fixed tiny model; new S111 acceptance PARTIAL_E1_EXTENSION. Data leakage and temporal holdout do not apply to exhaustive deterministic artificial enumeration; the risk of post hoc model selection is controlled by the prescore freeze, and the B audit is nonblind. No real-person sample, no empirical probability calibration, no uncertainty from sampling, no out-of-sample human test, no external independent team. R073 and PESEN v0.1 unchanged. E2=0, E3=0. CI NOT_RUN. No paid operations or Actions dispatch. Actual account billing status UNKNOWN.

Next: in a clean checkout run the exact three archived CLI commands listed in the R report and check remote blob identity, preserve stdout/stderr and exit codes, and perform a distinct original-source 210-row audit only if it closes a new recorded gap. Never reinterpret program execution as full scientific acceptance.
