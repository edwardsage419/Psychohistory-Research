# R214 回归不连续设计（09-005）：12人工门槛世界与192个完整原噪声来源

日期2026-10-22（Asia/Taipei）。严格对应原239目录**09-005 Regression Discontinuity Design（P1）**。科学状态**CLOSED_BOUNDED_E1_ARTIFICIAL_SHARP_RDD_DISCRETE_GRID**。此项只是自造四点固定门槛数据的数学机制审计；新增真人E2=0、真实历史E3=0。

## 原始研究依据与事前冻结

Hahn, Todd and van der Klaauw (2001), [Identification and Estimation of Treatment Effects with a Regression-Discontinuity Design](https://doi.org/10.1111/1468-0262.00183), *Econometrica* 69:201–209，提供门槛因果识别分析。Imbens and Lemieux (2008), [Regression discontinuity designs: A guide to practice](https://doi.org/10.1016/j.jeconom.2007.05.001), *Journal of Econometrics* 142:615–635，讨论正确局部估计与实际实施。McCrary (2008), [Manipulation of the running variable in the regression discontinuity design: A density test](https://doi.org/10.1016/j.jeconom.2007.05.005)，关注运行变量操纵及门槛附近密度跳跃的识别威胁。本项目没有执行任何原论文实证研究/原作者程序，没有取得运行变量门槛附近任意小距离的真实密集观测，也**没有实施McCrary密度检验**。

在计算全完整来源之前冻结[12个世界、16原扰动、三种估计器及因果违例口径](../../protocols/R214_RDD_12_WORLDS_192_ORIGINAL_NOISE_SOURCES_PRESCORE_FREEZE_2026-10-22.md)，提交[2f697e74](https://github.com/edwardsage419/Psychohistory-Research/commit/2f697e74ee80cb5b4f5a7c00c7a76971bf40f936)。冻结全部下列人工生成参数、估计器线性权重、条件概率、数学检验与真实因果目标，不在评分后修改研究来源。

## 真结构、独立原噪声与观察信息权限

固定四个不同单位的位置X=(-2,-1,+1,+2)，门槛c=0；实际接受处理D=1{X≥0}，是sharp RDD且**没有任何位置正好位于门槛**。每世界一对连续坐标意义下的固定潜在结果函数：当x<0时`Y0(x)=b+sL·x+qL·x²`；当x≥0时`Y0(x)=b+sR·x+qR·x²+baseline_step`；每个x处理潜在结果`Y1(x)=Y0(x)+tau`。真正人工恒定处理因果效应为tau，但如果baseline_step≠0，未处理潜在结果在门槛处本身不连续，门槛两侧实际观察均值的真结构跳跃为`tau+baseline_step`，不能独立解出tau。

每个单位有**独立等概率**噪声ε∈{−1,+1}、方差1，实际观测`Yobs(x)=Y_D(x)+ε`。四个噪声的全部2^4=16个完整有序原来源逐一枚举，每世界来源概率1/16，12世界共**192条完整人工原观察来源**。每条保留四个原潜在处理/未处理真值（只供oracle审计）、四个真实ε、对应四个实际观察值、三估计器、每种估计相对真tau的平方误差。噪声是4名人工单位之间独立随机来源；**16组互斥可能扰动向量并不等于16次实际独立真人重复实验**。所有估计器只读每来源同一组真实可见Yobs与固定X，不准使用潜在未观察反事实、原tau、baseline_step或独立噪声源确定拟合权重。

## 三个固定估计器及其真正平方误差

按X=-2,-1,+1,+2原顺序，估计器固定：

1. **GLOBAL**：两右侧被处理观察均值减两左侧对照观察均值，线性权重(-1/2,-1/2,+1/2,+1/2)。目标是两侧已观测远离门槛水平的汇总差，不自动等于门槛处的因果效应。
2. **NEAREST**：位于门槛两侧最近实际观测位置差`Y(+1)-Y(-1)`，权重(0,-1,+1,0)。距离仍然为1，无法模拟极限趋于0。
3. **TWO_SIDED_LINEAR**：各侧恰两个样本分别拟合直线，截距差`[2Y(+1)-Y(+2)]-[2Y(-1)-Y(-2)]`，权重(+1,-2,+2,-1)，额外假设所选距离范围内局部线性近似合理。

全16原扰动来源每条真实平方损失`(estimate−tau)^2`以精确Fraction平均得到MSE。逐世界双路核验：每个估计器真正噪声平方方差等于其四个独立扰动的线性权重平方和；全来源平均MSE等于人工真期望偏差平方+真噪声方差。对应方差严格为**GLOBAL 1、NEAREST 2、TWO_SIDED_LINEAR 10**。拟合更复杂并不单调提高独立外生噪声实现下的均方精度。

## 全部12种人工真世界的完整来源期望平方损失

|人工世界|真处理tau|未处理基线跳跃|GLOBAL MSE|NEAREST MSE|两侧线性MSE|
|---|---:|---:|---:|---:|---:|
|FLAT_NULL|0|0|1|2|10|
|FLAT_TAU_TWO|2|0|1|2|10|
|LINEAR_CAUSAL_TWO|2|0|10|6|10|
|LINEAR_NULL_SLOPE_TWO|0|0|37|18|10|
|BASELINE_STEP_FALSE_CAUSAL|0|2|26|18|14|
|NEGATIVE_CAUSAL|−2|0|10|6|10|
|RIGHT_QUADRATIC|2|0|125/4|11|14|
|LEFT_QUADRATIC|0|0|5/4|3|14|
|MATCHED_QUADRATIC|2|0|10|6|10|
|DIFFERENT_SLOPES|2|0|85/4|11|10|
|NEGATIVE_TAU_WITH_STEP|−1|3|37|27|19|
|LEFT_CURVATURE_WITH_NEGATIVE_TAU|−2|0|53/4|11|14|

所有12世界的**16来源原完整四观测联合分布**、真理论门槛处理效果、真未处理结果跳跃、真观察跳跃、每估计器均值、偏差、噪声方差、来源实际MSE及独立恒等式见[精确结果JSON](R214_EXACT_RESULTS.json)；192条真正原噪声、完整潜在真值与只可见结果另见[原来源CSV](R214_ALL_192_ORIGINAL_RDD_NOISE_SOURCES.csv)。

### 反例一：一样的观测联合分布，真实因果效果为2或0

LINEAR_CAUSAL_TWO的未处理潜在结果连续、实际处理tau=2、左/右基线斜率均1。BASELINE_STEP_FALSE_CAUSAL的实际处理tau=0，但未处理基线在x≥0突然增加2，且两侧斜率亦1。两世界四X点上实际**无噪声观察向量均严格为(-2,-1,3,4)**；因同四位置噪声来源独立同分，**全部16组完整四维实际可见观测联合分布逐有理数来源一致**。但是一个世界真因果tau=2、另一个真因果tau=0。所有只依据实际X,Y的估计程序不可能区分两者，却会遇到不同的真实因果目标。两侧线性外推在前者为真因果无偏、噪声方差/MSE均10；在后者仍输出观测跳跃2、对真tau的偏差2、MSE14。**观测跳跃等于因果效应依赖额外未处理潜在结果连续性假设**，而不能由此观察分布内部自动验证。

NEGATIVE_TAU_WITH_STEP世界baseline_step=3且真实tau=−1，却同样呈现观察跳跃+2，说明即使门槛观察结果看似向上，真实处理因果效果可以为负；并非暗示真实研究中门槛密度操纵已被观察到。

### 反例二：真实连续性成立，稀疏观测仍可能导致线性曲率外推偏差

RIGHT_QUADRATIC保持门槛未处理Y0左右极限相同（baseline_step=0），真tau=2，但在右侧Y0额外包含x²。在四个固定距离1/2处的线性截距外推，`2Y(+1)-Y(+2)`受到非线性项的**−2**偏差，导致两侧线性估计的人工真期望为0、相对真tau的偏差−2、完整源MSE=14。对应LEFT_QUADRATIC左侧二次项造成线性截距偏差+2，也得到MSE14。而MATCHED_QUADRATIC左右同曲率时，两侧外推中的二次项偏差在相减时恰好抵消，MSE回复噪声方差10；这不是说二次项本身已被消除或模型变得真实线性。

这个实验仅有x距门槛1与2，**没有**任何运行变量支持点按带宽缩小趋近于0，无法用这些固定数据模拟经典RDD平滑性下的非参数极限识别结果；只是展示有限稀疏设计必须额外承担外推形式风险。

### 反例三：简单估计器的偏差与方差，无法依方法复杂度简单排序

在完全没有斜率的FLAT_TAU_TWO，三个估计器均对tau=2无偏，完整来源MSE依次GLOBAL=1、NEAREST=2、两侧线性=10，复杂外推纯粹增加噪声方差。在线性但存在基线斜率2、真实tau=0的LINEAR_NULL_SLOPE_TWO中，GLOBAL估计因为两侧位置均值差包含远离门槛的斜率贡献，MSE=37；NEAREST MSE=18；线性外推由于正确线性结构无偏，MSE=10。**最优方法依人工结构和真效应目标改变**；这不构成真实人群预先选择带宽/阶数的性能推荐，也不等于本研究提供了任何真实独立历史E3的预测增益。

## 代码执行与严格归档验收

[原生Python Fraction代码与39项测试](r214_exact_sharp_rdd.py)，全部四节点16扰动、12人工世界、三种固定估计器、原真反事实和完整观察联合来源、偏差与方差和MSE双途径验证。GitHub Actions [run39740585568](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39740585568)，Python3.11、3.12分别**39项测试全部成功、共78次**，第三作业真实产生全部12世界主结果、192条原完整噪声来源、逐世界概率和为1、三估计器噪声方差及所有SHA核验，机器人原结果提交[af59326b](https://github.com/edwardsage419/Psychohistory-Research/commit/af59326bd3990d83e94e1d490ce5e839f2d5d3ce)永久写回main，三个CI作业success。

归档可独立核验：
* [评分前冻结协议](../../protocols/R214_RDD_12_WORLDS_192_ORIGINAL_NOISE_SOURCES_PRESCORE_FREEZE_2026-10-22.md)；
* [全部原12世界完整计算JSON](R214_EXACT_RESULTS.json)，SHA256 `c4b5ba7fbc8d4371a3c796e8bffb3890a286be9c114318bd4f3f2ee6b8a03465`；
* [全部192条原人工独立扰动来源CSV](R214_ALL_192_ORIGINAL_RDD_NOISE_SOURCES.csv)，SHA256 `60456784a0d985af5e5f82568862cc1839cf9961632825456ef4cd8a545b957d`；
* [原数据和来源数SHA机器验收](R214_FINAL_MACHINE_ACCEPTANCE.json)；
* [本研究事后正式有限E1验收收据](R214_FINAL_ACCEPTANCE_STATUS.json)，明确所有数值仅支持人工数学结论。

**R214=CLOSED_BOUNDED_E1_ARTIFICIAL_SHARP_RDD_DISCRETE_GRID**。本研究提供的是RDD模型识别假设及带宽外推风险的人工机制学习，不得称作对任何真实研究RDD有效性、门槛操纵密度或历史因果效果的经验验证。新增真人E2=0、真实历史E3=0；R073、PESEN v0.1保持冻结。按真实原239项目录下一条为**09-006 Difference in Differences（P1）**，拟登记R215。维持先完成全部R目录再归纳分类、最后熔炼。
