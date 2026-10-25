# MKT038 DecisionOS 决策记录完整度、结果标签与邮件复查语义审计

run_date: 2026-10-26 Asia/Singapore
track: market
subflow: product
status: COMPLETE_BOUNDED_FIXED_SOURCE_AUDIT_AND_SYNTHETIC_CHECK
observed_main_head_before_write: 7cf0864fdf4a655b53c20612579ce02eac98b1a0
upstream_repository: shafaypro/DecisionOS
upstream_fixed_commit: af288e9f1e6c6c097e3eccd30f3b97a85ac22a69
evidence: SOURCE_CODE_MARKET_E1 + AUTHOR_DOC_MARKET_E1 + INDEPENDENT_SYNTHETIC_E1
real_product_run: NO
remote_ci_triggered: NO
new_cost: ZERO_ACTIVE_SPEND; account billing and free quota not independently checked

## 1. 选题与去重

开始前读取本仓库 main HEAD、market 目录 MKT001 至 MKT037、MKT035 至 MKT037 正文、E006、F002 和最新 R168/A 轨提交。MKT035 至 MKT037 集中在 Decision Journal 的长期记忆与备份。本轮选择不同真实开源产品 DecisionOS，研究此前未覆盖的“记录质量分数”和“复查结果标签”之间的逻辑关系。上游固定 commit 是已公开版本，本次发现指新增研究观察，不代表软件刚发布更新。非中文来源限定英文官方仓库与固定源码。

## 2. 产品输入、状态、算法、目标、反馈

DecisionOS 是面向团队的自托管决策记录系统，README 声称 MIT、免费、无按席收费；本轮读取了其 MIT LICENSE 存在性及官方 README/CHANGELOG/SECURITY。开发环境使用 SQLite，生产环境可配置数据库。可选 AI 起草和问答需要模型密钥，邮件/云部署可能带来第三方费用，故本研究仅免费只读源码，没有部署、配置模型、邮件或启动 CI。

输入字段包括 title、summary、problemStatement、chosenOption、rationale、alternativesConsidered、assumptions、risks、owner、reviewDate、links、tags。状态包括 draft/proposed/in_review/approved 等工作流状态，outcomeStatus 则取 unknown/successful/mixed/unsuccessful；DecisionReview 记录 reviewer、summary、lessonsLearned、followUpAction、时间，DecisionVersion 记录每次编辑的 snapshotJson。系统支持搜索、决策依赖图、导出 CSV/JSON/Markdown、历史版本和复查提醒。没有发现事前数值概率、客观结果标注规范、因果反事实或长期个人效用权重的已验证模型。系统的“质量分数”意在衡量记录可读性，不等同于决策正确率。

## 3. 新增发现 A：100 分记录质量不要求任何结果验证

固定源码 `src/lib/decision-quality.ts` 给 rationale 20、alternatives 18、problem 12、chosenOption 10、assumptions 10、risks 8、owner 8、reviewDate 6、summary 4、links 2、tags 2，合计 100 分。文本字段只看 trim 后字符长度，>=40 给满分，1 至 39 字符给一半分；布尔存在性给满分。其输入类型与计分规则没有 outcomeStatus、真实结果证据、概率预测质量或来源可信度。作者测试 `tests/smoke/decision-quality.test.ts` 明确验证“填满所有字段得100分”“短文本得半分”“40字符达到深度阈值”。

独立 Python 3 标准库重写这一局部规则，执行七项人工断言。结果：全字段填入重复的40字符无语义文本得到100分；在完全相同字段上分别设置 outcomeStatus=successful 与 unsuccessful，均得到100分；只有标题时0分；仅有 `rationale='because'` 得10分；11项权重合计100。此为逻辑反例，说明字段完整度和结果有效性必须分轴。该实验未执行产品 TypeScript 测试或真实 UI，不能宣称实际用户使用了无意义文本。

## 4. 新增发现 B：邮件“一键仍有效”会写入“成功”结果

`src/app/api/cron/review-reminders/route.ts` 在到期时发送两种签名链接：Still valid 与 Assumptions changed。 `src/lib/review-token.ts` 使用 HS256、七天有效的 token，载有 decisionId/userId/action。 `src/app/api/decisions/review-action/route.ts` 在 GET 请求中验证 token，然后将 action=valid 映射为 outcomeStatus=successful，将 changed 映射为 mixed，写入 DecisionReview、Decision.outcomeStatus、reviewedAt 与审计事件。独立人工逻辑断言复现了两个映射。

“前提仍然有效”与“决策最终结果成功”在语义上并不等价。例如决策方案仍合理而结果尚未观察到时，点击 Still valid 会产生 successful 标签。若下游将 outcomeStatus 直接用作客观成功标签，可能污染评价样本。此为固定源码支持的标签语义风险，尚无真实部署中实际发生污染的独立证据。该 GET 路径具有写入副作用；邮件客户端或安全扫描器的预取行为是否会触发，需在授权测试环境核验，本轮没有进行外部攻击或产品网络测试。

普通人工复查 POST `src/app/api/decisions/reviews/route.ts` 使用明确 outcomeStatus 枚举，并保存文字说明；与一键邮件简化路径需区分。 `prisma/schema.prisma` 的 DecisionReview 没有数值化事前概率与可独立核验的结果来源字段。本轮不推断作者有意把“仍有效”伪装为实证成功。

## 5. 隐私、权限、解释性、费用和边界

官方 README 说明团队 workspace、作者私有记录、可撤销的公开分享链接和账户数据导出；源码的 reviews route 使用 visibleDecision 检查可见性。旧版本隐私缺陷和修复由作者 ROADMAP 描述，属于作者审计记录，未进行外部渗透测试。公开分享与自托管部署有不同的安全责任。可选 AI 的成本取决于所用提供商；软件 MIT 免费不代表部署、邮件或 AI 免费。当前项目禁止启动可能计费的部署、CI、API 和新增订阅。

AUTHOR_DOC_MARKET_E1：README、CHANGELOG、ROADMAP 的产品说明及作者自测声明。
SOURCE_CODE_MARKET_E1：固定提交 decision-quality.ts、review-token.ts、review-action/route.ts、reviews/route.ts、review-reminders/route.ts、schema.prisma 与作者测试。
INDEPENDENT_SYNTHETIC_E1：本地 Python 重建局部规则并执行七项断言；不能等同于真实系统端到端测试。
MARKETING_E0：改善团队决策质量、长期判断提升等效果性描述尚无独立真人评价。
E2 HUMAN=0；E3 HISTORICAL=0；INDEPENDENT_REAL_DEPLOYMENT=0。

## 6. 对心理史学的候选方法

MKT038-C1：将“记录完整度”“前提仍有效”“实际结果”“预测校准”“事后后悔”“偏好变更”分别存储、分别评价。
MKT038-C2：事前概率与事件的可核验结果、观察期限和结果来源独立版本化；未到观察期不得因仍有效而记成功。
MKT038-C3：人为复查、邮件一键复查、外部证据复查使用不同来源标记；不能混合当作同质标签训练。
MKT038-C4：对有副作用的链接设置明确的用户确认和幂等语义，预取风险需在合成授权环境验证。
MKT038-C5：偏好权重必须保持可变、可争议和多目标；这些候选方法仅作知识储备，不开发个人决策产品，不修改任何冻结 R 协议。

## 7. E/F 及下一轮

E 2026-10-26：E004 完成日检，E005/E006 为只读增量；本轮另查 R168 冻结先于执行，最新 R168 第三方法与 B 轨参数盲复核均为内部 E1，指定提交未发现关联 Actions；A 轨168386行复合真人数据仅由公开文档声明，二进制和 session ID 尚未核实。另存 E007，不修改 R/A/B 研究轨。
F 2026-W44：F002 已完成本周专题，不重复立项。本轮新增候选风险：自动把“仍有效”记为“成功”、GET 复查副作用、完整度分数被误当作真实决策正确率；留待后续独立安全专题。
下一轮 MKT039：优先深读 DecisionOS 版本历史、结果标签更新及导出数据的可追溯性，检查同一决策多次复查是否可能覆盖汇总标签且无法从单行导出恢复历史；若证据不足，转向 Decidr 的真实源码与预测反馈闭环。继续 R 系列优先、完成后分类、最后熔炼。

## 8. 非中文原始来源

1. https://github.com/shafaypro/DecisionOS/tree/af288e9f1e6c6c097e3eccd30f3b97a85ac22a69
2. https://github.com/shafaypro/DecisionOS/blob/af288e9f1e6c6c097e3eccd30f3b97a85ac22a69/src/lib/decision-quality.ts
3. https://github.com/shafaypro/DecisionOS/blob/af288e9f1e6c6c097e3eccd30f3b97a85ac22a69/tests/smoke/decision-quality.test.ts
4. https://github.com/shafaypro/DecisionOS/blob/af288e9f1e6c6c097e3eccd30f3b97a85ac22a69/src/app/api/decisions/review-action/route.ts
5. https://github.com/shafaypro/DecisionOS/blob/af288e9f1e6c6c097e3eccd30f3b97a85ac22a69/src/app/api/cron/review-reminders/route.ts
6. https://github.com/shafaypro/DecisionOS/blob/af288e9f1e6c6c097e3eccd30f3b97a85ac22a69/src/lib/review-token.ts
7. https://github.com/shafaypro/DecisionOS/blob/af288e9f1e6c6c097e3eccd30f3b97a85ac22a69/src/app/api/decisions/reviews/route.ts
8. https://github.com/shafaypro/DecisionOS/blob/af288e9f1e6c6c097e3eccd30f3b97a85ac22a69/prisma/schema.prisma
9. https://github.com/shafaypro/DecisionOS/blob/af288e9f1e6c6c097e3eccd30f3b97a85ac22a69/docs/ROADMAP.md
