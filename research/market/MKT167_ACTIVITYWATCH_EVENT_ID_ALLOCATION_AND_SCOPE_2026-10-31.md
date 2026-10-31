# MKT167 ActivityWatch 事件 ID 分配、数据库作用域及 v2 同步边界

UTC 2026-10-31。目标键 (market,ActivityWatch,aw-server-rust-fe353a66,event-id-local-allocation-vs-v2-merge)。非盲态开源机制研究，承接 MKT166，未修改上游代码。

## 固定来源与真实机制

上游固定 commit fe353a66ca3859231ce306a0f4faf15f732d8b41。实读 aw-models/src/event.rs、aw-datastore/src/datastore.rs、aw-sync/src/v2/segment.rs，及 ActivityWatch 2026-10-06 官方同步说明。

1. Event::new 生成 id: None，模型注释明确事件进入服务器数据库后才分配 ID；显式传入 ID 会替换已有同 ID 事件。Event::PartialEq 仅比较时间、时长和数据，不比较 ID。
2. 数据库建表使用 events.id INTEGER PRIMARY KEY AUTOINCREMENT。insert_events 执行 INSERT OR REPLACE INTO events(bucketrow, id, starttime, endtime, data)，之后用 last_insert_rowid 返回 Some(id)。parse_event_row 从数据库行读取 Some(id)。
3. 同一数据库中 ID 属于整张 events 表，跨 bucket 共享；两个独立数据库可各自分配整数 ID=1。ID 本身缺少设备和数据库来源证明。
4. v2 SegmentWriter 把 event.id 写成可选 ID；开放尾部 merge_events 按整数 ID 合并，缺失 ID 直接保留。该局部函数没有跨设备全局唯一性证明；v2 文件按设备及 bucket 分区。现有读取路径通常从数据库返回 Some(id)，不能从 Event::new 可为 None 直接推断发布版同步经常出现无 ID 事件。
5. 2026-10-06 官方文章称 v2 写入器尚未接入正式命令，v0.14.0 的数据复制与文件同步工具选择由用户管理。删除同步尚不支持。没有证明发布版存在 ID 碰撞漏洞。

## 原生 SQLite 人工实验

运行 python research/market/mkt167_sqlite_event_id_scope_20261031.py，Python 3.13.5 标准库 sqlite3，15 项断言全部通过。两个内存数据库各自首次自动分配 ID=1，数据互相独立。同一数据库第二个 bucket 新事件得到 ID=2；显式 ID=1 更新可替换原记录，甚至将其从 bucket 1 移至 bucket 2。这是对源码 SQL 语义的 SQLite 复现，未执行 Rust 服务、同步命令或真实设备。结果不代表实际业务接口允许跨 bucket 更新。

## 产品与科研评价

真实输入是活动 watcher 的时间、持续时间、JSON 数据和 bucket 元数据；SQLite 记录存储本地 ID。产品目标是自动记录、跨设备复制和可视化活动，不具备经验证的长期人生效用函数或自动决策优化。反馈包括同步状态与事件查询；没有在本轮验证独立的修订历史或恢复证明。官方开源机制可解释，缺少真实用户长期预测改善试验。ActivityWatch 开源免费；可选第三方同步服务可能单独收费，本轮未使用。

候选要求：未来来源身份应至少绑定 (device_identity, datastore_identity, bucket_identity, event_identity, version)，删除/撤销及恢复记录另行处理。跨设备 ID 的数值相等不得单独判定同一历史事件。该建议属于方法储备，不提前开发个人决策系统。

来源：
* https://github.com/ActivityWatch/aw-server-rust/blob/fe353a66ca3859231ce306a0f4faf15f732d8b41/aw-models/src/event.rs
* https://github.com/ActivityWatch/aw-server-rust/blob/fe353a66ca3859231ce306a0f4faf15f732d8b41/aw-datastore/src/datastore.rs
* https://github.com/ActivityWatch/aw-server-rust/blob/fe353a66ca3859231ce306a0f4faf15f732d8b41/aw-sync/src/v2/segment.rs
* https://activitywatch.net/blog/syncing-your-activitywatch-devices/

证据：MARKET 官方固定源码支持机制；内部 SQLite E1 人工实验；原生 Rust/真实设备 NOT_RUN；独立用户效果验证 NOT_RUN；新真人 E2=0，历史 E3=0。下一步：追踪跨设备恢复时 bucket ID 与来源设备 ID 的绑定校验。
