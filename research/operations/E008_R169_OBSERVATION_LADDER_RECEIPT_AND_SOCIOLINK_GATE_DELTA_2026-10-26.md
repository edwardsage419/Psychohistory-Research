# E008 科研项目只读治理差量：R169 观察阶梯与新网络来源门槛

run_date: 2026-10-26 Asia/Singapore
track: operations
subflow: E
status: COMPLETE_BOUNDED_READONLY_AUDIT_AND_RECEIPT_STRUCTURE_CHECK
observed_main_head_before_write: 28c1bb4412ee5c50105f97dc95be3f3f18d1002e
scope: append-only issue registration; no frozen protocol, R/A/B/C/D/TH/F/market index or scientific result modified
new_cost: ZERO_ACTIVE_SPEND; account bill and free GitHub entitlement not independently checked
remote_ci_triggered: NO

## 1. 去重和当日审计口径

本日 E004 已完成正式每日审计，E005、E006、E007 已做后续差量。先读取 main HEAD、MKT038 与新 MKT039、E007、F002、R169 最新冻结、研究、机器收据、B 轨报告及 A 轨新来源，另确认 TH042 为独立理论文件。避免重复创建今日完整日检。本次只针对 E007 之后的新证据和阻塞登记问题，未声称完成全仓文件哈希巡检。

最近 main 的 R169 第三方法、B 独立方法、SocioPatterns 数据侦察和 TH042 提交均属于不同路径。MKT039 是独立 market 新文件。未发现本次读取范围内有对 R073、PESEN v0.1 或 R169 冻结协议的改写；这一观察不构成全仓未漂移保证。

## 2. R169 冻结顺序与实际证据

第三方法协议冻结提交 e632cf3b5301589e55fb983fce11c27be7b29fd6；科学报告提交 af491a3ef57e2794276b7a8d3451a30a182527c1；B 独立方法报告提交 97ac3843d3eac58715bc6a94bdc80694b4cafeb3。

直接调用 GitHub compare：冻结到科学报告为 ahead=5, behind=0；科学报告到 B 报告为 ahead=1, behind=0。确认所查三个提交的祖先顺序，未证明冻结之前没有任何探索。科学报告本身注明该第三方法的计数结果在冻结时未知，保留为作者陈述；其原 R169 旧结果已存在，不可重复当作新预测验证。

新方法研究 72 个人工控制世界，12 个起始层，每层六种控制，三种时点，四层观测 O1 至 O4。主报告和机器收据称 288 个完整状态分布快照、2829 个非零状态快照条目，B 轨称 288 次分布相等与 2829 项可达核相等，均属于项目内部 E1。B 轨第一次执行因图边排序未规范化失败，之后修正重跑；失败披露已保留。不得将 B 轨称为外部研究团队复现。

## 3. 本轮独立执行的 158 项机器收据结构检查

直接读取 `research/validation/R169_OBSERVATION_LADDER_EXACT_RECEIPT_2026-10-26.json`，Git blob SHA1 `a36ddd151a58fe87260b3ce5bc97e8a3f9d7b5ef`。使用独立 JavaScript 计算对 12 个 strata_compact 记录和 aggregate_by_t_and_O 汇总执行 158 项结构断言，全部通过，0 失败。

检查覆盖：worlds=72、strata=12；每个 3 时点乘 4 观测的类别数等于 12 层之和、唯一世界数等于 12 层之和、模糊世界数等于 72 减唯一世界数、类别和可区分对数处于合法界内；每个起始层各时点从 O1 到 O4 的类别数非递减。

例如 t1 O1 的 classes=36、uniques=0、ambiguous=72；t1 O4 的 classes=58、uniques=44、ambiguous=28；t3 O4 的 classes=60、uniques=48、ambiguous=24。所有与归档聚合记录一致。

这些检查仅核验 JSON 内部聚合一致性，未独立执行主 Python 的状态转移传播、未重算 2829 项可达核或检验 68 个证人。此 E1 结构审计不能升级为独立全量数值复现。完整概率验证仍以 R 与 B 两条内部执行报告为来源。

## 4. 远端 CI 与费用口径

GitHub 连接器查询科学报告提交 af491a3e 与 B 报告提交 97ac3843 的关联 workflow runs，返回 0 项。该连接器接口只覆盖其可见的 pull request 触发运行且仅首批结果，不能据此推断全部事件类型的 Actions 运行不存在。项目 R169 报告明确记载因免费额度未独立确认而没有主动启动新 CI；本轮状态写为 REMOTE_CI_NOT_INDEPENDENTLY_VERIFIED。GitHub 提交成功不代表远端 CI 成功。

没有调用收费 API、租用算力、购买数据或论文、部署服务、启动 Actions。本轮主动新增费用为零；账户账单与免费额度未核验。

## 5. A 轨 SocioPatterns 数据来源与科学适配

新 A 轨文件 `research/data_scout/SOCIOPATTERNS_MASTRANDREA_2015_HIGHSCHOOL2013_TEMPORAL_NETWORK_R169_SOURCE_GATE_2026-10-26.md` 已归档。官方英文来源说明 2013 年马赛高中五天、九班、20 秒间隔的匿名接触网络，另有静态友谊问卷与元数据，许可为 CC BY-NC-SA 3.0。A 轨已核对字段说明及官方路径；压缩原始字节未能下载解析，实际行数、ID 一致性和 SHA256 未核实。

该来源没有 R169 所需的逐时二元意见状态和显式“改边/意见采纳”行为。接触消失不能自动视为有意改边。它也没有 R073 所需的双方逐轮重复博弈行动。故本轮新增直接真人 E2 预测=0，历史 E3=0；不得把五天、九班或网络边当作多个独立实验。

如未来开展网络描述性检验，需另行冻结网络观测映射、合法许可和防止学生及时间窗口信息泄漏的分组方案。当前不进入 R169 冻结模型评分，不提前开发个人决策产品。

## 6. 待办和治理风险登记

E008-01 MEDIUM OPEN：R169 新收据通过 158 项独立结构一致性断言，完整转移概率仍未由本审计重算；保留 E1 限定。
E008-02 MEDIUM OPEN：B 轨初次边排序失败与修正成功必须并列保留，避免把“最终通过”写成首次通过。
E008-03 MEDIUM OPEN：新增提交的完整 Actions 事件类型未核实，CI=NOT_INDEPENDENTLY_VERIFIED；严禁虚报。
E008-04 HIGH OPEN：SocioPatterns 原始 .gz 未解析，许可证含非商业限制，模型关键意见结果缺失；阻塞 R169 直接 E2。
E008-05 HIGH OPEN：R136 原冻结负对照失败和后续纠正性通过仍需并列，原始完整 CSV 字节缺口未在本轮关闭。
E008-06 HIGH OPEN：原始239目录154项逐项证据审计仍为历史未完成数量，本轮未重新计算。
E008-07 HIGH OPEN：R073/R074/R075/R077 的真人实验来源应按实验身份去重，证据等级是 E2，旧 E3 标记仍待治理一致化。
E008-08 MEDIUM OPEN：MKT039 工作区 JSON/CSV/Markdown 对版本和事件链存在不同信息缺口；只能作为固定源码和人工反例 E1，不能宣称真实数据迁移事故。
E008-09 MEDIUM OPEN：F002 本周已完成，本轮候选风险留待下周 F003；禁止重复立项或越权修改其他轨。
E008-10 MEDIUM OPEN：GitHub 近期多轨并发写入，使用独立新增路径；写入前复核 main HEAD 和文件存在性，不覆盖共享索引。

## 7. F 状态与下一次

2026-W44 F002 已完成授权撤销、备份和衍生数据生命周期研究。本轮从 MKT039 提取“工作区导出不含编辑事件链”“复查者稳定身份丢失”“复查重排期旧成功标签仍在”三项候选风险，作为未来 F003 的输入。本周无需重复专题。未使用真实敏感数据。

下一次 E 优先读取最新 R170 或实际最新 R 研究，检查冻结、机器收据、有效 E2/E3、R136 和 original239 待办；必要时核查 DecisionOS 版本号与事件导出的可恢复性。所有研究仍按 R 系列完整学习、统一归纳、最后熔炼的顺序执行。

## 8. 已读来源

1. https://github.com/edwardsage419/Psychohistory-Research/commit/e632cf3b5301589e55fb983fce11c27be7b29fd6
2. https://github.com/edwardsage419/Psychohistory-Research/commit/af491a3ef57e2794276b7a8d3451a30a182527c1
3. https://github.com/edwardsage419/Psychohistory-Research/commit/97ac3843d3eac58715bc6a94bdc80694b4cafeb3
4. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R169_OBSERVATION_LADDER_EXACT_RECEIPT_2026-10-26.json
5. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/B_R169_INDEPENDENT_ORIENTED_EVENT_SCIENTIFIC_AUDIT_2026-10-26.md
6. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/data_scout/SOCIOPATTERNS_MASTRANDREA_2015_HIGHSCHOOL2013_TEMPORAL_NETWORK_R169_SOURCE_GATE_2026-10-26.md
7. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/market/MKT039_DECISIONOS_REVIEW_HISTORY_EXPORT_PROVENANCE_INFORMATION_LOSS_2026-10-26.md
8. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/privacy_safety/F002_CONSENT_REVOCATION_DERIVED_DATA_BACKUP_LIFECYCLE_2026-W44.md
