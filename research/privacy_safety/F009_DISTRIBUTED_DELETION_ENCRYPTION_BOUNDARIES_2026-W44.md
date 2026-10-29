# F009 第1阶段：多设备删除传播、同步副本与加密覆盖边界

日期：2026-10-30 Asia/Singapore；2026-W44。目标键：(privacy_safety,F009,phase1,distributed-erasure-and-encryption-scope)。状态：COMPLETE_PHASE1_STATIC_CANDIDATE_CONTROLS。F008 Keyhive持续研究保持IN_PROGRESS，本轮开设互补的隐私数据生命周期专题。无用户个人数据、密钥或银行信息。

## 1. 三个英文官方来源中的不同边界

A. ActivityWatch 0.14同步指南 https://docs.activitywatch.net/en/latest/syncing.html 明确设备各自写自己的数据，同步目录由用户选择Syncthing/Dropbox等传输；每台设备保留其他设备完整副本；来源设备最近7天内编辑可同步，**删除不传播**，同步设置也不传播。卸载指南 https://docs.activitywatch.net/en/latest/uninstalling.html 明确卸载软件后仍须另行删除数据目录。以上是官方文档支持的明确数据生命周期限制。不能把本地删除、软件卸载、同步目录删除及其他设备擦除当成同一操作。未经独立运行，未验证第三方同步工具的实际删除/备份行为。

B. Actual Budget官方同步安全文档 https://actualbudget.org/docs/getting-started/sync/ ：设备本地与选定服务器均保留数据，预算数据可选端到端加密。官方明确**银行同步令牌在服务器另存，端到端加密不覆盖这些令牌**，设备本地数据仍未加密。启用加密后忘记密码且没有本地副本会造成不可恢复；同步重置需要使其他设备接受新的sync id。不能将“预算数据端到端加密”推导为“所有元数据、令牌、终端副本和备份均已加密”。本轮没有实际部署、银行连接或加密攻击测试。

C. NIST Privacy Framework v1.0（2020）https://www.nist.gov/privacy-framework/privacy-framework 提供隐私风险治理结构；NIST CSWP 25（2022-05-20）https://csrc.nist.gov/pubs/cswp/25/data-structure-for-integrity-protection-with-erasu/final 讨论保留哈希链完整性时对任意记录执行删除的数据结构。标准和研究仅支持风险框架及可行方法背景，不能证明任一上述产品满足删除义务，也不能把区块链或特定数据结构视为未来项目默认实现。

## 2. 零费用候选控制与人工验收设计

未来如确需个人决策模型，优先最小采集、按数据用途隔离，并记录每条数据的origin_device、purpose、consent_version、storage_locations、replica_ack、backup_expiry、deletion_requested_at、tombstone_version、erasure_status。授权撤销、停止新收集、禁止新同步、删除各副本、删除备份、销毁密钥应分别标注状态。

候选人工测试（暂未执行）：三设备A/B/C，A产生合成记录x并同步；B离线；A请求删除x并发布tombstone；C确认拒绝旧x重新导入；B离线重连后不得使x复活；任一副本未确认则总体状态PENDING，不能宣称全局删除完成。另设加密边界负例：预算内容加密而服务器令牌未加密，显示INCOMPLETE_ENCRYPTION_SCOPE并禁止自动上传敏感凭据。所有测试仅可用虚构数据及本地现成设备。

风险登记：R1 删除未传播造成旧副本长期存在；R2 离线设备重放导致数据复活；R3 同步服务商保留备份；R4 仅加密主数据而遗留凭据/元数据；R5 过度采集形成不必要的敏感记录；R6 删除审计本身泄露用户身份。控制应提供解释、人工复核与撤销路径；不承诺技术上无法证实的远端彻底擦除。

## 3. Keyhive进度与证据边界

本轮通过GitHub连接器重新读取inkandswitch/keyhive main的design/threat_model.md、keyhive_content/src/lib.rs、keyhive_wasm/src/js/revocation.rs，Git blob分别为863e2f4220ff5d404668e788317dc7d7bf62c2a1、d65a62cf68f5dc7ba58658f74b26fcf8377caa06、105337aaa786cbf301979ff29abf83cf000d3de1，与F008 phase21固定文件一致。未发现这三个已读文件的变更；这不等于上游所有文件或PR无更新。G1/G4与内容水位执行仍按上轮已披露限制登记，避免重复宣称新漏洞。没有运行Rust/WASM/Playwright或独立安全审计。

证据等级：官方技术文档与NIST原始公开研究支持，属于静态候选安全方法；运行时有效性NOT_RUN，真实敏感数据0，E2/E3新增0。零新增收费操作、云服务、API、CI、设备或订阅。下一阶段F009：研究跨副本删除确认的失败与重试语义，核查开源同步项目公开测试；F008继续按上游真实变化推进。
