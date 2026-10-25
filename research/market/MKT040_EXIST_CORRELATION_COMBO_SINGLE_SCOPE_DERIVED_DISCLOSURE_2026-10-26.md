# MKT040 Exist 相关性组合查询的单侧读取权限与派生统计可见性

run_date: 2026-10-26 Asia/Singapore
track: commercial_market
subflow: product
status: COMPLETE_BOUNDED_OFFICIAL_API_DOCUMENT_REVIEW_AND_SYNTHETIC_POLICY_CHECK
observed_main_head_before_write: a57e8b092ece6af8c4028722f0851c7b70f44433
prior: MKT003, MKT025, MKT026, MKT039; F002, E008
evidence: MARKET_E1_OFFICIAL_API_DOCUMENTATION + INDEPENDENT_SYNTHETIC_PREDICATE_E1
authenticated_API_execution: NONE
actual_unauthorized_disclosure_verified: NO
remote_ci: NOT_TRIGGERED
active_new_cost: ZERO; account billing and free quota NOT_INDEPENDENTLY_VERIFIED
source_language: English only

## 1. 去重与新增问题

MKT003 已审查日级属性、同日和跨日相关、p 值、星级与缺失；MKT025/026 已审查 OAuth scope、属性所有权、inactive 和分页。此次新增问题是**相关性作为两种属性共同生成的派生统计，其访问条件是否与两个原始属性的读取权限一致**。这是一项既有 API v2 的机制深读；官方 changelog 可见最新 API 重大记录为 2022-08-18，不宣称产品本周新增功能。

## 2. 官方文档的两种权限表达

Exist OAuth2 官方参考将 activity_read、mood_read、sleep_read、health_read、finance_read 等分别授权，称 read scope 允许取得匹配组的属性和值。普通属性端点在缺乏对应 scope 时返回空结果。

相关性 API 参考提供两种接口：
* GET /api/2/correlations/：最近一周生成的相关性分页列表，受 read scopes 限制，支持 strong=1、confident=1、attribute、page 和 limit<=100。此处未明确规定涉及两个属性时采用 AND 或 OR。
* GET /api/2/correlations/combo/?attribute=A&attribute2=B：官方原文规定，只有“至少一个属性”属于调用者 read scopes 时才返回结果。参数顺序任意；不存在对应相关性时可返回 HTTP 404。该文字是必要条件说明，不保证满足条件必然得到结果。
* combo 示例返回 date、period、offset、attribute、attribute2、value、p、percentage、stars、可读解释句、rating 等字段。rating 是用户对相关性有用性的主观评价，不能等同预测模型得到真实结果反馈。

两种接口的权限文字没有完整说明派生统计对未授权属性的脱敏范围。尤其是 combo 的“至少一个”条件，和原始属性值读取的逐组 scope 有不同粒度。若服务端按字面执行且返回完整示例对象，单侧 scope 客户端可能看到另一属性的名称、关系方向、统计强度、显著性及用户主观评价。**这是文档推导的候选派生信息披露边界，未验证真实服务器行为，不能宣布安全漏洞。** 返回相关性不等于读取另一属性逐日原始值。

## 3. 可复算合成权限矩阵

只使用 JavaScript 原生布尔逻辑，不调用 Exist 服务。对两个属性 A/B 的 read scope 共四种组合，比较文档中的 any-of 最低条件 (A OR B) 与更严格的双侧条件 (A AND B)。

| A read | B read | 通过文档最低条件 | 双侧读取均授权 |
| --- | --- | --- | --- |
| 0 | 0 | 0 | 0 |
| 0 | 1 | 1 | 0 |
| 1 | 0 | 1 | 0 |
| 1 | 1 | 1 | 1 |

执行 14 项独立布尔断言，14 PASS、0 FAIL。四种情景中两种出现 OR=true 且 AND=false。结果只证明两种授权谓词的逻辑差异，不证明 Exist 的真实 HTTP 响应、数据内容或权限安全性质。

## 4. 输入、状态、算法、目标、反馈、权限、费用和局限

输入：来自授权第三方或手工记录的日级属性，带日期、来源、类型、缺失。状态：用户时区、属性组、read/write scope、owner、相关性对、offset、period、value、p、stars、rating。算法：官方文档说明每周周日生成相关性，最多一年历史，支持同日和跨日；未公开本轮所需的完整统计实现、多重检验控制、时间自相关修正或内部源代码。目标：个人描述性观察、相关性提示和习惯理解。反馈：rating 可表达主观有用性，未证明自动重新训练统计模型。解释：自然语言相关性说明、强度、p 与星级；不保证因果或未来校准。隐私：OAuth 分组读取、combo 的单侧最低条件，原始值和派生统计应分开审计。费用：官方公开个人 $6.99/月或 $62.90/年、30 天试用，未注册或购买。可验证性：官方文档 E1；合成逻辑 E1；真实产品跨 scope 实测=0；真人长期决策改善 E2=0；历史预测 E3=0。

## 5. 候选方法与风险

MKT040-R1 HIGH OPEN：两属性派生结果可能揭示未授权组的属性名称、关系方向或主观 rating；未来需经授权的人工测试账户逐项验证权限组合、返回字段和缓存，当前无测试授权和免费保障，保持 UNKNOWN。
MKT040-R2 MEDIUM OPEN：/correlations/ 与 /combo/ 的权限粒度是否一致尚不明确；不得从“受 scopes 限制”推断双侧 AND，也不得从 combo 文档推断真实跨组泄漏。
MKT040-R3 MEDIUM OPEN：404 可能由未生成相关性、筛选或权限边界造成；没有官方错误类型细分证据，不应据此推断未授权属性是否存在。
MKT040-R4 MEDIUM OPEN：相关性对象的 rating 是主观有用性反馈，不能作为客观干预成功标签；统计显著性和星级亦不能当作预测校准或因果收益。

候选设计 C1：原始属性读取权与跨属性派生统计访问权分别建模；每个派生对象保留两个来源 scope、生成时权限版本和撤销依赖。
候选设计 C2：明确文档化 ANY、ALL、REDACTED、DENY 四种可能策略，并用合成权限矩阵检查，选择权留给未来研究和用户，不提前实施。
候选设计 C3：任何可能跨敏感组的派生解释、自然语言句子、图表及缓存均纳入数据生命周期和来源撤销风险清单。
候选设计 C4：长期预测研究需要预先冻结相关性搜索族、时间分割、缺失机制与独立预测评分，保持 R 系列主线优先。

## 6. E/F 本轮状态及阻塞

E：E004 今日正式日检、E005 至 E008 增量已存在。本轮另核查 R170 预冻结提交、R/B 执行及公开真人数据来源；详见独立 E009 只读增量报告。不触碰 R/A/B/TH/C/D 或共享索引。
F：2026-W44 F002 已完成撤权与衍生数据生命周期专题，不重复创建。本轮将双属性派生统计的授权语义作为未来 F003 候选案例，不接入真实敏感数据。
阻塞：无 Exist 账户、令牌、认证测试许可或无需付费的服务端复验；因此仅报告官方 API 文字与合成谓词。未调用付费 API、购买产品、启用 CI 或增加订阅。

## 7. 非中文原始来源

1. https://developer.exist.io/reference/correlations/
2. https://developer.exist.io/reference/authentication/oauth2/
3. https://developer.exist.io/reference/object_types/
4. https://developer.exist.io/guide/read_client/
5. https://developer.exist.io/reference/changelog/
6. https://exist.io/
7. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/market/MKT003_EXIST_DAILY_LAG_SIGNIFICANCE_DATA_LIFECYCLE_2026-10-24.md
8. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/market/MKT026_EXIST_SCOPE_OWNERSHIP_INACTIVE_VISIBILITY_STATE_AUDIT_2026-10-25.md
