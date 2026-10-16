# R068：文化传递偏差、社会模仿与有限群体随机漂变

研究开始：2026-10-16。**当前正式状态：R068=CLOSED_BOUNDED（2026-10-16），E1 合成机制 PASS、E2 真实四选项留房预测 PASS_BOUNDED、E3 OPEN。** 接替 [R067 正式限定结题](../R067/R067_FINAL_ACCEPTANCE_AND_CLOSURE_2026-10-16.md)，研究全新文化演化机制族，不再扩张单项二策略博弈研究。

**正式结题与来源证据总入口：** [六门结题报告](R068_FINAL_ACCEPTANCE_AND_CLOSURE_2026-10-16.md) · [机读状态](R068_FINAL_ACCEPTANCE_STATUS.json) · [保留的开放科学问题](R068_POST_CLOSURE_OPEN_GATES.md)。早期文内 E2「待开展」只是研究开始时的状态，已被下面真实来源与实验补充。

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


## 真实 E2：先校验作者 LFS，再读懂前一轮信息，最后整房间留出（已完成）

- Toyokawa–Gaissmaier 2022，作者固定 Git `6fca0b26c33af3a5b3c415719fa3df0dced15149`，真正 Git LFS 实验表格经 SHA256 对齐：群体 12880×57、个体 7929×56；[来源 CI 38870499060](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38870499060) 成功、13 tests。
- [时间来源与语义结果](R068_E2_TOYOKAWA_SOURCE_TEMPORAL_RESULTS.json)：群体 184 人/39 rooms，上一轮同伴选择计数按原作者源码减去本人上一轮选择，可得 12674 条合法有同伴信息观测；原作者报告的 1 个混合任务房间保留异常并整房间排除；[CI 38870896074](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38870896074) 成功、12 tests。
- [正式 E2 详细审计](R068_E2_TOYOKAWA_REAL_SOURCE_AND_MODEL_AUDIT.md)及[全部匿名得分](R068_E2_TOYOKAWA_ROOM_HELDOUT_RESULTS.json)：先冻结 38 房间完整留出协议，每折仅其他 37 房训练模型网格，评价 12329 条有可见频率及前期个人选择的当前四选项选择。[真实 CI run 38871373620](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38871373620) 全成功、18 tests。38 房等权 NLL（越低越好）：混合 `1.15148`、自身上轮惯性 `1.16552`、Uniform `1.38629`、仅社会频率 `1.45677`。强频率强化 θ>1 在后者 38 折**从未被训练选中**。
- **重要边界：** 真实实验是四选项、非固定三人示范者，且仅展示同伴选择频率，不能直接证明 E1 三人多数或 success-weighted copying。纯社会频率不佳也不能否认作者更丰富的个人强化学习与群体社会学习解释；完整 cmdstanr/WAIC、外部 E3、多代文化历史均 OPEN。研究依照六门统一标准 `CLOSED_BOUNDED`，PESEN v0.1 保持 `FROZEN`。后续主线是 R069 网络局部阈值/级联机制。
