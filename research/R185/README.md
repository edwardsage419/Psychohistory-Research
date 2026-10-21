# R185 负二项回归：135人工世界的过度离散与相同矩数不同零概率

日期2026-10-21。原目录P1/08-009 Negative Binomial Regression。状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_NEGATIVE_BINOMIAL**。

[计算前冻结协议](../../protocols/R185_NEGATIVE_BINOMIAL_135_WORLDS_PRESCORE_FREEZE_2026-10-21.md)明确固定R177原始SHA计数数据，3种n×3组边际概率组合×5种源生成机制×3种NB已知形状r=2、6、8，共**135组人工世界、12,375条完整来源联合概率训练计数对**。NB预测概率由封闭组合分数公式与独立递推两条路径精确一致；所有真实测试源计数按其原始PMF计入损失，未将无界NB分布误截断归一。NB/Poisson固定采用同一预测强度`λ=K+1/2`比较，每项测试logloss由float math与60位Decimal两路核验。

**预冻结关键反例**：n=8、真实边际p=1/4，BetaBinomial浓度8与ZIB结构零1/4两类不同源的真实计数**均值完全相同2、方差完全相同8/3**，基于前两阶矩匹配NB形状同为r=6；但是前者原始零计数概率恰好**20%**，后者为`2443/8748`约**27.926%**。同一个NB(μ=2,r=6)零概率为`729/4096`约17.798%，不能同时解释上述两个不同来源零质量。仅检查均值和方差不足以识别计数的隐藏零来源或组内相关机制。

[正式科学报告](R185_SCIENTIFIC_REPORT_2026-10-21.md)、[完整135世界概率结果JSON](R185_EXACT_RESULTS.json)、[12,375条全部来源概率CSV](R185_ALL_12375_SOURCE_WEIGHTED_TRAINING_PAIRS.csv)、[机器科研验收](R185_FINAL_MACHINE_ACCEPTANCE.json)、[完整源码与27种测试](r185_negative_binomial_exact.py)、[源码协议结果确定性ZIP](R185_135_Negative_Binomial_Exact_Count_Worlds.zip)永久入库。[GitHub Actions39562923374](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39562923374)双Python各27测试共54次执行及全部135世界完整真实评分第三job三job全success，[正式数据结果提交0475e6b](https://github.com/edwardsage419/Psychohistory-Research/commit/0475e6b0db88bd1563b4a290f2874ab569fae31a)。

来源：[Cameron/Trivedi2013](https://doi.org/10.1017/CBO9781139013567)、[Nelder/Wedderburn1972](https://doi.org/10.2307/2344614)。全部结论仅人工数学E1，无真人E2或真实历史E3新增。R073与PESEN v0.1保持冻结。下一R186 P2/08-010 Zero Inflated Count Models（零膨胀计数模型）。完成全部R系列后统一归纳分类、最后熔炼。
