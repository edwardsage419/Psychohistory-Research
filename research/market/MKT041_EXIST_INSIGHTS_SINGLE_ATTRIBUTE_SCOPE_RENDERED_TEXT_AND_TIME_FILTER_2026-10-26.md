# MKT041 Exist Insights 自动洞察的单属性授权、渲染内容和时间语义审计

run_date: 2026-10-26 Asia/Singapore
track: commercial_market
status: COMPLETE_BOUNDED_OFFICIAL_DOC_VENDOR_SURVEY_SYNTHETIC_CHECK
preflight_main_head: 6982ee5257cc7bc4d7a8a15c77e61f3a1a89e2c9
prior: MKT003 MKT025 MKT026 MKT040 E009 F002
evidence: MARKET_E1_OFFICIAL_API_DOCUMENT + MARKET_E0_VENDOR_SELF_REPORTED_SURVEY + E1_SYNTHETIC_PREDICATE
authenticated_execution: NONE
new_E2: 0
new_E3: 0
remote_CI: NOT_TRIGGERED
active_new_spend: ZERO; overall billing and free quota NOT_INDEPENDENTLY_VERIFIED
source_language: English only

## 1. 去重与新增问题

MKT003 研究日级属性、相关性与缺失，MKT025/026 研究 OAuth 属性组和来源，MKT040 研究双属性相关性 combo 的“至少一侧有 read scope”文档条件。本轮转向 **Insights 自动生成的单属性派生事件**，直接审读官方 API v2 的对象结构、权限表述、日期筛选、呈现内容，并增加 2026-02-05 发布的厂商 2025 用户调查作为市场观察。API 重大更新日志可见 2022-08-18 API v2 上线，不声称本轮发现新发布功能。

## 2. 官方技术文档可支持的机制

**输入与状态**：Exist 汇总第三方同步及手动日级属性；缺失可表示为 null。Insights 对符合特定 insight type 条件的属性值自动生成事件。官方将事件分为当天、日、周、月，priority 1 至 4。示例返回 created（带时区时间戳）、target_date（可有具体日期）、type.name、type.period、type.priority、type.attribute.name/label/group/value_type，以及 html 和 text 两种渲染内容。文档称 target_date 仅在洞察与特定日期有关时出现。

**读取权限**：GET /api/2/insights/ 返回经认证用户的分页列表，官方明确“Results are limited to your read scopes”。样例中 type.attribute 只有一个属性和一个 group。与 MKT040 的两属性 combo “至少一侧 read scope”文字不同，Insights 页面没有说明对隐藏属性的跨组派生推断规则。不能从单属性嵌套结构推断实际洞察文本绝不引用其他属性，也不能宣布存在越权披露。

**查询和时间语义**：支持 limit 最大 100、page、date_min、date_max、priority。官方称 date_min/date_max 筛选结果日期，未在已读页面明确采用 created 的日期、target_date，还是其他事件日期。created 是生成时间，target_date 是被描述事件时间，二者可能不同；无 target_date 的周期事件应如何筛选亦未在已读参考中细分。这些是未来独立回放的候选审计问题，实际服务端行为 UNKNOWN。

**解释与反馈**：html 是带格式的呈现片段，text 是纯文本；例子为睡眠长短及星期几的比较语句。生成条件的完整算法、样本量门槛、异常值处理、缺失机制、置信区间、洞察选择偏差、错误更正与历史回填规则均未在本轮所读页面给出。无正式概率预测字段、预测校准或事后干预结果标签。HTML 的转义与客户端渲染需要审计，但目前没有证据证明脚本注入漏洞。该机制是规则/条件驱动的官方描述，不能等同生成式 AI 自主推理。

**费用**：官网个人订阅公开 $6.99/月或 $62.90/年，30 天试用；未购买、注册或使用认证 API。

## 3. 市场新增资料：2025 调查于 2026-02-05 发布

Exist 厂商博客报告，在参与其 2025 用户调查的受访者中，48% 将“寻求洞察以理解或改变行为”列为使用目的；35% 希望更多数据分析；32% 希望 2026 优先增加长期数据分析；46% 对 Exist 不添加生成式 AI 功能表示高兴；厂商称不计划加入生成式 AI 功能。此为 **厂商自报用户调查 MARKET_E0**，页面未给出本轮可核实的抽样框、响应率及完整样本量，不能外推所有用户或证明长期决策效果。厂商路线声明不保证未来永不改变。

该资料对未来方法的有限启示：个人数据洞察产品存在对长期分析的自报需求，也存在明确不希望接入生成式 AI 的受访者；未来研究应并列考虑可解释规则型分析和 AI 辅助分析，不能预设唯一产品架构。

## 4. 独立合成检查

用 Python 标准库构造三个纯人工 Insight 对象：sleep 当日、mood 当日、sleep 无 target_date 周期项；在四种 scope 集合（空、仅 sleep、仅 mood、两者）下测试单属性组过滤，另测试 created 与 target_date 区别、可选日期、html/text 不同表现以及无结果成功字段。实际执行 **23 assertions，23 PASS，0 FAIL**。这是自行定义的过滤谓词和人工结构测试；没有调用 Exist API，不能证明其服务端权限正确、过滤日期含义、HTML 安全或真实用户收益。

## 5. 候选风险和控制，仅供未来研究

MKT041-R1 MEDIUM OPEN：当洞察自动生成后撤销原始属性 scope，旧派生文本、缓存、客户端导出是否同步失效尚未验证；参考 F002 生命周期问题。
MKT041-R2 MEDIUM OPEN：created 与 target_date 混淆会改变时间窗、事后回填和泄漏防护；需要分开保存生成时间、事件时间和用户时区。
MKT041-R3 MEDIUM OPEN：html 和 text 双表示可能存在不同的转义、显示和历史重建行为；目前没有安全事故或注入复现证据。
MKT041-R4 HIGH OPEN：规则型洞察的“惊讶”“通常”等语言未附可独立验证的置信区间和样本量；不能作为因果结论、预先预测成功或个人效用权重。
MKT041-R5 MEDIUM OPEN：厂商自报调查的样本代表性和行为效果未知；不可将受访者比例当成市场总体参数。

候选方法 C1：每条派生洞察记录 attribute/group、来源版本、授权版本、created、target_date、周期、算法/模板版本和失效原因。
候选方法 C2：把描述性提醒、概率预测、干预建议、结果标签分开存储与评分；未来需冻结训练/测试时间边界及缺失处理。
候选方法 C3：优先使用文本安全呈现和本地处理；HTML 渲染和撤销传播需要合成测试，暂不实现个人决策产品。
候选方法 C4：将规则型解释和生成式 AI 解释并列为候选知识，不预设唯一架构或人生效用权重。

## 6. E/F、归档与下一项

E：本日已有 E004 正式日检和 E009 增量。此次对新 R171 的独立收据、冻结输入与 CI 作增量只读核对，单独记于 E010。R170 全状态跨语言比较缺口及 R136 历史失败保持开放。
F：2026-W44 的 F002 已完成授权撤销、衍生数据、缓存和备份专题；本轮只增加 Insight 派生文本权限候选案例，不重复创建 F003，不接入真实敏感数据。
GitHub：仅新建本文件，写入前核对 HEAD、文件不存在及并发目录；成功提交后应远端回读和 SHA 核验。无付费产品、论文、云资源、API、CI、新订阅或个人数据接入；账户整体账单未知。

下一项 MKT042：深读 Exist averages 官方文档中 60 天历史窗口、按星期分组和名为“average”但实际为 median 的规则；用人工数据对比均值与中位数对个人基准线、离群点及偏离控制的影响，严禁把统计基准线视为人生最优策略。

## 7. 非中文原始来源

1. https://developer.exist.io/reference/insights/
2. https://developer.exist.io/reference/object_types/
3. https://developer.exist.io/reference/authentication/oauth2/
4. https://developer.exist.io/reference/correlations/
5. https://developer.exist.io/reference/changelog/
6. https://exist.io/blog/exist-survey-2025/ (published 2026-02-05; vendor self-reported survey)
7. https://exist.io/ (public pricing)
8. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/market/MKT040_EXIST_CORRELATION_COMBO_SINGLE_SCOPE_DERIVED_DISCLOSURE_2026-10-26.md
9. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/privacy_safety/F002_CONSENT_REVOCATION_DERIVED_DATA_BACKUP_LIFECYCLE_2026-W44.md
