# R265 Sobol全局敏感度：九人工四独立Bernoulli输入、144完整原源、精确15子集方差分解；先行冻结

日期2026-10-23 Asia/Taipei。原239目录`11-025 Sobol Global Sensitivity`（P1），研究R265。原理论Sobol' I.M. (1993), *Sensitivity Estimates for Nonlinear Mathematical Models*, Mathematical Modeling and Computational Experiment 1(4):407–414；原始俄文1990，见https://www.andreasaltelli.eu/file/repository/sobol1993.pdf 。后续Saltelli et al (2010), *Variance based sensitivity analysis of model output. Design and estimator for the total sensitivity index*, Computer Physics Communications 181:259–270, https://doi.org/10.1016/j.cpc.2009.09.018 。本项仅研究**全部4个独立公平Bernoulli输入及九个有限离散显式函数**，精确计算ANOVA方差分量而不是采样Monte Carlo/Saltelli估计器偏差、真人数据敏感度或相关输入下的Shapley效应。真人E2/历史E3新证据0；R073和PESEN v0.1冻结；原R未完成前不开始统一熔炼。

## 全原source和输入独立性
每world有输入X=(X1,X2,X3,X4)，各为独立公平Bit，因此所有16种原输入组合穷尽、每原source设计概率1/16；九world合计**144完整原输入source**，均为人工数学结构，不是真实预测样本。逐row保存原四bit、每world精确有理输出Y=f(X)、Y²和源质量。对全部结果固定Var(Y)>0且每个输入都独立；若未来真实模型的参数分布相关，不得不经重新定义就套用本R正交Sobol拆分。

九个冻结world和精确Y：
1 ADDITIVE_WEIGHTED_123: Y=X1+2X2+3X3（X4不相关）；
2 ADDITIVE_EQUAL_FOUR: Y=X1+X2+X3+X4；
3 PURE_PAIR_PARITY: Y=X1 XOR X2；
4 PURE_TRIPLE_PARITY: Y=X1 XOR X2 XOR X3；
5 PURE_FOUR_PARITY: Y=X1 XOR X2 XOR X3 XOR X4；
6 AND_PAIR: Y=X1*X2；
7 AND_FOUR: Y=X1*X2*X3*X4；
8 SHIFT_SCALED_PAIR_PARITY: Y=7+3*(X1 XOR X2)；
9 INTERACTION_PLUS_ADDITIVE: Y=(X1 XOR X2)+X3+2X4。

## 两条完全独立精确计算验收
路线A读取全16source，对每个非空变量子集S⊆{1,2,3,4}求离散Walsh-Fourier系数`a_S=E[Y * Π_{i∈S}(2Xi−1)]`，并定义方差分量V_S=a_S²；常数a_∅=E[Y]，非空15子集V_S之和必须恰为Var(Y)。一阶Sobol`S_i=V_{ {i} }/Var(Y)`；总敏感度`S_Ti=(Σ_{S∋i} V_S)/Var(Y)`。每个输入各有1个一阶和8个包含它的高阶贡献，不得将总效应等同第一效应。
路线B**不调用路线A的Walsh系数计算器及其方差分量**，使用完整原16input函数，通过对每个输入子集S的固定取值先对补集平均`E[Y|X_S]`，得到`W_S=Var(E[Y|X_S])`，再从低维到高维用有限子集Möbius递推`V_S=W_S−Σ_{T⊊S} V_T`；对所有九world×15子集逐个Fraction一致并核对各总效应也可独立表示为`1−Var(E[Y|X_−i])/Var(Y)`。使用不同的输入边界函数实现检查源码产生正确Y，不把同一源错误逻辑复用为“独立证据”。

## 事前锁定精确目标
ADDITIVE_WEIGHTED_123：总Var(Y)=7/2，一阶`(1/14,2/7,9/14,0)`，总效应与一阶一致，全部高阶为0。ADDITIVE_EQUAL_FOUR：四个输入的一阶=总效应=1/4。
PURE_PAIR_PARITY：全部单一阶0，但二阶{1,2}Sobol=1，故ST1=ST2=1、其余0；PURE_TRIPLE_PARITY只有三阶{1,2,3}为1，PURE_FOUR_PARITY只有四阶{1,2,3,4}为1。**若仅检查四个一阶效应，后两世界所有一阶都为0，却所有涉及变量的总效应=1**，反例证明“所有一阶为0⇒模型不受这些输入影响”错误。
AND_PAIR：V总3/16，方差分量{1},{2},{1,2}分别1/16，每项Sobol=1/3，ST1=ST2=2/3，其他0。AND_FOUR：V总15/256，全部15个非空子集分量相等1/256、各Sobol=1/15，四输入一阶均1/15、总效应均8/15。
SHIFT_SCALED_PAIR_PARITY：Var=9/4，唯一非零子集仍是{1,2}且归一化Sobol=1，与PURE_PAIR_PARITY一样。该有限例说明对**正线性比例和常数平移**，方差归一化敏感度不变（数学标准定义，而不是“目标单位变化完全没有政策影响”）。
INTERACTION_PLUS_ADDITIVE：Var=3/2，两个输入交互{1,2}贡献1/6，X3一阶1/6，X4一阶2/3；一阶X1=X2=0，但它们总效应各1/6，总效应X3=1/6、X4=2/3。**不能将一阶效应视为最关键变量的唯一排序**，否则X1/X2会被错判为完全无影响。

## 统一验收
九world×完整16input source、设计质量1/16与原独立输入组合逐一核对；路线A与B全部15项方差分量相同，方差正且分量非负、分量sum=Var、全部first/total∈[0,1]、total≥first，以上预冻结具体一阶/全交互比例全中；CSV与结果JSON SHA256机读核验。GitHub Actions Python3.11/3.12各≥45真单测，加第三独立全原source审计及机器人永久main归档后才能科学有界E1结题。下一原目录将从目录核实11-026，不凭空猜其名称。
