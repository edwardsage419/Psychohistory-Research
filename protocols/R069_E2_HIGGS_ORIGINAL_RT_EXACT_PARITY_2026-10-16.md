# R069 E2：官方 Higgs RT 事件与聚合边逐边完全一致性验证

日期 2026-10-16。**在首次执行此项 RT 逐边双文件一致性计算之前冻结**。上游为已执行的真实来源门 [GitHub Actions 38876285461](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38876285461)：活动文件 563,069 行、RT 354,930 行、加权 RT 网络 328,132 行，权重总和 354,930。**仅权重总数相等不足以证明每一条边方向与次数一致**；本研究是独立逐边复核，不是再次传播因果分析。

固定官方 gzip 源文件及初次实得字节哈希：

| 文件 | 官方 URL | 原始 gzip 字节 | SHA256 |
|---|---|---:|---|
| `higgs-activity_time.txt.gz` | `https://snap.stanford.edu/data/higgs-activity_time.txt.gz` | 4,169,461 | `901b199716a23b0fc0371705e3ae9941b5c9493277aec65456abc4988674ad79` |
| `higgs-retweet_network.edgelist.gz` | `https://snap.stanford.edu/data/higgs-retweet_network.edgelist.gz` | 1,957,437 | `4097edebd539043cfc62d9b4ba67676f79523f6dbe896d345fcc127dec3e936e` |

## 数据校验、等价假说和失败先行

1. 从上述两个 SNAP 官方 URL 再下载、再 SHA256 校验，不允许直接从之前匿名汇总推断逐边一致；任何 SHA、gzip CRC/行格式漂移 fail-closed。
2. 从 `higgs-activity_time.txt.gz` 全部 RT 活动行按**原表动作方向** `(A,B)` 计算 `Counter[(A,B)] += 1`；MT 和 RE 不应混入。并记录 A=B 的 RT 条数，不假设不存在。
3. 从 `higgs-retweet_network.edgelist.gz` 获取有向 `(A,B)` 和整数权重；逐对全连接比较，输出：活动有而聚合缺失的唯一边数、聚合有而活动缺失边数、共有边中权重不同边数、绝对权重差总和；任何非零须**科学状态 FAIL**，另保存匿名计数，不反向调整方向达到零。
4. 正常研究假设：如果完全吻合，则两个文件不是两项独立观测数据——聚合图**由同一活动生成**；绝不能把该加权图充作先于事件的好友网络或两份独立证据来估计 IC 或 Watts 因果参数。即便精确逐边相等，这只证实源加工与行层数据一致。
5. 还需报告若将 RT 方向反转 `(B,A)` 后的**边集合不一致计数**，用于明确数据方向约束；反向比较不是正当修复方案。
6. 逐边真实对象和节点 ID 仅在 GitHub Actions 临时 runner 内存；保存纯匿名条数和全部文件哈希，不发布原 RT 边/人的时间线。
7. 合成测试包括对齐、单条权重变更、方向误置、重复事件聚合、MT 混入、SHA 错误、源文件缺失，以及不能将同一数据称为两独立样本。

`R069_HIGGS_RT_EXACT_PARITY_PROTOCOL=FROZEN`
`R069_TRUE_PRIOR_TIE_NETWORK=NOT_OBSERVED_IN_THE_RT_AGGREGATE`
`R069_CAUSAL_IC_AND_THRESHOLD_FITS=BLOCKED_BY_MEASUREMENT`
`PESEN_v0.1=FROZEN`
