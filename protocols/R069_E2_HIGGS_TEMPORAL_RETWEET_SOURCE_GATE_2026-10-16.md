# R069 E2：SNAP Higgs 2012 原始事件时间与转发网络来源关口

日期：2026-10-16。**首次下载两份 SNAP 完整 gzip 文件、读取真实事件之前冻结**。这是在 R069 HetRec 非因果测量审计之后的新独立公开来源。范围只限来源、匿名统计、时间先后可识别性；**不**拟合 Watts 阈值、独立级联 IC 的因果传播概率，也**不**宣布信息采纳。

## 来源与事先确认的版本限制

Stanford Network Analysis Project (SNAP), [Higgs Twitter Dataset](https://snap.stanford.edu/data/higgs-twitter.html)；相关论文 De Domenico et al. (2013), *The Anatomy of a Scientific Rumor*, *Scientific Reports* 3:2980, DOI `10.1038/srep02980`。官网声明原始收集区间为 **2012-07-01 至 2012-07-07**，来源资料**2015-03-31 更新**，要求使用更新版，不可把此前或别站镜像数字硬当作同版事实。

**仅下载两个官方完整原件：**

- `https://snap.stanford.edu/data/higgs-activity_time.txt.gz`：每行为 `userA userB timestamp interaction`，类型 RT / MT / RE。方向是活动人 A 指向被转发/提及/回复者 B；若讨论消息来源方向，RT 必须审慎反转，不能直接把 A→B 当作消息 B 被 A 感染的方向。
- `https://snap.stanford.edu/data/higgs-retweet_network.edgelist.gz`：有向有权重的聚合转发关系。它与上面时间事件是**同一观测活动的汇总层**，不属于预先存在的外生好友网络；不得当独立预测网络、不得利用完整聚合权重预测事件期初采纳。

官网另有 `higgs-social_network.edgelist.gz`，456,626 节点 / 14,855,842 边，为**超大静态快照**且建边时间未知。本关不下载它，避免 10+ million 边耗费且无新增的因果暴露信息。没有正式许可证信息就不再发行原作者 gzip、单人活动、匿名原始 IDs。

## 强制运行界限及匿名字段计数

1. 官方 gzip HTTP(S) 请求使用超时 35 秒和最多 80 MiB 压缩字节；stream gzip 解码活动表最多 5,000,000 行（每行长度上限 200），聚合有向有权图最多 2,000,000 行；只认按官网定义的空格分隔列，允许 `#` 注释和空行，其他行形状不符 / 非整数 / 负 user ID / 未知 RT、MT、RE：fail-closed。初始输出官方文件压缩字节 SHA256 和长度作为该实际获取版的**首次精确源指纹**；再次重放必须同时校验 sha256，不允许换镜像。
2. 分别统计三活动类型行数、唯一活动者数、唯一被互动目标数、最早/最晚 UTC 日期、落在 2012-07-01T00:00 至 2012-07-08T00:00 UTC **以外**的行数（不能静默排除）、自环、相同时刻量，以及以人为单位最早 RT 的统计总数；只存匿名聚合，不输出真实活动边/用户标识/单人时间线。
3. 对每个来源 RT `A retweets B at t`，统计 B 在此记录前已有**严格更早任何类型互动活动**、**严格更早 RT 活动**的事件数，以及“每位 A 的首次 RT”的上述先行关系计数。这只是**记录中可见的 earlier-activity proxy**，不是 A 实际看到 B 帖文的证据，更不能声称此次 RT 真正转自 B 的这条早期记录。
4. 验证汇总 retweet network 表含按方向的两整数 ID 与正权重；记录总行数、唯一边数、用户覆盖、权重和、是否存在同一有向对重复行。可以将其与活动 RT 数做**非强制差异报告**，但不强加同一性（发布流程可能去重/过滤）。禁止按错误假定“原先朋友边”对该层拟合独立级联。
5. 服务器不可达/超过上限/文件格式变化/源哈希无法获知，记录真实错误码和 `SOURCE_UNRESOLVED`，不伪称源完整。对于 gzip 的空文件、损坏 CRC、超长展开行 fail-closed。限制输出为一份 JSON，并用 GitHub Actions 保留匿名 aggregate artifact；不得再发行活动表、user IDs。

## 独立科学断言

转发是**被观察到的特定在线行为**，不是“一条传播尝试是否失败”或第一次相信希格斯新闻，更不自动意味着一个来源用户在本研究观测期内先转发。活动 RT 有明确时间与行为关联，较 Last.fm 的静态好友先行标签代理在可观察性上更强；但仍然**缺少没有转发的真实暴露机会、同一条消息/原始推文 ID、先前关注边有效起始时间**。所以本关至多 `E2_SOURCE_TIMED_INTERACTIONS_PASS_BOUNDED`，**真实 IC/阈值因果参数识别 BLOCKED**。

测试门：至少 12 个合成正反例，涵盖 RT 方向标注、同秒严格小于、身份=0 合法、重复边、非法类型、无效时间、gzip CRC、文件大小、原始 ID 不暴露、无网络边与完整周期限制。PESEN v0.1 FROZEN。

`R069_HIGGS_PRIMARY_SOURCE_GATE=FROZEN`
`R069_INDEPENDENT_CASCADE_CAUSAL_FIT=NOT_AUTHORIZED`
`R069_E3_EXTERNAL_CAUSAL_REPLICATION=OPEN`
