# R068 正式限定结题：文化传播偏差与真人社会信息预测

结题日期 2026-10-16。按照 [研究统一六门验收标准](../../protocols/RESEARCH_ACCEPTANCE_STANDARD_V1_2026-10-16.md)，本研究对**数学机制验证＋诚实区分数据可检验性的真实社会学习预测**形成完整有界证据包，状态 **CLOSED_BOUNDED**，不是完整原创文化演化模型建立，更不是多代历史预测成功。

## 一、研究内容及可独立复核证据

1. **E1 数学机制 PASS。** 来源 Boyd & Richerson (1985)；Henrich & Boyd (1998), DOI `10.1016/S1090-5138(98)00018-X`。固定二特征人口 `p_0=0.2`、传播错误 `μ=.01`、`N=100`、成功示范 A 权重倍数 2，三规则的后期概率分别为中性 `.206`、三人多数 `.11192`、成功权重 `.3366666667`。[E1 协议](../../protocols/R068_CULTURAL_TRANSMISSION_BIAS_2026-10-16.md)、[E1 结果](R068_E1_CULTURAL_TRANSMISSION_RESULTS.json)和 [CI run 38869217831](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38869217831)：18 tests，success。它是合成数学，没有真人参数拟合。
2. **真人来源 E2 源保真 PASS。** Toyokawa & Gaissmaier (2022), eLife e75308, DOI `10.7554/eLife.75308`，原作者 GitHub 固定提交 `6fca0b26c33af3a5b3c415719fa3df0dced15149`，两个真正 LFS 实验文件 SHA/字节均通过：群体 12,880 行×57 列，个体 7,929 行×56 列。[来源门](../../protocols/R068_E2_TOYOKAWA_EXPERIMENT_LFS_SOURCE_2026-10-16.md)，[CI 38870499060](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38870499060)，13 tests PASS。两份文件是论文四选项试验部分数据，**不声称已复现全部 619 名招募者或完整实验**。
3. **时间语义 PASS。** 原作者 R `multiVar_model_fitting_both_1022.R` 明确 t 轮使用 t−1 轮各选择频率，并减去本人的上一轮。现实 184 名群体实验人、39 rooms、12674 条真实可用同伴频率（零负频率反例）、1 混合 riskID 异常房间 350 条（可评分 345），[CI 38870896074](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38870896074) 12 tests PASS。此阶段已知只有**同伴行为频率**，不直接看到其他人的 payoff；真实成功示范权重的直接实证辨识 **BLOCKED_BY_MEASUREMENT**。
4. **真实选择的整房间条件预测 PASS_BOUNDED。** 在模型真实数据损失出现前独立提交 [38 房协议](../../protocols/R068_E2_38_ROOM_FREQUENCY_HOLDOUT_2026-10-16.md)，规定完全排除唯一混合任务 room，留余 **38 rooms/12329 个前一轮可见社会频率及本人前期选择合法的人×轮观测**；每次训练另外 37 房选择固定模型网格，按四选项当前选择 NLL 计分；未将房间内的同一人时间序列拆到训练/测试。[CI run 38871373620](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38871373620) 两作业 success、18 合成测试 PASS。

| 四选项统计预测 | **38 房等权 NLL（nats）** |
|---|---:|
| 混合：上一轮惯性与社会频率 | **1.1514808469** |
| 上一轮自身选择惯性 | 1.1655191937 |
| 随机均匀四选项 | 1.3862943611 |
| 仅社会频率幂 | 1.4567653051 |

全部 38 折中，纯频率幂 θ=0 被选 9 次、θ=0.5 被选 29 次，θ>1 **无一折**；混合模型 38 折都给社会信息权重 0.25（多任务条件），说明此简化模型里社会频率只能在自己上轮状态上提供小幅增益，不表示人类没有从众。来源、模型公式、预定参数、次级任务与加权指标、有限推断见 [E2 正式审计](R068_E2_TOYOKAWA_REAL_SOURCE_AND_MODEL_AUDIT.md)和 [机器可读结果](R068_E2_TOYOKAWA_ROOM_HELDOUT_RESULTS.json)。

## 二、六项有界标准

| 门 | 状态 | 被验收的确切对象 |
|---|---|---|
| A01 问题与有限范围 | PASS | 三合成传播规则＋真实四选项社会信息条件预测；E2 协议在来源结构审计后才设计，属于回顾性方案，**不冒充原始三人从众预注册验证** |
| A02 原始来源可追溯 | PASS | 原作者论文、代码提交、两个 LFS blob 指针和真实 SHA256、时间语义 R 代码；无个体行再分发 |
| A03 计算可重放 | PASS | GitHub Actions E1、LFS 真实下载、前期选择剔除、38 房留出均真实成功，合成反例测试可复算 |
| A04 失败/测量缺口保留 | PASS | 三示范者严格多数真人不可直接对应、他人 payoff 不展示、1 混合任务房间全体排除、纯频率低于 Uniform 的负结果 |
| A05 证据推断限制 | PASS | E1 与 E2/E3 分离、38 房是统计独立单位而不是 12329 独立被试、社会信息主效应与本人数值历史/收益混淆 |
| A06 结题与后续交接 | PASS | 本文、全部源码/单测/协议、真实匿名 JSON、[未完成关口移交](R068_POST_CLOSURE_OPEN_GATES.md)，研究主线转 R069 |

六门 PASS 仅表明这项**已明示限定范围研究材料完整**。没有足够证据宣布三示范者二特征理论在真实人群中得到完整复现，也不能从当前 Bandit 试验对历史文化扩散进行因果预测。已知原作者完整层级强化学习/cmdstanr 分析并未执行；后续需另立编号。

## 三、最终判定

`R068=CLOSED_BOUNDED`；
`R068_E1_MINIMAL_MATH=PASS`；
`R068_E2_TRUE_SOURCE_TEMPORAL_AND_38_ROOM=PASS_BOUNDED`；
`R068_E1_EXACT_THREE_DEMONSTRATOR_HUMAN=NOT_ESTABLISHED`；
`R068_PAYOFF_BIAS_DIRECT_EMPIRICAL=BLOCKED_BY_MEASUREMENT`；
`R068_E3=OPEN`；
`PESEN_v0.1=FROZEN`。

下一主线研究新家族 R069：局部网络阈值传播、独立级联及群体扩散；严格区别局部选择/采纳模型与当前重复 bandit 选择，不把未观测网络边虚构给文化实验。
