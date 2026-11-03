# MKT239：承诺合同需求可能与真实自控需求错配

track: market
run_date_utc: 2026-11-03
target_key: (market,commitment-contracts,Carrera-et-al-2019-2022-N1248,selection-accuracy-versus-adherence-and-welfare)
baseline_main: a3a02d3b7f767f4c6cccc456fdc445215286f4a0
status: COMPLETE_BOUNDED_ABSTRACT_REVIEW
product_specific_effect: NOT_VERIFIED
evidence: MARKET-E2_ADJACENT_RANDOMIZED_HUMAN_EXPERIMENT_AUTHOR_REPORTED
fulltext_tables_and_original_data: NOT_RUN
R_E2_E3: NO_CHANGE
E_daily: E168_ALREADY_COMPLETE_READONLY
F_weekly: F010_ALREADY_COMPLETE_READONLY
CI: NOT_RUN
paid_services: NONE
account_billing: NOT_VERIFIED

## 研究增量及去重
MKT193、MKT229、MKT230、MKT238已覆盖 Beeminder 目标轨道、押金合同的采纳率与行为结果。本轮只审查一个尚未在上述报告核实的独立问题：用户愿意购买或选择承诺合同，是否意味着该合同针对其真实自控问题？避免再次重做产品机制或已有试验。

Carrera, Royer, Stehr, Sydnor, Taubinsky, *Who Chooses Commitment? Evidence and Welfare Implications*, NBER Working Paper 26161 (2019，2021修订)，2022发表于 Review of Economic Studies 89(3), 1205–1244。NBER公开摘要报告健身房实验 N=1,248，另行测量实际及主观感知的时间不一致。参与者对提高健身次数的合同有较高接受度，并观察到显著运动增加。然而，合同选择受到估值噪声和对自身时间不一致的错误信念影响。大约一半选择“提高到访”合同的参与者，也选择了“降低到访”合同。这个反向选择结果为“接受承诺合同代表真实偏好或正确自控诊断”提供直接反例。

原始摘要支持：合同选择可以与行为改善并存，同时合同需求的方向缺乏可靠性。不能从摘要推断所有接受者受损、福利效应的具体数值、统计显著性分组或 Beeminder 实际用户的因果效果。完整论文回归表、福利估计、随机化细节、原始数据和代码未在本轮复算。2022正式发表身份来自NBER所列出版记录。

另一个不同随机实验 Bhattacharya, Garber, Goldhaber-Fiebert (2015), NBER 21406，对4000余名有意签订运动承诺合同的人随机提示20周或8周合同；作者报告长期合同提示增加目标达成和后续续签，但其福利模型指出某些条件下干预可能降低效用。该研究已由MKT193/MKT229覆盖，此处只用于区分目标完成与福利，绝不作为新独立重复计数。

## 产品研究含义
Beeminder 官方产品机制已经由MKT229核验：用户输入目标、速率、datapoint和承诺上限，系统计算轨道、安全缓冲和违约后果。产品实际生产算法、用户层面因果改善和长期净福利仍未知。本轮没有注册、付费或运行产品。

未来评价应分别测量：(1) 是否主动选择合同；(2) 对自身自控偏差的预测是否校准；(3) 随机提供合同后的客观行为改变；(4) 合同方向是否与事前稳定偏好一致；(5) 经济损失、压力、退出及其他目标挤出；(6) 净福利及长期保持。不能把更高合同采纳率、更多运动或更高续约率直接当作人生决策改善。潜在跨文化、跨目标外推均 UNKNOWN。

## E/F只读
2026-11-03 E168 blob 6f47d589c072b148b732ac3f279d40352ca680c5 已完成。实时 main 检查时为 a3a02d3b7f767f4c6cccc456fdc445215286f4a0，protected=false；12个开放PR全部Draft，未见合并。R272生产工作流写权限、自动推送和未接入强制前像验收的P0风险保持 OPEN，未作B轨重复验证。旧队列154/P0 27/P1 82/P2 45属于既有快照，本轮没有重新逐行统计，净变化 UNKNOWN。F010 blob b703777cd33fc72197e0368cc2f209e51e5dc420 本周已完成。新证据支持研究自愿同意与错误自我诊断的区别，未新增F编号。

## 来源及执行界限
1. NBER 原始工作论文摘要与正式出版记录：https://www.nber.org/papers/w26161
2. NBER 2015 对照研究摘要：https://www.nber.org/papers/w21406
3. Beeminder 官方机制（既有MKT229）：https://www.beeminder.com/overview

英文公开来源，2026-11-03检索。没有实际参与者数据、个人敏感信息、人工模拟、生产执行、付费API、收费Actions或仓库工作流触发。所有实验结果是原作者报告，不是本轮独立复算。建议下轮转向非押金类真实产品的独立决策结果，避免继续在承诺合同主题上编号扩展。
