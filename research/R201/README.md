# R201 Cox 比例风险模型，正式人工E1有界结题

2026-10-21。原239目录P1/08-025。状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_COX_EVENT_ORDER**。已事前冻结[研究协议](../../protocols/R201_COX_3_HR_9_WORLDS_120_PREFIXES_PRESCORE_FREEZE_2026-10-21.md)，之后实现、双版本测试与归档。

[正式科学报告](R201_SCIENTIFIC_REPORT_2026-10-21.md) · [完整结果](R201_EXACT_RESULTS.json) · [120条训练来源CSV](R201_ALL_120_ORIGINAL_TRAINING_PREFIXES.csv) · [机器验收及SHA](R201_FINAL_MACHINE_ACCEPTANCE.json) · [原生Python及26项测试](r201_exact_cox_partial_likelihood.py)。

三个HR来源1/4、1、4 × 前1、2、3件人工失败 = 9世界，全部72个完整原事件次序与120个训练前缀精确列举；候选HR按1、1/4、4同分优先，独立新队列事件身份按真实来源四类概率评分。真HR1仅见一件事件时模型无法选中null，Brier **0.84** 差于固定null 0.75；三次事件后0.81仍差于0.75。真HR4与1/4，三次事件时Brier 0.6984，相比固定null 0.75改善，已知真机制oracle为0.66。正确删失风险集因子2/25，错误保留已删失者1/15；Breslow、Efron、exact并列反例1/25、4/75、4/33。相同HR4在两种共同基准风险下下一事件身份概率相同，单位时间至少一次事件概率分别约0.63212和0.86466，证明部分似然缺乏绝对时间识别。

[GitHub Actions run 39596546636](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39596546636) 两个Python版本各26项共**52项全通过**，归档job success；[原始结果已写回main](https://github.com/edwardsage419/Psychohistory-Research/commit/f7de3dbc8e75f90ddfd69e90b2c4e9aad071874d)。仅人工E1，不涉及真人事件实证、真实制度采纳、一般连续风险比估计或因果解释。新增E2=E3=0；R073和PESEN v0.1冻结。

**下一 R202 P2/08-026 Accelerated Failure Time**。保持全R完成后再分类和熔炼。
