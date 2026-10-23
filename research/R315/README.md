# R315 | Watts Strogatz finite small-world rewiring | 04-017

Prescore frozen at [commit 7cbbc778](https://github.com/edwardsage419/Psychohistory-Research/commit/7cbbc7785a411d7d535536c028c3c051edf71e28).

Artificial exact E1 only: N in {8,10}, k=4, first clockwise original edges (0,1),(1,2), p in {0,1/2,1}, with endpoints constrained to existing non-neighbors. 210 conditional event atoms, 180 full paths, exact final clustering, mean shortest path and connectivity.

Reproduce:
```bash
python research/R315/r315_exact_small_world.py --test
python research/R315/r315_exact_small_world.py --audit
python research/catalogue_audit/independent_r315_source_audit.py --audit
```

See [scientific report](R315_SCIENTIFIC_REPORT_2026-10-24.md), [source CSV](R315_ALL_210_ORIGINAL_REWIRING_ATOMS.csv), [path JSON](R315_EXACT_180_TWO_EVENT_GRAPH_PATHS.json). Primary Watts & Strogatz (1998), https://doi.org/10.1038/30918 . No full ring sweep, human E2, historical E3, or large ensemble power/scaling result.
