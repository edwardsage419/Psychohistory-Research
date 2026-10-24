# MKT007 Trilium 本地优先个人知识图谱、同步墓碑与删除边界审读

研究日期：2026-10-24（Asia/Shanghai）
track: commercial_market
subflow: product
status: COMPLETE_BOUNDED_PRIMARY_DOCUMENT_REVIEW
observed_head_before_write: 5098c8837f20a04fa67619a6ba465ab631876977
preflight: 已读取 MKT006、E001、F001、docs/PROJECT_WORKFLOW_REQUIREMENTS_V2_2026-10-24.md、main 最近提交；目标路径写前不存在，MKT007 提交搜索无结果。只使用英文原始产品、开发者文档与开源仓库页面；未安装软件、运行源码、使用产品账号、调用付费接口或读取个人资料。

## 1. 研究对象与真实可核查机制

研究对象：Trilium Notes（TriliumNext/Trilium），开源本地个人知识库。与 MKT006 PaOS 厂商多智能体/个人知识图谱声称作证据可审计性比较。

1. **费用、许可证与部署**。官网称 AGPL-3.0、无付费层级、无需账号、可离线桌面使用；多设备同步需自行部署服务器或选用外部服务。开源仓库 README 与官网一致。研究只选择无需新设备、订阅或服务器的本地静态方法参考；不部署同步服务。来源 S1、S2。证据 MARKET-E2-OPEN-DOCUMENTATION（可检查仓库与官方开发文档）；未在本轮编译或运行。
2. **输入与状态表示**。官网说明笔记储存在本地 SQLite 数据库。开发者文档列出 Note、Branch、Attribute、Revision、Attachment 等实体。Branch 可让同一笔记在多个位置出现；Attribute 包括 label 与指向其他笔记的 relation；笔记关系图可展示引用、关系和树结构。这里的“图谱”有明确实体与关系文档，仍属于知识管理结构，不具备自动识别人生因果机制的能力。来源 S1、S3、S4。
3. **自动化与 AI 权限**。官方提供 token 授权的 ETAPI，允许读取、创建、更新笔记、属性、附件。AI 功能为主动选择开启，默认关闭；开启后可连接自带 API key 或自托管模型，并允许 AI 工具搜索、创建和修改笔记。官网未承诺自动规划人生的概率模型、最优效用或独立决策效益。项目不启用 API 或 AI。来源 S1、S5。
4. **敏感信息保护范围**。官方说明普通笔记默认不加密；用户显式设置受保护笔记后，标题、内容、图像和附件受保护，结构、修改日期及属性仍未加密。开发者指南确认单用户安装，不提供每条笔记细粒度的多角色授权。用户指南称 AES-128-CBC；另一开发者安全页面的概述出现 AES-256-CBC 与其内部 AES-128 数据密钥描述不一致。不能凭页面断言所有数据端到端加密或不存在元数据泄露。来源 S1、S6、S7。
5. **同步与冲突**。开发者文档描述客户端与自托管服务器双向同步、entity_changes 记录、内容散列、isErased 标记，以及内容冲突采用按修改时间的 last-write-wins。该机制可以同步删除和阻止已删实体被其他节点复活，但在并发编辑中也存在覆盖风险；没有本轮运行验证。来源 S8。
6. **删除传播的关键反例**。开发者专题明确指出：永久删除实体后，entity_changes 中 isErased=true 的墓碑记录长期保留，当前机制没有垃圾回收、全节点确认水位线、TTL 或压缩；初始同步可能重新处理历史墓碑。删除可见内容与清除同步元数据是不同事项。该文档还称删除笔记可能连带留下 branch、attribute、revision 的墓碑。此机制与未来个人敏感信息撤回和数据生命周期研究直接相关。来源 S9。不能把墓碑留存等同于已删原文仍可恢复，也不能证明历史备份已经同步删除。
7. **备份与残留**。用户指南记载日、周、月及升级前数据库备份，默认存放在本地 data/backup 目录。同步数据库副本和备份文件需要单独制定删除与保留策略；文档没有为本轮提供“所有副本与衍生关系已完全擦除”的自动验收证明。来源 S10。
8. **对比 PaOS**。PaOS 官网有多角色、个人图谱、云平台与安全宣称，MKT006 尚未取得完整图谱 schema、路由代码及删除协议；Trilium 有公开数据实体、API、加密边界、同步及墓碑文档，较容易设计可反驳的机制测试。两者用途不同，不能用文档透明度推断 Trilium 的长期决策质量优于 PaOS。

## 2. 候选方法与可证伪验证设计

MKT007-H1：未来候选人生状态图应区分观察事实、用户确认事实、模型推断、偏好、预测、建议、执行和后果，并给节点/关系绑定来源、时间、权限、证据等级、过期时间及撤回状态。当前只提出 schema 候选，不进行产品开发。

MKT007-H2：权限撤销测试应独立覆盖四个层次：停止新数据访问；删除活动原始记录；删除或标记无效的派生关系和模型摘要；处理本地/同步端备份、墓碑及审计日志。对每层预先声明可以验证的可观察结果与不可证明的完全擦除边界。

MKT007-H3：构造纯合成两客户端情景：A 修改记录，B 删除记录，之后重新连接；验证 last-write-wins 是否造成复活、旧关系保留或误删，分别报告内容、元数据和历史副本状态。此为未来试验方案，NOT_RUN。

MKT007-H4：比较“全部普通笔记”“仅敏感正文加密”“敏感属性也受保护”三种人工图谱，检查笔记内容隐藏后是否仍可由关系类型、时间戳或连接度推断敏感属性。仅为合成安全测试建议，尚无数据或结论。

MKT007-H5：在同等假设下比较静态规则、单模型、路由多智能体和图谱检索方案的建议质量、来源保真、风险遗漏、拒绝自动行动与额外开销。不得将开源图谱或 AI 接口本身视为决策预测已被验证。

MKT007-H6：对受保护笔记的加密算法及密钥管理，先核实确切代码版本并独立测试，解决官方文档摘要之间的不一致；本轮不能确认任何实现层面的密码学保证。

## 3. E 当日、F 本周去重与治理观察

E：research/operations/E001_READONLY_PROJECT_AUDIT_2026-10-24.md 已登记今日完整有界只读审计，故本轮不新增重复 E 文件。之后主线提交显示 R124 第三方法的有限 E1 报告与 original239 v7.4 队列，提交消息记录待审159项；R125 于 bccd77594f0d6729b50a84dd7c99939c158cadb5 新冻结矩阵树定理审计协议，其正文明确 NEW_EXECUTION_NOT_STARTED；TH010 提交 5098c8837f20a04fa67619a6ba465ab631876977。直接读取了 R125 提交 diff，其冻结状态只说明新协议存在，不能当作第三方法已执行。159 项来自提交消息，未逐项重算队列。未本轮逐一检查 R124 CI jobs、全仓冻结文件哈希或账户账单；这些保持 PENDING_DIRECT_AUDIT。README 导航滞后仍待 R 轨处理。

F：research/privacy_safety/F001_HUMAN_OVERRIDE_AND_DATA_MINIMIZATION_2026-W43.md 已完成本周专题，不重复归档。将“同步墓碑长期保留”“未加密属性可能泄露关系”“备份与派生信息删除传播”列为 F002 下周候选反例；尚未启动 F002，未接入敏感数据。

调度：现有每小时商业任务已包含 E 每日、F 每周执行登记。再次尝试分别创建 E 每日、F 每周独立自动任务，系统返回 unavailable。E/F 继续保留独立职责和目录，独立调度器未建立，不虚报。

## 4. 执行范围、费用、归档与后续

work_performed: 读取 Trilium 官方英文产品、开发者架构、关系、受保护笔记、API、同步、删除墓碑与备份文档，结合已归档 MKT006 对照；核对 main 提交、E001/F001 与统一工作流要求。
evidence_scope: MARKET-E2-OPEN-DOCUMENTATION 表示开源代码及开发者文档可供第三方检查，未实际运行、静态代码审计或独立验证；MARKET-E1 厂商功能陈述；没有真实用户长期决策效益证据，未形成 R E1/E2/E3。
output_paths: research/market/MKT007_TRILIUM_LOCAL_FIRST_GRAPH_SYNC_DELETION_2026-10-24.md
commit_sha: 由外部 GitHub 提交记录核验，本文不预填。
ci_status: NOT_RUN；提交消息使用 [skip ci]，仍需单独核查是否触发自动工作流。
billing_checked: 未注册、安装、订阅、购买、调用付费 API、部署服务器或主动触发 CI；本轮主动新增费用零。GitHub 账户整体账单及免费额度未独立核验。
blockers: 没有执行实际客户端删除、跨设备同步或源码级安全审计；无法证明完整数据擦除；E/F 独立定时任务创建不可用。
next_action: MKT008 比较开源 Logseq 与 Trilium 的本地状态、图谱权限、同步订阅及删除语义；优先核对 Logseq DB 版的公开源码和实际许可，再决定是否进入后续候选。F002 按下周登记独立研究删除传播；保持先全 R 后分类再熔炼。

## 5. 英文原始来源（2026-10-24 访问）

S1 https://triliumnotes.org/
S2 https://github.com/TriliumNext/Trilium
S3 https://docs.triliumnotes.org/developer-guide/concepts/entities
S4 https://docs.triliumnotes.org/user-guide/advanced-usage/attributes/relations
S5 https://docs.triliumnotes.org/developer-guide/architecture/api
S6 https://docs.triliumnotes.org/user-guide/concepts/notes/protected-notes
S7 https://docs.triliumnotes.org/developer-guide/architecture/security
S8 https://docs.triliumnotes.org/developer-guide/concepts/sync
S9 https://docs.triliumnotes.org/developer-guide/concepts/sync/entity-change-tombstones
S10 https://docs.triliumnotes.org/user-guide/setup/backup
