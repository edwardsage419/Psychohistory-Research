# MKT051 Confido 预测历史合并、每日导出与评分时间截面研究

日期：2026-10-26（Asia/Singapore）。track: market。subflow: commercial。状态：COMPLETE_BOUNDED_SOURCE_AND_SYNTHETIC。前序 MKT050。写前 main HEAD：`21768c5691bcdabdb87e49db17ee0fecbf903935`。CI：NOT_RUN。主动新增费用：0，整体账户账单和 GitHub 免费额度未独立核验。

## 1. 去重与固定来源

本轮先读 main 最新 HEAD、MKT050、E019、E004、本周 F002、R181 最新报告及B轨收据，确认 MKT051 文件不存在。MKT050 已讨论完整 CSV 中每行反事实 Brier 与正式评分资格不同；本轮新问题是：原始提交历史能否从 FULL 还原，以及 DAILY 如何选择同一天的预测。

固定英文源码版本：`confidoinstitute/confido1@91f4636a8013008ed573198d5d656fce091bcd27`。该源码版本只支持静态控制流分析，不能代表线上部署版本。

英文原始来源：
1. `src/jvmMain/kotlin/tools.confido.application/ServerState.kt`，Git blob `dec7bedbce8ab8d7eeb817119b3462d36ee44016`，`addPrediction`、历史查询排序和评分时点查询：https://github.com/confidoinstitute/confido1/blob/91f4636a8013008ed573198d5d656fce091bcd27/src/jvmMain/kotlin/tools.confido.application/ServerState.kt
2. `src/jvmMain/kotlin/tools.confido.application/CsvExport.kt`，blob `2b5df35ec7b4365da08d9fa71fe98e5b28a3c882`，`FULL`、`DAILY`、`LAST_SCORED` 的导出分支：https://github.com/confidoinstitute/confido1/blob/91f4636a8013008ed573198d5d656fce091bcd27/src/jvmMain/kotlin/tools.confido.application/CsvExport.kt
3. `src/jvmMain/kotlin/tools.confido.application/Calibration.kt`，blob `6a4ab620d4377deccf5ff9f40ad68d45bb5a1f2a`，`getScoredPrediction` 使用评分时间截面：https://github.com/confidoinstitute/confido1/blob/91f4636a8013008ed573198d5d656fce091bcd27/src/jvmMain/kotlin/tools.confido.application/Calibration.kt
4. `src/commonMain/kotlin/tools/confido/state/AppConfig.kt`，默认 `predictionCoalesceInterval=60`；`ServerState.kt` 可通过 `CONFIDO_PREDICTION_COALESCE_INTERVAL` 环境变量修改。默认值属于源码事实，实际部署值未验证。
5. 官方英文评分说明：https://confido.institute/manuals/scoring.html 。官方英文功能与费用说明：https://confido.institute/confido-app.html 。

## 2. 新增机制：FULL 是保留后的历史，DAILY 是逐日最后一条保留记录

`addPrediction` 先写当前预测。若同一用户同一问题的相邻提交间隔小于配置阈值，通常删除上一条历史记录，再插入新记录。存在特例：上一条时间不晚于评分截止、新提交时间晚于截止时，保留上一条，以维护截止时评分资格。默认合并阈值为60秒，严格使用 `<` 比较。群组历史也可能同步清理受影响的旧记录。

因此，`FULL` 查询的是数据库仍保存的预测历史，无法保证包括每次快速修改前的中间提交。即使名称为“全部更新”，在固定源码默认配置下也不具备不可变事件日志的语义。这个结论由删除旧记录的源码直接支持。

个人与群组历史 `query` 均按 `Prediction::ts` 升序读取。`DAILY` 将日期映射到单个预测，遇到同一天新记录即覆盖旧值。因此每个日期保留最后一个被查询到的预测。`LAST_SCORED` 则使用 `effectiveSchedule.score` 及历史 `at` 选取截止时可见预测。日期转换函数的具体时区实现未在本轮单独审计；合成示例全部使用同一日，避免跨日边界推断。

## 3. 隔离人工复核：12项断言全部通过

用独立 JavaScript 模拟已读到的历史合并分支、逐日覆盖及评分截止时选择。三组人工时间戳均处同一日期，概率和时间纯属合成输入。12项断言全部通过，0失败。未运行 Kotlin、MongoDB 或线上 API。

情景A：09:00:00 预测0.2，评分截止09:00:20；09:00:30 改为0.8；09:01:00 改为0.9。首次跨越评分截止，0.2得以保留；后两次相隔30秒且都在截止之后，0.8被合并删除。

| 记录口径 | 结果 |
| :--- | :--- |
| 三次人工原始提交 | 0.2、0.8、0.9 |
| FULL 所能保留 | 0.2、0.9 |
| DAILY 同一天导出 | 0.9 |
| LAST_SCORED 评分时点 | 0.2 |

情景B：没有评分截止；09:00:00预测0.2，09:00:30改为0.8，FULL和DAILY均只保留0.8。情景C：评分截止位于上述两次提交之间，FULL保留0.2及0.8，DAILY为0.8，LAST_SCORED为0.2。

合成断言覆盖三个情景的完整历史、每日记录、截止记录及长度，共12项。源码解释与合成结果相符。尚未进行数据库集成测试，真实同秒并发、回填时间戳、跨时区日期与部署配置属于未验证边界。

## 4. 产品结构、费用、权限与适用边界

数据输入包括问题、个人及群组概率分布、提交时间、结算、评分截止时间和成员身份。状态分为当前预测、合并后历史、问题结算与房间权限。二元评分采用标准化 Brier，历史选择通过按时间排序的数据库查询完成。产品目标为群体预测、校准和评分。用户通过更新概率自我修正，排行榜与校准图提供反馈；所查源码未证明系统能够自动更新人生目标或推断稳定偏好。

权限：服务端导出拒绝未登录及 guest 用户，分别检查个人、群组和评论权限。个人 CSV 可包含用户 ID、昵称、邮箱及时间序列；本轮未接入任何真实个人数据。历史合并属于数据库记录删除逻辑，不能据此推断外部缓存、备份和导出副本已删除。

费用：官方称标准工作区可免费申请，定制另议。本项目仅阅读公开英文材料和源码，不注册服务、不部署、不使用收费 API。开源 AGPL 许可的未来商业义务尚待专门法律审查。当前没有用户长期决策改善、线上导出一致性或跨文化公平的独立实证证据。

## 5. 证据分级与候选控制

SOURCE_CODE_E1：固定版本中历史合并、跨截止保护、升序查询、逐日覆盖、评分截面及权限分支。SYNTHETIC_E1：12项人工断言。VENDOR_DOCUMENTATION：官方评分和免费工作区说明。INDEPENDENT_PRODUCT_RUNTIME：NONE。LONG_TERM_HUMAN_OUTCOME_EVIDENCE：NONE。

MKT051-R1 HIGH：将 FULL 误认为所有原始提交，导致预测修订证据缺失。
MKT051-R2 HIGH：将 DAILY 最后一条误认为评分截止前的有效预测，造成回测信息泄漏。
MKT051-R3 MEDIUM：不同部署合并阈值改变可回放的历史密度，影响跨系统可比性。
MKT051-R4 MEDIUM：个人预测历史包含邮箱和时间轨迹，复制后可能形成可再识别记录。
MKT051-R5 MEDIUM：删除历史记录与授权撤销、备份删除的语义可能被混淆。

候选研究控制：分离不可变预测提交事件与可压缩展示视图；为每条保留记录记录合并策略版本和来源范围；评分采用明确的截止时点快照，逐日导出仅作行为诊断；所有回测记录 `forecast_created_at`、`scoring_cutoff_at`、`question_version`、`score_policy_version`、`history_compaction_policy` 和缺失类型。均为未来知识储备，不提前开发个人决策产品。

## 6. E/F 状态与下一项

E轨今日正式全轨日检 E004 已完成；本轮增量审计独立记录 R181 的新问题，不覆盖其他轨。F轨2026年第44周 F002 已完成，不重复立项。新增“历史合并后不可恢复的原始提交与授权撤销后的备份残留”候选风险，供后续F专题审阅。

下一轮 MKT052：研究 Confido 的评分截止时间修改、历史问题版本与回放边界，若缺乏新增证据则转向另一个免费开源预测日志系统。遵守完整R系列、系统归纳、模型熔炼的顺序。
