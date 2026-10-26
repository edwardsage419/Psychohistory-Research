# MKT046 Fatebook 预测初始零值、时间平均评分及题目可变性源码审计

日期：2026-10-26，Asia/Singapore。track: market。subflow: commercial。status: COMPLETE_BOUNDED_FIXED_SOURCE_AND_SYNTHETIC_EXACT_TEST。observed_main_head: 797bc604e447583bb54e2c703653e7b065a0e0c3。前序 MKT045。CI: NOT_RUN。主动新增费用：0；账户总账单及 GitHub 免费额度未独立核验。没有注册账户、调用认证 API、运行服务、输入真实敏感信息或启动 Actions。

## 1. 新研究对象与固定来源

本轮新增免费开源个人概率预测记录系统 Fatebook。官方英文网站 https://fatebook.io/ 描述：记录问题、概率、截止日期，以 YES、NO、AMBIGUOUS 结算，观察预测校准。固定源码 Git commit `ba7e89c790afd4532bc8e157d9c9c46fc0b4222f`：
* 数据模型：https://github.com/Sage-Future/fatebook/blob/ba7e89c790afd4532bc8e157d9c9c46fc0b4222f/prisma/schema.prisma
* 创建、编辑、结算及导出路由：https://github.com/Sage-Future/fatebook/blob/ba7e89c790afd4532bc8e157d9c9c46fc0b4222f/lib/web/question_router.ts
* 评分函数：https://github.com/Sage-Future/fatebook/blob/ba7e89c790afd4532bc8e157d9c9c46fc0b4222f/lib/_scoring.ts
* CSV 导出：https://github.com/Sage-Future/fatebook/blob/ba7e89c790afd4532bc8e157d9c9c46fc0b4222f/lib/web/export.ts
* 官方开源 README：https://github.com/Sage-Future/fatebook/blob/ba7e89c790afd4532bc8e157d9c9c46fc0b4222f/README.md

README 明示 MIT 许可证及 Docker 本地开发路径。托管网站当前定价、运行时数据库配置和服务端行为本轮未核实。公开源码可免费研究，本轮未安装部署。

## 2. 发现 A：二元问题创建时 0% 初始预测可能被静默跳过

`question_router.ts` 的 `create` 输入允许 `prediction: z.number().max(1).min(0).optional()`，包括数值 0；在二元问题创建路径却使用 `else if (!isMultiChoice && input.prediction)` 判断是否写入 `prisma.forecast.create`。JavaScript 中数值 0 为 falsy，因而该分支对初始 0% 预测不执行写入。0.5 与 1 则进入写入路径。多选选项初始预测采用 `option.prediction !== undefined`，条件不同。

这是固定源码的明确控制流结论。没有在实际数据库中执行创建流程，不能声称已在托管服务复现。研究候选控制：使用 `prediction !== undefined`，并为 0、0.5、1、缺失四类输入增加回归测试。

## 3. 发现 B：先平均概率再平方，可能降低时间变化预测的计分损失

`_scoring.ts` 中 `getWeightedAverageForecastOfInterval` 先计算一天内的时间加权平均预测概率，`relativeBrierScoring` 随后对该平均概率调用 `brierScore`。其二元 Brier 使用 YES 与 NO 两分量之和，等于 `2(p-y)^2`，范围为 0 至 2。与常见 0 至 1 的单分量 Brier 比较时需要统一刻度。

独立 Python 3 标准库 Fraction 合成计算：真实结算 YES；同一天前半日概率 0.1，后半日 0.9。源码结构的“先平均后评分”得到平均概率 0.5、损失 0.50。逐段先评分再按时间平均得到 `(1.62+0.02)/2=0.82`，差额 0.32。恒定概率 0.5 也获得 0.50。因此，若研究目标是评价整个时间段内实际发布的概率质量，先平均再平方会压低波动路径的惩罚。若目标是评价当日平均预测本身，该计算属于另一种评分对象，不能未经约定称为错误。

同一函数在一天内无此前预测且首次预测很晚时，将最后一条预测赋予该区间剩余权重 `1-sumOfWeights`；在只有一条、没有此前预测的情况下，此权重为 1。合成反例：第 23 小时首次给出 100% 且最终 YES，当前区间平均概率仍为 1，损失 0。预测覆盖时长没有在此分支单独扣除。需要明确早期缺报期的评分政策，禁止把晚期一次正确预测误当成整日连续准确。

## 4. 发现 C：预测序列与问题语义的历史版本分离

Prisma `Forecast` 模型含 `createdAt`、`forecast`、`questionId`；`Question` 有可变的 `title`、`resolveBy`、`notes`、`resolution`、`resolvedAt`。`editQuestion` 路由直接更新 title、resolveBy、notes。当前 schema 没有独立 QuestionRevision 或题目文字版本表。`questionsToCsv` 导出每次 Forecast 的创建时间和概率，同时读取 Question 当前 title、resolveBy、notes、resolution；没有独立导出历史题目文本版本。

因此，旧预测的导出行可能关联后来修订过的题目文本和期限。固定源码支持“常规 CSV 导出缺少题目历史版本”这一有限结论；不能排除其他日志系统、外部备份或实际运行配置记录了修改历史。

## 5. 输入、状态、反馈、权限、费用及可验证性

输入：用户录入题目、截止日期、0 至 1 概率、备注、标签、共享范围；也支持后续更新概率。状态：Question、Forecast、QuestionOption、QuestionScore、Comment、User；概率预测按时间独立存行，结算和题目文本当前态在 Question 中。算法：二分量 Brier、时间区间平均概率、相对群体中位数 Brier 排名；人工结算触发反馈。目标：改善概率判断校准，未发现内置的长期人生目标效用权重。解释性：可以追踪预测概率与时间及当前结算标签，历史题目文字语义需另行审查。隐私：Question 具有 sharedPublicly、unlisted、sharedWith；存在账户及 API key；本轮未完成真实权限攻击或删除生命周期验证。费用：开源 MIT；托管服务当前具体收费未独立确认，研究仅使用公开免费资料。

证据分层：官网功能为 VENDOR_DESCRIPTION；固定源码路径为 SOURCE_CODE_E1；16 项 Python Fraction 人工断言为 SYNTHETIC_E1；托管服务行为、真实用户校准改善、第三方独立验证均 NOT_VERIFIED。不能以开源许可推断托管服务零成本或运行效果。

## 6. 独立合成检查与候选控制

本轮独立实际执行 16 项 Python 标准库断言，16 PASS，0 FAIL，覆盖：初始 0/0.5/1/缺失值条件、二分量 Brier 四组边界、日内 0.1 到 0.9 平均、先平均与先平方的 0.32 差额、23 小时后首次预测、无预测区间、继承前期概率。未运行 TypeScript 项目或真实数据库。

MKT046-C1：冻结 forecast_id、question_text_hash、question_version、forecast_created_at、resolution_rule_version、目标日期和预测截止时间，题目修订产生新版本。
MKT046-C2：区分首次预测、后续修订、预测覆盖时长、未作预测时段；先声明评分对象及 0 至 1 或 0 至 2 刻度。
MKT046-C3：结果结算、更正与含糊结果保留事件身份和评分时点；导出同时提供题目版本、预测序列及结果版本。
MKT046-C4：明确删除、撤销授权与可保留的最小审计元数据边界，交由 F 后续专题研究。
MKT046-R1 HIGH：初始 0% 预测在二元创建分支被跳过。
MKT046-R2 MEDIUM：时间先平均再评分造成评分对象混淆；晚期预测覆盖整日的假设未披露。
MKT046-R3 MEDIUM：当前题目文本覆盖旧预测导出的原始语义，影响回测与事前证据。
MKT046-R4 MEDIUM：二分量与单分量 Brier 混用，跨产品比较出现 2 倍刻度差。

## 7. 轨道协调及后续

本日 E004 已完成正式日检；最新 R176 增量由 E015 独立只读审计。2026-W44 的 F002 已完成，本轮只新增未来候选案例，不重复开 F 专题。以上均为 R 系列完成前的候选知识储备，不改动冻结协议，不开发个人决策产品，不预设唯一人生效用权重。

下一项 MKT047：继续追踪 Fatebook 的问题修订、结算撤回与评分重算实现，检查题目改写后旧概率是否被重新评分，以及 CSV 导出如何保持可重放性；如缺乏公开源码证据则转向其他开源预测日志。
