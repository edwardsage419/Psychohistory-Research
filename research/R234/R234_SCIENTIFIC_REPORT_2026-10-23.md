# R234 纵向测量等值：九个双波人工机制、2304原来源与完整配对联合观察等价

日期：2026-10-23（Asia/Taipei）。原始239研究目录 **10-008 Longitudinal Measurement Invariance（P1）**。科学结论限定 `CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_LONGITUDINAL_MEASUREMENT_INVARIANCE`。数据全部为九个有限人工结构世界的完整枚举，没有真实受试者或历史跨期数据。

## 文献范围及研究预冻结

Widaman, Ferrer & Conger (2010), [*Factorial Invariance Within Longitudinal Structural Equation Models: Measuring the Same Construct Across Time*](https://doi.org/10.1111/j.1750-8606.2009.00110.x), *Child Development Perspectives* 4:10–18 (PMID 20369028) 讨论纵向同一构念是否在不同测量时点保持可比。Putnick & Bornstein (2016), [*Measurement Invariance Conventions and Reporting*](https://doi.org/10.1016/j.dr.2016.06.004), *Developmental Review* 41:71–90 (PMID 27942093) 回顾跨时与跨组的构型、载荷、截距和误差等值步骤。本文没有复算这些研究的真实人类调查样本、实际CFA估计、样本拟合优度及其经验效应。

在任何源码与结果产生前提交[独立完整来源、结构与评估协议](../../protocols/R234_LONGITUDINAL_INVARIANCE_9_WORLDS_2304_PAIRED_SOURCES_PRESCORE_FREEZE_2026-10-23.md)，冻结提交[90f38f8a](https://github.com/edwardsage419/Psychohistory-Research/commit/90f38f8a922650e2084d5ba64ce938aaf7754afa)。随后生成源码、CI及全部机器来源。算法、模型世界和目标没有根据观察结果重新调整。

## 八源256完整配对概率空间与两套验证

匿名同一单位两次施测三项测验。人工外生 `T,H,E01,E02,E03,E11,E12,E13` 互相独立、均匀±1；单世界2⁸=256条**完整双时间点原来源**，每行权重1/256，九世界**2304条**。T为稳定基因式符号特征，H为仅在time1可能起作用的独立特征创新，E0/E1分别代表两次项目噪声；某一世界复用第一次首题噪声以形成跨次相关测量误差。固定真实人工 `F0=T`、`F1=sT+hH+δ`，观察 `X0_j=T+E0j`、`X1_j=ν_j+λ_jF1+σ_j noise_j`。

完整来源逐行保存八独立源、两个人工真潜变量、真实人工变化值、六个可见项目及三项可见项目变化。第一统计路线仅从**六个实际可见项目**及原概率计算六维人口均值、全部36项人口协方差、整套`P(X01,X02,X03,X11,X12,X13)`和同一单位跨时三题平均分数变更的均值及方差；第二条独立路径不读取全原CSV，以冻结8维系数向量内积重构同一六维均值及36协方差，完全相符。真实F的平均改变量、改变量方差、跨时因子Cov及第二次方差从完整人工oracle独立计算，并与系数公式`(δ,(s−1)^2+h^2,s,s^2+h^2)`严格相符。观察差均值/方差另由六维Cov解析线性组合独立复核。

以上所有概率均为Fraction精确有限分布，绝无真实受试者独立随机抽样或测量效度保证。

## 九世界有限精确结果

| 世界 | 观察三题time1−time0均值 | 真潜在均值变化 | 真个体变化方差 | 观察三题平均变化方差 |
|---|---|---:|---:|---:|
| STABLE_BASE | (0,0,0) | 0 | 0 | 2/3 |
| TRUE_LATENT_SHIFT | (1,1,1) | 1 | 0 | 2/3 |
| UNIFORM_INTERCEPT_DRIFT_ALIAS | (1,1,1) | 0 | 0 | 2/3 |
| LATENT_INNOVATION | (0,0,0) | 0 | 1 | 5/3 |
| SINGLE_ITEM_INTERCEPT_DRIFT | (1,0,0) | 0 | 0 | 2/3 |
| METRIC_ITEM1_DRIFT | (0,0,0) | 0 | 0 | 7/9 |
| ERROR_VARIANCE_DRIFT | (0,0,0) | 0 | 0 | 1 |
| PERSISTENT_FIRST_ITEM_ERROR | (0,0,0) | 0 | 0 | 4/9 |
| LATENT_SCALE_REANCHOR_ALIAS | (0,0,0) | 0 | 1（原坐标，不可直接解释为改变） | 2/3 |

**最强反例一：相同六维纵向观察的真实潜在改变/截距漂移等价。** `TRUE_LATENT_SHIFT`的真潜在F1=T+1，三题time1相应增加1，模型的截距和载荷均不变；`UNIFORM_INTERCEPT_DRIFT_ALIAS`的真潜在F1=T始终未改变，但三题time1截距均上移1。对**全部256个对应八源同一个体的配对状态**，time0及time1六个可见分数逐项完全一致，完整六维联合概率亦逐格完全一致；观察三题均值变化均(1,1,1)，但真潜在构念均值改变分别1与0。这直接给出在缺乏独立项目截距稳定性锚定条件时，纵向观察变化不能单独确定真心理变化的人工数学反例。

**最强反例二：潜在量尺单位重标定。** `LATENT_SCALE_REANCHOR_ALIAS`把time1潜在定义为F1=2T、time1三个项目载荷同步设为1/2，故每个原来源的time1实际项目值还是T+E1j。它与STABLE_BASE拥有完全相同的六项配对来源与联合观察概率。但若**不统一单位**直接计算F1−F0=T，oracle“潜在改变量方差”是1，而同一共通尺度下STABLE_BASE的变化方差是0。这属于参数坐标重新标定引起的**假性变化表征**，并不能当成实际能力波动或无可辩护的跨时潜在变异检验。必要时应优先提供跨时共同锚题与固定因子单位。

**均值以外的独立风险：** `LATENT_INNOVATION`中真个体变化均值0但方差1，time1三题之间非对角Cov从1增至2，观察平均分变化方差增至5/3。 `ERROR_VARIANCE_DRIFT`中time1第一项目独立误差方差由1增至4，第一题观察总方差从2增至5，其他非对角项仍1，观察平均变化方差增至1。 `PERSISTENT_FIRST_ITEM_ERROR`中time1第一题重复使用其time0误差，跨时同题Cov从1增至2，其他跨时不同项目Cov仍1，观察均分变化方差降至4/9；因此跨时稳定性中可以存在持续测量误差贡献而非稳定心理特质。单一项目截距漂移只改变第一题可见均值，三项目联合结构有检测非统一漂移的人工机会，**但在真实量表中需验证剩余两题确实可锚定**。

原生raw参数布尔标签为已知生成式的oracle属性，不是现实拟合的多组CFA显著性测试；观察完整联合对证明的是限定人工概率机制的有限不识别，未证明跨文化/时代所有测验都不能比较。

## 代码、CI、永久原始科研证据

[原生标准库Fraction源码](r234_exact_longitudinal_invariance.py) · [2304条完整双波外生源CSV](R234_ALL_2304_ORIGINAL_TWO_WAVE_SOURCES.csv) · [全九世界六维观察联合、36格Cov及真值JSON](R234_EXACT_RESULTS.json) · [来源SHA256及验收机读收据](R234_FINAL_MACHINE_ACCEPTANCE.json)。

[GitHub Actions run39881566150](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39881566150)完整运行总体completed/success，三个job分别completed/success。Python3.11与3.12真实日志各`Ran 66 tests`与`OK`，双版本总**132次实际测试执行通过**。第三作业真实日志显示`R234_ALL_2304_PAIRED_LONGITUDINAL_ORIGINAL_ATOMS_AND_TWO_FULL_OBSERVATIONAL_ALIASES_VERIFIED`，对全2304来源每行1/256、各世界全部唯一八源、完整六维观察等价、真实变化反例、跨时Cov、观察平均变化方差、原来源和结果SHA进行独立复核并将原始CSV/结果/凭证通过机器人永久提交main：[689c8d47](https://github.com/edwardsage419/Psychohistory-Research/commit/689c8d47e9aab742bdd41e623c0578d6ee7a3f41)。

全原CSV SHA256 `9aff778b6a25562b1c53af0de818c4f317efc28b1169c41834b879a067fb9ae7`；结果JSON SHA256 `2d1f78b53af3b7e075e5d26259099cf102188a5da5512c81cd027927e6b6a1e8`。

新增真人E2=0，历史E3=0；R073/PESEN v0.1均冻结。后续为原239目录 `10-009 Differential Item Functioning`（R235）。全部原R研究完成后才统一归纳分类、最后熔炼，不提前更改R073模型与评分。
