# R232 结构方程模型（10-006）：八个人工结构—测量机制、1024完整来源和SEM因果路径界限

日期2026-10-23。原始239目录 `10-006 Structural Equation Modeling`（P1）。有界科学状态 `CLOSED_BOUNDED_E1_ARTIFICIAL_SEM_MEDIATION_MEASUREMENT`。

[先行冻结协议](../../protocols/R232_SEM_8_WORLDS_1024_ORIGINAL_STRUCTURAL_SOURCES_PRESCORE_FREEZE_2026-10-23.md) · [完整科学报告](R232_SCIENTIFIC_REPORT_2026-10-23.md) · [1024完整原结构来源CSV](R232_ALL_1024_ORIGINAL_SEM_EXOGENOUS_SOURCES.csv) · [原生Python计算](r232_exact_structural_mediation.py) · [全八世界观察协方差/因果真值JSON](R232_EXACT_RESULTS.json) · [SHA机读凭证](R232_FINAL_MACHINE_ACCEPTANCE.json) · [正式结题收据](R232_FINAL_ACCEPTANCE_STATUS.json)。

八人工世界精确区分观察多变量协方差和真do(A)路径。LATENT_CAUSAL_ALIAS/LATENT_COMMON_ALIAS对全部独立原来源实际五项`A,W,Y,Z1,Z2`完全相同，但真正do(A)总效应分别1与0；人工U完全决定A、不具给定U后的处理变化支持。另随机化处理的两个独立例子：共享未测媒介—结果U可令OLS媒介乘积3/2、假直达−1/2（真实媒介1、直接0）；W=M+误差可令OLS媒介/直达均1/2（真实媒介1、直接0）。观察两条路径相加得到总回归不自动验证它们的因果正确性。

[真实CI run39828613170](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39828613170)总体success，Python3.11和3.12各60测试均OK，完整原1024来源机器人永久提交[fc2bdfb6](https://github.com/edwardsage419/Psychohistory-Research/commit/fc2bdfb62c6164c400a1d364ee6dc75baea45d54)。无真人E2或真实历史E3新增。R073/PESEN v0.1冻结。

下一原239目录10-007 Measurement Invariance（R233），坚持完成全部R后统一分类再熔炼。
