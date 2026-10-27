# MKT067 KurrentDB预期版本、重试幂等、投影水位与许可边界

日期：2026-10-27 Asia/Singapore。轨道：research/market。MARKET E1（英文官方技术文档、固定许可源码及人工状态机）。主动新增费用：0。

## 去重、版本与证据身份
开始读取项目main HEAD 88ed3c1544347ba5b517dd444073f0a6e482bfc8、MKT001至MKT066目录、MKT066、E035、F002、R203第三方法与最新A/TH报告。MKT065与MKT066已覆盖pyeventsourcing的历史版本及缓存；本轮切换到KurrentDB（EventStoreDB后继），聚焦写入CAS、事件ID幂等边界、全局提交位置与异步投影之间的关系。官方英文资料：
1. Python客户端v1.2 Append: https://docs.kurrent.io/clients/python/v1.2/appending-events （版本限定；事件ID、expected revision、WrongCurrentVersionError、幂等重试及commit position）。
2. Python客户端v1.2 Persistent Subscriptions: https://docs.kurrent.io/clients/python/v1.2/persistent-subscriptions （ack/nack、超时重试与checkpoint）。
3. Server v26.2 Projections: https://docs.kurrent.io/server/v26.2/features/projections/intro （投影输出流归属、重放及checkpoint）。
4. Server v26.2 Quick Start: https://docs.kurrent.io/server/v26.2/quick-start/ （KLv1及免费单节点限制）。
5. 2026-08-13官方许可变更说明: https://new-next.kurrent.io/blog/licensing-in-kurrentdb-v26-2-and-beyond-what-s-free-and-what-s-licensed/ 。
6. 固定源码许可证 https://github.com/kurrent-io/KurrentDB/blob/ecca18768fa806b0f9707512227e663022854d90/LICENSE.md ，Git blob bbd37b682aff53b9adfd232088700e8deb17ca77。
公开仓库固定读取HEAD ecca18768fa806b0f9707512227e663022854d90；技术文档为版本固定网页而非同一源码commit，二者不能混为一个版本证明。

## 本轮新增机制
真实API输入：stream_name、NewEvent的UUID/type/data/metadata、current_version（NO_STREAM、EXISTS、ANY或整数）、可选订阅组与ack/nack。状态至少包括流内revision、全局commit position、投影处理到的水位、订阅确认状态与事件ID。写入使用expected revision进行乐观并发检查，版本不符返回WrongCurrentVersionError；ANY取消版本条件。文档说明append具幂等重试行为，但明确**事件UUID没有全局唯一性约束**，相同ID可在其他流、相同流新正确版本或很晚的无并发检查写入中重复。因而“重试幂等”与“永远不能重复业务动作”是不同承诺。

写入成功返回全局commit position，可用来等待最终一致的读取模型追上相应事件；不能仅凭append成功断言异步投影已追上。持久订阅的消费者应在处理成功后ack，失败nack/retry；业务副作用和ack分属不同边界，处理成功而确认前崩溃会形成重复交付的候选风险，消费端仍需去重和恢复验证。文档的投影输出流由投影独占，重置会重置checkpoint并重放；不应将其当作用户可直接随意修改的事件账本。

## 32项人工状态机检查
独立脚本 research/market/mkt067_kurrent_revision_watermark_synthetic_20261027.js 仅用JavaScript标准库构造简化事件流，检查NO_STREAM首写及同请求重试、预期revision冲突、ANY跳过版本条件、同一事件ID不同版本或流的重复、提交位置与投影水位、消费端先副作用后ack的重复投递、先ack后副作用的丢失风险等。32/32人工断言通过，失败0。该脚本是明确标注的**合成语义示例**，不是KurrentDB官方服务器、SDK或真实事务的执行。尤其模拟的幂等查找算法仅用于展示条件边界，不能当作上游精确实现。

## 决策研究候选映射
输入为用户允许的来源事件、目的授权及版本；状态表达建议分别保留stream_revision、commit_position、projection_watermark、consumer_ack、dedupe_scope、consent_generation。目标：避免并发覆盖、重复决策动作、旧投影冒充最新状态。反馈与修正：版本冲突后重新读取并重新审查，而非盲目重试覆盖；在重要建议前检查projection_watermark>=required_commit_position，无法确认则标为FRESHNESS_UNKNOWN；副作用消费以明确的业务操作ID去重。解释性：公开写入版本、读取水位、数据来源、更新滞后与异常原因。上述均为候选控制，尚未形成个人产品或经过真实效用验证。

隐私与权限：文档中的流版本控制不构成个人数据授权控制；事件日志、订阅、快照及投影副本均可能保留已撤销的敏感旧值。需与F002的来源依赖、授权代际、备份恢复与外部删除状态分别检查。未接入任何用户真实敏感数据。

## 许可、费用与产品局限
官方2026-08-13公告与v26.2文档称单节点可免费使用，多节点、只读副本、归档和静态加密等有Enterprise许可边界；实际许可证为Kurrent License v1（KLv1），**非OSI认可开源许可**，禁止未经授权将软件作为向第三方提供主要功能的托管服务。旧版/新版许可差异须按版本核对。免费自托管也可能产生机器与运维成本；本项目只做公开资料审查和本地人工测试，不部署、不注册云服务、不使用收费功能。官方产品能力和许可为文档/许可证支持；商业宣传不作为科研验证。

证据层级：DOCUMENTED_OFFICIAL（版本化文档和许可证）；SYNTHETIC_EXECUTED（32/32）；DESIGN_CANDIDATE（候选映射）；REAL_DB_EXECUTED=NO；REAL_CONCURRENCY_FAILURE=NOT_VERIFIED；INDEPENDENT_EXTERNAL_REPLICATION=NO；PERSONAL_DECISION_BENEFIT=NOT_VERIFIED。下一轮MKT068可检查KurrentDB客户端官方幂等测试与多流事务提交位置，或对照真正OSI许可的事件账本。R系列完成优先级不变。
