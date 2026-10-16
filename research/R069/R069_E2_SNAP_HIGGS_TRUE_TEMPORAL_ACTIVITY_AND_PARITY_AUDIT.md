# R069：SNAP Higgs Twitter 原始事件时序、转发网络逐边精确复核与机制识别边界

日期：2026-10-16。研究级别：**E2 / 真实数据来源与事件可观察性校验（PASS_BOUNDED）**；**未拟合、未识别**阈值或独立级联的真实社会传播参数。R069 继续 `ACTIVE`，PESEN v0.1 继续 `FROZEN`。

## 1. 研究问题与两份来源

[Stanford SNAP 官方数据页](https://snap.stanford.edu/data/higgs-twitter.html)描述了 2012-07-01 至 07-07 希格斯玻色子发现讨论期间的社交网络、转发、回复和提及活动；官网注明 2015-03-31 更换过原件版本。论文：De Domenico, Lima, Mougel & Musolesi (2013), *The Anatomy of a Scientific Rumor*, *Scientific Reports* 3, 2980，DOI [10.1038/srep02980](https://doi.org/10.1038/srep02980)。本轮只取官网**两份**文件：

| 官方源 | 下载字节 | 实际原始 gzip SHA256 |
|---|---:|---|
| `higgs-activity_time.txt.gz` | 4,169,461 | `901b199716a23b0fc0371705e3ae9941b5c9493277aec65456abc4988674ad79` |
| `higgs-retweet_network.edgelist.gz` | 1,957,437 | `4097edebd539043cfc62d9b4ba67676f79523f6dbe896d345fcc127dec3e936e` |

原始数据的再发行授权未独立确立，只有官网公开可读并不等于可自由再分发，所以原始 gzip、用户标识、单次社交边、逐人活动与文本**均未上传**至本仓库。Actions 使用临时内存处理，仅公开匿名聚合及固定文件哈希。

## 2. 时间事件来源成功

[首次完整真实读取前冻结协议](../../protocols/R069_E2_HIGGS_TEMPORAL_RETWEET_SOURCE_GATE_2026-10-16.md) 在 commit `84e39d03b95c40403ecb9eb6def721223a28fa9c` 首次提交。执行 [GitHub Actions 38876285461](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38876285461)，两作业 success，**18 项**合成来源/时间/方向反例 PASS；官方下载 gzip、完整解压与 CRC、整数、活动类型、文件 SHA256 均成功。

真实数据：

| 活动类别 | 行数 |
|---|---:|
| RT 转发 | 354,930 |
| MT 提及 | 171,237 |
| RE 回复 | 36,902 |
| 合计互动记录 | **563,069** |

279,379 个有活动者 ID，59,977 个互动目标 ID，并集 304,691 个节点；有 RT 的独立活动者 228,556 人。官方时间窗内全部 563,069 行，最早 `2012-07-01T00:02:52+00:00`，最晚 `2012-07-07T23:59:53+00:00`。194,437 个不同整数秒，存在大量时间完全相同的事件（重复秒除首行的额外事件数 368,632）；各活动合计有 7,588 条 userA=userB 自互行，**RT 单独自互行为零**。**不能从按秒同时时间排列创造虚假的严格先行序列**。

从观测时序中可直接得到以下纯记录代理：在 354,930 条 RT 活动 `A retweets B at t` 中，有 185,484 条其 B 在严格早于 t 时曾有任一 RT/MT/RE 动作；其中仅严格更早 RT 则为 112,692 条。若限于 A 的第一次观测 RT 发生的时间戳，228,578 条这样的 RT（比 228,556 位不同 RT 活动者多 22 条同秒并发）；其中 B 曾更早 RT 的记录 59,065 条。此时序代理**只能证明表内 B 的活动时间在先**，不能证明 A 看到了 B 的哪一条 tweet 或者 A 因其而转发。

## 3. 原作者汇总转发网络不是另一份独立观测网络

从 `higgs-retweet_network.edgelist.gz` 真正读取到：**256,491 节点、328,132 条唯一有向加权边，全部权重求和 = 354,930**，与官网正式发布的节点/边统计一致。不能仅凭汇总计数相等就判断每个边已对齐。

因此本研究先独立提交[逐边核验新协议](../../protocols/R069_E2_HIGGS_ORIGINAL_RT_EXACT_PARITY_2026-10-16.md)，commit `ccf8b9867798e93681d8722b4f67816aaa3ca290`，再运行 [GitHub Actions 38876563448](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38876563448)。**13 项**合成测试通过，真实作业重新下载并按 SHA256 复核两份源，然后在**原记录动作方向** `A→B` 上逐条累计原始 RT multiplicity，与聚合边权完全比对：

| 核验字段 | 真实结果 |
|---|---:|
| 事件存在但聚合表缺失的唯一有向边 | 0 |
| 聚合表存在但事件缺失的唯一有向边 | 0 |
| 共有有向边中权重不同的边 | 0 |
| 共有边权绝对差求和 | 0 |
| 聚合文件内重复有向边 | 0 |
| 反转方向后的有向边对称差 | 653,232 |

`DIRECTIONAL_RT_MULTISET_EXACT_PASS`。精确证明这两个源是**同一批行为活动的原始时序表示和汇总表示**，而不是互相独立的人类网络实验；前一版已汇总 RT 边用于新 RT 事件预测会产生使用全窗口未来数据的信息泄漏。数据官网也明确说明 RT 行方向为**转发者 A→被转发者 B**，若讨论信息流应谨慎反向，但这并不构成真正观察到谁给谁传播/消息继承的全部路径。

所有原始 ID 仅在 runner 处理，不在报告中输出任何边/人级数据。完整数值见 [R069_E2_SNAP_HIGGS_ORIGINAL_SOURCE_AND_RT_PARITY_RESULTS.json](R069_E2_SNAP_HIGGS_ORIGINAL_SOURCE_AND_RT_PARITY_RESULTS.json)。

## 4. 科学上不可成立的主张及下一关口

- **观察到**谁转发了谁、在何秒有转发；**没有观察到**某条消息/原帖 ID 的完整沿边谱系，也没有观察转发失败的全部暴露机会。因此不能拟合并宣称获得 IC 每次独立传播尝试成功概率。
- 转发网络由全部事件生成，并不是外生的**事件前**好友图。SNAP 另提供大型 `social_network.edgelist.gz`，但它也是没有关系建立时间的快照；本轮基于资源/边界没有下载 1480 多万条关系，更不能声称它具有逐日先验的真实关注网络。
- 单个话题的相近同时转发不等于心理阈值，可能由新闻公告、平台推荐、媒体大事件共同驱动。论文对整体活动的原始时空建模不等于本轮 E1 Watts/IC/Bass 模型已校准。
- 563,069 条是**定向 RT/MT/RE 互动边记录**，不是论文列出的所有 985,590 条相关 tweet，也不是同样数量的独立用户。因一个用户/秒/行为可能重复，不能以总事件数作为独立推断样本。
- 模型比较若继续，必须新冻结时间切分与有效的竞争基线，禁止将**全时间聚合 RT 边图**当作预测输入；若无真实完整风险集、实验性暴露或历史有效的外部邻接，最多得到有限条件性行为预测，而不是因果网络级联机制辨识。
- 原始 SNAP 官网并未提供确切适用于这两 gzip 的再发行许可；本研究保守遵守仅匿名科学结果公开。

## 5. 验收与当前状态

`R069_HIGGS_E2_ORIGINAL_SOURCE_SHA=PASS`；
`R069_HIGGS_E2_ORIGINAL_RT_EVENT_AGGREGATE_EXACT_PARITY=PASS`；
`R069_HIGGS_EVENT_ORDER_PROXY=PASS_BOUNDED`；
`R069_TRUE_RETWEET_TWEET_ID_CASCADE=NOT_OBSERVED`；
`R069_TRUE_EXPOSURE_FAILURE_RISK_SET=NOT_OBSERVED`；
`R069_REAL_IC_AND_WATTS_CAUSAL_PARAMETERS=NOT_IDENTIFIED`；
`R069_E3_EXTERNAL=OPEN`；
`R069=ACTIVE`；
`PESEN_v0.1=FROZEN`。
