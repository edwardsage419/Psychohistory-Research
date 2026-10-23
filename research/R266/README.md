# R266 有限蒙特卡洛模拟：9个人工世界（原目录11-026，P0）

研究状态：**CLOSED_BOUNDED_E1_EXACT_FINITE_MONTE_CARLO**。n为被积函数求值数，所研究的是四点均匀人工概率空间；所有5328种原source完整枚举，18组IID/对偶估计分布由独立卷积逐Fraction校验。新增真人E2=0、真实历史E3=0。

[事前冻结协议](../../protocols/R266_MONTE_CARLO_NINE_WORLDS_5328_FINITE_SOURCE_ATOMS_PRESCORE_FREEZE_2026-10-23.md) · [原生精确计算源码](r266_finite_monte_carlo.py) · [5328条完整来源CSV](R266_ALL_5328_FINITE_MONTE_CARLO_ORIGINAL_SOURCES.csv) · [9世界完整概率分布及计算结果](R266_EXACT_FINITE_MC_RESULTS.json) · [SHA256原数据凭证](R266_MACHINE_RECEIPT.json) · [正式科学报告](R266_SCIENTIFIC_REPORT_2026-10-23.md) · [机读验收](R266_FINAL_ACCEPTANCE_STATUS.json)。

关键反例：对于单调阈值p=1/4、3/4，固定相同函数评价数，对偶估计方差是IID的2/3；p=1/2的居中阈值可精确零方差；对称两端事件f(u)=f(3-u)的对偶估计方差反而是IID的2倍。结论只覆盖已冻结函数，不能被解释为真实社会模型的蒙特卡洛效率证明。

[双Python CI成功 run39900969661](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39900969661)：Python3.11与3.12各136项真实测试成功，第三作业完整验证来源和PMF并通过，合计三job全部success。全部来源及机器SHA已由GitHub机器人永久归档到main：[e46f0e06](https://github.com/edwardsage419/Psychohistory-Research/commit/e46f0e06afb637ba2bb0cc2e267f2c36c1cc9c35)。

下一原目录已核实为11-027 Latin Hypercube Sampling（拟R267）。原R学习完成之前，暂缓模型统一分类与熔炼；R073和PESEN v0.1继续冻结。
