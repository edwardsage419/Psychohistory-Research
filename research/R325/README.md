# R325 Regret Theory: finite statewise cubic comparison E1

Original239 **01-020**, P2. [Frozen protocol](https://github.com/edwardsage419/Psychohistory-Research/commit/2d4fec87becfc46b6f66da1db5187b557afdcb53) precedes [source and 1029 artificial rows](https://github.com/edwardsage419/Psychohistory-Research/commit/73c847c4be895b806621d929f80f20439b166c11). Three constructed kappa worlds 0, 1/4, 1, each containing all 343 three-state difference vectors from {-3,-2,-1,0,1,2,3}^3. Exact Q(d)=d+kappa*d^3 comparison reverses strict EU preference for (3,-2,-2): -1/3 to 7/12 and 10/3. Each positive-kappa world has 6 strict EU/regret reversals among 343 artificial vectors.

**PASS_BOUNDED_E1_PROJECT_CONSTRUCTED_CUBIC_REGRET_ONLY** after [three green CI jobs](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40021709853): Python 3.11/3.12 each 26 tests, independent no-import 1029-state audit.

[Scientific report](R325_SCIENTIFIC_REPORT_2026-10-24.md), [acceptance](R325_FINAL_ACCEPTANCE_STATUS.json), [receipt](R325_MACHINE_RECEIPT.json), [generator](r325_regret.py), [original artificial CSV](R325_ALL_1029_ARTIFICIAL_REGRET_STATES.csv), [exact JSON](R325_EXACT_THREE_REGRET_WORLDS.json).

Replay `python research/R325/r325_regret.py --test`, `--audit`, and `python research/catalogue_audit/independent_r325_regret_audit.py`. Project-created artificial E1 only; no 1982 empirical replication, human E2 or historical E3. R073/PESEN v0.1 frozen.
