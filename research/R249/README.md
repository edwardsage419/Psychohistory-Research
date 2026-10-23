# R249 分岔理论（原11-009，P1）

2026-10-23 正式有界人工E1结题`CLOSED_BOUNDED_E1_EXACT_LOGISTIC_FOLD_BRANCH_BIFURCATION`。五个Logistic参数和四个fold/saddle-node正规形参数世界，9初值×5时点×9world=**405完整原来源点**，精确数学而非历史制度阈值数据。

[独立先行冻结协议](../../protocols/R249_BIFURCATION_9_RATIONAL_PARAMETER_WORLDS_405_ORIGINAL_ATOMS_PRESCORE_FREEZE_2026-10-23.md) · [科学报告](R249_SCIENTIFIC_REPORT_2026-10-23.md) · [精确Python与形式多项式复合程序](r249_exact_bifurcation_parameter_worlds.py) · [405完整原CSV](R249_ALL_405_ORIGINAL_BIFURCATION_PARAMETER_SOURCE_ATOMS.csv) · [九参数根及重数和临界证明JSON](R249_EXACT_RESULTS.json) · [SHA256机器原来源凭证](R249_FINAL_MACHINE_ACCEPTANCE.json) · [正式有界验收](R249_FINAL_ACCEPTANCE_STATUS.json)。

Logistic r由1/2到1到2展示实数根0与1-1/r在r=1相交且局部稳定性交换；fold`f_mu(x)=x+mu-x²`展示mu<0无实根、mu=0重根、mu>0两固定点。r=3非双曲正固定点2/3与fold mu=1非双曲正固定点1都以精确第二次迭代多项式/9/64上界严格证明局部吸引，不能用乘子-1直接判为不稳定。未复现完整period-doubling曲线或真实历史阈值。

[GitHub CI run39894061461](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39894061461)三job成功，Python3.11/3.12各85真实单测，**170通过**；全部来源机器人归档[193cc657](https://github.com/edwardsage419/Psychohistory-Research/commit/193cc6576d9cd93748bb3c518d27ae6e91f621fa)。E2/E3新增0，R073/PESEN v0.1冻结。下一原目录11-010 Critical Phenomena（R250）。
