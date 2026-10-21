# R186 零膨胀计数模型：40个人工来源世界的机制识别边界

2026-10-21。239候选目录P2/08-010 Zero Inflated Count Models。正式状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_ZERO_INFLATION**。

[事前冻结协议](../../protocols/R186_ZERO_INFLATED_40_WORLDS_1860_SAMPLES_PRESCORE_FREEZE_2026-10-21.md)严格沿用R177源代码Git blob `2d032513ce84141214b6b3f84df9c0ed9976a02b` 和原结果SHA256 `57410cf2c110ce3117b7af72e4b7473cee0c3ffd013e6fb99fd43de62165a535`。以2种组内机会n×2种独立训练群组数m×2种边际成功率p×5种独立、正相关或潜在结构零计数机制，完整枚举**40个人工来源世界与1860条有序训练样本**。用普通BIN单参数11个候选与ZIB双参数55个候选的明确冻结网格精确求训练似然最大值。全部66种不重复有序等价profile的ZIB PMF、两套完全独立的Fraction概率及likelihood算法逐项一致，独立新群组测试logloss由math.log及Decimal.ln两条路径复核。

**重要不可识别反例：** 当n=2、边际p=1/2时，BB浓度2与ZIB结构零1/4两种真实机制具有**完全一致PMF=(1/3,1/3,1/3)**，因此针对2或3个训练群组，两个机制的拟合模型选择、预测损失与模型工作结构零归因全都一模一样。然而观测新群组K=0的真实结构零概率，在BB下为**0**，在真实ZIB下为**3/4**。2个群组训练时，模型选出非零zhat的概率在两种源都为33.33%，模型跨训练样本平均零归因为约28.11%，BIN与ZIB独立测试logloss分别1.546576与1.643415。额外模型参数提高或维持训练最大似然，未保证独立预测提升；也不能用模型生成的零来源后验冒充真实隐藏机制已被识别。

[正式科学报告](R186_SCIENTIFIC_REPORT_2026-10-21.md)、[40世界完整来源与独立预测JSON](R186_EXACT_RESULTS.json)、[1860条原始人工数据CSV](R186_ALL_1860_ORDERED_TRAINING_SAMPLES.csv)、[66种独立算法全概率拟合library](R186_ALL_66_FIT_PROFILES.json)、[机器验收](R186_FINAL_MACHINE_ACCEPTANCE.json)、[完整原生程序与29项测试](r186_zero_inflation_exact_grid_fit.py)、[源码协议全量结果ZIP](R186_Zero_Inflation_40_Worlds_Exact_Archive.zip)均已永久归档。[GitHub Actions39564090277](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39564090277) Python3.11与3.12分别29项共58次测试及第三工作流全部40世界和归档三job全success，[原结果提交eb4e6c5](https://github.com/edwardsage419/Psychohistory-Research/commit/eb4e6c52b7a3876706300a8ed3737a8a2e26b5cb)。

理论来源：[Lambert1992](https://doi.org/10.2307/1269547)、[Hall2000](https://doi.org/10.1111/j.0006-341X.2000.01030.x)。仅人工E1，新增真人E2与真实历史E3均0；R073、PESEN v0.1保持冻结。下一R187 P1/08-011 Ordinal Logistic Regression（有序逻辑回归）；继续原全R序列后统一归纳分类、最后模型熔炼。
