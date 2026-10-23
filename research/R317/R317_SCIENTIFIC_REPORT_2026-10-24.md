# R317: Temporal network exact time respecting contact reachability E1

Date 2026-10-24 Asia/Taipei. Original239 candidate 04-022 Temporal Networks, P1. Research scope: **artificial discrete finite time-order mechanism E1**.

## Sources and prescore freeze

Holme & Saramäki (2012), *Temporal networks*, *Physics Reports* 519(3):97–125, DOI https://doi.org/10.1016/j.physrep.2012.03.001 ; Pan & Saramäki (2011), *Path lengths, correlations, and centrality in temporal networks*, *Phys Rev E* 84:016105, DOI https://doi.org/10.1103/PhysRevE.84.016105 . Research is strictly methodological; not their empirical communication or transport data.

Frozen before any source/results at git [R317 freeze](../../protocols/R317_TEMPORAL_NETWORKS_THREE_CONTACT_81_SOURCE_STRICT_TIME_FREEZE_2026-10-24.md), commit `ff6ae9c21a559bce7e266a8203b1db0f674b41a3`.

Three artificial nodes with possible undirected contact identities 0=(0,1), 1=(0,2), 2=(1,2). At each of strictly increasing timestamps t=1,2,3 one edge activates. All **27 ordered three-contact schedules** enumerated; repeats allowed, producing **81 complete original contact source rows**. From all 3 seeds in each schedule, compute **81 schedule-origin outcomes** with earliest possible reception time and final reachable agents. A contact transmits only one hop when its participant already holds a message prior to the event; messages may persist and wait. Only strictly increasing timestamps may be used for multi-contact paths.

## Exact results and limitations

Among all 27 schedules and 3 possible origins, the number of **ordered origin-target pairs** declared reachable by the static union graph yet unreachable by any time-respecting walk is **12**. The denominator is 27 schedules × 3 origins × 2 other targets=162 directed source-target possibilities. This finite descriptive ratio 12/162 uses complete enumerated counterfactual schedules, not sampling or statistical inference.

Critical exact witness schedule id18, contact indices (2,0,0):
* t1 contact between agents1 and2; t2 and t3 contacts between0 and1.
* The undirected **static aggregate** is connected across all 3.
* Starting from node0 at t0, node1 is first reached at t2 and node2 is never reached: arrival times [0,2,null].
* Starting from node2 at t0, node1 is reached t1 and node0 t2: arrival times [2,1,0].
* Therefore time respecting reachability can be asymmetric even though every individual event is undirected, and aggregating away event time can create spurious possible paths.

Every time-respecting reachable node belongs to its original static connected component. This is a finite exact theorem checked across all 81 origin outcomes. An event with endpoints receiving the message at that same time cannot immediately retransmit it within the same event. This is mechanistically separate from R309 static SIR contagion probabilities, R315 static Watts Strogatz rewiring, and R316 stochastic block graph distributions.

These event schedules are synthetic, and no human communication timing, vaccination benefit, epidemic forecast, historical diffusion or statistical generalization has been tested. New human E2=0, historical E3=0.

## Reproducible research files

* [All 81 temporal contact source rows](R317_ALL_81_ORIGINAL_TEMPORAL_CONTACT_SOURCE_ROWS.csv) and [all 81 origin outcomes](R317_ALL_81_ORIGIN_TEMPORAL_REACHABILITY_OUTCOMES.json).
* [Primary exact recurrence with unit tests](r317_exact_temporal_reachability.py).
* [Independent no-import depth-first strictly increasing contact subsequence audit](../catalogue_audit/independent_r317_temporal_source_audit.py).
* [GitHub CI workflow](../../.github/workflows/r317-temporal-strict-time-paths-e1.yml), two Python unit test jobs plus independent full source audit.

Only when all CI jobs completed/success and exact archive replay passes should R317 be promoted to limited formal E1 and original239 v3.4 update 04-022 only. R073 and PESEN v0.1 remain frozen.
