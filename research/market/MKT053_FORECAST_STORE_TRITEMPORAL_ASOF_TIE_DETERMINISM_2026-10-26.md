# MKT053 forecast-store 三时间戳预测日志与同知识时间平局的可复现性审查

日期：2026-10-26（Asia/Singapore）。研究轨：market。状态：COMPLETE_BOUNDED_SOURCE_AND_SYNTHETIC。前序：MKT052。写前已核 main HEAD `af78fb4ff08a013e26f1999080b53c5abaf57ed2`，并核验本目标文件不存在。主动新增费用 0，未安装、部署、注册、购买、调用计费 API 或运行 Actions。GitHub 免费额度及整体账单未独立核验。

## 1. 本轮新增对象及来源固定

研究对象：timescale/forecast-store，免费开源预测记录与评价存储库，区别于此前研究的 Confido/Fatebook 消费端预测平台。英文官方 GitHub 仓库 https://github.com/timescale/forecast-store ，固定提交 `57c17880416ac1da440ff5759576f2c2c9c2a793`（2026-09-08）。官方 README：https://github.com/timescale/forecast-store/blob/57c17880416ac1da440ff5759576f2c2c9c2a793/README.md 。固定源码：
1. `src/forecast_store/ddl.py`：`_points_table` 的预测点主键为 `(series_id,target_time,run_id)`；`_latest_view` 的 `DISTINCT ON` 仅按 `series_id,target_time,available_at DESC` 排序。
2. `src/forecast_store/queries.py`：`forecast_asof` 支持 `available_at<=asof` 和可选 `recorded_at<=recorded_before`，最终同样只按 `series_id,target_time,available_at DESC` 排序。
3. `src/forecast_store/read.py`：`read_context_series` 的时间桶聚合使用 `last(value,knowledge_col)`，未在所查查询中明确同知识时间的第二排序键。
4. `src/forecast_store/write.py`：预测按独立 `run_id` 插入，`available_at` 是调用方可指定的知识时间。
5. `tests/test_queries.py`：包含按不同知识时间、记录时间和运行名过滤的测试；所查固定测试未建立同 `available_at` 且不同 `run_id` 的最终选择唯一性。
6. `pyproject.toml`：版本0.1.0、Python≥3.12、Apache-2.0，依赖 psycopg、PyYAML；README 标明 Postgres 14+，TimescaleDB 为增强选项，规范仍为 pre-1.0 草案。

以上均为项目自身源码及文档；没有第三方独立运行认证。原作者 README 中 OpenSTEF 实验和性能数字仅作为作者声称记录，未独立重跑，不升级科研证据等级。

## 2. 产品运行机制和本轮真实增量

数据输入：时序观测 actuals、外部预测 predictors、自有模型 forecasts；每个目标 `target_time`、来源声称可知时间 `available_at`、数据库记录时间 `recorded_at`，预测附带模型、模型版本、run_id 和参数。状态表示：按目标与时间保存多个预测版本及评价记录；更正采用新版本记录。算法：as-of 查询选知识截止前的最新预测，支持额外的数据库记录时间截断；评价可存独立版本。目标：减少回测中的未来信息泄漏，支持重放、版本比较和漂移追踪。反馈和自我修正：通过新预测 run 和新 evaluation 记录实现，未发现自动修改用户人生目标的机制。

**MKT053-R1 HIGH，排序平局尚未被唯一化。** 固定 schema 允许同一 series、target_time 的两个预测 run 拥有相同 available_at，因为主键依赖不同 run_id。固定 as-of SQL 与 latest 视图对这样的两行没有唯一的后续排序键。SQL 的 `DISTINCT ON` 选择同一排序键中的哪一行，在该查询文本下没有可复现的唯一保证。即使 `recorded_before` 固定且两行均在其范围内，这个平局仍存在。该判断是源码和 SQL 语义支持的潜在边界；没有运行 PostgreSQL 服务器来观察实际选择变化，不能宣称线上已发生评分错误。

**MKT053-R2 MEDIUM，聚合的相同知识时间并列问题。** `read_context_series` 使用 `last(value,available_at)`，当同桶同知识时间出现不同值时，所查源码未声明同时间并列的优先级。其实际执行结果取决于数据库聚合实现和执行条件，本轮仅登记需要集成测试的风险，不宣称已证实随机波动。

**MKT053-R3 MEDIUM，三时间戳各自的证据意义不同。** `available_at` 是来源或运行者声明的时间，可用于历史回测的声称可知性；`recorded_at` 是数据库时间，支持区分迟到写入。仅冻结 `available_at` 无法证明历史系统确实已取得该数据；加入 `recorded_before` 可排除其后入库的记录，但仍需要数据来源时间可信性及平局处理策略。原作者设计说明也承认 `available_at` 为可写入的 claim。

## 3. 独立合成反例及边界

使用本轮 Python 标准库 `datetime` 和 `itertools.permutations`，构造同一序列、同一目标日期、同一知识时间、同一 run_name 的两个预测，run_id 分别为 run-A/run-B，概率 q50 分别为0.2和0.8，记录时间依次相差1秒。asof 与 recorded_before 都晚于这两行。执行6项人工断言，全部通过，0失败：
1. 两条均满足 asof 与 recorded_before。
2. 按源码声明的排序字段，两条相同排序键仍允许两种候选首行。
3. 两种候选预测为0.2与0.8。
4. 两行同属相同 run_name，指定 run_name 也不自动解除平局。
5. 将 recorded_before 提前到第一行之后、第二行之前可排除第二行，说明系统时间截断本身有效。
6. 两行 run_id 不同，符合已检查主键允许的情形。

人工设最终二元事件发生，若误将 q50 当作事件概率并使用普通二元平方损失，仅用于演示下游敏感性，两个候选分别得到 `(1-0.2)^2=0.64` 与 `(1-0.8)^2=0.04`。该库的 q50 实际为预测分位数，**不是默认的二元事件概率字段**，上述评分只是说明同值选择歧义可传播到任意依赖该数值的评价，不能归为该产品已实现的 Brier 评分。

合成测试没有调用该库的实际 SQL、Postgres/TimescaleDB、数据库事务、真实用户数据或第三方平台；不等于真实部署验证。

## 4. 隐私、解释性、费用与候选控制

解释性：run_id、model_version、params、三个时间字段为数据与模型来源追溯提供基础；若出现同知识时间的多个运行版本，用户仍需要可解释的确定性选择规则。权限：所查项目是数据库存储 SDK，未发现面向个人的细粒度同意撤销或申诉工作流；不能据此断言 PostgreSQL 本身没有访问控制。敏感信息：未来若承载个人健康、财务、关系或决策日志，模型参数、预测时间及版本也可能成为个人画像；必须单独审查数据最小化、权限、删除与备份生命周期。

费用：Apache-2.0 代码免费。自托管需要现有机器和本地 Postgres，托管 TimescaleDB 可能收费。本轮没有安装任何组件或使用托管数据库；仅采用免费公开英文文档和已有工具进行静态分析，符合零新增费用。

候选方法：为预测 run 明确冲突策略，优先在同 `(series,target,available_at)` 时拒绝语义冲突，或在协议冻结后声明唯一且稳定的排序键；as-of 输出应返回被选 run_id 与选择理由；评分时同时冻结知识截止、系统记录截止、输入版本、模型版本、评价版本和并列处理策略。上述只是未来知识储备，不改变 R 系列冻结协议，也不开发个人决策产品。

## 5. 证据等级、治理联动及下一项

SOURCE_CODE_E1：固定仓库源码、schema、查询文本。SYNTHETIC_E1：6项人工断言及两种候选评分演示。VENDOR_DOC：作者 README、设计文档、依赖及许可证。INDEPENDENT_DB_RUNTIME=NONE；THIRD_PARTY_REPLICATION=NONE；HUMAN_LONG_TERM_DECISION_BENEFIT=NONE。风险级别表示需要测试的优先级，不等于漏洞已在生产环境证实。

E轨当日全轨实质日检 E004 已完成；E021 的 R181 交付偏离仍开放。F轨 2026-W44 F002 已完成，本轮登记同时间并列预测的申诉证据、模型运行标识与删除后历史可复算之间的后续候选风险，不重复本周专题。

下一轮 MKT054：检查 forecast-store 同知识时间并列在最新源码、集成测试和发行版本中的实际处理及数据库事务边界；如发现已覆盖，转向其它免费开源预测记录系统的时间版本及可删除性比较。坚持先完成全部 R 系列，再统一归纳分类，最后模型熔炼。
