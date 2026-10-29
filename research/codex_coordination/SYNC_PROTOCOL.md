# Codex 与 ChatGPT 三轨增量同步协议
版本 1，2026-10-29。仅工程协作；不改变项目阶段、任务频率、冻结协议或科学验收。

## 设计与取舍
用户要求在已授权边界自主推进、减少token浪费并保持两边同步。选择现有GitHub提交/PR作为事实来源，加三个既有任务prompt的短同步指令。不增建调度器或外部服务。相比共享可变总状态文件，分轨记录降低并发覆盖；相比只靠会话记忆，PR和短记录可供其他任务实际读取。尚未合并的本协议不冒充main制度；已更新的任务prompt内含可独立执行的同步规则。

## 每轮最小读取
1. 最新main HEAD、最近提交及开放codex/* PR的标题/摘要；用上轮observed_head或相关blob判断变化，首次启动无游标时读相关最新记录。
2. 仍按项目要求读取README、现行工作流要求、研究导航/关口及最新239索引/队列。文件相同blob可复用已读内容；新会话无缓存不能伪称已读。
3. 仅对所选目标展开相关变更、冻结协议、来源和结果；发现冲突/错误再扩大范围。摘要不替代正式科学验收材料。
4. PR #1包含R257 S53的6类检查器假阳性和盲态限制；其未合并结论是待审查证据。不能因PR存在/代码运行就宣称main已修复或通过科学验收。

## 去重与认领
目标身份为 track + model_or_source + protocol_version + question；跨轨另比较后三字段，不能因track不同忽略相同问题。已有人研究的模型仍允许不同算法独立复算，明确互补问题及已看信息，不虚称盲态。
跨轮有价值时才在research/coordination/{r,theory,market,codex}/建立短记录；各轨只写自己的路径，文件名UTC时间到秒加短目标标识，碰撞则后缀唯一标识。建议不超过一页，不复制长报告。
状态只用COMPLETE/PARTIAL/BLOCKED/NOT_RUN。PARTIAL加activity=claimed可表示认领，另列claimed_at_utc及expires_at_utc（两小时）；过期只是需重查的提示，绝不证明旧工作已停或已完成。记录不是原子锁，没有全局互斥保证。跨branch认领通过开放PR摘要发现；main目录缺记录不等于没有并发任务。
最小字段：track、subflow、run_date、observed_head、target_key、activity、status、source_links、work_performed、evidence_scope、results_seen、output_paths、commit_sha/PR（没有则null）、ci_status、billing_checked、blockers、next_action。
有进行中同问题先查看最新证据并选择互补任务；写前重读main/目标blob/本分支HEAD。并发变更重新核对，禁止覆盖、强推或破坏性重置。Codex始终独立分支+PR，不直接开发提交main。

## 完成与交接
一个有实质产物的阶段一次交接；能随同结果提交就不另造状态提交。无变化不写空日志、不发重复报告。其他轨发现问题只记具体路径/值/证据，历史原文件及冻结协议保留。
提交后回读commit、内容、分支和真实Actions状态；无CI写NOT_RUN。用最新PR摘要告知待办与限制，不能把PR已打开写成已审查/已合并。
不建立新付费服务、runner、API调用计算或新增定时任务。仅更新三个已有任务的prompt，不改变schedule、timezone或enabled。
这是周期任务启动时拉取信息的机制，不能推送到已经运行中的上下文；需要下一轮实际读取记录才能证明端到端采用。暂不声称已达成零重复、完全一致或token节省数量。

## Codex下一项
R257 S53严格收据验证器：固定八世界/五容量集合及唯一性，校验delta/C0/C、乘子/导数和E1元数据，用PR #1的六个假阳性作回归。与R主线新S阶段互不覆盖；不得修饰原盲态失败。
