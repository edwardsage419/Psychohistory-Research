# R215-3P 三期双重差分补充研究：768原集团时期噪声来源、前趋势与处理后冲击不可辨识

日期2026-10-22 Asia/Taipei。地位：**原目录09-006 Difference in Differences 的补充人工机制研究**，补充子编号 **R215-3P**，不能作为第240个模型条目计数，也不覆盖已经归档的**R215两期正式报告与3264条来源**。本补充科研状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_THREE_PERIOD_DID_SUPPLEMENT**，新真人E2=0、真实历史E3=0。

## 目录冲突与来源边界（必须先读）

本轮其他执行链已先提交[原R215正式两期设计](../../protocols/R215_DID_12_WORLDS_3264_EXACT_NOISE_SOURCES_PRESCORE_FREEZE_2026-10-22.md)、[科学报告](R215_SCIENTIFIC_REPORT_2026-10-22.md)，并经[CI 39741076513](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39741076513)验证12世界×两种噪声共24场景、**3264条完整原面板来源**、Python3.11及3.12各35共70测试，三个作业success，原数据永久[main提交1e58b4f6](https://github.com/edwardsage419/Psychohistory-Research/commit/1e58b4f67edb5155d5fab56c362b60d34d1321bb)并正式结题。这套原有报告、`R215_EXACT_RESULTS.json`、`R215_FINAL_MACHINE_ACCEPTANCE.json`以及`R215_FINAL_ACCEPTANCE_STATUS.json`仍为**R215主研究唯一权威记录**。

同时本三期研究按独立协议[12世界、768完整来源、三估计器预冻结](../../protocols/R215_DID_12_WORLDS_768_ORIGINAL_GROUP_TIME_SHOCKS_PRESCORE_FREEZE_2026-10-22.md)，提交[d6884f2](https://github.com/edwardsage419/Psychohistory-Research/commit/d6884f2a424795f759b5d517e5f051fe10ac4e69)，冻结之后才计算三期版本。运行中发现与原两期研究的共享文件名冲突，所以**不改变已冻结的来源、模型或评分规则**，仅把三期额外输出改为`R215_3P_EXACT_RESULTS.json`与`R215_3P_FINAL_MACHINE_ACCEPTANCE.json`，永久保留原`R215_EXACT_RESULTS.json`。第一次三期CI [run39741409871](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39741409871)两版本单测成功、完整输出核验成功但机器人`git push`因其他主分支提交同时推进而被拒绝，**没有覆盖原文件**。中间第二次[run39741530183](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39741530183)因工作流文件名不匹配而失败，随后修复输出命名、对机器提交先fetch/rebase再push。最终[run39741554338](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39741554338)双Python和原始资料归档job全部success，真实原数据机器人[main提交6f2a2d89](https://github.com/edwardsage419/Psychohistory-Research/commit/6f2a2d89a9d2060e25420a5679502473e64e7957)写入新的三期独立命名文件。**两套模型不能混用其源CSV、SHA、机器结题或来源数量。** 该程序修复记录与早期协议均不被删除、重写或伪装为一开始没有发生过冲突。

## 数学来源与冻结目标

参考 Abadie (2005), [Semiparametric Difference-in-Differences Estimators](https://doi.org/10.1111/0034-6527.00321), *Review of Economic Studies* 72:1–19；Bertrand, Duflo & Mullainathan (2004), [How Much Should We Trust Differences-in-Differences Estimates?](https://doi.org/10.1162/003355304772839588), *QJE* 119:249–275；Roth (2022), [Pretest with Caution](https://doi.org/10.1257/aeri.20210236), *AER: Insights* 4:305–322。本补充不复现以上作者的实际样本或估计代码、不模拟跨群体大样本，也不运行正式pre-trends功效检验或真实聚类稳健标准误。

两个**人工合成组平均值**T处理组和C对照组，各观测t=−1、0、+1三期，每组每时点一项。实际政策只在T组t=+1生效；固定真ATT=tau、无处理潜在组均值`Y0_g(t)=b_g+s_g t+q_g·1{t=1}`。另设额外观察提前效应anticip，于t=0让T组已观察均值抬升，即便尚未真正接受处理，用于审计no anticipation假设。六个group-time组层外生噪声互相独立各±1，因此每个固定结构世界有2^6=64条可能实现的完整原面板、每条原概率1/64；12个结构源世界共**768条原完整人工三期面板来源**。这些是组时段层噪声，不是组内独立研究参与者，也非768次已发生的现实政策实施试验。

每条原面板只读取实际观察组六个Y，计算：
- `STANDARD_DID = (Y_T,+1−Y_C,+1) − (Y_T,0−Y_C,0)`；
- `PRE_TREND_PLACEBO = (Y_T,0−Y_C,0) − (Y_T,−1−Y_C,−1)`，**只是一项处理前趋势诊断**，绝不以它作为真ATT估计器；
- `LINEAR_PRETREND_CORRECTED = STANDARD_DID − PRE_TREND_PLACEBO`，只有额外“前后差异趋势按线性持续、无组别post独立冲击、无anticip”成立时才有正确的均值校正。
严格由完整原来源Fraction验证`E[DID]=tau+(sT−sC)+(qT−qC)−anticip`、`E[PRE]=sT−sC+anticip`、`E[CORRECTED]=tau+(qT−qC)−2anticip`，与独立读预冻真结构直接代入公式相同。六个独立±1噪声项决定三统计量方差**4、4、12**；DID和CORRECTED的真ATT均方误差逐原来源精确等于偏差平方+噪声方差。无外部数据参与拟合。

## 12个已冻结人工世界的完整结果

|世界|真ATT|期望DID|期望PrePlacebo|期望TrendCorrected|DID真正MSE|Corrected真正MSE|
|---|---:|---:|---:|---:|---:|---:|
|PARALLEL_NULL|0|0|0|0|4|12|
|PARALLEL_TAU_TWO|2|2|0|2|4|12|
|PARALLEL_NEGATIVE|−2|−2|0|−2|4|12|
|LEVEL_GAP_ONLY|0|0|0|0|4|12|
|DIFFERENTIAL_SLOPE_FALSE|0|1|1|0|5|12|
|DIFFERENTIAL_SLOPE_TAU_TWO|2|3|1|2|5|12|
|POST_SHOCK_FALSE|0|2|0|2|8|16|
|POST_SHOCK_WITH_TAU_MINUS_ONE|−1|2|0|2|13|21|
|ANTICIPATION_TAU_TWO|2|1|1|0|5|16|
|ANTICIPATION_NULL|0|−1|1|−2|5|16|
|CONTROL_POST_SHOCK|0|−2|0|−2|8|16|
|LARGE_DIFF_SLOPE|0|3|3|0|13|12|

以上是对每世界全部64条外生组时段冲击来源的真实概率期望；不是样本实测均值或实证显著性检验。所有12真结构参数、三方法完整来源均值、真独立组时段冲击方差及每条来源实际误差见[三期额外JSON](R215_3P_EXACT_RESULTS.json)和[768条原噪声面板CSV](R215_ALL_768_ORIGINAL_GROUP_TIME_SHOCK_PANELS.csv)。

### 反例一：完整三期面板观察联合分布相同，但真实政策ATT是2、0或−1

PARALLEL_TAU_TWO真ATT=2、并满足未处理反事实平行趋势与无提前反应；POST_SHOCK_FALSE真ATT=0，但仅T组在政策后未处理潜在结果发生额外+2冲击；POST_SHOCK_WITH_TAU_MINUS_ONE的真ATT=−1，但只T组在政策后无处理潜在结果发生+3冲击。三者在本人工六组-时段位置上的**所有无噪声观察均值完全相同，独立同源的64组外生噪声下完整六维观察联合分布逐项相同**。全部观察DID、pre placebo、trend corrected统计量的分布也因此完全相同，却对应三种不等的真ATT。**仅有三期观测，无反事实平行趋势的外部识别假设时无法确认政策造成了多少因果变化**。本人工例子没有对真实个体运行变量进行操纵、没有执行实际社会政策，也不存在“观察到真未处理Y0 post”的现实权限。

### 反例二：平均处理前趋势为0，不证明政策后未处理趋势仍相同

POST_SHOCK_FALSE世界PRE_TREND_PLACEBO结构真期望恰0，且t=-1→0两组未处理潜在结果严格同趋势；但t0→t1仅T组未处理潜在结果多涨2，标准DID真期望2却真ATT0。样本随机pre placebo恰好近0甚至等于0也不足以确定未来断点无组特有其他事件。本项是一个固定离散人工反例，不声称执行了Roth (2022)真实统计功效/选择后覆盖率分析。

### 反例三：多加一段前史、趋势校正可能减偏但放大方差或遭提前效应污染

DIFFERENTIAL_SLOPE_FALSE真ATT0时，标准DID源期望1，pre placebo期望1，趋势线性修正后的源期望0；但误差方差从4增加到12，因此真实MSE从5增加到12，并未提高该固定单位噪声模型的MSE。LARGE_DIFF_SLOPE真ATT0、DID偏差3时，DID真正MSE13，修正后MSE12，才存在局部改进。ANTICIPATION_TAU_TWO世界真ATT2、提前效应anticip1使t0预期组值抬高，标准DID真实期望仅1、修正反而把t0波动重复扣除后期望变0，MSE由5扩大到16。故即使有更多处理前观察时点，不同解释目标/趋势机制会决定补充规则是否可信；不能把固定一条pre统计量当作无偏因果估计器。

## CI与原始文件形式验收

补充原生Python [r215_exact_three_period_did.py](r215_exact_three_period_did.py)以纯标准库/Fraction实现12结构、64原集团时段独立噪声、固定三估计器、完备观察分布与真因果偏差/MSE两路核查。[GitHub Actions 最终run39741554338](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39741554338)两个Python版本原生测试均success，第三原来源、源概率、全部三估计器和SHA归档job也success。两期主项目结果不被本次附加补充取代。

独立补充文件：
* [独立补充研究预冻结协议](../../protocols/R215_DID_12_WORLDS_768_ORIGINAL_GROUP_TIME_SHOCKS_PRESCORE_FREEZE_2026-10-22.md)，提交d6884f2；
* [三期全部12人工世界及64×12完整统计JSON](R215_3P_EXACT_RESULTS.json)，SHA256 `d72dd4539c1f4b329a29ef0d6f891bb3bbfd0ff385cb0eb4926b51d64ff30a14`；
* [三期768条原完整组时段外生冲击来源与真误差](R215_ALL_768_ORIGINAL_GROUP_TIME_SHOCK_PANELS.csv)，SHA256 `e4672fe25db5b3509d4c417cecc9c09e891c4ede7e3788bfe1a85319bc37efac`；
* [三期独立原SHA与来源数机器收据](R215_3P_FINAL_MACHINE_ACCEPTANCE.json)；
* [三期补充正式科学结题收据](R215_3P_FINAL_ACCEPTANCE_STATUS.json)。

**R215-3P=CLOSED_BOUNDED_E1_ARTIFICIAL_THREE_PERIOD_DID_SUPPLEMENT**，是原目录09-006的额外方法审计，**不占另一个原239目录条目**，仅人工E1，新增真人E2=0、历史E3=0，R073/PESEN v0.1继续冻结。保持实际原239目录下一项**09-007 Event Study Design（R216）**，全R完结后才统一分类，再熔炼。
