# MKT048 Fatebook 非排他多选结算顺序、AMBIGUOUS 评分及 CSV 选项归属审计

日期：2026-10-26，Asia/Singapore。track: market。subflow: commercial。status: COMPLETE_BOUNDED_SOURCE_AND_SYNTHETIC。前序 MKT047。写前 main 最新观察 HEAD：`c90c0e77b15ea785352a5f445b96f1a8326aee70`。CI：NOT_RUN。主动新增费用：0。账户整体账单与 GitHub 免费额度未核验。

## 1. 去重与固定来源

本轮延续 Fatebook 固定源码 `ba7e89c790afd4532bc8e157d9c9c46fc0b4222f`，研究 MKT047 尚未覆盖的非排他多选题分支。未注册、登录、使用认证 API、部署数据库或启动 Actions。

英文一手资料：
1. `lib/interactive_handlers/resolve.ts`，Git blob `9f11c6cbff8a3dd5fb48f3f92e6995876e2838cb`，重点第109至181、555至735、928至1000行：https://github.com/Sage-Future/fatebook/blob/ba7e89c790afd4532bc8e157d9c9c46fc0b4222f/lib/interactive_handlers/resolve.ts
2. `lib/web/question_router.ts`，Git blob `abc75187a6f6f715c1f8f48128dd5123d261da7c`，重点第615至679行：https://github.com/Sage-Future/fatebook/blob/ba7e89c790afd4532bc8e157d9c9c46fc0b4222f/lib/web/question_router.ts
3. `lib/_scoring.ts`，Git blob `f49c8840751963df502298561a5a8963a81b0748`，`brierScore` 将 YES 映射为1，其他枚举映射为0：https://github.com/Sage-Future/fatebook/blob/ba7e89c790afd4532bc8e157d9c9c46fc0b4222f/lib/_scoring.ts
4. `lib/web/export.ts`，Git blob `9c68048dfe9ae493bfcbd9075a67e55b33132628`，第13至40行：https://github.com/Sage-Future/fatebook/blob/ba7e89c790afd4532bc8e157d9c9c46fc0b4222f/lib/web/export.ts
5. `prisma/schema.prisma`，Git blob `0795c642f4564af62573521ac1ba878dbdfd8c4d`，QuestionOption、QuestionScore、Question 的当前态字段：https://github.com/Sage-Future/fatebook/blob/ba7e89c790afd4532bc8e157d9c9c46fc0b4222f/prisma/schema.prisma
6. 产品公开页面：https://fatebook.io/ 。页面展示二元及多选题预测，产品营销描述不能作为校准改善的科研证据。

## 2. 新发现 A：非排他多选题的最后一个选项决定整体评分路径

`handleQuestionResolution(questionId, resolution, questionType, optionId)` 在提供 `optionId` 时先写入该选项的 `resolution` 与 `resolvedAt`。只要仍有选项 `resolution === null`，函数提前返回。当所有选项都有结果时，调用 `scoreQuestionOptions(resolution, result, false)`，其中 `resolution` 是**本次最后一个选项的结果**。随后父题 `dbResolveQuestion` 也以该结果更新父题当前 `resolution`。

`scoreQuestionOptions` 以传入的单个 `resolution !== AMBIGUOUS` 作为全部选项评分的总开关。因此相同一组最终选项标签，若最后提交 AMBIGUOUS，所有选项本次跳过持久化评分；若最后提交 YES 或 NO，则进入逐选项评分。父题结果也跟随最后提交的结果。此为固定源码控制流可直接推导的**顺序依赖候选缺陷**。未通过真实 Prisma/PostgreSQL 端到端测试验证部署表现。

## 3. 新发现 B：先结算 AMBIGUOUS 选项，后结算正常选项，含糊选项可能被当作 NO 评分

当最后一个选项是 YES 或 NO，`scoreQuestionOptions` 遍历全部选项并调用 `relativeBrierScoring(option.forecasts, option)`。其中 `brierScore` 的目标值为 `resolution == YES ? 1 : 0`。因此较早标记为 AMBIGUOUS 的选项仍可能被作为 y=0 的 NO 事件评分。

人工例子：选项A的概率为0.9且结果YES，二分量 Brier 损失0.02；选项B的概率为0.2且结果AMBIGUOUS。若最后结算A，源码分支可能给B赋予按NO计算的0.08；若最后结算B，本次跳过所有选项评分。含糊结果不宜直接视为事件未发生。真实数据库结果、通知及前端显示仍需端到端验证。

## 4. 新发现 C：CSV 导出按父题ID查找分数，未按选项ID匹配

`questionsToCsv` 查询请求者的 `QuestionScore` 后，为每条 Forecast 使用 `questionScores.find(qs => qs.questionId === f.questionId)` 选择分数。虽然单独识别了 `mcqOption` 并导出选项文本和结果，分数查找条件没有包含 `f.optionId` 或 `qs.questionOptionId`。同一父题下的多个选项行因此可能重复显示同一条先匹配的分数。

人工例子：同一父题的A、B分别具有0.02和0.08的持久化分数；若A分数首先返回，两条选项预测导出都可能显示0.02。查询顺序未明确指定，具体被重复的选项分数不可预先断言。该发现不等于所有历史数据库必然存在错误记录。

## 5. 新发现 D：带 optionId 的撤回同时重置父题及删除父题所有分数

`question_router.ts` 的 `undoResolution` 先调用 `undoQuestionOptionResolution(optionId)`，随后无条件调用 `undoQuestionResolution(questionId)`。后者删除父题下全部 `QuestionScore` 并清空父题 `resolution/resolvedAt/resolved`。对于 `exclusiveAnswers=false`，其他选项的结果保持不变。因此单个选项撤回可能清除其余选项已有分数，同时保留其余选项结算标签。该操作的实际授权和事务间故障边界仍待真实数据库测试。

## 6. 独立合成检查

本轮实际使用 Python 3 标准库 `fractions.Fraction` 执行13项人工断言，13 PASS，0 FAIL。覆盖二分量 Brier 精确损失、AMBIGUOUS 与 NO 的区别、最后结算分支、父题状态依赖、父题ID导出匹配、单选项撤回的父题分数清除。测试模型按上述源码控制流抽象，不运行原作者 TypeScript、Prisma、PostgreSQL，也没有模拟并发请求。上述13项属于 SYNTHETIC_E1，不能视为线上漏洞复现。

## 7. 输入、状态、算法、反馈、权限、费用及验证等级

输入：父题文本、exclusiveAnswers、各选项文本、概率及时间、逐选项结果与结算顺序。状态：Question 当前 resolved/resolution/resolvedAt，QuestionOption 当前 resolution/resolvedAt，Forecast 历史概率，QuestionScore 当前逐选项分数。算法：逐选项二分量 Brier，非排他题对已有选项分数取均值；结算顺序决定进入哪条总分支。反馈：持久化评分、通知及 CSV 导出；分数归属可能与选项标签不一致。解释性：原始概率可查询，常规 CSV 缺少可靠的选项分数关联及历史结算事件。权限：路由要求题目作者身份，未测试 optionId 与 questionId 交叉归属及其他访问路径。费用：MIT 开源源码可免费审查，托管收费模式本轮未独立确认；未注册或部署。

证据：固定源码 SOURCE_CODE_E1；13项人工测试 SYNTHETIC_E1；网站产品介绍 VENDOR_CLAIM；真实服务、数据库、独立安全复现、用户决策收益 NOT_VERIFIED。以上均为未来心理史学的候选方法知识，不是个人决策系统的实现或科研效应证明。

## 8. 风险与候选控制

MKT048-R1 HIGH：非排他多选题最终结算顺序改变评分覆盖与父题结果。
MKT048-R2 HIGH：含糊选项在其他选项最后结算时可能按NO评分。
MKT048-R3 HIGH：CSV 使用父题ID选取分数，造成选项评分归属混淆。
MKT048-R4 MEDIUM：撤回一个选项清除父题全部分数，其他选项标签仍保留。

MKT048-C1：以选项状态集合决定父题状态，结算结果应对操作顺序不变，AMBIGUOUS 单独建模。
MKT048-C2：评分键至少绑定 userId、questionId、optionId、outcomeVersion、scoreVersion，导出和重算使用同一关联键。
MKT048-C3：单选项撤回需有明示的作用域和事务一致性测试，保留最小版本化更正记录，并与F轨删除权要求协调。
MKT048-C4：冻结预测时点与原题语义，分开标记未结算、含糊结算、无效评分和已撤回评分。

## 9. E/F状态与下一项

E轨今日正式日检 E004 已完成，本轮独立增量核查 R178 Wilson 区间收据与原始PMF，另归档 E017。F轨2026-W44的F002授权撤销专题已完成，不重复立项；新增候选风险是含糊结算、撤回、导出更正对个人决策解释和申诉的影响。没有修改R系列冻结协议、其他轨索引或人生效用权重。

下一项 MKT049：检查 Fatebook 多选题的前端结果约束与路由参数验证，特别是 optionId 所属题目一致性及排他题的特殊结果处理；若现有机制重复，则转向新开源预测日志或情景版本管理系统。
