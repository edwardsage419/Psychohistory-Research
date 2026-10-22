# R222 社会网络干扰因果模型：18固定人工世界、198完整随机分配与暴露支持性反例

日期2026-10-22。真实原239目录编号 **09-013 Causal Inference with Interference（P1）**。正式科研状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_NETWORK_INTERFERENCE**。全部人工四节点数据及数学机制E1；新增真人E2=0、历史E3=0，不存在此项针对真实社会关系与实际干预的外部证据。

## 一手方法与计算前版本

Hudgens and Halloran (2008), [Toward Causal Inference With Interference](https://doi.org/10.1198/016214508000000292), *Journal of the American Statistical Association* 103:832–842，讨论无干扰失效后与处理政策相关的直接、间接及总体效应及随机化设计。Aronow and Samii (2017), [Estimating average causal effects under general interference, with application to a social network experiment](https://doi.org/10.1214/16-AOAS1005), *Annals of Applied Statistics* 11:1912–1947，强调实验分配设计、个体暴露映射与定义明确的因果目标共同决定识别条件。此R只构造完全自建四节点网络响应面，不复现其真实社会网络试验、原作者程序、群组两阶段分配或一般网络相关标准误。

[原18世界×198真原分配的计算前冻结协议](../../protocols/R222_INTERFERENCE_18_WORLDS_198_ORIGINAL_ASSIGNMENTS_PRESCORE_FREEZE_2026-10-22.md)独立于模型源码、所有分配评分和后续结果先行提交[fa1f56fd](https://github.com/edwardsage419/Psychohistory-Research/commit/fa1f56fd475f07ee7f566539998002d2458ca15a)。三图、三机制、两政策、目标及两个独立数学验收式均事前固定。CI前修正了一条仅测试CYCLE具体可见邻居暴露的手写**夹具数值**，提交[8021c8d4](https://github.com/edwardsage419/Psychohistory-Research/commit/8021c8d41773d8b886afb1e963e3e181e277ea30)，没有修改冻结结构方程、来源生成概率或理论目标；该次修正按原顺序留痕。

## 真结构来源、处理政策与完整原样本

节点0..3，固定无向图三类：PAIRS边01和23；STAR边01、02、03；CYCLE边01、12、23、03。对任何完整人工处理向量z=(z0,z1,z2,z3)，单位i的同伴暴露`e_i(z)=Σ_{j∈neighbors(i)} z_j`，不计自身处理。真实人工结果响应`Y_i(z)=i+τ z_i+γe_i+δz_i e_i`，三个完整事前机制分别：
* **NO_SPILL**：τ=2、γ=0、δ=0，自己处理导致效果2，同伴暴露无作用。
* **LINEAR_SPILL**：τ=2、γ=2、δ=0，固定自己处理时新增一个处理邻居会增加结果2。
* **INTERACTION_SPILL**：τ=2、γ=1、δ=2，给定邻居处理人数e的真实自己处理效应为2+2e，新增一个邻居处理对自己的效果在自己不处理时1、自己处理时3。

真潜在结果取整数但使用Fraction来源概率积分；i作为稳定个体基线，只是数学索引，不代表任何真实人或心理变量。

每个三图×三机制组合下，考察两个**不同原随机化分配政策**：
* **BERNOULLI_HALF**：每个节点独立处理概率1/2，4人的全部**16个**原处理向量各概率1/16，包括全体处理和全体不处理，不事后条件剔除极端分配。
* **COMPLETE_TWO_OF_FOUR**：四人固定恰两人处理，六种组合各概率1/6。

三图×三机制×两政策共**18个设计世界**，原人工随机处理来源总量为9×16+9×6=**198条完整互斥原分配组合**。每条实际来源包含真处理向量、每单位4个e暴露数、全部4个实际Y、已固定真因果目标、真实HT统计及源概率，全部永久留存；与八个概率设计世界等权人口的意义不同，不得将198可能分配称作198次真实独立实验或198个被试。

## 事前固定目标：独立Bernoulli同伴政策下的平均自己处理因果效应

本研究无论实际来自哪种处理分配，因果目标都事先固定为**独立Bernoulli(1/2)的同伴分配政策Q**下的自己处理平均效应：

`ADE_Q=(1/4)Σ_i (1/8)Σ_{z_{−i}∈{0,1}³}[Y_i(1,z_{−i})−Y_i(0,z_{−i})]`。

这不是把一个实验的同伴政策事后改变成与本实验有利的政策，而是为了在同一真结构响应函数下**明确不同随机化政策的HT指标是否估计同一个外部固定目标**。在本真线性响应式中，给定邻居暴露e的受控直接效应为`τ+δe`，故对所有个体八种完全独立同伴处理来源积分可得目标解析闭式`ADE_Q=τ+δ×平均节点度/2`。程序用“逐个单位将自己的处理从0改为1、固定其他三人的处理”的完全潜在来源差，以及这条独立图度数学公式两路Fraction严密核验。

随机化估计量是使用**唯一实际观测**和已知每人边际处理概率1/2构造的Horvitz–Thompson形式

`HT=(1/4)Σ_i [2Zi Yi(z)−2(1−Zi)Yi(z)]`。

这在全处理或全不处理原路径上仍然可计算（区别于两组样本均值差，后者分母为0）；所有原16个Bernoulli事件因此完整保留。对全部真实原分配来源逐概率求E(HT)、Var(HT)和相对于同一外部目标ADE_Q的MSE，另以**不逐个分配求和**的条件暴露公式独立Fraction验收：

`E_HT(BERNOULLI)=τ+δ×平均度/2`；

`E_HT(COMPLETE_TWO)=τ+(δ−γ)×平均度/3`。

因后者在完全固定两人处理的设计中，给定Zi=1，其邻居被处理概率只有1/3；给定Zi=0则邻居被处理概率为2/3。因此同伴处理概率与自己的处理条件负相关，**即使Z由研究者完全随机化，仍不能忽略同伴干扰及政策变化后把HT期望机械解释为ADE_Q**。全部18世界逐Fraction的实际来源加权HT平均都与该独立解析设计公式严格一致，MSE亦与其方差加平方偏差严格相等。

## 完整18世界的核心结果

以下都是真结构人工政策Q的目标和在具体**各自随机分配政策**下HT完整期望，非任何单次实验的实际估计。PAIRS、STAR、CYCLE人工图平均度分别1、3/2、2。

|图|响应机制|固定ADE_Q真因果目标|独立Bern HT真设计期望|固定2人HT真设计期望|固定2人HT相对ADE_Q偏差|
|---|---|---:|---:|---:|---:|
|PAIRS|NO_SPILL|2|2|2|0|
|PAIRS|LINEAR_SPILL|2|2|4/3|−2/3|
|PAIRS|INTERACTION_SPILL|3|3|7/3|−2/3|
|STAR|NO_SPILL|2|2|2|0|
|STAR|LINEAR_SPILL|2|2|1|−1|
|STAR|INTERACTION_SPILL|7/2|7/2|5/2|−1|
|CYCLE|NO_SPILL|2|2|2|0|
|CYCLE|LINEAR_SPILL|2|2|2/3|−4/3|
|CYCLE|INTERACTION_SPILL|4|4|8/3|−4/3|

每个政策真HT的设计方差、相对同一ADE_Q目标的确切MSE以及每单位每一个z和暴露e组合的概率不宜省略，完整机器结果见[全部18世界JSON](R222_EXACT_RESULTS.json)及[全198条原处理来源CSV](R222_ALL_198_ORIGINAL_NETWORK_ASSIGNMENT_SOURCES.csv)。

本研究包含正面及阴性结果：**没有干扰**时两个随机化政策都正确估计目标2；在**独立Bernoulli处理**下，即使存在人工溢出或处理–暴露交互，HT的设计期望仍与这个已固定Bernoulli同伴政策ADE_Q一致；但在**固定总处理人数**设计下，真因果目标与HT设计期望发生有方向的差距。不能从本结果推断固定人数设计“不是随机化”或所有干扰模型下HT无法估计有意义的政策效应，只能明确它估计的暴露权重组合可能不同于ADE_Q。

### 暴露支持性反例：固定总人数导致某些反事实实际从未出现

预先固定暴露映射包含一个人自己的处理z和已处理邻居数量e。本项目对每世界每单位的全部理论可能`(Zi=z,e_i=e)`格逐真实分配来源积分得到其**设计出现概率**。在BERNOULLI政策下所有图的全部可行暴露格概率均>0。

但固定两人处理的STAR图中，中心节点0拥有3个邻居：
* `Z0=1`时，剩余邻居中**一定恰有1人处理**，所以中心只能观察`e0=1`，概率1/2。
* `Z0=0`时，剩余邻居中**一定恰有2人处理**，所以中心只能观察`e0=2`，概率1/2。
* 同一个中心节点在其他六个`(z,e)`潜在暴露格的真实实验概率均0，因此这六格的特定潜在结果不由这项设计的观察来源独立识别。

CYCLE每节点有2个邻居，固定两人处理导致每个节点某些极端暴露条件缺支持，全部图合计**8个无支持的个体暴露格**；PAIRS图的每节点只有一个邻居，固定两人处理在每个人所有4种理论自身处理×邻居暴露格下均有正支持，**但这并不消除HT与固定外部ADE_Q的偏差**：即使每一种局部暴露格都可能出现，设计内不同处理组的`e`权重仍然变化。可辨识性需要区分**支持存在**、**暴露映射正确**与**目标权重设计匹配**三项独立条件。

INTERACTION_SPILL的真受控邻居效应在自己z=0时1、z=1时3，是已知人工真结构Oracle；即便此次数值完整可从程序中算出，也不等于一项真实试验中单次个体反事实已经全部实测。

## 双版本运行、完整来源与永久归档

[原生标准库Fraction模型代码与43项单元测试](r222_exact_network_interference.py)实现真正所有16/6条分配、各种图的真实同伴暴露、单个原人工来源结果和HT、完整源概率归一、固定政策Q的两个完全独立真目标来源积分和图度公式，以及不依赖来源求和的条件暴露HT期望公式及所有暴露格正值性检测。

[GitHub Actions run39786040396](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39786040396) 的Python3.11/3.12两个测试job各**43项、共86项全部success**；第三job完整生成18世界、198全部原来源、每世界偏差/方差/风险与暴露格，加总与独立解析Fraction验证一致，核对结果及源文件SHA并成功永久写入main [机器人提交9d6e68da](https://github.com/edwardsage419/Psychohistory-Research/commit/9d6e68da4aeb253ca56c84d2c5d2737faa221911)。三个job的API元数据与实际作业均**completed/success**，与上一研究R221遇到的单个旧job API缓存不一致问题严格分开记录。

* [真正完整计算前冻结协议](../../protocols/R222_INTERFERENCE_18_WORLDS_198_ORIGINAL_ASSIGNMENTS_PRESCORE_FREEZE_2026-10-22.md)；
* [全部18世界及各个体暴露支持率JSON](R222_EXACT_RESULTS.json)，SHA256 `42475b0bd403914cd85c966fd7989e6b85bb2024cb32d89b66f0ccb3cac49303`；
* [全部198条原真随机化分配、同伴暴露及每人结果CSV](R222_ALL_198_ORIGINAL_NETWORK_ASSIGNMENT_SOURCES.csv)，SHA256 `4ea154698e18da2919af523de4a2f69ff7e7b5ad099e4e4f33bb82f9ace49eb5`；
* [两个原数据文件真实哈希机器验收](R222_FINAL_MACHINE_ACCEPTANCE.json)；
* [完成正式科研结题及GitHub验收机读收据](R222_FINAL_ACCEPTANCE_STATUS.json)。

**R222=CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_NETWORK_INTERFERENCE**。数学结果严格限制在三个人工四节点网络、两个分配设计与三个明示反应方程下。没有真人实验E2或真实历史E3新证据，不可用来直接预测实际社会政策对某社区或群体的溢出效应。R073/PESEN v0.1继续冻结。下一真实原239目录**09-014 Sensitivity Analysis for Confounding（P0）**，可编连续编号R223。保持先完成所有既定R、后统一分类、最后熔炼。
