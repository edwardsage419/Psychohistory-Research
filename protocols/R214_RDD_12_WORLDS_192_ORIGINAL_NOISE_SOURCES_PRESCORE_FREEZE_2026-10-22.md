# R214 Regression Discontinuity Design（09-005）— 12世界×16随机扰动、192完整原来源与门槛连续性反例，评分前冻结
2026-10-22（Asia/Taipei）。真实原239目录09-005 Regression Discontinuity Design，P1。状态 PRESCORE_FROZEN_E1_ARTIFICIAL_SHARP_RDD_DISCRETE_GRID。

## 文献
Hahn, Todd & van der Klaauw (2001), *Identification and Estimation of Treatment Effects with a Regression-Discontinuity Design*, Econometrica 69:201–209，DOI https://doi.org/10.1111/1468-0262.00183 研究断点因果效应的局部识别。Imbens & Lemieux (2008), *Regression discontinuity designs: A guide to practice*, Journal of Econometrics 142:615–635，DOI https://doi.org/10.1016/j.jeconom.2007.05.001。McCrary (2008), *Manipulation of the running variable in the regression discontinuity design: A density test*, Journal of Econometrics 142:698–714, DOI https://doi.org/10.1016/j.jeconom.2007.05.005。此人工审计不实施作者的实际估计程序、真实调查、密度检验或一般大样本RDD理论。

## 事先固定的人工结构、四个原观察位置与完整噪声
固定运行变量四个带编号位置X=(-2,-1,1,2)，门槛c=0，没有任何单位观测正好X=0。固定确定分配D=1{X≥0}（sharp RD）。每世界有两潜在结果函数Y0(x)=b+s_left·x+q_left·x²若x<0；若x≥0则Y0(x)=b+s_right·x+q_right·x²+baseline_step；处理潜在结果Y1(x)=Y0(x)+tau，且**真因果效应**定义为同一x在门槛右极限附近的`Y1(x)-Y0(x)=tau`（两侧皆恒tau）。在存在baseline_step时，Y0的门槛左右极限差不为0，破坏RDD从观测跳跃识别tau的连续性条件。即便没有baseline_step，本实验只有远离门槛的离散x，线性外推若曲率变化也可能产生有限网格偏差；没有宣称给定稀疏网格可非参数识别真门槛效应。
每个x位置有独立等概率噪声ε_x ∈{−1,+1}；实际原观察Yobs(x)=Y_{D(x)}(x)+ε_x。16条有序完整四噪声向量，原条件来源概率1/16。四个ε互相独立、均值0、方差1，任何单次观测有4个（彼此独立的人工噪声）样本。每个世界都以**全16源完整期望**报告三估计器风险，不把16条互斥可能噪声来源说成16次真正独立现实试验。

锁定12个世界，表中依次字段为 (b,s_left,s_right,q_left,q_right,baseline_step,tau)，全部参数原固定整数：
1 FLAT_NULL (0,0,0,0,0,0,0)
2 FLAT_TAU_TWO (0,0,0,0,0,0,2)
3 LINEAR_CAUSAL_TWO (0,1,1,0,0,0,2)
4 LINEAR_NULL_SLOPE_TWO (0,2,2,0,0,0,0)
5 BASELINE_STEP_FALSE_CAUSAL (0,1,1,0,0,2,0) — 与LINEAR_CAUSAL_TWO**每个X上的实际观察均值完全一致**，但真实tau不同。这组在16原噪声源下全部观测分布亦完全相同。
6 NEGATIVE_CAUSAL (0,1,1,0,0,0,-2)
7 RIGHT_QUADRATIC (0,1,1,0,1,0,2) — Y0两侧极限连续，却因右侧曲率、固定四点线性外推存在偏差。
8 LEFT_QUADRATIC (0,1,1,1,0,0,0)
9 MATCHED_QUADRATIC (0,1,1,1,1,0,2) — 两侧曲率相同，线性外推误差抵消，不代表曲率不存在。
10 DIFFERENT_SLOPES (0,1,2,0,0,0,2) — 两侧不同斜率，基线仍于0连续，正确两侧线性外推可识别已知结构下的tau。
11 NEGATIVE_TAU_WITH_STEP (0,1,1,0,0,3,-1) — 观测跳跃仍2，真因果tau为−1，再证明连续性重要。
12 LEFT_CURVATURE_WITH_NEGATIVE_TAU (0,2,2,1,0,0,-2)。

合计12世界×16原独立噪声向量=**192条完整原人工来源**；每行保留世界、完整原潜在Y0/Y1四对真值、X和D、四个ε、实际四Y、三估计器、与真tau误差，概率1/16。四原观察值同一噪声来源下组成一条可能实现的样本，不是独立测试人群。

## 先行冻结三个估计器及准确损失
(1) GLOBAL：右侧两个被处理观察均值减左侧两个未处理观察均值，系数按X=(-2,-1,1,2)为(-1/2,-1/2,+1/2,+1/2)。可观察的右/左均值差本身未必是**门槛局部**因果效应。
(2) NEAREST：Yobs(+1)−Yobs(−1)，系数(0,−1,+1,0)。注意两点离门槛距离仍是1，非趋近极限，若存在斜率会产生偏差。
(3) TWO_SIDED_LINEAR：仅用左右各两个点分别拟合一条直线，外推到x=0左右两条直线的截距差 `[2Yobs(+1)−Yobs(+2)]−[2Yobs(−1)−Yobs(−2)]`，系数(+1,−2,+2,−1)。这里的平滑度是**额外函数形式假设**，不是数据自证。

每源对真tau计算（estimate−tau）²，逐16真原噪声完整Fraction平均每世界MSE，拆分exact bias²及噪声variance两项、独立权重平方之和验证：
 GLOBAL随机方差 Σcoeff²=1，NEAREST方差2，TWO_SIDED_LINEAR方差10。每源同噪声向量三法评分公平比较。两侧外推即使在正确线性世界无偏，也有相对更大的噪声方差：独立新来源MSE不是单调随复杂估计程序降低。
对每世界同时保存四格实际观测的完整16源频数/加权分布（可用于观测等价比较），真实左右极限`jump_in_observed_conditional_mean=tau+baseline_step`，从X±1/±2非参数可见数据**不能**凭空识别该真实极限；仅作为真结构审计标签。真潜在因果效应tau和baseline_step严格分开保存。

## 预先固定失败与局限
- LINEAR_CAUSAL_TWO与BASELINE_STEP_FALSE_CAUSAL的所有四X处Yobs完整分布逐来源完全相同，全部三个估计器及其预测分布相同，但真tau=2与0。这是缺连续性假设下**纯观察等价不能识别因果跳跃**的示范，不能说两者具有相同干预结构或有真正操纵running variable的外部证据。
- RIGHT_QUADRATIC中baseline_step=0且潜在结果在门槛处连续，但是四点两侧线性外推会因右二次项产生有限离散网格偏差；与经典有足够密集近门槛数据并适当带宽缩小的RDD渐近理论不同。
- 噪声独立±1、无样本真实单位选择过程、X位置数量左右固定2/2，没有任何关于McCrary意义上的**门槛密度跳跃**的观测可实施测试；不能把一张人工网格中的baseline_step自动归因于真实个体操纵。
- 不包括 fuzzy RD, many thresholds, time varying, running variable measurement errors or real human/historical exogenous evidence.

## 验收
纯标准库 Fraction, ≥30测试; Python3.11/3.12两测试jobs均success，第三真正生成12世界主结果JSON、192条完整原原潜在与噪声/观察数据CSV、SHA收据，并经第三job核验12、192、来源概率、三法噪声方差与数学身份、两世界全观察等价后永久写入main。所有通过且正式科学报告存在后状态可为 **CLOSED_BOUNDED_E1_ARTIFICIAL_SHARP_RDD_DISCRETE_GRID**。仅人工E1，新增真人E2=历史E3=0。R073和PESEN v0.1冻结。下一真实原239目录**09-006 Difference in Differences**，拟R215。仍按原R完成后归纳分类、最后熔炼。
