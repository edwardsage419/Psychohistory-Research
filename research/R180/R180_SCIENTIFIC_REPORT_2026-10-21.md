# R180 Bootstrap 自助法：30个生成机制世界与7750个完整观察样本的精确有限群组审计

日期：2026-10-21。原冻结候选目录 P0/08-004 Bootstrap。科研状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_BOOTSTRAP**。本报告中的真实覆盖和抽样方差都指**人工已知生成机制下的完全穷举理论量**，没有人类观察数据或历史外推证据。

## 一手统计学基础与源模型

Efron (1979), [Bootstrap Methods: Another Look at the Jackknife](https://doi.org/10.1214/aos/1176344552)引入经验分布再抽样估计方法。Davison/Hinkley (1997), [Bootstrap Methods and Their Application](https://doi.org/10.1017/CBO9780511802843)系统论证重抽样设计。Cameron/Gelbach/Miller (2008), [Bootstrap-Based Improvements for Inference with Clustered Errors](https://doi.org/10.1162/rest.90.3.414)讨论群内相关与少群组推断的困难。本项目设计的是两种基本重抽样、简单有限m修正的Wald区间和未调整百分位区间；**未复算这三项来源的真实数据或Cameron等人的更复杂cluster bootstrap t方法**。

计算前[冻结协议](../../protocols/R180_CLUSTER_BOOTSTRAP_30_WORLDS_7750_SAMPLES_PRESCORE_FREEZE_2026-10-21.md)于`f2e935da4a3c3b478c619c86ca721d3e1de73948`提交main，早于R180计算结果。来源为R177原生人工分布程序、Git blob SHA1 `2d032513ce84141214b6b3f84df9c0ed9976a02b` 及完整结果SHA256 `57410cf2c110ce3117b7af72e4b7473cee0c3ffd013e6fb99fd43de62165a535`，每次实际研究执行均验证原字节和双算法输出。

每群组4个潜在二元试验机会，m=2、3、4个**群组之间独立**，同群内部可以有相关性或结构零风险。p=1/4、1/2为固定真边际成功率，五种源计数机制是独立二项BIN、Beta二项浓度2与8、零膨胀二项结构零1/8与1/4。合计30个机制世界，每世界列举所有有顺序群组计数 `(K1,...,Km)∈{0,1,2,3,4}^m`，共有10×(25+125+625)=**7750份人工完整观察样本**。每份样本以真实联合概率`∏P(Kg)`精确加权，全部概率用Fraction保存。

## 两种基础bootstrap，四种固定95%名义区间

1. **逐次独立经验重抽样（IID_BOOT）**：把4m次潜在二元行为视为独立经验观察，抽取4m个二元结果。每份观察样本的自助成功总数，分别由封闭二项PMF公式和真正逐次动态计数独立算出，两路所有概率逐项Fraction相等。
2. **保持完整群组经验重抽样（CLUSTER_BOOT）**：从实际m个群组中有放回等概率抽取m个完整群组。两路分别直接枚举所有m^m个群组编号抽取序列，与m步计数DP重建同一完整条件成功数PMF，全部120种不重复群组计数配置严格一致。
3. 有限群组条件bootstrap原生方差`V_cluster*`，单独报告修正后的`m/(m−1)*V_cluster*`。在全部30世界用**真正的原始有序样本分布**精确积分，证得原生组重抽样方差在重复抽样中的期望为`(m−1)/m*Var(p_hat)`，经固定修正后的期望恰好等于真实抽样方差。**这项无偏性属于方差估计的期望值，绝不保证单个观察数据的方差正确或区间覆盖95%。**
4. 固定四种区间：IID普通Wald区间，群组修正Wald区间，IID经验bootstrap未调整百分位区间，完整群组bootstrap未调整百分位区间。Wald覆盖均由有理数平方不等式验收，百分位为累计bootstrap PMF首个达到2.5%或97.5%的离散总成功数边界。不用数值随机近似、事后最优模型挑选或无限次蒙特卡罗模拟。

## 事前冻结m=4、p=1/4的真实人工覆盖率

| 固定人工生成过程 | E[IID自助方差] / 真抽样方差 | IID Wald实际覆盖 | 群组修正Wald实际覆盖 | IID百分位实际覆盖 | 群组百分位实际覆盖 |
| --- | ---: | ---: | ---: | ---: | ---: |
| IID_BIN | 93.75% | 90.939% | 90.158% | 92.905% | 90.158% |
| CLUSTERED_BB_C2 | 43.75% | 74.798% | 80.855% | 79.146% | 80.887% |
| CLUSTERED_BB_C8 | 68.75% | 85.353% | 86.772% | 88.409% | 86.772% |
| INACTIVE_ZIB_Z1_8 | 81.25% | 88.459% | 88.115% | 90.922% | 88.115% |
| INACTIVE_ZIB_Z1_4 | 68.75% | 85.210% | 85.754% | 88.263% | 85.754% |

这是事前统一规定的五种模型全体对照。强组内相关时，IID错误经验重抽样的期望方差仅为真实方差43.75%，导致两类未正确建模群组结构的区间覆盖率低。保留群组后覆盖有所改善，但仍未达到95%；在独立数据和某些零膨胀设置，群组修正区间覆盖也可以低于IID区间。**本研究不支持“群组bootstrap总是更好”这样的无条件结论。**

## 结构性有限样本失败与精确验收

无论真实原始群组计数分布是否有非零抽样方差，若实际m个群组在某次观察中刚好具有相同K值，完整群组经验重抽样所见结果均为同一个值，`V_cluster*=0`，修正后仍为0。此类样本事件在全部30个真实人工生成机制中有正概率；其准确概率按`sum_{k=0}^4 P(K=k)^m`验算。故**重抽样单位正确不代表少群组样本一定有充分可识别的误差信息**，这是本研究明确的数学负对照。

研究还验证：全30个世界中`E[p_hat]=p`、`MSE(p_hat)=Var(K)/(16m)`、四种区间覆盖均通过原始有序样本概率的全量求和，没有依赖生成随机数。全部条件bootstrap PMF保存了120种不重复群组计数组合的完整精确Fraction概率，各完整观察样本均保留对应profile引用及四种区间、概率和真假覆盖记录，可在独立程序中复算。

首次CI`39557961241`：两个Python环境测试通过，完整7750样本计算及全部数学恒等式通过，但档案压缩变量名错误造成最终job失败，**该次不计为成功结题**。随后只修复ZIP变量名，保留全部冻结科学协议、数学规则和失败原始提交轨迹；最终[GitHub Actions39558049744](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39558049744)两环境单元测试和完整计算/归档三job**success**，永久结果归档提交 [52a54fc](https://github.com/edwardsage419/Psychohistory-Research/commit/52a54fc2df5efd96f1c967dfc368c42c0f2ead17)。

## 实际归档证据与散列

* [R180_EXACT_RESULTS.json](R180_EXACT_RESULTS.json)，30世界完整真实均方风险与四区间覆盖、固定主对照、来源证据界限，SHA256 `8a94389b027f2015002fb81336970bb4f320867c0867696445f4fe1473d6b39e`。
* [R180_ALL_7750_ORDERED_SAMPLES.csv](R180_ALL_7750_ORDERED_SAMPLES.csv)，全部7750有序样本的概率、观察统计、三种自助方差、两类百分位端点和四种区间覆盖标记，SHA256 `f00d5a786fead011df080f67affbf1195ff2d5dc664133937e909a9237ed16e8`。
* [R180_ALL_CONDITIONAL_BOOTSTRAP_PMF_LIBRARY.json](R180_ALL_CONDITIONAL_BOOTSTRAP_PMF_LIBRARY.json)，全部120种无序计数组合与两类完整自助总计数条件概率，SHA256 `6348d713435148be25152ec7cfd1e61f9769b6c7cbebb6c0c5a28e77c9a8ace9`。
* [R180_FINAL_MACHINE_ACCEPTANCE.json](R180_FINAL_MACHINE_ACCEPTANCE.json)，源SHA、精确概率、数据行数与真实证据分级的机器验收。
* [r180_exact_cluster_bootstrap_finite.py](r180_exact_cluster_bootstrap_finite.py)，完整算法、条件分布枚举、独立DP及27种单元测试。
* [R180_Exact_Bootstrap_30_Worlds_7750_Samples.zip](R180_Exact_Bootstrap_30_Worlds_7750_Samples.zip)，全部源码、协议、JSON、原始CSV及机器验收确定性ZIP。

## 科研结论及下一研究

本轮只对**有限群组且已知生成概率的人工机制**证明重抽样方式与推断结果的联系。依赖结构可显著损害错误IID重抽样的方差估计；群组自助修正方差在研究给定条件下的期望可无偏，实际小样本区间仍有非理想覆盖、退化样本和离散边界问题。不能直接将上述覆盖率用于真实人类实验，也不能将它认作原始论文的实证复制。

科研等级正式为E1，新增真人E2=0、外部历史E3=0；R073和PESEN v0.1保持冻结。下一按原239目录进入 **R181 P0/08-005 Permutation Test（置换检验）**。仍然先完成全部R系列，最后统一归纳、分类、熔炼。
