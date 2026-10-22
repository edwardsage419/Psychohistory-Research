# R213 工具变量估计（09-004）：8个有效与违规人工IV世界、128条完整鼓励来源和LATE识别边界

日期2026-10-22（Asia/Taipei）。严格对应原239模型目录 **09-004 Instrumental Variables（P1）**。最终科学状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_BINARY_IV**。仅完整穷举八人有限来源下的人工数学关系，新增真人E2=0、真实历史E3=0。

## 原文与方法口径

Imbens & Angrist (1994), [Identification and Estimation of Local Average Treatment Effects](https://doi.org/10.2307/2951620), *Econometrica* 62(2):467–475，研究可促使实际参与状态改变的工具对顺从子群的局部平均效果识别；Angrist, Imbens & Rubin (1996), [Identification of Causal Effects Using Instrumental Variables](https://doi.org/10.1080/01621459.1996.10476902), *Journal of the American Statistical Association* 91(434):444–455，使用随机鼓励、非完全服从与潜在结果框架说明工具估计。此次数学模拟不等于作者原研究实证复现，未在任何真实数据上证明工具有效性或估计真实因果参数。

[事前冻结人工IV协议](../../protocols/R213_IV_8_WORLDS_128_ORIGINAL_ENCOURAGEMENT_SOURCES_PRESCORE_FREEZE_2026-10-22.md)提交[743a3a5b](https://github.com/edwardsage419/Psychohistory-Research/commit/743a3a5b507c999dd00821b97d6fa34c7f9e6b7e)，严格早于程序和任何实验评分；锁定8世界、潜在单位身份、独立或不独立的Z分配概率、单调性、排除限制以及反例，不在读结果后选择有利来源和模型。

## 128完整原来源与估计信息权限

每世界有8个带标号潜在人工类型，主阶层包括COMPLIER（鼓励Z从0到1使实际处理D从0到1）、ALWAYS（不论鼓励都处理）、NEVER（永不处理）、DEFIER（鼓励使D从1到0）。单个真实人工单位的潜在结果`Y(d,z)=base_i+τ_i·d+δ·z`；δ仅在两个**人为故意违反排除限制**的世界中为1，其他为0。8个单位每个有Z=0、Z=1两种潜在鼓励源，因此每世界**16个原联合来源**，8世界全部**128个源原子**。随机工具时每人鼓励概率1/2，非独立工具世界中前4种顺从者更可能接受鼓励，按原概率`P(i,z)=P(i)P(Z=z|i)`完整计权，每世界和为1。

观察结果只包括实际分到的Z、真正收到的处理D(Z)及结果Y(D(Z),Z)；完全潜在的D0,D1,Y0,Y1与固定真单位效应保留在源CSV用于**oracle验证和假设检查**，不可从单次观察宣称已识别。真实目标：整体ATE=8人的个体τ平均；顺从者LATE=所有COMPLIER的真实τ平均（无人顺从时不存在这个子群目标）。观察数学比值Wald为`[E(Y|Z=1)−E(Y|Z=0)]/[E(D|Z=1)−E(D|Z=0)]`，后一差是first stage，若0则明确报告`UNDEFINED_ZERO_FIRST_STAGE`，不可强置0。

对**Z独立潜在来源类型**的世界，固定潜在主阶层另有两个数学恒等式，完整128原来源的条件均值逐Fraction验算一致：`FS=(#COMPLIER−#DEFIER)/8`；`ITT_Y=Σ_i[(D_i(1)−D_i(0))τ_i]/8+δ`。后一式中的δ仅对人工直接工具效果成立。Z非独立的世界明确标记这两条结构式**不能替代观察条件均值**；正是把工具外生性误当已获证据会造成偏差。

## 所有八世界全部成果：Wald、LATE和总体ATE

|真世界|第一阶段FS|Wald观察比值|真实COMPLIER LATE|真实总体ATE|已破坏的关键条件|
|---|---:|---:|---:|---:|---|
|FULL_COMPLY|1|5/2|5/2|5/2|无|
|MONOTONE_MIX|1/2|3|3|3/2|无；但LATE≠ATE|
|WEAK_COMPLIERS|1/8|4|4|1/2|无，相关性正但偏弱|
|NO_COMPLIERS|0|**未定义**|**无顺从者，未定义**|2|相关性不成立|
|WITH_DEFIERS|1/4|**0**|2|2|单调性不成立|
|EXCLUSION_VIOLATION|1/2|**5**|3|3/2|排除限制不成立|
|WEAK_EXCLUSION|1/8|**12**|4|1/2|排除限制不成立、第一阶段较弱|
|Z_CONFOUNDING|1/2|**29/2=14.5**|3|3/2|鼓励工具与潜在类型不独立|

注意WEAK_COMPLIERS第一阶段**非零**，在这套人工无噪声总体期望下仍满足已冻结的有效工具条件，Wald精确=4即真LATE。此结果**没有验证**实际有限样本弱工具估计分布及其置信区间覆盖、检验大小或常见估计偏差，因为没有从有限总体重复抽取真实样本建立估计不确定性。表中“弱”只指人口第一阶段差异小。

## 不能回避的四种违反假设反例

**LATE≠ATE，即便工具有效**：MONOTONE_MIX中四名COMPLIER效果2,2,4,4，其余两名ALWAYS与两名NEVER效果0。独立鼓励Z与排除/单调性都成立，Wald=平均顺从者效果`(2+2+4+4)/4=3`；然而全人口八人ATE=12/8=**3/2**。工具有效性通常只在假设允许范围内识别**局部**政策响应者效果，不能直接标榜全人口均值。

**违反单调性**：WITH_DEFIERS中有四名COMPLIER(τ=2)和两名DEFIER(τ=4)，另外两人NEVER，净第一阶段`(4−2)/8=1/4`虽不为零，但鼓励对真实结果的减少与增加来源相抵，`ITT_Y=(4×2−2×4)/8=0`，因而Wald=0，仍不等于COMPLIER LATE2。不能将观测first-stage正数误认为每名个体D(1)≥D(0)。

**排除限制与弱第一阶段放大**：EXCLUSION_VIOLATION让工具Z额外直接增加人工结果1，first-stage1/2，故Wald从真实LATE3变成5，偏离2；若complier只占8人的1名，first-stage1/8，而工具同样直接增加1，WEAK_EXCLUSION比值从真LATE4变成**12**，偏差8。这是固定总体身份式下的`δ/FS`放大，不是给真实工具强弱设置统一阈值，也不能把它等同于有限样本IV偏误定理。

**鼓励Z自身不独立**：Z_CONFOUNDING让四名潜在COMPLIER的固定基线结果为10，其余四人基线为0，同时COMPLIER接受鼓励概率3/4，其他人1/4，人工总体P(Z=1)仍精确1/2。由于鼓励组系统富集高基线来源，观察条件均值的差远超过净接受处理的真局部效果，Wald=**14.5**，真LATE=3。这直接说明“工具与结果存在关联、第一阶段显著非零”并不能凭统计关联证明外生性。

**相关性完全为零**：NO_COMPLIERS中四名ALWAYS、四名NEVER，任何人的实际D都不会因Z改变，FS0。即使八个人的潜在处理τ都为2且总体ATE=2，Wald的分母仍是0；已知人工oracle的全体平均效果并不会因为鼓励工具能否影响D自动可识别。不得填任何数值Wald结果。

## 完整复算、机器人原证据与结题状态

[原生标准库Fraction脚本](r213_exact_instrumental_variables.py)复算16来源条件概率、八世界真潜在身份、工具ITTs、FS、Wald、LATE、ATE及排除/独立/单调性有效标记；所有非零分母与理论主阶层身份进行双路Fraction核对。

[GitHub Actions run39739297527](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39739297527)：Python3.11、Python3.12各**39项单测，总78项全部成功**；第三作业实际完整生成**8世界、128原鼓励来源**并核验全部原概率、八种冻结反例数值、结果SHA，机器人永久同步main [提交bf2f8282](https://github.com/edwardsage419/Psychohistory-Research/commit/bf2f82828acf04fbe5ba852ae9bc337d20a0f07c)。三个CI jobs全部success。

永久材料：
* [事前冻结8世界IV审计协议](../../protocols/R213_IV_8_WORLDS_128_ORIGINAL_ENCOURAGEMENT_SOURCES_PRESCORE_FREEZE_2026-10-22.md)
* [八世界完整分数结果JSON](R213_EXACT_RESULTS.json)，SHA256 `81f72fe5e977d52a8b62f289c73d93da349efe4ed497f8ff64e2f05bf4d8c948`
* [全部128条原因子×鼓励来源CSV](R213_ALL_128_ORIGINAL_INSTRUMENT_SOURCE_ATOMS.csv)，SHA256 `071e2eb91185fd7c47d6534363e322ee5f0349862995dfa20dd84542c7d8fe48`
* [原数据SHA、来源归一、口径边界机器验收](R213_FINAL_MACHINE_ACCEPTANCE.json)
* [科学结题后机读验收](R213_FINAL_ACCEPTANCE_STATUS.json)

本项为真正原239目录**09-004**的有界IV数学机制学习，仍缺真实鼓励实验E2、真实历史E3，亦没有证明任何可用现实工具的独立性/排除限制。**R213=CLOSED_BOUNDED_E1_ARTIFICIAL_BINARY_IV**，R073与PESEN v0.1冻结；下一实际目录**09-005 Regression Discontinuity Design（可按连续研究编号R214）**。保持全R学习后再分类、最后熔炼。
