# R265 Sobol全局敏感度：九人工四个独立二元输入世界、144完整来源、全部135个精确子集方差分量双路线验证

日期2026-10-23 Asia/Taipei。原239候选目录`11-025 Sobol Global Sensitivity`（P1）。科研结题状态`CLOSED_BOUNDED_E1_EXACT_FOUR_INDEPENDENT_BINARY_INPUT_SOBOL_ANOVA`。全部输入都是人工**独立均匀Bernoulli变量**，只在九个冻结函数与完整十六个配置上作精确数学计算，不是在真实心理历史模型上拟合输入分布或进行相关参数敏感性分析。新增真人E2=0、历史E3=0，R073与PESEN v0.1保持冻结。

## 一手文献、模型域和事前冻结

I. M. Sobol' (1993), [*Sensitivity Estimates for Nonlinear Mathematical Models*, Mathematical Modeling and Computational Experiment 1(4):407–414](https://www.andreasaltelli.eu/file/repository/sobol1993.pdf) 是采用正交函数/变量子集方差分解研究敏感性的重要原始文献（俄文原始版本1990）。Saltelli等(2010), [*Variance based sensitivity analysis of model output. Design and estimator for the total sensitivity index*, Computer Physics Communications 181(2):259–270](https://doi.org/10.1016/j.cpc.2009.09.018)，讨论总敏感度估计及实验设计。本项**不重新实现Monte Carlo Saltelli抽样估计器或宣称其无偏性**：因为只有四独立二元输入，16种结构全部可以在有限世界内直接积分计算。 [九world、所有子集解、144原source与数学不变量事先冻结协议](../../protocols/R265_SOBOL_9_FOUR_BINARY_INPUT_144_SOURCE_ATOMS_PRESCORE_FREEZE_2026-10-23.md)先独立提交[3236f95d](https://github.com/edwardsage419/Psychohistory-Research/commit/3236f95d7773c63f54fdfd521d060d9ef606b1ad)，代码提交在后，冻结的全部预期方差、独立路线、实际问题范围均保持未变。

九world每个独立源`(X1,X2,X3,X4)∈{0,1}⁴`，每bit独立公平，因此16个联合配置每项设计概率1/16。九world×16=**144条完整人工输入结构来源**。每条CSV显式保留四原输入、所冻结函数输出`Y=f(X)`、`Y²`及原概率质量。样本空间固定又完全枚举，不将144原配置称作独立现实试验或真实参数不确定性分布。各模型输出方差均大于0，故归一化Sobol方差分量定义良好；如果输入实际有相关性、约束或不同先验分布，一般不能直接沿用这里的独立正交方差分解。

## 完整方差分解：两套独立可审计数学路线

**第一条来源加Walsh/Fourier路线**逐world读全部16原source的有理输出和质量，对全部15个非空输入子集`S⊆{1,2,3,4}`计算正交系数
[
a_S=Eleft[Yprod_{iin S}(2X_i-1)ight].
]
由于四个输入独立且公平，非空子集Walsh乘积两两正交并与常量项正交，故各子集方差分量`V_S=a_S²`，总方差`V=∑_{S≠∅}V_S`；归一化子集Sobol指数`S_S=V_S/V`。每个输入i的一阶`S_i=S_{{i}}`，总效应`S_Ti=∑_{S∋i}S_S`。必须保留二阶、三阶、四阶的全部交互，而不是把各输入一阶相加误称总解释方差。

**独立第二条理论路线**不调用第一Walsh系数或其分量，也不沿用原source的逐项敏感性字段；从九函数对16完整输入的值，按任意子集S固定其bit取值，精确计算对其补集的条件均值`E[Y|X_S]`及方差`W_S=Var(E[Y|X_S])`，再按子集维数升序作Möbius反演：
[
V_S=W_S-sum_{Tsubsetneq S}V_T .
]
九world×15个非空子集共**135个方差分量**与第一Walsh分解逐项有理数严格相等；总V由独立直接原输出的离差平方求和验证，所有`V_S≥0`且总和恰为V。每个输入总效应再以独立式`S_Ti=1−Var(E[Y|X_{-i}])/Var(Y)`核查。全部四个输入的一阶和总效应均处于[0,1]且`S_Ti≥S_i`。因此数学验收不是只看实验直觉或单条近似曲线，而是所有子集的确切条件积分、傅里叶展开和方差闭合。

## 九个人工世界的全部一阶和总效应

下表各四元组依次对应X1、X2、X3、X4：

| 冻结world | Var(Y) | Sobol一阶 S1,S2,S3,S4 | 总效应 ST1,ST2,ST3,ST4 |
|---|---:|---|---|
| ADDITIVE_WEIGHTED_123 | 7/2 | 1/14, 2/7, 9/14, 0 | 1/14, 2/7, 9/14, 0 |
| ADDITIVE_EQUAL_FOUR | 1 | 1/4,1/4,1/4,1/4 | 1/4,1/4,1/4,1/4 |
| PURE_PAIR_PARITY | 1/4 | 0,0,0,0 | 1,1,0,0 |
| PURE_TRIPLE_PARITY | 1/4 | 0,0,0,0 | 1,1,1,0 |
| PURE_FOUR_PARITY | 1/4 | 0,0,0,0 | 1,1,1,1 |
| AND_PAIR | 3/16 | 1/3,1/3,0,0 | 2/3,2/3,0,0 |
| AND_FOUR | 15/256 | 1/15,1/15,1/15,1/15 | 8/15,8/15,8/15,8/15 |
| SHIFT_SCALED_PAIR_PARITY | 9/4 | 0,0,0,0 | 1,1,0,0 |
| INTERACTION_PLUS_ADDITIVE | 3/2 | 0,0,1/6,2/3 | 1/6,1/6,1/6,2/3 |

**完全纯交互时，一阶零不代表该输入不重要。** `PURE_FOUR_PARITY`把输出定义为X1 XOR X2 XOR X3 XOR X4。对于任意固定一个Xi，其他三个独立公平bit的异或仍然公平，因此`E[Y|Xi]`是常数1/2，四个一阶指数全部**0**。但一旦固定其他三个bit，Xi的改变总会使Y翻转，全部方差恰由四阶子集{1,2,3,4}贡献，**四个总敏感度均1**。同理`PURE_PAIR_PARITY`仅二阶{1,2}分量指数1，一阶四项全0，总效应X1=X2=1；`PURE_TRIPLE_PARITY`只三阶{1,2,3}分量1。这是事前定义、全16source枚举可独立重复验证的数学反例，足以阻断“第一阶为零→参数完全无关”的错误推断，但并不表示现实社会机制均由高阶交互主导。

**乘法门拆分单独影响和交互。** `AND_PAIR`令Y=X1X2，真实V=3/16，三个非零方差分量恰为`V_{1}=V_{2}=V_{12}=1/16`，归一化各1/3，因而X1、X2一阶各1/3、总效应各2/3。四个输入全AND门`AND_FOUR`只有16个输入之一输出1，`P(Y=1)=1/16`，`Var(Y)=15/256`；在独立fair输入下全部15个非空Walsh子集系数平方同为1/256，故每个子集的归一化指数1/15。各Xi只占其单独分量1/15，但它出现在总共8个非空子集，故总效应8/15；一阶和仅4/15，即使总效应很大，仍有许多解释方差来自高阶交互。不能用四个一阶和小于1就把剩余份额自动标成“未建模随机误差”，此处剩余全部是已完全枚举的明确交互。

**输出单位的仿射放缩不同于改变因果输入分布。** `SHIFT_SCALED_PAIR_PARITY`令Y=7+3(X1 XOR X2)。与仅XOR的`PURE_PAIR_PARITY`相比，方差从1/4变为9/4，但每个非空分量同乘9，归一化后仍唯一{1,2}占1，一阶均0、ST1=ST2=1。Sobol在正线性放大加常数时归一化指数不变，仅说明同一参数分布下统计**相对方差贡献**不变；不代表社会政策目标单位/损失幅度不重要。INTERACTION_PLUS_ADDITIVE模型`Y=(X1 XOR X2)+X3+2X4`方差3/2，{1,2}交互占1/6，X3一阶1/6，X4一阶2/3；X1/X2一阶均0但总效应各1/6。

## 双Python真实CI、原来源SHA、科学边界

[原生Fraction原source/Walsh与独立条件Möbius计算程序](r265_exact_fourbit_sobol.py) · [九world144完整输入source CSV](R265_ALL_144_ORIGINAL_FOURBIT_SOBOL_INPUT_SOURCES.csv) · [九world全部15方差分量、一阶/总效应及验证JSON](R265_EXACT_RESULTS.json) · [SHA256机读收据](R265_FINAL_MACHINE_ACCEPTANCE.json)。

[GitHub Actions run39900027884](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39900027884)总体completed/success，三个job全部success。Python3.11与3.12实际日志各`Ran 82 tests`、`OK`，**164次真实双版本单测通过**。第三独立source audit从144CSV完整读取每world16个原四位组合、每source1/16、Y及Y²、全部原输出严格方差；再次自行按每子集固定其bit求条件均值/方差及Möbius反演，135个分量逐Fraction与程序结果一致，并核对9world预冻结所有一阶和总效应比例、纯四阶交互和四位AND门、不等式、原CSV/结果JSON SHA。实际日志`R265_ALL_144_ORIGINAL_SOBOL_INPUTS_AND_135_EXACT_ANOVA_SUBSETS_VERIFIED`与`R265_ALL_144_ORIGINAL_SOBOL_SOURCES_ARCHIVED`。全部原CSV、结果JSON和独立SHA机器完整性凭证永久由GitHub bot提交main [ad9bd248](https://github.com/edwardsage419/Psychohistory-Research/commit/ad9bd248106dfefdb353ae449bb381dd5429df87)。

原CSV SHA256 `136ddd4dfa99c59b2b6d166ed01a52b044ae4d5f72dd96debcbede9f7e394a0f`，结果JSON SHA256 `427f388c59c8c8e85e4771d3c93099a047e3ff6312f1599c6cbdbc18054a8e70`。

本R只能认定为`CLOSED_BOUNDED_E1_EXACT_FOUR_INDEPENDENT_BINARY_INPUT_SOBOL_ANOVA`；没有复现真实输入分布参数独立性、Saltelli有限采样估计误差、历史社会敏感性因果解释、真实模型的参数交互关系或校准数据。新增真人E2/真实历史E3均0，R073/PESEN v0.1保持冻结。下一目录已核实`11-026 Monte Carlo Simulation`（P0，拟R266），之后`11-027 Latin Hypercube Sampling`（P1），按原R全部完成后才归纳分类与熔炼。
