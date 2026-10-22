# R212 因果有向无环图（09-003）：六种人工SCM与44个原外生来源，正式E1结题

2026-10-22。真实原239目录 **09-003 Causal Directed Acyclic Graph（P0）**。**CLOSED_BOUNDED_E1_ARTIFICIAL_SIX_DAGS**。

[正式科学报告](R212_SCIENTIFIC_REPORT_2026-10-22.md) · [原事前冻结协议](../../protocols/R212_DAG_6_SCM_WORLDS_44_ORIGINAL_EXOGENOUS_SOURCES_PRESCORE_FREEZE_2026-10-22.md) · [六SCM世界精确JSON](R212_EXACT_RESULTS.json) · [44条原来源和88个do干预结果CSV](R212_ALL_44_ORIGINAL_SCM_EXOGENOUS_SOURCES.csv) · [来源SHA机器验收](R212_FINAL_MACHINE_ACCEPTANCE.json) · [事后科研结题收据](R212_FINAL_ACCEPTANCE_STATUS.json) · [Python原生程序与38单测](r212_exact_causal_dags.py)。

六个独立人工因果图机制：共同原因CONFOUND、直接效果DIRECT、双路因果COMBINED、与混杂观察(T,Y)分布完全相同但真do效果不同的REVERSE_CAUSAL、COLLIDER碰撞点、MEDIATOR处理后中介。各图3/4节点、独立离散外生源，总44原来源，do(T0/1)同外生真正88个结局，全部原概率/两路do效应Fraction精确验收。关键反例：**CONFOUND与REVERSE的二元观察(T,Y)四格分布同为(3/8,1/8,1/8,3/8)，但真干预效应分别0与1/2**；COLLIDER观察T/Y总体独立，筛选K=1后观察差变−1/2；MEDIATOR真总效应1/2，但错误控制处理后的M会把总效应误写0。适用的前处理C后门调整与完整小图d-separation均单独核实，明确因果图已知是人工生成条件，无法由观察相关本身推出。

[GitHub Actions run39738558762](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39738558762) Python3.11及3.12各38项总76单测全成功，第三完整原来源/两路do效果与SHA归档job成功；[机器人原始数据提交e9f92f91](https://github.com/edwardsage419/Psychohistory-Research/commit/e9f92f91dcc155075c6ae7564f14b16a0f1a03aa)。

仅E1人工，有界方法学习；真人E2=0、真实历史E3=0，R073与PESEN v0.1冻结。下一真正原目录 **09-004 Instrumental Variables（P1）**，连续研究编号R213；全部R完成后统一分类，最后熔炼。
