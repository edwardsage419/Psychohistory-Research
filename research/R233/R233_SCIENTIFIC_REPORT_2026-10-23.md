# R233 跨群体测量等值：八人工双群体量尺、256完整来源及潜在均值与题目截距不可区分

日期：2026-10-23（Asia/Taipei）。原239目录**10-007 Measurement Invariance（P0）**，科研状态 `CLOSED_BOUNDED_E1_ARTIFICIAL_CROSS_GROUP_MEASUREMENT_INVARIANCE`。没有真实不同文化、性别、地区、年代、语言群体的测验原数据，新增真人E2和历史E3均0。

## 原始文献与本研究限界

Meredith (1993), [*Measurement invariance, factor analysis and factorial invariance*](https://doi.org/10.1007/BF02294825), *Psychometrika* 58:525–543，出版方一手摘要区分弱、强、严格因素等值与测量偏差。Vandenberg & Lance (2000), [*A Review and Synthesis of the Measurement Invariance Literature*](https://doi.org/10.1177/109442810031002), *Organizational Research Methods* 3:4–70，原方法综述强调在群体潜在均值及结构关系比较之前检验量尺可比条件。本工作没有接入上述作者的真人问卷或实际多群组CFA最大似然估计、组间差异显著性检验，不宣称已经证明任何现实社会群体的测量公平性。

[计算前独立冻结协议](../../protocols/R233_MEASUREMENT_INVARIANCE_8_TWO_GROUP_WORLDS_256_ORIGINAL_ATOMS_PRESCORE_FREEZE_2026-10-23.md)在任何模型运行前提交[da25e504](https://github.com/edwardsage419/Psychohistory-Research/commit/da25e50497f41ab416e34c6a18ca4f6a74ff93bd)，然后提交模型代码与独立CI。全部结果来自冻结的三题、两组、八模型及原外生机制。

## 双群体原人工测量结构与观察/oracle严格区分

每个人工世界中G=0、1各占1/2，两群分别16个等概率人工原潜变量T和E1,E2,E3源，全部外生互相独立，因而每世界32条完整类型、每条真概率1/32，八世界共**256条**。三项实际观察数值`X_j=ν_{g,j}+λ_{g,j}(s_g T+δ_g)+σ_{g,j}E_j`。0组统一冻结相同载荷1、截距0、误差幅度1、潜在尺度s0=1及真实均值δ0=0。

观察统计仅由G、X1/X2/X3及原概率算各组均值、3×3协方差和整个`P(G,X1,X2,X3)`。独立参数化解析路径由固定系数重新计算`μ_g=ν_g+λ_g δ_g`、`Cov_g(X_i,X_j)=λ_{g,i}λ_{g,j}s_g²+1{i=j}σ_{g,i}²`，逐项精确一致。全部Fraction，无群体真实抽样误差。

项目等值层次的布尔标记需要明确区分：构型指标是三题载荷**零与非零模式**是否相同，原始metric是固定同一人工潜在单位下的载荷参数数值是否一致，原始scalar是截距相等，原始strict是特异误差方差相等。它们分别只是**事前真机制参数的oracle声明**，不能直接当成在真实群体数据中通过了逐级拟合检验；如果前级不成立，后级参数一致也不自动允许跨群潜在比较。

## 八个人工世界精确验收

| 冻结世界 | 观察组1−组0三题均值差 | 人工真实潜在均值差 | raw构型/载荷/截距/残差等值 |
|---|---|---:|---|
| FULL_STRICT_INVARIANT | (0,0,0) | 0 | 是／是／是／是 |
| TRUE_LATENT_MEAN_SHIFT | (1,1,1) | 1 | 是／是／是／是 |
| INTERCEPT_SHIFT_ALIAS | (1,1,1) | 0 | 是／是／否／是 |
| METRIC_LOADING_CHANGE | (0,0,0) | 0 | 是／否／是／是 |
| PARTIAL_SCALAR_ITEM1 | (1,0,0) | 0 | 是／是／否／是 |
| STRICT_RESIDUAL_VARIANCE_CHANGE | (0,0,0) | 0 | 是／是／是／否 |
| LATENT_SCALE_ALIAS | (0,0,0) | 0 | 是／否／是／是（原单位） |
| CONFIGURAL_ITEM3_DETACHED | (0,0,0) | 0 | 否／否／是／是 |

**最重要的全观察等价反例：** 在`TRUE_LATENT_MEAN_SHIFT`世界，0组与1组载荷、截距和残差全部相同，真实潜在构念均值δ从0变1；在`INTERCEPT_SHIFT_ALIAS`世界，真实潜在均值不变，但1组三个题目截距均增加1。这两个世界每一相同人工原来源实际X1/X2/X3值都完全一致，群体联合完整概率`P(G,X1,X2,X3)`每格**完全相同**，所观察到的三题组均值差皆为1。二者真实潜在均值变化则分别为1和0。故只有可见跨群分数差，不能无条件宣布群体潜在心理特征发生变化，必须先确立充分可辩护的截距/量尺锚定与额外设计条件。

**尺度参数别名：** `LATENT_SCALE_ALIAS`在1组改用潜变量`F=2T`、项目载荷改为1/2，对所有人工原来源产生的三题X与`FULL_STRICT_INVARIANT`**逐源一致**，完整观察概率一致，尽管同一数值坐标下两组报告的原始载荷不相等。应把它视为未锚定潜变量单位导致的重参数化等价，**不是证明这个心理量尺在真实意义上跨群载荷发生改变**。独立锚定参照指标或固定潜变量方差后才可合理比较参数。

**其他约束反例：** `METRIC_LOADING_CHANGE`对第一题真实载荷加倍，其真实观测方差增加并且与题2/3的协方差随之改变；`PARTIAL_SCALAR_ITEM1`只产生第一题的可见均值+1，若另外两题能获得独立外部测量等值锚定，才可以针对第一题单独检验偏差；`STRICT_RESIDUAL_VARIANCE_CHANGE`仅对1组第一题独立误差幅度从1升为2，使该题观察方差从2变为5，均值和非对角协方差保持原结构，不可据此认为严格误差等值成立；`CONFIGURAL_ITEM3_DETACHED`第3题在1组不再有真实共同因子载荷，原协方差结构与0组不同，违反构型的固定模式要求。

以上人工oracle的测量参数不可由实际问卷分数天然读取。真实测量等值实验必须另外解决群体样本、潜在能力尺度、形式化参数拟合、题目内容变化、偏倚风险与跨时测量设计。本R没有把人工布尔标志当作样本显著性结论。

## 真实执行、机器核验与永久原档

[原生Python代码](r233_exact_measurement_invariance.py) · [256条完整跨群原来源CSV](R233_ALL_256_ORIGINAL_TWO_GROUP_MEASUREMENT_SOURCES.csv) · [八世界完整Fraction结果JSON](R233_EXACT_RESULTS.json) · [文件SHA256验收收据](R233_FINAL_MACHINE_ACCEPTANCE.json)。

[GitHub Actions run39829540299](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39829540299)中两个独立Python作业的真实日志分别显示`Ran 60 tests`和`OK`，合计120次实际测试执行通过；完整原资料归档作业亦有成功状态，其独立核验两种全观察等价、原来源质量、人工真潜在均值、各组条件概率和SHA。机器已将完整原文件永久归档main，由机器人源提交[7bd52938](https://github.com/edwardsage419/Psychohistory-Research/commit/7bd52938699ed040b86fb46a75d271baa04aa525)。在本报告撰写时，工作流总体run元数据由in_progress逐步转为completed，确认总结果以正式验收JSON及后续再次核验快照为准；不能因原资料已提交就推定尚未返回的API字段。

原CSV SHA256 `98c5b7f73f66a9c47f0106d20e13e516499de36fe81320b0a16f5223c2019a78`；结果JSON SHA256 `9a69bf114acd403b7a4ff5e6de2b521c97bc369bffedd79d48956fc5bb928c08`。

所有科学发现仅人工E1；新真人E2=0，历史E3=0，R073与PESEN v0.1冻结。下一原239目录 `10-008 Longitudinal Measurement Invariance`，拟R234；既定顺序不变：全R完成→统一归纳分类→最终模型熔炼。
