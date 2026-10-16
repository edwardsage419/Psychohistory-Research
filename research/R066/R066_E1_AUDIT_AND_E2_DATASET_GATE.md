# R066 第一阶段：三类群体意见形成模型的合成机制校验与经验数据入口

日期：2026-10-16。研究方向：从 R065 的个体观察性社会学习转入群体层互动与意见动力学。R066 状态：**ACTIVE**，当前完成等级 **E1**，经验性预测门继续 OPEN。

## 已完成：三类模型的数学基线

研究协议 [R066_OPINION_DYNAMICS_THREE_MODELS_2026-10-16.md](../../protocols/R066_OPINION_DYNAMICS_THREE_MODELS_2026-10-16.md) 在本阶段计算结果生成前已提交，commit `b7bce5a51002add42de69af23849eea85c3f6e1d`。

原始文献：
- Morris H. DeGroot (1974), *Reaching a Consensus*, JASA 69(345):118–121，DOI 10.1080/01621459.1974.10480137；线性加权共识模型。
- Noah E. Friedkin & Eugene C. Johnsen (1990), *Social influence and opinions*, Journal of Mathematical Sociology 15(3–4):193–206，DOI 10.1080/0022250X.1990.9990069；在社会影响中保留初始意见锚定。
- Rainer Hegselmann & Ulrich Krause (2002), *Opinion dynamics and bounded confidence: models, analysis and simulation*, JASSS 5(3)，[出版方原文入口](https://www.jasss.org/5/3/2.html)；界限内同步平均意见机制。

代码 [r066_three_opinion_models.py](r066_three_opinion_models.py) 采用标准库纯 Python，无网络/随机依赖；[25 项边界/机制测试](test_r066_three_opinion_models.py) 校验行随机矩阵、越界/非有限参数拒绝、模型退化一致性、HK 同步性、对特殊矩阵是否收敛的正确边界。

[GitHub Actions run 38845611874](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38845611874) 已 completed/success。执行日志显示 **Ran 25 tests / OK** 与实际三模型固定基线计算结果；聚合数字永久保存 [R066_E1_THREE_MODEL_RESULTS.json](R066_E1_THREE_MODEL_RESULTS.json)。每种模型输入同一 3 名代理初始意见 `[0,0.2,1]`；对于 DeGroot/FJ，W 各元素 1/3，FJ 易感性 0.5；HK 置信半径 0.25。

| 模型 | 第一轮更新后意见 | 该固定例子的结果形式 |
|---|---|---|
| DeGroot | [0.4,0.4,0.4] | 一步完全共识 |
| Friedkin–Johnsen | [0.2,0.3,0.7] | 保留初始意见差异 |
| Hegselmann–Krause | [0.1,0.1,1.0] | 两类分离群体 |

此表只有 **E1 合成机制证据**。这些结果只是选定参数下公式的数值后果，不意味着社会实际会如此变化、不能排除同样行为可由不同机制生成、更不能升级历史演化模型。

## 新候选经验来源：Monti 等 2020 年社会互动痕迹数据

已通过 GitHub 连接器核对 [作者公开仓库 corradomonti/learnable-opinion-dynamics](https://github.com/corradomonti/learnable-opinion-dynamics)，固定 `master` commit `5d31ba59e716e5bde85e4c56b9cdacc3920aaaf6`。项目 README 说明论文 *Learning Opinion Dynamics From Social Traces*（KDD 2020），具有 375 名按作者特定发言阈值筛选的 Reddit 用户、2008–2017 年按月索引的回复网络与社区参与。源数据集在该仓库 `data/reddit` 下，现已核对存在下列固定 Git blob，但**尚未读取原始压缩内容和完成行为变量验证**：

| 文件 | 来源 Git blob | 字节 |
|---|---|---:|
| `edges_user.tsv.bz2` | `e2e261b123963b257ed126a66b101fbaef6f937d` | 321422 |
| `edges_feature.tsv.bz2` | `12b6d3f407697e593bc368b9cd65fca1bfd7ce2d` | 490710 |
| `feature_scores.tsv.bz2` | `6c7d8a9e63d9860541d24b1c25c45d1cc2b8c565` | 776604 |
| `interaction_scores.tsv.bz2` | `18e367869399850fb4a1f28659a4b375e2ed43a1` | 1922336 |

**测量警告：** 用户回复、社区参与、帖子获赞数量是社会互动痕迹，**不等于直接观测到的个人意见连续分数**。因此该候选来源虽有时序与网络信息，也不能在未经额外测量定义和因果假设的情况下，直接当作 DeGroot/FJ/HK 的可观测意见真实值。项目代码许可 GPL-3.0，并不自动解决 Reddit 数据个人隐私、再分发、测量有效性问题；在未核验具体约束前，只存项目元数据及 blob，不复制任何原始帖子、用户 ID 或逐用户交互数据到本研究仓库。

**下一门：** 先做数据字节/字段/授权与潜在意见代理测量审计。若无法得到足够可信的重复意见测量、交流网络、时间序列及不泄漏的训练/测试界线，则标记 `EMPIRICAL_MODEL_DISCRIMINATION=BLOCKED` 并选择另一数据源，而不是用 E1 模拟宣传真实性。

`R066_E1=PASS`；`R066_EMPIRICAL_E2=OPEN`；`R066_INDEPENDENT_E3=OPEN`；`PESEN_v0.1=FROZEN`
