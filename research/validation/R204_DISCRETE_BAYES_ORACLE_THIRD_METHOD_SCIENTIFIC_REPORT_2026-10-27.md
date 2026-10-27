# R204 第三方法：真实离散源条件贝叶斯风险与高斯过程工作核预测差异

日期：2026-10-27。性质：正式 R204 有界 E1 结题后的新研究增量，原验收不变。先冻结协议：[R204 离散 Bayes 协议](../../protocols/R204_DISCRETE_BAYES_ORACLE_THIRD_METHOD_PRESCORE_FREEZE_2026-10-27.md)，提交 1fa4b015d3be86ad5f08ee4b250c81c79c9e8c63。

## 研究方法和来源

固定原 R204 的四种有限人工真实源 IID、CONSTANT、ALTERNATING、LINEAR，三种留出位置 EXTRAPOLATION、INTERPOLATION、GAP，原来源 912 条，12 个世界。每条源由独立等概率 ±1 潜在因子与三个独立 ±1 观察噪声生成。训练只使用三个已观察位置的 y，评价两个留出位置的真实潜在 f。原研究的高斯工作核选择和 GP 后验均值规则、参数、位置和同分顺序全部保持不变。

新增已知真实离散源条件下的最优平方损失预测 E[f*|y, source]，使用同一个可见 y 的原来源分组精确计数。该 Bayes oracle 的源身份为评价者已知，不能直接作为真实未知机制的部署模型。分别比较原训练选核 GP、原已知真核最优线性 GP、零预测和真实离散 Bayes。使用 Python 标准库 Fraction 无抽样计算，原 R204 12 世界已归档风险全部逐 Fraction 回归一致。

## 全部世界的新结果

| 留出布局 | 真实源 | 离散 Bayes 风险 | 已知真核 GP 线性风险 | 训练选核 GP 风险 |
| --- | --- | ---: | ---: | ---: |
| EXTRAPOLATION | IID | 1 | 1 | 127/72 |
| EXTRAPOLATION | CONSTANT | 1/8 | 1/4 | 499/288 |
| EXTRAPOLATION | ALTERNATING | 1/8 | 1/4 | 289/288 |
| EXTRAPOLATION | LINEAR | 0 | 5/12 | 587/288 |
| INTERPOLATION | IID | 1 | 1 | 14065/10368 |
| INTERPOLATION | CONSTANT | 1/8 | 1/4 | 17/32 |
| INTERPOLATION | ALTERNATING | 1/8 | 1/4 | 89/32 |
| INTERPOLATION | LINEAR | 0 | 1/9 | 1/9 |
| GAP | IID | 1 | 1 | 1191/800 |
| GAP | CONSTANT | 1/8 | 1/4 | 17/32 |
| GAP | ALTERNATING | 1/8 | 1/4 | 25/32 |
| GAP | LINEAR | 0 | 1/20 | 1/20 |

12 个世界的训练选核 GP 风险全部严格高于真实离散 Bayes；已知真核 GP 线性预测在 9 个世界仍严格高于真实离散 Bayes；零预测在 9 个世界严格高于 Bayes。IID 源的三个布局无法从独立训练位置预测未观测位置，Bayes 风险仍为 1。CONSTANT 与 ALTERNATING 的已知源离散 Bayes 风险为 1/8，GP 线性为 1/4。LINEAR 的三个布局离散 Bayes 风险均为 0：在已知源与冻结的 ±1 支持下，训练观测可精确恢复隐藏因子；GP 错设高斯收缩依然留下误差。

每个可见 y 组均检验 E[f*−E(f*|y)|y]=0。对所有 12 世界、GP 选核、已知真核 GP 与零基线均严格验证平方损失正交分解 R(g)−R(Bayes)=E[||g(y)−E(f*|y)||²]/2。各组概率归一。可见 y 的不同取值数分别为 IID 27、CONSTANT 15、ALTERNATING 15、LINEAR 16，三个位置布局均如此。

## 可复算性与科学边界

[可执行 R 脚本](r204_discrete_bayes_oracle_20261027.py)；[12 世界精确 JSON 收据](R204_DISCRETE_BAYES_ORACLE_12_WORLDS_EXACT_RECEIPT_2026-10-27.json)。本地标准库执行 `--test` 通过，重新计算 912 条原来源并验证全部原 R204 风险。B 轨独立因子卷积及条件二阶矩复算另见审计报告。新增计算属于内部 E1 扩展，未新增真人 E2、历史 E3、外部研究者独立复现。高斯核矩阵与离散源仅共享二阶矩，已知源 Bayes 风险优势不能解释为现实心理状态可观察。R073 模型与评分规则及 PESEN v0.1 均保持冻结。

方法来源：Rasmussen and Williams (2006), Gaussian Processes for Machine Learning, Chapter 2, https://gaussianprocess.org/gpml/chapters/RW2.pdf。原始冻结来源见 [R204 正式报告](../R204/R204_SCIENTIFIC_REPORT_2026-10-21.md)。
