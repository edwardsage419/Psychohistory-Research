# E024 R187三级观察后验收研究的594项独立只读审计

日期：2026-10-26（Asia/Singapore）。轨道：operations。状态：COMPLETE_BOUNDED_READONLY_WITH_OPEN_GATES。写前 main HEAD `d3d23f2cc7fd2b020c20d8c58222fa2708256fb8`。当日E004已完成全轨实质日检。本轮只读新增范围：R187计算前冻结、原始来源、主收据、B轨收据、CI状态，以及新归档MKT055。未改写R、B、TH、C、D、F或共享索引。主动新增费用0，未启动CI或收费资源；账户整体账单与免费额度未核验。

## 1. 来源和提交先后

本轮检索 main 最近18次提交。R187新增计算前冻结提交 `9ae693193b166cd8ecfa86bd828f8cfaca4434e1` 早于主程序 `c06fb66dc190e7d835b2ecf6a74f4b943a32e2` 和主收据 `81040e1b5c2de18dd6517ebfbba19e6fe9929df7`，B轨程序和收据在后。之后主报告 `248ba7cb9af763a35fba918a3e9bd9df282d5436` 与B报告 `9a6988a6d8e0c4e020d6b0a9574bd23672690ee7` 已归档。

冻结协议：`protocols/R187_ORDINAL_THRESHOLD_COARSENING_POSTSCORE_PRECOMPUTATION_FREEZE_2026-10-26.md`，Git blob `0f15383da3295f331c257b27dcc04b978d0cec28`。原始来源 `research/R187/R187_EXACT_RESULTS.json`，Git blob `6b1602aec4327d66b0586e8fba771306a8efcc62`。主收据 `research/validation/R187_ORDINAL_THRESHOLD_COARSENING_54_EXACT_RECEIPT_2026-10-26.json`，Git blob `4f1030eb0c75e2486d41f52ffdca33cdb7503832`。B轨收据 `research/evidence_audit/B_R187_ORDINAL_HISTOGRAM_AUDIT_RECEIPT_2026-10-26.json`，Git blob `57b5b426d0b2b51e5967e17965317bd82882e433`。以上SHA均由GitHub连接器实时读取核对。

## 2. 独立复算方法和结果

本轮在独立JavaScript BigInt有理数实现中直接读取R187原始12条来源结果，从六种人工机制各取m=3的唯一三级真PMF。未调用R主程序或B程序。对于m=1、2、3，完整三级通道枚举3^m个有序序列，两个累计阈值二元通道各枚举2^m个有序序列。逐序列相乘生成两组概率，精确计算TV=1/2∑|P0−P1|、Bayes错误率=(1−TV)/2。

共54组，每组执行6项原始PMF分数身份比较、2项概率归一化、1项TV比较、1项Bayes错误率比较和1项有序支持数比较，总计 **594项通过、0项不一致**。其中原始PMF身份324项，独立分布质量和指标270项。与主收据54组精确分数完全一致。

关键独立核验：
1. NULL在全部9组条件中TV=0。
2. CROSSED_THRESHOLDS在m=1时完整三级TV=4/15，两个二元阈值均为2/15。
3. COMPRESS在m=1时完整三级TV=1/6，低阈值TV=1/6，高阈值TV=0；高阈值的组别差异完全丢失。
4. 六个人工机制中，PARALLEL_UP在m=1时低阈值TV=1/6、高阈值TV=2/15；PARALLEL_DOWN恰好反向。
5. 本轮的54组复算只验证固定人工分布和指定TV指标，不是独立真人预测评价。

## 3. 新增治理发现：TV摘要不足以验收阈值身份

B轨归档的故意交换低阈值和高阈值负对照，在18个源×m条件中只有9个TV数值发生变化。另9个条件中两种阈值的TV相同，摘要层面无法检出标签互换。

这一限制在CROSSED_THRESHOLDS更为重要：m=1时两阈值TV同为2/15，然而原始组别累计概率差方向相反。以group1减group0为方向，低阈值Y≤0为+2/15，高阈值Y≤1为−2/15。只检验TV大小将丢失方向。该情况已由冻结原始真PMF直接复核。

登记 `E024-01 OPEN_METHOD_STRENGTHENING`：如后续需要严格验证通道身份，原研究轨应新增对每个阈值的组别累计概率、方向和通道标签的绑定检查，并使用交换标签的人工负对照。当前冻结协议仅要求至少一类非交叉源检出互换，既有结果满足该有限要求，因此本项为**可加强的审计覆盖缺口**，不宣布现有R187验收失败，也不擅自修改冻结协议或B轨结果。

## 4. CI、证据等级及其他开放事项

对主收据提交 `81040e1b5c2de18dd6517ebfbba19e6fe9929df7` 查询GitHub关联workflow runs得到空数组，combined status亦为空数组。查询接口有范围限制，故只能认定本次新增计算的远端CI PASS尚未证实，不能推断仓库从未运行CI。

R187本次后验收研究仍为 `INTERNAL_MATH_E1`，新增真人E2=0，历史E3=0，外部独立团队复现=0。原R187正式有界验收与本次新问题分开登记。B轨的54组直方图复核及222种直方图配置已归档，本轮独立验证采用有序序列枚举，未执行B轨的全部变异测试。

原有问题继续开放：R181冻结交付文件名和脚本语言偏离说明；R073第二真人重复博弈独立数据适配与留出评分；R136原冻结负对照、R170全状态比较、R175来源工作簿、R176后期复算、original239剩余审计。未进行全仓哈希巡检，不能宣称所有协议或所有提交已核验。

MKT055已新增并读取远端文件，路径 `research/market/MKT055_PREDICTIONBOOK_RETROACTIVE_SCORE_TIMESERIES_AND_EXPORT_LOSS_2026-10-26.md`，本轮仅作为市场知识候选，不改变R轨。F轨2026-W44 F002已经完成，维持本周单专题去重，不额外写入F轨。

## 5. 下一步

E024-02 CLOSED_BOUNDED：R187固定来源54组有序观察的594项独立精确核对。
E024-03 OPEN_CI：新增提交远端CI成功状态未证实。
E024-04 OPEN_LEGACY：R181、R073及其他历史开放事项仍待原研究轨或独立审计处理。
E024-05 COST_SCOPE：主动新增费用0；账单及GitHub免费额度未独立核验。

下一轮E优先检查R188新实质结果；若没有新增，核对R187阈值方向负对照或R181交付偏离说明。继续坚持R系列完成后归纳分类、最后模型熔炼，不预设唯一人生效用权重，不提前开发个人决策产品。
