# R317 Temporal Networks | original239 04-022

Finite exact E1 only, based on temporal paths from Holme & Saramäki (2012), DOI https://doi.org/10.1016/j.physrep.2012.03.001 and Pan & Saramäki (2011), DOI https://doi.org/10.1103/PhysRevE.84.016105 .

Prescore freeze git commit `ff6ae9c21a559bce7e266a8203b1db0f674b41a3`.

Three nodes, 3 strictly ordered contacts, every 3^3=27 artificial contact schedule, 81 original event source rows and 81 origin-conditioned outcomes. Static aggregation overstates 12/162 directed pair instances relative to exact temporal reachability. No real human E2 or historical E3.

```bash
python research/R317/r317_exact_temporal_reachability.py --test
python research/R317/r317_exact_temporal_reachability.py --audit
python research/catalogue_audit/independent_r317_temporal_source_audit.py --audit
```

[Report](R317_SCIENTIFIC_REPORT_2026-10-24.md), [source CSV](R317_ALL_81_ORIGINAL_TEMPORAL_CONTACT_SOURCE_ROWS.csv), [full outcome JSON](R317_ALL_81_ORIGIN_TEMPORAL_REACHABILITY_OUTCOMES.json).
