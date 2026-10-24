# MKT009 Logseq 与 Trilium 导出回导、身份保真和备份安全有界比较

run_date: 2026-10-24（Asia/Shanghai）
track: commercial_market
subflow: product
status: COMPLETE_BOUNDED_DOCUMENT_AND_UPSTREAM_ISSUE_REVIEW
observed_head_before_write: 2acfa1e7c1d205aee4a9c596b060e6b0d04d19d3
preflight: 读取 main 最新 HEAD、MKT007/MKT008、E001、F001、统一工作流规范、R127 临时报告及当日后续提交；目标路径写入前不存在。仅使用英文官方文档、公开 GitHub PR 与 issue；没有安装、登录、数据下载、调用收费服务或触发 CI。

## 1. 本轮真实新增技术事实

### 1.1 Logseq DB：导出格式有不同的保真边界
官方 DB 指南明确区分 SQLite DB、SQLite 加 assets ZIP、EDN、标准 Markdown。EDN 是可编辑且意图完整捕获图数据的格式，官方仍明确不建议将其作为唯一备份。标准 Markdown 不保证保留时间戳和全部属性。页面级 Build EDN 导入既有页面时采用追加块内容的语义，不能假定重复导入具备幂等性。参见 S1。

上游 2026-06-22 的开放 issue #959 提供了重复导入同一页面 EDN 后内容重复的具体复现步骤；它是单名报告者在指定 nightly 版本的观察，未由本轮重跑，不推断所有版本均有此问题。参见 S2。

另一开放 issue #957 报告同日 nightly 版 EDN 导出再导入时出现 journal-day 索引警告；报告中的图仍通过验证，页面数和块数相同，但 datoms 从 2409 变为 2783。差值不能直接解释为用户内容丢失或损坏，提示“导入成功”与“字节级或语义级往返等价”需要分开验收。报告称 SQLite 导入无同样警告，本轮未独立复验。参见 S3。

### 1.2 Logseq：2026 年 10 月的真实修复
直接读取上游 PR #13629。2026-10-06 创建，2026-10-07 合并。修复 file graph 转 DB 时，属性与标签同名且导入顺序不同时可能错误复用 UUID、将属性实体与类别实体合并的问题。PR 修改 `deps/graph-parser/src/logseq/graph_parser/exporter.cljs`，并新增对应测试。此为真实源码和合并记录，能证明修复已合并至相应开发分支；未核实进入哪一个稳定发行版本，也未由本项目运行测试。参见 S4。

候选方法：图节点的显示名与稳定 ID 分离；同名属性、标签、人物或组织不应因文本相同而被错误合并。需要在合成数据上测试两种导入顺序。

### 1.3 Trilium：ZIP 导出与数据库备份用途不同
官方 Import & Export 指南明确建议：全根节点 ZIP 导出不能替代数据库备份。备份保留笔记 ID、选项和 token，并更妥善处理受保护笔记。自 v0.104.0 起，导入根节点会将其放在现有根节点下作为子节点，避免覆盖既有根。单纯检查页面标题和正文无法验证身份及关系的完整恢复。参见 S5。

官方 Markdown 指南称，受保护笔记需要先开启受保护会话才能导出；导出内容为未加密形式，重新导入后需要重新保护。该流程存在保护状态降级和明文临时副本风险。参见 S6。受保护笔记正文、标题和附件加密，但结构、时间戳和属性不加密；不能将“笔记受保护”解释成“全部图谱元数据保密”。参见 S7。

### 1.4 Trilium：备份加密的时间边界
官方 Backup 指南列出每日、每周、每月、升级前四类自动备份（总数上限四份，具体客户端功能另有差异），并描述 .tnbackup 使用 AES-256-GCM、scrypt 和随机 salt 的备份加密机制。**启用加密只影响随后新建的备份，旧备份仍可能是未加密文件。** 官方也指出恢复旧数据库时，多设备同步成员必须协调，否则可能被较新状态覆盖。参见 S8。以上为厂商文档，不代表本轮完成了密码学实现审计。

## 2. 对照与可反驳验收矩阵（均 NOT_RUN）

| 合成场景 | 需要检查的结果 | 失败定义 |
| --- | --- | --- |
| G01 相同显示名的属性和标签，先导入属性 | 类别与属性的稳定 ID、类型、边保持区分 | 发生实体混并或非法属性 |
| G02 同样输入，反转导入顺序 | 与 G01 语义等价 | 顺序改变图谱身份 |
| G03 EDN/SQLite/Markdown 各导出再导入 | 节点、关系、类型、属性、时间戳、附件逐字段比对 | 预期保留字段缺失；区分格式限制与程序缺陷 |
| G04 对相同页面执行两次导入 | 明确 append/replace/upsert 语义，记录内容数变化 | 声称幂等而产生重复 |
| G05 Trilium 根 ZIP 与 DB 备份分别恢复 | note ID、branch、attribute、token、受保护状态逐项检查 | 将 ZIP 的预期身份变更误报为备份恢复成功 |
| G06 受保护笔记导出和回导 | 导出文件的明文状态、回导保护状态、残留副本 | 受保护内容意外明文留存或未重新保护 |
| G07 先生成明文备份再开启备份加密 | 新旧备份逐份标记、验证可读取性 | 错误声称旧备份自动加密 |
| G08 删除后恢复旧备份并同步 | 撤销标记、派生关系、备份副本及远端状态 | 已撤销数据未经重新授权被恢复使用 |

以上是研究方案和验收口径，没有执行产品代码，也没有使用任何用户数据。未来只在确定零新增费用、冻结版本和许可边界后使用纯合成数据进行离线测试。

## 3. E 当日治理增量核查

E001 当日已完成正式只读审计，避免重复新建 E 日报。本轮读到 main 新增 R127 构造数据、独立验证脚本、工作流和临时报告。R127 临时报告在提交时明确 CI 尚未核验，原始239 v7.6 保留 157 项待逐项审计。

本轮通过 GitHub REST 只读查询直接核实：R127 push workflow run 40099180033 对应提交 d58f71bceacc08fba2ae8b0ce478dc51e54900e3，状态 completed，结论 success；其 Python 3.11 和 3.12 两个 job 均 completed/success，步骤中“Independent exact payoff and tamper audit”与“Unmodified original 60 tests”均标为 success。该状态发生于临时报告写作之后，属于后续核验增量，不能倒推报告写作时已核验，也不能代替 R 主线正式接受收据或原始239 索引更新。未独立复算原始数据、日志全文或科研结论；R127 仍需由 R 轨决定正式验收。证据限于现有 CI 状态与步骤元数据。run URL: https://github.com/edwardsage419/Psychohistory-Research/actions/runs/40099180033

另外确认 A 轨 Kim 2023 数据搜寻记录为 PUBLIC_METADATA_ONLY，尚未读取原始数据、许可证或 R073 可评分字段；TH012 理论研究提交存在。未发现本轮有理由改写 R、A、TH、original239 或冻结协议。未进行全仓哈希巡检。README 导航滞后仍为 E001 已知 OPEN 问题。

## 4. F 本周专题状态

F001（2026-W43）已经完成，不重复创建 F 文件。为下周 F002 登记具体风险：受保护笔记导出后可能形成明文副本；启用备份加密不会追溯加密旧文件；回导可能重建已经撤销的数据与派生关系；UI 隐藏、内容加密、备份加密和授权撤销是四种独立控制。仅提出合成验收方案，不接入真实敏感数据或提前开发个人决策产品。

## 5. 证据等级、费用、归档与后续

evidence_scope:
* MARKET-E1-OFFICIAL-DOC：Logseq/Trilium 功能、导出、备份和加密说明。官方声明未经本轮实现验证。
* MARKET-E2-UPSTREAM-CODE-REVIEW：Logseq PR #13629 的合并状态、源码修改和新增测试文件；未运行代码，稳定发行覆盖未知。
* MARKET-ISSUE-UNREPLICATED：Logseq #959/#957 为上游公开缺陷报告；未独立复现，不代表总体故障率或用户效果。
* R 系列 E1/E2/E3 完全独立于上述市场证据。无真实人生决策质量改善证据。

work_performed: 直接读取英文官方技术文档、上游 PR/issue、E001/F001/MKT007/MKT008、R127 临时报告和 GitHub Actions run/jobs 元数据，形成 8 项可反驳合成测试矩阵。
output_paths: research/market/MKT009_LOGSEQ_TRILIUM_ROUNDTRIP_BACKUP_ENCRYPTION_2026-10-24.md
commit_sha: 以 GitHub 实际提交和回读核验为准，本文件不预填。
ci_status: 本轮未主动运行 CI；只读核验 R127 已有 push CI。
billing_checked: 未购买、未注册、未部署云端、未下载付费资料、未调用计费 API 或启动 CI；主动新增费用 0。GitHub 免费额度与账户整体账单未独立核验。
blockers: 未安装或运行 Logseq/Trilium；未验证格式往返、权限恢复、备份密码学实现及真实删除传播；上游修复是否进入稳定发行版本未知；E/F 不具有独立定时调度器，沿用已有每小时研究任务内的每日/每周登记。
next_action: MKT010 深入分析免费本地优先量化工具的真实数据导出与撤销机制，优先 ActivityWatch 或 Open Humans；若继续 Logseq，则仅针对 2026-10 合并修复的版本可用性和回归测试证据做增量。E 次日按日志重新巡检，F002 下周研究备份及衍生数据删除传播。保持全部 R 系列先完成、再分类、最后熔炼。

## 6. 英文公开来源（2026-10-24 核查）

S1 https://github.com/logseq/docs/blob/master/db-version.md
S2 https://github.com/logseq/db-test/issues/959
S3 https://github.com/logseq/db-test/issues/957
S4 https://github.com/logseq/logseq/pull/13629
S5 https://docs.triliumnotes.org/user-guide/concepts/import-export
S6 https://docs.triliumnotes.org/user-guide/concepts/import-export/markdown
S7 https://docs.triliumnotes.org/user-guide/concepts/notes/protected-notes
S8 https://docs.triliumnotes.org/user-guide/setup/backup
