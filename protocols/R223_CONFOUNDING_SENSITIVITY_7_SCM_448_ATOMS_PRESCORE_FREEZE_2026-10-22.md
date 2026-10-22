# R223 原239目录09-014：未测混杂敏感性分析，有限七SCM完整来源与风险比边界，评分前冻结

日期2026-10-22。对象为原始239候选项目录 `09-014 Sensitivity Analysis for Confounding`（P0），研究编号R223。科学目标是**有限人工机制 E1 与敏感性界限方法审计**。不对真人处理政策、药物、社会制度作识别声明，不视为原作者真实实证复算。

## 可核实的一手方法背景

Ding and VanderWeele (2016), *Sensitivity Analysis Without Assumptions*, Epidemiology 27:368–377, DOI https://doi.org/10.1097/EDE.0000000000000457，建立未测混杂风险比敏感性界。VanderWeele and Ding (2017), *Sensitivity Analysis in Observational Research: Introducing the E-Value*, Annals of Internal Medicine 167:268–274, DOI https://doi.org/10.7326/M16-2607，介绍E-value、观测风险比所需关联强度及解释范围。

本实验只验算有限二元U/T/Y数学生成机制，不复现论文原观察研究，也不生成真实置信区间。

## 完整有限原来源及冻结的七个世界

七个人工机制，隐蔽二元基线U∈{0,1}各概率1/2。每人处理T在U下按给定Bernoulli概率分配；独立均匀V∈{0,…,15}，二元真潜在结果Y(t,u,v)=1{v < c[t,u]}，c为下表对应成功数/16。实际观测仅(T,Y)，部分附加诊断允许看到U来计算**可测U标准化**；真Y0/Y1和V仅人工oracle。每世界2U×2T×16V=64行完整**结构性来源状态**，七世界共448行。NO_POSITIVITY世界有32行处理分配概率严格为0，这些仅表示不可观察的完整潜在结构，不得记作有观察支持的来源。总正概率行数416；每世界全部行概率总和为1。

| 世界 | P(T=1|U=0), P(T=1|U=1) | c[Y0|U0], c[Y0|U1] | c[Y1|U0], c[Y1|U1] |
|---|---|---|---|
| NULL_CONFOUNDED | 1/4,3/4 | 2,14 | 2,14 |
| CAUSAL_ALIAS | 1/2,1/2 | 5,5 | 11,11 |
| UNCONFOUNDED_CAUSAL | 1/2,1/2 | 2,8 | 6,12 |
| CONFOUNDED_CAUSAL | 1/4,3/4 | 2,8 | 6,12 |
| CONFOUNDED_REVERSED | 1/4,3/4 | 6,14 | 2,10 |
| WEAK_OVERLAP | 1/16,15/16 | 2,8 | 6,12 |
| NO_POSITIVITY | 0,1 | 2,8 | 6,12 |

重点反例：NULL_CONFOUNDED与CAUSAL_ALIAS实际可见联合P(T,Y)必须逐格严格相等，但前者真实风险比=1，后者真实风险比=11/5；两者观察风险比都为11/5。故从无U的实际观测分布不能唯一判断因果关系。

## 事前固定计算目标与假设门槛

1. 仅观察T/Y的风险：r1=E[Y|T=1]，r0=E[Y|T=0]，观测关联RR_obs=r1/r0。真反事实干预风险：R_t=1/2 Σ_u E[Y(t,u,V)]，RR_true=R1/R0。都用精确Fraction来源枚举，两种数学程序路径核对。
2. 当所有四个(U,T)条件事件都有正支持时，计算真实可测U标准化r_t^std=1/2Σ_u E[Y|T=t,U=u]，并验证等于人工oracle R_t；当存在结构性零支持时，标准化返回明确 `UNIDENTIFIED_NO_POSITIVITY`，不能从人工真潜在值填充一个伪观察估计。
3. 定义真实但通常不可见的混杂强度 RR_EU=max_u P(U=u|T=1)/P(U=u|T=0)，RR_UD=max_t max_u P(Y=1|T=t,U=u)/min_u P(Y=1|T=t,U=u)。在本冻结的全部条件风险均正时，计算B=(RR_EU×RR_UD)/(RR_EU+RR_UD−1)，核验下界 RR_true ≥ RR_obs/B 的方向性条件；若U/T无正重叠则B和调整标记无效/未识别。
4. 对正观测RR计算E-value：q=max(RR_obs, 1/RR_obs)，E=q+sqrt(q(q−1))；输出50位Decimal的数值（非有理数时并非精确Fraction）。检验 `E²/(2E−1)≈q` 的代数数值恒等式，单一E-value作为**观察关联的敏感性诊断**，并非自动证明任何真实因果效应。没有真实CI，不填入虚构“CI E-value”。
5. 计算观测混杂差异与真实效果差异、观察同分布异真效果、弱重叠与完全零支持区别。禁止在看到结果后更改上述世界、风险界或阈值。

## 执行与验收

创建原生标准库Python程序，至少35项不依赖额外软件包的真正单元测试，CI分别用Python3.11/3.12各跑一遍。第三GitHub Actions job完整产生448行全部原结构源与其零概率标签、各世界Fraction结果JSON、相应SHA256机读收据，永久入main。正式后续科学报告和独立结题JSON必须绑定真实commit、完整原来源SHA及实际CI job结果，未完成前只能标记 `PRESCORE_FROZEN_E1_PENDING_EXECUTION`。

证据等级最多人工数学E1。新增真人E2=0，真实历史E3=0。R073和PESEN v0.1保持冻结。下一个R序号及实际239目录须另行核验，不得从本研究标签推断整个目录全部完成；按原安排先完成全部R学研，再统一分类，最后熔炼。
