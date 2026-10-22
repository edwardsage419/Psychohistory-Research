# R219 逆概率加权（09-010）：完整1281真赋值来源、隐藏混杂、极端权重与不可识别

日期2026-10-22（Asia/Taipei）。实际原239目录 **09-010 Inverse Probability Weighting（P1）**。正式科研状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_IPW**。本项只为六个完整固定人工总体中的赋值机制检验，真人E2=0、真实历史E3=0。

## 第一手研究与固定原理

Horvitz and Thompson (1952), *A Generalization of Sampling Without Replacement from a Finite Universe*, [原论文可获取版本](https://www.stat.cmu.edu/~brian/905-2008/papers/Horvitz-Thompson-1952-jasa.pdf)，阐明按已知不等概率加权估计有限总体。Cole and Hernán (2008), *Constructing Inverse Probability Weights for Marginal Structural Models*, *American Journal of Epidemiology* 168:656–664, [DOI 10.1093/aje/kwn164](https://doi.org/10.1093/aje/kwn164)，强调一致性、交换性、正值性、模型正确性及极端权重诊断。本研究没有使用作者的真实原样本，没有时间变化暴露或动态边际结构模型，也没有真实 propensity 估计、误差标准推断、连续暴露、机器学习或实际观察群体因果识别。**公式和有限来源是我们明确自造的数学E1**。

计算前冻结[完整六来源世界、1281真赋值来源与方差两路检验协议](../../protocols/R219_IPW_6_WORLDS_1281_EXACT_ASSIGNMENTS_PRESCORE_FREEZE_2026-10-22.md)，提交[43ccc72b](https://github.com/edwardsage419/Psychohistory-Research/commit/43ccc72b13ea17d81f5401a1771faa13f1240fba)，早于执行程序、CI和完整源结果。没有在取得结果后改真倾向来源、目标或估计器；正式随机化结果仍保留最差情形和失效来源。

## 原世界、因果目标、信息权限

八个带编号人工单位i=0..7，已观察的二元协变量X=00001111，隐藏基线U=00110011；无干扰，固定每人两种潜在结果Y_i(0)、Y_i(1)，真实每个世界有限总体ATE恒为**2**。处理Z_i条件于已冻结真概率p_i独立Bernoulli(p_i)。六世界中五个满足0<p_i<1，各完整2^8=256种互斥处理分配来源，另一个零一概率世界仅有一种真分配，全部**5×256+1=1281条原人工处理分配历史**。每世界原条件概率精确和为1；不能把1281条互斥数学可能来源当1281次真实研究、1281名人或跨环境独立预测。

所有公共估计器只能看到实际Z、对应一人的实际Yobs以及预先已知的**公共X层真倾向e(X)**；研究明确没有“从一次Z向量拟合倾向评分”的统计任务。隐藏U、每人真个体概率p_i及未观测潜在结果只供**机器审计oracle**；不得偷输入公共估计量。因此公共e(X)即使确实等于同X层真p的均值，也不代表给定X的潜在结果与治疗选择可交换。

六个固定世界：
1. CORRECT_X：e(X=0)=1/4，e(X=1)=3/4；Y0=2X、Y1=Y0+2，公开e(X)与每人真正p一致。
2. HIDDEN_U_BOTH：真正p在X、U四种组合依次1/8、3/8、5/8、7/8；公共e(X)=1/4或3/4，仅给公共估计器使用X；Y0=2X+2U、Y1=Y0+2。隐藏U同时影响分配和潜在结果。
3. HIDDEN_U_ASSIGNMENT_ONLY：真正p与第2世界完全相同，但Y0=2X、Y1=Y0+2，U仅影响选择、不影响潜在结果，形成检验“隐藏选择机制是否必然造成偏差”的负面对照。
4. WEAK_OVERLAP：公共与真实p在X两层分别1/16、15/16；Y0=2X，Y1=Y0+2；两臂都有非零数学概率，但极端倒数权重最大16。
5. HETEROGENEOUS_TAU_X：p公共与真取1/4、3/4，Y0=2X、Y1=Y0+4X，X0组效果0、X1组4、总体仍ATE=2。
6. POSITIVITY_FAILURE：p(X0)=0、p(X1)=1，Y0=2X、Y1=Y0+2。真ATE=2仅人工oracle知道，对观测处理政策而言两个层次从无另一处理可能，不能从相同X层的观察数据识别ATE；因果HT、Hájek、clip均必须发布`null`并明确不可识别，不得从虚构的正概率求值。

## 所有方法事前锁定与估计目标区别

**PUBLIC_HT_X**：按公共e(X)对实际治疗Y除以e(X)，对实际对照Y除以1−e(X)并取差，再对八人取平均。若权重正确且真潜在结果给定X与Z可交换、正值性成立，才期望无偏。**PRIVILEGED_TRUE_HT**：同公式但使用真实每个人p_i，由于p_i在隐藏U世界不可观察，它只是知道人工真赋值机制的oracle检验，不是一个现实可实施的已识别估计器。**WRONG_CONSTANT_HT**：所有单位强行假设p=1/2，故意错误。**CLIPPED_PUBLIC_HT**：把公共e(X)裁到[1/4,3/4]，在弱重叠世界使最大倒数权重降至4，可能引入额外偏差。

**PUBLIC_HAJEK_X**与**PRIVILEGED_HAJEK_TRUE**：各对处理和对照分别把加权结果之和除以本臂权重之和，再相减。它们是分母随机的**自归一化比率估计器**，不是同一条无条件有限HT公式，也不等同所有MSM稳定权重。若某赋值全部治疗或全部对照，则这两个比率、普通样本均值差均**undefined**；项目完整记录此种来源的真实概率和`null`，只在有两臂的条件来源上计算Hájek与朴素差的**条件均值、条件方差**，不会以其条件期望冒充无条件HT无偏性。逐来源记录处理/对照有效样本量ESS、实际最大倒数权重及两臂分母。

## 完整有限来源结果

每世界均为真ATE=2，表中HT的值为对该世界全部256真分配事件**按真正不均等概率加权**所得期望；方差也是包括极端罕见赋值在内的完整设计随机化方差。表中“不适用”是没有真正的观测正值性，不是数值0。

|人工世界|公开X-HT期望|公开HT方差|知道每人真p的理论HT期望|错误常量p=1/2的HT期望|裁剪公开HT期望|
|---|---:|---:|---:|---:|---:|
|CORRECT_X|2|17/6≈2.8333|2|3|2|
|HIDDEN_U_BOTH|8/3≈2.6667|145/24≈6.0417|2|7/2=3.5|8/3|
|HIDDEN_U_ASSIGNMENT_ONLY|2|187/72≈2.5972|2|3|2|
|WEAK_OVERLAP|2|257/30≈8.5667|2|15/4=3.75|5/2=2.5|
|HETEROGENEOUS_TAU_X|2|3|2|4|2|
|POSITIVITY_FAILURE|**不可识别**|**不可识别**|**不可识别**|仅错误模型值，不报告|**不可识别**|

对全部正值性完整世界，数值HT期望和方差都有两套独立精确Fraction复验：
* 路径A：按256个真实Bernoulli人工联合赋值`P(Z)=∏p_i^{Z_i}(1−p_i)^{1−Z_i}`逐个计算并加权。
* 路径B：不再枚举Z，仅按每个人独立Bernoulli方差恒等式直接计算
`E(HT_q)=(1/8)Σ_i[p_iY1_i/q_i−(1−p_i)Y0_i/(1−q_i)]`
和
`Var(HT_q)=(1/64)Σ_i p_i(1−p_i)(Y1_i/q_i+Y0_i/(1−q_i))²`。
四个固定HT候选×五完整来源世界，**20组均值+方差全部逐Fraction相等**。oracle真ATE只从完整真潜在结果审计计算，不影响公开预测。

### 关键反例一：公共e(X)正确也不能自动处理未观测混杂

HIDDEN_U_BOTH世界公开e(X0/X1)=1/4、3/4**确实正确反映两X层的处理平均概率**，但由于在X内部U既影响治疗又影响Y0，给定X的交换性不足。公共X-HT期望**8/3**，真ATE为2，因而严格偏差**+2/3**。如果人能看到每人真正p_i，那么人工oracle HT期望2，但在实际观测权限中不可实现。与之严格匹配的HIDDEN_U_ASSIGNMENT_ONLY世界具有完全相同的八个真p_i，却删除U对潜在结果影响；公开X-HT于是又精确无偏，期望2。**隐藏分配概率异质性本身不必然构成未观测结局混杂，关键是遗漏原因是否与结果联合相关**。

### 关键反例二：方差下降不意味着保留原ATE目标无偏

WEAK_OVERLAP中未经裁剪的公共HT权重最大16、方差**257/30≈8.56667**，在完整真分配来源上的期望仍为2。事前预设clip[1/4,3/4]把最大倒数权重降为4，实际**方差变85/96≈0.88542**；但其期望变**5/2**，相对真ATE产生**+1/2**偏差。裁剪后的总体均方误差为`85/96+(1/2)^2=109/96≈1.13542`，虽然在这套有限人工世界中其真实ATE MSE较小，却不能说它仍是无偏ATE估计器、适用于其他结构或拥有普遍优越性。若目标是无偏识别，clip改变权重模式就会改变需要检验的假设与目标偏差。

### 关键反例三：自归一化Hájek与HT不是相同的设计无偏性质

在CORRECT_X世界，公开HT的完整无条件期望**2**，但PUBLIC_HAJEK仅在处理和对照都存在时定义，事件质量为**32687/32768**；定义条件下其期望恰`30371388/12584495≈2.4134`（不等于真ATE2）。本项既不把条件均值当作无条件比较，也不把undefined来源记0。其他世界所有Hájek条件均值与大整数Fraction方差均保存完整机读JSON，未因数值不漂亮或结果阴性删除。自归一模型不同损失、不同精确来源支持，应区分其方差/偏差效应；未做大样本性质推断。

### 正值性失效：不能用预测分母硬凑“成功估计”

POSITIVITY_FAILURE真实第一层X0个体永不治疗，第二层X1个体永不对照，只有一个可观测赋值来源、真实概率1；普通未匹配组间差恰为**4**（两个X层不同潜在本底叠加处理），真ATE由人工潜在结果oracle知为2。由于没有任何X层交叉治疗支持，**公共X-HT/知道p的oracle HT/错误常量HT/裁剪HT和全部Hájek结果均严格`null`**，状态是`UNIDENTIFIED_NO_POSITIVITY`，防止把任意事后有限数值当做对原目标的可信识别。完整真潜在反事实表只供方法验收，不等于现实研究中已观察全部反事实。

## GitHub真实执行、原数据与验收级别

[纯Python标准库Fraction和39项单元测试](r219_exact_inverse_probability_weighting.py)实现各项有限来源HT/ratio估计、真正赋值联合概率、极端来源、ESS、错模型/截尾/不正值性标志与第二独立解析数学验证。[GitHub Actions run39749875165](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39749875165) Python3.11和3.12各**39项单元测试、78次全成功**；第三job完整输出六世界、1281原分配来源、全部源归一与SHA复核，三个job均success，原资料由[机器人永久提交e75fd5dc](https://github.com/edwardsage419/Psychohistory-Research/commit/e75fd5dc9452b3ca02d972e690f8746619c7b568)同步main。

- [完整六世界机读评估](R219_EXACT_RESULTS.json)，SHA256 `094cbf0bdd70ea7d0dfea9c03903f7a82f38f0a21e6843c29a5aed0649b713be`。
- [1281个真正处理赋值原来源及全部方法逐原样本成绩CSV](R219_ALL_1281_ORIGINAL_TREATMENT_ASSIGNMENT_SOURCES.csv)，SHA256 `b928345812d28c121290cbde22041ea7288c90a42053fc0c6bb324b27c3c9958`。
- [原资料文件SHA、样本数及两路验收机器记录](R219_FINAL_MACHINE_ACCEPTANCE.json)。
- [事后正式有界E1结题机器记录](R219_FINAL_ACCEPTANCE_STATUS.json)。
- [真实原239候选目录](../../docs/MODEL_CANDIDATE_CATALOG_v0.1.json)，R219映射为09-010，不复用补充研究错误后缀。

**R219=CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_IPW**。只是有限8人工单位的IPW机制和识别限制，不是现实人类社会因果效应或独立历史预言。新增E2=0、E3=0；R073及PESEN v0.1均冻结。下一真实原目录 **09-011 Doubly Robust Estimation**，连续研究编号拟为R220；仍先完成全部原239模型，再统一归纳分类，最后熔炼。
