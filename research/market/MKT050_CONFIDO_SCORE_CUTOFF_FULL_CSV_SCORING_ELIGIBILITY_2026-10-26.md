# MKT050 Confido 评分截止时间、完整CSV历史与评分资格的可追溯性研究

日期：2026-10-26（Asia/Singapore）。track: market。subflow: commercial。状态：COMPLETE_BOUNDED_SOURCE_AND_SYNTHETIC。前序 MKT049。写前 main HEAD：`f46b26f9bbd39652ef8fabdb0e48d97b1084c4c5`。CI：NOT_RUN。主动新增费用：0；账户整体账单及 GitHub 免费权益余量未独立核验。

## 1. 去重与来源固定

本轮先读取 main 最新提交、MKT049、E018、当日 E004、本周 F002，以及 R180 新增协议、主研究和 B 轨收据。MKT046 至 MKT049 已审查 Fatebook 的题目修改、结算撤回、评分、选项身份与导出；本轮改为审查新的开源系统 Confido 的**评分时间截面与完整历史导出的语义差异**。

固定英文开源版本：`confidoinstitute/confido1@91f4636a8013008ed573198d5d656fce091bcd27`。该仓库默认分支 master，公开 AGPL-3.0。固定版本仅用于源码结论，不能代表托管服务器实际部署版本。

原始英文资料：
1. 官方评分说明：https://confido.institute/manuals/scoring.html ，明确允许持续更新预测，评分采用预先选定时间点，之后更新不改变评分。
2. 官方功能与费用：https://confido.institute/confido-app.html ，说明二元、数值、日期问题、群组、权限、CSV 导出、免费工作区及可另行报价的定制功能。
3. 源码 DATAMODEL.md：https://github.com/confidoinstitute/confido1/blob/91f4636a8013008ed573198d5d656fce091bcd27/DATAMODEL.md ，每个问题保留预测历史；预测包括时间、用户、分布，数值分布支持正态截断及离散化。
4. 源码 Calibration.kt：https://github.com/confidoinstitute/confido1/blob/91f4636a8013008ed573198d5d656fce091bcd27/src/jvmMain/kotlin/tools.confido.application/Calibration.kt ，`getScoredPrediction` 使用 `effectiveSchedule.score` 和历史管理器 `at` 选取评分时点的预测。
5. 源码 Score.kt：https://github.com/confidoinstitute/confido1/blob/91f4636a8013008ed573198d5d656fce091bcd27/src/commonMain/kotlin/Score.kt ，二元评分为 `4*(0.25-(outcome-p)^2)`，范围 -3 至 1，越高越好；数值题当前返回 null。
6. 源码 CsvExport.kt：https://github.com/confidoinstitute/confido1/blob/91f4636a8013008ed573198d5d656fce091bcd27/src/jvmMain/kotlin/tools.confido.application/CsvExport.kt ，`LAST`、`LAST_SCORED`、`DAILY`、`FULL` 四种导出；每个有二元结算结果的导出行都单独计算 `brier`。
7. 源码 CsvExportDialog.kt：https://github.com/confidoinstitute/confido1/blob/91f4636a8013008ed573198d5d656fce091bcd27/src/jsMain/kotlin/components/redesign/rooms/dialog/CsvExportDialog.kt ，导出界面支持四种历史粒度和群组或个人预测。
8. 源码 Server.kt：https://github.com/confidoinstitute/confido1/blob/91f4636a8013008ed573198d5d656fce091bcd27/src/jvmMain/kotlin/tools.confido.application/Server.kt ，导出要求登录、拒绝 guest，并按群组预测、个人预测、评论分别验证房间权限。
9. 源码 routes/Score.kt：https://github.com/confidoinstitute/confido1/blob/91f4636a8013008ed573198d5d656fce091bcd27/src/jvmMain/kotlin/tools.confido.application/routes/Score.kt ，排行榜使用 `getScoredPrediction`。

## 2. 真实新增机制：完整导出每行的 brier 与官方评分资格不同

Confido 允许用户不断更新概率，评分仅取问题 `score` 时间点对应的历史预测。另一方面，`PredictionExport.predictionRow` 对任何有二元结算结果的预测行均生成 `brier` 字段。选择 `FULL` 会导出全部预测历史，包括评分截止时间后的预测；选择 `DAILY` 会按日保留一条；选择 `LAST_SCORED` 才直接调用 `getScoredPrediction`。

因此，完整CSV中的每个 `brier` 是**该行概率对最终结果的单行反事实评分**，不自动代表该行进入官方排行榜。所查导出字段有 `timestamp`、`date`、`time`、`probability`、`resolution`、`brier`，多问题时另有 `question_id`；没有逐行写出 `score_time`、`is_scoring_eligible`、`scoring_policy_version`。若下游直接平均 `FULL` CSV 的全部 `brier`，得到的是另一种评价规则。这个结论基于固定源码的静态控制流，尚未在真实服务器执行。

## 3. 独立人工测试：14项全部通过

使用隔离 JavaScript 对固定源码可见的二元评分公式与截止时间选择做独立人工模拟，14项断言全部 PASS。仅模拟可见的选择与计算逻辑，没有运行 Kotlin 服务端、MongoDB 或真实账户。

人工题目最终结果 YES，评分时间为2026-10-25 10:30 UTC。10:00提交 p=0.2，11:00提交 p=0.9。

| 对象 | 概率 | 标准化 Brier 得分 |
| --- | ---: | ---: |
| 截止前 10:00，官方应计入 | 0.2 | -1.56 |
| 截止后 11:00，FULL 导出仍可单行评分 | 0.9 | 0.96 |
| 错误地平均两行 |  | -0.30 |

两行简单平均 -0.30 与官方截止时点评分 -1.56 不同。若下游误选最新一行，则得分0.96，差异更大。人工断言还覆盖截止时间恰好等于预测时间、截止前无预测、截止后两条均可选、正确100%得1、错误0%得-3、50%得0及反向结果等情况。人工测试证明两套评价语义可以分离，不能据此证明产品存在实际线上故障。

## 4. 数据、算法、目标、反馈、隐私、费用与边界

真实输入：二元或数值/日期问题、用户时间戳预测、结算结果、房间及用户身份、评分时间。状态表达：问题和房间、成员角色、预测历史、概率分布、结算、群组聚合；数值题采用概率分布，公开 DATAMODEL 记录正态、截断和离散化机制。算法：二元标准化 Brier、时点历史选择、个人与群组校准；群组聚合细节未独立数值复算。目标：帮助用户记录不确定性、观察校准和群体判断；未证实能改善长期人生决策。反馈：房间排行榜、校准曲线、CSV，依赖问题是否可结算和评分时间设置。自我修正：用户可更新预测；所查资料没有证明系统会自动纠正用户的偏好或价值权重。

隐私与权限：服务器在导出时验证登录与房间权限，拒绝 guest；个人导出行包含 `user_id`、`nick`、`email`，应按潜在个人信息处理。文档称可自行部署，但本轮没有检查托管方数据保留与删除的实际执行。CSV中的单行得分、时间与邮箱可形成可再识别的行为轨迹。费用：官方声明标准工作区免费，定制需求可报价；本项目未申请账户、未部署服务、未使用收费API或云资源。开源许可为 AGPL-3.0，未来商用集成须单独审查义务。

局限：固定源码可能不同于托管版本；未运行端到端导出；没有完整题目修订事件账本或评分规则版本的证据；对用户长期效用、跨文化公平、预测准确率的独立实证验证均为零。

## 5. 证据等级与候选控制

SOURCE_CODE_E1：固定源码直接支持评分时间选择、导出四种模式、每行单独得分、权限与字段结构。SYNTHETIC_E1：14项人工断言。VENDOR_DOCUMENTATION：官方产品、价格、功能及评分说明。INDEPENDENT_REAL_WORLD_VALIDATION：NONE。MARKET_CLAIM：不能替代科研证据。

MKT050-R1 MEDIUM：FULL 或 DAILY 导出在下游被误当作官方评分样本，导致回测口径改变。
MKT050-R2 MEDIUM：CSV缺少逐行评分资格及评分时间元数据，跨工具复算难以确认截止语义。
MKT050-R3 MEDIUM：个人预测导出包含邮箱与历史时间序列，存在敏感行为推断及二次分享风险。
MKT050-R4 MEDIUM：评分时间或结算结果事后变更时，旧导出是否可完整重建仍未验证。

候选控制：将 `forecast_created_at`、`scoring_cutoff_at`、`resolution_at`、`scoring_policy_id`、`is_eligible`、`question_version` 与原始概率分离保存；保留按评分时间截面重放和全历史诊断两种评价，输出时显式区分；个人数据导出按最小权限、去标识化和撤销生命周期管理。上述均是未来研究候选，当前不开发个人决策产品。

## 6. E/F状态与后续

E轨今日全轨正式日检 E004 已完成。本轮已读取 R180 冻结协议、主收据、B独立整数笛卡尔积收据，进行增量审计并另行登记 E019；未改写 R、B、TH、A、C、D、F 轨。F轨 2026-W44 F002 已完成，继续保持每周一个独立专题，新增“完整预测历史导出的可再识别性与撤销后评分副本”候选风险，留待 F003 或后续周。零新增费用，未启用 CI。项目仍按完整 R 系列、系统归纳、模型熔炼的既定顺序推进。

下一轮 MKT051：深查 Confido 的 `DAILY` 导出顺序和聚合、评分时间修改的历史语义，以及导出权限与最小数据字段的风险边界；优先从同一固定源码做负对照，必要时转向其他免费开源预测日志系统。