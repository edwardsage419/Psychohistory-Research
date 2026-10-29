# F008 第三阶段：Automerge并发删除与更新、旧数据复活及授权门

日期：2026-10-29 UTC；track=privacy_safety；subflow=F；status=PHASE3_BOUNDED_E1_IN_PROGRESS_UNADOPTED；基线main 70b3e24481a50a072d7f86fa25f1eaf2f18dedae。target_key=(privacy_safety,F008,phase3,concurrent-delete-update-revocation)。承接F008 Phase1、Phase2。没有真实个人敏感数据。

## 公开英文原始来源及证据范围

Automerge 官方 Conflicts https://automerge.org/docs/reference/documents/conflicts/ ，明确并发同属性写入有确定性可见winner，getConflicts可访问其他并发值，操作ID决定优先级，非墙上时钟顺序。官方 Merge Rules https://automerge.org/docs/reference/under-the-hood/merge-rules/ ，明确同一map key的一边删除、一边赋新值时，合并后保留新赋值；不同key的写入可以并存。官方首页 https://automerge.org/docs/ 说明离线编辑与联网同步。这些是库的合并行为文档，未承诺应用层授权撤销与物理擦除。

## 本轮新增风险与人工检验

场景：服务器授权epoch从7变为8并撤销，离线设备B持有epoch7旧派生数据；A并发删除某键，B仍在同键写旧值。按官方map合并规则，旧写可能在合并后的可见状态重新出现；若两个节点同时set同键，某一值成为winner，另一值仍可能在冲突历史中可见。不能把CRDT收敛视为撤销传播或物理清除证明。

自拟候选应用规则：服务端持有独立权威授权版本与active标记；只在active=true且事件epoch严格等于当前epoch时允许派生数据使用。撤销后拒绝全部旧写，重新授权新epoch也不恢复旧epoch内容。合并后再做授权校验，冲突集合和离线/备份仍列入生命周期核查。这个门属于候选应用政策，不是Automerge内建保证。

Python标准库脚本 research/privacy_safety/f008_merge_revocation_gate_20261029.py 在本地执行24项确定性检查、失败0，覆盖并发delete/set两顺序、set/set两可见winner、epoch8撤销、epoch9重新授权、冲突历史和离线副本。脚本SHA256 e472ee65075dd27bfee3c6e0c780b6357c4ad1e7abbc5100862da3045af9f0e2。脚本为文档语义的简化人工状态机，未安装或运行Automerge库；没有浏览器、实际设备、真实密钥、真实擦除或外部独立验证。

候选风险 F008-R6：并发删除/更新复活旧内容；F008-R7：getConflicts保留非可见值；F008-R8：授权epoch与合并结果分离；F008-R9：本地历史/离线副本无法远程验证清除。候选控制均 UNADOPTED。GLOBAL_ERASED=UNVERIFIED，F008整体仍 IN_PROGRESS。零新增费用；仅公开资料与本地标准库，账户账单未独立核验。

下一项 F008 Phase4：核对实际开源测试中删除/更新合并与getConflicts行为，优先只读源码和既有免费环境；无法免费运行则保留NOT_RUN。
