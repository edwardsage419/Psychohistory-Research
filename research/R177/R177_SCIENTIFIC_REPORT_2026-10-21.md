# R177 概率分布族：四类有限计数生成机制的108世界精确概率评价

日期：2026-10-21。原目录 P0/08-001 Probability Distribution Families。正式等级 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_FINITE_PMF**，没有新真人E2或外部历史E3。

## 研究文献与范围

一手统计学材料为美国NIST的[二项分布定义](https://www.itl.nist.gov/div898/handbook/eda/section3/eda366i.htm)、[Beta二项分布与Pólya urn等价表述](https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/bbnpdf.htm)，以及[He等2015零膨胀二项统计论文](https://doi.org/10.1080/02664763.2015.1023270)。超几何不放回抽样使用标准组合计数公式。研究内容是按这些明确生成假设独立建立本项目的有限人工概率试验；没有实读或复算原作者社会行为原数据，也没有推断任何历史社会的真实生成机制。

[R177计算前冻结协议](../../protocols/R177_FOUR_FINITE_COUNT_DISTRIBUTION_FAMILIES_108_WORLDS_PRESCORE_FREEZE_2026-10-21.md)在模型评分前以提交 `c8feb4fbf4cb0933705c0e10524f5bc0d3eaf368` 正式进入main。

设n∈{4,8,12}、无条件单位成功均值p∈{1/8,1/4,1/2}，为四类分布分别选择3档内部结构参数。完整研究为 4分布×3次数×3基础p×3内部档位=**108个世界**；每个世界输出n+1个完整概率，合计**972个状态概率单元**。原生二项分布无第三额外参数，保留3份精确相同分布以检测冗余变量，故独特参数组合为90组，不将额外重复当作独立证据。

四个机制具有相同期望np，但内部依赖、总体抽样、隐藏零类型不同：独立二项BIN，正相关BetaBinomial BB，有限总体不放回超几何HG，及含结构零且将激活状态成功概率补偿为q=p/(1-z)的ZIB。每一组都经逐项Fraction验证均值恰好np、非负、概率和为1、理论方差与直接PMF二阶矩相等。

## 预先冻结的实际说明性对照

n=8，基础p=1/4，全部使用第一档内部参数。四分布在观察计数的期望值都精确等于2。

| 分布 | 内部参数 | 完整概率计算的精确方差 | 完整概率计算的精确P(X=0) |
| --- | --- | ---: | ---: |
| BIN | 固定p=1/4 | 3/2 = 1.5 | 6561/65536 ≈ 0.100113 |
| BB | 浓度c=2，alpha=1/2，beta=3/2 | 5 | 12155/32768 ≈ 0.37094 |
| HG | N=24，成功总体K=6，抽取8次 | 24/23 ≈ 1.043478 | 26/437 ≈ 0.059497 |
| ZIB | 结构零z=1/8，激活状态成功率q=2/7 | 2 | 151771/823543 ≈ 0.184291 |

上述说明性情景与其余107组同样由计算前协议锁定，不作后验有利参数筛选。所有27个(n,p,内部档位)的同均值横向对照中，均有 HG方差小于BIN、BB与ZIB方差高于BIN；HG零概率小于BIN、BB与ZIB零概率大于BIN。该差异来自被明确固定的生成机制，是人工理论分布的结构性质，不足以识别现实事件成因。

## 完全相同观测计数分布的两种机制

独立于108世界主网格，先冻结了n=2、p=1/2的机制对照：

* BetaBinomial，浓度c=2，beta混合权重alpha=beta=1，作为单位内相关重复观察。
* ZeroInflatedBinomial，结构零z=1/4，参与者条件成功率q=2/3。

两种机制的支持X∈{0,1,2}，在公式计算与独立逐次抽样动态路径中均严格得到
`(P0,P1,P2)=(1/3,1/3,1/3)`，因此E[X]=1、Var[X]=2/3完全相等。

这一反例在概率分布层面证明：给定**仅观察每单元总成功数X**的计数设计，潜在正相关重复试验与结构零混合能完全不可区分；若额外获得内部逐次顺序、结构零身份或外生干预信息，是否可区分属于新的观察方案问题。不能把全分布等价扩展为所有n、所有参数的普遍不可区分定理。

## 严格双算法验证与归档

方法A使用组合数、上升阶乘与封闭PMF函数；方法B使用每一次原始抽样的计数状态动态规划，分别独立执行抽后强化、不放回删除、二项独立和潜在零混合。**108组每个支持点完全有理数一致**，同时通过上述均值、方差和P0全量数学恒等式。

执行 **26个不同单元测试**，在Python 3.11和3.12各完成26次，共52次，全部通过。GitHub Actions [39553799453](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39553799453)另有单独第三job完整运行所有108分布，复核结果SHA256、逐项独立算法相等、972个完整单元、反例、确定性ZIP，**三job全部success**。主要结果由Actions提交 [127ff6c](https://github.com/edwardsage419/Psychohistory-Research/commit/127ff6c087e64694ded7d2eb7ede4becf3668d9e) 到main。

永久归档：

* [R177_EXACT_RESULTS.json](R177_EXACT_RESULTS.json)，108个完整精确PMF，972单元，全样本均值、方差、P0、证明反例；SHA256 `57410cf2c110ce3117b7af72e4b7473cee0c3ffd013e6fb99fd43de62165a535`。
* [R177_FINAL_MACHINE_ACCEPTANCE.json](R177_FINAL_MACHINE_ACCEPTANCE.json)，模型数、通过条件、可复验SHA及无真实来源证据标记。
* [r177_four_finite_count_families_exact.py](r177_four_finite_count_families_exact.py)，完整两条独立算法、26种测试。
* [R177_Four_Count_Distribution_Families_108_Exact_Worlds.zip](R177_Four_Count_Distribution_Families_108_Exact_Worlds.zip)，含冻结协议、源码、机器验收和全部计算结果。

## 最终科研验收与边界

R177已正式验收为 **人工有限计数分布机制E1数学研究**：不同来源能够拥有相同均值却不同方差及无事件风险，甚至明确存在不同模型拥有完全相同一维计数PMF的事前反例。任何真人行为概率、跨文化机制、制度效果、冲突事件次数或历史预测的实证结果都没有本轮新增。不可将本轮概率模型本身标记为真人E2或独立历史预测E3，增量均为0。

下一项按原目录 R178 P0 / 08-002 Maximum Likelihood Estimation（最大似然估计）。R073及PESEN v0.1冻结。继续完成全部既定R模型，再统一归纳分类，最后模型熔炼。
