# R313 Axelrod cultural dissemination | catalogue 04-014

Frozen protocol: [R313 freeze](../../protocols/R313_AXELROD_THREE_SITE_TWO_FEATURE_EXACT_ONE_STEP_PRESCORE_FREEZE_2026-10-24.md) at `8b69fc8c`.

Scope: 64 artificial three-site path cultures (two binary features each), all 256 oriented neighbor choices and 512 potential feature atoms. Similarity-dependent directional copy rule. 16 absorbing worlds; 128 positive copy atoms. No new human E2 or historical E3.

Run on Python 3.11 or 3.12:
```bash
python research/R313/r313_exact_axelrod.py --test
python research/R313/r313_exact_axelrod.py --audit
python research/catalogue_audit/independent_r313_source_audit.py --audit
```

Machine archives: [all 512 source atoms](R313_ALL_512_ORIGINAL_FEATURE_SOURCE_ATOMS.csv), [all 64 exact outcomes](R313_EXACT_64_WORLD_ONE_STEP_RESULTS.json). See [scientific report](R313_SCIENTIFIC_REPORT_2026-10-24.md). E1 promotion requires all GitHub CI jobs to pass. Original Axelrod (1997), https://doi.org/10.1177/0022002797041002001 .
