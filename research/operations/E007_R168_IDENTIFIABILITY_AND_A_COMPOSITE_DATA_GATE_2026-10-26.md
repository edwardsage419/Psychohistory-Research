# E007 当日只读治理差量：R168 完整核等价与 A 轨复合真人数据身份门槛

run_date: 2026-10-26 Asia/Singapore
track: operations
subflow: E
status: COMPLETE_READONLY_DELTA
observed_main_head_before_write: cf471565b7a4a465cf3eb4a6750ab9ca4e952e5c
scope: append-only issue register; no R/A/B/C/D/TH/F/market index or frozen protocol modified
cost: GitHub public read and one text report; no paid API, CI or hosted computation; active new spend zero; account bill and free quota not independently verified

## 1. 当日去重与研究轨状态

已先读取 main HEAD、market MKT001 至 MKT038、operations E004/E005/E006、privacy_safety F002 及最近提交。E004 是 2026-10-26 正式每日审计，E005/E006 是差量；本次仅核查 E006 后出现的 R168 及 A 轨来源门槛，避免重复生成完整日检。最近提交显示 R168 protocol、research、B 独立方法、A 数据侦察以及 TH041 理论轨并行更新；仅核实所列具体文件，不宣称全面扫描所有轨所有历史文件。项目研究顺序仍为全部 R 系列、之后归纳分类、最后熔炼。

## 2. R168 冻结与执行次序

直接读取 GitHub commit：
* 冻结协议 8cc8f44bf64bc630874f12c540c64e1a2ced0c4d，提交时间 2026-10-25 18:47:40 UTC，文件 protocols/R168_EFFECTIVE_OPPORTUNITY_KERNEL_IDENTIFIABILITY_AUDIT_FREEZE_2026-10-26.md。
* 主研究报告 83f7dba13ee4147a9b6044e7c5c0b9365540f00f，提交时间 18:50:51 UTC，文件 research/validation/R168_EFFECTIVE_KERNEL_IDENTIFIABILITY_THIRD_METHOD_SCIENTIFIC_REPORT_2026-10-26.md。
* B 方法报告 4561a95ce7cb75245b94b7a9cb99cc8a0603af34，提交时间 18:51:06 UTC，文件 research/evidence_audit/B_R168_PARAMETER_BLIND_KERNEL_IDENTIFIABILITY_SCIENTIFIC_AUDIT_2026-10-26.md。

主报告声明冻结前已探索性观察 16 个核等价类与 23/32 非单例参数行，故这些数字不能写成前瞻性预注册发现。直接读取 research/R168/R168_EXACT_RESULTS.json，记录 32 个合成核、64 个合成世界；读取 B_R168_OBSERVABLE_KERNEL_RECONSTRUCTION_RECEIPT_2026-10-26.json，确认记录 288 个核单元复核、16 个可观察类、64 个实际执行的代数突变、0 个漏检。报告另称主方法完成 960/960 五时点概率单元比较，本轮没有独立执行原 JS 程序，也未逐行复算全部 960 项；该数字属于归档报告证据。主方法与 B 方法来自同一项目的两条不同内部数学路径，证据仍为 E1，不能称外部独立科研团队复现。

主结果的数学形式：A=(1-u)^m，B=(1-f)^m，完整 3x3 群体状态转移核只依赖 A、B。未知 m 时 (m,u,f) 不可唯一识别。该命题限定于研究项目自造三状态群体模型；原作者真人实验、E2 行为数据、E3 历史社会数据均未因此获得新证据。原冻结 E1 结题范围未扩大，R073 与 PESEN v0.1 未修改。

直接查询 GitHub Actions runs API 的 head_sha=83f7dba13ee4147a9b6044e7c5c0b9365540f00f 与 4561a95ce7cb75245b94b7a9cb99cc8a0603af34，均返回 total_count=0。仅说明这两个提交未见关联运行，不能推断所有历史 CI 均不存在，也不能把 GitHub 提交成功称作 CI 成功。

## 3. A 轨新复合数据门槛

直接读取 research/data_scout/NAY_VOROBEYCHIK_2016_DATAFSM_NV_GAMES_168386_COMPOSITE_IDENTITY_GATE_2026-10-26.md，来源为 Nay 与 Vorobeychik 2016 PLOS ONE、JohnNay/datafsm。其公开手册声称 NV_games 为 168386 行、51 列、30 种游戏变体，涉及八项底层真人研究。A 轨验证了上游文本手册和二进制 Git blob 的存在与身份，但未解码原始 RDA，因此 168386 是作者文档行数，尚未独立统计。公开字段说明未列出独立 session ID、对手身份或配对 ID；group 为游戏版本，不能擅自用作 session。底层 DF/FR 研究与 R074/R075 可能重叠，需按原始研究身份去重。该复合数据不能直接作为 R073 的第五个独立实验，也不能直接运行冻结留出场次评分。A 轨此轮是来源侦察与拒绝越级使用，新增可认证 E2=0、E3=0。

## 4. 跨轨治理与待办

E007-01 MEDIUM OPEN：R168 16 类/23 行属于冻结前已知的探索性结果，后续任何汇总都必须保留时间说明。
E007-02 MEDIUM OPEN：R168 288 核单元和 64 负对照有机器收据，但本轮未执行源码；同项目 B 轨不能升级为外部独立复现。
E007-03 MEDIUM OPEN：上述两项 R168 新报告提交无关联 Actions 运行；保持 CI=UNVERIFIED_FOR_SPECIFIED_COMMITS。
E007-04 HIGH OPEN：NV_games 168386 行为手册声称，二进制未解析；session/participant/opponent 身份缺口阻塞 R073 冻结留出评分。
E007-05 HIGH OPEN：NV_games 八项底层研究必须与 R073/R074/R075/R077 原实验逐一去重，禁止按复合文件计为新增独立实验。
E007-06 HIGH OPEN：R136 原冻结负对照失败及后续纠正性通过须并列保留；完整原始 CSV 的核验缺口未在本轮关闭。
E007-07 MEDIUM OPEN：original239 的154项待审为此前记录，本轮未重新计算；不能因 R168 归档自动减项。
E007-08 HIGH OPEN：旧 E3 标签与当前 E3 历史社会证据的口径冲突继续开放；R074/R075/R077 为 E2 真人实验。
E007-09 MEDIUM OPEN：MKT038 的完整度评分与一键结果标签仅做源码和合成检查，禁止升级为真实产品事故或真人决策改善。
E007-10 MEDIUM OPEN：仓库并发活跃，写入前已重新核查 main HEAD 和目标路径；本文件独立路径增量写入，不修改其他轨索引。

## 5. F 状态、费用和下一步

2026-W44 的 F002 已完成授权撤销、衍生数据和备份生命周期专题。本轮新增候选风险为 DecisionOS 邮件“一键仍有效”被映射为 successful 结果，以及 GET 复查写入副作用；仅作为未来 F003 或后续主题的风险输入，避免本周重复专题。未接入真实敏感数据，未提前开发个人决策产品。

下次 E 优先核查 R169 或当时最新 R 系列冻结及机器收据、A 轨复合来源去重、R136 原始收据可用性、旧 E3 映射，以及共享路径并发覆盖风险。无新收费资源、无购买、无 CI 触发。仍需在未来有安全免费渠道时独立核验账户免费额度。

## 6. 仓库来源

1. https://github.com/edwardsage419/Psychohistory-Research/commit/8cc8f44bf64bc630874f12c540c64e1a2ced0c4d
2. https://github.com/edwardsage419/Psychohistory-Research/commit/83f7dba13ee4147a9b6044e7c5c0b9365540f00f
3. https://github.com/edwardsage419/Psychohistory-Research/commit/4561a95ce7cb75245b94b7a9cb99cc8a0603af34
4. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/R168/R168_EXACT_RESULTS.json
5. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/B_R168_OBSERVABLE_KERNEL_RECONSTRUCTION_RECEIPT_2026-10-26.json
6. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/data_scout/NAY_VOROBEYCHIK_2016_DATAFSM_NV_GAMES_168386_COMPOSITE_IDENTITY_GATE_2026-10-26.md
7. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/operations/E006_R073_R077_STUDY_LINEAGE_EVIDENCE_TAXONOMY_AND_R167_E1_2026-10-26.md
8. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/market/MKT038_DECISIONOS_RECORD_QUALITY_VS_OUTCOME_AND_MAGIC_LINK_REVIEW_2026-10-26.md
