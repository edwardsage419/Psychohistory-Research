# MKT006 PaOS 多智能体路由、个人知识图谱与安全声明边界审读

研究日期：2026-10-24（Asia/Shanghai）
track: commercial_market
subflow: product
status: COMPLETE_BOUNDED_DOCUMENT_REVIEW
observed_main_head_before_write: a40a8efa2a19fcd23f584fc44c84c3f36ca9cae3
preflight: 已读取 MKT005、MKT004、E001、F001、统一工作流规范及 main 最近18次提交；本目标路径在写入前查询为 NOT_FOUND。仅检索英文公开网站，不注册、不试用、不调用产品接口、不接入个人资料。

## 1. 本轮确实新增的产品机制

1. **11 个角色与编排结构**。PaOS 官网列出 Router、Task Planner、Scheduler、Researcher、Decision Advisor、Goal Coach、Wellness Monitor、Financial Advisor、Synthesizer、Action Proposer、Knowledge Graph Builder，共11个命名角色。官网同时称 Router 分析请求、召集相关角色、Synthesizer 合并输出并提出行动。这说明厂商所称“11 AI agents”包含路由、综合与知识图谱构建等编排角色，不能将其理解为11个相互独立的专业预测模型。官方没有公开调用拓扑、模型供应商、提示模板、冲突解决规则、各角色误差评估或实际运行轨迹。来源 S1；MARKET-E1 厂商功能声明，独立运行验证缺失。
2. **输入与状态表达**。官网描述五个 life perspectives：Business、Family、Health、Learning、Creative；个人知识图谱连接 values、relationships、goals 和 context，并声称智能体在回答前参考该图。输入还包括任务、里程碑、日历、Gmail 和 Whoop 的恢复、睡眠、负荷数据。未找到公开的图节点/边 schema、关系时间戳、冲突证据优先级、推断置信度或图更新/删除协议。不能推断存在可复算的长期人生状态方程。来源 S1；MARKET-E1。
3. **行动与反馈**。官网称 Goal Coach 跟踪目标进展、发现阻碍并建议下一步；Scheduler 优化日程；Decision Advisor 比较取舍；Action Proposer 提出动作。官网未披露任何可验证的优化目标函数、约束集、前瞻预测校准、因果识别或真实行动成功率；“优化”目前仅属功能用语。无法确定建议是否需要人工确认、能否自动修改日历或发送消息。来源 S1；MARKET-E1，效能声称 MARKET-E0。
4. **隐私与权限**。官网自述 Firebase Authentication、Google Cloud、API keys 使用 Fernet 加密、数据库保存 tokens、可导出知识图谱到 Obsidian，并宣称从不出售或分享数据。页面标题使用“End-to-End Encryption”，具体解释只明确 API keys 加密；尚无证据说明用户所有内容在服务器不可解密、是否真正端到端加密、第三方 OAuth 权限范围、撤销后的缓存与衍生图清除、数据保留期限或删除传播。直接访问 /privacy 与 /terms 返回相同的简化产品介绍页面，未获得可供逐项核查的完整政策文本。不能据此认定其没有隐私政策，也不能独立验证“从不分享”。来源 S1、S2、S3；MARKET-E1 厂商声明与有限公开资料检索。
5. **安全合规证据边界**。PaOS 自称采用 HIPAA-eligible infrastructure、SOC 2 compliant stack。Google Cloud 原始官方指南明确：受 HIPAA 约束的客户须核查适用服务、接受 BAA 并自行保证所建应用配置与合规，基础设施合规不自动证明应用整体合规。Firebase 官方文档证实其服务存在 SOC 审计与加密机制，不能据此推出 PaOS 本身已经获得独立 SOC 2 报告或符合 HIPAA。PaOS 官网未提供本轮可独立核验的产品级报告、BAA 或审计范围。来源 S1、S4、S5；GOOGLE_PRIMARY_COMPLIANCE_GUIDANCE + MARKET-E1，产品级合规 INDEPENDENT_NOT_VERIFIED。
6. **费用模式**。PaOS 官网公布 early adopter 3个月免费、无需信用卡，之后 Pro 为每月19美元。注册、试用、订阅均未执行；免费试用有到期后的收费安排，不能把其当作项目长期免费依赖。来源 S1；MARKET-E1。
7. **产品状态与证据空缺**。本轮只验证官网公开内容，未取得可公开复现的 API 文档、知识图谱导出样本、架构白皮书、独立测评或真人长期决策改善试验。此为有限搜索下的未找到，不能声称相关材料绝对不存在。未核验活跃用户数、付费转化率或服务可用性。

## 2. 对心理史学的可测试候选方法

MKT006-H1：将输入事实、用户确认价值、模型推断、任务、行动建议、实际行动与后果记录成不同类型节点，并对每条关系绑定来源、时间、授权、证据等级与有效期。知识图谱结构只是候选，未实施。

MKT006-H2：多智能体协作必须与单模型、简单规则、预先冻结的无路由基线比较，报告额外计算开销、错误传播、意见冲突和最终预测损失；角色数量不应充当性能证据。

MKT006-H3：在未来合成案例中冻结路由策略，测试不同角色对同一事实给出冲突结论、遗漏高风险约束、工具输出污染、重复计数证据、图谱过期、用户偏好变更等情形。比较路由合成器是否忠实保留不同观点及不确定性。

MKT006-H4：每个拟执行动作分离为 proposal、user_authorization、execution、outcome 四阶段；默认只读建议，尤其对邮箱、日历、健康及资金操作不得因“智能体可执行”推断已有用户授权。

MKT006-H5：对任何云端个人图谱必须分别验证导出完整性、第三方连接撤销、源记录删除、派生关系清除、备份保留和日志处理；F 专题后续研究，当前不接入真实数据。

MKT006-H6：区分供应商平台的 HIPAA/SOC 报告与具体产品自身的安全控制和合规范围；不以厂商官网声明替代独立审计。

所有 H 项为未来模型分类/熔炼的候选知识储备，不改动 R073、PESEN v0.1 或其他冻结协议，不预设唯一人生效用权重，也不提前开发个人决策产品。

## 3. E 当日治理与 F 本周专题状态

E：2026-10-24 E001 已登记 COMPLETE_BOUNDED_READONLY_AUDIT，避免重复创建当日 E 文件。本轮新读的最近 main 提交显示 R122 已有有限合成 E1 复核相关报告与 original239 v7.2 的队列提交消息（称161项仍待审）；另有 R123 新协议冻结提交 0ddb7e16、TH009 理论提交 a40a8efa。仅核验提交存在和 E001 的原有范围，未独立复算 R122 的16930案例、v7.2 队列或查询全部 CI jobs，因此 R122 科学验收与 CI 结论在本轮均为 PENDING_DIRECT_RECHECK。E001 所记 README 导航滞后仍 OPEN；未逐文件哈希巡检所有冻结协议。R123 的“freeze”提交仅证明提交消息和协议存在，不能推定其后续计算完成。此轮不更改 R 或理论轨文件。

F：本周 F001 已完成，避免重复。新增 F002 候选反例：OAuth 连接撤销后旧知识图谱中的派生健康/关系边是否保留；平台 SOC/HIPAA 声称的责任边界；“End-to-End Encryption”与只加密 API key 的差别。均为待研究问题，未执行 F002 专题。

调度：三条原有每小时任务存在且商业任务内已包含 E/F 日历检查；尝试额外创建独立 E 每日与 F 每周自动任务返回 unavailable。依照仓库工作流规范 v2.0，E/F 保留为独立研究职责及路径，目前无独立系统触发器。不得虚报。

## 4. 本轮范围、成本、阻塞与下一步

work_performed: 读取 PaOS 英文官网及 /privacy、/terms 两路径公开返回内容；阅读 Google Cloud HIPAA 官方指南与 Firebase 官方安全文档；读取市场 MKT005/MKT004、E001、F001、统一工作流规范、main 最近提交，检查目标文件不存在。
evidence_scope: MARKET-E1 厂商声明；MARKET-E0 未验证效果；GOOGLE_PRIMARY_COMPLIANCE_GUIDANCE；无产品级独立审计或真人效果证据。
output_paths: research/market/MKT006_PAOS_MULTI_AGENT_GRAPH_SECURITY_2026-10-24.md
commit_sha: 待 GitHub 提交后另行回读核验，本文不预填。
ci_status: NOT_RUN；没有触发 GitHub Actions。
billing_checked: 本轮没有购买、注册、试用、订阅、付费 API、云算力、额外 CI，主动新增支出为零；未独立核验 GitHub 免费额度及账户账单。
blockers: 未获公开 schema、路由源代码、独立用户效果研究、完整隐私政策或产品级合规报告；独立 E/F 调度器创建不可用。
next_action: MKT007 优先分析一个开源本地优先的个人知识图谱/代理框架，核对真实源码、许可证、权限与删除语义；与 PaOS 的厂商自述进行可验证性对照。

## 5. 非中文公开来源（2026-10-24 访问）

S1 https://www.paos.app/
S2 https://www.paos.app/privacy
S3 https://www.paos.app/terms
S4 https://cloud.google.com/security/compliance/hipaa/
S5 https://firebase.google.com/support/privacy/
