# F008 第十八阶段：离线分区写入、并发密钥树合并与撤销时序的测试边界

日期：2026-10-30（UTC+08）。目标键：(privacy_safety,F008,phase18,offline-partition-write-and-revocation-causal-merge)。阶段状态 COMPLETE_PHASE18_STATIC，F008整体仍IN_PROGRESS。研究用途为未来个人决策数据安全的候选知识储备，未接入真实个人数据或开发产品。

## 1. 固定版本及直接读取的源码测试

固定上游 inkandswitch/keyhive main HEAD 930c4290b92940d7b716a2a18ecc46eb56308069；本轮直接读取三个测试文件与生产API部分源码，保留Git blob身份：

* keyhive_core/tests/concurrent_instances.rs，blob 06e62a4dbaac63b10e4848dadb8d54bbb11ece15，https://github.com/inkandswitch/keyhive/blob/930c4290b92940d7b716a2a18ecc46eb56308069/keyhive_core/tests/concurrent_instances.rs
* keyhive_core/tests/sync.rs，blob daab789eda6a6b23f7d2e4b1c127d6d76e1d90dc，https://github.com/inkandswitch/keyhive/blob/930c4290b92940d7b716a2a18ecc46eb56308069/keyhive_core/tests/sync.rs
* keyhive_core/tests/revocation_sync.rs，blob 638eebbd507a39d6edc8028e53d4fe22932d19b1，https://github.com/inkandswitch/keyhive/blob/930c4290b92940d7b716a2a18ecc46eb56308069/keyhive_core/tests/revocation_sync.rs
* keyhive_core/src/keyhive.rs，blob 55551596c8059efcee300566c6e0f04ee72c7279，https://github.com/inkandswitch/keyhive/blob/930c4290b92940d7b716a2a18ecc46eb56308069/keyhive_core/src/keyhive.rs

这些是固定源码与测试断言，尚未在本轮实际运行Rust。当前环境command -v cargo/rustc均未找到，未安装工具链、未启动云端CI。

## 2. 本轮新增可核查事实

concurrent_instances.rs 的 writes_made_during_a_partition_survive_the_merge 用例在同一身份的两个实例断开同步时分别执行密钥轮换与加密写入，恢复连接、交换密钥秘密并同步后，原两个实例及另一合法读者均可解密分区期间的两份密文。测试目标是合法分区写入的可恢复性。另一个用例 the_instance_that_lost_the_leaf_reads_again_once_it_has_the_winning_secret 检查并发轮换合并后，未获得胜出密钥的实例在交换秘密之前无法解密，之后恢复。两项断言明确区分了密文存在、密钥树合并及密钥秘密可得性。

sync.rs 的 a_replica_sent_a_concurrent_removal_still_applies_later_ones 测试两名管理者对同一成员并发撤销后，后续撤销仍被处理，成员列表在已同步的两个观察者之间一致。revoking_a_member_whose_add_is_still_outstanding_removes_them_from_the_cgka_group 则检查未应用的并发添加与后续撤销，避免被撤销者残留在最终成员列表。revocation_sync.rs 主要检查撤销事件及所需prekey传播，包含被撤销成员所持历史密钥的分发条件。

keyhive.rs 的 KeyhiveState 明确包含待依赖事件队列 pending_events、已知文档/CGKA状态及密文存储。其注释指出同一Keyhive句柄克隆共享实时状态，跨独立实例需实际同步。这些结构说明需要区分本地权限视图与跨设备最终视图，不能由一个设备显示撤销推断所有离线设备立即获知撤销。

## 3. 尚未被本轮所读测试直接联合证明的边界

上述测试分别验证分区写入恢复、并发撤销收敛及密钥传播。本轮所读三个测试文件没有直接展示完整组合：设备B离线保留旧权限，设备A撤销B，B在未收到撤销时继续加密写入，网络恢复后验证该写入的因果合法性、密文可见性、接收者权限、回滚或隔离状态。也没有在这一组合中验证旧密文缓存是否清除。

这是一项限定文件与限定场景的覆盖调查，不能据此认定上游全仓库缺失测试、生产系统可被越权访问或密文在撤销后自动失效。并发写入能够恢复的现有测试也不能直接推出撤销后离线写入必定被接受。是否需要拒绝、隔离或人工复核，取决于未来产品的授权时点语义及经实验证明的协议能力。

## 4. 零新增费用候选安全控制和复验协议

候选测试设计：固定一个文档、两实例与独立读者，先同步合法读权限，再人为分区；主实例撤销离线成员并记录撤销证书因果前驱、CGKA状态与写入密钥版本；离线成员分别在撤销已签发前后但尚未同步时尝试写入；恢复同步后逐份核验密文存在性、可解密主体、权限判断时点、错误类型及审计记录。另设持续失败的成员移除签名、缺失撤销事件、重放旧操作三类故障。任何缺失观察值记UNKNOWN，保留失败结果，不修改上游协议或冻结研究。

未来个人决策系统候选原则：本地优先与离线操作必须附带权限版本及待同步状态；涉及敏感数据分享的离线队列在重连时重新评估授权并允许人工确认或隔离；历史明文、未来密文、权限视图与备份删除分别追踪；权限冲突时阻断自动扩大分享范围。原则不构成Keyhive现有功能声明，也不构成已验证安全保证。

证据等级 STATIC_SOURCE_AND_TEST_EXPECTATIONS，原生Rust故障注入 NOT_RUN，第三方独立安全认证 UNKNOWN，新增真人E2=0，历史E3=0。零新增费用，无收费API/云GPU/CI、无密钥或敏感资料输入。

下一项phase19：调查上游是否已有“撤销与离线写入同场景”测试及跨设备因果权限解释；有重叠则转为只读差距对照，不重复报告静态结论。
