# MKT169 ActivityWatch Rust 来源身份测试覆盖审查

UTC 2026-10-31T06:23:11.467Z。目标键 (market,ActivityWatch,aw-server-rust-fe353a66,distinct-device-same-origin-test-coverage)。接续 MKT168。固定上游提交 fe353a66ca3859231ce306a0f4faf15f732d8b41。只读源码与测试，无 Rust 编译、设备操作或收费服务。

## 固定源码与测试

直接读取 aw-sync/src/sync.rs Git blob 1daffa82dec2efe877923f4789bc8c4c897b5c95，aw-sync/tests/sync.rs blob 0d53df58d1c112bb61e22817467f12034eb029e6，aw-sync/tests/sync_roundtrip.rs blob 1e35aab0829e69651afee96699016750f8a25e91，以及 aw-sync/tests/historical_edit.rs blob 59e03794395d7d78cded8c70b8c9531b5398439c。

生产路径 discover_peers 以远端 device_id 去重；pull_from_remotes 传入 sync_datastores 的来源 device_id 为 None；get_or_create_sync_bucket 的签名只有 bucket_from、ds_to、is_push。目的 bucket 原名、规范化名及历史 $aw.sync.origin 匹配均未对来源远端 device_id 做强制一致性核对。源码在该位置提及未来 (device_id,id) 身份工作 ActivityWatch/activitywatch#302。不能据此认定已发布版存在可利用漏洞。

已存在真实 Rust 测试：test_whitespace_hostname_pull_creates_sanitized_bucket，test_whitespace_hostname_pull_reuses_legacy_unsanitized_bucket，test_pre697_origin_scan_resumes_legacy_bucket，test_pre697_origin_scan_refuses_ambiguous_candidates，daemon_deduplicates_same_device_in_both_layouts，test_own_data_does_not_return_via_peer。它们覆盖单来源名称迁移、多个历史候选拒绝、同设备跨目录去重及回环去重。

本轮已读上述三个测试文件及 sync.rs 内联 peer discovery 测试，未找到直接构造“不同 device_id、相同规范化 hostname、相同原始 bucket ID、两设备先后导入同一目的 datastore”的端到端回归。此为已读范围内测试覆盖缺口，不能宣称全仓库或所有外部测试均不存在。

## 候选原生测试矩阵

T1 两台不同 device_id 但 hostname 都规范化为 office_laptop，原始 bucket ID 相同，A→B 与 B→A 两顺序分别执行，验证各自历史及来源身份。T2 一个 device_id 下原始与规范化 hostname 迁移应保留合法旧 bucket。T3 两个历史候选均匹配时继续拒绝模糊自动合并。T4 unknown hostname 且没有可靠来源 ID 时拒绝。T5 事件时间交错时，验证来源隔离与早期回填不会被最新时间游标掩盖。T1/T5 为尚未执行的建议，需先明确兼容旧数据的迁移合同，不擅自修改上游或本项目 R 轨。

## 产品机制维度

输入为 watcher 事件、bucket 元数据、文件夹设备 ID；状态为 SQLite bucket 与来源映射；算法为来源发现、名称兼容、游标增量同步；目标是跨设备活动汇集。反馈为状态日志与查询，未提供经实证验证的人生效用最优化。源码可审计，本地优先；用户自选文件传输工具可能额外复制敏感记录。官方文档明确删除不会跨设备传播。开源代码及免费文档可用，本轮未购买产品。候选要求：来源身份绑定 (device_id, bucket_id, event_id, version)，历史迁移冲突保留 UNKNOWN。

来源：
* https://github.com/ActivityWatch/aw-server-rust/blob/fe353a66ca3859231ce306a0f4faf15f732d8b41/aw-sync/src/sync.rs
* https://github.com/ActivityWatch/aw-server-rust/blob/fe353a66ca3859231ce306a0f4faf15f732d8b41/aw-sync/tests/sync.rs
* https://github.com/ActivityWatch/aw-server-rust/blob/fe353a66ca3859231ce306a0f4faf15f732d8b41/aw-sync/tests/sync_roundtrip.rs
* https://github.com/ActivityWatch/aw-server-rust/blob/fe353a66ca3859231ce306a0f4faf15f732d8b41/aw-sync/tests/historical_edit.rs
* https://docs.activitywatch.net/en/latest/syncing.html

证据等级：固定上游原始源码及已归档 Rust 测试的静态审查。新增原生 Rust 执行=0；新增 E2=0，E3=0。下一项：有免费本地 Rust 条件时按 T1/T5 运行独立临时回归，先核对最新上游修复与测试，避免重复。
