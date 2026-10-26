# MKT052 Confido 评分截止修订、房间继承日程与问题语义版本审查

日期：2026-10-26（Asia/Singapore）。track: market。subflow: commercial。状态：COMPLETE_BOUNDED_SOURCE_AND_SYNTHETIC。前序：MKT051。写前 main HEAD：`433675a0b11875823a6e2b58ce662cd295dd9e95`。主动新增费用：0。GitHub CI：NOT_RUN。整体账单及 GitHub 免费额度：NOT_VERIFIED。

## 1. 去重与来源

先读取 main HEAD、MKT051、E020、当日 E004、本周 F002、R182/B最新增量，确认本报告路径不存在。MKT051 已检查 60 秒历史合并与 FULL/DAILY/LAST_SCORED 的不同口径；本轮新增问题为：**评分截止或题目描述在预测提交之后被修改时，历史预测是否仍可按当时语义重建**。

固定英文源码：confidoinstitute/confido1@91f4636a8013008ed573198d5d656fce091bcd27。相关 Git blob：
1. `src/commonMain/kotlin/Question.kt`，`da402aeda1c1b4021f91564d8ce3ce0bdff82f5e`：Question 包含 name、description、schedule、stateHistory；`effectiveSchedule = schedule ?: room?.defaultSchedule ?: QuestionSchedule()`。
2. `src/jvmMain/kotlin/tools.confido.application/routes/Question.kt`，`9860d9f0799660c48e81b043d6e6441b52f95f1c`：`EditQuestionComplete` 覆盖题目内容；仅状态变化时补充 stateHistory；权限要求 `MANAGE_QUESTIONS`。
3. `src/jvmMain/kotlin/tools.confido.application/routes/Room.kt`，`71b153133c95cc017524efde5c5aab101c614fb0`：房间拥有者可以修改 defaultSchedule。
4. `src/jvmMain/kotlin/tools.confido.application/Calibration.kt`，`6a4ab620d4377deccf5ff9f40ad68d45bb5a1f2a`：`getScoredPrediction` 读取当前 `effectiveSchedule.score` 并选取当时可见预测。
5. `src/jvmMain/kotlin/tools.confido.application/routes/Score.kt`，`498d2271152fb85cfc75ccaa18c53254f747e264`：记分板从当前问题和当前截止条件计算。
6. `src/jvmMain/kotlin/tools.confido.application/ServerState.kt`，`dec7bedbce8ab8d7eeb817119b3462d36ee44016`：添加预测时按**当时**的截止时间决定是否合并历史。
7. `src/jvmMain/kotlin/tools.confido.application/CsvExport.kt`，`2b5df35ec7b4365da08d9fa71fe98e5b28a3c882`：多题 CSV 读取当前 `question.name`，`LAST_SCORED` 使用当前有效日程，逐行 Brier 使用当前 resolution。
8. `src/jsMain/kotlin/components/redesign/questions/dialog/QuestionResolveDialog.kt`，`4ac3bd1b31c97f083f1c6a2e61a2bd8f0cfdfb0a`：结算对话框允许设置评分时间，并通过完整题目编辑提交；源码注释提示 TODO 防止覆盖。

官方英文文档：https://confido.institute/manuals/scoring.html 明确截止后预测不计分；https://confido.institute/encyclopedia/calibration.html 说明题目作者或管理员可在创建时或结算时设定评分时间；https://confido.institute/confido-app.html 提供免费工作区与开源自托管说明。以上均为厂商资料，不能当作独立实证。

## 2. 机制发现

**MKT052-R1 HIGH：事后提前截止时间，可能找不回原先有效的预测。** 固定源码在提交时使用当时截止值执行历史合并，随后计算评分时使用当前截止值。若先以09:01:00为截止，09:00:00提交20%，09:00:30提交80%，两次相距30秒且未跨当时截止，较早20%历史可被删除。事后把截止改成09:00:15，原先20%提交无法从保留历史找回，评分可从80%变成无有效预测。此结论为固定源码控制流与人工反例，未做数据库集成验证。

**MKT052-R2 HIGH：事后推迟截止时间，可直接改变同一题目的正式评分截面。** 若初始截止09:00:15，20%与80%两条预测因跨越截止而同时保留。初始评分取20%；截止改成09:01:00后评分取80%。若事件最终发生，标准化 Brier 得分从 `1-4*(1-0.2)^2=-1.56` 改为 `1-4*(1-0.8)^2=0.84`。此处公式和数字为人工计算，不声称真实用户的历史排名已发生变化。

**MKT052-R3 HIGH：继承房间默认日程的题目，可能被房间级设置追溯影响。** `schedule=null` 时当前房间 `defaultSchedule` 直接成为有效截止。房间拥有者修改默认值，可能影响所有继承它的题目的评分选择。源码所查路径未显示逐题历史截止版本快照。

**MKT052-R4 MEDIUM：题目文本更改缺少专门的语义版本轨迹。** `Question.stateHistory` 记录状态变化，完整编辑在状态未变时不会新增该状态记录。CSV 在多题导出时读取当前题目名称。旧概率可以被后来修改的题目语义解释；当前源码字段中没有独立 `question_semantic_version` 或 `score_policy_version`。不能据此断言所有数据库备份、外部审计日志都不存在。

**MKT052-R5 MEDIUM：当前结算值可重算历史行分数。** `predictionRow` 根据当前 resolution 计算导出 Brier。若结果事后更正，导出分数随当前值变化；所查 CSV 不提供逐次结算版本。该结论属于静态代码路径。

## 3. 独立人工检查

使用 Python 标准库模拟已核对的固定源码分支，在同一天内运行 **12项断言，12 PASS，0 FAIL**，无数据库、Kotlin 服务或线上请求：
A. 初始截止60秒，0秒提交0.2、30秒提交0.8，历史合并只保留0.8；后来截止15秒时没有可评分预测。
B. 初始截止15秒，同样两次提交跨截止而均保留；截止15秒时评分0.2，事后改成60秒时评分0.8。
C. 题目 `schedule=null`，房间默认截止由15秒变为60秒，继承题目的评分选择随之改变。
D. 题目名称改变而状态保持 RESOLVED，单靠状态变更历史无法证明旧题目文本。
E. 两次提交相隔恰好60秒，因合并条件是严格小于60秒，两条记录均保留。

上述反例仅证明在指定源码机制和人工时间条件下可能出现差异。未验证真实服务器部署参数、时区、事务竞争、备份、管理员操作日志、用户感知、真实评分改善。

## 4. 产品机制、权限、成本及证据等级

输入：题目名称、描述、二元或数值概率、预测时间、房间默认与题目日程、结算值及成员权限。状态：当前问题、继承或独立日程、历史预测、当前结算、当前评分截面。算法：按有效截止时间选取历史预测，二元题采用 Brier 评分。目标：校准、预测反馈与群组比较。自我修正由用户更新概率实现；源码未证实自动优化个人长期人生目标。

权限：题目编辑需要 MANAGE_QUESTIONS，房间默认日程修改需要 ROOM_OWNER；个人导出可能包含用户邮箱与时间轨迹。修改权有访问控制，仍需可追溯的版本控制。官方免费工作区可申请，特殊开发另行报价；本项目不申请账户、不自托管、不采购、不触发付费资源。

证据分级：SOURCE_CODE_E1 固定源码静态分析；SYNTHETIC_E1 12项人工断言；VENDOR_DOC 官方帮助文档与收费声明；INDEPENDENT_RUNTIME=NONE；HUMAN_LONG_TERM_OUTCOME=NONE。不得将上述人工反例解释为线上已发生的漏洞或真人决策改善。

候选研究控制：预测创建时冻结 `question_text_hash`、`question_version`、`score_cutoff_version`、`scoring_policy_version`、`resolution_version`；保留原始事件与事后修订事件；房间日程继承须保存当时生效值；历史回测采用可验证的 as-of 截面，事后更正产生新评分版本而保留旧评分证明。均为知识储备，不提前开发个人决策产品。

## 5. E/F状态与下一项

E004 今日全轨日检已完成；E020 后 R182 新增960人工风险计算及 B轨对R181真实负对照补证，交 E021 单独只读复核。F002 2026-W44 已完成，不重复专题；本轮新增“历史问题语义修改与撤销后评分版本保留的冲突”候选风险。R系列全部完成后统一归纳，最后模型熔炼。

下一轮 MKT053：优先检查 Confido 结算修订和导出评分版本的更具体可复算路径，若与 MKT052 重复，则转向新免费开源预测日志系统的事件版本化与数据导出。
