# MKT064 eventsource-py 快照版本、事件分支与历史回放完整性

日期：2026-10-27（Asia/Singapore）。轨道：market。状态：COMPLETE_BOUNDED_SOURCE_SYNTHETIC_E1。主动新增费用：0。

## 1. 起点、去重与来源固定

本轮开始读取 main 最新 HEAD `f3a4e40e505107677788992b63f283aff2eeb573`、MKT063、E032、F002（2026-W44）及最新 R199、TH067 提交。MKT062研究显式关闭审计后重启的历史缺口；MKT063研究 SQLite 表原地恢复导致触发器消失。本轮选择另一套开源事件溯源实现，研究**快照版本与实际已持久化事件流不一致**时的重建风险，避免重复前两项。

研究对象：tyevans/eventsource-py，固定 main commit `98fee074989a26e2748a8de1d90b1143760a9b8a`（2026-10-16 的0.15.1发布提交），MIT许可，免费开源库，不代表个人决策产品或收费SaaS。只使用英文上游来源：

1. https://github.com/tyevans/eventsource-py/blob/98fee074989a26e2748a8de1d90b1143760a9b8a/src/eventsource/application/aggregates/snapshotting.py ，blob `d4ee6f336abaff248d64c42142f521606f97dd87`。
2. https://github.com/tyevans/eventsource-py/blob/98fee074989a26e2748a8de1d90b1143760a9b8a/src/eventsource/application/aggregates/repository_query.py ，blob `a7fcbf721dbf9f1a67e79f06dede2a487a7f8d9c`。
3. https://github.com/tyevans/eventsource-py/blob/98fee074989a26e2748a8de1d90b1143760a9b8a/src/eventsource/application/aggregates/repository_snapshots.py ，blob `09643d11e5c44334590dd0e0fafd803f48f49b71`。
4. https://github.com/tyevans/eventsource-py/blob/98fee074989a26e2748a8de1d90b1143760a9b8a/docs/guides/snapshotting.md ，blob `d483a49b3cfba20d967d11b03382ef6ec997516c`。
5. https://tyevans.github.io/eventsource-py/guides/snapshotting/ ，官方文档。README与MIT许可证：https://github.com/tyevans/eventsource-py 。

## 2. 机制与实际可观察的边界

`take_snapshot()`直接读取聚合体的当前 `version` 和 `_serialize_state()`，再保存快照。`create_snapshot()`调用该函数，没有在此路径显式核对未提交事件、事件流高水位或状态摘要。`read_valid_snapshot()`校验快照是否存在、schema_version是否与类匹配；`AggregateRepository.load()`接受该快照的版本，读取版本大于快照版本的后续事件。恢复异常会触发完整重放；**成功反序列化且版本或内容不一致的快照未在这些路径进行完整前缀一致性验证**。

官方文档已明确提醒：手工快照应先 `save()` 再 `create_snapshot()`，否则未提交事件会进入快照；手工构造错误版本的快照可能重复应用或跳过事件。故本轮属于已公开机制的固定源码复核与跨项目对照，不声称发现上游未知漏洞。

新增边界推演：即使快照版本与当前事件流高水位相等，若快照状态来自不同恢复分支或被错误替换，单凭版本和schema相同仍无法证明其来源于同一事件前缀。此处是**条件性完整性风险和候选控制要求**，尚无真实上游故障记录。

## 3. 独立标准库人工实验

归档脚本：`research/market/mkt064_snapshot_integrity_synthetic_20261027.py`。仅Python标准库，模型化固定源码的快照读取、后续事件应用及schema回退。未下载、安装或运行上游包。人工事件流为 v1:+5、v2:+7，完整重放结果12。

| 快照情景 | 按已核源码边界模型重建值 | 预期真实值 | 候选前缀校验 |
| --- | ---: | ---: | --- |
| 合法v2/state12 | 12 | 12 | 通过 |
| 未提交事件形成v3/state112 | 112 | 12 | 拒绝 |
| 状态12误标为v1 | 19 | 12 | 拒绝 |
| v2但错误state99 | 99 | 12 | 拒绝 |
| v2但来自分支B的state -8 | -8 | 12 | 拒绝 |
| schema版本不符 | 12（完整重放） | 12 | 拒绝快照 |

另验证无快照完整重放、事件版本缺口、有效v1前缀和分支身份检查。**24项人工断言通过，0失败。** 该脚本验证设计边界的逻辑，不能替代上游包集成测试或实际生产故障证据。

## 4. 个人量化决策系统的候选方法映射

真实输入候选：原始事件ID、持久化序号、聚合体ID、来源/分支ID、schema版本、授权generation、提交证明、快照摘要、历史更正事件。状态表达候选：EVENT_STREAM_VERIFIED、SNAPSHOT_PREFIX_VERIFIED、SNAPSHOT_STALE、SNAPSHOT_AHEAD_OF_COMMIT、BRANCH_MISMATCH、FULL_REPLAY_REQUIRED、UNKNOWN。

算法候选：写快照前确认全部相关事件已提交；恢复时绑定事件前缀哈希或可信checkpoint及分支身份；版本连续性检查；快照和完整事件重放的抽样比对；出现冲突时丢弃快照、停用历史评分并人工复核。上述保护是研究候选，**不声称已由该开源库实现**。

目标与反馈：可信历史回放比例、快照校验失败率、完整重放差异、回放耗时和权限撤销后的旧快照失效情况。解释输出应显示历史分支、最后已验证提交、快照适用范围和未知区间。对个人目标权重保持开放与可更改，不引入唯一人生效用函数。

隐私与权限：快照可能保留旧敏感状态。沿用F002的撤销授权、派生数据失效、备份恢复隔离和最小审计原则。版本一致性不代表处理授权仍有效。仅人工合成数据。

费用模式：该库采用MIT许可，免费源码可在现有设备审查，内存或SQLite适合无新增服务费用的有限研究。其他部署依赖、维护和运行成本须另行评估；没有订阅价格或真实用户决策效果可供证明。本轮没有购买、计费API、收费CI、云服务器或GPU。

## 5. 证据分级、风险与下一步

MARKET E1：固定上游源码与英文官方文档；24/24独立合成断言。官方文档警示属 DOCUMENTED_LIMITATION，分支身份一致性属于 SOURCE_BASED_INFERENCE 与 DESIGN_CANDIDATE。UPSTREAM_PACKAGE_EXECUTION=NO；REAL_INCIDENT=NOT_VERIFIED；INDEPENDENT_EXTERNAL_REPLICATION=NO；PERSONAL_DECISION_OUTCOME=NOT_VERIFIED。

MKT064-R1 HIGH：未提交事件先进入手工快照，历史状态提前出现。
MKT064-R2 HIGH：快照版本与状态前缀错配，重放跳过或重复应用事件。
MKT064-R3 MEDIUM：跨恢复分支相同版本的快照缺乏额外来源绑定，可能被误接受。
MKT064-R4 MEDIUM：历史快照保留已撤销的敏感信息，需单独生命周期控制。

下一轮MKT065优先对照另一开源事件账本的快照哈希、分支标识和恢复后验证，并评估是否有上游包级免费集成测试条件。E轨只读检查最新R199，F轨本周F002已完成。研究顺序仍为完整R系列、系统归纳、模型熔炼。
