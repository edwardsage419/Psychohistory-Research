# F009第五阶段：删除审计元数据最小化与离线副本复活防护

日期：2026-10-30 UTC，2026-W44。目标键：(privacy_safety,F009,phase5,minimal-receipt-retention-and-stale-replica-resurrection)。状态：COMPLETE_BOUNDED_ARTIFICIAL_E1。本专题是未来个人决策模型的候选安全知识储备，未开发产品，未接入真实敏感信息。

## 英文官方来源与适用边界

英国ICO《Right to erasure》：https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/individual-rights/individual-rights/right-to-erasure/ 。其公开指导要求对删除请求建立处理流程、通知相关接收方，并明确说明备份数据的处理边界；备份不能立即覆写时可能需要采取beyond use隔离措施。该指导提示正在因2025年法律变化接受复核，不将其视为所有法域的普遍强制规则。

英国ICO《Storage limitation》：https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/storage-limitation/ 。说明不必要的长期保留会增加隐私与误用风险。NIST Privacy Framework：https://www.nist.gov/privacy-framework/privacy-framework 。作为风险治理原则来源。

已读F009第一至四阶段记录：设备删除确认、Syncthing历史归档、restic备份引用与prune证据。第五阶段单独研究删除请求审计所需最少元数据与长时间离线设备重新出现之间的冲突。

## 候选最小收据

候选字段：随机不透明case token、删除epoch、已知设备集合及各设备确认epoch与verified状态、未知副本计数、历史归档清理状态、备份仍引用计数、prune证据、法律保留状态、审计收据过期时刻。避免把姓名、原始活动文本、健康或财务内容直接放入审计记录。case token和设备清单仍可能构成可关联的个人信息，需要独立授权、访问控制和明确到期策略。未经密钥保护的可预测标识哈希可能被字典攻击，不能宣称“不可逆摘要”就等于匿名化。

收据生命周期与删除防复活状态应分开管理。若审计收据过期而仍存在未确认离线设备，重连旧数据需要隔离并重新取得有效权限与删除状态证据。只因审计元数据到期就自动接受旧副本会重新暴露已删除内容；无限期保存完整个人信息同样有风险。到期后应保留最低必要的安全阻断能力，并明确依据、保留期限和复核责任，具体期限不能由本人工实验预设为普遍合规值。

## 人工故障注入与实际执行

归档JavaScript：research/privacy_safety/f009_minimal_receipt_resurrection_gate_20261030.js，Git blob ca45749077b3c26df20fe69f99c4d485af68f113。三设备phone/laptop/tablet，删除epoch=7，候选收据到期时刻30，全部为无身份的人工整数。

正常三设备确认、无未知副本、归档已清、备份引用0且prune核验时，仅返回MODEL_SCOPE_COMPLETE。平板离线确认停留epoch5，返回PENDING_DEVICE；同一旧内容重连被REJECT_STALE_OR_REVOKED。到时刻31审计收据过期，旧内容改为QUARANTINE_EXPIRED_AUDIT。未知副本、备份仍被引用、归档未清、法律保留、prune缺失均不能通过。epoch8的新内容没有可核验重新授权时隔离；即使标记verified_new_grant也只返回候选状态，仍需要实际密码学签名与权限验证。

程序从远端重新读取后在隔离V8运行：12项正向状态断言通过，5项非法输入拒绝。没有执行真实设备同步、签名校验、密钥擦除、物理数据销毁或外部渗透测试。MODEL_SCOPE_COMPLETE只表示本人工字段合同检查通过，不构成实际删除完成或合规证明。证据E1人工、内部非盲态，真人安全E2=0、历史E3=0、外部审计0。

## 风险登记与下一项

F009-05A：审计元数据过多，造成二次隐私暴露。候选控制为最小字段、独立访问权限、明确到期和理由记录。
F009-05B：过早删除阻断证据，离线旧副本重新进入。候选控制为过期未知状态隔离、重连授权核对与删除epoch检查。
F009-05C：伪造设备确认或伪造重新授权。当前人工布尔verified未验证真实性，未来必须单独检查签名、设备身份和完整设备清单。
F009-05D：第三方备份与法律保留。需明确数据处理者、合同、地域法律和具体到期依据，不能由人工状态机保证。

本轮零新增费用，没有安装或购买产品，没有调用收费API或GitHub Actions。账单与免费额度NOT_VERIFIED。

下一F009第六阶段：研究最小审计记录中的设备身份轮换、丢失设备与合法重新授权的冲突，优先官方开放标准和人工反例。