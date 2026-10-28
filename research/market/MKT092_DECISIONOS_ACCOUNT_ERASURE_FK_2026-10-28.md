# MKT092 DecisionOS账户删除与外键约束的固定源码审计
日期：2026年10月28日（Asia/Singapore）。范围：商业产品与市场方法研究。证据：MARKET E1，源码及独立合成SQLite重演。主动新增费用0，真实个人数据0。

## 固定来源及新发现
官方英文开源仓库 https://github.com/shafaypro/DecisionOS ，固定提交 `af288e9f1e6c6c097e3eccd30f3b97a85ac22a69`。直接读取：
* `src/app/api/account/route.ts` Git blob `3b72215a694c4848d17e1da34e521da7bbd89c75`
* `prisma/schema.prisma` Git blob `f29af9a7ad8fb8f23a388f46850d1133b4205498`
* `prisma/migrations/20260615000000_init/migration.sql` Git blob `7299bfbfb50dac6c2117cebf8cbae0ccf2593544`
* `tests/integration/account.test.ts` Git blob `810a874149fa3efbc99b0b747ec15bff8159b1c5`
* `prisma/migrations/20260701000000_add_audit_log/migration.sql` Git blob `00c7695211450432531301a8cb3b9ee67e9a8de2`
* `src/lib/audit-log.ts` Git blob `ad6eb0dfd4f6d3b81fe1d1775918c339584c173c`

新增发现：账户删除路由检查“是否为某工作区唯一管理员”，然后直接执行 `prisma.user.delete`。注释声称User子关系全部级联删除。实际正式PostgreSQL迁移中，`Decision_createdByUserId_fkey` 使用 `ON DELETE RESTRICT`；`DecisionNote_userId_fkey`、`DecisionVersion_changedById_fkey` 等多条必需作者关系也使用 `RESTRICT`。因此，在用户已经创建决策或留言、且该记录仍存在的条件下，单独删除User与迁移外键约束冲突。拥有多个管理员也不能解除这个冲突。迁移中的工作区成员关系则为 `CASCADE`。

上游集成测试仅让没有创建决策的co-admin账户删除成功，另外测试唯一管理员被拒绝。测试fixture中的决策由另一个管理员创建，尚未覆盖“删除已经创建决策的非唯一管理员”反例。

独立脚本 `research/market/mkt092_decisionos_account_erasure_fk_20261028.py` 用Python标准库SQLite重演正式迁移的核心约束。14项检查通过：含决策作者删除受限、仅有成员关系者删除成功、留言作者删除受限、删除引用后成功，以及独立AuditLog保留。此为结构等价人工反例，尚未运行真实PostgreSQL、Prisma或完整Web应用，真实接口HTTP响应未知。

另外，账户删除路由在删除成功后追加 `account.deleted` 审计记录。AuditLog刻意不设User外键，含actorEmail、actorUserId、IP、UserAgent等字段。即使主账户删除成功，日志仍可保留可识别信息。代码将其解释为合规审计用途；实际保留期限、必要性和法律依据均未在本轮确认。不能由此判定违法或真实隐私泄露。

## 产品机制矩阵
输入：决策、理由、备选项、假设、风险、标签、成员活动、历史快照、复盘。
状态：Decision当前记录、DecisionVersion快照、DecisionReview、成员权限与审计日志。
算法：结构化CRUD、工作区可见性、关系外键、账户删除守卫；没有取得能证明长期人生效用优化或独立因果推断的源码证据。
目标及反馈：定期复盘、历史修改、结果记录；人工确认与编辑可作为反馈。自动自我修正能力及长期有效性未知。
隐私权限：工作区权限、个人导出、账户删除、审计日志。账户删除完整性存在条件性阻塞，历史日志另行保留。
解释性：保存理由、版本与复盘。MKT089至MKT091已分别检查导出范围、历史显示与可见性边界，本轮只新增删除外键冲突及保留日志边界。
费用：官方MIT开源，自部署可使用现有设备与免费软件；云部署和外部AI服务可能计费，本轮未启用。
局限：未取得真实产品对长期个人决策质量改善的独立实证；本轮没有安装、注册、调用计费API或测试生产数据库。

## 证据分层与未来方法候选
SOURCE E1：固定源码及正式迁移外键；SYNTHETIC E1：14项本地SQLite结构测试；DOCUMENTED CLAIM：账户删除路由的“所有个人数据永久删除”文案；UNKNOWN：生产故障发生率、真实HTTP结果、合规性及用户影响。未来研究候选是把删除前引用图完整性、授权撤销、审计保留目的与删除完成收据分别验证。不可提前开发个人决策产品，也不可预设唯一人生效用权重。

下一轮MKT093可对比另一开源系统的账户删除与派生数据生命周期，避免连续仅研究DecisionOS。
