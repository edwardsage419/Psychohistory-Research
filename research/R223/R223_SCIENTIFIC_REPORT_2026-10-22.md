# R223 未测混杂敏感性分析：七个人工世界、448原结构来源与可观察同分布异真因果反例

日期2026-10-22。原始239目录 **09-014 Sensitivity Analysis for Confounding（P0）**。有界科学状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_CONFOUNDING_SENSITIVITY**。本研究没有真人受试者或真实历史干预资料。

## 一手方法与计算前证据

Ding and VanderWeele (2016), [Sensitivity Analysis Without Assumptions](https://doi.org/10.1097/EDE.0000000000000457), *Epidemiology* 27:368–377，提供风险比尺度未测混杂敏感性参数与联合偏差界。VanderWeele and Ding (2017), [Sensitivity Analysis in Observational Research: Introducing the E-Value](https://doi.org/10.7326/M16-2607), *Annals of Internal Medicine* 167:268–274，提出E-value。此工作仅依据相同数学对象自建有限人工机制，不复现其真实经验研究或软件。

[计算前正式冻结协议](../../protocols/R223_CONFOUNDING_SENSITIVITY_7_SCM_448_ATOMS_PRESCORE_FREEZE_2026-10-22.md)在源码创建及所有实测结果之前单独提交：[commit1fec84f1](https://github.com/edwardsage419/Psychohistory-Research/commit/1fec84f11e180f4dcd409f42318d8585d2787374)。未在结果之后改变七种机制、exogenous U/V赋值方式、二元暴露风险模型、隐藏偏差界或无重叠处理。

## 完整结构原来源与资格边界

人工潜在二元U分布各1/2，处理T由U下已固定倾向分配，二元潜在结果Y(t,u,V)由固定0..15共16个等概率V阈值定义。每个世界64个完整 **U×T×V结构可能状态**，七世界448行，包含未来无法实际出现的结构性零处理源32行，正概率支持416行。各世界所有64行**概率总和严格为1**，只有正概率行可表示本人工随机化真正可能被观察的来源，故这448行不能误称448名真人或448次实际实验。

实际关联分析只用可观察(T,Y)；在声明“基线U也可观察”条件下进行分层标准化；隐藏原潜在Y(0)/Y(1)和V只用于人工结构oracle与可识别性审计。所有比率和偏差下界先用Fraction精确计算，E-value开平方部分使用Decimal50位高精度和独立代数核验，没有置信区间。

## 核心结果

| 人工世界 | 仅T/Y的观测RR | 真干预RR | 隐藏偏差因子B | 结论 |
|---|---:|---:|---:|---|
| NULL_CONFOUNDED | 11/5 | 1 | 7/3 | 无真实处理效果但观察正相关 |
| CAUSAL_ALIAS | 11/5 | 11/5 | 1 | 与前者观察完全同分布却真因果不同 |
| UNCONFOUNDED_CAUSAL | 9/5 | 9/5 | 1 | 独立随机分配时观察与真风险比相同 |
| CONFOUNDED_CAUSAL | 3 | 9/5 | 2 | 未测U夸大观测关联 |
| CONFOUNDED_REVERSED | 1 | 3/5 | 15/7 | 零观察关联掩盖真实保护效果 |
| WEAK_OVERLAP | 93/19 | 9/5 | 10/3 | 虽有重叠，处理几率极端放大观察偏差 |
| NO_POSITIVITY | 6 | 9/5 | 不定义 | U×T部分结构零支持，可测U标准化仍不能由实际资料识别 |

核心**非识别定理的一个明确有限反例**：NULL_CONFOUNDED和CAUSAL_ALIAS的完整四格观察联合P(T,Y)完全相等，观察RR均11/5；第一真RR=1，第二真RR=11/5。两世界通过同一个观察数据接口无法区分，E-value亦相同（约3.8248076809），因此单独的E-value对这两个实际不同因果机制并不给出唯一选择。

在U已测且各U×T细胞均有正概率的六世界，用U标准化的实际观察条件风险可恢复本人工oracle真干预风险；对NO_POSITIVITY则严格返回 **UNIDENTIFIED_NO_POSITIVITY**，即便模拟程序内部包含完整Y0/Y1。隐藏oracle RR_EU、RR_UD及 B=(RR_EU RR_UD)/(RR_EU+RR_UD−1) 用作数学审计，不在实际估计过程中偷用U或反事实。点E-value计算 `q+√(q(q−1))`，q=max(RR,1/RR)；实际执行中未虚构95%置信区间或“置信区间E-value”。

这些限定结论不能自动推广到现实无测U、多值干预、时间变化混杂、测量误差、选择偏倚或模型未知的真实人群。

## 复现、CI和正式归档

* [完整448结构源CSV](R223_ALL_448_ORIGINAL_CONFOUNDING_STRUCTURAL_ATOMS.csv)，[七世界精确结果](R223_EXACT_RESULTS.json)，[源SHA收据](R223_FINAL_MACHINE_ACCEPTANCE.json)。
* [原生Python程序](r223_exact_confounding_sensitivity.py)，两版本各48项单元测试，合计96次成功运行，包含正概率416、零概率32、完整四格观察别名及隐藏因果差异测试。
* GitHub Actions [run39788126049](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39788126049) 整体状态completed/conclusion success。Python3.11和3.12的真实日志分别显示Ran 48 tests与OK；第三原资料作业日志显示源数、零源数、观察同分布异真效果、SHA严格校验成功。
* 机器人真实永久原资料提交 [b2dd10d7](https://github.com/edwardsage419/Psychohistory-Research/commit/b2dd10d7c2383ad0a8490a98f4f5e9f4509add7a)。若GitHub jobs详情有运行结束后尚在刷新中的字段，必须与主run和实际job日志分开如实记载，不擅自改为success。

本研究**仅人工有限E1**，真人E2新增0、历史E3新增0；R073与PESEN v0.1继续冻结。原239目录每研究一项才另行结题；之后统一分类，最后模型熔炼。
