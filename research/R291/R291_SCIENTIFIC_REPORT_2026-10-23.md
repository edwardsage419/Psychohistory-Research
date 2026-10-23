# R291 科学报告：原239目录01-013理性行动理论的有限人工意向中介检验

日期2026-10-23 Asia/Taipei。按既定R系列主线处理原目录P1缺口，不更改239项唯一原始候选目录。科研结论限定为**BOUNDED_ARTIFICIAL_E1**；无新真人E2及历史E3证据。

## 研究来源及模型边界

Fishbein, M. & Ajzen, I. (1975), *Belief, Attitude, Intention, and Behavior*, Addison-Wesley。[Ajzen本人提供的原著开放目录与章节入口](https://people.umass.edu/aizen/f%26a1975.html)，第7章意向形成、第8章行为预测。Ajzen & Fishbein (1980), *Understanding Attitudes and Predicting Social Behavior*，见[作者本人书目](https://people.umass.edu/aizen/pubstxt.html)。TRA的态度、主观规范、行为意向、行为路径有对应理论来源；**本研究的二值变量、线性概率、权重和合成负对照完全为本项目自定义**，不能作为原著参数或心理测量复算。

原目录01-014 Theory of Planned Behavior增加感知行为控制，是独立待研究条目。本研究没有偷偷添加TPB特征，也未在任何真人数据上估计规范影响。

[先于结果冻结的R291完整协议](../../protocols/R291_TRA_ATTITUDE_NORM_INTENTION_BEHAVIOR_8_WORLDS_128_SOURCES_PRESCORE_FREEZE_2026-10-23.md)，GitHub [commit161d40a0](https://github.com/edwardsage419/Psychohistory-Research/commit/161d40a01451f1e89be045910f95ec536768754c)。

## 冻结人工设计及两种独立计算

态度A和主观规范N独立均等取-1和+1，意向I与行为B均取0/1。四组权重分别为BALANCED(1,1)、ATTITUDE_HEAVY(2,1)、NORM_HEAVY(1,2)、NORM_NULL(2,0)，每组与完全意向中介MEDIATED或直接规范应激反例DIRECT_NORM_STRESS交叉，一共8个人工世界。16个(A,N,I,B)联合source/世界，完整128条人工数据。

冻结条件概率：

* Pr(I=1|A,N)=1/2+(aA+nN)/8。
* Pr(B=1|I,A,N)=1/4+I/2+dN/8，完全中介d=0，负对照d=1。
* 在意向尚未观察的实际预测时间点，Pr(B=1|A,N)=1/2+[aA+(n+2d)N]/16。

直接枚举128个精确Fraction联合来源，比较完整(A,N)、只用A、只用N、恒定1/2四个**同一预测信息时点**的Brier损失。独立计算的闭式式子为：

R_full=1/4−[a²+(n+2d)²]/256；
R_Aonly−R_full=(n+2d)²/256；
R_Nonly−R_full=a²/256；
R_constant−R_full=[a²+(n+2d)²]/256。

完全中介世界给定I时Pr(B|I,A,N)=Pr(B|I)；直接规范反例中同一个I、A条件下N=+1与-1的Pr(B=1)差恒为1/4。该条件独立与违反仅在设定的人工DGP中成立，**不能在现实观测数据上直接解释为因果机制已识别**。

## 八个世界的精确输出

| 权重配置 | 机制 | 全变量 Brier 风险 | 省略规范额外损失 | 省略态度额外损失 |
|---|---|---:|---:|---:|
| BALANCED | MEDIATED | 31/128 | 1/256 | 1/256 |
| BALANCED | DIRECT_NORM_STRESS | 27/128 | 9/256 | 1/256 |
| ATTITUDE_HEAVY | MEDIATED | 59/256 | 1/256 | 1/64 |
| ATTITUDE_HEAVY | DIRECT_NORM_STRESS | 51/256 | 9/256 | 1/64 |
| NORM_HEAVY | MEDIATED | 59/256 | 1/64 | 1/256 |
| NORM_HEAVY | DIRECT_NORM_STRESS | 47/256 | 1/16 | 1/256 |
| NORM_NULL | MEDIATED | 15/64 | **0** | 1/64 |
| NORM_NULL | DIRECT_NORM_STRESS | 7/32 | **1/64** | 1/64 |

主发现是给定意向后的条件独立在MEDIATED四世界严格成立，在DIRECT_NORM_STRESS四世界严格失败。尤其NORM_NULL基线的省略规范损失为0，增添冻结直接规范通道后变成1/64。这区分了“规范影响意向”与“规范在意向之外改变行动概率”的人工机械结构。最优完整Brier预测被设定为知道正确合成世界参数的oracle，不意味着真实行动场景中研究者事先知道这些参数。

## 科研验收及永久归档

* [完整128条带标签原始人工联合来源](R291_ALL_128_ORIGINAL_TRA_LABELED_JOINT_SOURCES.csv)
* [8世界全部分数精确结果JSON](R291_EXACT_TRA_RESULTS.json)
* [原数据与结果SHA256来源凭证](R291_MACHINE_RECEIPT.json)
* [主模型可执行程序和106项unittest](r291_exact_reasoned_action.py)
* [完全不导入主模型的独立来源重算与14项反例审计](../catalogue_audit/independent_r291_source_audit.py)

[GitHub Actions run39912378382](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39912378382) 三个job completed/success。双Python3.11/3.12各106个主程序单测及独立源审计，第三作业再次独立核查128原来源和所有分数表达式，永久归档[GitHub commit7c99ef05](https://github.com/edwardsage419/Psychohistory-Research/commit/7c99ef05424e4e2470dcba424d913882ef6a687a)。

正式研究状态：CLOSED_BOUNDED_E1_ARTIFICIAL_R291_TRA_MEDIATION. 无真人参与、无真实行为实验、无自然历史事件验证、无跨实验复现，也无原作者定量回归重算。R073/PESEN v0.1继续冻结。后续先核对目录01-014 TPB的旧材料，再冻结独立R292；所有R学习完成以后才统一分类与模型熔炼。
