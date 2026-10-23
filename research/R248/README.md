# R248 动力系统平衡分析（原11-008，P1）

2026-10-23 正式有界人工E1结题`CLOSED_BOUNDED_E1_EXACT_RATIONAL_EQUILIBRIA_NONHYPERBOLIC_PROOFS`。九个一维离散自治映射，9初值×5时点×9world=**405完整人工原来源点**。

[独立先行冻结协议](../../protocols/R248_EQUILIBRIA_9_RATIONAL_MAP_WORLDS_405_IVP_TIME_SOURCES_PRESCORE_FREEZE_2026-10-23.md) · [科学报告](R248_SCIENTIFIC_REPORT_2026-10-23.md) · [原生Fraction映射与独立形式多项式计算](r248_exact_rational_equilibria.py) · [全部405原CSV](R248_ALL_405_EXACT_MAP_IVP_TIME_SOURCES.csv) · [固定点和严格非双曲证明JSON](R248_EXACT_RESULTS.json) · [SHA256完整来源收据](R248_FINAL_MACHINE_ACCEPTANCE.json) · [正式有界验收](R248_FINAL_ACCEPTANCE_STATUS.json)。

精确证明`f(x)=3x(1-x)`在x*=2/3乘子-1仍可经两次迭代在|x-2/3|≤1/12局部收敛；`f(x)=x-x³`在0乘子+1也局部吸引；恒等映射全实数皆固定且不吸引别的点；`f(x)=4x(1-x)`中3/4乘子-2局部排斥却可由x0=1/4一步精确到达。局部稳定证书和有限轨道体验严格分离，不做历史平衡实证推断。

[真实CI run39893826278](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39893826278)三job成功，Python3.11与3.12各84真实单测，**168通过**；完整来源机器人归档[10068ac1](https://github.com/edwardsage419/Psychohistory-Research/commit/10068ac15ec8a1f74b5dd9c2e7fb03db16a4af96)。E2/E3新增0，R073与PESEN v0.1冻结。下一原目录11-009 Bifurcation Theory（R249）。
