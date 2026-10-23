# 心理史学：原239目录R291理性行动与R292计划行为分立研究，交叉索引v0.6审计

日期2026-10-23（Asia/Taipei）。本轮按原R主线继续独立学习，两项均是**有限人工数学E1**正式验收。未读取真人试验数据，无新的真人E2或历史E3。原239项目录未改变，用户既定先全部R→统一分类→最后熔炼的顺序不变。

## 两项理论文献、研究和分离

| 原239候选 | 原作者文献 | 先行冻结提交 | 完整人工源 | 双Python主真实单测 | 独立审计CI |
|---|---|---|---:|---:|---|
| 01-013 TRA | Fishbein & Ajzen (1975), https://people.umass.edu/aizen/f%26a1975.html | [161d40a0](https://github.com/edwardsage419/Psychohistory-Research/commit/161d40a01451f1e89be045910f95ec536768754c) | 128 | 106+106 | [39912378382](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39912378382)，三job成功 |
| 01-014 TPB | Ajzen (1991), https://people.umass.edu/aizen/obhdp.html | [eaec7179](https://github.com/edwardsage419/Psychohistory-Research/commit/eaec7179a52e01fa86130e7c496c620093205500) | 256 | 106+106 | [39912808354](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39912808354)，三job成功 |

[TRA正式科学报告](../research/R291/R291_SCIENTIFIC_REPORT_2026-10-23.md)及[正式验收](../research/R291/R291_FINAL_ACCEPTANCE_STATUS.json)：人工A/N→I→B中介结构下，完整意向中介时给定I后的规范条件效应严格为0；新增**预先冻结的人工直接规范路径**后该差为1/4，显示条件独立边界。TRA不是TPB；没有真人测量或实验因果结论。

[TPB正式科学报告](../research/R292/R292_SCIENTIFIC_REPORT_2026-10-23.md)及[正式验收](../research/R292/R292_FINAL_ACCEPTANCE_STATUS.json)：人工态度A、主观规范N、**感知控制C**作用于意向I，独立的潜在**实际可行性F**限制B=I F。若C对意向与F都不提供信息（c=0,κ=0），省略C的预期Brier损失为0；若C仅概率预测F（c=0,κ=1），完整模型相对不含C的模型损失优势为33/2048。全部为指定模拟概率下的精确计算，并不能由该数值推出真实控制感测量能力。

R291与R292的原作者来源、变量、计算、SHA256机器凭证和正式验收分别归档。不要把两种人工世界产生的性能数值当作交叉实验真人比较；也不能将“计划行为”误称为对同一R291数学试验的第二次独立验证。两者分别属于原目录不同候选。

## 来源审计与真实CI状态

* R291完整带标签人工原来源128条及第三独立源码重算：见[完整R291研究目录](../research/R291/README.md)，永久机器人归档[7c99ef05](https://github.com/edwardsage419/Psychohistory-Research/commit/7c99ef05424e4e2470dcba424d913882ef6a687a)。模型106×2真测试及独立审计均成功。
* R292完整256正质量人工原来源及第三独立源码重算：[完整R292研究目录](../research/R292/README.md)，永久机器人归档[29c72816](https://github.com/edwardsage419/Psychohistory-Research/commit/29c7281617b45c9bb1d2a9b589cc64d138f18e34)。模型106×2真测试及独立审计均成功。
* R291目录[239项v0.5全来源机器审计](../research/catalogue_audit/verify_p1_r291_crosswalk_v0_5.py)，CI [39912586564](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39912586564)三作业通过。
* R292目录[239项v0.6全来源机器审计](../research/catalogue_audit/verify_p1_r292_crosswalk_v0_6.py)，CI [39913041918](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39913041918)三作业通过。双Python各14项机读元数据核验和第三完全独立源数据审计，未改原239条候选，只有原01-014相对v0.5变动。

## 原239逐项证据v0.4→v0.5→v0.6

| 状态 | R290后v0.4 | R291后v0.5 | R292后v0.6 |
|---|---:|---:|---:|
| 已建立主R来源关联 | 178 | 179 | **180** |
| 共享已有R数学机制，不能重复计算 | 3 | 3 | **3** |
| 仅旧范围有限关联 | 5 | 5 | **5** |
| 现有核对材料无逐条关联 | 53 | 52 | **51** |
| 尚待确认主R关联的原始条目 | 58 | 57 | **56** |
| 原始模型候选总数 | 239 | 239 | **239** |

[唯一当前v0.6模型证据交叉索引](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.6_2026-10-23.json)与[剩余56项原目录证据待核队列](ORIGINAL_239_PENDING_56_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv)：P1=29，P2=27。180个主R候选链接是**真实目录关联计数**，不代表180项原论文已经真人复现、获得E2/E3、或整个239研究清单已经科学结题。剩余缺口也不能直接解释为“历史上从未学习”。

## 下一优先项

原目录下一个未确认P1为 **01-016 Schwartz Basic Human Values**。先核对早期知识包与历史研究，审核Schwartz 1992价值结构理论的原作者来源、不同价值类型和测量模型，再考虑R293所需的理论数学或可获得的真实测量复现。任何真实PVQ/ESS数据需先按来源、样本、量表版本、评分和许可独立审计；**不要从人工几何圆环证明真人价值结构**。R073及PESEN v0.1继续冻结；个人辅助决策系统仍暂停。
