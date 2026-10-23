# R319 Mixed Logit finite two-point E1

Original239 **01-007 Mixed Logit**, P2. Frozen protocol commit `93c0c409c0a33f478eaa6942e211a2b0a3baecb0` precedes all source/results. Exact 5 choice sets × 3 mixture masses × 2 coefficient types yield 15 artificial worlds, 84 complete source atoms, 42 marginal probabilities. Nondegenerate mixture odds A/B change from 1 to 5/4 when a third option is introduced. R111 fixed logit is shared formula only; no human E2, no history E3.

[Scientific report](R319_SCIENTIFIC_REPORT_2026-10-24.md), [source](R319_ALL_84_ORIGINAL_CONDITIONAL_MIXTURE_SOURCE_ATOMS.csv), [results](R319_EXACT_15_MIXED_LOGIT_WORLDS.json), [code](r319_exact_finite_mixed_logit.py). Commands: `python research/R319/r319_exact_finite_mixed_logit.py --test`, `--audit`; independent `python research/catalogue_audit/independent_r319_mixed_logit_audit.py`. Formal acceptance awaits 3 green CI jobs and Git blob verification. R073/PESEN v0.1 frozen.
