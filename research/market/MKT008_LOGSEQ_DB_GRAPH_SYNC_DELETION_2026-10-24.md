# MKT008 Logseq DB 知识图谱、权限与删除生命周期有界审读

研究日期：2026-10-24（Asia/Shanghai）
track: commercial_market
subflow: product
status: COMPLETE_BOUNDED_PRIMARY_SOURCE_REVIEW
observed_head_before_write: 789e02998647059f47cd55fcfb72d7b12cb0931a
preflight: 已读取 MKT007、MKT006、E001、F001、docs/PROJECT_WORKFLOW_REQUIREMENTS_V2_2026-10-24.md 与 main 最近提交；目标文件写入前返回 NOT_FOUND，仓库 MKT008 提交检索无结果。只读英文公开资料，无安装、登录、付费或真实个人数据。

## 1. 本轮真实新增机制

1. **版本与数据输入**。Logseq 原有文件图谱使用 Markdown/Org 文本属性；新的 DB 图谱以 SQLite 为持久化数据容器，支持文本、数字、日期、复选框、URL、节点引用等属性，以及标签、父标签继承、双向属性与页面或块引用。数据库开发者指南把属性定义 schema 与属性值分开，公开 `getProperty`、`upsertProperty`、`upsertBlockProperty` 等 SDK 接口。记录、属性和关系可结构化，但并未证明存在可计算人生效用或预测模型。来源 S1、S2、S3。等级 MARKET-E2-OPEN-DOCUMENTATION，未运行源码。
2. **本地状态与版本风险**。官方仓库 README 将 DB 版标为 beta，将新移动端和实时协作同步标为 alpha，明确提示存在数据丢失可能并建议备份。官方 DB 文档标注功能描述基准日期 2026-04-28；文档“latest stable”与 README 的 beta 风险说明应并列保存，具体发行版成熟度需以版本与发行记录复核。来源 S1、S2。
3. **权限与隐私边界**。DB SDK `PropertySchema` 含 `hide` 与 `public` 字段；开发指南把 `hide` 描述为 UI 属性面板隐藏。隐藏显示不能自动推断为加密、读权限隔离或秘密数据保护。DB 图谱的插件与脚本有读取及写入属性能力，第三方扩展的授权范围与审计需要另行核验。未查到可用于本轮证明所有图节点均具备细粒度访问控制的公开验收记录。来源 S3、S2。
4. **删除与恢复语义**。官方 DB 文档称普通页面被移入回收状态，可在 30 天内恢复；标签、属性、当天日记页面删除为永久操作，其他未特别说明的删除也没有回收机制。该行为只说明应用界面的恢复窗口，不能证明历史 SQLite 页、备份、远端同步副本和派生节点均已安全擦除。来源 S2。与 MKT007 Trilium 的同步墓碑文档属于不同实现，不能直接套用 Trilium 的墓碑结论。
5. **备份与导出保真度**。官方 DB 文档称桌面自动备份保留最近 12 份，浏览器选择目录后每小时备份且保留最近 12 份。提供 SQLite、SQLite+附件 ZIP、EDN、标准 Markdown 等导出；标准 Markdown 明确不保留全部属性或时间戳，EDN 可表达更完整的图数据但官方不建议作为唯一备份。导出成功不等于数据可完全重建；删除后的备份留存是单独风险。来源 S2。
6. **同步与费用**。官方 DB 文档称 Logseq Sync/RTC 是付费且邀请制，支持实时协作；也描述自行托管的可能性。上游 `deps/db-sync` README 包含 Cloudflare Worker 与 Node 适配器、管理员删除图谱及用户的脚本，但文档中的删除命令不证明所有副本及缓存被安全擦除。项目不订阅同步、不注册、不部署服务器，不调用任何云 API。来源 S2、S4。同步确切价格本轮未从可靠官方资料核实，记 UNKNOWN。
7. **许可证**。直接读取上游 `logseq/logseq/LICENSE.md`，确认为 GNU Affero General Public License v3 正文，blob `0394f2b6e73d87eff0394dc454f3b189d5fce14f`。未来商业代码复用必须先做许可证义务审查；本轮仅阅读方法，未复制实现。来源 S5。
8. **与 Trilium 比较**。Trilium 公开 Note/Branch/Attribute/Revision/Attachment 及同步墓碑文档；Logseq DB 公开更细的类型化属性、节点、标签继承、备份导出及回收机制。两者的权限与删除生命周期风险各异。两者均无本轮可独立复验的跨领域人生预测质量、因果识别或长期决策改善证据。来源 MKT007、S2、S3。

## 2. 候选方法与未来可反驳测试

MKT008-H1：未来个人状态图的每个属性区分 schema、观察值、来源、用户确认、模型推断、时间有效期、敏感级别与授权目的；对 UI 隐藏、访问控制和静态加密分别设计独立测试。NOT_RUN。
MKT008-H2：建立合成图的删除矩阵：普通页面、标签、属性、附件、引用、派生摘要；分别观察活动数据库、回收区、最近 12 份备份、导出文件和同步副本。仅提出方案，尚未执行。
MKT008-H3：构造人工图谱含时间戳、数字属性、节点引用、标签继承、附件，比较 SQLite、EDN 与 Markdown 导出再导入后的结构差异；在选定版本上冻结输入并逐字段验收。NOT_RUN。
MKT008-H4：将结构化图谱、静态规则、单模型和多智能体决策建议置于相同合成测试集，检验来源保真、冲突提示、撤销后禁止继续读取和错误建议拒绝能力。不得用图谱丰富度冒充预测性能。
MKT008-H5：对公开许可证、同步服务付费边界、数据保留和安全承诺逐项设置证据门槛，未来只考虑确认零新增费用的本地方法研究。

## 3. E 当日治理增量核对

2026-10-24 已有 E001 完整有界只读审计，本轮避免重复创建 E 文件。直接读取 original239 v7.6 交叉索引 blob `cac8c19dd4459e89f28c1f4562cc21f86928f639`：实际 rows=239、provisional_itemwise_audit_open_count=157，05-002 已关联 R126；R126 接受收据 blob `26839c249bc731acf800604a0a5f13010b9b4738` 自报 CI run 40095282746 为 completed/success，新增 E2/E3 均 0，原论文 Table 3 舍入差异仍未解决。直接读取新 R127 第三方法冻结提交 `6223c0980c42c147bd32eb2a75bb391568139da4`，协议明确第三方法代码和结果尚未开始、原始239队列不得提前减项。R126 接受提交的 combined statuses 查询返回空列表，本轮没有独立验证其 GitHub Actions jobs，不能据收据宣称本轮 CI 已核验。TH011 理论提交及其索引已存在，主线未见被商业研究替代。全仓冻结哈希、全部 CI 和账单均未完成巡检。README 导航滞后仍 OPEN。E 不改写 R/TH 或 original239 索引。

## 4. F 本周专题状态

2026-W43 的 F001 已归档并完成有界标准审读，本轮不重复创建 F 文件。新增 F002 下周反例：Logseq 普通页面 30 天回收、特殊页面直接删除、最近 12 份自动备份、Markdown 导出丢失属性，及 UI hide 字段不代表数据权限；未来分别测试撤销后的源数据、衍生边、备份、远端副本与审计日志。无真实敏感数据或产品开发。

## 5. 验收、费用与下轮

work_performed: 直接阅读上游 Logseq LICENSE.md、DB 官方文档、属性 SDK 开发指南、DB Sync 上游 README，比较 MKT007；直接读取项目 crosswalk v7.6、R126 收据、R127 冻结提交、E001/F001 与统一工作流规范。
evidence_scope: MARKET-E2-OPEN-DOCUMENTATION（公开源码/开发者文档可核查，尚未运行或安全审计），MARKET-E1（官方功能与费用说明），未获得独立产品效果验证；与 R 的 E1/E2/E3 证据体系分开。
source_links: S1-S5 及本报告前述 GitHub 记录。
output_paths: research/market/MKT008_LOGSEQ_DB_GRAPH_SYNC_DELETION_2026-10-24.md
commit_sha: 提交后在 GitHub 回读确认；不预填。
ci_status: NOT_TRIGGERED_BY_THIS_RUN；文档提交采用 [skip ci]，是否触发其他自动运行需独立核查。
billing_checked: 未付费、未注册、未安装、未部署云服务、未调用收费 API、未主动触发 CI；本轮主动新增费用零。账户整体账单及 GitHub 免费额度未核实。
blockers: DB beta/alpha 风险；未验证实际删除、恢复与导入一致性；未获得独立安全和长期决策效果证据；Logseq Sync 官方精确定价未知。
next_action: MKT009 对比 Logseq DB 与 Trilium 的导出可逆性、图关系撤销与本地备份可验证性，或选择另一款有公开源码的离线个人量化工具，避免重复已有 MKT001 至 MKT008。E 明日按登记重新审计；F002 下周专题研究删除传播。

## 6. 非中文原始来源（2026-10-24 访问）

S1 https://github.com/logseq/logseq
S2 https://github.com/logseq/docs/blob/master/db-version.md
S3 https://github.com/logseq/logseq/blob/master/libs/guides/db_properties_guide.md
S4 https://github.com/logseq/logseq/blob/master/deps/db-sync/README.md
S5 https://github.com/logseq/logseq/blob/master/LICENSE.md
