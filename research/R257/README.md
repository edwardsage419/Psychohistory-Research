# R257 最优化理论（11-017，P1）

九有理二维三角可行域世界（8个Hessian=2I的严格凸平方损失+1非凸反例），**225完整格点原候选source**，有界人工数学E1结题`CLOSED_BOUNDED_E1_STRICT_CONVEX_TRIANGLE_KKT_AND_NONCONVEX_COUNTEREXAMPLE`。

[事前冻结](../../protocols/R257_OPTIMIZATION_9_TRIANGLE_KKT_WORLDS_225_CANDIDATE_ATOMS_PRESCORE_FREEZE_2026-10-23.md) · [完整科学报告](R257_SCIENTIFIC_REPORT_2026-10-23.md) · [精确Fraction源代码/KKT四条件](r257_exact_triangle_optimization.py) · [225完整候选格点CSV](R257_ALL_225_ORIGINAL_GRID_CANDIDATE_SOURCE_ATOMS.csv) · [完整九world连续最优/格点最优JSON](R257_EXACT_RESULTS.json) · [SHA256机器收据](R257_FINAL_MACHINE_ACCEPTANCE.json) · [正式验收](R257_FINAL_ACCEPTANCE_STATUS.json)。

主要机制：前8个严格凸世界独立解析投影到三角形、Slater存在+全部KKT约束真值证明唯一全局最优。INTERIOR_OFF_GRID连续最优(3/5,1/5)、目标0，25格点无法达到，格点最佳损失1/80。非凸世界驻点(1/2,1/2)满足全部KKT且f=0，但(0,1/2)全局f=−1/4更好，说明非凸KKT不能自动充作全局充分性。原source包含不可行格点并标注，不能当可行解。

[成功CI run39897185617](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39897185617)三job通过，Python3.11/3.12各82真实测试共164项通过，全部源CSV/JSON/SHA bot归档[e328edc4](https://github.com/edwardsage419/Psychohistory-Research/commit/e328edc4eff479b4453219e3b9c622f87968e4b8)。无新增E2/E3，R073/PESEN v0.1冻结。下条原目录11-018 Optimal Control（R258）。
