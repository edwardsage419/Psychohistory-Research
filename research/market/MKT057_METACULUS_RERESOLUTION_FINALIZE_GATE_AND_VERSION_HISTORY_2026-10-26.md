# MKT057 Metaculus重新结算时间、排行榜冻结与版本可追溯性

日期：2026-10-26（Asia/Singapore）。轨道：market。状态：COMPLETE_BOUNDED_SOURCE_AND_SYNTHETIC。开始前main HEAD e9f3005c020bccbfa230d1ef6c25e49c0a393356。前序MKT056已审计划关闭时间与提前结算加权；本轮限定为重新结算后的评分资格与历史版本问题。主动新增费用0，未登录、购买、调用计费API、启动Actions或接触个人敏感数据。

## 1. 固定来源及证据等级

官方英文FAQ：https://www.metaculus.com/faq/ ，确认管理员决定结算，并在适当情况下允许重新结算；AMBIGUOUS和ANNULLED不计分。官方评分FAQ：https://www.metaculus.com/help/scores-faq/ ，描述时间加权及评分规则。官方API文档：https://www.metaculus.com/api/ ，明确一般认证账号对自身预测可访问，聚合历史、选项历史等字段有访问分层。官方FAQ和API的表述为OFFICIAL_DOCUMENTATION，未进行在线账户集成测试。

源码固定于 Metaculus/metaculus Git commit 68db27f800271d952ca01017a4a6a94f8c36fdd3，2026-10-26通过GitHub连接器直接读取：
1. questions/services/lifecycle.py，Git blob c67950c88567e2b6cf256fcd5e86a1f161002ce6，resolve_question设置resolution_set_time为当前时间；unresolve_question将其置空，并触发评分撤回。
2. scoring/utils.py，Git blob a326163302f51f15a9b407d8d3dcedac3d137e6a，score_question删除旧Score后批量写入新Score；retrieve_question_scores以题目当前resolution_set_time和scheduled_close_time相对于finalize_time过滤。
3. scoring/models.py，Git blob 55de494c05828aa1fc9f0d692d5b2ef8a0345ccf，Leaderboard.finalized字段注明自动更新冻结、管理员手工更新例外。
4. posts/services/versioning.py，Git blob b8eb8966c84ccec353f8f05c3e3207e0eb4827fc，包含可选S3题目快照；开关取决于AWS_STORAGE_BUCKET_POST_VERSION_HISTORY，不能据此假定每个部署和每次变更均保留完整历史。
源码证据为DOCUMENTED_FIXED_SOURCE，数值情景为SYNTHETIC_E1，生产数据库、实际历史榜单及长期人生决策效果为NOT_VERIFIED。

## 2. 本轮新增机制：重新结算时间会影响历史排行榜的候选集合

固定代码显示，首次结算将resolution_set_time写为当前时刻；撤销结算将其设为None；再次结算重新赋予当前时刻。retrieve_question_scores在有finalize_time时要求两个条件同时满足：scheduled_close_time <= finalize_time，以及resolution_set_time <= finalize_time。finalize_time优先使用排行榜字段，缺失时可回退到项目close_date。

因此，一道原本在截止日前结算并有分数的题目，若在截止日后撤销并重新结算，按当前题目状态重新计算历史截止榜单时可能被排除。此为固定源码条件组合推导，不等于线上已发生错误结算。

关键限制：update_project_leaderboard在finalized=True且force_update=False时返回既有榜单条目，防止自动更新。管理员显式force_update或在未冻结榜单上重算，才需要考察上述过滤后的不同候选集合。不能将此机制写成已冻结榜单会自动改写。

## 3. 20项独立人工断言

用Python标准库datetime在不接入数据库的条件下复现日期门槛和finalized/force_update控制条件。人工情景：2026-01-10题目计划关闭，2026-01-20首次结算，2026-01-31榜单最终日期，2026-02-03撤销，2026-02-05再次结算。

| 查询截面 | 当前resolution_set_time | 对1月31日历史榜单的资格 |
| --- | --- | --- |
| 首次结算后 | 2026-01-20 | 符合日期过滤 |
| 撤销结算后 | None | 不符合 |
| 再次结算后 | 2026-02-05 | 不符合 |
| 再次结算后且改查2月底截止榜单 | 2026-02-05 | 符合 |

另核对边界等于截止时刻、迟关闭、缺少finalize_time、冻结榜单不自动更新、显式force_update可以进入重算路径，以及YES/NO/AMBIGUOUS/未结算的合成分数状态。20项断言全部通过，0失败。这里的人工分数0.7和负0.4仅用于区分不同结果版本，并非Metaculus实际分数公式。

## 4. 输入、状态、算法、反馈、隐私和费用

真实输入为带时间戳的用户预测、问题规则、计划关闭时点、实际结算时点、结果标签与排行榜配置。状态包括resolution、resolution_set_time、finalized、finalize_time及Score表。算法为既有严格适当评分和时间覆盖加权，加上榜单日期资格过滤。反馈包括个人得分和排行榜；用户可更新预测，管理员可撤销或重结算。可解释性较高，因为日期门槛和重算路径可从固定源码直接检查。权限上，普通认证账号只能获得API允许的历史字段，未确认全量结算事件链和历史榜单快照可公开导出。公开FAQ显示有免费使用情景，专用域可收费；本轮只用公开材料，没有新增开支。

局限：同一题目ID与当前结算字段不足以直接证明历史榜单所采用的结果版本；源码包含可选题目快照机制，不能据此推断快照完整性或可由普通API读取；Score删除重建路径不能单独证明其他归档机制不存在。没有真实PostgreSQL/Django执行、生产榜单比对、用户效果评估或独立外部验证。

## 5. 心理史学候选方法与后续

MKT057-C1：候选预测账本分别保存question_version、resolution_event_id、resolution_set_time、leaderboard_finalized_at和score_rule_version；在更正时保留历史资格截面。
MKT057-C2：区分“当时已知结果的评分”“采用今天最终结果的回顾评分”“正式冻结榜单”，禁止跨口径比较。
MKT057-C3：将自动冻结与管理员强制重算列为不同权限事件；审计记录仅保留必要的版本和变更证据。
MKT057-C4：将预测撤回、结算撤回、榜单重算和隐私数据删除视为不同事件，留给F轨后续安全研究。
MKT057-C5：以上仅为方法储备，不改变R073/PESEN冻结协议，不设唯一人生效用权重，不提前开发个人决策产品。

E轨本日E004已完成全轨实质审计；本轮另对R190新增结果作只读独立复算。F轨2026年第44周F002已完成，本轮不重复立项。

下一轮MKT058优先比较另一个开源预测或情景版本管理系统的结果版本事件、正式评分快照和可导出性；如继续Metaculus，优先检查可选题目版本快照的调用路径及测试覆盖，避免重复MKT056至MKT057。