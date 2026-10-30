# MKT140 入样概率误设与 Beeminder Webhook 丢失反馈风险

日期：2026-10-30 UTC。目标键：(market,MKT140,none,inclusion-probability-misspecification-and-Beeminder-webhook-reconciliation)。状态：COMPLETE_BOUNDED_ARTIFICIAL_E1。沿用 R 系列完成后统一分类再熔炼的方向。

## 研究问题与固定人工设计

与 MKT139 互补。本轮保持原四群组规模 [1,2,3,4]、最终标签 [0,1,0,1]、独立真实入样概率 [3/4,1/2,1/2,1/4]，完整总体阳性率为 3/5。MKT139 已检验正确已知入样概率时的 HT 无偏性；MKT140 检查分析者错误设定入样概率的后果。

固定估计器 HT(q)=sum_i I_i n_i y_i / q_i / 10。真实设计中 I_i~Bernoulli(p_i)，分析者使用假设 q_i。独立群组的解析期望为 sum_i n_i y_i p_i/q_i/10，解析方差为 sum_i (n_i y_i)^2 p_i(1-p_i)/q_i^2/100。另逐一枚举16种群组入样世界，用 BigInt 有理数核对解析期望与方差。

| 分析者假设 q | E[HT] | 对真值3/5的偏差 | 设计方差 | 均方误差 |
| --- | --- | --- | --- | --- |
| 全部正确 p | 3/5 | 0 | 13/25 | 13/25 |
| 所有群组均 1/2 | 2/5 | -1/5 | 4/25 | 1/5 |
| 所有群组均 3/4 | 4/15 | -1/3 | 16/225 | 41/225 |
| 所有群组均 1/4 | 4/5 | 1/5 | 16/25 | 17/25 |

即使估计量的方差或 MSE 更小，也不能推断入样概率正确或总体推断无偏。例如全部假设3/4时 MSE=41/225，小于正确概率时的13/25，但偏差达到 -1/3。所有结果只适用于本人工独立入样模型。

### 概率不确定性敏感界

如果每个分析者采用的 q_i 只能确定落在真实 p_i 的 0.8 至 1.2 倍之间，则以真实 p_i 为固定设计概率，对这一候选 q 集合的 HT 设计期望范围为 [1/2,3/4]。该区间是针对假设概率误设的人工敏感性范围，绝非95%统计置信区间，也不构成真实未知 p_i 可由数据识别的证据。实际应用中真实 p_i 通常未知，不能用这个示例的真 p 作为可用输入。

## 实际执行、反例与证据等级

归档程序：research/market/mkt140_inclusion_misspecification_exact_20261030.js。2026-10-30 在隔离 V8 实际执行，四套假设各枚举16世界，解析公式逐套核对，18项断言通过，5项非法概率/数组输入被拒绝。程序源已归档；原生 Node CLI 和 GitHub Actions 均未执行。E1 人工精确算术，NONBLIND，E2真人预测0、E3历史独立证据0、外部独立复现0。无需购买或运行付费资源。

## 产品机制深读：Beeminder

一手资料：
1. https://help.beeminder.com/article/41-can-i-export-my-data
2. https://api.beeminder.com/
3. https://www.beeminder.com/money
4. https://www.beeminder.com/premium

官方帮助文档确认，用户可导出 CSV/TSV，或通过 API 获取全部 datapoints。系统可在新增数据时调用 Webhook，但官方明确提醒 Webhook 失败可能没有可见告警，建议定期读取全部 datapoints 进行同步核对。API 记录包含时间戳、daystamp、updated_at、requestid、origin；requestid 支持同目标范围内的幂等写入或更新，diff_since 支持按更新时间增量查询。这些是官方文档支持的功能，不代表每个用户的端到端传输已经被独立验证。

输入：用户目标及历史 datapoints、第三方自动采集与 API 写入。状态：目标进度曲线、数据点、更新时间、承诺金额及脱轨状态。反馈：目标偏离后的提醒和承诺金额机制。自我修正：历史 datapoint 可更新；Webhook 可能漏报，需要周期性全量对账。算法：公开 API 说明幂等及增量机制，未取得可复算的长期人生预测算法。解释性：曲线和目标数据可查，未来决策效用权重未公开验证。隐私：API 使用认证令牌，Webhooks 需外部接收端；本轮未核验供应商内部权限与实际删除效果。费用：官网显示 Core 0 美元/月，其他会员 8/16/81 美元/月；Core 可能产生脱轨扣款，官方说明创建目标需付款方式。因此本项目不注册、不绑定支付方式、不启用 Webhook 或付费 API。

候选知识储备：数据同步必须同时保存 source_event_time、received_at、updated_at、requestid、source_revision、last_full_reconciliation_at；若增量链存在缺口，则标记 UNKNOWN，不直接将缺失反馈视为行为未发生。任何对用户真实人生效果的结论仍缺独立验证。

## 下一项

MKT141：研究 webhook 丢失与全量对账延迟对观察到的行为改善率的可识别界，保持人工 E1 先行。真实数据获取、付费试用和产品开发均不在本阶段范围内。零新增费用；GitHub 账单与免费额度未独立核验。
