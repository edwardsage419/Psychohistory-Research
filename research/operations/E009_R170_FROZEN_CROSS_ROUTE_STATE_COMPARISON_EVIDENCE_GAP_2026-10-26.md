# E009 R170 预冻结跨路线全状态核对与归档证据缺口

run_date: 2026-10-26 Asia/Singapore
track: operations
subflow: E incremental readonly governance
status: COMPLETE_BOUNDED_READONLY_WITH_OPEN_ACCEPTANCE_EVIDENCE_GAP
observed_main_head_before_write: 14d6dd8f01af5a9b00ade24313bcf6d2dc36c6db
prior: E004 formal daily check; E005 through E008 incremental; MKT040; F002
new_spend: ZERO_ACTIVE; account billing and free quota NOT_INDEPENDENTLY_VERIFIED
ci: NOT_TRIGGERED_BY_THIS_AUDIT

## 1. 范围和并发去重

读取 main HEAD、当日 E004 至 E008、MKT039 至 MKT040、F002、R170 事前冻结、科学报告、机器收据、JavaScript 主程序、B 轨 Python 独立程序与审计摘要、A 轨真人命名实验来源登记。另核对 R170 冻结与报告的 GitHub 祖先顺序、两个研究提交的 Actions REST 记录及 TH043 并发更新。仅新增本 E 文件；未修改 R/A/B/C/D/TH/F、冻结协议或共享目录索引。全仓冻结对象没有逐一哈希巡检，不能据此宣称全局无漂移。

## 2. 冻结与提交真实顺序

R170 第三方法冻结提交：6bba9f855b470ecbc7fe1a8a373468083a874c0c，仅新增 protocols/R170_OBSERVATION_LADDER_THIRD_METHOD_FREEZE_2026-10-26.md。
科学结果提交：c6e9296ac369db35ed5fd28cde15c9d9ef1120f2，仅新增主 JS、报告及 JSON 收据。
B 轨及 A 轨提交：e31d562c303aa5c9c0551ae4d6758d0c44b70c03，新增独立 Python 源码、B 审计、B 精简 JSON 和真人来源门槛说明。
直接 GitHub compare 冻结到科学提交 ahead=1、behind=0。先后顺序已核实，不能从提交顺序推出全部测试在冻结前从未探索。

本轮检查期间理论轨 TH043 独立新增 theory 文件及索引，未与 E/market 路径冲突。MKT040 在独立 market 路径新增并已收到提交 SHA；没有对共享索引写入。

## 3. 实质新发现：跨路线全状态等式的独立验收仍有证据缺口

冻结协议规定，主路线和独立 B 路线对 72 个世界、四个时点比较精确的完整状态分布，并要求 B 不导入或调用主路线。冻结的 PASS 条款要求完整跨路线等式、规范化、负对照与失败披露。

主 JS 代码 mainKernel/secondaryKernel 在同一文件中分别枚举事件，两者共享 update 状态更新函数；其程序和科学报告记录 288 项完整状态分布等式通过。这是同一运行环境中两种事件枚举的精确核对，共享 helper 的共同错误风险仍在。

独立 Python Fraction B 程序自行构造 288 个归一化分布快照，报告了12组聚合结果、首个证人和扰动负对照与主 JS 一致。B 审计**明确承认**尚未逐个将 Python 的 288 个完整状态分布与 JS 的所有状态概率质量逐项比较。独立 B 的完整本地 JSON 收据 23004 字节只记录 SHA256 8cdf817c0e32cd48ea1a70dd1f9d0c5fc55022c8d355981157d0181934ab2565，未上传远端；远端仅有精简摘要和源代码。

因此，主 JS 内部全状态比较有执行记录，Python B 跨语言聚合与指定证人有执行记录；**预冻结要求的独立 B 与主 JS 全量状态质量逐项相等，当前没有可审计的比较结果**。这属于验收证据范围缺口，未发现实际概率不一致，不据此宣布模型计算失败。既有 PASS_BOUNDED_INTERNAL_E1 应带限定说明；正式关闭该缺口前不升级独立复核范围，更不能称外部团队复现。

## 4. 本轮独立执行 130 项 JSON 结构与跨摘要检查

直接读取主收据 blob SHA1 0d5b10125475a66a243be1632e21bd269027a866 和 B 精简摘要 blob SHA1 165f14511c7c7ee57b43a18851d2e65729c50044。
使用独立 JavaScript 计算检查：72 worlds、12个 graph×initial strata、36个 stratum×time 行、288项主报告完整分布等式数量；12个 time×O1..O4 组合的四项聚合值与 B 精简摘要一致；36个 stratum×time 分组求和与主 aggregate 一致；unique+ambiguous=72；观测精细化时类别数及可区分对数非递减。
合计 130 项断言，130 PASS、0 FAIL。初步检查曾将 36 个 stratum×time 行误认为 12 个独立 strata，发现后依据冻结设计纠正断言并重算；保留此说明，避免虚报首次零错。

此检查证明两个归档 JSON 的计数和结构一致性，不能代替 288 个完整状态概率向量的跨语言逐项比较。冻结的 180 个可区分对是在每个固定 stratum 内合计，不能当作 180 个真人独立样本。

## 5. 远端 CI、真实证据与 A 轨适配

直接读取 Actions REST /actions/runs?head_sha=...，R170 科学提交 c6e9296a 和 B/A 提交 e31d562c 各返回 total_count=0。仅对指定 SHA 的已返回运行负责，不推断仓库全部 CI 历史。两个提交消息均含 [skip ci]，本轮没有启动工作流。GitHub 文件存在及 commit 成功不代表 CI 通过。

A 轨 Centola 与 Baronchelli 2015 三种网络条件的官方公开文本已经检查，但缺可核实的个人 ID、轮次/场次、完整代码本、原始字节哈希和明确数据重用许可。原实验为48人网络条件，与 R170 四人双词冻结模型不直接同构。R170 本轮新增 E1 内部有限数学=1，新增合格真人 E2=0、历史 E3=0、外部团队复现=0。不得将三份文本当作三项独立 E2 实验。

## 6. 只读问题登记

E009-01 HIGH OPEN：独立 Python B 与主 JS 288 个完整状态分布未完成逐项概率质量比对；需 R/B 原轨在固定输入下输出可复算比较收据，保持原报告不被改写。
E009-02 MEDIUM OPEN：B 完整本地执行收据只见 SHA256，原始 23004 字节未远端归档；不把摘要当完整归档。
E009-03 MEDIUM OPEN：R170 关联指定 SHA 的 CI 无运行，远端新算法验收未建立。
E009-04 HIGH OPEN：A 轨真人命名数据的代码本、身份、许可与冻结观测映射未闭合，禁止 E2 预测升级。
E009-05 HIGH OPEN：R136 旧冻结负对照失败及纠正性新协议成功须并列保留，原完整 CSV 缺口未由本轮关闭。
E009-06 HIGH OPEN：original239 v7.8 的154项逐项证据审计待办是既有数值，本轮未独立重算；schema/date 元数据滞后仍开放。
E009-07 MEDIUM OPEN：MKT040 Exist combo 的“至少一个 read scope”仅文档证据与合成逻辑，未做认证服务端实测；未来 F003 可研究派生统计权限。
E009-08 MEDIUM OPEN：当前仅抽查 R170 及近期独立轨，未完成全仓同名文件/冻结对象/重复研究全面扫描。

## 7. F 本周状态、费用和下一项

2026-W44 F002 已完成，专门处理撤销授权、派生数据、缓存与备份；本轮不重复创建 F003。MKT040 的跨 scope 派生相关性披露作为下周候选案例，保留 UNKNOWN，不访问真实敏感数据。没有开发个人决策系统。

主动新增费用零；仅现有 ChatGPT 与公开免费 GitHub/英文官方文档，无产品购买、付费论文、计费 API、GPU/云租赁、新订阅或 CI 启动；账户总账单及 GitHub 免费额度未独立核验。

下一项 E：如 R/B 原轨提供完整跨语言状态收据，先只读核验 SHA、全量质量等式、首次失败记录及协议符合性；同时追踪最新 R171 和 R136 原始数据缺口。保持先完成 R 系列、再归纳分类、最后熔炼。

## 8. 已读来源

1. https://github.com/edwardsage419/Psychohistory-Research/blob/main/protocols/R170_OBSERVATION_LADDER_THIRD_METHOD_FREEZE_2026-10-26.md
2. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R170_OBSERVATION_LADDER_THIRD_METHOD_SCIENTIFIC_REPORT_2026-10-26.md
3. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R170_OBSERVATION_LADDER_EXACT_RECEIPT_2026-10-26.json
4. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/B_R170_EDGE_UTTERANCE_INDEPENDENT_SCIENTIFIC_AUDIT_2026-10-26.md
5. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/B_R170_INDEPENDENT_PYTHON_EXECUTION_SUMMARY_2026-10-26.json
6. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/data_scout/CENTOLA_BARONCHELLI_2015_HUMAN_NAMING_THREE_NETWORK_SOURCE_GATE_2026-10-26.md
7. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/market/MKT040_EXIST_CORRELATION_COMBO_SINGLE_SCOPE_DERIVED_DISCLOSURE_2026-10-26.md
8. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/privacy_safety/F002_CONSENT_REVOCATION_DERIVED_DATA_BACKUP_LIFECYCLE_2026-W44.md
