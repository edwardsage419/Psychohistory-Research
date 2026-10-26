# MKT056 Metaculus 计划评分区间、提前结算截断与历史回顾评分边界

日期：2026-10-26（Asia/Singapore）。轨道：market。状态：COMPLETE_BOUNDED_OFFICIAL_SOURCE_AND_SYNTHETIC。前序MKT055已研究PredictionBook的历史结算结果回填；本轮研究另一套公开预测平台对提前结算和固定评分区间的明确处理。起始main HEAD `9e6141b8edf3f7c8144586b4e7cd303827ce0909`。主动新增费用0，无账号注册、产品购买、付费API、线上预测提交、真实敏感数据或Actions运行。

## 1. 产品和一手资料

对象：Metaculus。主要官方英文资料：

1. 评分官方说明（2026-10-26核读）：https://www.metaculus.com/help/scores-faq/ ，明确对每个预测按实际持续时间加权，分母使用预定关闭时间减开放时间；提前结算后到原计划关闭时段计零分；另有spot score、Baseline和Peer分数。
2. 官方问题与结算FAQ：https://www.metaculus.com/faq/ ，可提前关闭，支持适当情况下重新结算，预测默认在题目生命周期10%后自动撤回（可在设置调整），撤回前成绩保留。
3. 官方API说明：https://www.metaculus.com/api/ ，2026年现行访问分层，登录用户可访问自己的预测和分数；普通认证用户无法获得全部聚合历史、选项历史及所有已结算题目的内容/结果，部分字段返回null。
4. 官方免费参与证据：https://www.metaculus.com/bridgewater/contest-rules/ ，指定赛事可使用免费账号参加，无须购买；专用域及某些服务可能收费，见FAQ，不能据此宣称全部服务永久免费。
5. 官方开源源码固定版本 `68db27f800271d952ca01017a4a6a94f8c36fdd3`：
   * https://github.com/Metaculus/metaculus/blob/68db27f800271d952ca01017a4a6a94f8c36fdd3/scoring/score_math.py （Git blob `6ebc0491cf39f27099a128777966b3ec1c3f2d3c`）
   * https://github.com/Metaculus/metaculus/blob/68db27f800271d952ca01017a4a6a94f8c36fdd3/questions/services/lifecycle.py （Git blob `c67950c88567e2b6cf256fcd5e86a1f161002ce6`）
   * https://github.com/Metaculus/metaculus/blob/68db27f800271d952ca01017a4a6a94f8c36fdd3/questions/utils.py （Git blob `6961e1a4c23c10489d69673f0e69cf9f1dc35c45`）
   * https://github.com/Metaculus/metaculus/blob/68db27f800271d952ca01017a4a6a94f8c36fdd3/tests/unit/test_questions/test_views.py （Git blob `5f4e6a191148ed0c9902da01022ce93a9a5425e0`），存在预测到期自动撤回测试。
6. 官方评分方法讨论：https://www.metaculus.com/notebooks/20027/scores-and-medals-trade-offs-and-decisions/ ，解释对尾部事件偏好log score和持续更新的动机；为平台方法立场，不是独立证明长期人生决策收益。

## 2. 真实新增机制：提前结算后继续保留计划评分分母

固定源码 `evaluate_forecasts_baseline_accuracy` 明确设置 `total_duration = forecast_horizon_end - forecast_horizon_start`，其中 `forecast_horizon_end = question.scheduled_close_time.timestamp()`；有效预测结束时间取 `actual_close_time` 和该预测的 `end_time` 较早者；`forecast_coverage = forecast_duration / total_duration`；二元题单段Baseline为 `100*log2(2*p_outcome)`，再乘覆盖比例。问题生命周期代码在结算时更新实际关闭时间。上述结论是固定源码直接支持，非产品宣传推断。

因此，提前结算不会把历史评分的分母缩短为实际存续时间；剩余区间按零分处理。这使得相同预测概率、相同最终结果，在不同提前结算日期或撤回时点下产生不同的总分。该机制与MKT055 PredictionBook的历史结果回填属于不同问题，不能直接把两套平台的分数比较为同一指标。

## 3. 独立合成数学检查

用Python标准库 `math.log2`，人工设定：题目第0日开放、第10日计划关闭、第4日提前结算，用户从第0日提交YES概率0.8。二元Baseline单时点 `100*log2(2*0.8)=67.8071905113`。

| 人工条件 | 得分 |
| --- | ---: |
| 第4日结算YES，错误地以4日为分母 | +67.8071905113 |
| 第4日结算YES，按10日预定时长加权 | +27.1228762045 |
| 第1日自动撤回且未重新提交，仍在第4日结算YES | +6.7807190511 |
| 第2日首次提交0.8，第4日结算YES | +13.5614381023 |
| 第4日结算NO，预测0.8全程有效 | −52.8771237955 |
| 0.5概率预测且最终YES或NO | 0 |

17项独立人工断言全部通过，0失败。测试检查覆盖率、早结算、撤回、迟提交、两种结果、无预测、边界和常数基线。该模拟没有启动Django/PostgreSQL，也没有访问Metaculus账号，属于 `MARKET_E1_SOURCE_AND_SYNTHETIC`，不能称为线上集成验证。

## 4. 历史已知评分、回顾性评分和重结算

官方文档允许在适当情况下重新结算，`questions/services/lifecycle.py` 有 `score_resolved_question` 统一更新评分的逻辑。历史时点尚未有结算结果时，当时可计算的已结算评分样本可能为空；事后采用最终结果重新评价该时点的历史预测，则属于回顾性评分。若YES改为NO，上述人工0.8预测从+27.1229变为−52.8771，表示**在相同评分公式下结果标签变化的数学后果**；未执行线上重新结算，不能据此宣称所有线上排行榜都会以同样方式历史改写。

Metaculus通过固定计划分母控制提前结算激励，但API访问分层意味着普通研究者可能拿不到完整聚合历史或全部题目历史版本。可访问自己的预测和分数不等于可以完整重建全平台榜单；需要明确数据可用性、权限和历史版本覆盖。

## 5. 产品机制映射、限制与零费用

输入：概率预测、预测时间、撤回/再确认、题目及结算标准、计划和实际关闭时点。状态：问题类型、开放/计划关闭/实际关闭/结算时间、预测起止、结算标签、用户和聚合预测。算法：对数严格适当评分、时间覆盖加权、Baseline/Peer/spot分数，部分社区聚合。目标：提高群体预测准确性并激励及时更新；反馈为分数、排行榜和预测历史。自我修正：用户更新或撤回预测，管理员更正题目和结果。解释性：评分公式公开，历史可重建性受权限和数据导出范围约束。隐私权限：个人预测可由认证用户查询，完整聚合历史有权限门槛；没有全面审查日志、删除、备份和第三方接收者。费用：基础参与有官方免费赛事证据，专用域/服务可能收费；本轮只阅读公开英文资料和源码，未开通任何账户。

缺口：没有长期个人生活效用目标、多目标冲突约束、人生情景模拟或个体因果效果实验。营销和平台设计主张仅作 `OFFICIAL_CLAIM`；公开API规范和固定源码为 `DOCUMENTED_SOURCE`；17项人工计算为 `SYNTHETIC_E1`；真人长期决策收益、真实生产数据库和外部复现为 `NOT_VERIFIED`。

## 6. 未来候选方法与E/F联动

MKT056-C1：明确区分 `forecast_at_t`、`known_outcomes_at_t`、`retrospective_outcomes` 三种信息截面。
MKT056-C2：每个评分记录绑定 `scheduled_close_at`、`actual_close_at`、`resolution_version`、`forecast_start/end`、`score_rule_version`；历史修订保留前后分数和审计链。
MKT056-C3：将预测撤回、预测到期、授权撤销和删除敏感数据分别建模，防止“撤回预测”被误报为“删除个人数据”。
MKT056-C4：每次导出声明字段权限、隐藏聚合、版本历史、覆盖区间和缺失原因，禁止以公开榜单代替独立可复现证据。
MKT056-C5：上述均为候选知识，不更改R073/PESEN等冻结协议，不提前开发个人决策产品，不设唯一人生效用权重。

E轨当日E004已完成全轨检查；本轮追加R189最新数学收据的独立审计。F轨2026-W44 F002已完成撤销和数据生命周期专题，本轮不重复创建。MKT056新增的“预测撤回与隐私删除不同义”列为F003候选案例。

下一轮MKT057：审查Metaculus公开源码中评分版本、重结算历史与API导出之间的身份绑定，或切换另一个开放项目进行跨产品可重建性对照。所有费用维持零新增。
