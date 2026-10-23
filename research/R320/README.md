# R320 finite absorbing random walk: DDM analogue only

Original239 **01-009 Drift Diffusion Model (P2)**. Prescore frozen at `ff112a92d32fd07695c77c6d6010cf121bfd8e8a`. All six artificial worlds, 384 six-bit exogenous path rows and exact first-hit summaries preserved. This is a discrete-time lattice analogue and does not replicate the original continuous DDM or human reaction times.

[Scientific report](R320_SCIENTIFIC_REPORT_2026-10-24.md), [384 original paths](R320_ALL_384_ORIGINAL_SIX_STEP_PATHS.csv), [6 exact world summaries](R320_EXACT_6_FIRST_HIT_WORLDS.json), [source and tests](r320_exact_absorbing_walk.py). Replay: `python research/R320/r320_exact_absorbing_walk.py --test` and `--audit`. Independent audit: `python research/catalogue_audit/independent_r320_absorbing_walk_audit.py`. Formal E1 acceptance awaits green CI and source Git blob verification; E2=0 E3=0. R073/PESEN v0.1 frozen.
