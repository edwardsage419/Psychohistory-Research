# MKT068 Message DB 分类锁、跨分类提交顺序与全局游标风险

日期：2026-10-27 Asia/Singapore。研究轨：research/market。证据等级：MARKET E1。主动新增费用：0。

## 起点、去重和来源
开始读取 main HEAD 630626247f77e7808471b78e9044db9db2b6ca11、MKT001 至 MKT067 目录、MKT067、E036、F002、R204 新增冻结协议与计算、A/TH/C/D轨登记。本轮从 MKT067 KurrentDB 的预期版本和提交位置切换到 MIT 许可的 PostgreSQL Message DB，专门检查全局序号与提交可见性之间的区别。来源均为英文一手技术资料：
1. Message DB 官方 GitHub 固定源码提交 25da82b044f94416202ac3daa1866791b385badc，write-message.sql blob 415a1f8e3ed72e59ba3497336fb4f7d21d145910，get-category-messages.sql blob 7c246a5d7f8025bfbf27fa8ce9ef43491033c607，acquire-lock.sql，messages.sql，messages-id.sql，MIT-License.txt。https://github.com/message-db/message-db/tree/25da82b044f94416202ac3daa1866791b385badc
2. Eventide 官方接口和结构说明：https://eventide-project.org/user-guide/message-db/server-functions.html 与 https://eventide-project.org/user-guide/message-db/anatomy.html 。
3. PostgreSQL 官方序列说明：https://www.postgresql.org/docs/18/functions-sequence.html 。
4. Marten 官方异步投影高水位文档：https://martendb.io/events/projections/async-daemon.html 。
5. KurrentDB Python v1.3 多流原子追加官方文档：https://docs.kurrent.io/clients/python/v1.3/appending-events 。

## 实际确认的机制
输入：message UUID、stream_name、type、JSONB data、metadata、可选 expected_version；读取按 category、global_position 起点、batch_size、可选 consumer group 参数。存储包含流内 position、跨流 global_position、时间戳、消息体和元数据。写入函数首先对 category(stream_name) 的哈希取得 PostgreSQL 事务级 advisory lock，然后检查流版本并插入；同一分类下不同流的写入也被该锁串行化。预期版本为空时跳过显式版本匹配。全局 UUID 有唯一索引，和 MKT067 的 KurrentDB 不强制全局事件 ID 唯一形成可核实差异。

messages.global_position 为 bigserial，PostgreSQL 序列值按分配顺序产生，事务提交可晚于其他分类事务。get_category_messages 使用 global_position >= cursor 并按该序号升序排序。**官方分类读取与自建跨分类全局游标需要分开评价**：分类锁在正常 write_message 路径下为同一分类提供事务串行化；若自行合并多个分类、按当前可见最大 global_position 永久推进单一游标，可能跳过稍后才提交的低序号记录。此跨分类问题为源码和 PostgreSQL 事务语义推导的条件性风险，没有观察到 Message DB 官方分类消费者出现该遗漏。

## 独立人工事务模型
脚本 research/market/mkt068_category_commit_cursor_synthetic_20261027.js 使用纯 JavaScript 状态机，**20项断言全部通过**。人工事务 A 在分类 alpha 分配序号1并保持未提交；同分类 B 被锁阻塞；另一分类 beta 的 C 分配序号2并先提交。自建全局读取器看到2并将游标移至3，随后 A 提交序号1，后续按3读取将漏掉1。官方按分类分别读取时 alpha 从1取得1，beta 从1取得2。另检查事务中止形成永久空洞、跨分类序号间隙、全局安全高水位保守等待及同分类恢复写入。

该状态机是明确标记的合成事务语义测试，未执行 Message DB、PostgreSQL 并发事务或 KurrentDB 服务器。Marten 官方文档提供已知序列空洞与高水位保守推进的工程对照；其实现有效性未由本轮独立复验。

## 面向未来决策研究的候选映射
数据输入为经过授权的状态变更事件和业务操作ID；状态至少区分 stream_version、category、global_sequence、transaction_visibility、safe_read_watermark、projection_progress、consent_generation。目标是避免旧状态、漏读和跨分类错序进入长期反馈。重要建议前需要可证明的读取边界，不能直接将最大已见序号等同完整已提交历史。反馈与修正可采用分类分离游标、具事务状态证明的全局高水位或可重放的去重扫描。解释性应显示来源分类、观察位置、提交可见性和数据新鲜度。上述均为 DESIGN_CANDIDATE，没有预设个人效用权重或开发产品。

隐私权限：数据库角色和消息 UUID 约束不等同个人授权撤销；JSONB 原文、元数据和消费副本仍需按 F002 检查生命周期。费用与许可：Message DB 固定源码为 MIT 许可，公开研究免费；PostgreSQL 本地部署可能占用现成设备资源，本轮仅审查公开代码并运行人工 JS，没有部署或订阅。商业售价、真实运营成本、生产性能、故障率及人生决策收益均未验证。

证据分层：OFFICIAL_SOURCE_CODE=YES；POSTGRES_OFFICIAL_SEMANTICS=YES；SYNTHETIC_EXECUTED=20/20；REAL_DATABASE_CONCURRENCY=NO；REAL_PRODUCT_FAILURE=UNVERIFIED；INDEPENDENT_EXTERNAL_REPLICATION=NO；LONG_TERM_DECISION_EFFECT=UNVERIFIED。下一轮优先查 Message DB 真实多连接事务测试及 Eventide 消费者位置持久化策略，避免将自建全局游标风险误归于官方分类接口。
