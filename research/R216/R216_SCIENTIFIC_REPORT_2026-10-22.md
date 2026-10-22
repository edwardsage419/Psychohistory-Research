# R216 事件研究设计（09-007）：交错实施队列、24576条完整人工面板来源与已处理对照污染

日期2026-10-22（Asia/Taipei）。真实原239项目录 **09-007 Event Study Design（P1）**。最终科学状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_STAGGERED_EVENT_STUDY**。研究仅使用自造三队列四期人工面板；新增真人E2=0、真实历史E3=0，不包含任何实际政策评估、真实历史事件或外部研究数据复现。

## 文献与算法边界

Sun and Abraham (2021), [Estimating dynamic treatment effects in event studies with heterogeneous treatment effects](https://doi.org/10.1016/j.jeconom.2020.09.006), *Journal of Econometrics* 225:175–199，指出处理时点不一致、处理效应异质时，事件研究中的传统TWFE lead/lag系数可能受其他时期处理效应污染。Callaway and Sant’Anna (2021), [Difference-in-differences with multiple time periods](https://doi.org/10.1016/j.jeconom.2020.12.001), *Journal of Econometrics* 225:200–230，给出组别×时期ATT的识别与多期变化框架。本R216仅以这两篇文献为统计机制参照，**没有实施Sun–Abraham交互加权估计器、完整TWFE回归、Callaway–Sant’Anna一般条件ATT估计、标准误估计或其原论文实证数据**。其中故意错误的晚组对照是一个具体朴素2×2 DiD对比，不能偷换为真实TWFE的回归系数。

[完整六世界与24576原噪声面板的事前冻结协议](../../protocols/R216_EVENT_STUDY_6_WORLDS_24576_ORIGINAL_STAGGERED_PANELS_PRESCORE_FREEZE_2026-10-22.md)在原研究计算与评分前提交[51125f9a](https://github.com/edwardsage419/Psychohistory-Research/commit/51125f9a8ba97a94cb22d872b38f5f9197b16986)，完整规定三组、四期、真实外生冲击、六个人工潜在结果世界、固定六事件对比以及所有源评分；没有以结果好坏选择有利时期或增减真实模型。

## 全部人工来源：三组、四期、六真世界

三个带编号的固定人工组：
- EARLY（E）在t≥2接受政策并永久持续；
- LATE（L）在t≥3才接受政策；
- NEVER（N）在t=0,1,2,3一直不接受政策。

全部固定四期t=0,1,2,3，对应12个组×时期观察位置。各位置噪声ε_{g,t}独立、等概率取±1，每人工世界**12条独立冲击构成2^12=4096条完整原噪声历史**，全部六真世界共**24576条原人工结果面板**，每原历史概率1/4096。对每份来源，保存全部12个噪声、12个实际可见Y、六种预定估计及按人工生成真政策效应评价的六个真实平方误差。

未处理基础潜在均值具有组固定截距E=+1、L=−1、N=0与共同时间趋势t；额外真政策效应、未处理结果组别冲击和政策前提前反应按如下六个设计世界事先固定：
1. **VALID_CONSTANT**：正式因果处理效果τ_{E,2}=2、τ_{E,3}=2、τ_{L,3}=2；平行未处理趋势成立，无提前反应。
2. **VALID_HETEROGENEOUS**：τ_{E,2}=1、τ_{E,3}=1、τ_{L,3}=3；组间政策效应异质但未处理趋势平行。
3. **VALID_DYNAMIC**：τ_{E,2}=2、τ_{E,3}=4、τ_{L,3}=1；早组真实效应随事件时间增长。
4. **POST_EVENT_SHOCK_MIMIC**：全部真政策效果0，却在人工未处理潜在均值中额外添加E2=2、E3=4、L3=1的**同期政策后组别冲击**。这项非政策来源与VALID_DYNAMIC在全部12个实际观测点、全部4096噪声历史上**逐条观察结果完全相同**，但真政策效果分别为(0,0,0)与(2,4,1)。
5. **DIFFERENTIAL_PRETREND**：全部政策效果0，E组未处理潜在均值额外随t上升+t，L和N仅公共趋势；故E在政策前已与NEVER的斜率不同。
6. **LATE_ANTICIPATION**：正式政策效果τ_{E,2}=1、τ_{E,3}=2、τ_{L,3}=3；L在政策前t=2已有明确政策预期效应+1。该组的t2虽然尚未正式接受处理，却不再是干净的未受政策影响基线。

以上是真潜在结果规则，仅用于完整人工源生成与oracle核验，不属于估计器可见的信息；不能将六世界作为从现实经济或历史群体抽取的样本。

## 六种预先固定的时间对比与独立来源风险

全部差值的实际计算**只读各组时间的观察结果**；三项使用从未处理组N的事件对比（条件依赖未处理平行趋势与不提前反应）为：

`E_k0_clean=(E2−E1)−(N2−N1)`，真目标τ_{E,2}；
`E_k1_clean=(E3−E1)−(N3−N1)`，真目标τ_{E,3}；
`L_k0_clean=(L3−L2)−(N3−N2)`，真目标τ_{L,3}。

两项固定前趋势/提前反应诊断：
`E_pre_placebo=(E1−E0)−(N1−N0)`，
`L_pre_placebo=(L2−L1)−(N2−N1)`。

最后一项**错误使用已处理群体作为对照**的朴素对比：
`E_k1_BAD_L_ALREADY_TREATED=(E3−E1)−(L3−L1)`，虽然目标是τ_{E,3}，但t3的L已经正式接受政策。有效平行趋势下其真正来源期望为**τ_{E,3}−τ_{L,3}**，不是τ_{E,3}。这是确切的符号污染反例，**不是对Sun–Abraham论文TWFE估计器的数值复现**。

六种固定对比在12组时间位置均有恰四个±1权重。12外生噪声各自独立方差1，故解析噪声方差**4**。对每人工世界与每种预冻对比的**4096完整独立噪声历史逐项计算**，并与两条独立Fraction公式核验：其一以实际四组结果独立差分运算对照预计算12维权重向量内积；其二全来源均值、方差与真实平方误差逐Fraction对照`E[估计]=Σw·μ`、`Var(估计)=Σw²=4`、`MSE=Bias²+4`。六世界×六指标形成**36个完整条件评分**，全部两个路径实际完全相等。

## 全部六世界的关键数学结果

以下“干净E滞后1”是EARLY政策后t3相对于t1且以NEVER对照；“错误晚组对照”则误以t3已经受处理的L为对照。数值均是对完整4096个原独立冲击来源的**期望**，不是一条观察的随机估计值。括号中列真EARLY滞后1政策效应。

|真世界|真τ_E3|干净N对照E_k1期望|错误已处理L对照期望|E前期placebo期望|L前期placebo期望|
|---|---:|---:|---:|---:|---:|
|VALID_CONSTANT|2|2|0|0|0|
|VALID_HETEROGENEOUS|1|1|**−2**|0|0|
|VALID_DYNAMIC|4|4|3|0|0|
|POST_EVENT_SHOCK_MIMIC|0|**4**|3|0|0|
|DIFFERENTIAL_PRETREND|0|2|2|**1**|0|
|LATE_ANTICIPATION|2|2|−1|0|**1**|

正确解释“干净N对照”：这一方法在**VALID_CONSTANT、VALID_HETEROGENEOUS、VALID_DYNAMIC**三个预冻真平行世界，对应τ_E2、τ_E3、τ_L3三个政策窗口确实完全无偏；但在**POST_EVENT_SHOCK_MIMIC**，虽然NEVER从未被处理、但EARLY的未处理反事实在政策后发生组专有额外冲击，故观察事件差不是政策因果效果；在**LATE_ANTICIPATION**，L_t2基线已受未来政策预期影响，L_k0_clean期望2、真τ_L3=3，偏差−1。

### 反例一：正确正向处理效果，错误对照却为零甚至负值

VALID_HETEROGENEOUS世界：早组政策后t3真实τ_E3=+1，晚组t3真实τ_L3=+3，两组对政策本身都是**正向**；但错以t3已经受处理的晚组为对照的对比期望`1−3=−2`，对真实目标早组τ_E3=1的偏差−3，独立全部来源真实均方误差为`(−3)^2+4=13`。若以真正从未处理的N作对照，早组t3对比期望+1、无偏、同样外生噪声风险仅为4。这是**已处理组污染**的有限精确算例，不能从“结果负号”反推政策真的伤害早组。

VALID_CONSTANT里所有组正式处理效果都是2，错误L对照差为0，虽然早组真政策效果2。VALID_DYNAMIC早组真滞后1效应4，晚组当期效应1，错误差成3，仅保留早效应与晚效应之差。这个结果不代表一般双向固定效应回归的精确权重结构，只是错误指定对照的已处理比较。

### 反例二：零预趋势仍不保证政策后平行潜在结果

VALID_DYNAMIC和POST_EVENT_SHOCK_MIMIC在三个队列四个时期**全部12格的无噪声观察均值完全相同**，加上同样独立的12个Rademacher噪声来源后，**整个12维实际观察联合分布在所有4096条来源上逐一相同**。两世界所有实际估计器结果的条件分布因而无法区分，E与L预趋势诊断在两个世界的期望**全部都是0**。但真实政策效果在VALID_DYNAMIC为(E2,E3,L3)=(2,4,1)，另一世界全部为(0,0,0)，观察改善是政策后未处理结果组专属冲击制造的。假如只用政策前趋势或当前数据解释政策因果效果，无法证明后期不存在这个额外组冲击。此数学反例是预设不同潜在结果模型间的**观察不可辨识性**，不是一次真实实验支持这些模型等概率发生。

### 反例三：实际前趋势差异和政策提前反应是两种不同问题

DIFFERENTIAL_PRETREND即便真政策效应全零，早组有额外 untreated 时间斜率，E的前期placebo期望+1，可揭示当前人工趋势偏离；政策后E_k1_clean期望2不等于真政策效果0。LATE_ANTICIPATION不同：L组正式政策前已对**尚未开始的政策产生额外结果反应**，L前期placebo期望+1，L_k0_clean把受预期影响的t2用作基线而低估正式政策效应1。这两种模型的前期诊断都有信息，但诊断也依赖具体生成机制；对照选择、平行趋势及无提前反应是需要明确的识别假设，不能用“事件时间回归公式已算出来”替代。

## 机器验收与原始归档证据

[纯Python标准库Fraction原生程序](r216_exact_staggered_event_study.py)实现六预冻人工真政策时序和潜在未处理反事实、六固定事件对比、完整12独立±1原来源、各世界真实目标及其损失，以及两套分别实现的公式与逐来源一致性检查，不依赖蒙特卡洛或付费API。人工oracle用于报告真实政策ATT（由我们预先指定）而不参与预测。

[GitHub Actions run39744311501](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39744311501) Python 3.11与3.12各执行**41项单测，共82项全部成功**，第三job实际重算6世界×4096完整历史，核验原完整24576来源条数、六人工统计量、等价观察原路径、两路Fraction与文件SHA、并真正永久写回main；三个CI作业全部success，[机器人原材料归档提交77673e5a](https://github.com/edwardsage419/Psychohistory-Research/commit/77673e5a78fb4128a896baf9dc7d7e712bbff21f)。

正式可复算材料：
* [原计算前冻结协议](../../protocols/R216_EVENT_STUDY_6_WORLDS_24576_ORIGINAL_STAGGERED_PANELS_PRESCORE_FREEZE_2026-10-22.md)。
* [所有六世界×六事件对比真实Fraction风险JSON](R216_EXACT_RESULTS.json)，SHA256 **`cc7b0f96f46b932689fac7bee3d5a2fc947efe12728e9f3a8eb7c03abf139f10`**。
* [全部24576组×时期真实噪声向量、12实测结果、六对比与损失CSV](R216_ALL_24576_ORIGINAL_STAGGERED_GROUP_TIME_SHOCK_PANELS.csv)，SHA256 **`5bbac97d12dd504cce7f03e1d629736e7ed32c22f693d55ade7d2470b934dbf8`**。
* [全部源及SHA机器验收](R216_FINAL_MACHINE_ACCEPTANCE.json)。
* [正式E1结题机读收据](R216_FINAL_ACCEPTANCE_STATUS.json)，在CI真实成功和原全部来源永久归档后作事后承认。

**结论：R216=CLOSED_BOUNDED_E1_ARTIFICIAL_STAGGERED_EVENT_STUDY**。此次完成的是原239目录09-007下的一个有限人工识别机制审计，R215正式两期DiD与其R215-3P三期补充各自证据单独保留，不能以本R重复占09-006。无真人E2或历史E3，R073及PESEN v0.1继续冻结。下一真实目录条目为**09-008 Synthetic Control（合成控制法，可记R217）**，先完成全部原R研究再统一归纳分类，最后熔炼。
