# R246 泊松过程与 Hawkes 过程目录（11-006）：九个有限Bernoulli事件代理，非连续点过程复现

日期2026-10-23。原239目录`11-006 Poisson and Hawkes Processes` P1；正式科学状态`CLOSED_BOUNDED_E1_FINITE_BERNOULLI_EVENT_SELF_EXCITATION_SURROGATE`。**所有模型是四格、每格至多发生一次事件的Bernoulli条件概率过程**，不能称为高斯或真正Poisson/Hawkes连续时间点过程，不能恢复同格多次事件、真实条件强度或原论文谱/协方差结论。

[计算前冻结协议](../../protocols/R246_POISSON_HAWKES_DISCRETE_SURROGATE_9_WORLDS_4608_ORIGINAL_EVENT_ATOMS_PRESCORE_FREEZE_2026-10-23.md) · [完整科学报告与限定范围](R246_SCIENTIFIC_REPORT_2026-10-23.md) · [九世界4608完整外生事件原source CSV](R246_ALL_4608_ORIGINAL_BINNED_EVENT_SOURCES.csv) · [原生Fraction概率程序](r246_exact_binned_poisson_hawkes_surrogate.py) · [观察完整四元路径/条件概率/协方差JSON](R246_EXACT_RESULTS.json) · [来源SHA256机器收据](R246_FINAL_MACHINE_ACCEPTANCE.json) · [独立正式验收](R246_FINAL_ACCEPTANCE_STATUS.json)。

三种不同机制可产生人工事件正相关：显式上一格事件提高后一格Bernoulli率（Cov=3/32），隐藏稳定U令总体观察正相关但在给定U后各格独立（Cov=1/16），四格共享同一外生shock（Cov=1/4）。另在两格记忆过程中，即使最新一格无事件，早一格有无事件会令第三格概率1/2 vs1/4，不能单凭目前最新一格认定预测已充分。STATIC_HIDDEN_SELF_EXCITING_SENSOR_ALIAS的真实隐藏事件全0，却同SELF_EXCITING_LAG1逐原source可见事件路径完全一致。这些都为有界人工反例，非真实心理/历史事件因果发现。

[GitHub Actions run39891833189](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39891833189)三job全success，Python3.11/3.12各84实际测试、共168通过；所有4608来源及SHA永久机器人归档[8ebea75a](https://github.com/edwardsage419/Psychohistory-Research/commit/8ebea75a9b5aaa70d330466a2c42a60306b4db43)。仅人工E1，新增真人E2/历史E3均0，R073与PESEN v0.1冻结。下一目录11-007 Branching Processes（拟R247）。保持全部原R完成后再分类与熔炼。
