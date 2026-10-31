# R317 S113: temporal contact observation coarsening, finite exact E1

Date: 2026-10-31 UTC. Track r. Target key (r,R317,original_2026-10-24_plus_S113_v1,temporal_observation_loss). Prescore freeze: research/validation/R317_S113_TEMPORAL_OBSERVATION_COARSENING_PRESCORE_FREEZE_2026-10-31.md, committed before all S113 score computations in commit d01a96964c05e987a46f969f2f8bbe36d707c56b. Original R317 acceptance remains PASS_BOUNDED_E1_ONLY for its own original finite claim, without promotion of S113.

## Frozen population, target and provenance

Exactly 27 lexicographic three-contact schedules on three labeled nodes, exactly 162 ordered distinct origin-target evaluations. The target is existence of a strictly time-respecting message path. Equal weight is assigned to each artificial schedule and all six directed origin-target pairs. This is a finite enumerated hypothetical population, not a sample from human communication. Original 81 contact source rows independently rebuilt byte-identical to Git blob 926c1fee6a473da6bbedb9746cf109f5a3a3eb16. The original R317 81 origin outcomes Git blob af19d64d8132f351861fecb074bcd3aae1e261c9 was read through the GitHub connector and separately checked across all 81 earliest-arrival vectors, static and temporal reachable sets, including 12 static-overstatement pairs.

Total binary target positives: 138; negatives: 24. The 12 original static false-positive pairs are a different statistic from the 24 truly unreachable directed pairs.

## Prespecified observation comparison

Every observation key also includes origin and target identity. Bayes-oracle majority classification uses the *complete artificial universe* to assign the best class to each observation group. The table is exact and descriptive; it is in-sample mathematical observability, **not** out-of-sample forecast accuracy or empirical probability calibration.

| Observation channel | Keys | Mixed-label keys | Correct of 162 | Exact accuracy | Exact oracle Brier |
| --- | ---: | ---: | ---: | ---: | ---: |
| PAIR_ONLY, no event data | 6 | 6 | 138 | 23/27 | 92/729 |
| FULL ordered event triple | 162 | 0 | 162 | 1 | 0 |
| MULTISET contact counts | 60 | 12 | 150 | 25/27 | 4/81 |
| STATIC unique edges | 42 | 6 | 150 | 25/27 | 4/81 |
| FIRST contact only | 18 | 12 | 138 | 23/27 | 26/243 |
| LAST contact only | 18 | 12 | 138 | 23/27 | 26/243 |
| DISTINCT_COUNT unique-edge count | 18 | 12 | 144 | 8/9 | 22/243 |

Under these fixed schedules and the binary eventual-reachability target, knowing exact multiplicities beyond the static set of unique edges gives no further oracle accuracy or Brier improvement: MULTISET and STATIC tie at 25/27 and 4/81. Both leave 12 classification errors. FULL strict event ordering resolves all 162 labels. FIRST and LAST do not improve 0/1 accuracy over PAIR_ONLY, although their exact oracle Brier decreases. DISTINCT_COUNT provides an intermediate accuracy of 8/9. These conclusions are specific to the finite target and weighting; they do not establish general sufficiency of static graphs.

The FULL channel has one observation key per labeled instance, making perfect in-sample oracle discrimination a mathematical identity. It must not be presented as an externally validated prediction model. No parameter tuning, observed human outcome, sampling confidence interval, historical event or independent team validation is present.

## Source and computation

Primary executable: research/validation/r317_s113_temporal_coarsening.js. Machine receipt: research/validation/R317_S113_OBSERVATION_MAPS_EXACT.json. Full 162 labeled targets: research/validation/R317_S113_ALL_162_DIRECTED_LABELS.csv. Primary local Node v22.16.0 implementation of the same frozen recurrence and exact Fraction-style arithmetic executed successfully before archive; a compact archived JavaScript scorer was also executed through a V8 test adapter against the exact persisted CSV and JSON and reproduced both byte-for-byte. The adapter simulated the Node SHA1 provider, so archived native Node CLI replay remains an explicit NOT_RUN item. Independently, the original source Git blob was calculated and verified in native local execution and the B Python oracle.

Independent Python subsequence search, rather than the primary stepwise update, rebuilt all 162 targets and seven exact scores, rejected eight corruptions under both Python 3.13.5 and Python -O, and produced byte-identical normal and optimized audit stdout. This is internal, nonblind verification; the original R317 frozen E1 result and this new S113 result are separate.

## Scientific limitations and next gate

New S113 acceptance: PARTIAL_E1_EXTENSION. E2 human outcome prediction: 0. E3 historical prediction: 0. Independent external replication: NOT_RUN. For real temporal contact data, timestamp ties and within-bin simultaneity require an independently frozen rule; sorting tied contacts as sequential events could create false two-hop paths. No real hospital or school infection, communication or opinion adoption outcome was evaluated. R073 and PESEN v0.1 unchanged. original239 v7.8 crosswalk and 154 pending itemwise queue unchanged. No paid resources and no Actions dispatched. CI for new commits: NOT_RUN, account billing/quota UNKNOWN.

Foundational sources: Holme and Saramäki (2012), *Temporal networks*, https://doi.org/10.1016/j.physrep.2012.03.001; Pan and Saramäki (2011), https://doi.org/10.1103/PhysRevE.84.016105. Original R317 report: research/R317/R317_SCIENTIFIC_REPORT_2026-10-24.md.
