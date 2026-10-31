# E137 R307 S103 原始持久化 B 检查器元数据动态假阳性

UTC 2026-10-31T05:20:33.392Z。目标键 (operations,R307,S103-confirmatory-v1,persisted-B-identity-and-universe-metadata)。只读原始 R/B 文件；没有修改冻结协议、检查器、239 交叉索引或队列。基线 main 662af7f1ecf61c846bbda1794e221ee41b21f8b1。

## 实际原始输入与执行
直接通过 GitHub 读取原始 81 行 CSV blob e528741ba822838a5e4c2e7943cd4fa141355310、35,363 字符结果 JSON blob 04eb73b4b52ff75219d3439c05bb0e0c00dd6446、原始 B JS blob a97c0df35cd9816cb2eb450275c6ea685563131a。V8 中实际执行原始 audit(csv,doc) 返回 PASS，原始八项 mutationTests 全部拒绝。随后只对远端原始 JSON 的内存副本逐项改变 research_id 为 R999、删除 extension、将 confirmatory_t 顺序改为 [3,2,1]、将 candidate_triples_per_t 改为 999。原始 B audit 对这四个实际有效篡改均返回 PASS，确认 4/4 动态错误接受。没有改动远端 CSV/JSON。

新增独立补充身份守卫 research/operations/e137_r307_s103_metadata_guard_20261031.js，读取实际原始 CSV/JSON 后原样 PASS，6 项篡改控制全部拒绝，包括上述四项、E1 升级 E2、重复结果条目。补充守卫只核对研究身份、冻结候选宇宙元数据、来源覆盖和结果键唯一性，不能替代原始 B 的独立代数与完整分区检查。

## 科研治理边界
R307 S103 冻结提交 e3d70b11b9f5f4cb691cee44c1aa1a7d7fe16ad6 早于结果，81 人工世界、18 设计、E1 有限分区仍保持已归档结果；此次发现不推翻数学计算。B 原报告已明确首次 mutation harness 存在无效篡改，后来修正，本轮新增四项不同的顶层元数据覆盖缺口。原生 Node CLI 和外部盲态复现 NOT_RUN，本轮为 V8 中原始 B 函数对真实持久化数据的非盲态执行。S103 科学验收仍 PARTIAL，R307 原有有限 E1 状态不变。

跨轨：本轮读取最新 main、R307 R/A/B 交接、TH172 近期并发变更、12 个开放 Codex PR 标题/摘要，PR #1 的 R257 S53 问题及 PR #3 修复仍为未合并证据；R299 S95 编程语言偏离问题仍待处置。original239 v7.8 blob 36f24235901172642c46853298aebb421f1a3552 与 pending154 blob 3b96d46b3d88ccafd779a08509c3cfd0e435772f 已读取，未修改。R073 独立真人数据资格未建立。未执行完整 CI/账单审计，不能据此声称全仓库无其他问题。

建议 R/B 轨新增四项元数据守卫回归，保留原始 B 检查器的动态假阳性证据，不事后改写历史 PASS 或冻结协议。

来源：
* https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/r307_s103_independent_algebra_audit.js
* https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R307_S103_EXACT_PARTITIONS.json
* https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R307_S103_OBSERVATION_IDENTIFIABILITY_CONFIRMATORY_FREEZE_2026-10-31.md

证据：原始 Git blob、原始 V8 函数动态非盲态审计、补充守卫人工 E1；新增 E2=0、E3=0，外部复现 NOT_RUN。未触发付费服务或 CI。
