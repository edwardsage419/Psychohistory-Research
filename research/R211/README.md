# R211 潜在结果框架（09-002）：256完整因果表、1536随机试验结果的E1结题

2026-10-22。真实原239目录 **09-002 Potential Outcomes Framework（P0）**。最终状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_BINARY_POTENTIAL_OUTCOMES**。

[完整科学报告](R211_SCIENTIFIC_REPORT_2026-10-22.md) · [原事前冻结协议](../../protocols/R211_POTENTIAL_OUTCOMES_256_SCHEDULES_1536_ASSIGNMENTS_PRESCORE_FREEZE_2026-10-22.md) · [256真因果世界精确结果JSON](R211_EXACT_RESULTS.json) · [1536完整原随机化观测来源CSV](R211_ALL_1536_ORIGINAL_RANDOMIZED_OBSERVATIONS.csv) · [256条非随机选择反例原来源CSV](R211_ALL_256_NONRANDOM_SELECTION_COUNTEREXAMPLES.csv) · [原数据SHA机器验收](R211_FINAL_MACHINE_ACCEPTANCE.json) · [正式结题状态](R211_FINAL_ACCEPTANCE_STATUS.json) · [纯Python及34单测](r211_exact_potential_outcomes.py)。

四个带编号的人工单位各有四种二元潜在结果类型，完整4^4=256个有序真因果表；每表C(4,2)=6个等概率处理分配，一共1536条人工真实因果表×可能单次随机观测，外加256条“按真实基线结果选择处理”的故意混杂世界。对全部256真表，随机均值差的设计期望精确等于真有限ATE、设计方差逐Fraction符合完整Neyman公式；但**每一份单次观测四人各只见一个结果，均有16个相容完整因果表，无附加假设的ATE集合宽度必为1**。额外个体无伤害单调性虽可缩区间，却在原1536条来源中有558个违反假设的真来源组合令真ATE被缩后界限排除。真`00|00|11|11`和`01|01|10|10`两个人工世界的处理/对照人口潜在边际相同且ATE都0，但个体效应平方均值分别0和1。真ATE0的`00|00|11|11`若故意高基线挑两人处理，可呈现虚假的实测均值差1。

[GitHub Actions run39737678033](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39737678033) Python3.11/3.12各34单测合计68通过、第三完整原结果SHA归档job success，[机器人原数据提交c76315f8](https://github.com/edwardsage419/Psychohistory-Research/commit/c76315f883d5cad709d376ac8951dd9ec0feeb54)。只有人工因果数学E1，新增真人E2=0、历史E3=0，R073与PESEN v0.1冻结。

下一真实原239目录条目 **09-003 Causal Directed Acyclic Graph（P0）**，连续研究编号R212。继续原全部R研究后再归纳、最后熔炼。
