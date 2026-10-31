# MKT166 ActivityWatch v2 可选事件ID与开放尾部分段合并

UTC日期 2026-10-31。目标键 (market,ActivityWatch,aw-server-rust-fe353a66,v2-optional-event-id-merge). 基线main 04c466865e1bb5806f42bb9c36f7d6819ba39e4e。承接MKT160分段和MKT165历史回填，本轮只分析v2的事件身份与重复导入边界。非盲态工程研究。

## 原始源码与产品范围

固定上游 commit fe353a66ca3859231ce306a0f4faf15f732d8b41。
[segment.rs](https://github.com/ActivityWatch/aw-server-rust/blob/fe353a66ca3859231ce306a0f4faf15f732d8b41/aw-sync/src/v2/segment.rs) Git blob ff96977f17d59776af03bb797d45c1326fcbd901。第68至75行的WireEvent.id类型为Option<i64>；第389至408行merge_events把有ID的事件存入BTreeMap<i64,Event>，同ID后出现者覆盖前者；无ID事件直接追加Vec；合并结果按时间戳排序。第117至119行空输入立即返回，第172至176行开放尾部合并已有事件与新事件。第315至319行写入可选ID、时间、持续时间和data。源码未在这个局部合并函数验证跨设备的事件ID全局唯一性，也未把无ID事件按内容去重。写入器按device_id和bucket_id创建对象，不能将局部假设扩大为跨设备真实冲突。

[manifest.rs](https://github.com/ActivityWatch/aw-server-rust/blob/fe353a66ca3859231ce306a0f4faf15f732d8b41/aw-sync/src/v2/manifest.rs) Git blob a67f9033b3a304c0443e069dea51923541624244。目录按设备ID分隔，清单按bucket ID保存分段。官方[2026-10-06同步状态文章](https://activitywatch.net/blog/syncing-your-activitywatch-devices/)明确v2写入器尚未接入命令，现行v0.14.0同步不支持删除传播。不能把实验性v2行为描述成发布版用户已遇到的故障。

真实输入是本地Event对象和bucket元数据，状态包括可选本地事件ID、时间戳、开放尾部分段、generation及清单。目标为活动历史复制与查询，未提供人生效用权重或自我优化算法。反馈来自同步状态、日志和开发测试。隐私权限受本地设备和用户选定同步文件夹影响，第三方传输工具可能另有副本。公开源码支持机制解释，未见完整历史来源证明或真实事件修订审计。ActivityWatch核心软件免费开源；第三方文件同步服务可能单独收费，本轮没有使用任何服务。

## 人工E1实跑

本地Python标准库运行 research/market/mkt166_v2_event_id_synthetic_20261031.py，18项断言PASS，原生Rust未运行。
1. 同ID的修订记录覆盖旧记录，两个不同ID保留；同ID重复导入幂等。
2. 无ID的相同人工事件重复输入后保留两份，五轮重复输入可累积五份。
3. 人工恢复后重用ID=1的另一事件覆盖旧事件，说明单独的整数ID不构成不可变全局来源证明。
4. 时间相同而ID不同的事件仍分别保留；空新增列表不构成删除传播。

以上为局部Rust函数语义的人工镜像，不证明实际ActivityWatch重复事件发生率、数据库ID重用、跨设备碰撞或可利用漏洞。上游没有运行本轮测试。无真人E2、历史E3和外部独立复现。

## 候选知识储备

长期数据记录应将设备身份、bucket身份、事件ID、事件版本、删除墓碑和恢复权限分开；缺ID时保留UNKNOWN或显式重复策略，禁止把一次成功同步等同完整历史证明。候选规则需要未来独立验证，不提前开发个人决策产品。下一轮核对真实Event ID生成和v2 writer上游更新，确认哪些ID可以缺失及其来源。
