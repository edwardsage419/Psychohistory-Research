# 心理史学原239候选：R299无模型RL有限数学E1完成，历史R063范围保全与v1.3来源目录

日期2026-10-23 Asia/Taipei。目标保持不变：先完成全部原R模型研究，再统一归纳分类，最后模型熔炼。**239项全局科学正式结题尚未成立**。

## R299有限研究

原目录02-005 **Model Free Reinforcement Learning**（P1），新增专属主研究R299：[完整科学报告](../research/R299/R299_SCIENTIFIC_REPORT_2026-10-23.md)与[正式机读科学验收](../research/R299/R299_FINAL_ACCEPTANCE_STATUS.json)。原作者理论锚Sutton(1988), *Learning to Predict by the Methods of Temporal Differences*, DOI https://doi.org/10.1007/BF00115009；Sutton & Barto第二版 *Reinforcement Learning: An Introduction* Chapter6。

[事前协议f8885c13](https://github.com/edwardsage419/Psychohistory-Research/commit/f8885c130b2d6d12280cd6ace30085b3ad90e835)先于源码结果。将固定策略两步S0→S1→终端奖R的人工时序设置R∈{0,2}、γ∈{0,1/2,1}、α∈{1/2,1}和TD0_ONLINE/MC_FULL_RETURN两个更新，完整计算**24人工世界、120完整状态原source**，每source含两状态更新前后价值、TD误差、回报目标、状态预测误差与闭式解。实验没有任何真人或动物主体。

冻结精确对照：R=2、γ=α=1/2、训练4回合后，TD0对更早状态S0的估值为**11/16**、Monte Carlo估值为**15/16**、两者更晚S1估值同为15/8、S0真实策略回报为1。在线TD0使用前一回合S1价值更新更早状态，蒙特卡洛使用完整已知回报。这只是固定人工序列的延迟信用分配例子，并不说明真实人体的RL强度、实际随机预测效度或TD/MC一般算法优胜。

[完整120行原source CSV](../research/R299/R299_ALL_120_ORIGINAL_MODEL_FREE_TD_MC_STATES.csv)、[24世界结果JSON](../research/R299/R299_EXACT_MODEL_FREE_TD_MC_RESULTS.json)、[来源/结果SHA256凭证](../research/R299/R299_MACHINE_RECEIPT.json)、[不导入主程序的独立重算源码](../research/catalogue_audit/independent_r299_source_audit.py)已提交。**GitHub Actions run [39927231561](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39927231561)** 三个job completed/success，Python3.11+3.12各492项主unittest和16项独立来源审计，第三独立job复算120行并永久归档至[commit8f74e565](https://github.com/edwardsage419/Psychohistory-Research/commit/8f74e56573be6a9fde21e12bb886c9f041d3f74b)。正式边界**CLOSED_BOUNDED_E1_ARTIFICIAL_R299_TD0_MC_FIXED_POLICY**。新真人/动物E2=0、历史E3=0。

## R063历史数据证据保留与防止重复

[原R063证据审计](../research/R063/R063_EVIDENCE_AUDIT.md)针对Najar等(2020)真人社交模仿强化学习metaVS/VS2，实读原作者MATLAB机制、复核Fig6作者汇总拟合数据及精确统计；本体并未完成trial CSV本地SHA端到端回算，也未形成固定条件完整独立预测验证。R299研究Sutton的**一般无模型状态价值预测更新**，不是R063已有真实实验的第二次独立人群复现；R063源关联仍保留在02-005旧证据列表中，不因有R299主要关联而消失或升格。

R297 Q Learning 02-003及R298 Model Based RL 02-004原有各自主R关联保持原样。它们的模型关系不会生成新的E2证据或新增真人样本量。

## 原始239项目录证据覆盖

| 来源分类 | v1.2（R298后） | **v1.3（R299后）** |
|---|---:|---:|
| 已建立原候选主R研究来源链接 | 186 | **187** |
| 共享数学但不独立主R | 3 | **3** |
| 旧有限范围来源，无专属主R | 5 | **4** |
| 检查材料未找到逐条关联 | 45 | **45** |
| 尚待确立候选主R研究来源 | 50 | **49** |
| 239原始唯一候选目录 | 239 | **239** |

[全239行来源证据交叉索引v1.3](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.3_2026-10-23.json) 相对[v1.2](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.2_2026-10-23.json)**仅02-005一行科研来源字段变更**，保留该行R063既有审计路径；原始239模型ID、名称、顺序和P1/P2优先级完全未改。[当前49项待核P1/P2队列](ORIGINAL_239_PENDING_49_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv)：P1 **22**，P2 **27**。链接覆盖187条仍**不等于187项原始真人心理学论文得到独立预测复现**。

[239行、旧R063和SHA机读独立校验源码](../research/catalogue_audit/verify_p1_r299_crosswalk_v1_3.py)及[GitHub Actions run39927488591](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39927488591)，三个作业completed/success，Python3.11/3.12各16项目录测试，第三次原始source/目录独立复验，验证仅一行改变及R063证据保留。区分科研有界接受与纯归档完整。

## 后续

下一个P1原目录编号**02-008 Hidden Markov Model**。需要明确隐藏状态、状态转移、观测发射、过滤和隐藏路径推断的可识别性限制，先行冻结独立数学任务和观察数据证据范围。随后继续完整R系列；最后统一分类，之后模型熔炼。R073、PESEN v0.1继续冻结，个人辅助决策系统继续暂缓。
