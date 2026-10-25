# MKT026 Exist API v2：读取权限、属性所有权与停用可见性的状态边界

date: 2026-10-25 (Asia/Singapore, UTC+08)
track: commercial_market
subflow: market
status: COMPLETE_BOUNDED_OFFICIAL_DOC_AND_LOCAL_SPEC_CHECK
prewrite_main_head: adc66d9b78dafd870377aff11c5c1348b561504f
prior: MKT003、MKT025；本报告只补充此前未展开的 API 读取查询差异、状态组合、属性类型冲突和分页完整性。
source_language: English only
evidence: MARKET_E1_OFFICIAL_DOCUMENTATION + LOCAL_DOCUMENT_DERIVED_SYNTHETIC_CHECKS
remote_product_API_execution: NONE
CI: NOT_RUN
new_spend: 0 (account-wide billing and GitHub free allowance not independently checked)
scope: public pages only; no account, token, personal data, paid API, cloud instance, or personal decision product.

## 1. 本轮真实增量

此次未发现 2026 年新 API 版本发布。官方 changelog 最新列出的 API 重大变更是 2022-08-18 的 API v2 GA；本轮属于对既有机制的深读。相较 MKT025 的 OAuth/ownership 与删除生命周期概述，本轮新增 **读权限和写入所有权的正交性、三个列表端点的不同可见性边界、inactive 查询遗漏风险、属性 template/name 类型冲突及批处理部分成功的审计约束**。

### F1 读取 scope 与写入 ownership 是不同维度

[MARKET_E1_OFFICIAL_API] OAuth2 官方参考将各数据组 read/write scopes 分开。read scope 允许读取对应属性及值；write scope 允许在对应组创建、取得所有权及写入。ownership 文档规定同一属性仅有一个写入服务。写入要求两项条件同时满足：相关 write scope 与当前 owner 身份。已取得 read scope 的第三方能否读取某属性，不以其是否拥有该属性为文档列出的必要条件。

候选权限矩阵（只作官方规则的有限抽象，不代表实测 HTTP）：

| read scope | write scope | client 为 owner | 候选可读 | 候选可写 |
| --- | --- | --- | --- | --- |
| 0 | 1 | 1 | 否 | 是 |
| 1 | 0 | 1 | 是 | 否 |
| 1 | 1 | 0 | 是 | 否 |
| 1 | 1 | 1 | 是 | 是 |

实际还受 token 有效性、属性分组、服务端规则及资源状态约束。表格未覆盖这些因素，不能据此证明具体 HTTP 响应。**重要推论：释放写入所有权不能自动视作撤销原客户端的 read scope**；撤销读权限和删除已导出的数据需要另行处理。

### F2 三类属性读取接口的查询契约不同

[MARKET_E1_OFFICIAL_API] 文档明确：

* `GET /api/2/attributes/`：按 read scopes 列出属性元数据，支持 `owned=true`、`include_inactive=true`、`include_low_priority=true`、`page`、`limit`。
* `GET /api/2/attributes/owned/`：仅列出当前客户端拥有的属性元数据；也支持 `include_inactive=true`，不返回历史值。
* `GET /api/2/attributes/with-values/`：按 read scopes 返回属性与最近日期值，`days` 最大 31，支持 `date_max` 和分页。该端点文档的参数表**没有列出** `include_inactive` 或 `owned`。
* `GET /api/2/attributes/values/?attribute=...`：单属性历史值分页，每页最多 100，受 read scopes 限制。

`include_inactive=true` 说明默认属性列表可能隐藏停用项。**文档没有列出某一端点参数，不等于服务器拒绝该参数；也不能断言停用属性在 with-values 或 values 中绝对不可读取**。这两项仍为 UNKNOWN，需认证环境的合成账户实测；零新增费用约束下不注册或付费。

API 列表含 `count`、`next`、`results`。只读取第一页会造成统计样本截断。一个客户端获得的数据子集还受 read scopes 与 inactive/priority 过滤影响，因此不能把 API 响应计数当作用户全部历史属性总数。

### F3 服务切换和停用形成不同状态

[MARKET_E1_OFFICIAL_API] release 当前 owner 后，若用户已连接另一声明可提供该属性的服务，ownership 可转移；否则属性变为 inactive。返回字段 `service` 表示当前来源，`available_services` 表示可提供数据的候选服务列表；候选列表本身不证明某次转移已经成功。

审计所需状态至少包含：`attribute_id/name`、`template`、`group`、`value_type`、`owner/service`、`available_services`、`active`、`read_scope`、`write_scope`、`value_date`、`value`、`observed_at`。这是未来研究数据血缘账本的候选字段，非产品实施。

切换数据来源可能带来不同量表、单位、测量时段和缺失机制；官方接口不保证新旧来源具有测量等价性。未来量化研究应在来源切换处设断点并检验分布变化，不能把不同来源的时间序列自动拼接为同质观测。

### F4 template 与 name 的语义不同

[MARKET_E1_OFFICIAL_GUIDE] 官方写入教程明确举例：用户可创建同名但不同类型的手工属性。以 `name` 获取所有权可能取得该手工属性，类型与集成应用期望的整数模板不一致；`template` 明确指定系统模板，避免此类错误的类型选择。模板也可能在首次获取时创建新属性。后续模型必须保留值类型与来源，避免把百分比和整数计数混用。

### F5 批处理的 HTTP 202 不能当作全部成功

[MARKET_E1_OFFICIAL_API] acquire/release 每批最多35项；`200` 代表全部成功，`202 Accepted` 可能表示部分失败。响应包含 `success`、`failed` 和逐项错误代码。安全与数据血缘审计应逐项确认状态，不能仅按 HTTP 2xx 标记完成。对 release 的部分成功尤其要避免宣称所有属性都已撤权。

### F6 输入、目标、算法、反馈、解释、费用与可验证性

输入为来自各服务的日级属性值及用户手工记录；状态为属性类型、日期、活动标记、owner/source 和 scopes。此轮没有获得内部相关性算法源码或预测评分的新增证据。Exist 提供属性级追踪与描述性反馈，未见公开、唯一且经验证的人生效用函数。用户可更换来源、修改已有值和隐藏属性；这些操作不证明算法会自动因果纠错。解释性在本轮可核实范围限于 API 字段、官方示例和文档。产品付费信息沿用 MKT025 当日官网记录：$6.99/月或 $62.90/年，未购买；本轮没有重新独立核验结算页面。API 文档是功能契约，缺少真人长期决策改善的独立实证。

## 2. 本地文档派生状态检查

在不连接 Exist 的 JavaScript 隔离环境，执行14项合成断言，14/14通过。覆盖 read/write 分离、owner 写权限、inactive 默认过滤与显式包含、release 后转交或停用、202部分成功、旧 owner 失去写权限、inactive 过滤不能覆盖 read scope。

**这些断言仅检验根据文档编写的抽象状态逻辑内部一致性；没有运行 Exist 官方服务端源码、认证请求或第三方集成。不能提升为独立 API 功能复现或漏洞验证。**

## 3. 新增风险登记与未来候选控制

* MKT026-R1：服务 A 释放 owner 后仍可能持有 read scope。候选控制：分开核对 owner 变化、OAuth 令牌权限与历史导出副本。
* MKT026-R2：inactive 默认隐藏造成统计缺口。候选控制：数据清单查询显式包含 inactive、逐页读取，记录响应过滤条件与时间；with-values 的 inactive 行为标为 UNKNOWN。
* MKT026-R3：来源替换造成测量漂移。候选控制：source change point、单位、量表、缺失率及测量不变性审计。
* MKT026-R4：同名属性类型冲突。候选控制：template/name 双重身份与 value_type 一致性检查。
* MKT026-R5：202 部分成功误报。候选控制：按每项 success/failed 登记，必要时使用后续只读查询确认状态。
* MKT026-R6：分页与 read scope 限制导致观测样本选择偏差。候选控制：保留查询参数、count、next、总页数、授权范围和未获取项目数；不推断被排除项不存在。

这些控制均为未来候选方法，不修改 R 系列冻结协议，不设人生单一权重，不接入真实敏感数据。

## 4. E 今日治理增量（只读）

2026-10-25 E002 和 E003 已完成实质检查，本轮不重复创建 E 文件。读取 main 最新提交与 R150、R151 新科学报告及 B R151 独立 Fraction 审计。R150 新第三方法将243个人工人口率轨迹按终点与完整轨迹划分等价类；R151 新第三方法用12组参数×91组人工初始队列研究三时点总人口观测的线性可观测性，B 用 Fraction 复核。两者均明确为有界内部 E1；无新真人 E2、历史 E3 或外部独立复现。直接查询 R150 新报告 SHA `45b7883c4bb3dd763c01ec89bf1c49c50a8ea770` 和 R151 新报告 SHA `3446d25a50642eafe811b916e87d977cd4d05c8f` 的 Actions head_sha，均返回 total_count=0；这仅说明这两个提交没有关联 run，不代表仓库没有其他历史 CI。

R151 的零行列式负对照未触发，科学报告如实保留；不能将未触发条件记为成功识别。A 轨新增联合国 WPP2024 历史人口数据候选，官方元数据已核，原始 CSV 字节、字段映射和历史留出评分尚未完成，E3=0。original239 v7.8 文件存在，原有154项逐项审计待办与 schema/date 仍标 v7.6 的元数据滞后继续开放；本轮未重新逐行核对239条。R136 冻结负对照历史失败、R074/R075 标签口径问题继续保留。没有修改 R、A、B、TH、C、D、F 或共享索引，未声称任何未验证的 CI 成功。

## 5. F 本周状态

2026-W43 已有 `research/privacy_safety/F001_HUMAN_OVERRIDE_AND_DATA_MINIMIZATION_2026-W43.md`，本轮重新核对路径存在，避免重复生成。F002 留待下周独立研究：授权撤销与数据生命周期，加入本轮发现的 read scope 与 owner 分离、inactive 隐藏、来源切换及部分撤权失败；无真实数据与产品开发。

## 6. 官方英文来源与证据等级

S1 OAuth2 scopes：https://developer.exist.io/reference/authentication/oauth2/
S2 属性列表、with-values、values：https://developer.exist.io/reference/attributes/
S3 acquire/release/owned：https://developer.exist.io/reference/attribute_ownership/
S4 写入教程及 template/name 类型冲突：https://developer.exist.io/guide/write_client/
S5 官方 changelog：https://developer.exist.io/reference/changelog/
S6 先前 MKT025：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/market/MKT025_EXIST_OAUTH_ATTRIBUTE_OWNERSHIP_ERASURE_LIFECYCLE_2026-10-25.md
S7 R150 第三方法：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R150_TERMINAL_TRAJECTORY_IDENTIFIABILITY_THIRD_METHOD_SCIENTIFIC_REPORT_2026-10-25.md
S8 R151 第三方法：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R151_AGGREGATE_OBSERVABILITY_THIRD_METHOD_SCIENTIFIC_REPORT_2026-10-25.md
S9 B R151：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/B_R151_FRACTION_OBSERVABILITY_INDEPENDENT_E1_AUDIT_2026-10-25.md
S10 A WPP2024：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/data_scout/UN_WPP2024_R151_AGE_STRUCTURE_HISTORICAL_E3_SOURCE_GATE_2026-10-25.md
S11 F001：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/privacy_safety/F001_HUMAN_OVERRIDE_AND_DATA_MINIMIZATION_2026-W43.md

## 7. 归档、阻塞与下一轮

此文件为增量 market 路径；GitHub 提交 SHA 须在写入后远端核验。没有启用 Actions、计费 API、收费云资源、购买或订阅；新增费用 0，账户整体账单及免费额度未知。

未解决：inactive 对 with-values/values 的真实可见性、OAuth 撤销后的旧 read token 行为、来源切换后的历史统计是否重算、所有第三方数据副本生命周期；均需要有授权的合成账户或服务端证据，目前受零新增费用与无账号约束。

MKT027 优先轮换至 ProjectionLab 的情景参数、现金流事件与 Monte Carlo 敏感性/解释性，比较参数扰动和结果不确定性。仅公开英文官方文档与独立免费研究。E 下轮检查新提交及阻塞，F 下周独立专题。保持先完成全部 R 系列，再统一归纳，最后模型熔炼。
