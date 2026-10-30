# R283 S79 finite sample Cochran Q tail gate, prescore freeze

Date UTC: 2026-10-30. Track: r. Baseline main HEAD: 548a7d913d39747e9f344394c93b3da9c3163324.
Target key: (r,R283,original-freeze-310b1343+S79-v1,finite-Q-tail-and-zero-diagnostic).
Prior results read: R283 original protocol, report, exact results, acceptance JSON, Python source. This is a NONBLIND internal exploratory extension; the original R283 E1 closure and its protocol remain unchanged.

## Frozen question and scope
For the three existing artificial DGPs HOMOGENEOUS, BALANCED_HETEROGENEITY, ONE_REVERSAL, quantify the exact finite sample distribution of the original oracle-weight Cochran Q and the probability of a fixed high-heterogeneity alert Q >= 6. Include exact P(Q=0), P(Q>=6), E[Q], minimum and maximum attainable Q, and full rational PMF by regime. All 64 ordered T1C1T2C2T3C3 sources per regime are included, even zero-alert sources. The threshold 6 is fixed here before calculating S79 results. It is a descriptive diagnostic threshold, with no claim of a nominal statistical significance level or real-world Type I error control. Do not change the original DGP, study weights, source probability or Q definition. Compare to the original R283 expected Q values (2, 10/3, 34/9) as fixed anchors.

## Independent checks and stop rules
R route: enumerate all 64 six-bit sources per regime using exact rational arithmetic, record source mass and Q, aggregate PMF. B route: independently enumerate 27 triples of study-level d in {-1,0,1}, with exact marginal probabilities P(d=1)=pT(1-pC), P(d=-1)=(1-pT)pC, P(d=0)=pTpC+(1-pT)(1-pC); compute the same PMF without importing R route or enumerating six-bit strings. Compare all PMF supports and masses, P(Q=0), P(Q>=6), E[Q], min/max. Each regime's mass must be 1; missing or duplicate sources must fail. Include negative controls by corrupting a mass and removing a source; preserve failure evidence. If independent checks differ, mark FAIL and do not publish a success claim.

## Evidence limits
E1 artificial only. No actual literature search, real meta-analysis, real E2/E3 prediction, chi-square approximation validation or external-team replication. The oracle variances use inaccessible true DGP parameters in real one-observation-per-arm studies. R073 model and score and PESEN v0.1 remain FROZEN. No Actions dispatch without verified zero incremental cost. Source and result files must be additive only.
