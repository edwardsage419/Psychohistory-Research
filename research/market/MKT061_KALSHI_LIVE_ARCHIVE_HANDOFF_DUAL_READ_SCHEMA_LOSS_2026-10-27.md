# MKT061 Kalshi实时与历史分层迁移的双读一致性、结算字段损失及分页边界

日期：2026-10-27（Asia/Singapore）。研究轨：market。状态：COMPLETE_BOUNDED_OFFICIAL_DOC_SYNTHETIC_E1。主动新增费用：0。研究起点main HEAD：4a5550e3372b96ca3107fa50d5c7abf09f2efd50。

## 1. 去重与一手资料

MKT058至MKT060已经研究Manifold撤销审计、答案级权限和交易时间戳并列游标。本轮转向另一产品Kalshi，聚焦其官方明确描述的实时数据与历史档案迁移，避免再次复述Manifold时间戳并列问题。

2026-10-27实际查阅的英文官方资料：

1. Kalshi Historical Data：https://docs.kalshi.com/getting_started/historical_data
2. Kalshi Understanding Pagination：https://docs.kalshi.com/getting_started/pagination
3. Kalshi Get Trades：https://docs.kalshi.com/api-reference/market/get-trades
4. Kalshi Get Market Candlesticks：https://docs.kalshi.com/api-reference/market/get-market-candlesticks
5. Kalshi Rate Limits and Tiers：https://docs.kalshi.com/getting_started/rate_limits

资料级别为OFFICIAL_DOCUMENTATION。没有访问Kalshi交易API、创建账户、交易、支付、请求私人资料或执行线上端到端测试。官网描述不能自动证明生产系统每次迁移都符合其文档。

## 2. 真实新增机制及证据边界

MKT061-F1 分类型时间切分。官方Historical Data说明live与historical为不同数据分区，GET /historical/cutoff给出market_settled_ts、trades_created_ts、orders_updated_ts、market_positions_last_updated_ts。市场按结算时间、交易按成交时间、订单按完成或取消更新时间、持仓按最后更新时间处理。不能将单一cutoff推广到所有对象。历史市场及K线、历史成交、历史订单与历史持仓各有独立读取路径。官方还明确部分已结算持仓在迁移缓冲期继续停留于live，持仓cutoff仅为backfill horizon。

MKT061-F2 两次查询不构成一个事务快照。官方明确建议持仓先分页读取GET /portfolio/positions?settlement_status=all&subaccount=<number>，再读取GET /historical/positions?subaccount=<number>；两次读取之间可能发生归档，存在重叠与缺失风险。文档要求以subaccount+ticker去重，并在精确完整性重要时于迁移边界重复对账。仅查询默认subaccount=0会遗漏其他子账户。整事件缓冲迁移使“已超过cutoff”不能推断“已在historical可见”。

MKT061-F3 不同读取次序的边界。人工模型中某持仓P在t0位于live，t1完成迁移。若先读historical于t0得到空，再读live于t1也得到空，P被漏掉。按官方推荐先读live于t0得到P，再读historical于t1又得到P，简单拼接会重复；按(subaccount,ticker)去重后为一条。该模型仅说明两阶段非快照读取的逻辑边界，不能据此推断线上实际漏失频率、内部原子性或事务隔离实现。

MKT061-F4 结算字段不可对称恢复。官方明确GET /portfolio/settlements只返回仍在live的已结算持仓；迁入历史后GET /historical/positions可提供持仓、已实现盈亏与费用，但目前没有同等结算记录字段的历史端点。由此，事后重建完整结算事件时，某些live-only字段可能无法仅凭historical positions恢复。缺失字段的逐项列表尚未审计，不能推断具体哪一项永久消失。

MKT061-F5 分页契约与行情汇总层不同。Get Trades文档提供trade_id、ticker、created_time、价格、数量、taker side及游标，默认100条、上限1000条；官方分页指南提示页面之间数据可能改变，建议刷新。该游标为服务端返回token，其内部稳定排序及并列时间处理未见本轮源码证据，不能声称其已经解决Manifold MKT060的时间戳并列遗漏。K线为1/60/1440分钟的汇总价格和成交量，不能从OHLC恢复逐笔成交的完整事件顺序。历史结算市场的K线需改读historical路由。

## 3. 15项人工分层迁移检查

使用纯JavaScript内存数组与对象，未调用任何Kalshi接口，构造单持仓跨分区、重叠、不同子账户、不同ticker及多种cutoff。执行15项断言，15通过、0失败。

覆盖：稳定live、稳定archive、historical先读后迁移的漏读、live先读后迁移的重复、按复合键去重、只读live漏掉旧记录、只读historical漏掉新记录、重叠期重复、不同subaccount必须保留、不同ticker必须保留、相同复合键合并、市场与交易cutoff不同、持仓与市场cutoff不同、超过持仓cutoff仍可能留在live，以及读取顺序的非等价性。

该测试验证人工状态模型的逻辑，不能作为Kalshi线上系统故障测试、真实数据完整性证明或独立第三方验证。未测试HTTP分页、数据库事务、账户权限、接口费率及真实K线精度。

## 4. 面向心理史学的候选方法映射

真实输入候选：预测对象ID、事件或交易ID、目标、时间戳、来源数据分区、游标、数据版本、子账户或身份域、权限状态。Kalshi本身提供市场成交和结算资料，市场交易价格并不等于经过校准的个人主观预测概率，不能直接用其衡量人生决策质量。

状态表达候选：LIVE、ARCHIVE_PENDING、ARCHIVED、OVERLAP、UNKNOWN，分别记录采集时间与来源路径。完整事件账本、汇总图表、评分快照、结算更正历史使用独立契约。

算法候选：按数据类型分别读取cutoff；多页记录游标与采集窗口；跨live/historical用稳定复合身份去重并保留来源；临近迁移执行重读对账；缺字段标注UNAVAILABLE而不自动补造。未获得一致快照时只给出“按某次采集可见”的结果。

目标与反馈：完整率、重复率、缺字段率、迁移边界再对账差异和重放可确定性；检测到异常时提示重新采集或人工审核，不能以市场产品销售效果作为科研效应。

隐私与权限：公开成交资料、个人账户持仓和个人决策日志分离。个人持仓端点属于用户范围，未经授权不访问；未来的本地最小采集、可撤销授权及外部复制状态参考F002候选控制。任何真实用户敏感数据均未接入。

解释性：展示记录ID、采集时间、live/historical来源、cutoff版本、是否为K线汇总、去重键及仍缺失的结算字段。

费用与可验证性：仅阅读英文公开官网文档并运行免费隔离内存测试，新增费用0。官方rate limits中的tokens是请求速率配额单位，不能直接视为美元计费；本轮未核验注册条件、商业许可和真实账户账单，禁止因此宣称可无限免费使用API。后续如需调用API，须先独立确认无收费且用户已授权；本阶段优先继续文档与本地合成研究。

## 5. 证据等级、风险与下一项

MARKET E1 = 官方产品技术文档 + 人工分层迁移逻辑验证。源码执行：NO。真实API或数据库测试：NO。线上故障或发生率：NOT_VERIFIED。对个人长期决策质量的因果改善：NOT_VERIFIED。

候选风险MKT061-R1 HIGH：分层迁移期间两次读取非同一快照，存在逻辑上的重复与遗漏风险。
候选风险MKT061-R2 HIGH：历史持仓接口缺少与live结算事件完全同等的字段契约，事后重建有未知缺口。
候选风险MKT061-R3 MEDIUM：跨对象复用单一cutoff、遗漏其他subaccount、用K线代替逐笔事件导致完整性误判。
候选风险MKT061-R4 MEDIUM：把服务端游标存在性误当作全量一致快照或确定性并列时间排序的证明。

与MKT060比较：Manifold固定源码揭示单时间键游标可能漏掉并列时间记录；Kalshi官方文档明确采用服务端游标并承认live/archive非快照迁移，当前证据尚不能比较两者真实漏失率或宣称某方完全可靠。

E轨2026-10-27日检E028已完成，本轮增量治理优先R195新增ESS第三方法。F轨2026-W44 F002已完成，故不重复建立F003。市场发现保留为F未来安全主题候选，R系列优先完成、再系统归纳、最后熔炼；不改变任何冻结协议或人生效用权重。

下一项MKT062：核对另一免费开源事件账本的快照标识与双读对账实现，优先寻找可运行的免费测试与可复核源码；若未找到，继续Kalshi结算字段契约的官方版本差异审计。
