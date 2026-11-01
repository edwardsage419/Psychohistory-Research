# B addendum: R331 S127 exact Fraction independent audit
Date 2026-11-01 UTC. Scope: supplemental internal nonblind E1 audit; the primary B target for this run is R330 S126.

The separate Python script `b_r331_s127_fraction_oracle.py` uses Fraction and itertools to enumerate nine fixed (a,b,w) worlds and 72 time points, independently calculating S(t), S(t+1), retention, hazard, fast-share and homogeneous comparator. It imports no primary JS code. Its locally generated full 13,960-byte JSON has Git blob `b74142527d87e458fe363c40e50bbc6d8c2eadba`, equal to the persisted remote JS receipt. Script blob `75510c805bee8eb330a37f2eb865959fce0010b2` equals the executed local source byte identity.

Normal Python: 3 unittest PASS. Python -O: 3 unittest PASS. In each mode six active corruptions were rejected: removed row, duplicated row, changed hazard, changed survivor share, falsified monotonic summary, and E1 to E2 evidence promotion. The main source rechecked all 72 new rows against the original archived 81-atom source at both t and t+1, 144 matches. Prespecified W05 H0=1/2,H1=3/8,H2=3/10 and W0=1/2,W1=1/4,W2=1/10 confirmed.

No human data, no model fitting, no leakage target, no probabilistic calibration or uncertainty estimate applicable to this finite deterministic universe. No external blind replication. Native Node CLI and GitHub Actions NOT_RUN. This is an internal same-researcher mathematical verification; no E2/E3 and no change to original R331 accepted E1 status.
