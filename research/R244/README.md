# R244 马尔可夫随机过程（11-004）：九人工二态世界、1152七位完整原来源

日期2026-10-23。原239目录 `11-004 Markov Stochastic Processes` P1，有界研究 `CLOSED_BOUNDED_E1_EXACT_FINITE_MARKOV_HIDDEN_MIXTURE`。

[预评分完整冻结协议](../../protocols/R244_MARKOV_9_WORLDS_1152_FULL_SEVEN_BIT_PATH_ATOMS_PRESCORE_FREEZE_2026-10-23.md) · [科学报告](R244_SCIENTIFIC_REPORT_2026-10-23.md) · [1152条全七位原source CSV](R244_ALL_1152_ORIGINAL_BINARY_MARKOV_SOURCE_PATHS.csv) · [Fraction概率及独立转移核源码](r244_exact_markov_hidden_mixture.py) · [九模型完整4时点路径/条件独立JSON](R244_EXACT_RESULTS.json) · [SHA机器原档收据](R244_FINAL_MACHINE_ACCEPTANCE.json) · [独立有界验收](R244_FINAL_ACCEPTANCE_STATUS.json)。

重要反例：隐藏U确定人工个体stay概率3/4或1/4、但U在完整路径不变时，**给定可见当前Y2=0**，此前Y1=0或1对Y3=0条件预测分别7/10或3/10，只有Y2时恰1/2。两种真实条件Markov内核的总体混合使可见Y不再一阶Markov，有限路径Markov条件缺陷1/5；固定隐藏switch策略产生缺陷1/2；时间非齐次但无隐藏混合的world虽每期stay率不同仍Markov缺陷0。另三人工世界全部七比特原source实际Y0…Y3相同，但真隐藏状态可以是真Markov链、恒定仪器隐藏态或互补标号状态。独立完整路径产品公式以及时间齐次核的Chapman–Kolmogorov矩阵平方/立方检验通过。所有只是有限人工E1。

[CI run39889712674](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39889712674)三job completed/success，Python3.11/3.12各83真实单测，共166通过；全部1152原路径、JSON和SHA永久机器人归档[90765065](https://github.com/edwardsage419/Psychohistory-Research/commit/907650659e92e8abff7a07b3eeb2b2e873f67938)。

新增真人E2=0、真实历史E3=0，R073及PESEN v0.1冻结。下一原目录 **11-005 Renewal Processes（R245，P2）**，其后 **11-006 Poisson and Hawkes Processes**。先完成全部原R，再分类，最后熔炼。
