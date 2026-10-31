# MKT168 ActivityWatch 来源设备 ID 与目标 bucket 身份绑定审查

UTC 2026-10-31T05:20:33.392Z。目标键 (market,ActivityWatch,aw-server-rust-fe353a66,remote-device-id-vs-import-bucket-provenance)。非盲态源码审查和人工 E1，承接 MKT167。

## 固定原始证据
上游固定提交 fe353a66ca3859231ce306a0f4faf15f732d8b41，aw-sync/src/sync.rs Git blob 1daffa82dec2efe877923f4789bc8c4c897b5c95。直接读取第 57 至 76 行、第 507 至 518 行、第 592 至 768 行及第 821 至 918 行。discover_peers 以 RemoteDb.device_id 分组，解决同一 device_id 多目录重复发现。pull_from_remotes 调用 sync_datastores(*ds_from,dest,false,None,...)；sync_datastores 以 bucket_from 调用 get_or_create_sync_bucket，未传入 RemoteDb.device_id。目标 bucket ID 由原始 bucket ID 与 $aw.sync.origin（缺失时用 hostname）组成，先查原名，再查规范化名，随后尝试历史来源元数据匹配。两个不同 device_id 且同名来源的 bucket 在这些路径中没有强制 device_id 一致性检查。unknown 来源有拒绝保护，历史回退多候选时也会拒绝；这些保护应保留。

## 实际人工实验
脚本 research/market/mkt168_peer_bucket_provenance_20261031.js 在 V8 执行，18 项显式断言全部通过。设备 A 与 B 的 device_id 不同，主机名 Office Laptop 和 office_laptop 规范化相同，原始 bucket ID 相同。A 有时间 1、3 事件，B 有时间 2、4 事件。按模拟的最新事件游标增量导入：A 后 B 得 A1,A3,B4，漏 B2；B 后 A 得 B2,B4，漏 A1,A3。候选设备 ID 命名空间模型两种顺序均得到全部四事件。人工模型仅模拟 bucket 命名和最新游标；未执行 Rust sync_one、真实数据库、设备迁移或真实攻击。不能将此直接断言为当前发布版已复现缺陷。

## 产品维度与研究意义
输入：watcher 事件时间、持续时间、JSON、bucket 元数据、同步文件夹设备 ID。状态：本地 SQLite 及同步来源 bucket。机制：按来源分组、规范化名称、增量游标、有限历史修订。目标：多设备活动记录合并，未提供经验证的人生效用优化。反馈：同步状态、事件查询；无独立长期人生决策改善证据。权限：本地优先，文件传输工具由用户选定，第三方云可能持有副本；官方承认删除不会跨设备传播。解释性：源码可读；正式 Rust 端到端验证未做。费用：开源免费，本轮没有使用第三方收费同步。

候选方法：来源身份至少绑定 (device_id, datastore_id, bucket_id, event_id, version)；在兼容旧 hostname bucket 时明确 UNKNOWN/冲突人工处理，避免静默跨设备合并。未来产品仍暂缓开发，不指定唯一效用权重。

来源：
* https://github.com/ActivityWatch/aw-server-rust/blob/fe353a66ca3859231ce306a0f4faf15f732d8b41/aw-sync/src/sync.rs
* https://docs.activitywatch.net/en/latest/syncing.html
* https://activitywatch.net/blog/syncing-your-activitywatch-devices/

证据：固定上游源码及官方文档，内部人工 E1 18/18；真实 Rust、设备和用户效果 NOT_RUN；新增 E2=0、E3=0。下一项：检查 peer discovery 与 bucket 元数据身份不一致时真实 Rust 单元测试覆盖及安全迁移路径。
