# MKT070 Eventide 消费者错误吞没与检查点跨越风险

日期：2026-10-27 Asia/Singapore。轨道：research/market。状态：COMPLETE_BOUNDED_MARKET_E1。主动新增费用：0。

## 去重与来源

本轮开始读取 main HEAD 2d3393491bbe81fcf34ecd49741e80d588626633、MKT069、E038、F002、R206 最新记录及当日/本周子任务。MKT069 已研究正常重放、消费者身份和检查点周期。本轮聚焦错误处理覆盖后返回成功的不同控制流。

固定英文官方源码：
1. https://github.com/eventide-project/consumer/blob/5674f17a9a8ac6321e052acdc015d4a16e47ac13/lib/consumer/consumer.rb ，blob 14ee50a1f2c95d0ba8ef86328f38c2122c304701。
2. https://github.com/eventide-project/consumer/blob/5674f17a9a8ac6321e052acdc015d4a16e47ac13/lib/consumer/subscription.rb ，blob 86887fd917673a4d202a46f4774a135a5262bef6。
3. https://github.com/eventide-project/consumer/blob/5674f17a9a8ac6321e052acdc015d4a16e47ac13/lib/consumer/controls/consumer/error_handler.rb ，blob abae983633910df5b91397d594dcc78f69972a09。
4. https://github.com/eventide-project/consumer/blob/5674f17a9a8ac6321e052acdc015d4a16e47ac13/test/automated/error_handling/error_handler.rb ，blob 0d2f130dcee6b380476fcb543dfa2945d1ecc3c2。
5. 官方英文指南 https://eventide-project.org/user-guide/consumers.html ，明确说明默认错误需重新抛出，除明确重试外不应吞没。
6. 官方重试原理 https://blog.eventide-project.org/articles/retries-in-eventide-microservices/ （2018-12-24），强调处理器幂等性。

## 新增机制

真实输入为 category 消息、global_position、业务 handler 顺序及 consumer 的 error_raised 覆盖。状态为内存 subscription.position、成功处理计数、持久化 position_store、各 handler 副作用。consumer.dispatch 先逐个运行 handler，全部成功才 update_position；若 handler 抛错，进入 rescue，调用 error_raised。默认 error_raised 再抛错。官方测试中的 ErrorHandler.Example 故意覆盖为只记录异常而不重新抛出，测试验证 dispatch 没有抛错。

subscription.dispatch 在 consumer.dispatch 返回后，无条件把内存 position 设为 global_position+1。由这两处固定源码共同推出：自定义 error_raised 吞没异常时，失败消息未计入 checkpoint，但 subscription 已跳过它。后续成功消息可以把持久化 checkpoint 推进到失败位置之后。重启后失败消息可能永久漏处理，除非另有人工恢复、独立重放或外部事务机制。

这属于错误处理配置引发的条件性风险。默认错误传播会阻止上述 subscription 内存推进。默认路径仍可能出现先执行 handler 的不可回滚副作用，故需独立处理幂等性。上游现有单元测试覆盖吞错和正常订阅位置，所读测试没有把二者组合为失败后下一条成功的恢复测试；不能据此断言上游完整测试库没有其他覆盖。

## 合成验证

research/market/mkt070_eventide_error_checkpoint_synthetic_20261027.js 为 Node.js 18+ 标准库独立状态机，六类情景28项断言，28项通过，0失败。吞错且 interval=1 时消息2第二 handler 失败，第一 handler 已有副作用；消息3成功后 checkpoint 从1跳到3，重启从4开始，消息2未完整处理。默认重抛时内存位置停在2，checkpoint 停在1。interval=3 时成功计数跨过失败消息，消息4成功后仍可将 checkpoint 推至4。还覆盖首次失败、正常基线及副作用部分完成。

测试执行的是独立控制流模拟，没有运行 Eventide Ruby 包、PostgreSQL 或真实服务。上游源码与文档支持机制，合成测试支持逻辑反例。生产事故、发生率及任何个人决策收益均未验证。

## 候选知识映射与费用

未来个人量化输入可记录经过授权的状态变更事件及人工纠错；状态应区分 message_id、source_position、handler_effects、error_outcome、durable_checkpoint、consent_generation。目标为防止漏掉撤销、纠错和反馈事件。候选控制：默认传播不可恢复错误；只有具备可验证重试契约时允许抑制异常；保存每条消息的 handler 完成标记；对外部副作用使用稳定幂等键；独立对账已读、已完成、已持久化位置；对授权撤销事件提供高优先级人工复核。

隐私：跳过撤销消息可能继续使用旧授权；日志本身应避免保存敏感原文。可解释性：应显示某条事件实际处理结果及数据版本。Eventide 的事件机制不包含个人效用函数、自我修正决策算法或量化人生价值。开源仓库固定版本提供 MIT-License.txt，可免费阅读；真实部署与服务维护费用未知。本轮未注册服务、调用计费API、部署数据库或启用CI。账户整体账单未独立核验。

证据：DOCUMENTED_MECHANISM 为官方源码和文档；INDEPENDENT_SYNTHETIC_MODEL 为28项人工测试；REAL_DEPLOYMENT=UNVERIFIED；MARKET_E1 为内部机制研究标签，不升级为 R 科研 E1/E2/E3。

下一轮 MKT071：优先回到 Exist、ProjectionLab 或 Beeminder 的近期官方个人反馈机制，比较错误更正是否能追溯并修复长期目标偏离记录，避免工程账本连续研究掩盖产品主线。
