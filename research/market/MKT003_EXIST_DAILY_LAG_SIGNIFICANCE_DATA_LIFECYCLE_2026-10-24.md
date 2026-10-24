# MKT003 Exist 每日属性、跨日相关、显著性与数据生命周期审读

研究日期：2026-10-24（Asia/Shanghai）；轨道：commercial_market；状态：COMPLETE_BOUNDED_DOCUMENT_REVIEW。
observed_main_head_before_write: 1155a35520fc743f9ea7245603dfdb93df514ceb
preflight: 已读取商业基线、MKT001、MKT002、E001、F001；目标路径在写入前 GitHub fetch_file 返回 NOT_FOUND。E 当日、F 当周均已有实质归档，避免重复生成。无个人 Exist 账户或 API 令牌。

## 1. 本轮新增的具体机制（非新发布消息）

1. **日级统一属性模型及缺失编码**。官方 API 对象定义：属性以用户当地日期为单位，没有小时或分钟粒度；缺失日返回 `null` 而非删除行；日期依用户时区，原始数值采用公制。手动属性有量、时长、比例、等级等类型。官方手工跟踪说明对特定可计数类型未记录的日子填零，其他类型保持缺失。两种缺失含义不可混淆。来源 S1/S2，MARKET-E1。
2. **观察窗与跨日搜索**。官方知识库规定至少三周有数据的日期，N/A 日不计入；每周一更新相关性。官方明确同日未发现相关时，继续检查连续两天的相关，示例为今日饮酒与次日睡眠、今日运动与次日情绪。API `offset` 字段可见，文档实例含 0 与 -1；具体符号与时间方向应依据正式接口语义再核查，不能仅凭示例推断完整实现。来源 S3/S4/S5，MARKET-E1。
3. **相关性数值与显著性元数据**。API 返回 `period`、`offset`、`value`、`p`、`stars`、`strength_description`、`stars_description` 等字段，可按强度和五星置信度过滤；开发者文档称 `p<0.05` 一般视为显著，五星对应更小 p 值。官方没有在已读页面说明其多重比较控制、时间自相关修正、置信区间、缺失机制建模、完整的检验族定义或模型外预测验证，均记为 UNKNOWN，禁止推断未采用。来源 S5/S6/S7，MARKET-E1。
4. **用户反馈及解释**。相关性可显示人类可读语句、强度与星级；2019 年官方功能说明支持用户将相关结果评价为有用或无用并隐藏不想看到的相关。此为展示反馈，不足以证明后台统计参数随反馈自动学习。来源 S8，MARKET-E1。
5. **数据来源与权限**。同一属性一次由一个来源服务更新，用户可切换来源；OAuth 以组级读写 scope 控制。断开数据服务后，官网 FAQ 明确既有数据仍保留；账户关闭才声明删除 Exist 数据副本，同时保留必要的支付记录与支持邮件。提供 PDF、CSV 和 JSON 导出；2026-04-23 官方更新说明 PDF 可按一或两个属性生成报告，CSV 最多五属性、可选时间段。来源 S9/S10/S11/S12，MARKET-E1 厂商文档，未独立验证实际删除传播。
6. **商业模式**。官网公开个人订阅 6.99 美元/月或 62.90 美元/年，30 天试用；账户创建页面需要支付卡资料。仅记录公开价格，没有注册、试用、付款或调用认证 API。来源 S13，MARKET-E0/E1。

## 2. 科学方法风险及可迁移设计

R1 多重搜索风险：同日和次日、多个属性对、每周反复筛选可扩大候选假设集合。p 值与五星在未核对检验族、校正和序贯选择规则前，不应等同已控制全局假阳性。NIST 统计手册指出自相关会破坏常用独立样本检验假设；statsmodels 官方文档提供 Benjamini–Hochberg 和 Benjamini–Yekutieli 等 FDR 方法作为未来候选工具，但本轮没有证据说明 Exist 是否使用它们。来源 S14/S15，方法文档，与 Exist 实际实现区分。
R2 时间对齐风险：本地日期、时区迁移、延迟同步、`null` 与“未记录视作零”会改变配对有效样本和滞后解释。应分别记录数据来源、日期边界、观测时点、缺失原因、实际配对样本量。
R3 因果与外推风险：Exist 明确提醒相关性不表示因果。跨日先后顺序本身仍不足以排除共同原因；不能将关系强度当成干预收益，也不能从一个人的相关性直接推断群体规律。
R4 授权撤销与删除差异：断开来源仅阻止后续同步，厂商明确说明既有数据保留。未来候选设计应区分断开连接、撤销权限、删除原始数据、删除衍生数据、删除备份及导出副本，不能声称所有环节均可即时彻底删除。
R5 数据安全：官方 scope 和账户删除说明仅能证明有相应产品流程，未经第三方安全评估、渗透测试或数据删除实验，不能视为实现有效性证据。

## 3. 候选研究设计（仅知识储备）

MKT003-H1：未来个人量化状态层以“本地日期、数值、单位、数据源、采样时间、缺失原因、权限版本”作为候选字段，避免将未记录强制视为零。
MKT003-H2：未来在合成日级序列上预冻结假设族，比较原始相关、考虑时间自相关的检验、FDR 调整和独立未来时段外测；报告每种方法的误报与预测校准。
MKT003-H3：将同日关联与跨日关联分别标注为描述性发现；仅在满足独立预测、因果识别条件后再进入干预建议候选池。
MKT003-H4：数据权限与删除控制未来应按来源、属性、原始值、衍生统计、日志及备份分别登记；不得自动连接真实健康、财务或关系数据。

以上未被采纳为 R 系列模型改动，不构成用户决策系统实现，也未证明 Exist 能改善长期人生结果。

## 4. E、F 日历状态与跨轨风险

E：2026-10-24 已有 E001 只读审计；本轮仅查看增量。原始239项 v6.7 R117 收据提交 9e004eef24d7361390ffa66f61b24aaa777f8847 报告 provisional_pending=166，new_E2=0，new_E3=0，CI run 40075430741 为收据中的 success 声明；本轮读取了收据的 GitHub commit diff，**没有直接查询该 CI 的 jobs**，所以将 CI 结果标记 RECEIPT_CLAIM_NOT_INDEPENDENTLY_RECHECKED。本轮不修改 R 索引或其他轨成果。TH006 提交 1155a35520fc743f9ea7245603dfdb93df514ceb 为有限理论笔记。E001 的根 README 导航滞后问题仍待所有者研究轨处理。
F：2026-W43 已有 F001 人工否决、解释与最小采集专题；本轮不重复。下周 F002 优先研究本地优先、撤销授权、衍生数据删除；本轮 Exist 的“断开来源仍保留既有数据”作为候选案例进入 F 待审池，尚未完成 F002。
调度：既有每小时商业任务包含 E 日、F 周检查。独立 E 日和 F 周自动任务的创建本轮均返回不可用，**未声称已独立创建**。

## 5. 费用、验证与下一轮

只使用免费公开英文官网、技术文档和 NIST/statsmodels 方法资料。无新订阅、购买、注册、计费 API、云算力、CI 或敏感个人数据接入。新增操作费用 0；GitHub 账户总账单和免费权益余额未独立核对。CI: NOT_RUN。提交仅归档公开文档分析，非产品实测或科学 E2/E3。
下一轮：优先核实 ARDA 真实发布/上架状态与版本来源，若证据不足则转向 Dcider 的价值权重、解释与反馈数据结构，记录哪些属于营销声明、哪些有接口或开发文档。

## 6. 公开原始来源（2026-10-24 访问，均非中文）

S1 https://developer.exist.io/reference/object_types/
S2 https://exist.io/page/help-manual-tracking/
S3 https://kb.exist.io/article/18-how-long-does-it-take-to-find-correlations
S4 https://kb.exist.io/article/55-will-exist-find-correlations-across-multiple-days
S5 https://developer.exist.io/reference/correlations/
S6 https://developer.exist.io/reference/object_types/
S7 https://kb.exist.io/article/37-what-are-correlations
S8 https://exist.io/blog/new-ios-correlations/
S9 https://kb.exist.io/article/119-how-can-i-check-which-service-is-updating-an-attribute
S10 https://developer.exist.io/reference/authentication/oauth2/
S11 https://exist.io/page/faqs/
S12 https://exist.io/blog/pdf-export/
S13 https://exist.io/about/values/
S14 https://www.itl.nist.gov/div898/handbook/eda/section2/eda251.htm
S15 https://www.statsmodels.org/dev/generated/statsmodels.stats.multitest.fdrcorrection.html
