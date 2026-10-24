# R124 independent endpoint covariance scientific report

Date 2026-10-24. Original239 04-015 Homophily Models. Reuse unchanged R124, including 2001 McPherson et al. baseline homophily, Newman (2003) categorical assortativity, and 2009 Kossinets and Watts abstract-only empirical boundary.

## Frozen experiment and primary sources

Protocol frozen before execution at `research/validation/R124_THIRD_METHOD_ENDPOINT_COVARIANCE_PROTOCOL_FREEZE_2026-10-24.md`. Primary non-Chinese sources: McPherson, Smith-Lovin and Cook (2001), DOI 10.1146/annurev.soc.27.1.415; Newman (2003), DOI 10.1103/PhysRevE.67.026126; Kossinets and Watts (2009), DOI 10.1086/599247. The original R124 project report and tests were strictly reused. Original source/test/report Git blobs verified in CI: `382859d6dcf55201e316a12da276d0ab04514842`, `652d43c34852e08bccdd0b083d2119c0c06d5ea3`, `99bc82d03045ec90f2719272280b1ef10d7d738f`.

## Independent method and complete constructed data

For each undirected edge, construct two oriented endpoint observations X,Y, encoding category A as 1 and B as 0. Compute exact binary Pearson r = [E(XY) - E(X)E(Y)]/[E(X²) - E(X)²] with Fraction arithmetic, using neither original mixing matrix nor original degree-stub tally. For undirected edges the two oriented marginal distributions agree. When there are no edges the statistic is undefined for empty domain; when all active endpoints have the same category the variance denominator is zero and r is undefined. Both are recorded explicitly.

All simple undirected labeled graphs with n=2..4 and both A/B categories were enumerated: 4, 48, 896 cases, total **948**. **926** have at least one edge, **22** have none. Among 926 nonempty cases, **74** have a zero Pearson denominator. All 926 nonempty cases agree exactly with the unchanged original R124 Newman-matrix calculation, including undefined results. The 948 rows are archived in `research/validation/R124_ENDPOINT_COVARIANCE_948_CONSTRUCTED_GRAPHS_2026-10-24.csv`, Git blob `2ace3cf66e941fae07f19619fa3c35ebac7a1615`, SHA256 `4901466eb6215bdd90c9f9e70057be49a1d9a5373df68db431c82a40b8416b74`.

Six fixed controls: AAA/BBB disconnected triangles r=1; all-cross K3,3 r=-1; five-A-one-B K6 r=-1/5 despite raw same-edge fraction 2/3; A-A edge with isolated B has undefined r; empty graph has no metric; identical observed triangles have distinct population-pair baseline 2/5 and focal-opportunity baseline 1. Wrong source blob and altered raw CSV are rejected.

## CI and scientific scope

Workflow `.github/workflows/r124-independent-endpoint-covariance-audit.yml`, run [40091492475](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40091492475), commit `e2141458a0c9dda629517a961418343636d44736`, **completed / success**. Python 3.11 job `120864915211` and 3.12 job `120864915347` both succeeded. Actual job logs contain `R124_AUDIT_PASS total=948 nonempty=926 empty=22 undefined_nonempty=74 controls=6 csv_sha256=4901466eb6215bdd90c9f9e70057be49a1d9a5373df68db431c82a40b8416b74 verify=True` and `Ran 56 tests ... OK` on both versions.

**PASS_BOUNDED_INTERNAL_ENDPOINT_COVARIANCE_E1**. The outcome is a deterministic identity of three internal finite mathematical implementations. It is not a real-network empirical effect, does not estimate preference for similar others, and does not identify selection, opportunity or influence mechanisms from cross-sectional links. No human E2 held-out predictions, independent human social network sample, historical E3, real longitudinal identification, calibration or external research-team replication. R073 and PESEN v0.1 remain frozen. Free public standard Ubuntu runner; no new fees.
