# F008 第七阶段：ARK 身份密钥存储、恢复与撤销边界

UTC 2026-10-29。目标键：(privacy_safety,F008,phase7,identity-key-storage-recovery-and-revocation-boundaries)。状态 PHASE7_BOUNDED_DOCUMENT_AUDIT_COMPLETE，F008 整体 IN_PROGRESS。

## 官方英文来源与本轮真实增量

Automerge ARK 官方 API 指南 https://automerge.org/docs/keyhive/ark-api-guide/ 说明该包仍为 alpha；初始化时 Ed25519 身份密钥对生成或从 storage adapter 读取，身份密钥持久化为 `active-key-pair-2` 的 JWK JSON。Keyhive 的 archives、ops、prekey secrets、leaf secrets 分别存储；同一身份的多个实例可共享存储。官方明确表示清除存储会破坏身份，当前没有密钥备份或恢复机制。public member 可以让所有人获得被授予的访问级别。权限有 relay、read、edit、admin 四种，Keyhive 权限状态通过独立同步协议传播。

NIST SP 800-57 Part 1 Rev.5 官方出版页 https://csrc.nist.gov/pubs/sp/800/57/pt1/r5/final 讨论密钥保护、备份、归档、恢复的一般方法。该标准作为风险审阅参考，不能据此推断 ARK 已经实现恢复能力或通过安全认证。

前序 F008 Phase6 已研究 `repo.create2` 与 `repo.create` 的保护差异。本轮新问题是身份密钥存储损坏或被清空时，授权历史与文档副本即使仍在，也无法据此保证身份连续性和恢复。密钥丢失、密钥泄露、成员撤销、历史副本清理必须分别记录。

## 四种候选场景

| 情景 | 文档支持的事实 | 未验证的结论 |
| --- | --- | --- |
| 单设备存储被清空 | 身份可能丢失，官方当前没有恢复机制 | 重装应用自动恢复原身份 |
| 多标签页共用身份存储 | 多实例可共享身份存储 | 关闭一个标签页即销毁全部旧密钥 |
| 成员授权撤销 | 提供撤销 API 和独立 Keyhive 同步 | 离线缓存、旧密钥、备份已经物理擦除 |
| public 文档授权 | public member 可赋予所有人相应权限 | 登录状态自动保证文档私有 |

## 零费用候选控制与风险

R20 身份丢失：未来产品需要显式说明组件当前缺乏官方恢复能力，身份无法确认恢复时显示 LOST/UNKNOWN，禁止自动承诺重建。

R21 密钥副本：任何未来本地备份方案先独立审查密钥类型、用户同意、存储保护、恢复授权和删除证据。本轮不生成、导出或读取用户真实私钥。

R22 共享实例：身份、标签页会话、文档副本、撤销确认分别登记；单实例退出不能当作全局密钥清除证据。

R23 public 访问：显式显示文档公开权限并取得用户授权，不从默认登录状态推断文档私有。

全部控制 UNADOPTED。没有部署 ARK、运行 WASM、进行网络同步或读取个人敏感数据。证据为官方文档支持的组件语义及 NIST 一般标准；真实密钥恢复、跨设备撤销、物理擦除均 NOT_RUN。主动新增费用零，账户账单及免费额度 UNKNOWN。

下一步在零费用且依赖固定可复现时审查 ARK 上游身份初始化与共享存储测试；否则继续固定源码审计，不注册付费服务。
