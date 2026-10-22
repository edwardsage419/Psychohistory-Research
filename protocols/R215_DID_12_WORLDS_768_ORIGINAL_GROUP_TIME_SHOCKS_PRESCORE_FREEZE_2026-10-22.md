# R215 Difference in Differences（09-006）：12人工三期双组面板×64完整独立冲击来源、趋势与可识别性，计算前冻结

日期2026-10-22（Asia/Taipei）。真实原239项候选目录**09-006 Difference in Differences（P1）**。科研状态PRESCORE_FROZEN_E1_ARTIFICIAL_THREE_PERIOD_DID。

## 原方法与限定边界
Abadie (2005), *Semiparametric Difference-in-Differences Estimators*, Review of Economic Studies 72:1–19, DOI https://doi.org/10.1111/0034-6527.00321，强调常规DID识别需要处理组和对照组**未接受处理时的平行反事实趋势**。Bertrand, Duflo & Mullainathan (2004), *How Much Should We Trust Differences-In-Differences Estimates?*, Quarterly Journal of Economics 119:249–275, DOI https://doi.org/10.1162/003355304772839588，特别提示时间序列相关性使标准误错误。Roth (2022), *Pretest with Caution: Event-Study Estimates after Testing for Parallel Trends*, American Economic Review: Insights 4:305–322, DOI https://doi.org/10.1257/aeri.20210236，提醒pre-trend检验不一定足以保障结果。本研究是完全人工三期、两组**单个合成组平均值**的数学DID结构审计，不复现这些论文的真实样本、估计器或聚类稳健推断。

## 人工双组×三期真结构与完整原来源

两个带编号的组C（对照）与T（受处理），同样于三个固定时间t∈{−1,0,1}各提供一个**合成组平均值**。D组的严格处理时点在t=1：Z_T(1)=1，其他所有group-time无处理。每个组在未处理下的潜在组均值Y_g^0(t)=b_g+s_g t+q_g·1{t=1}。所有系数均事前人为固定，为整数。处理组T在t=1的真正因果ATT定义为tau，即Y_T^1(1)−Y_T^0(1)=tau，而对照组从未处理。额外变量anticip可在t=0把T组可见结果从Y_T^0(0)提高anticip，尽管t=0实际尚未接受处理；**这是刻意违反无提前反应的观察机制**，不能硬解释成t=0“正在处理”。所有来源真潜在组均值、观察额外anticip、真实tau分别存证。

每一组×时点有独立等概率Rademacher外生组-时期冲击ε_{g,t}∈{−1,+1}，真实可见六个结果为Y_g^0(t)+ε加相应post tau或pre anticip。六个ε各自独立、方差1。全部2^6=**64条完整外生冲击向量**，每世界每条原来源概率1/64，全部真实组时段来源概率严格和为1。**这六个噪声是独立的组-时期层冲击，不是把组内多位独立个体当作样本；并未提供多组的聚类稳健标准误、时间自相关或实证抽样。**

固定12个人工结构世界，字段依次为(bT,bC,sT,sC,qT,qC,anticip,tau)：
1 PARALLEL_NULL (3,0,1,1,0,0,0,0)
2 PARALLEL_TAU_TWO (3,0,1,1,0,0,0,2)
3 PARALLEL_NEGATIVE (3,0,1,1,0,0,0,-2)
4 LEVEL_GAP_ONLY (10,0,1,1,0,0,0,0)
5 DIFFERENTIAL_SLOPE_FALSE (3,0,2,1,0,0,0,0)
6 DIFFERENTIAL_SLOPE_TAU_TWO (3,0,2,1,0,0,0,2)
7 POST_SHOCK_FALSE (3,0,1,1,2,0,0,0)
8 POST_SHOCK_WITH_TAU_MINUS_ONE (3,0,1,1,3,0,0,-1)
9 ANTICIPATION_TAU_TWO (3,0,1,1,0,0,1,2)
10 ANTICIPATION_NULL (3,0,1,1,0,0,1,0)
11 CONTROL_POST_SHOCK (3,0,1,1,0,2,0,0)
12 LARGE_DIFF_SLOPE (3,0,3,0,0,0,0,0)。

在三世界PARALLEL_TAU_TWO、POST_SHOCK_FALSE和POST_SHOCK_WITH_TAU_MINUS_ONE中，完整六组-时点可见**期望值及64原独立噪声联合分布完全相同**，但真ATT分别为2、0、−1（post仅T组的未处理潜在结果冲击互换真因果效果）。这些案例用于审计**仅凭三期实际观测及任何处理前趋势检验，无法区分post才发生的未处理反事实冲击与真实处理效应**。在PARALLEL_TAU_TWO的真世界满足平行趋势且没有anticip；POST_SHOCK两个违规世界潜在未处理反事实趋势在post改变，不满足post平行趋势。不得误称两者反事实模型相同。

**完整来源规模**：12世界×64个六组-时期冲击向量=**768条人工原可观测三期面板来源**。每一行保留世界、所有六个未处理潜在值、真post处理潜在值、anticip、真实ATT、实际六个观测、原独立ε、三个观测估计器的具体估计及真误差；联合来源条件权重1/64。12个设计世界各自独立作为数学场景，不能称768次真实独立社会干预试验或768名真人。

## 预先冻结三项统计量、反事实与评分

令G_t=Yobs_T,t−Yobs_C,t为当期实际观测组均值差。
1 STANDARD_DID=G_1−G_0，常规双重差分估计，利用t0作为处理前基线。
2 PRE_TREND_PLACEBO=G_0−G_{−1}，只读取实际处理前t−1和t0的组间差异变化。不是因果效应估计量；衡量能否发现已存在的斜率趋势/提前反应。不能由其值在某次观测恰为0推断下一期未处理反事实平行趋势。
3 LINEAR_PRETREND_CORRECTED=G_1−2G_0+G_{−1}=STANDARD_DID−PRE_TREND_PLACEBO，事前追加一种固定“把前一期组间差变化向post外推”的假设模型，仅当处理/对照未处理差异按时间线性持续且无post组特有冲击或anticip时才是正确校正。不能凭该方法的低训练误差主张它普遍优于常规DID。

预冻方法权限：三统计量只读实际六个观测及固定处理时点，不准读取人工tau、q或提前反应潜在结构。对STANDARD_DID与LINEAR_PRETREND_CORRECTED，在每原噪声来源上计算`(estimate−true ATT tau)²`；对PRE_TREND_PLACEBO报告真无处理前趋势/提前反应条件下的期望、分布和噪声方差，明确**不给pretrend placebo当真ATT的估计MSE**。完整64原来源按Fraction真概率平均，验证`expected_MSE=bias²+actual_noise_variance`。由于每个group×time原噪声互相独立且方差1，G_t的噪声方差2，STANDARD_DID和PRE_TREND_PLACEBO方差各4，LINEAR_PRETREND_CORRECTED方差12。另按独立组六个ε系数平方和核验三方差。
对每世界真三种**无噪声观察期望**分别计算理论：
    E[STANDARD_DID]=tau+(sT−sC)+(qT−qC)−anticip
    E[PRE_TREND_PLACEBO]=(sT−sC)+anticip
    E[LINEAR_PRETREND_CORRECTED]=tau+(qT−qC)−2anticip
用与逐64原扰动直接求和独立的**固定结构参数公式Fraction**验证，不偷用实际噪声源来选择机制。
记录真实“平行反事实趋势是否在处理前/后均成立”，定义为sT=sC且qT=qC（在离散三期的未处理结果下），并且anticip=0作为DID另外的无提前反应条件。某世界pre placebo期望0可能只是前趋势无差，也可能因为前斜率与anticip抵消；它不证明post没有仅一组受到的新冲击。

## 阴性对照与科研边界
- PARALLEL_TAU_TWO真ATT2与POST_SHOCK_FALSE真ATT0、POST_SHOCK_WITH_TAU_MINUS_ONE真ATT−1在**整个实际六变量联合分布**精确相同。三种观测统计量的整个来源分布也必须相同，但真实ATT完全不同。此为**如果没有反事实平行趋势/无遗漏post冲击假设时的因果不可辨识**，不等于随机噪声引起的有限样本不精确。
- DIFFERENTIAL_SLOPE_FALSE真ATT0、标准DID期望1，pre placebo期望1，趋势校正预期0；这项**仅证明固定稳定线性趋势假设下**增加一段完整pre期能做出正确校正，噪声方差则由4变12。
- POST_SHOCK_FALSE真正post违反平行趋势，但pre placebo**源期望严格0**，所以pre趋势阴性不能保证未来反事实有效；有噪声时更不能把单条placebo=0作真无违规保证。这个发现呼应Roth 2022 pretest谨慎性，但本实验不实施其真实前趋势统计检验。
- ANTICIPATION_TAU_TWO真实tau2，但t0被+1预期反应污染，STANDARD_DID期望1、PRE_TREND_PLACEBO期望1、校正预期0；校正错误地把提前反应双重扣除。无法靠t−1至0仅一个pre趋势统计量同时辨识anticip与未处理趋势。
- 本研究只有两个合成组均值、三期、没有组内单位或真实政策采纳，**不提供标准误估计的抽样一致性检验**，不实施Bertrand等原文的串行相关修正或许多组聚类推断，不支持现实政策效果预测。

## 验收和下一步
纯标准库Fraction，≥30单测，GitHub Actions Python3.11和3.12双版本测试各success；第三确实生成12世界完整JSON、768真原组六噪声来源CSV、两组数学方差与来源SHA收据，真正永久提交main。只有全部结果存在且三CI jobs success、科学报告和README更新后正式结题 **CLOSED_BOUNDED_E1_ARTIFICIAL_THREE_PERIOD_DID**。新增真人E2=0、历史E3=0；R073/PESEN v0.1冻结。下一真实原目录**09-007 Event Study Design（P1）**，拟R216。继续原239项全部R先完成再统一归纳分类，最后进行熔炼。
