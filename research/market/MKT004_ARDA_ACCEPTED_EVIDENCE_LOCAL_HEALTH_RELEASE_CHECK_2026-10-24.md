# MKT004 ARDA 已接受证据、评分纠正、本地健康数据与发布状态审读

研究日期：2026-10-24（Asia/Shanghai）。
track: commercial_market；subflow: product；status: COMPLETE_BOUNDED_DOCUMENT_REVIEW。
observed_main_head_before_write: 3c0d96ee5208e40a2876e36ccb4c680ecf014832。
前置记录：已读取商业基线、MKT001、MKT002、MKT003、E001、F001、统一工作流规范及近期 R/理论提交；本文件目标路径写入前为 NOT_FOUND。研究使用公开英文资料，无账户、个人健康记录、付费功能、认证 API 或产品实测。

## 1. 本轮新增的具体产品机制

1. **公开发布状态与身份核查**。ARDA 官网支持页截至本次访问仍称处于 TestFlight，原目标为 2026 年 9 月上架；首页仍显示 Coming soon 和等待 App Store 链接。公开检索未找到能与 ARDA AI, INC. / Nicolas Rowe 明确匹配的正式 App Store 产品页，因此发布状态记录为 PUBLIC_RELEASE_NOT_CONFIRMED，不能从旧目标日期推定已经发布或必然未发布。检索中出现的“Life Audit AI” App Store 产品由 Sarah Tomor 提供，不能视为 ARDA。ARDA 价格和试用条件在官方支持页仍为尚未公布。来源 S1/S2/S6，MARKET-E1 及公开搜索的有限否定结果。
2. **输入及个人状态表达**。官网称 Life Audit 通过可暂停的引导对话采集用户自选的 11 个领域，建立 Life Profile；存储已接受的事实证据、评分、置信度、轨迹、目标、计划、历史和更正。敏感问题可拒答；缺失可能降低置信度或导致领域不可评估，设计说明不应默认为负面证据。公开资料未披露完整评分函数、跨领域权重、校准样本或误差分布。来源 S1/S2/S3，MARKET-E1。
3. **证据准入与评分纠正**。隐私政策明确要求从自由文本提取的内容在成为评分证据前须经过验证或接受，模型假设不得自动成为确认的个人事实。用户可检查事实、解释、评分和历史，纠正事实、补充证据或质疑方法；厂商称仅在新增或修正的已接受证据足以支持时才更新评分。纠正保留可见历史，删除个人证据可能改变评分或降低置信度。尚无独立实验验证其实现的稳定性、拒绝错误提取能力或用户纠错有效性。来源 S1/S3/S4/S5，MARKET-E1。
4. **AI 与长期状态分层**。ARDA 自述将账户、证据、评分和计划保存在 Supabase，OpenAI 用于限定任务的解释、草拟、规划和安全分类；服务器为单次请求选择相关上下文，AI 输出在产品确认前与已接受事实隔离。文档提到 eligible API 请求设置 store:false，并明确常规供应商滥用监测日志可能保留最多 30 天，尚未声称生产环境获得 Zero Data Retention。该机制属于厂商设计声明，没有第三方代码审计或真实请求追踪。来源 S3/S5，MARKET-E1。
5. **Apple Health 的隔离边界**。可选只读获取身高、体重、步数、锻炼、运动和睡眠，在设备本地展示；厂商称导入的原始 Health 记录不上传到 ARDA 服务器、不传给 AI、不自动改变 Life Rating。用户自行粘贴或输入的健康内容则成为提交内容，可进入服务器和 AI 处理。停止导入、删除本地副本和删除 Apple Health 原始记录是三种不同动作。来源 S1/S3/S4/S5，MARKET-E1。
6. **权限与删除的不同层级**。官网允许删除单条对话，但会在确认前提示该对话是否产生已接受证据；删除对话不会悄然删除已接受证据。特定证据的有限删除需联系支持；全账户删除可在应用内发起。隐私政策设计说明活动账户数据移除与 Supabase 备份过期最多七天，供应商滥用监测日志可能最长三十天，有限的不含内容完成凭证可能保留二十四个月。均为公开政策承诺，实际传播效果未测。来源 S3/S4，MARKET-E1。
7. **反馈与行动环**。产品文档说明 Chat 利用相关档案与计划帮助讨论选择，Plan 组织目标、项目、任务和周期性承诺，Overview 展示评分历史与当前行动；文档没有给出严格的长期因果推断、自动校准、样本外预测或数学优化算法。官网所列目标设定与进度监测元分析研究明确注明尚未测试 ARDA 产品本身。来源 S1/S2，MARKET-E0/E1。
8. **费用与服务依赖**。ARDA 的产品定价和试用条件未公布。公开列明 Supabase、OpenAI、Apple、Google Workspace、Railway 等外部依赖；厂商网站的运营成本不能推定为心理史学项目可免费复用的资源。本项目不调用相关服务。来源 S1/S5，MARKET-E1。

## 2. 可借鉴机制与科学问题

MKT004-H1：未来状态模型应区分 raw_observation、user_confirmed_fact、model_inference、rating、recommendation、correction_history，记录每条证据的来源、时间、权限、版本及确认状态。此为候选结构，未进入现有 R 系列。
MKT004-H2：在合成数据上预冻结错误事实提取、冲突事实、数据撤销、缺失信息、偏好改变等反例，比较“自动接受 AI 推断”和“必须确认才入库”的误纳入率、可纠正性及长期状态漂移。
MKT004-H3：缺失值应触发置信度降低或拒绝评分的候选规则，未来必须评估不同群体与缺失机制下的公平性及误拒率，禁止将未知默认为差。
MKT004-H4：未来数据删除需要记录 provenance graph，区分会话文本、衍生已接受事实、评分、计划、日志、缓存和备份；撤销授权后旧数据的处理应可见、可测试。
MKT004-H5：对厂商给出的“人生评分”须单独验证评分构念效度、信度、跨时间可比性、偏好权重来源和实际决策效益，禁止将评分展示直接当成客观人生质量。
MKT004-H6：高敏感来源先考虑本地计算和隔离，若用户将相同数据自行粘贴进 AI 对话，必须明确不同的数据路径及风险。未来产品开发仍暂停。

## 3. 证据分级与未解问题

本轮结论为 MARKET-E1 厂商官网、支持页、隐私与信任文档支持的公开设计和政策陈述；MARKET-E0 为营销展示与自述效果。没有 MARKET-E2 独立产品测试、MARKET-E3 前瞻长期效果证据。官网引用的外部目标设定元分析只支持一般方法研究，不能外推为 ARDA 的真实效果。

OPEN-01：App Store 正式发布和实际版本仍未由匹配开发者的商店页面确认；TestFlight 和 2026-09 目标日期可能滞后。
OPEN-02：11 领域评分的数学公式、证据权重、误差模型、信度效度与外测未知。
OPEN-03：已接受证据与 AI 推断隔离、健康数据本地处理、撤销授权和删除传播均缺乏独立行为复验。
OPEN-04：用户对评分算法的质疑是否能触发可解释的计算修正，未知。
OPEN-05：厂商当前产品价格、服务可用国家和商业持续性未知。

## 4. E 当日治理与 F 本周专题状态

E：research/operations/E001_READONLY_PROJECT_AUDIT_2026-10-24.md 已记录 2026-10-24 的完整限定只读审计，本轮避免重复。GitHub 最近 R119 及 original239 v6.9 的提交消息记录待审队列推进至 164，相关提交为 03ae1786bffde9f99b69732a3088f3fbe420b344、de699b8737cc55c3a266f086428f7041fd63b268、c6a36350310aad8cd22f18fd9fbc35482f0c368f。此处为提交元数据核查，尚未独立重跑 R119、重验 v6.9 全部队列或直接查询对应 CI jobs，故其科研验收与 CI 结果仅列 PENDING_INDEPENDENT_RECHECK。根 README 旧导航问题仍见于 E001，不擅自修改。
F：research/privacy_safety/F001_HUMAN_OVERRIDE_AND_DATA_MINIMIZATION_2026-W43.md 已完成本周专题，避免重复。ARDA 的“删除会话与删除已接受证据分离”“本地健康记录与粘贴内容不同路径”进入 F002 候选案例；F002 尚未执行。独立 E 每日和 F 每周自动调度创建在本轮尝试时返回不可用；现有每小时商业研究自动任务仍包含 E/F 日历检查要求。没有声称建立了独立调度。
主线：先全部 R 系列，再统一归纳分类，最后模型熔炼；本轮不更改任何冻结协议或人生效用权重。

## 5. 执行与费用

work_performed: 实际读取 ARDA 官网、FAQ、信任页、隐私政策、隐私选择页，有限搜索 App Store 发布状态，并核对既有 market/E/F 归档和近期 R/理论提交。
evidence_scope: MARKET-E1 厂商文档；发布状态有限搜索未确认；E/F 为既有归档只读核对。
output_paths: research/market/MKT004_ARDA_ACCEPTED_EVIDENCE_LOCAL_HEALTH_RELEASE_CHECK_2026-10-24.md。
ci_status: NOT_RUN；billing_checked: 本轮无新增购买、订阅、注册、计费 API、云算力或 CI 操作，新增操作费用为零；未审查 GitHub 账户账单和免费额度。
blockers: 正式发布链接、真实产品测试、评分数学细节、独立数据安全验证均缺失；E/F 独立定时任务创建不可用。
next_action: MKT005 优先审读 Dcider 的价值权重与决策评分证据结构，核查其公开产品实际状态及隐私权限；若缺乏技术细节，转向公开开源决策工具作可复算方法比较。

## 6. 公开来源（均为英文，2026-10-24 访问）

S1 ARDA Support / FAQ: https://www.ardaapp.com/support
S2 ARDA Home: https://www.ardaapp.com/
S3 ARDA Privacy Policy（页面标记 2026-09-07 更新）: https://www.ardaapp.com/privacy
S4 ARDA Privacy Choices: https://www.ardaapp.com/privacy-choices
S5 ARDA Trust: https://www.ardaapp.com/trust
S6 Apple App Store “Life Audit AI” by Sarah Tomor，独立不同开发者，不能误认 ARDA: https://apps.apple.com/us/app/life-audit-ai/id6766145432
