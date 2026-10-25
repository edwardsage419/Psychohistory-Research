# MKT027 ProjectionLab 区块重采样、路径依赖与相关账户风险

date: 2026-10-25 (Asia/Singapore, UTC+08)
track: commercial_market
subflow: market
status: COMPLETE_BOUNDED_OFFICIAL_CHANGELOG_AND_EXPLORATORY_EXACT_TOY
prewrite_main_head: b01595b5610b18db3f1966241efaa8ff6247fa2d
prior: MKT002_PROJECTIONLAB_SAMPLING_SCENARIOS_2026-10-24.md；本报告仅新增此前未深入的 2025 v4.4.0 区块重采样、账户相关性配置与精确路径顺序演示。
source_language: English only
evidence: MARKET_E1_OFFICIAL_CHANGELOG_AND_HELP + INDEPENDENT_EXPLORATORY_TOY_ARITHMETIC + PRIMARY_PAPER_ABSTRACT
product_engine_execution: NONE
CI: NOT_RUN
new_spend: 0 (account-wide billing and free allowances not independently checked)
scope: publicly accessible pages and standard-library synthetic arithmetic; no account, personal data, paid product, paid API, cloud instance, or decision product.

## 1. 官方机制新增事实

### F1 2025-10-13 v4.4.0 新增 Block Bootstrap

[MARKET_E1_OFFICIAL_RELEASE] ProjectionLab 官方版本记录明确，Chance of Success 增加 Block Bootstrap 历史抽样，随机拼接连续年份的历史区块；用户可设置 Block Length，用于调整不同历史时期的混合程度和区块内连续模式的保留长度。官方同时表示，当特定账户使用自定义正态分布收益率时，这些账户在模拟中作为 **100% correlated group** 一同变动。此条是 MKT002 尚未记录的明确相关性约束，属于官方实现说明，实际联合分布源码与 HTTP/界面运行未取得。

[MARKET_E1_OFFICIAL_RELEASE] 同版引入弹性支出规则，允许将支出分为必要、可自由裁量和非支出，并依据投资组合表现改变支出；因此模拟中的行为反馈可由用户配置的规则驱动。公开材料不足以证明模型会依据用户长期预测误差自动校准这些规则。

### F2 2026-04-20 v4.6.0 及 2026-08-18 说明

[MARKET_E1_OFFICIAL_RELEASE] 4.6.0 提供 Fan chart、直方图筛选试验、税收策略阈值及优化视图。官方 2026-08-18 帮助文档强调 Plan 固定增长情景与 Chance of Success 随机或历史情景使用同一计划基础输入；其他选项卡使用 Plan 的假设。2026-06-30 引擎文档称模拟按年结算现金流、税务、资产、提款与负债。2025-04-11 官方帮助文档明确随机采样最多 2000 次，Historical No Looping 的确定历史路径不会因增加抽样次数而产生新信息。

不能将官方成功率当作现实未来事件的已校准概率；随机次数增加只能减少特定抽样机制的 Monte Carlo 误差，无法消除历史样本选择、参数设定、模型结构与现实制度变化造成的不确定性。

## 2. 精确有界合成演示，探索性

这是对 MKT002-H3 提议的探索性数学演示，未事前冻结正式科研验收协议，不能当作产品引擎复现。

设初始资金 100 单位，四年各年回报分别为两次上涨20%和两次下跌20%，每年先按回报调整余额，再固定提取25单位。年度更新 b_t=b_(t-1)*(1+r_t)-25。6种不同排列各恰有同一回报多重集；无提款时终值都为 100*(6/5)^2*(4/5)^2=92.16。使用 Python 标准库 fractions.Fraction 和 itertools.permutations 逐一精确计算，得到：

| 顺序（U=上涨，D=下跌） | 第1年 | 第2年 | 第3年 | 第4年 | 全程不出现负余额 |
| --- | ---: | ---: | ---: | ---: | --- |
| DDUU | 55 | 19 | -11/5 | -691/25 | 否 |
| DUDU | 55 | 41 | 39/5 | -391/25 | 否 |
| DUUD | 55 | 41 | 121/5 | -141/25 | 否 |
| UDDU | 95 | 51 | 79/5 | -151/25 | 否 |
| UDUD | 95 | 51 | 181/5 | 99/25 | 是 |
| UUDD | 95 | 89 | 231/5 | 299/25 | 是 |

这里的负余额仅是用于判定失败的算术诊断值；真实现金耗尽后应停止提款并按明确规则处理缺口。六种排列中两种未触发负余额。若额外人为赋予六种排列相同权重，得到合成条件成功占比 2/6=1/3。该数字没有真实世界概率含义，不能对应 ProjectionLab 的实际算法输出。

第二个有限例子：历史顺序 UUDD 中，长度为2且不跨界的三个连续区块是 UU、UD、DD。按区块均匀抽样时单区块 UU 占比1/3；按单年独立抽样且上涨占比1/2时，UU 占比1/4。两种构造有不同的局部路径权重。此例仅说明区块长度影响路径分布，不能断言产品具体边界处理、循环方式或区块抽样权重。

原始方法学文献 Künsch (1989), DOI 10.1214/aos/1176347265 的公开摘要说明随机有放回抽取连续区块来处理平稳序列依赖。此次仅核对摘要和书目，未取得完整论文实证结果。Block Bootstrap 的区块边界可能破坏跨区块依赖，区块长度和非平稳结构需要单独敏感性检验。

## 3. 产品状态、目标、反馈、权限、解释、费用及局限

输入：人工录入账户余额、收入、支出、投资增长、税务、债务、退休与里程碑事件；可配置历史数据、正态分布、Block Length、弹性支出规则。官方 2026-06-23 帮助文档说明无直接金融账户连接，部分插件可以辅助导入。

状态：年度余额、现金流、提款、税务与里程碑；Chance of Success 以多条路径展示失败与成功条件、Fan chart 和单次试验。抽样器内部实现、跨资产完整协方差、极端尾部及 regime shift 的真实估计未获得独立证据。

目标：用户设置的财务约束、成功类别与阈值；不存在公开验证的唯一人生效用权重。反馈：用户可调整情景、支出灵活度及里程碑并查看结果；未见已核实的现实误差在线自动统计校准。

解释性：单条路径、收益顺序、年度收支和分布图属于可见的机制解释界面；算法源码和前瞻概率校准尚未独立验证。

隐私：官方文档称保存计划后使用 Google Cloud/Firebase、传输及静态加密、JSON 导出与账户删除；无需绑定银行账户。属于厂商说明，缺乏本轮独立安全测试。云端存储与 JSON 可携带副本的生命周期需要分别审计；不能将其描述为已经验证的本地优先实现。

费用：2026-10-25 官网公开 Basic $0/年（列有 Monte Carlo 与历史回测），Premium $129/年，Pro $549/年；付费功能包括更深入的 What-If、Compare、Flexible Spending 和高级分析等，具体功能归属以当前官网为准。未注册、购买或试用。

## 4. 候选方法与风险记录

MKT027-R1：忽略收益时间顺序导致提款风险误判。候选控制：报告完整路径、现金耗尽时间与早期冲击压力测试。
MKT027-R2：将 Block Bootstrap 当成已验证的现实生成模型。候选控制：对区块长度、边界、历史窗口、非平稳性和尾部事件作独立敏感性分析。
MKT027-R3：自定义正态账户被设为完全相关组，可能误读分散投资风险。候选控制：明确展示相关性假设，未来比较独立、完全相关和经验协方差情景。
MKT027-R4：随机模拟比例被解释为现实校准概率。候选控制：分列模型内情景占比、采样误差、结构不确定性和外部校准状态。
MKT027-R5：云端计划和 JSON 导出形成多个副本。候选控制：未来单独记录导出、授权、保留与删除传播，不接入真实财务信息。

这些仅是未来研究知识储备，未采纳为 R 系列模型规则，未开发个人决策产品，未设置人生效用权重。

## 5. E 今日只读治理检查

读取 main HEAD b01595b5610b18db3f1966241efaa8ff6247fa2d、MKT002/MKT026、E002/E003、F001，以及 R152 科学报告、B R152 独立多项似然审计、A ACS 来源门槛。2026-10-25 的 E002/E003 已完成实质检查，本轮未重复创建 E 文件或改动他轨索引。

R152 科学报告明确区分216条有标签场景和72组独特概率配对，135项独特阈值比较、207项赔率比较；其结果为内部人工 E1。B R152 以 Python Fraction 检查两张人工 OD 表的行条件多项似然在三个 alpha 下相等，并报告预指定方向偏置反例成功鉴别；这是同项目独立程序复核，外部独立复现尚未成立。A 轨 ACS 2016至2020 县际迁移资料只完成官方来源和固定宽度字段核查，原始行字节未取得，E3 历史预测尚未开始。新增真人 E2=0，历史 E3=0。新算法的远端 CI 本轮未核实，不能借用历史 CI。E003 登记的 R136 冻结负对照失败、缺少完整 CSV 和 original239 154项逐项待审继续保留。本轮未独立全仓文件冲突扫描、重算 R152 或验证全部 Actions。

## 6. F 本周专题状态

2026-W43 的 F001 已完成，候选控制包含人类否决、最小采集、解释与数据生命周期；本轮不重复立项。新增供 F002 下周研究的候选风险是云端计划与 JSON 导出副本删除范围、财务数据用途隔离、模拟高精度造成的自动化偏差。没有真实敏感数据或产品开发。

## 7. 来源与证据等级

S1 官方 2025-10-13 v4.4.0 changelog: https://projectionlab.com/changelog
S2 官方 2026-04-20 v4.6.0 changelog: https://projectionlab.com/changelog
S3 官方 2026-08-18 Plan vs Chance of Success: https://projectionlab.com/help/plan-vs-chance-of-success
S4 官方 2026-06-30 Simulation Engine: https://projectionlab.com/help/simulation-engine
S5 官方 2025-04-11 Trial Counts: https://projectionlab.com/help/increase-trials-in-chance-of-success
S6 官方 2026-10-25 Pricing: https://projectionlab.com/pricing
S7 官方 2023-06-09 Data Security: https://projectionlab.com/help/data-security
S8 Künsch (1989) abstract and bibliographic record: https://openalex.org/works/W2047694274
S9 官方 2026-06-23 External Account Linking: https://projectionlab.com/help/plugins

MARKET_E1 官方资料证实产品公开的机制与价格；探索性 Fraction 合成运算只证实本文自定义四年模型的数学结论；Künsch 仅核对公开摘要。产品内部源码、真实试用、第三方独立预测验证和安全渗透测试均未完成。营销、文档、数学演示和现实预测效能分开记录。

## 8. 下一项具体研究

MKT028：聚焦 ProjectionLab 的 Block Length 与弹性支出联动，先读官方 Flexible Spending 帮助与 2025 v4.4.0 原始版本说明，设计不同支出底线与区块长度的可复算合成压力测试。事前冻结评分与采样规则后再运行正式方法验证；如重复已有研究，则转向 Beeminder 偏离控制机制。E 每日、F 每周按现有任务登记推进。

归档策略：本报告仅新增 market 独立路径，不覆盖任何研究轨。无新增费用、无计费 API、无 CI、无个人数据；账户整体账单及免费额度尚未独立核验。
