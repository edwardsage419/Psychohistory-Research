# MKT170 ActivityWatch 设备身份迁移候选方案深读
UTC 2026-10-31T07:18:57Z。目标键 (market,ActivityWatch,fe353a66,device-id-migration-open-prs)。本轮直接读取 ActivityWatch/aw-server-rust 官方仓库最新 master fe353a66ca3859231ce306a0f4faf15f732d8b41（2026-10-26），以及开放 PR #786、#836、#835、#789。它们尚未合并，不能算已发布功能。

PR #786（2026-10-06 创建，10-27 更新）提出 SQLite v6→v7 迁移：UNIQUE(name) 改为 UNIQUE(device_id,name)，保存事件、历史 rowid、AUTOINCREMENT 高水位、现行及归档元数据。旧行标记 local。作者明确保留旧的 name 唯一冲突保护，公共 API 与缓存仍按 name 寻址。作者自报 104 测试通过、1 ignored，未由本轨独立执行。

PR #836（2026-10-23 创建，10-26 更新）为依赖 #786 的 DRAFT，提出 (device_id,id) 桶缓存、历史别名双向解析、设备分组查询、导入导出及身份预检。作者明确 Python 兼容、同名共存、完整验收及 V2 导入尚未完成。分组导入先预检身份，但运行期失败仍可能只导入部分分组。自报测试不能视为独立科研证据。

PR #835 提出本地设备 UUID 发现 API；PR #789 提出按 (source_device_id,bucket_id) 保存 rowid 游标以捕获迟到历史事件，HTTP 来源或游标数据库不可用时回退时间游标。均仍 OPEN。

机制维度：输入 watcher 事件、SQLite bucket、设备 UUID、主机名及同步文件夹；状态是桶、来源别名、游标与回执；算法为来源识别、兼容旧名称、增量导入及查询。目标是活动记录汇集，反馈为同步日志与查询。无已证实的人生效用优化或自我修正能力。代码可审阅，本地优先；用户选择的云同步工具可能传输敏感数据。删除传播仍有限制。免费公开来源，无产品购买。

候选要求：以 (device_id,bucket_id,event_id,version) 追踪来源；先完成旧库迁移及兼容验证，再解除 name 冲突保护；模糊别名保留 UNKNOWN；迟到事件、游标丢失、部分导入、撤销和重放须独立回归。当前仅上游 PR 文档证据，原生 Rust、真实设备和外部验证 NOT_RUN，E2/E3 新增0。

来源：https://github.com/ActivityWatch/aw-server-rust/pull/786
https://github.com/ActivityWatch/aw-server-rust/pull/836
https://github.com/ActivityWatch/aw-server-rust/pull/835
https://github.com/ActivityWatch/aw-server-rust/pull/789
https://github.com/ActivityWatch/activitywatch/issues/302
https://activitywatch.net/blog/syncing-your-activitywatch-devices/

下一项 MKT171 转向 ProjectionLab 情景模拟和 Beeminder 偏离反馈机制，扩展产品覆盖。
