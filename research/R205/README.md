# R205 PCA：12个人工尺度与有限训练PCA，正式有界E1结题

日期 2026-10-21。原239目录P1/08-029 Principal Component Analysis。**CLOSED_BOUNDED_E1_ARTIFICIAL_AXIS_PCA**。

[原计算前冻结](../../protocols/R205_PCA_12_WORLDS_240_TRAIN_960_HELDOUT_PRESCORE_FREEZE_2026-10-21.md) · [正式完整科学报告](R205_SCIENTIFIC_REPORT_2026-10-21.md) · [12世界结果JSON](R205_EXACT_RESULTS.json) · [240条原始训练来源](R205_ALL_240_ORIGINAL_PAIRED_PCA_TRAINING_HISTORIES.csv) · [960条独立未来联合来源](R205_ALL_960_INDEPENDENT_TEST_SOURCE_PAIRS.csv) · [SHA机器证据](R205_FINAL_MACHINE_ACCEPTANCE.json) · [正式机读结题验收](R205_FINAL_ACCEPTANCE_STATUS.json) · [原生Python及36单测](r205_exact_axis_pca.py)。

六个人工二维尺度源(a,b)∈{(1,1),(2,1),(1,2),(3,1),(1,3),(2,2)}，独立选轴3或5次；每次产生正负一对相关训练观察。完整12来源世界，240条原训练轴选择历史以及960条完整训练×真正独立未来轴及符号联合来源。**每对的两行观察互相依赖**，不能认作两次独立抽样。中心化协方差经源原2m条数据直接求和与独立轴频数公式精确Fraction一致；正确先验同分优先+e1，训练解释比与完全留出未来保留比、重建误差以及两个不同目标都分别完整评分。

主要结论：真(1,1)、m5的训练解释方差11/16=68.75%，独立未来真实保留仍1/2；(3,1)、m5按无目标的最大方差选第一轴概率31/32，实际Y2目标MSE31/64，对应目标先验知情理想保留轴MSE0；(1,2)真源训练对数从3到5，独立重建MSE由11/16增加为25/32，说明当前**有限训练选轴程序**不存在逐样本规模单调改善保证。这个有界理论结果与一般PCA所有方向、真实心理测量因子推断和社会因果解释严格区分。

[GitHub Actions run 39610637466](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39610637466) Python3.11、3.12各36项测试共72次全通过；第三实际输出12世界、240条全原训练、960条真正独立来源测试，核验SHA与完整源归一并永久写回 [main原结果提交 f09b4065](https://github.com/edwardsage419/Psychohistory-Research/commit/f09b40653907ee2f20653747e76b7762b39fb1d7)。

新增真人E2=0，真实历史E3=0；R073/PESEN v0.1冻结。**下一 R206 P2/08-030 Clustering Methods**，保持先完成全部R系列，再统一分类，最后熔炼。
