# MKT025 Exist API v2：OAuth2 授权、属性所有权与数据删除生命周期的边界审查

run_date: 2026-10-25 (Asia/Singapore, UTC+08)
track: commercial_market
subflow: market
status: COMPLETE_BOUNDED_OFFICIAL_DOCUMENT_AUDIT
observed_main_head_before_write: 72398a8be389f887c5c998ac5a0bcb179d072fbe
prior: MKT003（Exist 的日级属性、相关性和断开服务后的保留）；MKT015（Open Humans 的授权与副本）；MKT024（Solid 缓存撤权边界）。
work_performed: 读取 Exist API v2 官方 OAuth2、属性所有权、写入 API、知识库属性停用/删除、手工值清除、隐私政策及价格页面。仅公开英文资料。无账户、令牌、真实数据、API 请求、服务器、付费、CI。
ci_status: NOT_RUN
billing_checked: active_new_cost=0; account_total_billing_and_free_quota=NOT_INDEPENDENTLY_VERIFIED
output_paths: 本文件
commit_sha: GitHub 写入后通过提交和远端文件回读核验；不在预提交文件中伪填。

## 1. 相对 MKT003 的真实增量

MKT003 已记录日级属性、相关性、OAuth 组级 scope、断开集成服务不清除旧数据。此次新增的是**属性写入所有权的独立状态、属性类型决定删除能力、已写入单日值无法复原为空、备份与第三方处理器的保留边界**。没有证据表明 Exist 在本轮发布了新版本；属于现有机制深读。

### F1 OAuth2 权限与属性所有权是两个不同的条件
[MARKET-E1 OFFICIAL_API_REFERENCE]

Exist API v2 的 OAuth2 access token 按 activity、mood、sleep、finance、health、location 等组分别提供 read/write scopes；文档明确要求最小 scope。只有具备写 scope 仍不足以更新某个属性，写入服务还必须 acquire 该属性的 ownership。同一用户属性同时只由一个服务拥有写入权。用户可在属性页面更换服务。

`POST /api/2/attributes/acquire/` 可获得属性所有权，若模板属性尚不存在还会创建属性。官方文档特别说明这一动作**无需用户再次逐项批准**，并建议集成应用自行向用户说明。由此可提出候选风险：OAuth 授权与属性接管的用户可见性不同；不能推断已经越权或违反某一法域法律。

`POST /api/2/attributes/release/` 可释放写入所有权。若其他已连接服务能提供该属性则转交；否则属性变为 inactive。release 不是删除历史数据，也不能等同于 OAuth 撤权。acquire/release 单批最多 35 项；官方示例对部分失败返回 HTTP 202，必须检查 success/failed 项，不能只凭 2xx 认定全部完成。

官方 OAuth2 access token 约一年过期，可用 refresh token 续期并轮换原令牌；简单 read-only token 被官方文档描述为不自动过期。官方概述称不同 OAuth2 客户端各自有可撤销令牌，但本轮未获得独立撤销后的 HTTP 401、刷新令牌失效及会话传播实测。

### F2 数据删除能力依属性类型不同
[MARKET-E1 OFFICIAL_KNOWLEDGE_BASE]

2024-03-13 更新的官方帮助文档指出：来自集成服务的属性，以及由官方模板创建的手工属性，**不能单独删除**，可以 inactive 隐藏，原属性和历史值继续保留；用户自定义的标签与手工属性可以永久删除，相关数据一并删除。

2026-08-26 更新的官方帮助文档指出：手工属性在某日一旦有非空值，无法将该日值单独清除为“未记录”；可以覆盖成另一个值，例如将 1 改为 0。API v2 写入参考也明确，`POST /api/2/attributes/update/` 不允许把非 null 改回 null。这里的 0 代表真实零值，不等于未知、撤回或未采集。

因此，未来任何个人状态数据设计应区分 `not_observed`、`observed_zero`、`redacted`、`inactive`、`deleted`、`retained_in_backup`。此处仅为候选方法字段，未写代码或接入个人数据。

### F3 断开来源、释放写入权、隐藏、删除属性、关闭账户各有不同结果
[MARKET-E1 OFFICIAL_HELP_AND_PRIVACY_POLICY]

官方说明：断开集成服务后停止未来同步，既有数据继续保留；其他服务可能接管数据来源。释放属性写入权同样允许其他服务接管。停用属性仅隐藏。自定义手工属性可删除。关闭账户的官方帮助文档宣称删除账户中的用户数据，隐私政策同时保留备份与归档所需的“商业上合理期限”，并允许保留会计、支持往来及已公开/被复制的信息。

**文档张力：** 官网价值页面的“永久删除”描述针对 Exist 主数据库，隐私政策明确存在备份/归档、第三方及法定留存例外。未找到明确备份清除天数或衍生相关性删除传播的可执行证明，记录为 UNKNOWN；不能把“账户关闭”升级为全域零副本的已验证事实。

### F4 数据处理器与日志形成额外副本边界
[MARKET-E1 OFFICIAL_PRIVACY_POLICY]

官方隐私政策列出支持邮件、支付记录、地理位置服务、邮件营销及错误监控处理器。其错误监控说明可能在崩溃日志中包含用户属性相关数据。该表述只证明厂商公开披露的数据流，未实测处理器实际收到的字段、访问权限、留存期限或删除行为。对未来个人量化模型，候选方法是将诊断日志、导出副本、派生统计和备份分别列入数据生命周期账本，避免将原始表删除误判为所有副本删除。

### F5 产品定位、反馈、费用和科学验证边界
[MARKET-E0/E1]

输入：第三方集成数据、手工属性、按用户本地日期记录的值；状态：属性名、组、active、owner/source、date、value、OAuth scopes；算法：本轮审查范围仅包括权限与写入接口，既有 MKT003 记录的相关性统计属于描述性功能。目标：个人观察、相关性反馈与习惯追踪，未公开唯一人生效用函数。反馈与修正：可以改写日级值、替换数据来源、切换 active；这不证明因果建议自我修正或自动改进预测模型。解释性：用户可见属性来源、相关性说明和 API 字段；删除传播与权限撤销的实际审计日志尚未验证。费用：官网 2026-10-25 公开个人 $6.99/月或 $62.90/年、30 天试用；本研究没有注册试用或购买。

没有用户真实数据的独立预测测试、因果效果评估、长期个人决策收益实验。厂商隐私承诺与 API 文档均为 MARKET-E1 或 E0，不是 R 系列 E2/E3。

## 2. 风险与候选验证（未执行）

R1 属性所有权变化可能在 OAuth 组级许可范围内无需单独用户确认。候选验证：合成用户授权后的 acquire/release 事件、可见通知、拒绝后是否仍能写入，分别检查。
R2 非空日值无法改回 null。候选验证：区分未知、真实零、撤回和覆盖更正的状态迁移；不能以 0 冒充删除。
R3 inactive 与断开服务保留历史。候选验证：分别审计 API 可见性、统计计算是否继续引用、用户界面隐藏状态；目前 UNKNOWN。
R4 关闭账户后的备份、处理器、支持邮件及派生统计的清除周期不明确。候选验证：按数据位置登记所有者、删除触发、保留期限、核验方法和例外。
R5 OAuth 撤销后 access token、refresh token、客户端缓存是否失效未独立执行。候选验证：撤销前后新请求、刷新尝试及日志审计；不接入真人账户。
R6 产品的相关性和星级统计不构成个人长期决策改善的因果证据。维持 MKT003 的独立未来时段预测、时间自相关和多重比较审计待办。

## 3. E 当日治理增量（只读，不重复 E002/E003）

E002 与 E003 在 2026-10-25 已完成正式实质审计；本轮读取新增 R149、B 审计、A 数据侦察、TH028 提交与原始239 v7.8 文件元数据。R149 事前冻结提交 `bca1a42472536dc585179858da66c25862cd3bbc`，之后出现第三方法源码、精确收据与 B 独立方法报告 `916679ea594d3b270dd9f440d44203d4d167c828`。B 报告记录五状态树权重精确比对、256 步 survival 级数尾界与错误突变负对照，属于项目内部数学 E1；本轮没有独立运行脚本。直接查询 B 报告 SHA 和 R149 科学收据 SHA `ec3c9820b1b0c91f426076b41cff6c8a6b498ba5` 的 Actions REST head_sha，均返回 total_count=0，不能把既有历史 CI 套用至这两个新增提交。

A 轨 Cooper/Kagel 2023 openICPSR 数据仅核实公开存档元数据，直接原始行数据仍受 HTTP403 阻塞，未形成 R073 冻结迁移或新的真人 E2。TH028 已新增理论笔记及索引，未独立审查其学术来源。原始239 v7.8 文件存在，前部 schema/date 仍保留 v7.6/2026-10-24 元数据；既有 E003 登记的 154 项逐项证据审计队列仍开放，本轮未重新逐行复算。R136 历史冻结负对照失败、R074/R075 旧证据标签冲突和全仓冻结哈希审计仍为已登记问题，未修改其他轨文件或索引。

已检查最近提交没有本轮目标路径的同名文件。E 只读、没有发起 CI。未验证 GitHub 账户全部账单或全仓每条提交的费用、权限、冻结哈希，不能宣称全仓合规完成。

## 4. F 本周专题状态

2026-W43 的 `research/privacy_safety/F001_HUMAN_OVERRIDE_AND_DATA_MINIMIZATION_2026-W43.md` 已完成。本轮没有重复生成 F 文件。下周 F002 候选专题进一步加入“数据类型决定删除能力”“非空日值不能恢复缺失”“OAuth scope 与属性 ownership 分离”“备份和诊断日志留存”。F002 本周仍为 PENDING，未提前记为完成。

## 5. 公开英文来源与证据等级

S1 API v2 OAuth2 scopes、access/refresh token：https://developer.exist.io/reference/authentication/oauth2/
S2 属性 acquire/release/owned：https://developer.exist.io/reference/attribute_ownership/
S3 写入值和不可恢复 null：https://developer.exist.io/reference/writing_data/
S4 删除与停用属性（2024-03-13）：https://kb.exist.io/article/99-how-can-i-delete-or-deactivate-an-attribute
S5 手工值不可清除（2026-08-26）：https://kb.exist.io/article/116-can-i-remove-a-value-for-a-manual-attribute
S6 断开服务保留数据：https://kb.exist.io/article/21-what-happens-when-i-disconnect-a-service
S7 隐私政策、备份和第三方处理器：https://exist.io/privacy/
S8 关闭账户说明：https://kb.exist.io/article/4-how-do-i-close-my-account
S9 当前价格和数据价值声明：https://exist.io/about/values/
S10 API 简单令牌说明：https://developer.exist.io/reference/authentication/token/
S11 本项目 MKT003：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/market/MKT003_EXIST_DAILY_LAG_SIGNIFICANCE_DATA_LIFECYCLE_2026-10-24.md
S12 E003：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/operations/E003_R136_FROZEN_NEGATIVE_CONTROL_INCIDENT_DELTA_2026-10-25.md
S13 F001：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/privacy_safety/F001_HUMAN_OVERRIDE_AND_DATA_MINIMIZATION_2026-W43.md
S14 B R149：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/B_R149_STATIONARY_TREE_SURVIVAL_INDEPENDENT_E1_SCIENTIFIC_AUDIT_2026-10-25.md
S15 A Cooper/Kagel：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/data_scout/COOPER_KAGEL_2023_OPENICPSR_176881_TEAM_VS_INDIVIDUAL_PD_SOURCE_GATE_2026-10-25.md

source_scope: OFFICIAL_PRODUCT_DOCS + OFFICIAL_API_REFERENCE + EXISTING_PROJECT_RECORDS. 仅文档审计，无产品实测、外部独立复现、真人 E2 或历史 E3。
blockers: no authenticated account testing by zero-cost policy; deletion propagation and OAuth revocation HTTP behaviour unknown; GitHub Actions free quota not checked; original239 audit queue remains open.
next_action: MKT026 审查 Exist API v2 细粒度 OAuth scope 与属性 ownership 在服务替换、数据可见性、inactive 过滤中的边界，或轮换到 ProjectionLab 的情景输入敏感性，优先选择此前记录未覆盖且有官方可核查依据的机制。E 下次仅核对新提交与未结项；F002 下周独立专题研究数据生命周期。保持先完整 R 系列，再系统归纳，最后模型熔炼。
