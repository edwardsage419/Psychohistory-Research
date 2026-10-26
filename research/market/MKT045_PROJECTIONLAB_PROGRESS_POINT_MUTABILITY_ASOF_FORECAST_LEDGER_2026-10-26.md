# MKT045 ProjectionLab Progress Points 可编辑历史与预测评分时点审计

日期：2026-10-26，Asia/Singapore。track: market。subflow: commercial。status: COMPLETE_BOUNDED_OFFICIAL_DOCUMENTATION_AND_SYNTHETIC_ASOF_REPLAY。observed_head: 595a6f2a01d2f67b94ce303387b0d29d113a0396。前序 MKT044。ci_status: NOT_RUN。billing_checked: 本轮主动新增费用 0，账户账单与免费额度未独立核验。未注册、未购买、未输入真实个人数据、未使用计费 API。

## 1. 已确认的官方机制及来源

2026-06-16 英文官方帮助《How do I update account balances and check progress over time?》明确，修改 Current Finances 余额时系统自动创建当日 Progress Point；用户可关闭自动创建。进度点记录 Net Worth、Assets、Liabilities，可执行 Edit、Duplicate、Delete。Edit 可以更改日期及单个账户值，Duplicate 可另存修改后的日期或账户值，Delete 删除指定进度点。官方文字同时出现“each day you make updates”和“each time you make a change”，没有解释同一天多次修改的去重或版本规则，因此不推断其内部事件数。https://projectionlab.com/help/update-account-balances

2026-09-08 英文官方《How to Update Current Finances》指出，普通计划继承 Current Finances，具有 custom starting conditions 的计划例外；余额更新会形成当日 Progress Point。https://cdn.projectionlab.com/help/update-current-finances

2023-12-13 官方《How do I compare actual progress to my projections?》明确，Actual Progress 叠加需要足够早的 fixed-date plan 及进度点。https://projectionlab.com/help/overlay-actual-progress

2023-06-09 官方《How is my planning data stored and protected?》称可以导出、恢复 JSON，计划存于账户云端；未说明 JSON 是否包含每次进度点编辑的历史事件及删除墓碑。https://projectionlab.com/help/data-security

2026-04-20 v4.6.0 changelog 称 Reports 支持 PDF、CSV、JSON 导出，这是计划级表格导出；不能据此推断完整账户事件日志随之导出。https://projectionlab.com/changelog

2026-10-26 官网价格 Basic 0 美元每年、Premium 129 美元每年、Pro 549 美元每年；Downloadable Reports 列于 Premium。研究仅访问公开文档。https://projectionlab.com/pricing

2026-08-07 更新的官方服务条款第7.3节称终止服务后一般在60日内删除 Customer Content，且删除前给予至少30日的合理导出机会，适用法律例外另论。该条款不证明实际进度编辑历史可恢复，也不证明外部备份已删除。https://projectionlab.com/terms

## 2. 新发现及证据边界

官方帮助直接支持“历史进度点可改日期、改数值、复制及删除”。历史评分若只读取当前可见进度点，就可能随事后编辑而变化。是否存在产品内部不可修改的审计事件表、修订时间戳、旧值及删除墓碑，公开资料未证实，不能声称厂商一定丢失历史。

真实输入为人工财务余额及可选插件同步，状态为当前余额、进度点、计划起始条件和固定日期预测；算法与反馈为按文档保存快照并将实际进度叠加于预测。目标是用户设定的财务目标及里程碑，解释界面显示进度图与计划比较。授权与数据权限以云端账户、JSON 导出及插件边界为主，本轮未审查真实权限实现。缺少外部验证的历史预测误差校准、可回放的修订日志和实际用户决策改善证据。

## 3. Python 标准库人工反例，已实际运行

人工预测值100单位，原始进度点80，之后编辑为100，再删除；另有一条在2026-01-05才录入、有效日期回填至2025-12-30的1000单位记录。分别保存 effective_date 与 recorded_at，并按记录时点重放。

| 截至记录日期 | p1 当前可见值 | 与原预测100的绝对误差 | p2 是否已知 |
| --- | ---: | ---: | --- |
| 2026-01-01 | 未记录 | 不可评分 | 否 |
| 2026-01-02 | 80 | 20 | 否 |
| 2026-01-03 | 100 | 0 | 否 |
| 2026-01-04 | 已删除 | 不可评分 | 否 |
| 2026-01-05 | 已删除 | 不可评分 | 是，回填日期2025-12-30 |

以 Python 3 标准库 dataclasses、datetime、fractions 编写并执行8项断言，全部通过。核心规则是 replay(asof) 仅处理 recorded_at 不晚于 asof 的事件，按稳定事件 ID 执行 create、edit、delete。断言覆盖未发生事件不入账、初始误差20、修订后误差0、删除后缺测、回填事件不得进入历史时点。此为自定义人工事件账本的数学与程序演示，未运行 ProjectionLab。

因而同一原始预测在不同数据版本上的 MAE 可以变化，删除后分母也可能改变；历史回填若仅按 effective_date 排序，还会造成事后信息进入过去的评分。数值示例证明这种机制风险可发生，不代表该产品真实产生了错误分数。

## 4. 未来研究候选控制与阻塞

MKT045-C1：冻结 forecast_id、生成时间、输入数据截止时间、预测目标日期、模型及假设版本。记录 forecast_asof 与 outcome_asof，不预设人生效用权重。

MKT045-C2：每个观察点分别记录 event_id、effective_date、recorded_at、修订链、原始来源、操作类型、保留权限和删除状态。修订可以更正历史事实，但评分必须声明使用哪个已知信息截面。

MKT045-C3：将“最新修订事实上的重算分数”与“当时已知事实上的原始分数”并列保留，缺失与删除分别报告，禁止静默用新值覆盖旧分数。

MKT045-C4：导出数据时检查原始预测、进度点当前态、完整修订事件、删除墓碑和来源时间戳是否各自可恢复。厂商是否支持这些字段仍待独立验证。

MKT045-R1 HIGH：可修改进度值改变历史误差。MKT045-R2 HIGH：回填日期形成时间泄漏。MKT045-R3 MEDIUM：删除导致评分样本选择变化。MKT045-R4 MEDIUM：计划级报告导出与账户级备份范围混淆。MKT045-R5 MEDIUM：云端副本与 JSON 恢复涉及 F002 已登记的撤销及删除生命周期。

证据等级 MARKET_E1_OFFICIAL_DOCUMENTATION + INDEPENDENT_SYNTHETIC_EVENT_REPLAY。产品事件日志内部实现、实际导出结构、实时产品执行、真实预测改善及第三方独立安全验证均 NOT_VERIFIED。所有控制仅是候选知识储备。

## 5. E、F 与后续

E004 已满足本日正式治理检查，最新 R175 增量另归档 E014。2026-W44 F002 已完成，本轮不重复创建 F 专题。后续 F003 可考虑“历史更正权与不可篡改预测评分账本的冲突”，须限制审计记录中的敏感信息。

下一项 MKT046：查找免费开源预测日志工具的不可变预测、结果更正、时间截面回放和导出 schema，优先检查源码及测试；若公开资料不支持，登记待核。项目先完整 R 系列，再归纳分类，最后模型熔炼。
