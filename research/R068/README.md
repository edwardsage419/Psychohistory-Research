# R068：文化传递偏差、社会模仿与有限群体随机漂变

研究开始：2026-10-16。**当前状态：ACTIVE；E1 数学机制 PASS，真实行为 E2 OPEN，外部独立 E3 OPEN。** 接替 [R067 正式限定结题](../R067/R067_FINAL_ACCEPTANCE_AND_CLOSURE_2026-10-16.md)，研究全新文化演化机制族，不再扩张单项二策略博弈研究。

## 原始文献与机制

- Robert Boyd & Peter J. Richerson (1985), *Culture and the Evolutionary Process*，University of Chicago Press。出版方原文目录明确区分文化传递、频率依赖偏差和间接模仿，研究是文化演化理论，不是历史预测实证。
- Joe Henrich & Robert Boyd (1998), *The Evolution of Conformist Transmission and the Emergence of Between-Group Differences*，*Evolution and Human Behavior* 19(4):215–241，DOI [10.1016/S1090-5138(98)00018-X](https://doi.org/10.1016/S1090-5138(98)00018-X)。

[事先冻结的 R068 数学研究协议](../../protocols/R068_CULTURAL_TRANSMISSION_BIAS_2026-10-16.md) · [独立可执行 Python 程序](r068_cultural_transmission.py) · [18 项边界/公式/反例测试](test_r068_cultural_transmission.py) · [机读匿名数学结果](R068_E1_CULTURAL_TRANSMISSION_RESULTS.json)。

## 已真实完成的数学基线

[GitHub Actions run 38869217831](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38869217831) `completed/success`，18 tests OK。在固定初始文化特征比例 `p=0.2`、对称传播错误 `μ=0.01`、有限样本 `N=100`、成功示范相对权重 2 下：

| 传播机制 | 选择后特征 A 原始概率 | 对称错误后概率 | 100 人抽样的频率方差 |
|---|---:|---:|---:|
| 中性随机复制 | 0.2 | 0.206 | 0.001635640 |
| 3 个示范者中的多数从众 | 0.104 | 0.11192 | 0.000993939 |
| 成功加权示范复制 | 1/3 | 0.336667 | 0.002233222 |

这组对照展示：**相同初始文化比例与相同变异率**，不同学习规则可产生相反方向的特征扩散，即从众倾向压低稀有特征，成功加权提升获得优势的特征。这里简单三人多数是对 Henrich–Boyd 更复杂模型的限定示例，不代表其论文中每项推导、空间扩散与实验已经复制。

有限样本方差 `q(1−q)/N` 是事前假设的独立二项抽样理论量，**不是现实人类群体的抽样方差或估计的社会统计量**。没有任何人类文化传播数据用于校准或验证；因此目前证据仅为 E1。

## 下一 E2 研究关口

优先查找同时观察：学习者文化特征/选择、候选示范者出现的特征频率、不同示范者可观察的表现或成功反馈、重复学习的时序数据集。只有具备这些识别条件，才能区分中性复制、从众学习和成功偏好，而不是仅凭群体频率变化宣称具体心理机制。相关 E2 若不可获取则保持 OPEN，另立期限明确的封闭验收范围，避免阶段编号继续膨胀。

`R068_ACTIVE=YES`
`R068_E1=PASS`
`R068_E2=OPEN`
`PESEN_v0.1=FROZEN`
