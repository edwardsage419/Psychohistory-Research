# R292 科学报告：原239目录01-014 计划行为理论，感知行为控制与实际可行性的有限数学分离

日期2026-10-23 Asia/Taipei。此轮为原始候选01-014 Theory of Planned Behavior的独立补充研究R292。**只验收人工离散概率机制E1**，不构成真人行为E2或历史预测E3证据，亦不修改原239候选目录。

## 第一手理论依据、协议及限制

Ajzen (1991), *The Theory of Planned Behavior*, *Organizational Behavior and Human Decision Processes* 50(2):179–211, DOI https://doi.org/10.1016/0749-5978(91)90020-T，[作者本人提供的原刊获取页面](https://people.umass.edu/aizen/obhdp.html)。该理论考虑态度、主观规范和感知行为控制对意向的关系，也探讨意向与控制知觉如何与行为相关。本文的所有二值化、分数权重、潜在实际可行性F、结构门控B=I·F、控制校准系数都属于**研究团队新增的教学性人工结构**，并非原作者的实验公式、数据或校准结论。

[R292先行完整研究协议](../../protocols/R292_TPB_PERCEIVED_VS_ACTUAL_CONTROL_8_WORLDS_256_SOURCES_PRESCORE_FREEZE_2026-10-23.md)，冻结GitHub [eaec7179](https://github.com/edwardsage419/Psychohistory-Research/commit/eaec7179a52e01fa86130e7c496c620093205500)，先于源程序和结果。

## 原数据生成与数学计算

态度A、主观规范N、**感知行为控制C**独立均等取-1或+1。意向I与**实际可行性F**为二元变量，实际行为B=I F。I与F是在给定A,N,C下独立生成的两个变量，C和F保留不同含义，不假装感知能力就是真实能力。

四种冻结意向权重：(1,1,1) BALANCED、(1,1,2) CONTROL_HEAVY、(1,1,0) CONTROL_NULL、(1,2,1) NORM_HEAVY。每组分别交叉控制信息无效κ=0或有效κ=1，共8个人工世界，世界内完整穷举2^5=32个(A,N,C,I,F)原source，合计**256个带标签、联合质量为正的原来源**。

* P(I=1|A,N,C)=1/2+(aA+nN+cC)/16；
* P(F=1|C)=1/2+κC/4；
* P(B=1|A,N,C)=P(I=1|A,N,C) P(F=1|C)。

同一预测时间点，在尚未观察I和F时比较完整A,N,C预测、正确边际化C的TRA_AN预测、只知C预测和截距常量预测，评分统一Brier。

记μ=1/4+cκ/64；V_AN=(a²+n²)/1024；V_C=(c+4κ)²/1024；V_cross=κ²(a²+n²)/4096。独立解析式为：

* R_constant=μ(1−μ)；
* R_TRA=R_constant−V_AN；
* R_control=R_constant−V_C；
* R_full=R_constant−V_AN−V_C−V_cross。

**省略感知控制产生的精确额外风险V_C+V_cross**。主程序逐256条真实合成来源计算Fraction精确结果；另一个独立程序完全不导入主程序，重建所有联合概率、四策略预测、世界质量和风险，与解析式完全一致。

## 8个人工世界的最终输出

| 条件 | 控制可行性校准κ | 完整Brier风险 | 省略感知控制的额外Brier |
|---|---:|---:|---:|
| BALANCED | 0 | 189/1024 | 1/1024 |
| BALANCED | 1 | 689/4096 | 51/2048 |
| CONTROL_HEAVY | 0 | 93/512 | 1/256 |
| CONTROL_HEAVY | 1 | 337/2048 | 73/2048 |
| CONTROL_NULL | 0 | 95/512 | **0** |
| CONTROL_NULL | 1 | 347/2048 | **33/2048** |
| NORM_HEAVY | 0 | 93/512 | 1/1024 |
| NORM_HEAVY | 1 | 337/2048 | 105/4096 |

精确反例：当c=κ=0时，C既未进入意向也未携带F信息，模型完整条件下对行为没有额外预测价值；当c=0、κ=1时，C虽然没有进入意向方程，仍可作为F的**人工校准概率指示变量**，其额外Brier信息价值为33/2048。意向固定I=1时C=+1与−1的行为概率差在κ=1时是1/2，在κ=0时为0；意向I=0时行为皆为0。

这种分离是构造式概率推导，**没有证明现实感知行为控制能准确测量真实客观行为条件，也没有建立任何人的因果机制或外部预测效度**。即使原始文献有实证研究，本轮也没有重跑原论文受试者数据。R291 TRA仍为独立01-013项，本轮不将其算成新实证对照。

## 真正执行及来源保全

* [完整256条原始人工来源](R292_ALL_256_ORIGINAL_TPB_CONTROL_FEASIBILITY_SOURCES.csv)
* [全部8世界Fraction精确结果](R292_EXACT_CONTROL_RESULTS.json)
* [源CSV与结果JSON的SHA256机读凭证](R292_MACHINE_RECEIPT.json)
* [主Python程序及106项实际数学单测](r292_exact_planned_behavior.py)
* [不导入主程序的256条来源独立审计与14项逆向检验](../catalogue_audit/independent_r292_source_audit.py)

[CI run39912808354](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39912808354)三job completed/success，Python 3.11/3.12双环境各106主单测和14项独立审计；第三独立作业重算全部原来源、公式及SHA，并把完整人工源码数据永久归档在[GitHub main commit29c72816](https://github.com/edwardsage419/Psychohistory-Research/commit/29c7281617b45c9bb1d2a9b589cc64d138f18e34)。

正式状态：CLOSED_BOUNDED_E1_ARTIFICIAL_R292_TPB_CONTROL_FEASIBILITY。E2=0，E3=0。R073与PESEN v0.1继续冻结。原239全部学习、科学分级及独立验收后再统一分类，最后才开始熔炼。
