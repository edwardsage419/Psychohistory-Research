# MKT242 ProjectionLab 确定性规划与随机成功概率的语义隔离

track: market
run_date_utc: 2026-11-03
baseline_main: d4488c03d84e8b657fbf9ec9defa3b731ff3a62b
status: COMPLETE_BOUNDED_OFFICIAL_DOCUMENT_REVIEW
evidence: MARKET-E1_OFFICIAL_DOCS_PLUS_INDEPENDENT_USER_REPORTS
native_execution: NOT_RUN
real_decision_effect: NOT_VERIFIED
paid_services: NONE

## 实际产品机制

官方2026-06-30帮助文档解释模拟器按365天处理一年内工资、扣缴、支出、债务、股息、税、最低分配和租金等，按年输出余额与现金流。用户输入账户、收入、费用、投资与税收假设，调整后可看年度结果。https://projectionlab.com/help/simulation-engine

官方2026-08-18文档明确：Plan标签使用用户输入的固定增长率，Chance of Success运行多次历史或随机市场路径，回报、股息和通胀可变；两者共用规划输入，其余标签依赖Plan的固定假设，而非Chance of Success随机路径。https://cdn.projectionlab.com/help/plan-vs-chance-of-success

因此单一路径的年度数字不能被误读为随机结果的期望或置信区间，成功率亦是给定假设和模拟规则的条件性输出。官方说明可以自定义概率分布、历史回测及风险容忍度，但本轮未核验底层抽样代码、随机种子、各路径权重、校准和外部有效性。https://cdn.projectionlab.com/monte-carlo

## 独立外部材料与证据界限

2025-11-13的公开用户讨论报告：同一家庭规划在ProjectionLab与理财顾问软件中出现相反的成功判断。该报告是未经独立审计的自述，无法确认输入、税务、通胀和风险定义完全一致，也无法断定任何一方计算错误。它是有意义的外部失效疑点，值得设计同输入、同定义的跨软件复验。https://www.reddit.com/r/DIYRetirement/comments/1owbyb6/the_accuracy_of_projectionlab/

官方隐私说明：保存的规划数据位于云账户，使用Google Cloud/Firebase，支持JSON导出与删除；不要求链接金融账户。免费基础版与付费保存能力需区分；本轮未注册、未输入个人财务数据、未购买。https://cdn.projectionlab.com/help/data-security

## 对未来研究的可检验问题

1. 同一规划输入下，固定路径和随机路径是否被清晰标注并解释其条件性。
2. 以相同现金流、收益路径、税收规则、成功定义对照不同软件，隔离输入差异与引擎差异。
3. 模拟成功概率是否经过真实滚动预测校准，以及用户看过结果后是否改善真实决策，仍无本轮独立证据。
4. 免费研究只审公开文档与匿名案例，禁止输入用户私人财务资料。

## E/F协调

E168与F010的既有完成记录仅由先前交接支持，本轮代码搜索未返回对应日志路径，未重复登记。R272 P0无关闭证据；不升级科学等级。开放PR按实时查询为12项，均draft，未合并；队列净变化UNKNOWN。CI未触发，账单未核实。R073及PESEN v0.1保持冻结。
