# R181 置换检验：六群组随机化与错误事件级置换的42,000记录精确误报率报告

日期：2026-10-21。原目录P0/08-005 Permutation Test。科学状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_RANDOMIZATION**。全部数据来自原R177已验证的人工来源PMF，不含真正随机化试验参与者或真实历史政策记录。

## 理论来源、零假设和预冻结

Fisher (1935), [The Design of Experiments](https://books.google.com/books/about/The_Design_of_Experiments.html?id=-EsNAQAAIAAJ)奠定实际随机分配下的精确检验；[Imbens and Rubin (2015), Chapter 5](https://www.cambridge.org/core/books/abs/causal-inference-for-statistics-social-and-biomedical-sciences/fishers-exact-pvalues-for-completely-randomized-experiments/23AF990D2EF9C90D0A424D555FACE578)正式区分Fisher所有单位效应均为零的sharp null与其他平均效应假设。[Cameron, Gelbach and Miller (2008)](https://doi.org/10.1162/rest.90.3.414)指出组内相关及少群组推断的困难，该原文的cluster bootstrap t并非本次置换法。

[研究开始前冻结协议](../../protocols/R181_EXACT_SIX_CLUSTER_RANDOMIZATION_42000_PROFILES_PRESCORE_FREEZE_2026-10-21.md)于 commit `f65d3ab0d2e2563cb7b9a096df0b0d81c0a31678` 先于结果评分入库。沿用R177已通过字节与SHA验收的人工计数生成器，其源程序Git blob SHA1 `2d032513ce84141214b6b3f84df9c0ed9976a02b`，结果SHA256 `57410cf2c110ce3117b7af72e4b7473cee0c3ffd013e6fb99fd43de62165a535`。每组四次潜在事件，六群组彼此独立，同组允许事件相关；源机制为独立BIN、BB浓度2/8、ZIB结构零1/8或1/4，p=1/4或1/2，共**10个独立人工生成情景**。

人为把所有六群组的**处理结果与对照结果设置为严格相同**，所以这里所有单位处理效应都恰好为零，是Fisher sharp null严格成立的人工测试台。真正的随机分配是在六群组中等概率选三个处理组，C(6,3)=20个均匀方案，整个组内四次事件随群组一起移动。没有在24条原始事件层进行独立处理分配。

## 检验统计与两套相互独立的方法

每次给定群组计数K1至K6、固定总成功次数S和真实随机分配的处理组成功次数T。对处理与对照组成功比例的差异只看绝对统计`|2T−S|/12`，两个置换方案必须使用相同的统计量：

1. **正确群组Fisher双侧随机化检验**：在真正可分配的20种群组处理分配上全部枚举处理组总成功次数T，并计算同等或更极端`|2T−S|`的随机化概率。以独立“六群组选择三个”的整数动态规划直接计算全部T概率，两种完整条件随机化PMF逐项Fraction相等。
2. **错误逐事件置换对照**：错误假定24次组内事件都可以独立重分配，其中12次属于处理。该假设下T的条件PMF为`C(S,T)C(24−S,12−T)/C(24,12)`。与另一种从24个含S个成功的事件中无放回抽12次的独立事件计数DP严格逐项Fraction相等。但此随机化方案从未出现在所设人工试验中，故它产生的p值缺乏正确的处理分配概率基础。

全部双侧p值纳入相等的同极端统计，拒绝阈值事先冻结为0.10和0.20。没有随机蒙特卡罗近似，也没有事后改变阈值。

## 完整零假设抽样空间

固定每个群组成功数可以是0至4，六组所有有序来源记录共有`5^6=15,625`种。由于六组独立同分布且实际处理等概率，使用对应**210个有序计数的无序多重集**、精确原组合排列系数 `6!/∏m_k!` 和对应真实源概率表示全部15,625种有序状态，没有把210个无序样本简单等权。每个真实来源机制分配到20个处理方案，总共210×20×10=**42,000条机器可读概率评价记录**，其中每条都含原始profile真概率、赋值真概率、正确与错误p值、四种拒绝判定。

通过全概率积分核验：每来源210个profile真实概率严格和为1，20分配条件概率严格和为1。每个固定profile在正确群组检验下的条件误报概率严格不超过名义α，10来源世界的实际误报率也没有超过10%或20%。这一可检验事实依赖**已经设定的真实群组随机化与sharp null**，无法自动应用于没有实际随机处理分配的历史观察数据。

## 全10种源机制在名义10%时的实际误报率

| 真边际p | 来源机制 | 正确六群组Fisher检验 | 错误24事件置换 |
| --- | --- | ---: | ---: |
| 1/4 | IID_BIN | 3.3648% | 4.4254% |
| 1/4 | CLUSTERED_BB_C2 | 4.4589% | 16.8115% |
| 1/4 | CLUSTERED_BB_C8 | 4.0667% | 8.3776% |
| 1/4 | INACTIVE_ZIB_Z1_8 | 3.8745% | 6.1283% |
| 1/4 | INACTIVE_ZIB_Z1_4 | 4.3530% | 8.6152% |
| 1/2 | IID_BIN | 3.8292% | 6.4033% |
| 1/2 | CLUSTERED_BB_C2 | 5.6576% | 20.1984% |
| 1/2 | CLUSTERED_BB_C8 | 4.5322% | 11.1329% |
| 1/2 | INACTIVE_ZIB_Z1_8 | 4.5086% | 12.5064% |
| 1/2 | INACTIVE_ZIB_Z1_4 | 5.2295% | 20.2301% |

在p=1/2、强群内依赖BB浓度2下，正确置换误报率5.6576%，错误逐事件置换误报率20.1984%，即实际零效应也可能被错误假设赋予过度显著性。与此同时，当真实组内事件独立时，错误事件置换在此设置下的误报率仍不超过名义10%；**错误分配单位造成的失配并不意味着每个世界都必然反保守**。名义20%的十组对照也在机器JSON中完整给出，不因结果不同而省略。

### 事先固定的直接反例

当六群组数为`(0,0,0,0,4,4)`，实际随机分配选中两个含4成功的组与一个含0成功的组时，S=8、T=8。正确群组随机化总数20，双侧极端结果出现8次，所以`p_group=8/20=2/5=0.4`。错误24事件超几何分配模型计算的双侧概率为`10/7429≈0.001346`。**同一批人工观测可能在错误单位置换下给出显著结果，而正确设计的Fisher检验不拒绝。** 这是真实完整概率的数学反例，不是一个模拟软件随机种子造成的巧合。

## 独立复现与科研证据归档

Python 3.11与3.12各完成28种自动化单元测试，合计**56次实际单元测试执行且全部成功**。测试包含来源SHA、每个group profile的20项赋值和独立组选择DP一致、从0到24个成功事件的超几何组合与顺序抽取DP逐概率一致、profile原始排列倍数及来源总概率=1、组层sharp null拒绝上界、预设反例、非法输入失败、处理与对照补集恒等。第三个CI job单独真实执行全部42,000行概率穷举、来源权重审计、三份永久文件SHA和ZIP内部完整性。[GitHub Actions39558955703](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39558955703)三个job全部success，原始结果归档提交[40d07a3](https://github.com/edwardsage419/Psychohistory-Research/commit/40d07a38fb61a476d360575b830f7b431d08e83d)。

* [R181_EXACT_RESULTS.json](R181_EXACT_RESULTS.json)：10来源世界下两类精确检验在10%/20%名义阈值的实际误报率、原始profile 000044反例及全部验收数据，SHA256`431269ed601731f8ce0c039327082451824ba9effa3d21462a086ccf315f86fb`。
* [R181_ALL_210_RANDOMIZATION_PROFILES.json](R181_ALL_210_RANDOMIZATION_PROFILES.json)：210个完整群组计数profile、20真实随机分配、每种处理组总成功次数的独立双算法完整PMF，以及正确和错误p值，SHA256`ef522253061b883a43f8f164cc8aa112fb26621db84fb3ac33c4b1fc6498bd84`。
* [R181_ALL_42000_SOURCE_WEIGHTED_ASSIGNMENTS.csv](R181_ALL_42000_SOURCE_WEIGHTED_ASSIGNMENTS.csv)：10种源机制×全部42,000带原始真实生成和随机分配联合权重的全量评价行，SHA256`0a5f7e400910f5b03a1a3396fed16a66fb0cfd712c76ca5442a3e8263b60168b`。
* [R181_FINAL_MACHINE_ACCEPTANCE.json](R181_FINAL_MACHINE_ACCEPTANCE.json)：完整一致性、来源哈希、成功归档及E1/E2/E3证据分级。
* [r181_six_cluster_exact_randomization.py](r181_six_cluster_exact_randomization.py)：四条独立计算通道、所有完整概率、28项测试。
* [R181_Six_Cluster_Exact_Randomization_42000_Assignments.zip](R181_Six_Cluster_Exact_Randomization_42000_Assignments.zip)：事前冻结协议、实际源码、全量原始记录及汇总报告的数据文件，确定性ZIP。

## 结果边界与下一研究

R181研究的是**人工Fisher sharp null且实际在六群组层完全随机赋值**的正确性。检验数据源来自预先给定的概率分布，不能把人工误报率推广为某个真实政策的统计显著性，也不能从此证明真实群组间无潜在干扰、任意行为可以随机化或任意观察研究满足群组置换可交换性。

R181科研等级仅人工E1；新增真人E2=0和外部历史E3=0。R073与PESEN v0.1保持冻结。下一R182 P0/08-006 Linear Regression（线性回归），须先核对原239目录与数据源，再执行原先先全部R系列后统一分类、最后熔炼顺序。
