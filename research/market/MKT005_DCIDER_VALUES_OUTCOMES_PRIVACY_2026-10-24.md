# MKT005 Dcider 价值权重、选项评分、结果追踪与隐私生命周期审读

研究日期：2026-10-24（Asia/Shanghai）
track: commercial_market
subflow: product
status: COMPLETE_BOUNDED_DOCUMENT_REVIEW
observed_main_head_before_write: 0b57a39624b9db874a6c4913eb6183c73f67d34a
preflight: 已读取 MKT003、MKT004、E001、F001、统一工作流规范；检索 MKT005 相关提交无命中，目标路径写入前 NOT_FOUND；E 当日与 F 本周均已有专题，避免重复。只用公开英文网页与学术资料，没有安装产品、创建账户、试用、提交个人决策或调用 API。

## 1. 产品机制与证据分层

1. **产品身份及发布渠道**。Dcider 官网直接指向 App Store，官方自述目前仅 iOS；App Store 地区页 id6756816042 展示名 Dcider，开发者 Jose Mota Cruz，英文功能介绍包含价值观、AI 决策分析、历史记录和结果追踪。隐私及服务条款的运营主体为 Mota International LLC。两者信息可并列记录，但本轮未核查公司与开发者的法律关联。官网和商店均属厂商/分发平台资料，非独立产品效能验证。来源 S1、S4、S5，MARKET-E1。
2. **输入与状态表达**。官网介绍首次设置价值观（健康、家庭、职业成长、经济安全、创造力等），由用户给出重要程度，可在设置中调整；随后输入决策情境，AI 提问澄清并提出候选方案。隐私政策明确列出个人价值及其重要性权重、决策描述、备选项、已选结果、类别、笔记和事后结果评分，外加账户、设备、使用和诊断数据。没有公开严格的数据字典、字段范围、状态转移规则或时间粒度。来源 S1、S2，MARKET-E1。
3. **评分与建议**。官网承诺显示每个备选方案与预设价值观的 alignment score，用户拥有最终决定权。尚未披露分数的计算公式、归一化、模型版本、AI 对选项的贡献、价值权重的可加性假设、风险约束、置信区间或概率校准。官网“objective alignment score”是营销表达，不能推断为客观人生价值或经科学验证的最优选择。来源 S1、S3，评分功能为 MARKET-E1 厂商说明，效能主张 MARKET-E0。
4. **反馈与结果追踪**。官网说明记录已做决策、结果和模式；服务条款另列 outcome tracking/reflection 与 achievement/milestone tracking。公开资料未说明结果如何被观测、何时评价、是否有反事实对照、是否自动更新价值权重或评分参数。仅能确认宣称提供记录和回顾功能，不能认定存在已验证的强化学习或因果更新。来源 S1、S3，MARKET-E1。
5. **运行与网络依赖**。官网表示离线可查看价值观和历史，AI 分析需要网络并由云端服务器处理。隐私政策称第三方云基础设施负责存储与认证，AI 服务商处理决策内容；服务商身份和模型版本未在所读页面公开。厂商称 AI 服务商不保存决策内容或用于训练，尚无独立流量或合同审计。来源 S1、S2，MARKET-E1 厂商政策声明。
6. **隐私与生命周期**。隐私政策列举传输/静态加密、行级安全控制 RLS、员工访问控制；用户可在设置导出、编辑和删除，单条决策保留至删除，操作日志最长90天，删除后备份可能保留最长30天，另有法律/业务保留例外。用户删除请求的传播、第三方副本与备份期限均未实测。首页 FAQ 的“never share ... with third parties”与正式政策允许受托服务商处理的措辞存在解释口径差异，应以完整政策逐项区分“出售”“分享”“受托处理”，不能据此直接认定违规。来源 S1、S2，MARKET-E1。
7. **商业模式**。官网及条款公布7天试用、月费4.99美元、年费44.99美元，官网称试用不需信用卡；条款规定 Apple App Store 订阅自动续费，具体商店地区价格可能不同。未注册、未试用、未支付。来源 S1、S3，MARKET-E1。
8. **局限与责任边界**。服务条款明确 AI 输出可能错误、有偏差，不构成医疗、法律或财务专业建议，决策由使用者承担。未找到独立前瞻研究证明该产品能减少长期决策错误、改善校准或跨领域长期结果。此为本轮有限资料检索结果，不能等同全网不存在。来源 S3，MARKET-E1 与 INDEPENDENT_EVIDENCE_NOT_FOUND。

## 2. 与公开方法研究的差距

英国政府公开 MCDA 指南说明，加权求和中的权重应结合各准则从最差到最好的实际变化幅度进行 elicitation（swing weighting），只根据“健康比财务重要多少”的抽象标签给权重容易产生误导。指南建议对权重进行敏感性分析。此为通用方法指导，不代表 Dcider 实际采用或违反某个算法。来源 S6、S7，METHOD_PRIMARY_GUIDANCE。

公开 2026 年研究展示，归一化方式可以在权重和原始数据相同时改变 TOPSIS 选项排序。该结论适用于其研究的 MCDA 设置，不能推断 Dcider 使用 TOPSIS 或存在同样的错误。来源 S8，METHOD_PEER_REVIEWED。

公开开源 DecisionMatrix MCP 项目文档展示加权求和、加权乘积、TOPSIS、权重敏感性和逐项解释，并提示选项集合内归一化所得分数属于相对排名。其代码和 README 是开源开发者资料，本轮未下载或复算，不能当成经独立验证的科学产品。其远程接口存在配额与付费层级，心理史学项目不调用。来源 S9，OPEN_SOURCE_AUTHOR_DOCUMENTATION。

## 3. 对心理史学的候选研究储备

MKT005-H1：未来决策模型的用户价值权重必须记录时间、获取方式、语境和允许变化区间。不能设定唯一固定的人生效用向量。价值偏好与预测事实分别记录。
MKT005-H2：在合成反例上预冻结评分方法，检验权重扰动、准则单位/归一化、增删无关选项、缺失值与不可补偿硬约束是否改变推荐。对排序不稳的情形明确显示多个可接受方案或拒绝单一排序。
MKT005-H3：未来将 ex ante 预测、用户自主选择、ex post 结果、不可观测反事实及模型事后校准分开记录。只有结果回顾不能证明某建议造成了改善。
MKT005-H4：评分须绑定实际输入、证据来源、模型版本、可复算计算路径、风险与不确定性，避免把语言模型生成的数值包装为已校准概率。
MKT005-H5：未来权限设计需分离本地可见历史、云端推理所需的最小数据、第三方服务处理、账户删除、备份删除及衍生统计；默认人工最终决定。
MKT005-H6：对厂商营销“客观评分”与真实长期决策效果设置独立验证门槛。不得将 MARKET-E1 厂商文档升级为 R 系列真人 E2 或历史 E3。

上述均为候选方法，不修改 R073、PESEN v0.1 或任何冻结协议，不启动个人决策产品开发。

## 4. E 当日与 F 本周状态及新增治理观察

E：已读取 research/operations/E001_READONLY_PROJECT_AUDIT_2026-10-24.md，当日已有实质检查，无需重建。此轮另读最新 main 提交：R122 的 2cbf3e71 只新增 research/validation/R122_THIRD_METHOD_ASYNC_BITMASK_PROTOCOL_FREEZE_2026-10-24.md；TH008 的 0b57a396 更新 theory/INDEX.md 和理论笔记；original239 v7.1 提交 85270e7a 新增 workflow 文件。对 85270e7a 的 combined status 查询返回空列表，故 **不能**将其解释为 CI success 或 CI failure，相关运行结论保持 PENDING_DIRECT_RUN_CHECK。原始239 v7.1 提交消息称待审162项，仅确认消息与文件提交，未独立重算该队列。E001 中 README 导航滞后问题继续 OPEN。本轮未对全仓冻结文件做 SHA 巡检，不能宣称全部未改变。
F：本周 research/privacy_safety/F001_HUMAN_OVERRIDE_AND_DATA_MINIMIZATION_2026-W43.md 已完成，避免重复 F002。本轮新增候选案例为 Dcider 云端推理、第三方受托处理与30天备份删除窗口，留待下一周 F002 的本地优先及衍生数据删除专题。独立 E/F 定时任务创建本轮仍返回 unavailable，未成功创建；现有每小时市场任务承担 E 日/F 周检查目标。
主线：全部 R 系列先完成，再系统归纳分类，最后模型熔炼。

## 5. 执行、归档与费用

work_performed: 实际读取 Dcider 官网、隐私政策、服务条款、公开 App Store 地区页，英国政府 MCDA 指南、2026 年开放学术论文、开源 MCDA 工具 README；核对 MKT003/MKT004/E001/F001/工作流规范及 R122、TH008、original239 近期提交。
evidence_scope: MARKET-E1 厂商/分发平台资料；MARKET-E0 未验证营销；METHOD_PRIMARY_GUIDANCE；METHOD_PEER_REVIEWED；OPEN_SOURCE_AUTHOR_DOCUMENTATION。没有产品实测、外部独立决策效果验证。
output_paths: research/market/MKT005_DCIDER_VALUES_OUTCOMES_PRIVACY_2026-10-24.md
commit_sha: 由 GitHub create_file 返回，提交后单独核验；本文件内容内不预填未知 SHA。
ci_status: NOT_RUN；combined status 对既有 workflow commit 查询为空，不等于运行结果。
billing_checked: 本轮未新增购买、注册、订阅、计费 API、云服务、远程 MCP 调用或 CI 操作，新增主动操作费用 0；账户整体账单、GitHub 免费额度未独立核验。
blockers: 评分公式、价值权重提取、模型供应商、用户效果及数据删除实测不可得；E/F 独立调度创建不可用。
next_action: MKT006 深入 PaOS 的 11 个 AI 智能体、个人知识图谱、数据权限与可解释性，优先核查是否存在公开接口或技术白皮书；若缺乏可验证技术资料，则研究公开本地优先开源决策系统。

## 6. 公开来源（非中文，2026-10-24 访问）

S1 https://dcider.app/
S2 https://dcider.app/privacy
S3 https://dcider.app/terms
S4 https://apps.apple.com/jp/app/dcider/id6756816042
S5 https://apps.apple.com/de/app/dcider/id6756816042
S6 https://analysisfunction.civilservice.gov.uk/policy-store/an-introductory-guide-to-mcda/
S7 https://www.gov.uk/government/publications/green-book-supplementary-guidance-use-of-multi-criteria-decision-analysis/use-of-multi-criteria-decision-analysis-in-options-appraisal-of-economic-cases
S8 https://www.mdpi.com/1099-4300/28/1/114
S9 https://github.com/inity13/decisionmatrix-mcp
