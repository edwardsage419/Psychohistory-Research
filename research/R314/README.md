# R314 | Barabási Albert preferential attachment | Original239 04-016

Scope: 3 synthetic connected seed networks, two sequential additions per seed, single degree-proportional target attachment per addition. Exactly 54 target-choice source atoms and 44 complete paths with exact rational probabilities.

Frozen prescore protocol: [R314 freeze](../../protocols/R314_BARABASI_ALBERT_THREE_SEED_TWO_ARRIVAL_54_TARGET_SOURCE_PRESCORE_FREEZE_2026-10-24.md), commit `0426722f05cb409655f0bee5897d4b57c87cfa0a`. Original paper Barabási & Albert 1999, https://doi.org/10.1126/science.286.5439.509 .

To independently reproduce:
```bash
python research/R314/r314_exact_preferential_attachment.py --test
python research/R314/r314_exact_preferential_attachment.py --audit
python research/catalogue_audit/independent_r314_source_audit.py --audit
```

Archives: [54 exact source atoms](R314_ALL_54_ORIGINAL_TARGET_SOURCE_ATOMS.csv), [44 complete paths](R314_EXACT_44_TWO_ARRIVAL_PATH_RESULTS.json), [science report](R314_SCIENTIFIC_REPORT_2026-10-24.md). Strictly finite artificial E1. No scale-free exponent, no real-world network verification, no human E2, no historical E3.
