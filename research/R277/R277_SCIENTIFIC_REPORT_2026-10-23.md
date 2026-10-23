# R277 正式科学报告：边缘预测评分完全相同仍存在时间依赖结构错设

日期2026-10-23 Asia/Taipei。原239候选目录12-007 Model Misspecification Checks（P0）。研究编号R277。科研证据范围：有界人工E1有限二元Markov数学世界。

## 研究出处和诊断问题
Gelman, Meng & Stern (1996), *Posterior predictive assessment of model fitness via realized discrepancies*, Statistica Sinica 6:733–807（主文733–760，之后为评论讨论），原作者公开文本 https://sites.stat.columbia.edu/gelman/research/published/A6n41.pdf；Roberts et al. (2017), *Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure*, DOI https://doi.org/10.1111/ecog.02881。R277以自定义三状态概率机制检查**仅看边缘评分不能证明完整联合过程正确**；并未用原作者真实实验数据或其特定预测模型。

## 事前冻结的三个人工Markov过程
[冻结研究协议](../../protocols/R277_MISSPECIFICATION_3_MARKOV_DEPENDENCE_WORLDS_192_FULL_SOURCES_PRESCORE_FREEZE_2026-10-23.md)，独立SHA提交[923a161b](https://github.com/edwardsage419/Psychohistory-Research/commit/923a161bbdc012c138e53f1fa316e6085ff2704e)。

构造长度6的有序二状态序列X1…X6，X1公平取0/1，随后每次转移保持当前状态的概率s；三个真实模型分别ANTIPERSISTENT s=1/4、IID_FAIR s=1/2、PERSISTENT s=3/4。单条完整序列有5个保持指示，T为相邻相同次数；原source概率为(1/2)s^T(1−s)^(5−T)。每模型穷举全部2^6=64个有序source，每种都有严格正质量，三个world合计**192种完整带模型标识人工原source配置**，不是192个受试或真实历史时期。

三个模型每个时刻的X边缘均严格Bernoulli(1/2)，因而冻结常数半概率预测器的每个原source、每个时点单行Brier都为1/4；仅报告逐点评分会错误掩盖三机制的不同连续依赖结构。独立真实Markov转移保持指示为5个iid Bernoulli(s)，T~Binomial(5,s)。

## 两条独立推导与原source重新审核
路线A对三个world各64个完整六bit原source逐项记录序列、5保持指示、T、原质量、六个边缘Brier和事前预定T≥4或T≤1两个区域标记，并将原质量加权求解T全部6类别PMF、均值、两侧触发概率，以及每时点边缘P(X_t=1)=1/2。
路线B绝不调用六bit原来源枚举，直接依据五次独立转移保持指示，建立T~Binomial(5,s)，计算所有PMF、E[T]=5s、上尾P(T≥4)=5s^4(1−s)+s^5和下尾P(T≤1)=(1−s)^5+5s(1−s)^4；边缘由对称公平首状态推出。三完整world所有来源数学结果与独立组合推导逐Fraction一致。
路线C GitHub Actions第三独立机器审计直接解析全部192原CSV，逐条重构序列、保持指示、来源质量、六次逐点Brier、两侧尾区、按原概率质量汇总得到完整PMF，再与独立Binomial(5,s)和SHA256逐项比对。来源零遗漏。

## 事前冻结真值与正确解读

|真实机制|保持概率s|E[相邻相同次数T]|P(T≥4)|P(T≤1)|每个时点Brier|
|---|---|---|---|---|---|
|ANTIPERSISTENT|1/4|5/4|1/64|81/128|1/4|
|IID_FAIR|1/2|5/2|3/16|3/16|1/4|
|PERSISTENT|3/4|15/4|81/128|1/64|1/4|

所有模型在同样半概率边缘预测下Brier均1/4，但真实持续性机制进入预定高T区的概率为81/128，对比IID模型的3/16；真实反持续机制进入低T区的概率也为81/128。这是完整联合序列依赖模型的诊断能力。

**重要比较边界**：上述两侧分别是有向诊断区域，若对两侧同时检查，则在IID原参考世界的联合触发概率为3/16+3/16=3/8；不得说“同时报告上下尾仍保持3/16家族误报率”。本实验的3/16来自特定冻结整数区域概率，并未事先采用标准5%显著性阈值，也不涉及从真实世界估计Markov依赖强度或检验真实数据多重比较误差。

## GitHub执行与科学范围
[Python标准库源码](r277_exact_misspecification_markov.py) · [192完整原source CSV](R277_ALL_192_ORIGINAL_MARKOV_MISSPECIFICATION_SOURCES.csv) · [所有PMF和尾概率结果JSON](R277_EXACT_RESULTS.json) · [机器SHA256凭证](R277_MACHINE_RECEIPT.json)。[GitHub Actions run39904180046](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39904180046)所有三job completed/success；Python3.11及3.12各50项真单测，共100项通过；第三独立来源审计通过，全部原source由机器人永久main归档[12b5de59](https://github.com/edwardsage419/Psychohistory-Research/commit/12b5de59e410a5044e480b192e60df7e72436a14)。

来源CSV SHA256 `3faf8616c97f7c0bbc46284ec7a2598bd9d6af5211551e824ee2a766cc6f9cf9`，结果JSON SHA256 `9cffc3dea66b758e7daf5521c81f458ebb1ce10b7eb18fe818a51d9569f8f96b`。源有序类型全部人工，无新增真人E2、真实历史E3、外部历史回测或真实社会心理机制证据。R073及PESEN v0.1仍冻结。下一原目录12-008 Model Averaging and Ensembles（P2，拟R278）。完整R系列学习研究完成后再进行统一归纳、分类及原创模型熔炼。
