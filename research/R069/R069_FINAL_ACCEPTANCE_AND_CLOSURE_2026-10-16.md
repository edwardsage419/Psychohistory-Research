# R069 正式有界结题：网络阈值、独立级联、Bass 与真实社交活动的可验证边界

2026-10-16。统一验收依据 [研究验收标准 V1](../../protocols/RESEARCH_ACCEPTANCE_STANDARD_V1_2026-10-16.md)。本报告对**E1 数学反例＋真实来源结构审计＋跨日有限行为预测**结题，状态 **CLOSED_BOUNDED**。**不**声称 E1 三扩散模型在真人数据上进行了真实机制拟合，不将在线标签/转发活动升级成“信息采纳”“独立边感染”或“政策传播效果”。

## 一、已经实际执行的证据链

1. **E1 数学可重放 PASS**。冻结 [三机制研究协议](../../protocols/R069_NETWORK_CASCADE_THREE_MECHANISMS_2026-10-16.md)，6 节点固定路径同步阈值、全部 32 个独立级联活边情形精确穷举和 Bass Euler 新产品采纳宏观近似。阈值 0.5 传播全 6 节点、0.75 不扩散；IC β=0.5 期望最终 1.96875 节点；Bass 固定初态第 5 步比例 0.6807123。 [GitHub Actions run 38872162843](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38872162843) 真正执行，22 tests PASS。[E1 数值 JSON](R069_E1_NETWORK_CASCADE_RESULTS.json)。
2. **真实来源 HetRec E2 / 负时间戳与不可能日期**：从官方 GroupLens HetRec Last.fm ZIP 下载、MD5 和 SHA256 固定。1892 名源网络用户、12717 条对称好友关系，186479 条网站艺术家标签；最初严格审计因为 4 条负时间戳 FAIL，独立诊断后先冻修订协议，只剔除 4 条时间异常参与时间排序，正式 run 38874783610 PASS。又检测 1 条 1979 年正时间明显早于 Last.fm 2002 年启动，以单独日期敏感性协议过滤后先行好友标签代理保持 **11602 / 71062**。原始失败仍记录，不能将这项回顾性好友在先视为感染。[HetRec 真实性与阻塞审计](R069_E2_HETREC_SOURCE_AND_IDENTIFICATION_AUDIT.md)及[机器结果](R069_E2_HETREC_REAL_SOURCE_AND_TIME_PROXY_RESULTS.json)。
3. **真实来源 SNAP Higgs 2012 事件 E2**：源自 Stanford SNAP 官方，563069 条 2012 年 7 月 1–7 日 A→B 事件（RT 354930、MT 171237、RE 36902）。gzip SHA256 和真正 gzip 内容可验证；[run 38876285461](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38876285461) 两作业成功，18 tests PASS。原来的加权转发汇总图有 328132 条唯一有向边，所有权重总数 354930；**逐边**与原始每对 (A,B) 的 RT 次数完全相同，缺失/多余边均为 0、权重差异均为 0，[run 38876563448](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38876563448) 13 tests PASS。这意味着 RT 汇总网络不能当作独立事前曝光网络。[SNAP 来源与 parity 审计](R069_E2_SNAP_HIGGS_TRUE_TEMPORAL_ACTIVITY_AND_PARITY_AUDIT.md)。
4. **真人 SNAP 四个未来日行为预测 E2 / 有限对照 PASS_BOUNDED**：在任何真实损失产生前提交[跨日留出协议](../../protocols/R069_E2_HIGGS_FORWARD_DAY_RT_2026-10-16.md)，commit `730ce9639c86f08ca772ebd2b7fd3ce6844b487c`。当日 00:00 前曾发起 RT/MT/RE 的账户才进入风险集，2012-07-02/03 是最初训练标签窗口，固定评估 7 月 4–7 日；每个测试日仅看过去观测的个人历史、以前互动对象的**前日 RT**，不读取完整 7 日 RT 聚合关系作预测输入。4 日共 763846 个**重复账户日**观测，绝不是独立个体数。[正式真实数据结果 JSON](R069_E2_HIGGS_FORWARD_DAY_RT_RESULTS.json)与[详细审计](R069_E2_HIGGS_FORWARD_DAY_RESULTS_AUDIT.md)。

| 未来日的预测方法 | 四天等权二元 logloss nats | 四天等权 Brier |
|---|---:|---:|
| 历史训练总 RT 率 | **0.3654034** | **0.1070849** |
| 训练中昨天的 RT 率 | 0.3668847 | 0.1133377 |
| 历史个人活跃度分组 | 0.3738350 | 0.1105265 |
| 历史活跃度＋以前互动对象上日 RT 代理 | 0.3749479 | 0.1114940 |

**简单个人活动＋历史对象 RT 代理没有提供正向样本外增益。** 历史总体率最小，但这一结果不能推断“没有社会扩散”。一个关键外推问题：**单 7 月 4 日共有 143001 名当天 RT 人此前没有作为 A 发起行为，因而被完全排除出当天预测风险集**。对首次出现的用户、外部新闻冲击或未观察到曝光者无预测覆盖。只有 4 个日期，不做虚假的 763846 独立观测显著性推断。

首次 GitHub Actions [38878398763](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38878398763) 的真实数据作业成功但 22 项合成测试中 1 项断言错误，总体结果 FAIL；测试断言被单独修复于 commit `f9f9508ac954f7c5a2f163ede9407a944d70eb7e`，真实算法不变。[GitHub Actions run 38878472077](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38878472077) **双作业 success、22 tests PASS**，首次失败作为可审计记录保留。

## 二、统一六项形式验收（限已完成科学对象）

| 科学交付门 | 判定 | 必须区分的限制 |
|---|---|---|
| A01 问题和范围 | PASS | 三个 E1 数学机制、两真实原始来源、一个滚动在线行为预测；完整真实 Watts/IC 机制因果验证明确不在有界结题范围 |
| A02 原始来源与测量 | PASS | HetRec 原 ZIP 哈希；Higgs 官方 2 gzip 精确字节 SHA256；原始 RT 到汇总 RT 边逐边完全一致；4 条负时间/1 条 1979 年异常保留 |
| A03 程序可执行可重放 | PASS | 5 个成功或失败但留证的阶段核验流程、标准库纯 Python、全程 GitHub Actions 实际公开源执行、所有适用反例测试 |
| A04 负面/阻塞结果 | PASS | HetRec 初次源失败、跨日期代码测试失败、Higgs 纯个体/社交代理比总率预测差、首次 RT 用户未覆盖、大型网络的未来泄漏风险 |
| A05 证据级别和推断 | PASS | E1、E2、E3 分别登记；有时戳的 RT≠真实曝光机会≠首次信念采纳，历史好友图/全周期 RT 聚合不是事前网络 |
| A06 交接和正式存档 | PASS | 本文、可执行代码及测试、原始来源和聚合 JSON、独立冻结协议及[未完成问题](R069_POST_CLOSURE_OPEN_GATES.md)，下一模型家族转 R070 |

六门 PASS **仅代表本有界研究包及科学负结果已得到完整审计**，不是“真实 Watts/IC/Bass 三机制全部 empirically validated”。

## 三、关闭范围与延续工作

**R069=CLOSED_BOUNDED**；E1 网络三机制数学 PASS；E2 真实来源、逐边网络加工保真、时序代理、四天条件预测 PASS_BOUNDED；**Watts/IC/Bass 真实因果识别 BLOCKED_BY_MEASUREMENT**；真人社交图的历史有效边、每次传播失败暴露风险集、真实首次采纳、外部 E3 与跨历史制度演化均 OPEN。参见 [后续研究阻塞清单](R069_POST_CLOSURE_OPEN_GATES.md)。

后续研究主线 R070 建议换到规范形成/制度约束与群体合作的可计算机制，**不把先前的社交活动代理作为新增因果证据**。PESEN v0.1 保持 `FROZEN`。
