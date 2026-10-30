# F009第七阶段：可同步通行密钥备份状态与计数器异常

日期UTC：2026-10-30，2026-W44。目标键：(privacy_safety,F009,phase7,backup-flags-signcount-race-risk)。初始main HEAD：22c7651851cd32b5dab1800df8a6094b5e8b8dde。状态：COMPLETE_BOUNDED_ARTIFICIAL_E1。仅候选安全研究，不接入敏感数据或开发个人决策产品。

## 英文一手标准

W3C WebAuthn Level 3，https://www.w3.org/TR/webauthn-3/ ，2026-10-30阅读备份状态和签名计数器章节。BE表示备份资格且创建后不可变；BS可以改变；BE=0/BS=1是非法组合。签名计数未增长可能提示克隆、设备故障或并发乱序，单独不足以证明克隆。零计数器无法提供可靠的递增证据。

NIST SP 800-63B-4，https://pages.nist.gov/800-63-4/sp800-63b.html ，2026-10-30阅读同步认证器附录。同步密钥可导出，AAL3要求不可导出；同步备份需加密、访问控制及适当恢复机制。此为候选设计参考，未开展NIST符合性评估。

## 原生Node人工测试

归档脚本research/privacy_safety/f009_passkey_backup_counter_risk_phase7_20261030.js，Node.js v22.16.0执行18项断言与非法输入拒绝，exit=0。全部为虚构布尔字段及整数。

| 条件 | 人工分类 | 风险边界 |
| --- | --- | --- |
| BE=1,BS=1,计数器0到0 | CONDITIONAL_ACCEPT_ARTIFICIAL | 零计数器信息不足，同步密钥可导出 |
| BS从1到0 | REVIEW | 需检查恢复通道与其他凭据 |
| 计数器3到2或3到3 | REVIEW | 异常信号不等于克隆证明 |
| BE=0,BS=1 | REJECT_INVALID_FLAGS | 非法标志组合 |
| 旧凭据撤销或操作早于绑定epoch | BLOCK_REVOKED_OR_STALE | 人工授权字段判定 |
| 签名未验证 | BLOCK_UNVERIFIED | 缺密码学验证时阻止 |

脚本的signatureVerified字段由人工输入，未执行公钥签名验证。CONDITIONAL_ACCEPT_ARTIFICIAL只代表模型条件通过。真实多设备并发可能导致计数器乱序，候选系统应保留人工复核与不确定性。

## 风险与候选控制

F009-07A：备份状态变化与克隆告警混淆。候选为BS单独提醒及恢复审查。
F009-07B：计数器异常导致正常设备被误封。候选为多信号判断和人工复核。
F009-07C：同步凭据被误标AAL3。候选为可导出性明示，禁止未经认证的等级声称。
F009-07D：旧设备内容借新授权重放。候选为独立操作epoch、撤销日志及删除水位复核。
F009-07E：设备审计元数据长期留存。候选为最小化、期限及访问隔离。

本轮无真实WebAuthn、密码学签名、设备同步、物理擦除或认证评估。证据为标准文档与内部人工E1；新增E2/E3预测0，外部复验0。未购买、注册收费服务或启动CI；账单及免费额度NOT_VERIFIED。下一阶段研究撤销后同步凭据在不同RP的生命周期与权限边界。
