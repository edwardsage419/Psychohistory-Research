# MKT039 DecisionOS 决策复查历史、导出信息损失与证据来源审计

run_date: 2026-10-26 Asia/Singapore
track: market
subflow: product
status: COMPLETE_BOUNDED_FIXED_SOURCE_INSPECTION_AND_SYNTHETIC_CHECKS
observed_main_head_before_write: 4c585cfcd2b2ce7dbee213400c0e55e5e1310dd3
upstream: shafaypro/DecisionOS
upstream_fixed_commit: af288e9f1e6c6c097e3eccd30f3b97a85ac22a69
evidence: SOURCE_CODE_MARKET_E1 + AUTHOR_DOCUMENTATION_E1 + INDEPENDENT_SYNTHETIC_E1
real_deployment_test: NO
real_human_outcome_evidence: NO
new_remote_ci: NOT_TRIGGERED
new_cost: ZERO_ACTIVE_SPEND; billing and free-quota entitlement not independently verified

## 1. 去重与研究问题

读取本项目 main HEAD、MKT038、E007、F002、当日新 R169 与 TH042 提交。MKT038 已审查质量评分和邮件一键复查语义。本轮继续同一固定上游版本，研究此前未验证的具体机制：DecisionVersion、DecisionReview、DecisionEvent 的记录边界，以及 CSV、JSON、Markdown、个人账户导出对历史的保真度。当前固定提交的发现属于新增审查结果，不声称 2026-10-26 发生产品更新。检索只使用英文官方源码、英文技术文档与 W3C 原始规范。

## 2. 产品输入、状态、反馈、权限和费用

输入包含问题、备选、选择、理由、假设、风险、负责人、复查时间、链接与标签。Decision 保存当前 outcomeStatus、reviewedAt、reviewDate。DecisionReview 逐条保存复查者、结果枚举、总结、教训、后续行动、创建时间。DecisionVersion 保存编辑前的 snapshotJson、versionNum、编辑者、时间。DecisionEvent 保存特定变更事件。PUT 编辑路径将更新、编辑前快照和事件置于数据库事务；人工复查 POST 路径创建 Review、更新当前结果并创建 reviewed 事件；邮件 GET 路径另有一键写入流程。

目标是组织内的结构化决策记录和事后复查。未发现固定版本提供事前预测概率与客观结果来源之间的标准化校准评分，也未发现多目标人生效用的已验证机制。系统可自托管、MIT 开源，软件本身无席位收费；实际托管、邮件、AI 服务、数据库及运维可能产生费用。本轮没有部署或使用这些资源。

访问控制：决策导出仅包含当前会话可见的工作区记录和本人私有记录，单项版本接口检查可见性；个人账户导出是另一独立作用域。源码检查仅证明所读路径的意图和静态逻辑，未完成真实租户渗透测试。

## 3. 发现 A：版本历史和复查历史是两种独立记录

固定源码 `src/app/api/decisions/[id]/route.ts` 在 PUT 时为编辑前 Decision 生成 DecisionVersion；`src/app/api/decisions/reviews/route.ts` 在 POST 复查时新增 DecisionReview、更新 Decision.outcomeStatus 并写入 DecisionEvent，该 POST 路径未调用 DecisionVersion.create。邮件复查 GET 也创建 Review 和 Event，未创建 DecisionVersion。

因此，查询版本接口只能取得通过该 PUT 路径记录的编辑前快照；单靠版本时间线无法恢复每次复查。Review 表能恢复已保存的复查结果和文本，但需要与版本、事件、当前状态联合解释。源码支持这一路径级结论，尚未证明所有其他修改路径都有同等覆盖。

`prisma/schema.prisma` 的 DecisionVersion 对 (decisionId,versionNum) 未声明复合唯一约束，PUT 先计数再创建版本。注释称事务避免并发编号冲突；数据库事务并不自动等于在所有并发执行下具有唯一递增编号。本轮未运行并发测试，因此只登记为需要验证的假设，不能宣称实际产生重复编号。

## 4. 发现 B：三种工作区导出具有不同的信息损失

直接审查 `src/app/api/decisions/export/route.ts` 和 `src/lib/decision-export.ts`：

* CSV 导出 23 列，包含当前 Outcome、Reviewed At、Reviews Count，未包含逐条复查结果、DecisionVersion 或 DecisionEvent。两段不同的复查历史可以产生相同 CSV 行。
* JSON 导出有 schemaVersion=1、当前决策字段、tags、links 和 reviews；每条 review 包含 outcomeStatus、summary、lessonsLearned、followUpAction、reviewedBy 名称、createdAt。JSON 工作区导出未包含 DecisionVersion、DecisionEvent，也未序列化 review 主键及 reviewer 用户 ID。不同编辑历史可能产生相同 JSON。名称不能替代稳定身份。
* Markdown 包含当前状态、推理字段和 Outcome reviews 的文字时间线；未序列化 DecisionVersion、DecisionEvent 或稳定复查记录 ID。Markdown 适合阅读和 ADR 归档，不能据此声称可完整重放。
* `GET /api/account/export` 的个人账户导出确实包含关联的 decisionVersions、events、reviews 等，密码哈希被排除；它按登录账户及其关联数据组织，无法直接等同于完整工作区决策历史导出。
* `GET /api/decisions/[id]/versions` 是另一可见性检查后的版本读取接口。导出格式的限制不意味着数据库中相应历史一定丢失；意味着单份导出文件缺少重建所需的部分字段。

这构成“可迁移的当前记录”和“可完整重建决策证据链”之间的可验证区别。官方 README 将 JSON 称为备份和迁移格式，属于作者对预期用途的说明；完整历史可恢复性仍需明确验收协议。

## 5. 发现 C：重新安排复查时可能保留上次结果标签

`src/app/api/decisions/[id]/route.ts` 对新的 reviewDate 采用规则：当新日期晚于上次 reviewedAt 时，将 reviewedAt 置为 null 以重新安排复查。此代码路径没有同步清空 outcomeStatus。`src/lib/trends.ts` 的 outcomeMix 直接统计当前 outcomeStatus，已知结果中 successful 的占比进入 successRate，unknown 被排除。

因此，一个决策可以同时处于“下一次复查尚未完成”和“当前标签仍为 successful”的状态。这可能是保留历史结果的有意设计；在未来将 successRate 解释为“当前最新复查已完成且成功的比例”时会造成口径混淆。源码静态分析支持状态组合的可达性推断，尚未执行产品端到端操作。

## 6. 独立合成反例与可复算边界

本轮使用 Python 3 标准库实现与固定源码字段投影一致的简化人工序列化，执行 10 项断言，10 项通过，0 失败。仅证明所审查字段选择导致的数学信息损失，没有调用上游 TypeScript、数据库或产品 API。

人工情景 A 与 B：当前决策和复查记录完全相同，历史编辑快照的 rationale 分别为 A 和 B。版本接口投影不同，工作区 CSV 与 JSON 投影完全相同。

人工情景 C 与 D：当前 outcomeStatus 同为 successful，复查次数同为 2，但第一条复查结果分别为 mixed 与 unsuccessful。CSV 投影相同，JSON 复查数组不同。

人工情景 E 与 F：复查文字、时间与结果相同，复查记录主键和 reviewer 用户 ID 不同。固定 JSON 导出字段投影相同。

另验证：reviewedAt=null 与 outcomeStatus=successful 可以同时存在；该状态仅是静态路由规则下的合成可达状态。

十项检查包括版本不同、CSV 对版本不可区分、JSON 对版本不可区分、复查序列不同、CSV 对复查序列不可区分、JSON 保留复查结果差异、复查元数据不同、JSON 忽略主键及用户 ID、复查重新排期保留旧结果、版本读取区分历史。所有结论限定于这些构造的人工反例。

## 7. 科学证据等级与候选方法

SOURCE_CODE_MARKET_E1：固定提交的 schema、PUT、复查 POST、邮件 GET、版本 GET、工作区导出、个人导出、序列化、trends。
AUTHOR_DOC_MARKET_E1：README、docs/API.md、docs/SETUP.md 对功能和用途的描述。
INDEPENDENT_SYNTHETIC_E1：10 项本地纯 Python 断言。
NORMATIVE_PRIMARY：W3C PROV-O 推荐规范将 Entity、Activity、Agent 及派生、生成、责任联系作为来源表达工具；这不是 DecisionOS 合规认证，也不证明个人决策效果。
MARKETING_E0：改善决策质量或学习成效等尚无独立真人实验验证。
E2 新增=0；E3 新增=0；独立真实产品运行=0；外部研究团队复现=0。

候选方法：
MKT039-C1 分离“决策原始版本”“主观复查”“客观结果”“结果来源”“用户偏好版本”“预测概率”和“观察截止时间”。
MKT039-C2 对可用于模型训练的结果标签记录稳定 review ID、actor ID、证据 ID、事件发生时间、记录时间和来源类型；允许更正与申诉，保留纠错链。
MKT039-C3 导出格式分别声明 CURRENT_STATE、REVIEW_HISTORY、EDIT_HISTORY、EVENT_PROVENANCE 的覆盖率；未包含的历史应显式标记。
MKT039-C4 复查重新排期和结果统计需区分“上一观察期已成功”和“本期结果待定”，避免以单一成功率混淆。
MKT039-C5 W3C PROV-O 只作未来证据链候选参考；不得在 R 系列完成前熔炼模型或预设唯一人生效用权重。

## 8. E/F 状态、阻塞与下一轮

E：当日正式 E004 和增量 E005 至 E007 已存在。本轮核查新 R169 第三方法冻结和独立 B 轨，另形成 E008 只读增量；不修改 R/A/B/C/D/TH/F 或共享索引。
F：2026-W44 F002 已完成授权撤销与衍生数据生命周期专题，本轮不重复创建。将“导出遗漏来源链”“姓名非稳定身份”“复查重新排期的旧结果标签”加入未来 F003 候选风险。
阻塞：真实 DecisionOS 数据库、授权端到端实验和实际迁移恢复均未运行；零新增费用约束禁止启动可能计费资源。GitHub Actions 未启动，账户账单未独立核验。
下一轮 MKT040：优先检查 Exist 或其他官方个人量化产品的跨源相关性、滞后窗口、缺失数据和反馈闭环；先核对既有 market 是否已覆盖同一机制。保持先全部 R 系列、再统一分类、最后熔炼。

## 9. 非中文来源

1. https://github.com/shafaypro/DecisionOS/blob/af288e9f1e6c6c097e3eccd30f3b97a85ac22a69/prisma/schema.prisma
2. https://github.com/shafaypro/DecisionOS/blob/af288e9f1e6c6c097e3eccd30f3b97a85ac22a69/src/app/api/decisions/%5Bid%5D/route.ts
3. https://github.com/shafaypro/DecisionOS/blob/af288e9f1e6c6c097e3eccd30f3b97a85ac22a69/src/app/api/decisions/reviews/route.ts
4. https://github.com/shafaypro/DecisionOS/blob/af288e9f1e6c6c097e3eccd30f3b97a85ac22a69/src/app/api/decisions/review-action/route.ts
5. https://github.com/shafaypro/DecisionOS/blob/af288e9f1e6c6c097e3eccd30f3b97a85ac22a69/src/app/api/decisions/%5Bid%5D/versions/route.ts
6. https://github.com/shafaypro/DecisionOS/blob/af288e9f1e6c6c097e3eccd30f3b97a85ac22a69/src/app/api/decisions/export/route.ts
7. https://github.com/shafaypro/DecisionOS/blob/af288e9f1e6c6c097e3eccd30f3b97a85ac22a69/src/app/api/account/export/route.ts
8. https://github.com/shafaypro/DecisionOS/blob/af288e9f1e6c6c097e3eccd30f3b97a85ac22a69/src/lib/decision-export.ts
9. https://github.com/shafaypro/DecisionOS/blob/af288e9f1e6c6c097e3eccd30f3b97a85ac22a69/src/lib/trends.ts
10. https://github.com/shafaypro/DecisionOS/blob/af288e9f1e6c6c097e3eccd30f3b97a85ac22a69/docs/API.md
11. https://www.w3.org/TR/prov-o/
