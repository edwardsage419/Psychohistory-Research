# 心理史学原239候选：R299无模型时序差分、R300隐藏马尔可夫过滤的独立E1研究与v1.4证据追踪

日期：2026-10-23 Asia/Taipei。落实用户研究顺序：**完成全部R系列原候选的学习和分级验收→统一归纳分类→最后熔炼原创模型**；个人辅助决策系统继续暂缓。此次两项正式限定研究均为**E1精确人工数学**，无新真人/动物E2，无历史E3，原239整体科学结题**尚未成立**。

## 1. 本轮两项已独立验收的研究

| 项目、原候选ID | 先行冻结提交 | 完整人工原source | Python3.11/3.12各主模型单测 | 独立三job科学CI |
|---|---|---:|---:|---|
| R299 Model Free RL, 02-005 P1 | [f8885c13](https://github.com/edwardsage419/Psychohistory-Research/commit/f8885c130b2d6d12280cd6ace30085b3ad90e835) | 120状态（24世界×5轮） | 492+492 | [39927231561](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39927231561) SUCCESS |
| R300 Hidden Markov Model, 02-008 P1 | [ef56b01c](https://github.com/edwardsage419/Psychohistory-Research/commit/ef56b01c3c2b5da98e433f9d2fefdd61fd9028c3) | 128观测前缀（2模型×16完整字符串×4前缀） | 394+394 | [39927762571](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39927762571) SUCCESS |

两个研究合计**248条人工source行**，而非248位被试/248个独立抽样轨迹；Python3.11+3.12主模型合计**1772项实际unittest通过**，再加每研究双版本各16项独立来源逆向审计及第三作业完全独立重建。两项均固定精确Fraction计算、CSV完整原source、完整结果JSON、SHA256机读凭证及独立审计代码；R299原source永久Git commit [8f74e565](https://github.com/edwardsage419/Psychohistory-Research/commit/8f74e56573be6a9fde21e12bb886c9f041d3f74b)；R300归档[38830d98](https://github.com/edwardsage419/Psychohistory-Research/commit/38830d98e6c12c891e5fc542903b39ca6976f4ec)。

### R299：模型无关预测、延迟信用分配，不迁移R063实证

原作者Sutton(1988) *Learning to Predict by the Methods of Temporal Differences*, DOI https://doi.org/10.1007/BF00115009。只用固定策略两步状态转移经验，TD(0)在状态S0以**此前**S1估值自举，Monte Carlo在回合结束后使用全部真实回报；R=2、γ=α=1/2、四次训练后：TD预测S0=**11/16**，MC预测S0=**15/16**，S1共同=15/8，真回报S0=1。此例说明在指定时序下较早状态的奖赏信用传播会延迟，**不说明MC在所有任务中预测性能优于TD**；本研究没有优化动作或学习环境模型。

[详细科学报告](../research/R299/R299_SCIENTIFIC_REPORT_2026-10-23.md)、[120原人工状态](../research/R299/R299_ALL_120_ORIGINAL_MODEL_FREE_TD_MC_STATES.csv)、[真实结果与机器验收](../research/R299/R299_FINAL_ACCEPTANCE_STATUS.json)。

历史[原R063审计](../research/R063/R063_EVIDENCE_AUDIT.md)属于Najar等(2020)社交模仿学习的metaVS/VS2作者代码与Fig6参数汇总检查；并未在原完整trial CSV本地重算后完成独立预测关口。R299通用TD/MC数学机制**不能挪用R063真人报告作为新增人类模型E2**。v1.3将02-005从仅有R063有限资料关联变更为专属R299有界数学主R；旧R063证据路径仍原样保留。

### R300：HMM隐状态推断、历史依赖及无记忆负对照

原作者Rabiner(1989) *A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition*, DOI https://doi.org/10.1109/5.18626。两个二元隐状态/观测人工模型共128条source，隐藏状态持续概率3/4或1/2（潜在状态i.i.d.），发射正确率3/4，先验各1/2。独立审计逐原source穷举全部潜在路径，直接验证HMM前向递推得到的观测证据、末端潜在后验及下一观测预测；每模型每时长的**不重复前缀概率和**精确为1。

持续隐状态模型：观察1110后末期隐藏1的后验=**19/46**，观察0000后=**3/22**，相应预测下一观察1概率=11/23、9/22。两条历史最后一位均为0，仍携带不同跨期信息。i.i.d.潜在模型对两条历史的当前潜在1后验均为1/4，下一观测1预测均1/2。此结果**没有从人类数据拟合转移或发射参数、不能确认心理学隐藏状态的客观存在、不包含Baum–Welch和Viterbi原始实测结果**。

[详细科学报告](../research/R300/R300_SCIENTIFIC_REPORT_2026-10-23.md)、[128原人工来源](../research/R300/R300_ALL_128_ORIGINAL_HMM_PREFIX_SOURCES.csv)、[真实结果与正式机读验收](../research/R300/R300_FINAL_ACCEPTANCE_STATUS.json)。

## 2. 原始239项证据索引 v1.2→v1.3→v1.4

| 来源状态 | v1.2（R298后） | v1.3（R299后） | v1.4（R300后） |
|---|---:|---:|---:|
| 已有候选主R研究来源 | 186 | 187 | **188** |
| 共享早期有限数学，无专属新主R | 3 | 3 | **3** |
| 仅有旧范围有限审计关联 | 5 | 4 | **4** |
| 已查材料没有逐项主R联系 | 45 | 45 | **44** |
| 原候选主R待核关联 | 50 | 49 | **48** |
| 原始唯一候选总数 | 239 | 239 | **239** |

[最新v1.4所有239条完整来源交叉索引](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.4_2026-10-23.json)相对[v1.3](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.3_2026-10-23.json)**仅02-008单行变更**，此前v1.3相对v1.2仅02-005单行变更。原239目录、优先级、名称、顺序均保持；相邻02-003 R297、02-004 R298、02-005 R299的独立验收归属保留，特别是R063旧有限证据路径持续可追溯。**188个主R来源关联是来源追踪完整度，不是188个原论文已经被独立真人实证复现**。

[最新剩余48候选主R关联核查队列](ORIGINAL_239_PENDING_48_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv)，P1 **21**，P2 **27**；缺乏当前链接既不说明从未研究，也不表示科学理论被证伪。

四个真实GitHub Actions工作流共12个成功job：
* [R299研究CI39927231561](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39927231561)、[R299 v1.3目录CI39927488591](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39927488591)，后者双Python各16条目录来源测试+第三原数据SHA重放，特别检查R063历史链接；
* [R300研究CI39927762571](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39927762571)、[R300 v1.4目录CI39928010621](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39928010621)，后者双Python各16条目录验证+第三独立128源隐藏路径审计，确认只有02-008变更。

**结论**：两项有界人工E1均已按冻结协议正式验收，材料与源码永久归档；全部239科研结题仍未成立。R073/PESEN v0.1冻结，无新E2/E3。

## 3. 下一研究

下一条P1原候选编号**02-012 Bayesian Change Point Detection**。研究前应检查早期信念更新、贝叶斯滤波及灾变变化相关R系列是否已经提供逐项证据；随后冻结观测序列、hazard参数及change-point run-length后验的精确穷举，避免将合成变点检测视为真实历史预报。保持全部R→统一分类→最后原创熔炼的既定顺序。
