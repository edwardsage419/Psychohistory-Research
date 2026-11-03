# MKT236补充：PNAS正式全文的建议采纳与因果识别边界

track: market
run_date_utc: 2026-11-03
target_key: (market,PSA-judicial-advice,PNAS-2025-e2505106122,fulltext-identification-and-adoption)
baseline_main: d669b3204d2da62518ce18a27c02980541fc027d
status: COMPLETE_BOUNDED_FULLTEXT_READING
evidence_grade: MARKET-E2_PUBLISHED_HUMAN_RCT; NUMERICAL_RECALCULATION_ONLY_FOR_PUBLISHED_TABLE1
participant_data: NOT_ACCESSED
native_replication: NOT_RUN
CI_dispatch: NOT_RUN
billing_checked: NOT_VERIFIED
source: https://imai.fas.harvard.edu/research/files/ai.pdf (PNAS 2025, published 2025-09-17, pages 2–4, Table 1, Theorem 1)
related_prior: research/market/MKT236_AI_JUDGE_RANDOMIZED_NULL_AND_HUMAN_OVERSIGHT_ACCURACY_2026-11-03.md

## 实际增量

正式全文Table 1给出无建议组法官与PSA建议的四格人数510、195、89、149，合计943；有建议组543、162、70、173，合计948。无建议组与PSA一致为(510+149)/943=69.88%；有建议组为(543+173)/948=75.53%；按原表四格人数直接算术差为5.65个百分点。论文正文报告采纳一致性增加约5.6个百分点，标准误2.0个百分点。该变化表示法官更常与建议一致，不能当作决策准确性提升。

PSA输入为既往犯罪记录九项因素及年龄，输出FTA、NCA六级风险和NVCA二值风险；DMF结合风险及辖区资源生成现金保释或签名保释建议。具体模型参数与生产实现未在本轮运行核实。法院实际保释决定也不等同于最终是否获释。

研究的可识别性依赖：建议展示的随机化/条件无混杂、分配概率重叠、单盲排除直接影响、跨案件无干扰。因保释决定会改变能观察到的后续结果，存在选择性标签。正式全文Theorem 1识别的是有无AI建议的人类分类损失**差值**；单独各组的绝对分类风险通常不可点识别。AI独立决策在原试验中没有被随机实际执行，作者给出相对性能的界限。主要判据基于签名保释下潜在结果Y(0)，无法自动代表完整社会福利或所有潜在结果。

作者在该研究环境中报告提供建议未显著改善分类准确性，PSA独立决策的分类性能较差。建议一致性提高与准确性未改善可以同时成立。此处没有从论文图表重新提取全部损失估计、置信区间或附录；不可宣称完成全量数值复算。

## 方法与商业价值

将“用户看到建议”“用户采纳建议”“实际选择质量”“后续真实结果”作为四个不同评价指标。未来对高风险个人决策辅助研究，需预先指定错误成本、随机展示策略、识别未观察反事实的假设和公平性分组；真实人生福利指标仍须单独验证。司法PSA研究不直接验证任何商业个人规划产品。

## E/F只读协调与限制

E: 本轮读取main HEAD与MKT236历史报告，PR搜索仍显示12个开放Draft、无合并；未重算完整待核队列，净变化UNKNOWN。R272此前报告的Python子进程隔离P0保留OPEN，未重复开展B数学审计。
F: F010本周既有完成登记保留；本轮只提出建议采纳率与决策质量分离的评估问题，不新增F专题，不读取私人资料。
No paid service, no workflow dispatch, no CI, no frozen protocol change, no cross-track write.
Next: 检查论文附录和公开复制档案的免费访问及具体损失估计；在没有合法免费原始数据和清晰复制授权时仅作只读方法审查。
