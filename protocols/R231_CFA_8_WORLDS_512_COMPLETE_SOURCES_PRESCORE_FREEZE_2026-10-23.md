# R231 验证性因子分析：八种四指标因子生成世界、512外生原来源与四项协方差确认约束，计算前冻结

日期：2026-10-23（Asia/Taipei）。实际239模型目录 `10-005 Confirmatory Factor Analysis` P1，研究编号 `R231`。承接R230探索性因子分析，但本R完全独立研究**固定预设确认结构、协方差矩阵隐含限制、tetrad必要条件、模型错误拟合假阳性及不可识别的共同残差机制**。数学人工E1，真人E2新增0，历史E3新增0；R073/PESEN v0.1不变。

## 一手方法背景与合法证据边界

* Karl G. Jöreskog (1967 ETS Report RB-67-48; 1969 `Psychometrika` 34:183–202), *A General Approach to Confirmatory Maximum Likelihood Factor Analysis*. 一手出版社 DOI https://doi.org/10.1007/BF02289343，原1967 ETS公开稿 https://www.ets.org/research/policy_research_reports/publications/report/1967/hpql.html。其原始研究以模型参数的预先固定/释放定义确认性假设，讨论极大似然与整体拟合；本R不模拟原作者样本极大似然、χ²自由度计算、渐近拟合置信区间或其人群实验。
* Kenneth A. Bollen (1989), *Structural Equations with Latent Variables*, Chapter 2, DOI https://doi.org/10.1002/9781118619179.ch2。区分潜在测量方程、结构方程及观测协方差。只作为原方法定位，当前有限构造无需宣称阅读全文推导。

## 事前冻结的八世界和全部独立原来源

独立等概率六个离散外生源 `T,U,E1,E2,E3,E4∈{−1,+1}`。每个世界2⁶=**64条**完整概率原来源，统一每行1/64；八世界合计**512条**。四个可观测数值项目 `X_j=l_{jT} T + l_{jU} U + E_j`，所有系数固定为整数且误差E彼此及T/U独立。原来源保留隐T/U/误差与真实可见X、1/64来源权重。全部协方差由来源Fraction和第二条固定载荷系数计算双路径核对。

八个生成世界的前两列是四行 `(l_T,l_U)`；每题误差系数均为1：

1. `ONE_FACTOR_VALID`: (1,0),(1,0),(1,0),(1,0)。
2. `ONE_FACTOR_SIGNED`: (1,0),(1,0),(−1,0),(1,0)；允许负载荷，单因子仍应合规。
3. `TWO_FACTOR_BLOCK`: (1,0),(1,0),(0,1),(0,1)；局部单因子共同协方差tetrad违例。
4. `CORRELATED_RESIDUAL_METHOD`: (1,1),(1,1),(1,0),(1,0)；U被指定为条件T下共同方法残差。
5. `SECOND_FACTOR_SEMANTIC_ALIAS`: 数学全部四行及完整观测与4一致，但U被标为第二个原潜在因素；**仅语义标签不同**，不冒称两个不同结构方程经验上不可识别的更强证明。
6. `TETRAD_FALSE_REASSURANCE`: (1,1),(1,1),(1,1),(1,1)；虽然条件T所有题目共享额外U残差，公共部分有效秩只有1，所有tetrad为0；证明一个必要条件零值**不足以确认单一原始T与局部独立测量误差**。
7. `CROSS_LOADING_CANCEL`: (1,0),(1,0),(1,1),(1,−1)；两个跨载荷正负抵消指定项目协方差，但仍产生tetrad非零。
8. `ONE_FACTOR_UNEQUAL_LOAD`: (1,0),(2,0),(1,0),(2,0)；真实单因子、不相等载荷，同一tetrad零，但**严格等载荷单因子**预先模板失配。

## 固定统计目标与可接受结论

A. 对四指标真实总体`Σ`计算Fraction精确均值、4×4协方差和完整观察四元组`P(X1,X2,X3,X4)`。独立理论式 `Σ=LLᵀ+I₄`必须每个格一致。人工源完全均匀、无任何真人抽样误差。

B. 在 **先验固定假说** `H_equal: λ=(1,1,1,1), φ=1, ψ=(1,1,1,1)` 下给出预先冻结的**非标准假说差异分数** `D_equal=Σ_{i≤j}|Σ_ij−(λ_iλ_j+δ_ij)|`。精确0仅表示本预定义矩约束被吻合，非推断检验p值、未执行最大似然模型拟合。ONE_FACTOR_VALID必须D=0；ONE_FACTOR_UNEQUAL_LOAD有D>0，但其一般单因子tetrad为0。此二关口必须明确区分。

C. 事前冻结三tetrad有符号方程：
`t_A=σ12σ34−σ13σ24`, `t_B=σ12σ34−σ14σ23`, `t_C=σ13σ24−σ14σ23`。
对真正单因子、题项特异误差互相独立的测量世界，均为0（包括负载荷及不等载荷）。TWO_FACTOR_BLOCK、CORRELATED_RESIDUAL_METHOD、SECOND_FACTOR_SEMANTIC_ALIAS与CROSS_LOADING_CANCEL必须至少一个非0。TETRAD_FALSE_REASSURANCE三项均0但在给定指定T时`Cov(X_i−l_{iT}T,X_j−l_{jT}T)≠0`，说明该必要条件无法独立检验原始局部独立假设。

D. Oracle中计算`Cov(X_i−l_{iT}T,X_j−l_{jT}T)=l_{iU}l_{jU}+δ_ij`的非对角矩，并从完整来源直接计算；独立载荷计算并核对。**T和U是真正人工内置变量**，在真实问卷中不能被CFA观测估计器查看，不得将Oracle违例当成可见统计证据。

E. 完整观察分布别名：世界4与5按每个来源观察X完全相同，保留两种语义解释；世界6可写成等价单一复合 `W=T+U`，四题`X_j=W+E_j`，观察分布源点级别一致，但W是{−2,0,2}并不是原T，说明tetrad=0不识别“单一原始二元心理特质”的含义。额外对ONE_FACTOR_UNEQUAL_LOAD以 `T'=2T`, `λ'=(1/2,1,1/2,1)`证明完全相同四项X，潜因子尺度需外部锚定。

F. 每世界64原来源总权重严格1；完整记录全部512行；双Python3.11/3.12各至少40项单测、第三GitHub Actions作业独立校验概率、tetrad、Oracle假设、两个源点级别别名、SHA256、永久归档main。研究报告与正式有界验收只在真实CI成功并完整原来源文件已存在后发布；保留所有失败/纠错记录。理论式必须与枚举路线独立。

G. 不应泛化为真实心理构念确认、χ²拟合优度、模型选择显著性、因果结构定向或样本外复现。本R完成后原目录下一条 `10-006 Structural Equation Modeling`，连续号拟 `R232`；此项须在完成R231后重新从目录核对。全R完成后统一分类，最终熔炼。
