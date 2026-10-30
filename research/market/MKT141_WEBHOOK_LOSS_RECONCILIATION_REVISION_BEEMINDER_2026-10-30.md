# MKT141 Webhook静默丢失、全量对账延迟与历史修订

日期：2026-10-30 UTC。目标键：(market,Beeminder-API,MKT141-v1,webhook-loss-reconciliation-delay-and-revision). 状态：COMPLETE_BOUNDED_ARTIFICIAL_E1。研究顺序保持先完整R系列、再统一归纳、最后模型熔炼。

## 一手来源与产品证据

Beeminder英文官方帮助《Can I export my data?》于2026-09-24更新：https://help.beeminder.com/article/41-can-i-export-my-data 。官方明确提供CSV/TSV和API数据导出，新增数据可触发Webhook POST；Webhook失败可能静默发生，建议偶尔完整拉取所有datapoints。该说明属于产品文档支持，未独立运行生产Webhook。

官方API：https://api.beeminder.com/ 。用户端点支持diff_since，按创建或更新时间筛选目标和数据点；datapoint具有id、timestamp、daystamp、updated_at、requestid和origin；datapoints_count的最近条目按更新时间排序，历史日期的数据可能最近才录入。API也提供删除单个datapoint的操作。官方文档所见diff_since说明不足以保证所有删除事件都能通过增量查询可靠传播，因此删除检测需另行设计全量对账。此处“缺乏保证”是文档范围判断，不是已经验证的API缺陷。

输入：目标和数据点、第三方自动采集、用户手动修改。状态：日期、事件ID、更新时刻、目标进度及历史修订。目标与反馈：承诺进度、偏离提醒及失约扣款机制。算法：本轮只验证数据同步与确定性统计可行界，没有取得长期人生效用或因果改善算法。自我修正：按updated_at增量拉取与周期性完整快照比对，修订与删除分开处理。解释性：每条记录来源与可见时间需要在本地研究账本中保留。权限：API需要认证，外部Webhook接收端存在独立授权和副本风险，本轮未核验真实账户隐私设置。费用：官方存在免费基础会员与可能发生的失约扣款，本项目不注册、不绑定支付方式、不调用计费API。

## 人工E1实验与真实执行

程序 research/market/mkt141_webhook_reconciliation_exact_20261030.js，远端Git blob f5a6bca9ae9a75625286486cebe93a7448db06b5。使用12个固定人工事件，前后两期各6个；真实原始成功数分别为5和3。Webhook只到达前期2条（成功1）及后期4条（成功3），其余6条静默丢失。

Webhook视图：前期成功率1/2，后期3/4，观察差为正1/4。按预先固定每期6个应观察位置、缺失标签允许0或1，完整总体差的确定性可行区间为负1/3至正2/3。此时“观察到改善25个百分点”无法确定真实总体方向。

首次完整对账：前期5/6，后期3/6，真实差负1/3。由此出现观察改善而真实下降的人工反例。随后上游把后期一条成功标签从1修订为0：本地未更新时仍报告负1/3，按updated_at成功对账后为负1/2。再模拟上游删除前期一条失败记录，完整快照发现该位置缺失；保持固定预期6个位置并将其标记UNKNOWN，前期真实可行率5/6至1，后期2/6，总体差区间负2/3至负1/2。删除是否改变合法统计总体需要预先定义，此处固定研究位置仅作安全示例。

已从远端重新读取归档JavaScript并在隔离V8执行：12项正向断言通过，4项非法输入被拒绝。原生Node.js CLI、真实Webhook传输、生产API和GitHub Actions均NOT_RUN。该实验是人工E1、内部非盲态，E2真人样本外预测0、E3历史独立验证0、外部团队复现0。区间为确定性可行界，绝非95%置信区间。人工固定12个位置的可见性先验不能默认推广至未知真实事件总数。

## 候选设计与限制

未来候选数据合同分别记录source_event_id、event_time、source_updated_at、received_at、source_revision、last_full_reconciliation_at、deleted_or_missing、expected_universe_provenance。Webhook成功不能单独证明无漏报；增量拉取不能单独证明删除已传播；历史修订不能冒充原评价时点已知信息。快照完整性与来源新鲜度分开标记，过期或无来源证明时保留UNKNOWN。

该机制适用于所有依赖外部反馈的量化工具。对长期人生决策的实际效用、Beeminder用户真实改善率和因果效果没有推断资格。未新增费用，未取得GitHub账户账单与免费额度证据。

下一项MKT142：研究在总事件数未知时，Webhook丢失率的可识别界和来源完整性证明，优先对比公开免费API文档，不购买服务。