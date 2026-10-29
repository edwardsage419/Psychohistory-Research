# F008 第十二阶段：Keyhive 并发成员读取测试覆盖与错误传播

日期：2026-10-29 UTC。目标键：(privacy_safety,F008,phase12,pr239-concurrent-member-read-tests-and-failure-path)。阶段 COMPLETE_BOUNDED_STATIC，F008整体IN_PROGRESS。仅审查上游公开源码与已合并PR，未运行Rust或真实设备。

## 固定一手来源

官方仓库 https://github.com/inkandswitch/keyhive ，固定提交 b93f55bd3a5c274c10497f5cf834f95f3ff86930。官方PR #239 https://github.com/inkandswitch/keyhive/pull/239 ，2026-09-26合并，合并提交8c2ceb8c926496fb2a0a1e1cf0069686d4ca0200。直接读取PR五个文件diff和固定提交下 beekem/src/tests/concurrent_membership_changes.rs（775行）、keyhive_core/tests/sync.rs（541行）、beekem/src/cgka.rs、keyhive_core/src/principal/document.rs。PR #239与此前F008 phase11为同一补丁，本阶段只追踪测试覆盖及错误传播，避免重复申报补丁本身。

## 已发现的明确测试覆盖

beekem/src/tests/concurrent_membership_changes.rs 有 member_ids_resolves_pending_concurrent_adds，构造并发添加后调用member_ids并断言全部副本的成员集合一致。另有 local_remove_sees_a_pending_concurrent_remove、a_removal_beats_a_concurrent_add_of_the_same_member 和 concurrent_removals_of_one_member_leave_a_usable_tree 等独立场景，说明已有一定撤销覆盖。

keyhive_core/tests/sync.rs 有 a_replica_sent_a_concurrent_removal_still_applies_later_ones，构造两方并发撤销同一成员，随后另一撤销操作仍须同步；有 revoking_a_member_whose_add_is_still_outstanding_removes_them_from_the_cgka_group，验证添加仍在待处理时撤销后成员集合不保留该成员。以上为源码中的测试定义及断言，尚未在本环境实际执行。

PR补丁使member_ids变为可变读取并返回Result，先执行resolve_structural_changes，后者可能通过replay_ops_graph返回错误；document.cgka_members向上传播错误。在所审查的两份测试文件中，没有检出专门注入replay_ops_graph失败并断言错误沿member_ids/cgka_members向上传播的测试。此为明确的限定范围覆盖缺口，不能推断全仓库不存在其他测试，也不能认定已存在可利用漏洞。原有测试普遍使用expect来断言正常成功路径，尚未独立检查异常回滚与重复读取幂等性。

## 候选风险控制

F008-R12-01：成员列表读取触发状态重放时，区分成功、待同步、重放失败；失败返回UNKNOWN并拒绝越权决策，不用旧列表兜底。

F008-R12-02：在免费本地Rust环境可复现时，加入受控故障注入，验证member_ids及cgka_members错误传播、重复读取幂等性、并发重复撤销和分叉后重联；先固定源码与依赖身份，禁止使用计费CI。

F008-R12-03：区分CGKA成员集合、当前权限、历史密钥、离线明文缓存及撤销传播。成员集合收敛无法证明历史数据删除或端到端撤销安全。

证据等级为UPSTREAM_CODE_AND_TEST_STATIC_SUPPORTED。Rust cargo test、设备密钥与历史缓存实验均NOT_RUN；独立安全认证0；真实敏感数据0；候选控制UNADOPTED。下一阶段F008 phase13优先调查本地无额外费用Rust依赖复验的可执行性及失败路径最小测试设计，保持个人决策产品开发暂停。
