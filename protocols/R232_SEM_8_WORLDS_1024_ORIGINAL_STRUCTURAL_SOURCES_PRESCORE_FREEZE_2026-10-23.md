# R232 结构方程模型：八人工结构—测量联合机制、1024完整外生来源与媒介路径非识别，评分前冻结

日期：2026-10-23（Asia/Taipei）。真实原始239研究目录**10-006 Structural Equation Modeling（P1）**，研究编号R232。连续承接R231但不覆盖其冻结模型，专门研究SEM结构路径与测量模型的联合计算、人工oracle真实干预效应、媒介路径简单OLS分解对混杂与测量误差的脆弱性、完全观察等价的潜在共同原因反例。严格E1人工；新增真人E2=0、真实历史E3=0，R073/PESEN v0.1保持冻结。

## 一手文献与边界

Kenneth A. Bollen (1989), *Structural Equations with Latent Variables*, Wiley, [第8章 The General Model, Part I: Latent Variable and Measurement Models Combined](https://doi.org/10.1002/9781118619179.ch8) 对观测—潜变量联合协方差与结构因果路径分解提供原始方法定位。Imai, Keele, Tingley (2010), [*A General Approach to Causal Mediation Analysis*](https://doi.org/10.1037/a0020761), *Psychological Methods* 15:309–334 强调把中介效应的定义、识别、估计和敏感性区别开来；本实验不是原研究的JOBS II真人数据复现，也没有识别自然间接效应在一般非线性/不可交换情形下的普遍定理。

## 固定完全有限外生源与观测

七个独立均匀Rademacher来源`U,R,E_M,E_Y,E_W,E_Z1,E_Z2∈{−1,+1}`。每世界共2⁷=**128条完整原外生来源**，每条质量1/128；八世界合计**1024条**。人工SEM结构：
- 人工处理变量`A=R`或`A=U`（指定世界），R独立U，后者由不可观察U完全决定，不能用同一U条件内的处理选择证明随机性。
- 真潜在媒介`M=m_A A + m_U U + E_M`。
- 真结局`Y=y_M M + y_A A + y_U U + E_Y`。
- **实际观察媒介指标** `W=M+w_E E_W`；两个实际观察潜在U指标 `Z1=U+E_Z1`、`Z2=U+E_Z2`。可见观测完整五元组`(A,W,Y,Z1,Z2)`，隐藏原U/R/E与真M、干预oracle仅用于人工真值计算。所有系数为固定0/1整数，全部概率与协方差Fraction精确。

## 八个事前固定机制（A来源; m_A,m_U,y_M,y_A,y_U,w_E）

1. `RANDOMIZED_MEDIATED`：R;1,0,1,0,0,0。完全外生处理，经M影响Y，真实total=1, direct=0, indirect=1。
2. `RANDOMIZED_NULL`：R;0,1,1,0,0,0。处理完全无效，真total=0。
3. `LATENT_CAUSAL_ALIAS`：U;1,0,1,0,0,0。A因U决定但do(A)真正改变M/Y，总效果1。
4. `LATENT_COMMON_ALIAS`：U;0,1,1,0,0,0。A因U决定，真正M/Y完全由U控制，do(A)总效果0。**第3和4世界所有128原源的完整实际观测(A,W,Y,Z1,Z2)逐来源完全一致**，即使有两个U代理测量Z1/Z2、一次观测到的M（w_E=0）也不可识别do(A)效果，因为U内A没有干预变化支持。
5. `RANDOMIZED_DIRECT_AND_MEDIATED`：R;1,0,1,1,0,0。真total=2、direct=1、indirect=1。
6. `RANDOMIZED_MEDIATOR_CONFOUNDED`：R;1,1,1,0,1,0。真实处理完全随机且真total=1，媒介M与结局Y共享U，观察OLS的媒介条件路径应为**3/2**、OLS`A|M`直达路径为**−1/2**；观察OLS路径间接项为3/2，非真实间接效应1。两项OLS相加为总处理效果1，但不能单独验证路径因果有效。
7. `RANDOMIZED_DIRECT_ONLY`：R;0,1,1,1,0,0。真实total=1, direct=1, indirect=0。
8. `RANDOMIZED_MEDIATOR_MEASUREMENT_ERROR`：R;1,0,1,0,0,1。W=M+E_W，真实total=1, direct=0, indirect=1；只读W的普通两预测量OLS中`β_{Y,W|A}=1/2`、`β_{Y,A|W}=1/2`，假直达效应源自媒介测量误差。无权将W当作真M。

## 冻结真因果目标与观察OLS

1. 对每个原来源固定U、R、E并用`do(A=+1)`、`do(A=−1)`重新计算真实M、Y，真实总效应为两种潜在结局差除以2（因为人工干预将A由−1改成+1，尺度差2）。真受控直接效应为固定M后变更A的Y差除以2；真中介路径为固定A后把M在两种do(A)状态间变更得到的Y差除以2；本线性无交互世界真实total=direct+indirect。第二独立路线由冻结结构系数直接算 `total=y_A+y_M m_A`、`direct=y_A`、`indirect=y_M m_A`，与所有128原来源实际人工干预逐源核验。
2. **纯观察OLS** 只读取(A,W,Y)的总体方差协方差，禁用隐藏U/M和真oracle。计算`β_total=Cov(A,Y)/Var(A)`、`β_A→W=Cov(A,W)/Var(A)`，`β_Y~W|A=[Cov(W,Y)Var(A)−Cov(A,Y)Cov(A,W)]/D`、`β_Y~A|W=[Cov(A,Y)Var(W)−Cov(W,Y)Cov(A,W)]/D`，`D=Var(A)Var(W)−Cov(A,W)²`，须真实大于0。观察OLS代理中介乘积`β_A→W β_Y~W|A`只是统计路径分解，不自动等于真干预间接效应。
3. 用独立系数向量展开(A,W,Y,Z1,Z2)对七个独立原外生来源的线性组合，解析 `Cov(X,X')=`系数内积；与完整128源观察协方差每格严格相同。全部分数运算精确，不能用已经汇总的观察Cov“复算”伪充独立路线。
4. 第3与4世界必须逐来源检验实际所有五项观察完全相同，完整`P(A,W,Y,Z1,Z2)`每格Fraction一样，且真do(A)的总、间接分别是1与0。该反例只在冻结的`A=U`不重叠机制下成立，不泛化为所有潜在代理条件的非识别性定理。
5. `RANDOMIZED_MEDIATOR_CONFOUNDED`观察总处理OLS 1但媒介路径3/2及直达路径−1/2，真因果direct=0、indirect=1。 `RANDOMIZED_MEDIATOR_MEASUREMENT_ERROR`观察媒介路径1/2、直达路径1/2，真direct=0、indirect=1；随机处理并不能替代正确媒介测量和媒介—结局可交换条件。
6. 全部源CSV保存七独立原来源、实际A/M/W/Y/Z1/Z2、反事实Mdo±1、Ydo±1、受控Y(A±1,M fixed)、总/直接/间接oracle及每原源质量1/128，完全128×8；机器结果JSON与SHA256；Python3.11及3.12各至少40单元测试及第三完整原来源归档CI门槛。只有成功核实真实运行与永久main归档后才能正式有界结题。
7. 本R仅人工线性无交互、二值外生状态的总体数学恒等式，未开展模型参数真实拟合/标准误、实际潜在社会心理构念测量、一般自然间接效应识别、跨期反事实因果推断、真人或历史资料验证。完成后从真实239目录核验后续`10-007 Measurement Invariance`（拟R233）；依所有者顺序先完成全部R，再统一分类，最后熔炼。
