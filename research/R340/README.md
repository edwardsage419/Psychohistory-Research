# R340: two-node SIS CTMC, bounded artificial E1

Original239 04-007 SIS Epidemic Model. Frozen protocol: ../../protocols/R340_SIS_TWO_NODE_48_ARTIFICIAL_GENERATOR_ATOMS_PRESCORE_FREEZE_2026-10-24.md

Run `python research/R340/r340_sis_generator.py --test --audit` and `python research/catalogue_audit/independent_r340_sis_audit.py`. To regenerate source files in a separate working copy, run `python research/R340/r340_sis_generator.py --write`.

The 48 source entries and 3 generator matrices are exact constructed Fraction data. The two-node graph has an absorbing healthy state. The result is only a finite E1 mechanism test. No real human E2, historical E3, network epidemic threshold, empirical replication or parameter fitting. R073 and PESEN v0.1 remain frozen.
