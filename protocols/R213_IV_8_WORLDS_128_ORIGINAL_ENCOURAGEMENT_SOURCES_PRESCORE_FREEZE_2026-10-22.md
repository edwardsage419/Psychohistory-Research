# R213 工具变量估计（09-004）：八个人工机制世界、128条原始二元鼓励来源、Wald-LATE与识别假设失效，评分前冻结

日期2026-10-22（Asia/Taipei）。真实原239候选目录 **09-004 Instrumental Variables（P1）**。状态 **PRESCORE_FROZEN_E1_ARTIFICIAL_BINARY_IV**。

## 原始学术依据及边界

Imbens & Angrist (1994), *Identification and Estimation of Local Average Treatment Effects*, *Econometrica* 62(2):467–475, DOI https://doi.org/10.2307/2951620；Angrist, Imbens & Rubin (1996), *Identification of Causal Effects Using Instrumental Variables*, *JASA* 91(434):444–455, DOI https://doi.org/10.1080/01621459.1996.10476902 。原始文献区分鼓励Z、实际处理D、单调顺从者与可识别局部平均效应。本研究限定八个四值/线性人工潜在结果分配案例，不执行现实工具变量应用或原作者实证复现；第一手英文文献信息在冻结前核对。

## 全部完整人工来源
每个模型条件含**8个等权有序潜在个体类型i=0..7**，每人主阶层类型s_i∈{COMPLIER,ALWAYS,NEVER,DEFIER}决定D_i(0)、D_i(1)，其潜在处理结果Y_i(d)=base_i+tau_i*d。COMPLIER对应D(0)=0,D(1)=1；ALWAYS=(1,1)，NEVER=(0,0)，DEFIER=(1,0)。部分世界另有直接工具效应δZ，使完整结构结果Y_i(d,z)=base_i+tau_i*d+δz，**明确违反排除限制**。Z是人工二元“鼓励工具”，实际处理D(Z)，不是把Z误叫做观察处理D。

七个有效随机鼓励或违反其他假设的世界，另加一项弱工具与排除冲突的组合，共**8世界**：
1. FULL_COMPLY：全部8为COMPLIER，base_i=i mod3，tau_i=1+(i mod4)。独立Z∼Bern(1/2)，δ=0。
2. MONOTONE_MIX：i0..3为COMPLIER，tau=(2,2,4,4)，i4..5 ALWAYS，i6..7 NEVER，全部非complier tau=0、base_i=i mod2；Z独立、δ=0。真实COMPLIER LATE=3、总体ATE=3/2。
3. WEAK_COMPLIERS：仅i0为COMPLIER，tau0=4，i1..4 ALWAYS、i5..7 NEVER，所有人base_i=i mod2、其他τ=0，Z独立、δ=0；first stage=1/8。
4. NO_COMPLIERS：i0..3 ALWAYS、i4..7 NEVER，全部tau_i=2、base_i=i mod2，Z独立δ0。first stage=0；**任何Wald比率必须设为UNDEFINED_ZERO_FIRST_STAGE**而不是0、NaN或无穷，虽然总体ATE=2。
5. WITH_DEFIERS：i0..3 COMPLIER τ=2，i4..5 DEFIER τ=4，i6..7 NEVER τ=0，全部base_i=i mod2；Z独立δ0。net first stage=(4−2)/8=1/4；Wald因COMPLIER与DEFIER相反的权重变为0，而COMPLIER真实平均效应=2。
6. EXCLUSION_VIOLATION：和MONOTONE_MIX完全相同的潜在顺从者和基础Y，Z独立，但δ=1直接影响Y。first stage=1/2，Wald=5，真实COMPLIER效应3。数字增加部分1/(1/2)=2来自直接影响。
7. WEAK_EXCLUSION：和WEAK_COMPLIERS潜在类型相同，Z独立但δ=1。first stage=1/8，Wald=12，COMPLIER真实效应4，人工排除误差被1/(1/8)=8放大；这一**人口量级的工具弱相关放大机制**不等同有限样本弱工具分布推断。
8. Z_CONFOUNDING：MONOTONE_MIX同样的顺从类型及τ，但base_i=10对COMPLIER i0..3、否则0，工具分配**不独立**：COMPLIER的q_i=P(Z=1|i)=3/4，其他4人的q_i=1/4，满足P(Z=1)=1/2但给定Z的潜在类型分布不同；δ=0。分析必须明确工具与潜在结构相关，不允许套用有效随机Z的LATE等式。

每世界固定8个不同潜在个体的所有二元鼓励值z∈{0,1}共**16条真原来源**，真实联合概率 `P(i,z)=1/8×q_i^z (1−q_i)^(1−z)`，每世界原16条求和1。8世界共**128条完整原始人工联合来源CSV**，保存世界、个体序号、主阶层、两个潜在D、两个Y(d)与各直接δ项、鼓励值及真实联合概率、已观察D(z)与Y(D(z),z)、潜在均衡真个体处理效应。两个z值可能对应同一个潜在个人，**不是128名独立真人**；全部来源只是有限原概率空间。

## 固定评价
对每世界完整独立数学原来源按其真实权重，算P(Z)、E[D|Z=1]、E[D|Z=0]及first stage FS；E[Y|Z]及ITT_Y，Wald比率 ITT_Y/FS 若FS≠0。与人工潜在先知oracle目标总体ATE=Στ_i/8、COMPLIER LATE=Σ_{i:C}τ_i/#C（若#C=0则NOT_DEFINED_NO_COMPLIERS）、单调与工具独立/排除假设逐项比较，不可将LATE无条件当全部人的ATE。

**两条独立准确路线**：对所有Z独立、排除成立的来源用潜在主阶层恒等式
FS=(#C−#DEFIER)/8，ITT_Y=(Σ_i[D_i(1)−D_i(0)]τ_i)/8。
在直接δ≠0但Z独立的世界有ITT_Y=结构表达式+δ。与16条原实际联合概率按条件均值计算的FS、ITT_Y逐Fraction严格一致。对于Z_CONF参与者真实条件先验不同，**此结构等式禁止作为观察独立识别式断言**，须定量报告人口来源选择造成的偏差。

限制：二元鼓励、八个潜在个体、无真实人类/历史数据；没有随机抽样带来的渐近误差、现实非服从、测量误差、社会溢出干扰或工具有效性的实证论证。“工具有效”是人工来源定义的假设，不是只通过观察工具与结果相关就可以证明。真实社会的工具排除和独立往往不可直接验证，必须依赖设计/外部事实。输出所有阴性和违反假设场景，不对样本上有利结果重选世界。

## 正式验收
纯Python标准库、Fraction、≥30单测，GitHub Actions Python3.11及3.12两组测试，第三完整生成8世界、128原联合来源、三个输出文件SHA并永久提交main。所有三job success及实际文件入库后标记**CLOSED_BOUNDED_E1_ARTIFICIAL_BINARY_IV**，新增真人E2=0、历史E3=0，R073/PESEN v0.1冻结。原目录下一**09-005 Regression Discontinuity Design**，拟R214。继续先完成所有原239目录研究，再统一分类，最后熔炼。
