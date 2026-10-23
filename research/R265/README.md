# R265 Sobol全局敏感度（11-025，P1）

九个人工独立公平Bernoulli四输入函数，完整**144条原四bit source**、逐world全部15非空变量子集方差ANOVA，共135项独立精确数学分量。正式科研状态`CLOSED_BOUNDED_E1_EXACT_FOUR_INDEPENDENT_BINARY_INPUT_SOBOL_ANOVA`。不是对真实历史数据或相关参数现实模型的敏感性估计。

[事前冻结](../../protocols/R265_SOBOL_9_FOUR_BINARY_INPUT_144_SOURCE_ATOMS_PRESCORE_FREEZE_2026-10-23.md) · [正式报告](R265_SCIENTIFIC_REPORT_2026-10-23.md) · [原生Fraction Walsh和独立条件期望Möbius源码](r265_exact_fourbit_sobol.py) · [全部144原source CSV](R265_ALL_144_ORIGINAL_FOURBIT_SOBOL_INPUT_SOURCES.csv) · [九world15子集指数、first和total JSON](R265_EXACT_RESULTS.json) · [SHA256完整来源](R265_FINAL_MACHINE_ACCEPTANCE.json) · [机器正式验收](R265_FINAL_ACCEPTANCE_STATUS.json)。

四位全XOR世界的一阶四个Sobol指数全部0，但总敏感度全部1、只有四阶交互贡献1；四位全AND世界全部15个非空子集各1/15、一阶各1/15、总效应各8/15。证明“没有一阶敏感度”不等于变量不重要；结论严格要求输入分布独立且冻结。

[最终成功CI run39900027884](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39900027884)三job success，Python3.11和3.12各82真测试共164次，原CSV/JSON/SHA机器人永久归档[ad9bd248](https://github.com/edwardsage419/Psychohistory-Research/commit/ad9bd248106dfefdb353ae449bb381dd5429df87)。新增E2/E3=0，R073/PESEN v0.1冻结。下原目录11-026 Monte Carlo Simulation（R266）。
