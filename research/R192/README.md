# R192 潜在类别模型：两指标观测等价、第三指标增量与标签交换

2026-10-21。原239目录P2/08-016 Latent Class Models。科研状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_LATENT_CLASS**。

[事前冻结协议](../../protocols/R192_LATENT_CLASS_8_WORLDS_1312_TRAINING_PRESCORE_FREEZE_2026-10-21.md)固定两个等权潜在类别C=0/1，两个/三个条件独立二值显性指标，参数方向A=(3/4,5/6)、B=(5/6,3/4)，第三指标固定类别1成功率3/4、类别0为1/4，独立训练个人m=2/3。完整2来源×2显性维数×2样本量，**8个人工世界、1312组有序完整人工训练数据及186种无序显性观察拟合profile**。人工源概率由潜在C显式混合及独立偶数阶指标相关展开两种Fraction算法完全相等，训练联合似然由逐个人相乘与观察向量直方图频数幂双法精确一致。固定只选A/B两候选、所有似然同分选A。未来独立新个体可见对数评分由math/Decimal双算法比较，此外只在人工已知真C标签条件下算潜在分类Brier与其理论最优风险。

**核心不可识别反例**：只有前两个显性指标时A/B联合可见PMF逐状态完全一致，任何独立样本都不能据此区分，但给定观测(X1,X2)=(1,0)，潜在C=1的真概率在A是3/8、B是5/8。因完全观测等价，训练固定选A、两真来源独立显性新个体logloss完全一样≈1.329661；若实际真源是B，人工oracle真类别Brier额外恶化1/48。加入第三个指标时两特定候选A/B观测分布可以区分，但有限训练m2/3并不保证全部正确；若把所有潜在类别标签同时0↔1互换，第三指标也仍无法打破整体标签命名不变性。严格区分可见数据预测、固定候选参数可识别、潜在类别语义识别三种层次。

[正式科研报告](R192_SCIENTIFIC_REPORT_2026-10-21.md)、[8世界全部原概率及评分结果](R192_EXACT_RESULTS.json)、[1312完整原训练记录CSV](R192_ALL_1312_OBSERVABLE_TRAINING_DATASETS.csv)、[186精确显性似然profile](R192_ALL_186_LATENT_CLASS_FIT_PROFILES.json)、[机器科学验收](R192_FINAL_MACHINE_ACCEPTANCE.json)、[原生程序及31种单测](r192_exact_two_class_latent_structure.py)、[含原协议、全部源码及结果ZIP](R192_Exact_8_Latent_Class_Worlds.zip)永久归档。[GitHub Actions39580014706](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39580014706) Python3.11/3.12各31项共62次测试和全部1312样本评分/ZIP科研验收三job全success，[原数据结果提交32dda2b](https://github.com/edwardsage419/Psychohistory-Research/commit/32dda2bfe0384b0a5982b1fd405392f30c64e0e1)。

一手依据：Lazarsfeld/Henry (1968), *Latent Structure Analysis*；[Goodman (1974)](https://doi.org/10.1093/biomet/61.2.215)。只达人工E1、E2/E3新增0，R073与PESEN v0.1冻结。下一 **R193 P2/08-017 Finite Mixture Models（有限混合模型）**。研究主线为先全部R，再分类，最后熔炼。
