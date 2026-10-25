# E006 只读治理差量：R073 至 R077 真人实验来源、证据等级口径及 R167 验收边界

run_date: 2026-10-26 Asia/Singapore
track: operations
subflow: E
status: COMPLETE_READONLY_CORRECTION_AND_BOUNDED_R167_CHECK
observed_main_head_before_write: 8e0bf45f0693724ecbd6fb2c63ffc3859012fcd9
scope: append-only governance audit; no other track file or frozen protocol changed
cost: GitHub 免费只读审计及本项目报告写入，无 CI、付费 API 或云计算；主动新增费用零，账户账单未独立核验

## 1. 当日去重与变更范围

E004 已对 R165 和 C003/D002 做日检，E005 对 R166 事后勘误与 Montero 原实验排除做差量审计。本次检查 E005 之后的 A 轨来源纠正、B 轨证据等级冲突说明、R074/R075/R077 原始机器验收文件，以及 R167 最新冻结、执行、B 轨独立方法记录。E005 的“缺少第二独立真人实验”已被后续归档证据否定，故本报告登记为 **已纠正的过时项目级缺口**，保留 E005 原文以保持审计可追溯性。没有重复创建当日完整日检。

## 2. 高优先级：R073 的第二独立真人实验已经归档

已直接读取以下固定仓库验收 JSON：
* research/R074/R074_FINAL_ACCEPTANCE_STATUS.json，Git blob 6fe05c642a1d64f8fc292315f34574c274091f55，原研究 Dal Bó 与 Fréchette 2011，18 个独立日期场次、15338 个合格 t>=3 目标，留出完整场次；第二项原始真人实验。
* research/R075/R075_FINAL_ACCEPTANCE_STATUS.json，Git blob 1241ad79fd1f19195eb591ce60b56668ead8cd76，原研究 Fudenberg、Rand 与 Dreber 2012，18 场次、26116 个合格 t>=3 意向行为目标；第三项原始真人实验。
* research/R077/R077_FINAL_ACCEPTANCE_STATUS.json，Git blob 24e45b65878ca400cb7f149ad863dd74e7fd5cd9，原研究 Drouvelis 与 Pearce 2025，15 场次、1040 个合格 t>=3 目标；第四项原始真人实验。

原 R073 Montero 2022 是基线。R076 重用 R074/R075 的实验来源，不能计为第五项。2026-10-26 A 轨来源登记确认四项不同原始实验；B 轨独立审计确认旧机器状态使用的 E3 与当前 owner 口径冲突。E005 中“第二独立真人重复博弈数据集仍缺”只适用于未看到后续项目档案的旧信息状态，**现在项目级结论应为第二、第三、第四项原始真人实验均已有有界评估归档**。本轮没有重新下载个人数据、复算全量人类评分或重新核验历史 Actions；现有原始报告中的成功声明仍应追溯其原始 run ID，不把归档本身当作本轮独立执行。

研究强度不能合并：
* R074、R075 在各自新实验的训练场次估计条件概率，再按整场次留出评分；属于不同实验来源的内部评估，不能称为零目标训练。
* R076 是事后源模型数值迁移，实验身份重复且时间上已有先前结果可见。
* R077 使用 R073 来源参数，目标实验标签零拟合；保留 Rev-001 来源门槛失败及 Rev-002 在首次目标模型评分前的修订。属于更强的目标数据隔离，但原论文早已公开，不能称新招募的未来盲测。
* 不同原论文作者与样本来源不代表外部研究团队对本项目计算模型的独立复现。

## 3. E1/E2/E3 证据等级冲突登记

当前项目统一口径：E1=人工或合成数学；E2=真人行为实验；E3=历史社会演化/历史事件数据。R074/R075/R077 的旧 JSON 将“跨实验真人研究”标为 E3，这是历史版本中对不同轴的使用。当前报告只读映射为 E2_HUMAN，保留 legacy_archive_grade 原始字段，不擅自覆盖冻结机器文件。**当前 E3_HISTORICAL=尚未由这些真人实验建立。**

未来报告分别记录 source_class、original_study_id、study_independence、training_source、target_label_fit、holdout_unit、protocol_timing、research_team_independence、legacy_grade。若使用旧 E3 字符串作唯一筛选，会将真人跨实验评分错误统计为历史预测验证。

已读 B 轨原文：research/evidence_audit/B_R073_R077_LEGACY_E3_LABEL_VS_CURRENT_E2_HUMAN_E3_HISTORY_TAXONOMY_2026-10-26.md。已读 A 轨原文：research/data_scout/R073_R074_R075_R076_R077_HUMAN_SOURCE_LINEAGE_AND_E3_GAP_CORRECTION_2026-10-26.md。

## 4. R167 新研究只读验收

协议冻结提交：3ff757de60838bb742fe5347c94f2a3a0a935fea，报告声明先于执行。原 R167 结果 Git blob 86839d8d473e4aee2f450d8c598797299ec1cf41；新主执行收据 Git blob 5fb48d97371b99292ce04424699722dbfe487950，记录 72 个人工世界、792 个精确原归档标量比较、24 个正 delta 的阈值符号测试、36 个边界测试、42 个控制，5 个网格情景发生严格总量反转。B 轨 Python Fraction 独立直接权重方法报告记录相同 72 个世界和边界结果，指纹 39e5a121a6c8a286；B 本地完整 JSON 收据未在本次取得。此处两条实现共享人工模型与研究项目，属内部 E1，外部团队独立复现、真人 E2、历史 E3 均为零。

本轮直接通过 GitHub Actions REST 查询 R167 科学报告提交 d0aac9d6edce90220a37cf6936acc04d19b984fb 和 B 审计提交 a0bb78aa81cbec571172a4d37ac2dd41c4d4945a，head_sha 过滤结果均 total_count=0。因此只报告这两项提交 **未发现关联 Actions 运行**，不能推断全部历史运行均不存在；未触发 CI。

R136 既有冻结负对照失败及后续纠正性通过仍须并列保留。original239 154 项待逐项审计为既有队列数字，本轮没有重新计算全索引或扫描所有冻结协议。新近 R167 通过不构成 R 系列全部研究完成。

## 5. 并发、归档、费用和问题登记

E006-01 HIGH RESOLVED_AS_READTIME_CORRECTION：E005 项目级第二独立实验缺口陈述过时；按 A/B 后续记录更新读时解释，不改 E005 原文，不把 R076 计第五项。
E006-02 HIGH OPEN：旧 E3 跨真人实验等级与当前 E3 历史证据等级冲突；未来统一采用分轴字段，禁止混计。
E006-03 HIGH OPEN：R077 目标零拟合与 R074/R075 新研究内部留场训练强度不同，禁止无差别宣传为前瞻性独立盲测。
E006-04 MEDIUM OPEN：R167 新方法本次指定提交无远端 Actions 运行，内部 E1 报告与 CI 证明分开。
E006-05 HIGH OPEN：R136 原冻结负对照失败、完整原始 CSV 复核仍有未完成项。
E006-06 MEDIUM OPEN：original239 154 项待审为历史记录，未由本轮重数确认。
E006-07 MEDIUM OPEN：MKT037 仅为公开源码和人工 SQLite 合成负对照，不能宣称真实 Decision Journal 备份发生故障。
E006-08 HIGH OPEN：项目历史 E3 社会演化预测和外部独立团队复现尚未建立，保留研究缺口。

本轮只在 operations 路径增量登记治理发现，未更改 A/B/R/TH/market/F 的研究结果、索引、冻结协议或 CI 设置。未核验 GitHub 账户整体账单及免费额度，不启用收费资源。

## 6. F 当周状态及下一次检查

2026-W44 F002 已归档授权撤销、衍生记忆、缓存及备份生命周期专题。本轮无新周专题，继续保留 MKT037 的备份文件身份与恢复前验证作为候选风险。下一次 E 优先核查 R168 或最新实际研究提交、R136 完整数据收据、legacy E3 的读时映射在新报告中是否正确执行，以及是否存在新并发归档冲突。

核心顺序：先完成全部 R 系列，再系统归纳分类，最后熔炼；零新增费用。

## 7. 仓库来源

1. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/R074/R074_FINAL_ACCEPTANCE_STATUS.json
2. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/R075/R075_FINAL_ACCEPTANCE_STATUS.json
3. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/R077/R077_FINAL_ACCEPTANCE_STATUS.json
4. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/data_scout/R073_R074_R075_R076_R077_HUMAN_SOURCE_LINEAGE_AND_E3_GAP_CORRECTION_2026-10-26.md
5. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/B_R073_R077_LEGACY_E3_LABEL_VS_CURRENT_E2_HUMAN_E3_HISTORY_TAXONOMY_2026-10-26.md
6. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R167_KAPPA_REVERSAL_CRITICAL_THRESHOLD_THIRD_METHOD_SCIENTIFIC_REPORT_2026-10-26.md
7. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/B_R167_INDEPENDENT_DIRECT_WEIGHT_THRESHOLD_SCIENTIFIC_AUDIT_2026-10-26.md
8. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/operations/E005_R166_POSTEXEC_AMENDMENT_AND_R073_SOURCE_DEDUP_DELTA_2026-10-26.md
