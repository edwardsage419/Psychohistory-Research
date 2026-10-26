# MKT054 forecast-store 事务时间戳与历史提交可见性边界

日期：2026-10-26（Asia/Singapore）。轨道：market。状态：COMPLETE_BOUNDED_SOURCE_AND_SYNTHETIC。前序：MKT053。写入前 main HEAD：`79469e504443e53fc7d771097ffb8ae3b30f3c22`。主动新增费用为0，未启动数据库、CI、收费API、GPU或云资源。整体账单及 GitHub 免费权益余额未独立核验。

## 1. 资料、固定版本与本轮新增问题

研究对象为英文开源项目 timescale/forecast-store，固定上游 HEAD `57c17880416ac1da440ff5759576f2c2c9c2a793`，该版本也是本轮检查到的上游最新提交。许可证 Apache-2.0，Python>=3.12，核心路径可使用 PostgreSQL 14+，TimescaleDB 为增强选项。固定源码：
1. https://github.com/timescale/forecast-store/blob/57c17880416ac1da440ff5759576f2c2c9c2a793/src/forecast_store/ddl.py ：`runs.recorded_at` 和预测点 `recorded_at` 均声明 `DEFAULT now()`；预测点主键 `(series_id,target_time,run_id)`。
2. https://github.com/timescale/forecast-store/blob/57c17880416ac1da440ff5759576f2c2c9c2a793/src/forecast_store/write.py ：`write_forecast` 写入 run 和 points，不显式写入 recorded_at；模块函数不负责 commit。
3. https://github.com/timescale/forecast-store/blob/57c17880416ac1da440ff5759576f2c2c9c2a793/src/forecast_store/queries.py ：`forecast_asof` 可选 `f.recorded_at <= recorded_before`，同时限制 `available_at <= asof`；同知识时间并列仍按 `available_at DESC` 选行，MKT053 已登记，不重复计为新发现。
4. https://github.com/timescale/forecast-store/blob/57c17880416ac1da440ff5759576f2c2c9c2a793/tests/test_queries.py ：所读 live test 在两次预测之间显式 commit、取 `clock_timestamp()` 作为截点，再 commit，测试正常先后提交场景。所查测试未覆盖事务起始时间早于截点、实际提交晚于截点的历史可见性边界。
5. PostgreSQL 官方英文文档：https://www.postgresql.org/docs/current/functions-datetime.html ，明确 `now()` 等于 `transaction_timestamp()`，为事务开始时间，不是实际提交时间。
6. PostgreSQL 官方英文文档：https://www.postgresql.org/docs/current/transaction-iso.html ，默认 Read Committed 下普通 SELECT 仅看到查询开始前已经提交的其他事务数据。

## 2. 本轮真实增量：recorded_at 不是历史提交可见性的充分证据

MKT054-R1 HIGH，源代码和数据库规范共同支持的历史回放边界。预测点的 `recorded_at DEFAULT now()` 使用事务开始时间。假设一个事务于09:00:00开始且已经执行首个语句，09:00:30写入预测，09:01:00才提交；`available_at` 声称08:59:00。09:00:15时另一连接查询看不到该行。09:02:00重新执行历史回放，指定 `asof=09:00:15` 与 `recorded_before=09:00:15`，该行满足两个时间字段筛选，且此时已经提交，于是可被选入回放候选集合。由此可见，仅凭这两个时间字段，无法保证精确重建09:00:15时其他连接真实可见的行集合。

该问题与 MKT053 的相同 available_at 并列排序不同。即使每个目标只有唯一预测，事务开始时戳与提交可见性仍可能分离。风险成立需要事务跨越目标截点且随后成功提交。不能推断产品实际已发生历史评分污染，也不能将其表述为未授权安全漏洞。

## 3. 独立合成检查

本轮使用 Python 标准库 datetime/dataclasses 编写独立时间线模拟，明确区分事务开始、插入、提交、来源知识时间、历史截点、回放执行时间。完成12项断言，12通过，0失败。主要覆盖：
1. 跨截点事务在回放时满足 recorded_at 与 available_at 条件。
2. 同一行在原历史截点时因尚未提交而不可见。
3. 更早的截点可以排除该行。
4. 回放执行时点早于提交时，该行仍不可见。
5. 提交发生在历史截点之后、但早于回放的变体，同样造成差异。
6. 截点前完成提交的对照可见性一致。
7. 回滚事务在历史时点和回放中均不可见。

这是根据 PostgreSQL 官方语义编写的人工状态模型，未启动 PostgreSQL、未运行仓库 SQL 或事务集成测试。证据等级：SOURCE_CODE_E1 + PRIMARY_DATABASE_DOC + SYNTHETIC_E1；真实数据库集成验证=NONE，线上影响=NONE，真人长期决策改善=NONE。

## 4. 产品机制完整记录

真实输入：时序 actuals、predictors、forecasts，以及模型运行标识、来源知识时间、目标时间和数据库时间。状态表示：多版本追加记录、run_id、model_version、可另存的评价版本。算法：按 asof 选取历史知识截点前预测，recorded_before 额外过滤系统记录时间。目标：历史回测、漂移检测、模型版本比较。反馈与修正：新运行和新评价版本；未查到自动调整人生效用权重的功能。解释性：可以返回被选 run_id，仍需补充事务可见性和并列决策的证明。权限与隐私：数据库 SDK 未提供面向个人的完整同意撤销和申诉机制；不能据此断言数据库自身没有访问控制。费用：开源代码免费，现有本地设备可能满足研究需求，任何新托管或付费数据库都被当前零新增费用约束排除。

## 5. 原则性候选控制及限制

候选 C1：未来预测评分必须显式区分事务开始、记录写入、成功提交和评分读取快照的语义。
候选 C2：若要求重建某历史时刻其他连接的真实可见集合，需验证数据库快照或可审计提交顺序的具体实现，不能只把 `DEFAULT now()` 改名为“提交时间”。
候选 C3：评分清单保留输入 run_id、知识截点、记录截点、读取事务快照或等价证据、评分版本、唯一选择规则。
候选 C4：使用两连接、跨截点未提交事务、提交后重放、回滚、并列 available_at 等场景进行免费本地数据库集成测试；只有确认设备上已具备所需组件且无费用时才执行。否则维持文档审查和待办。
候选 C5：审计日志保留必要的不可识别事件标识，避免存储可反推出健康、财务或关系敏感信息的完整原文。

所有候选均为未来知识储备，不开发个人决策产品，不改变 R073、PESEN 或其他冻结协议，不预设统一人生效用权重。

## 6. E、F 联动与下一轮

E轨今日全轨实质日检 E004 已完成；本轮继续独立审计最新 R185，并保持原有问题队列。F轨 2026-W44 F002 已完成，记录本次时间戳与可见性错配可能影响申诉证据，暂不重复创建本周专题。下一轮 MKT055：优先审查其他免费开源预测日志在事务提交可见性、历史评分快照与数据删除之间的机制差异，或在英文官方文档中寻找 PostgreSQL 可复核的零费用集成验证方法。