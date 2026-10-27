# MKT069 Eventide 消费者检查点、身份隔离与重放边界

日期：2026-10-27 Asia/Singapore。轨道：research/market。状态：COMPLETE_BOUNDED_MARKET_E1。主动新增费用：0。

## 起点、去重与原始来源

起点 main HEAD 8c1307991e0a2bc56aa75f4bf41e99691cab663a。已核对 MKT068、E037、F002、最新 R205 冻结协议与验证收据及 A/TH/C/D 登记。MKT068 研究 Message DB 的分类锁与跨分类全局游标。本轮转向 Eventide 官方消费者的检查点持久化，专门检查处理失败、身份冲突和分组调整，避免重复上轮的全局序号结论。

固定公开源码：
1. Eventide consumer 仓库 commit 5674f17a9a8ac6321e052acdc015d4a16e47ac13（2024-09-09）；lib/consumer/consumer.rb blob 14ee50a1f2c95d0ba8ef86328f38c2122c304701，lib/consumer/subscription.rb blob 86887fd917673a4d202a46f4774a135a5262bef6，lib/consumer/defaults.rb blob c45887ebead95e6264a9354685d0f76ba6070358。https://github.com/eventide-project/consumer/tree/5674f17a9a8ac6321e052acdc015d4a16e47ac13
2. Eventide consumer-postgres 仓库 commit 1619390c50be9d573796cc8223827902a97b2e31（2024-04-25）；lib/consumer/postgres/position_store.rb blob a55e0d4d19ed9c473bc9e38f8a6ff58fd5d16c9，position_store/stream_name.rb blob c3e289276624a5a451d1468cc6edca2397685379。https://github.com/eventide-project/consumer-postgres/tree/1619390c50be9d573796cc8223827902a97b2e31
3. Eventide 官方英文消费者手册，2026-10-27 查阅。https://eventide-project.org/user-guide/consumers.html
4. Eventide 官方 2024-04-26 变更说明，旧文档提及的预取机制已移除，不能把旧描述当作当前行为。https://blog.eventide-project.org/articles/notice-consumer-prefetching-is-removed/
5. 两个固定仓库均提供 MIT 许可证文件；源码研究免费，真实部署成本未验证。

## 实际读取的运行契约

输入为单一 category 的 Message DB 消息，包含 global_position、stream_name、type、消息体和元数据。消费者可配置 handler 顺序、category、consumer identifier、批量大小、轮询间隔、group_member/group_size、position_update_interval。输出是业务 handler 的副作用和另存于位置流的处理进度。此机制管理事件处理进度，并未定义个人目标优化、人生效用或自主纠错算法。

consumer.rb 的 dispatch 先依次调用全部注册 handler，成功后才调用 update_position(global_position)。update_position 每处理达到指定条数时写一次位置，默认间隔100。subscription.rb 在一次成功 dispatch 后把下一次内存读取位置设为 global_position+1。Postgres PositionStore 读取位置流的最新 Recorded 消息并写入新的 position；位置流名以 category 和可选 identifier 构成。

直接后果一：检查点周期内发生进程崩溃时，已处理而未写入位置的消息会在恢复后再次派发。若某个 handler 已产生不可回滚副作用，后续 handler 失败也可能导致前者重复执行。默认100是位置记录间隔，不等于恰好一次外部副作用保证。

直接后果二：两个消费者使用同一 category 且未分配不同 identifier 时，共用位置流，较快消费者可覆盖较慢消费者的进度。官方手册对此明确警告。分组消费者须采用独立 identifier；代码的 stream_name 构造确实包含 identifier。

条件性后果三：更改 group_size 会改变部分流的分区归属。若同时复用旧成员的 checkpoint，新成员可能接手比旧 checkpoint 更早的消息。该情况来自分区映射与位置重用的合成推演，未证明官方提供了安全的在线分组调整操作。应将分组变化视为需要迁移/重放计划的配置事件。

官方手册也警告自定义 SQL condition 可能漏处理或乱序，且激活该功能可能增加安全风险。本轮仅登记警告，未测试数据库 SQL 条件。

## 可执行合成验证

脚本 research/market/mkt069_eventide_checkpoint_synthetic_20261027.js，Node 18+ 标准库，28项断言全部通过。人工模拟间隔5处理7条后只记录位置5，恢复重放6、7；间隔100处理99条仍无持久化位置；第二 handler 在位置2失败时，第一 handler 已有副作用而位置只推进到1；同名位置流被另一个消费者推进至10后，较慢消费者可能跳过6至10；独立 identifier 隔离位置；分组大小2变3时，人工哈希3的消息从成员1迁到成员0，复用旧位置20会漏掉位置9。分组哈希仅用于逻辑反例，未实现真实 PostgreSQL hash_64。

测试结果：SYNTHETIC_ASSERTIONS=28/28，SOURCE_CODE_READ=YES，UPSTREAM_PACKAGE_EXECUTED=NO，POSTGRES_CONCURRENCY_EXECUTED=NO，REAL_WORLD_INCIDENT=UNVERIFIED，EXTERNAL_INDEPENDENT_VALIDATION=NO。

## 未来心理史学候选知识映射

候选数据输入是经过授权的状态变更事件；状态表达建议至少记录 category、consumer_identity、group_configuration_version、source_position、durable_checkpoint、handler_effect_identity、processing_outcome、consent_generation。目标为避免重放造成的重复反馈、旧授权事件复活和跨轨消费遗漏。可考虑幂等副作用键、位置与业务效果原子提交或可补偿重放、独立身份检查点、分组变更前迁移核验、人工可读的处理水位。解释时必须区分已读取、已处理、已持久化位置及外部副作用是否确认。

隐私：检查点身份隔离不自动实现授权撤销。持久化位置流及业务副本仍需依 F002 处理来源、缓存、备份与敏感信息生命周期。许可与费用：MIT 源码可免费审阅；本轮未注册服务、部署数据库、购买产品、调用计费 API 或启动 CI。账户整体账单与 GitHub 免费额度未独立核验。市场销售或部署效果、性能与长期个人决策收益均为未验证。

证据分层：官方文档/固定源码为 DOCUMENTED_MECHANISM，28项为 INDEPENDENT_SYNTHETIC_MODEL，实际 Eventide 运行、真实事务和人生决策收益为 UNVERIFIED。候选设计标记 DESIGN_CANDIDATE，不提升为 R 系列科研 E1/E2/E3 验收。

下一轮 MKT070：优先比较官方开源消费者对 handler 失败、检查点与业务副作用原子性以及分组迁移的实际回归测试；必要时切回个人量化/目标反馈产品的近期官方机制，避免市场研究长期偏离应用问题。
