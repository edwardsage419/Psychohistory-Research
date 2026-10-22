# R215 双重差分（09-006）：12人工两期面板、3264完整来源与政策同步冲击的观察不可辨识

日期：2026-10-22（Asia/Taipei）。真实239项模型目录 **09-006 Difference in Differences（P1）**，有界数学研究状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_TWO_PERIOD_DID**。新增真实人类E2=0、真实历史E3=0；不使用真实政策、社会实验或外部研究对象。

## 直接来源、科研权限与预先冻结的设计

Abadie (2005), [Semiparametric Difference-in-Differences Estimators](https://doi.org/10.1111/0034-6527.00321), *Review of Economic Studies* 72:1–19，说明传统DiD依赖无处理情况下反事实组均值平行趋势；Bertrand, Duflo & Mullainathan (2004), [How Much Should We Trust Differences-In-Differences Estimates?](https://doi.org/10.1162/003355304772839588), *QJE* 119:249–275，说明序列相关与标准误推断在多期真实政策资料中的重要性。本研究仅是**自建四人工单位两期固定面板、完整有限噪声数学来源**；未复现上述原作者任何真实实证、估计样本、渐近推断或cluster-robust标准误结论。

事前冻结的[12真世界、两种噪声生成、3264完整来源及因果边界](../../protocols/R215_DID_12_WORLDS_3264_EXACT_NOISE_SOURCES_PRESCORE_FREEZE_2026-10-22.md)，GitHub [提交762c418d](https://github.com/edwardsage419/Psychohistory-Research/commit/762c418d1b13d2daa2dfd4655fa3f24cac3cfd20)，**早于实际评分**。固定四个人编号0..3，其中控制0、1，两名处理对象2、3；时间t0为政策前，t1为政策后，仅处理组在t1接受目标政策。所有四单位都有前后完整观察，未引入回归拟合、第三时期或事后选择处理组。

## 完整真实人工源和两个噪声相关结构

每个模型预设四人未接受目标政策时的固定基线与人工自然趋势、共同时期冲击、独立同时冲击、预期或溢出等项。真因果目标固定为**同一时期t1、同一环境下处理组两人的目标政策直接效应**均值`ATT=(tau_2+tau_3)/2`；估计器只能看到真实实际观察值，不准读取为了审计而另外保存的“如果没有目标政策”个人反事实面板，也不能读取已冻结真参数。

两种预设噪声：
1. `CELL_INDEPENDENT`：四人×两期8个独立±1等概率人工噪声。每世界有2^8=256条**完整潜在来源状态**，各真实来源概率1/256。
2. `UNIT_PERSISTENT`：每人工单位只有一个±1噪声，在t0、t1完全相同。每世界2^4=16条人工噪声来源，概率1/16。两噪声机制分别在12个真世界中固定，合计**12×(256+16)=3264条原始人工面板完整来源**，24个世界×噪声方案结果单元。

这些互斥来源状态不是3264次现实独立实验或3264位真实人。每条来源保留完整8个实现观察值、真正非政策潜在面板、实际目标政策直接效应、源噪声及概率、实测DiD和POST_ONLY值、两种相应平方误差；每条件的所有原来源概率严格归一为1。

## 预注册估计器与双路独立数学验证

**DiD**：处理组t1与t0的观察均值变化减去控制组t1与t0的观察均值变化。程序分别从两个组的人员先个人前后差再组平均，以及先按四个组×时期格求平均再双重差，二者全原来源逐Fraction严格相同。

**POST_ONLY**：只用t1两名处理人的实际观察均值减t1两名控制人的实际观察均值；其无需平行趋势前提作描述性比较，但作为政策因果估计器需额外约束组之间的固有水平差异。

第三个数字**true ATT oracle**是人工真生成因果参数，专门供审计判断偏差，不能当作第三种从实际观察数据能执行的估计器。

每世界×噪声方案计算两个实际估计器相对于真ATT的完整来源期望、真实偏差、真实方差与均方误差MSE；MSE以各源真实误差平方加权和以及独立公式`MSE=Bias²+Var`逐Fraction两路一致。期望另由已知冻结无噪声因果结构直接推导，与原完整噪声来源枚举独立一致。此处**没有**研究有限样本中的经验标准误、置信区间、wild cluster bootstrap、TWFE多批次或真实采样分布外推。

## 十二个预设世界完整结果

下表为`CELL_INDEPENDENT`的数学源概率积分结果（单位期独立噪声），括号内DiD MSE与真政策ATT相比较。对于`UNIT_PERSISTENT`，同世界的DiD期望和偏差完全不变，但DiD MSE减去2；后期单独比较POST_ONLY的噪声方差在两方案均是1。

|人工真世界|真ATT|DiD期望|DiD偏差|DiD原来源MSE|POST_ONLY期望|
|---|---:|---:|---:|---:|---:|
|VALID_CONSTANT_TWO|2|2|0|2|4|
|VALID_LEVEL_GAP|2|2|0|2|12|
|VALID_COMMON_SHOCK|2|2|0|2|4|
|VALID_HETEROGENEOUS|2|2|0|2|4|
|VALID_NULL|0|0|0|2|2|
|VALID_NEGATIVE|−2|−2|0|2|0|
|NONPARALLEL_TREATED_UP|2|4|+2|6|6|
|NONPARALLEL_TREATED_DOWN|2|1|−1|3|3|
|CONTROL_SPILLOVER|2|1|−1|3|3|
|ANTICIPATION|2|1|−1|3|4|
|SIMULTANEOUS_TREATED_SHOCK_NO_CAUSAL|0|2|+2|6|4|
|HETEROGENEOUS_TRENDS_BALANCED|2|2|0|2|4|

[主结果JSON](R215_EXACT_RESULTS.json)保存24世界×噪声方案的完整有理数期望、偏差、真方差、MSE和独立解析公式。绝不可把不同世界、政策和人为赋值来源直接合并为随机代表真实社会资料的风险。

### 核心反例一：两份完整观察数据同分布，真政策效果却相差2

`VALID_CONSTANT_TWO`世界中，t1处理组政策真实直接效应+2，无其他处理组特有同步冲击。另一个`SIMULTANEOUS_TREATED_SHOCK_NO_CAUSAL`世界目标政策真实因果效果**0**，但处理组t1有独立于目标政策的外部共同冲击+2。

两世界四人全部两个时期的固定非噪声观察潜在面板**逐单元完全相同**；对同一原噪声向量、同一噪声模式`CELL_INDEPENDENT`或`UNIT_PERSISTENT`，八个实际观察数字**逐条完全相同**。因此其**全部随机观察面板的联合分布也完全相同**，所有只依赖这些观察数据的DiD或POST_ONLY程序根本无法从该次数据区分：两个世界DiD期望同为2，POST_ONLY期望同为4，但目标政策真ATT分别为2和0。这是由未排除并发政策外冲击导致的**因果不可识别性反例**，不能用单纯增加相同两期观察的人数自动排除。只有外部结构证据、额外政策设计、合理的处理组反事实限制等才能提升因果解释权限。

### 核心反例二：偏离组均值平行趋势引入系统偏差

`NONPARALLEL_TREATED_UP`固定控制组无政策趋势均值+1、处理组无政策趋势均值+3，真政策ATT+2，但实际DiD平均计算为**4**，偏差+2。在`NONPARALLEL_TREATED_DOWN`处理组无政策趋势0、控制组+1，则真ATT+2而DiD平均为**1**，偏差−1。

`HETEROGENEOUS_TRENDS_BALANCED`各人工单位自然趋势分别(0,2,0,2)，每个人趋势**并不相同**，但两组各两人的未处理趋势**均值均为1**，所以DiD数学平均仍准确恢复真ATT+2。正例明确限定经典两组两期平均处理效应的识别假设是**组均值的反事实平行**，不是每一人的完全同速增长。

本项只有**一个政策前时期**，现实中无法直接从同一数据实现两个不同处理前期的趋势差异检验。这里由人工oracle生成函数可以指出哪些世界反事实平行，但**不能把这当作从一次现实观察自动验证平行趋势**。

### 核心反例三：处理前预期、对照组受影响均破坏简单DiD目标

`ANTICIPATION`世界中处理组t0已有+1的人工政策预期影响，t1真目标政策额外直接效果仍+2，DiD由于把受影响t0当“无政策基线”而在完整来源期望仅为**1**。`CONTROL_SPILLOVER`世界对照组虽然没有被赋目标直接政策处理，但t1实际结果受到政策相关的+1人工间接溢出，结果其作为“未暴露对照趋势”也不再可用，真处理组直接ATT+2而DiD期望仍仅**1**。两者都显示**SUTVA/干扰限制、没有提前响应**必须根据实际因果目标和政策机制逐一澄清；数学对照算法自身不能创造这些识别假设。

### 核心反例四：单位内时间相关影响方差与可靠度判断

同样四人、同样两期、同样12真实人工政策世界，仅噪声设定不同：
* 每单位×时期独立随机±1：DiD每个人的前后差出现两个独立噪声，以组平均再次加减，其真噪声方差固定**2**；POST_ONLY只取四个t1值加权，真噪声方差固定**1**。
* 每单位时间持续的±1噪声：DiD对同一人的前后差消除该常数噪声，所以真噪声方差**0**；POST_ONLY仍为**1**。

所以某个估计程序即使无偏，其MSE相对其他程序的大小也依赖已知样本/噪声结构与基线水平。这里的`Var=0`是**特别冻结的完全同单位持久噪声假设**下的人工恒等式，绝不能推广成真实DiD中串行相关不重要、置信区间可取零或普通面板估计必定无误差。Bertrand等(2004)所警示的是多期、政策串行相关以及无效标准误等更一般的现实问题，本实验并未重演其标准误研究。

## 原生实现与真实归档

[原生Python标准库和35项测试](r215_exact_did_panel.py)严格依据冻结世界×噪声来源真实评分。第一轮[Actions run39740995365](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39740995365)因一个解析途径的辅助均值函数不能直接求生成器长度，发生测试失败；未将失败结果作为科学证据。程序已由[修复提交7872a6a8](https://github.com/edwardsage419/Psychohistory-Research/commit/7872a6a808e4aec2e6f7145bd6f4bb58439e4f66)只修正算术辅助函数、**不改变冻结任何因果世界或评分**。

最终[GitHub Actions run39741076513](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39741076513) Python3.11及3.12各**35项单测，共70项全部成功**，第三作业确实生成24个世界×噪声模式结果和**3264条完整人工噪声原来源CSV**，核验两种解析与数学MSE路径、完整来源概率、观察同分布反例及SHA，全部三个jobs成功，机器人永久提交[原结果归档1e58b4f6](https://github.com/edwardsage419/Psychohistory-Research/commit/1e58b4f67edb5155d5fab56c362b60d34d1321bb)到main。

原始固定材料：
* [计算前冻结协议](../../protocols/R215_DID_12_WORLDS_3264_EXACT_NOISE_SOURCES_PRESCORE_FREEZE_2026-10-22.md)；
* [全部24个真世界×噪声模式数学评分](R215_EXACT_RESULTS.json)，SHA256 `abb7926c9d773e34045cb22dcf10b29122edf85fd680835522b1afb6adc0c24e`；
* [全部3264条原人工政策面板随机来源及双估计平方误差](R215_ALL_3264_ORIGINAL_PANEL_NOISE_SOURCES.csv)，SHA256 `a3c7bc22f75b1dbc4a13853d734f8741af461813325f7cdb4f6c50face004ef6`；
* [实际全部来源数与文件SHA机器验收](R215_FINAL_MACHINE_ACCEPTANCE.json)；
* [科研事后正式有界结题收据](R215_FINAL_ACCEPTANCE_STATUS.json)。

**R215=CLOSED_BOUNDED_E1_ARTIFICIAL_TWO_PERIOD_DID**，仅覆盖原239目录`09-006`的有界两期DiD数学方法学习，不代表一般多期/错位政策DiD分析、真实政策效果或历史过程预测得到独立实证确认。新增人类E2=0、真实历史E3=0。R073及PESEN v0.1继续冻结。下一实际原239目录为**09-007 Event Study Design（P1）**，研究编号R216。继续全部R完成后分类、最后熔炼。
