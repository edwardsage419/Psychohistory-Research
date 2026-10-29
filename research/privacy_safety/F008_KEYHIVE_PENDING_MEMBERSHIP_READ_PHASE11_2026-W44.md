# F008 第十一阶段：并发撤销与成员列表读取一致性

日期：2026-10-29 UTC。目标键：(privacy_safety,F008,phase11,pending-cgka-membership-read-after-concurrent-revocation)。阶段 COMPLETE_BOUNDED_UPSTREAM_PATCH_REVIEW，F008整体IN_PROGRESS。仅使用公开固定源码与官方PR记录，未运行Rust或真实设备。

## 上游一手证据

Keyhive官方仓库 inkandswitch/keyhive 固定main b93f55bd3a5c274c10497f5cf834f95f3ff86930。官方PR #239 https://github.com/inkandswitch/keyhive/pull/239 ，标题 Resolve pending membership changes before reporting tree members，2026-09-26合并。PR正文确认：并发撤销时CGKA移除操作可能暂存，旧member_ids读取结果可能仍列出已被移除的成员，属于读取层状态过期，作者说明并未影响BeeKEM正确性。该问题与F008 phase10的PR #238因果时序授权缺口是不同目标键。

实际阅读PR #239官方files diff，涉及beekem/src/cgka.rs、beekem/src/tests/concurrent_membership_changes.rs、keyhive_core/src/cgka.rs、keyhive_core/src/principal/document.rs、keyhive_core/tests/sync.rs。补丁新增resolve_structural_changes，读取member_ids前如有pending_ops_for_structural_change便replay_ops_graph，member_ids接口由不可变借用变为可变借用并返回Result。相关测试新增并发添加与撤销同步后读取的检查。此为UPSTREAM_CODE_AND_TEST_SUPPORTED，尚未在本环境执行cargo test。

同时复核PR #236 https://github.com/inkandswitch/keyhive/pull/236 于2026-09-26合并，涉及撤销后的同步事件过滤；PR #238 https://github.com/inkandswitch/keyhive/pull/238 于2026-09-28合并，作者明确保留曾获授权主体在撤销后操作的因果时序风险。三者修补不同层面。PR合并证明代码进入上游分支，不构成独立安全认证或端到端撤销保障。

## 候选控制与风险登记

F008-R11-01：读取成员列表前必须处理所有已收到的并发结构变更；无法完成重建时返回UNKNOWN或错误，避免以过期成员列表判断当前权限。实际权限决策仍需独立授权证明。

F008-R11-02：区分已收到但未应用的移除、尚未收到的远程撤销、已取得历史密钥和已复制明文。更新成员显示只能改善第一类状态，无法证明全网撤销传播完成。

F008-R11-03：成员列表API由只读变成可能执行状态重放的操作，应保留重放失败、性能、重复操作幂等及审计时点；需要以固定上游版本运行人工身份、并发撤销和离线重联测试。

F008-R11-04：禁止将CGKA当前成员身份与未来个人决策系统的最终数据访问权直接等同；后者还需服务器权限、密钥状态、历史缓存和授权撤销日志联合检查。

## 证据与限制

官方代码diff与测试说明已读；真实Rust测试NOT_RUN，离线设备/密钥清除NOT_RUN，个人敏感数据0，独立安全审计0。Rust依赖与本地缓存未确认，保持完全免费静态审查。所有控制为UNADOPTED候选知识储备。

下一阶段优先检查PR #239的同步测试是否覆盖重复撤销、跨设备分叉与错误传播；在本地依赖和零费用条件确定前不执行云端CI。
