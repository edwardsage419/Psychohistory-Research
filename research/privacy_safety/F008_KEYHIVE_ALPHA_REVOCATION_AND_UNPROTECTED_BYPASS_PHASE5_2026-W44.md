# F008 第五阶段：Keyhive Alpha的授权撤销、同步与未保护文档边界

日期：2026-10-29 UTC。track=privacy_safety，subflow=F，target_key=(privacy_safety,F008,phase5,keyhive-alpha-revocation-unprotected-bypass)。状态 PHASE5_OFFICIAL_DOCUMENT_REVIEW_COMPLETE_OVERALL_IN_PROGRESS。本轮仅审阅公开英文官方文档，没有部署软件或接入个人数据。

## 第一手英文来源

1. Automerge Repo Keyhive API Guide：https://automerge.org/docs/keyhive/ark-api-guide/ 。实际阅读Alpha状态、身份持久化、访问等级、addMemberToDoc、revokeMemberFromDoc、unprotected doc例外、服务端策略、网络适配器包装、keyhive独立同步、密钥持久化与恢复说明。
2. Automerge Repo参考：https://automerge.org/docs/reference/repositories/ 。实际阅读NetworkAdapter与StorageAdapter的数据传播责任。
3. Automerge冲突合并规则：https://automerge.org/docs/reference/under-the-hood/merge-rules/ 。延续F008第四阶段已审阅的delete/set行为；未运行实际Automerge测试。

## 新发现与证据边界

官方明确标记 @automerge/automerge-repo-keyhive 为alpha，API可能变化。ARK提供基于Keyhive的访问控制与端到端加密。访问级别为relay、read、edit、admin，撤销接口为 revokeMemberFromDoc。官方明确描述添加成员会旋转文档密钥；本轮阅读范围没有足够证据保证撤销成员后已缓存的明文、旧密钥、离线副本或历史备份全部消失。

关键边界1：文档写明 unprotected（pre-keyhive）文档不具有keyhive状态，成员操作会抛UnprotectedDocError；其示例服务端SubductionPolicy对未保护文档ID绕过访问检查。未来如使用类似机制，必须先独立确认文档是否受保护，并禁止把“授权查询返回undefined”当作访问许可。

关键边界2：服务端策略说明读取文档至少需要relay权限、推送变更至少需要edit权限。它属于官方提供的可选策略能力，不能由API存在推断所有部署默认启用。应用须确认服务器实际配置、适配器包装、同步版本与权限查询时效。

关键边界3：额外网络适配器包装时periodicallyRequestSync默认false，即使初始化时为true。Keyhive状态与文档状态经不同同步机制传播。撤销事件与文档变更可能存在到达顺序和离线滞后，具体延迟和故障恢复需运行时实测。

关键边界4：官方说明身份密钥保存在本地StorageAdapter，当前没有密钥备份或恢复机制。清除本地存储会破坏身份；数据恢复、授权撤销与真正擦除应分开验收。

## 候选控制与风险登记

R11 未保护文档权限绕过：新文档创建时显式标记保护状态；未受保护的敏感文档一律拒绝同步或读取；审计服务端策略实际是否启用。
R12 撤销传播延迟：每次受保护操作核对授权版本和有效权限；离线设备返回PENDING_ACK，超过期限后继续拒绝服务端写入。
R13 旧密钥与明文缓存：分开登记密钥旋转、缓存清理、派生索引、设备确认、备份删除；不能从一次撤销成功推出GLOBAL_ERASED。
R14 适配器配置差异：检查每个网络适配器是否经过授权层包装及定时同步设置；在隔离测试环境模拟撤销后断网、恢复及旧写入重放。
R15 身份恢复失败：记录身份密钥存储与恢复限制，避免在缺乏恢复方案时把本地数据清除视为可逆操作。

以上均为未来候选控制，UNADOPTED。官方文档支持API存在和配置语义，威胁情境及防护效果属于推论或待验证。F008真实Automerge/ARK运行、双设备同步、撤销后历史密钥可解密性、实际物理删除均NOT_RUN。没有注册服务、购买软件、调用计费API或处理敏感数据。主动新增费用0，实际账户账单UNKNOWN。

下一阶段F008：确认零费用本地依赖环境后，对ARK未保护文档绕过、撤销传播和旧密钥可访问性编写可反驳的最小运行时测试；若依赖无法获取，保留NOT_RUN并转向版本固定源码审计。
