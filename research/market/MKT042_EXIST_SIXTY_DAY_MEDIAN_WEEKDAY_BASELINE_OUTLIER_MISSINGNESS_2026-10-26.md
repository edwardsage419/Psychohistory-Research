# MKT042 Exist 60天中位数与星期基准线的离群值、缺失及偏离判读审计

run_date: 2026-10-26 Asia/Singapore
track: commercial_market
status: COMPLETE_BOUNDED_OFFICIAL_DOCUMENT_AND_SYNTHETIC_RECOMPUTATION
preflight_main_head: 9db74f35b200d0d824432ee6c00195ed39b6dcd6
dedup: MKT003 MKT025 MKT026 MKT040 MKT041 E010 F002
evidence: MARKET_E1_OFFICIAL_DOCUMENT + E1_INDEPENDENT_SYNTHETIC_ARITHMETIC; vendor pricing and product promises MARKET_E0
authenticated_product_execution: NONE
new_human_E2: 0
new_historical_E3: 0
remote_CI: NOT_RUN
active_new_spend: ZERO; account-wide billing and free quota NOT_INDEPENDENTLY_VERIFIED
source_language: English only

## 1. 新增机制和原始资料边界

本轮从 MKT041 的 Insights 转向 Exist 官方 v2 Averages 和 object types 文档。该资料没有证据表明是2026年新上线功能，故作为既有产品机制深读。官方明确：名为 averages 的数值实际按 **median 中位数** 计算，基于**最近60天数据**，**每周生成一次**，保存 overall 和 monday 至 sunday 七个星期分组的基准值。官方要求客户端面向用户继续称 average。历史记录可由 GET /api/2/averages/ 的 include_historical=true 与 attributes 参数读取，结果受 read scopes 限制。

真实输入模型：来自手动录入或第三方同步的日级数值属性，缺失日的属性值可为 null；用户当地日期是记录粒度。状态表达：attribute、基准生成 date、overall 及星期七值，支持按周历史快照。反馈：客户端可把当日值相对相应星期中位数绘制进度条，并按周更新通常行为参照；历史快照可绘制趋势。当前所读官方文档没有提供完整缺失日排除/补值算法、星期样本不足时回退、偶数样本中位数约定、0分母处理、历史回填是否重算旧快照、异常值剔除、置信区间或因果反馈学习规则。不能从“每周更新”推断产品自主优化人生目标。

官方文档展示 Averages API 的 page、limit、date_min、date_max、groups、attributes、include_historical 查询参数。结果限制于调用者 read scopes。官方产品支持个人手动及第三方数据、历史图表和相关性洞察，服务端授权及真实历史数据处理未在本轮实测。

## 2. 独立合成实验，Python 3 标准库

只用人工数列、datetime 与 statistics，实际执行17项断言，17 PASS，0 FAIL。数据均为人工示例，与 Exist 用户和服务器无关。

A 离群点：60个观测值为59个7及1个1000。算术均值23.55，中位数7。假设某天观测20、仅以观测/基准作示意性比值，则 20/23.55=0.849257，20/7=2.857143。两个参照对“是否高于通常水平”的判断相反。此比值是本轮人工计算，不声称是 Exist 内部进度条公式。

B 星期分层：2026-08-28至2026-10-26共60天，其中9个星期一。除星期一均为7，星期一通常为4，仅2026-08-31为80。overall 中位数7、overall 均值7.816667；星期一中位数4、星期一均值12.444444。对当天值20，星期一中位数参照比值5，整体中位数参照比值2.857143。星期分层影响偏离量的解释。只有9个星期一样本，稳定性需要额外验证。

C 缺失偏差：60个潜在观测值，前30天4，后30天10。完整数据中位数7。假设后30天中的5个高值未记录且仅使用其余55个非缺失值，中位数变为4。该人工缺失机制可使基准明显下降；不能据此断言 Exist 采用相同缺失处理。

D 状态迁移：前30天4，后30天10。60天中位数7，最近30天中位数10。滚动基准可能滞后于已经改变的行为水平。每周快照也意味着相邻两次更新之间的基准陈旧，具体更新时间以产品实现为准。

E 窗口退出：60天包含59个7和1个1000时，均值23.55、中位数7；该异常值退出窗口且新进入7后，均值变为7、中位数仍为7。说明中位数对单个极端值的稳健性，不能推导对制度变迁、系统性缺失或多峰分布同样稳健。

上述17个断言验证人工数列的算术及比较条件。没有产品端到端测试、长期跟踪、预测质量、用户决策改善或安全测试。

## 3. 对心理史学未来候选方法的限定启示

1. 将“过去60天通常行为的描述性参照”与“个人自主选择的目标”“经过独立检验的风险约束”分开存储；中位数没有规范性最优含义。某些指标越高越好，某些越低越好，某些存在区间偏好；不能统一假设偏离为坏。
2. 未来候选基准对象应携带原始时间窗、统计量名称、有效样本量、缺失比例、星期组、来源/单位、版本、生成时点、是否回填及不确定性。界面应允许解释真实使用的是 median，避免 average 命名引起误解。
3. 比较全周与星期条件中位数、不同长度窗口、缺失处理和状态突变，必须在独立未来时间段评价误报率、稳定性及实际效用；不预设人生唯一权重，不改变任何 R 系列冻结协议。
4. 中位数可降低个别离群点的影响，但对样本选择、缺失非随机、时间漂移及季节变化仍敏感。对低频事件或只有少数观测的星期组，需标示数据不足。
5. 自动更新的“通常水平”存在目标漂移风险。若长期目标是减少有害行为，习惯性恶化会改变参照线。候选未来设计应同时保留固定参照、当前状态、用户修订记录与证据支持的安全边界。

## 4. 权限、费用、证据等级和限制

Averages 官方 API 明示 read scopes 限制；文档没有证明撤销授权后第三方已缓存基准快照被同步清除。原始值、派生中位数、历史快照及导出副本应分开做权限与生命周期审计，沿用 F002 候选控制。

官方网页在2026-10-26公开显示个人订阅 USD 6.99/月或62.90/年及30天试用。仅阅读网页，没有注册、试用、付费、认证API调用、下载模型、运行云服务或CI。账户总账单与 GitHub 免费额度未独立核验。

证据分类：官方技术说明 MARKET_E1_DOCUMENTED；厂商定价/功能宣称 MARKET_E0_VENDOR；本轮17项人工算术 E1_SYNTHETIC。实际服务端统计、个人行为改善、预测校准、因果关系、权限执行、商业市场总体需求均 UNKNOWN。

## 5. E/F 登记及下一轮

E：2026-10-26 E004正式日检及E010增量已经归档。本轮另外只读复核新R172历史回测和B独立计算，详见另行新增E011；保留R170跨语言全状态、R136原冻结负对照和original239未完审计。E不修改其他研究轨或索引。

F：2026-W44 F002已完成撤销授权及派生数据生命周期专题，本轮不重复立项。新增候选风险为滚动参照漂移导致误导性“达标”、低样本星期分组误差及撤权后历史派生基准保留；仅作未来安全研究储备。

下一项 MKT043：比较 Exist 的描述性滚动中位数与 Beeminder 用户承诺目标及缓冲/ratchet 机制。聚焦“通常行为改变”与“规范目标改变”是否被混淆，先检查已有 MKT001/MKT029/MKT031，再查英文官方 API、帮助文档和可复算的边界案例。

## 6. 非中文公开来源

1. https://developer.exist.io/reference/object_types/  (Averages: weekly median, 60 days, weekday and overall, progress bar)
2. https://developer.exist.io/reference/averages/  (v2 GET, history, scopes and fields)
3. https://developer.exist.io/guide/read_client/  (weekday progress example and historical averages)
4. https://developer.exist.io/reference/attributes/  (daily values and read scopes)
5. https://exist.io/  (features and public price, accessed 2026-10-26)
6. https://exist.io/about/values/  (vendor privacy claims and export)
7. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/market/MKT041_EXIST_INSIGHTS_SINGLE_ATTRIBUTE_SCOPE_RENDERED_TEXT_AND_TIME_FILTER_2026-10-26.md
8. https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/privacy_safety/F002_CONSENT_REVOCATION_DERIVED_DATA_BACKUP_LIFECYCLE_2026-W44.md
