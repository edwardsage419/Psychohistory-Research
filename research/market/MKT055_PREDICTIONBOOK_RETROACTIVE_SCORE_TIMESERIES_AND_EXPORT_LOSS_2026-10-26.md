# MKT055 PredictionBook 历史评分回填与导出完整性边界

日期：2026-10-26（Asia/Singapore）。轨道：market。状态：COMPLETE_BOUNDED_LEGACY_SOURCE_SYNTHETIC。上次 MKT054 已研究 forecast-store 事务时间，当前改为另一款免费开源预测记录系统的历史评分语义。写前 main HEAD `461987ad4a4e0e85123b305ba570229760f4c14e`。主动新增费用0，未调用收费 API、启动 CI、注册账户或运行真实数据库。

## 1. 原始资料与产品生命周期

研究对象：PredictionBook，原项目 `bellroy/predictionbook`，固定 master HEAD `23c83dab7af5312494f215e7118b0f433352d0fd`。该仓库已归档，上游公告说明 PredictionBook.com 于2024-01-10转为只读，并宣布后续停运计划。此处只分析归档代码的机制，未核验2026年线上服务是否仍运行，也未验证真实数据库。

英文一手来源：
1. 固定源码评分器：https://github.com/bellroy/predictionbook/blob/23c83dab7af5312494f215e7118b0f433352d0fd/app/models/score_calculator.rb （固定 Git blob `1178d834532126ee7c4cbe52bee0ec57425a91bb`）。
2. 历史图表：https://github.com/bellroy/predictionbook/blob/23c83dab7af5312494f215e7118b0f433352d0fd/app/views/calibration_scores/_show.html.erb （blob `0e4e99f51876ff3d9b8318ad9d125df9a5d3eec3`）。
3. CSV 控制器：https://github.com/bellroy/predictionbook/blob/23c83dab7af5312494f215e7118b0f433352d0fd/app/controllers/predictions_controller.rb （blob `c9ea76b12526f37a00c871e286e6707a5bb0d7ec`）。
4. 查询分页：https://github.com/bellroy/predictionbook/blob/23c83dab7af5312494f215e7118b0f433352d0fd/app/queries/predictions_query.rb （blob `d3fb9e883d89a4f8ca271b1f1f3b3d656dad8563`）。
5. 序列化：https://github.com/bellroy/predictionbook/blob/23c83dab7af5312494f215e7118b0f433352d0fd/app/serializers/prediction_serializer.rb （blob `b046048dd104d390dfbae09d1ad5a60216bacde2`）。
6. 历史版本字段：https://github.com/bellroy/predictionbook/blob/23c83dab7af5312494f215e7118b0f433352d0fd/app/models/prediction_version.rb （blob `8a859186b4b54c166f9e349e0c22633935622227`）。
7. 原维护者退役公告：https://github.com/bellroy/predictionbook/issues/262 （2023年公告，2024年只读计划）。
8. 第三方研究资源：https://github.com/niplav/iqisa 声称收集过 PredictionBook 历史预测数据，未对其数量、许可和重现性独立审计。

## 2. 真实新增发现：历史评分曲线使用事后最终结果

`ScoreCalculator#score_sql(end_date)` 只对预测响应使用 `cast(r.created_at as date) <= end_date`。它从 `judgements` 中选择每个问题当前已有的最新非空结果，未添加 `j.created_at <= end_date`。因此在后来重新计算早期曲线时，后续才发生的结算可以进入较早日期的评分。图表视图将 `time_series` 中每个 `end_date` 画为该日期的 Brier Score。

独立合成案例：2026-01-10记录概率80%；2026-01-31作为历史曲线截点；2026-02-10首次结算YES；2026-03-10修订结算为NO。按照归档 SQL 的相关筛选：
* 在2026-01-31真实时点，问题尚无结算，历史可见已结算记录数为0。按该类的默认返回，分数为1，count为0，默认分数不能解释为预测质量。
* 2026-02-10之后重算2026-01-31的曲线，该响应被纳入，Brier损失为(1−0.8)^2=0.04，count=1。
* 2026-03-10之后再次重算同一2026-01-31曲线，当前最新结算变为NO，Brier损失为0.8^2=0.64，count=1。

结论：这条曲线可以被理解为“截至某日提交的预测，以今天已知最终结果回顾性评分”。若用户把它解释为“该日当时已知结果所能计算的评分”，就会产生未来信息回填。事后结果修订也会改变过去曲线。未发现图表明确保证历史as-of可见性，故将其登记为**指标语义和可重建性风险**，不推断线上服务存在未经证实的漏洞。

## 3. 独立合成测试与导出完整性

使用 Python 标准库 `datetime` 与 `fractions.Fraction` 模拟时间截点、结果更正和分页，完成15项断言，15通过、0失败。覆盖事前无结算、后续YES、修订NO、同一截点损失变化、100条默认分页及撤回过滤。该模拟未执行 Ruby、SQL 或真实服务，证据等级 `MARKET_E1_SOURCE_CODE_PLUS_SYNTHETIC`。

另有两项独立源码事实：
* `PredictionsController#mine` 使用 `current_user.predictions.not_withdrawn`，调用分页 `PredictionsQuery`，其默认每页100条；导出一次请求没有自动循环所有页。若拥有120条符合条件的预测且未显式分页，按控制流只会输出首100条。撤回的预测不在此路径的导出集合。
* `mine` 对 `PredictionSerializer` 调用 `except(:responses)`，CSV 包含当前预测的部分字段和 `version` 号码，但没有逐条响应历史、旧题目版本、结算事件链。仓库数据库模型另有 `PredictionVersion` 与 `Judgement`，因此不能把这个CSV当成完整的可重放事件账本。独立API另有响应字段，需逐端点审查；不能据此推断所有可用导出方式均缺失事件。

## 4. 产品机制、隐私与费用

真实输入：用户创建的预测文字、截止日期、概率响应、结算结果、后续更正与可见性。状态表示：Prediction、Response、Judgement、PredictionVersion。算法：按最新非空结算与截止前响应计算平方概率误差，生成随历史响应日期变化的平均Brier损失。目标：预测校准和反馈；没有看到跨生活领域的长期多目标最优化或自动人生权重学习。自我修正：用户可以修订结果和预测描述，系统的历史曲线随当前状态重算。解释性：源代码可审计，导出不能独立重建全部历史。权限：可见性包括所有人、创建者和群组；未检查完整访问控制和备份清理。费用：归档代码按BSD许可证开放，当前托管服务可用性和任何收费状态未确认；本轮没有产生新增费用。

## 5. 原则性候选控制与证据等级

C1：将 `as_known_at` 的历史可见评分与 `retrospective_final_outcome` 的回顾性评分分开命名、分开计算。
C2：评分记录绑定预测版本、结算版本、知识截止、评分时点和算法版本；修订触发可审计的增量重算。
C3：导出明确说明记录范围、分页数量、撤回项目策略、事件版本覆盖率及校验和；不能仅凭CSV文件存在宣称数据可完整迁移。
C4：隐私与数据生命周期研究应同时检查用户可见历史、导出、备份和已撤回数据的保留差异。
C5：以上均为未来候选知识，不开发个人决策产品、不设唯一人生效用权重、不更改R系列冻结协议。

证据：上游固定源码 `SOURCE_CODE_PRIMARY`；维护者退役公告 `OFFICIAL_PROJECT_NOTICE`；15项人工检查 `SYNTHETIC_E1`；第三方归档介绍 `THIRD_PARTY_UNVERIFIED`；线上真实运行、用户效果、外部独立复现均为 `NOT_VERIFIED`。

## 6. E、F联动及下一轮

E轨本日已有E004全轨日检；本轮将独立审计R187新后验收研究，不改其他轨文件。F轨本周F002已完成，暂不重复立项。新增候选隐私风险为导出遗漏撤回历史、事后修订对评分解释的影响。

下一轮MKT056优先核对另一款免费开源系统的“历史已知结果评分”与“最终结果回顾评分”是否明确区分，并寻找本地可执行、零新增费用的跨产品导出完整性测试。
