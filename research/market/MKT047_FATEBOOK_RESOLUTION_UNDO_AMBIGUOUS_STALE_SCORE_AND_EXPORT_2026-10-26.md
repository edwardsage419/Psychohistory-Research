# MKT047 Fatebook 结算撤回、含糊结算旧评分与导出证据语义审计

日期：2026-10-26，Asia/Singapore。track: market。subflow: commercial。status: COMPLETE_BOUNDED_FIXED_SOURCE_AND_SYNTHETIC。前序 MKT046。写前 main HEAD: `6a8668590c1946854e4a99cdf7122804bee25bdf`。CI: NOT_RUN。主动新增费用 0，账户账单和 GitHub 免费权益剩余额度未独立核验。

## 1. 固定来源、去重和范围

延续 MKT046 对 Fatebook 的固定源码版本 `ba7e89c790afd4532bc8e157d9c9c46fc0b4222f`。本轮新增深读结算、撤回、重新评分和 CSV 导出之间的交互，不重复前轮的初始0%与日内概率加权问题。

原始英文来源：
* 官方项目及许可证：https://github.com/Sage-Future/fatebook/tree/ba7e89c790afd4532bc8e157d9c9c46fc0b4222f
* 路由与作者校验，blob `abc75187a6f6f715c1f8f48128dd5123d261da7c`：https://github.com/Sage-Future/fatebook/blob/ba7e89c790afd4532bc8e157d9c9c46fc0b4222f/lib/web/question_router.ts
* 结算、撤回和评分写入，blob `9f11c6cbff8a3dd5fb48f3f92e6995876e2838cb`：https://github.com/Sage-Future/fatebook/blob/ba7e89c790afd4532bc8e157d9c9c46fc0b4222f/lib/interactive_handlers/resolve.ts
* 评分函数，blob `f49c8840751963df502298561a5a8963a81b0748`：https://github.com/Sage-Future/fatebook/blob/ba7e89c790afd4532bc8e157d9c9c46fc0b4222f/lib/_scoring.ts
* 导出，blob `9c68048dfe9ae493bfcbd9075a67e55b33132628`：https://github.com/Sage-Future/fatebook/blob/ba7e89c790afd4532bc8e157d9c9c46fc0b4222f/lib/web/export.ts
* 数据模式，blob `0795c642f4564af62573521ac1ba878dbdfd8c4d`：https://github.com/Sage-Future/fatebook/blob/ba7e89c790afd4532bc8e157d9c9c46fc0b4222f/prisma/schema.prisma

## 2. 新发现 A：结算为 AMBIGUOUS 时存在旧评分保留路径

`question_router.ts` 的 `resolveQuestion` 在作者校验后调用 `handleQuestionResolution`；`getQuestionAssertAuthor` 只核查题目存在与作者身份，未发现“已经结算不可再次结算”的条件。`dbResolveQuestion` 更新 Question 当前 `resolved`、`resolution`、`resolvedAt`。

`resolve.ts` 中 `scoreQuestion` 仅在结果不等于 `AMBIGUOUS` 时调用 `scoreForecasts`。后者删除旧 `QuestionScore` 并重新写入新分数。结果为 `AMBIGUOUS` 时仅生成临时零分对象供后续通知使用，没有在此分支删除原先已持久化的 `QuestionScore`。

所以在固定源码下存在如下候选路径：作者先把二元题目结算为 YES，持久化分数；随后直接再次通过 `resolveQuestion` 将同一题结算为 AMBIGUOUS；Question 当前结算变为 AMBIGUOUS，旧 `QuestionScore` 仍可能保留。与此不同，先执行 `undoResolution` 会通过事务删除该题 `QuestionScore`，再重新结算则重新计算。以上是源码控制流支持的潜在数据一致性缺口，尚未执行真实数据库端到端测试，其他数据库约束和运行配置未验证。

## 3. 新发现 B：撤回结算删除评分，原始结算版本未保留在当前数据库模式

`undoQuestionResolution` 事务将 Question 的 `resolution`、`resolvedAt` 设为空，`resolved=false`，并对当前题目 `QuestionScore` 执行 `deleteMany`。对 exclusiveAnswers 为真的题目，还将全部选项的结算字段置空。非排他选项另有 `undoQuestionOptionResolution` 删除选项评分的分支。

重新结算时 `resolvedAt` 使用新的 `Date()`，时间评分函数将题目创建时间到当前结算时间作为评分视窗。相同历史预测序列、相同结果标签，只要重新结算时间不同，评分视窗就可能改变。当前 Prisma 模式只有 Question 当前结算和 QuestionScore 当前分数，没有独立 QuestionResolutionRevision 或 QuestionScoreRevision 表。应用层分析事件可能记录操作类别，不能等同于可重放的结算历史。

## 4. 新发现 C：常规 CSV 导出不足以重建结算撤回史

`questionsToCsv` 为每次 Forecast 导出概率和时间，但题目标题、截止时间、当前结果、当前 `resolvedAt`、当前 `QuestionScore` 均从当前对象读取。没有导出结算事件ID、前次结果、撤回时间、评分算法版本或评分使用的原始题目版本。先前 MKT046 已指出题目编辑语义问题；本轮新增确认撤回结算和再结算也会造成历史评分证据缺失。仅限定该常规导出路径，不推断数据库备份、第三方日志或外部备份完全不存在。

## 5. 独立合成检查

使用 Python 3 标准库 `fractions.Fraction`，按源码二分量 Brier 公式 `(p-y)^2+(1-p-(1-y))^2` 计算，人工固定 p=4/5：
* YES 的损失为 `2/25=0.08`。
* NO 的损失为 `32/25=1.28`。
* 结果标签改变导致损失差 `6/5=1.20`。
* 人工状态机重建 YES→直接 AMBIGUOUS：若只更新结算字段且 AMBIGUOUS 不删除分数，则旧 `2/25` 仍在。
* YES→撤回→NO：撤回清空旧分数，再结算得到 `32/25`。
本轮实际执行7项独立合成断言，7 PASS、0 FAIL。状态机是源码条件的简化模型，未运行 Fatebook TypeScript、Prisma 或 PostgreSQL，不能视为线上漏洞复现。

## 6. 输入、状态、目标、反馈、隐私、费用、证据

输入：题目、概率、时间、作者结算标签及后续修订。状态：Question 当前结算与时间、Forecast 历史概率、QuestionScore 当前评分。算法：二分量 Brier、日内概率聚合和相对评分。反馈：结算后生成分数与通知，撤回清除当前评分，重结算可改变评分时点。解释性：历史概率可读，历史题目语义与结算事件缺少该常规导出路径的版本化重建。权限：结算和编辑均要求作者身份，undoResolution 在此路由要求登录用户作者身份且未公开 apiKey 参数；尚未测试其他客户端与访问控制。费用：MIT 开源源码可免费研究，托管服务定价未核实，本轮未注册、部署或调用认证接口。

证据分级：固定源码 `SOURCE_CODE_E1`；7项合成计算 `SYNTHETIC_E1`；官方产品自述 `VENDOR_DESCRIPTION`；真实数据库路径、线上行为、用户长期校准改善与独立外部复现均 `NOT_VERIFIED`。

## 7. 候选控制与风险登记

MKT047-C1：结算、撤回、重新结算各有不可混淆的事件ID、时间、作者、结果、题目版本和评分算法版本。
MKT047-C2：含糊结算明确规定历史分数是失效、撤销还是单独保留，当前评分视图必须与当前结算状态一致。
MKT047-C3：冻结首次预测时点、题目文本哈希、截止日期和评分窗口；重结算须同时提供原视窗与新视窗分数，避免回测时点漂移。
MKT047-C4：导出应包含版本化结算事件、评分记录及删除和更正证明，保留最小审计信息且遵守F轨数据撤销约束。
MKT047-R1 HIGH：直接改为 AMBIGUOUS 后旧持久化分数可能仍被读取。
MKT047-R2 MEDIUM：撤回再结算使用新 resolvedAt，可能改变时间评分对象。
MKT047-R3 MEDIUM：当前态导出遗漏撤回和重算历史，无法完整重放。
MKT047-R4 MEDIUM：作者可以重新结算，需明确结果更正和审计权限。

## 8. 轨道边界与下一项

E当日正式日检 E004 已完成；本轮另行核查 R176 完整收据归档修复与 R177 新增研究，归档于 E016。F本周 F002 已完成，不重复创建专题；把含糊结算旧评分及撤销历史保留纳入未来候选。所有发现仅作为未来研究知识储备，先完成R系列，再系统分类，最后模型熔炼。没有更改任何冻结协议或预设人生效用权重。

下一项 MKT048：检查 Fatebook 多选题结算及选项撤回的状态一致性，特别是非排他多选的父题目结算与选项评分是否同步；若无新的源码证据则转向另一免费开源预测日志。
