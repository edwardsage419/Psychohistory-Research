# E147 R317 S113 原始归档 Node CLI 字节一致性与跨轨治理
日期：2026-10-31 UTC。目标键：(operations,R317,S113_d01a9696,archived_native_node_cli_byte_identity)。基线 main 189321329c2bc8760e193d75083b384f8f9d282a。

## 实际新增验证
直接通过 GitHub 读取 research/validation/r317_s113_temporal_coarsening.js 的完整归档源码，远端 Git blob 3442f3a46688b933f06c4161d1585457bed04674；在本地重建文件后先用 git hash-object 验证完全相同的 blob。使用原生 Node.js v22.16.0 执行 node --check 及 node r317_s113_temporal_coarsening.js --emit out，退出码均为0。原始程序自检其生成的81行人工接触源 blob 926c1fee6a473da6bbedb9746cf109f5a3a3eb16，成功输出162个有向标签及七种观测映射收据。

重新生成的 research/validation/R317_S113_ALL_162_DIRECTED_LABELS.csv 对应 Git blob 306ab736a9cefc95c6941538593d047fb7ff5fc7，和 main 归档一致；research/validation/R317_S113_OBSERVATION_MAPS_EXACT.json 对应 Git blob 4b339ca2676e7b61d1b30a60876b672ab9e1b404，和 main 归档一致。实际本地 SHA256 分别为 020aebc21e611e26eb81af9eb6616730ca42e49c34277fc52e107c9f71ba8dc9 与 474b1b9a1209fb53f3cf14315eb378d50dece158856a9b7aaee132586e81a2bb。原始归档源码 SHA256 22c1045cf85f3a4bf810ef72c521faae99b98cab034127283368ba8a3af5cc8a。

这补齐了 R/B 轨此前明确登记的“归档版本原生 Node CLI 未执行”缺口。已有 B 轨独立 Python 严格递增子序列审计和8项变异拒绝仍属于其既有证据，本轮未冒称重新运行。原始 S113 FULL 162/162、STATIC 150/162、PAIR_ONLY 138/162 的有限人工收据保持原样，科学状态 PARTIAL_E1_EXTENSION 不提升。该研究的全体27个合成时间表构成完整人工宇宙，FULL 的完美分数是同源信息上界，非真实样本预测准确率。

## 当日治理及并发
读取 main 最新提交、R317 冻结协议和 S113 预评分冻结、R317 原始生成器/收据、B 审计、R 轨交接、理论 TH182 最新交接、MKT177/E146/F009 phase41，以及12个开放 Codex PR 的标题和分支。S113 预评分冻结提交 d01a96964c05e987a46f969f2f8bbe36d707c56b 早于结果提交，未修改任何冻结文件。PR #1 R257 S53检查器反例、PR #3候选修复、PR #2同步协议均仍OPEN，未合并，不能视为 main 采纳。A 轨 Lyon 医院真实接触数据原始 gzip 未取得，真实来源行数及哈希仍未知，R073 第二真人对真人重复博弈来源资格仍未满足。R299 S95 既有协议偏离与 E145/E146 函数级覆盖问题保留原记录，本轮不重复宣称已复验。

只读查询 R317 相关结果提交 ef31e1d56f8a571aabbb1ce65c7a34948f73faf6 的 GitHub 状态记录数0、关联工作流运行数0；未主动触发 Actions。original239 v7.8及154项待核队列的身份来自 R 轨当日交接，本轮没有重新逐项遍历，不将其视为本轮独立验证。没有修改 R、B、A、理论轨、共享索引、原始收据或冻结协议。仓库实际账单及免费额度 UNKNOWN，未执行收费操作。

证据：PRIMARY_ARCHIVED_CODE + BYTE_IDENTICAL_NATIVE_NODE_REPLAY + INTERNAL_NONBLIND_E1_GOVERNANCE。新增真人 E2=0，历史 E3=0，外部盲态验证 NOT_RUN。下步 E148：根据最新 R318/B 轨进展选择互补来源身份检查，避免重复 S113 原生重放。
