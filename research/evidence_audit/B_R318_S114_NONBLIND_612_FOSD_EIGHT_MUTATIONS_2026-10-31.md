# B track R318 S114 independent exact audit
Date: 2026-10-31 UTC. Evidence class E1 only. This is internal NONBLIND independent implementation, not external blind replication.
Target key: (B,R318,S114_c12d3c90,FOSD_612_full_coverage_and_negative_control).

Read scope: original R318 frozen protocol and 36 valuations JSON; R318 S114 prescore protocol; R S114 generated 612 CSV and summary; recent main/market E147 and 12 open Codex PRs. No R scorer imported into B audit.

Independent route 1: research/evidence_audit/b_r318_s114_independent_fosd.js. Exact BigInt rational arithmetic, original noncanonical weighting independently expressed as odds a^2/(a^2+2(b-a)^2), and survival-tail FOSD criterion instead of R's CDF form. Actually executed on remotely fetched 50,029-byte 612-row CSV, blob a1202593194c96aa8ac5002dcc3b9d3548582a93, and 1,275-byte JSON, blob fa6d98d04aa385d48fc4745e31ef5ed4fb4d04b7. Verified 612 unique keys, 18 source identities, 117 FOSD pairs for each transform, zero actual CPT violations, two normalized negative-control violations, nine strict reversals and exact witness fractions. Source script blob 3d17632981ad555d41e00228d78d4505c6178ffa. Archived function was fetched and re-executed under V8 adapter, not native Node.

Eight archived mutations were actually executed and rejected: remove row, duplicate row, alter cpt_delta, flip FOSD, flip normalized negative-control flag, swap transform, tamper ranking aggregate, falsely promote real_E2. No silent false positives observed in this bounded mutation set.

Independent route 2: research/evidence_audit/b_r318_s114_fraction_oracle.py, SHA1 4d4cfd58bd2d9592b5274b997cadcee8f7936573, was executed with local Python standard-library Fraction and separate CDF/valuation construction. It independently recovered all aggregate counts. It does not read the remote CSV, so its agreement is a separate calculation route rather than an independent remote receipt verifier.

Scientific checks: synthetic full enumeration makes sample split, cluster bootstrap and empirical probability calibration NOT_APPLICABLE_WITH_RATIONALE. No measured human labels exist. A human prediction improvement claim is prohibited. Negative control deliberately violates FOSD after normalizing mixed-sign weights; actual frozen CPT has zero violations in the 117 FOSD comparisons per transform. Original R318 status unchanged. E2=0, E3=0, external independent replication NOT_RUN.
Open: archived Node native CLI replay; actual empirical data license and raw parsing; new preregistered E2 holdout if feasible. CI NOT_TRIGGERED; billing quota not independently verified.
