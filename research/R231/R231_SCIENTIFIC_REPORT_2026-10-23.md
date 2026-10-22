# R231 验证性因子分析：八人工确认性测量世界、512完整外生来源与tetrad反证界限

日期：2026-10-23（Asia/Taipei）。原始239目录**10-005 Confirmatory Factor Analysis（P1）**。科学结论严格限定 `CLOSED_BOUNDED_E1_ARTIFICIAL_CFA_TETRAD_CONSTRAINTS`。全部是有限人工概率机制，不存在新真人E2、真实历史E3数据。

## 原始文献与研究范围

Jöreskog (1967 ETS Research Bulletin RB-67-48；1969 *Psychometrika* 34:183–202), [*A General Approach to Confirmatory Maximum Likelihood Factor Analysis*](https://doi.org/10.1007/BF02289343)，[ETS当年原稿介绍](https://www.ets.org/research/policy_research_reports/publications/report/1967/hpql.html)。原作者的方法背景是通过指定固定/自由载荷、误差等参数建立可测试的确认结构，完成样本模型极大似然拟合与模型拟合检验。Bollen (1989), [*Structural Equations with Latent Variables*, 第2章](https://doi.org/10.1002/9781118619179.ch2) 讨论测量模型与观察协方差。本研究只构造有限四指标人口协方差精确验算，**未计算实际人群的CFA极大似然估计、χ²、CFI/TLI/RMSEA、置信区间或抽样总体的经验适用性**。

[预先冻结协议](../../protocols/R231_CFA_8_WORLDS_512_COMPLETE_SOURCES_PRESCORE_FREEZE_2026-10-23.md)提交 [8e7924a2](https://github.com/edwardsage419/Psychohistory-Research/commit/8e7924a2f14710440c78665a7e8ce35fe508b486)，然后才提交模型、CI与机器源结果。八人工世界皆为独立等概率 `T,U,E1,E2,E3,E4` 六个Rademacher外生源，每世界64条完整概率类型，各1/64，八世界512条。观测四指标 `X_j=l_{jT}T+l_{jU}U+E_j`。完整源CSV保留隐藏T/U/E及真实观察四指标，区分观察统计和人工oracle。

## 原始概率、冻结模型限制与第二套独立核验

从64完整来源求每个世界真实均值及全部16项总体 `Σ`，使用 `Fraction` 保证所有系数精确。第二条独立解析算法只读取冻前固定载荷矩阵L，得到 `Σ=LLᵀ+I₄`，与来源结果逐格一致。另将基于四个实际观察指标的协方差用于三项事前确定的必要tetrad多项式：

- `tA=σ12σ34−σ13σ24`
- `tB=σ12σ34−σ14σ23`
- `tC=σ13σ24−σ14σ23`

假设每个潜因子载荷可以自由变化，但测量误差彼此独立并只有单一公共维度时，这三项必须为0。**零值只是必要条件而非对“唯一潜在心理特征T”的充分证明**。独立的更严格确认模板 `λ=(1,1,1,1),Var(T)=1,Var(Ej)=1` 用 `D_equal=Σ_{i≤j}|Σ_ij−(1+δij)|` 检验是否完全吻合。此D是冻结的精确人口协方差距离，不是标准CFA样本χ²拟合优度统计量。

## 八世界精确结果

| 冻结模型 | 三项tetrad `(tA,tB,tC)` | 等载荷模板D | Oracle：控制T后非零残差对数 |
|---|---|---:|---:|
| ONE_FACTOR_VALID | (0,0,0) | 0 | 0 |
| ONE_FACTOR_SIGNED | (0,0,0) | 6 | 0 |
| TWO_FACTOR_BLOCK | (1,1,0) | 4 | 1 |
| CORRELATED_RESIDUAL_METHOD | (1,1,0) | 3 | 1 |
| SECOND_FACTOR_SEMANTIC_ALIAS | (1,1,0) | 3 | 1 |
| TETRAD_FALSE_REASSURANCE | (0,0,0) | 10 | 6 |
| CROSS_LOADING_CANCEL | (−1,−1,0) | 3 | 1 |
| ONE_FACTOR_UNEQUAL_LOAD | (0,0,0) | 13 | 0 |

**确认性检验的两个层次**：只有ONE_FACTOR_VALID完全符合提前固定的等载荷及全部误差方差1模板；真正单因子但不等载荷的ONE_FACTOR_UNEQUAL_LOAD及负载荷ONE_FACTOR_SIGNED，虽然不吻合等载荷模板，三个tetrad却仍然全部等于0。固定假说的精确拒绝不能直接解释为所有可能的单因子模型都失败。

**必要条件的假安全感反例**：TETRAD_FALSE_REASSURANCE的四个指标均由两个原始潜在Rademacher信号T和U与项目噪声形成，每个指标 `X_j=T+U+E_j`。因此所有观察项目间公共协方差相等，tetrad三项恰好全0。但在给定原始T时四个项目仍共享U，六对残差协方差都为1。该全部观察数据亦能写成单一复合公共变量`W=T+U`加独立误差；说明四指标tetrad约束无法单独判定潜在构念的原始心理含义，甚至不能独立证明选择T作为唯一因子时的误差独立。注意**一个复合W因子在协方差意义上仍是合法一因子重参数化**，不能混称“全体单因子解释均已被否证”。

**共享残差的语义等价**：CORRELATED_RESIDUAL_METHOD把U解释为项目1/2相互关联的共同残差，SECOND_FACTOR_SEMANTIC_ALIAS把同一U称为第二潜变量。两者的四个观察指标在每一原外生状态下严格完全相同，其完整P(X1,X2,X3,X4)逐格相同。这是同结构数学方程的**解释标签等价**，不能声称是不同真实心理构造的经验验证。另一实际重参数化为ONE_FACTOR_UNEQUAL_LOAD把潜变量 `T'=2T`、载荷调整为 `(1/2,1,1/2,1)`，观察数值逐源不变，提醒因子单位必须锚定。

**可见证据与隐变量oracle严格隔离**： `D_equal`、全部tetrad和完整观察联合概率不读取隐藏T或U；“控制原始T后的残差协方差”是**仅可在人工拥有真潜在来源时计算的oracle真机制诊断**，现实CFA不能无条件观察这一矩，也不能用oracle结果冒充实证测量检验。

## CI、原始资料与结题凭证

[完整原生Python](r231_exact_cfa_tetrad.py) · [512条真实原结构CSV](R231_ALL_512_ORIGINAL_CFA_STRUCTURAL_ATOMS.csv) · [八世界矩和全部观察概率JSON](R231_EXACT_RESULTS.json) · [SHA256机器凭证](R231_FINAL_MACHINE_ACCEPTANCE.json)。

[GitHub Actions run39827579194](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39827579194)总体completed/success，3个作业均completed/success；Python3.11与3.12真实执行日志各 `Ran 60 tests`，`OK`，共120次成功测试执行。第三独立归档作业重审每世界64完整均匀原来源，预冻结tetrad结果，完整观察联合分布语义等价，真正oracle不同，并对完整数据与结果文件SHA校验后，机器人提交[aaab882c](https://github.com/edwardsage419/Psychohistory-Research/commit/aaab882c78b75a31af7abc4e0d1b8fdd713f9a6d)永久归档。

原来源CSV SHA256 `1bdd4af7770d6fe38450eece4eff7ef4272a6b37b40db202fe1f935373501926`；结果JSON SHA256 `a20914e56426a1d2862b492968e178b26cc4294519cefe5e7a803249f0efe469`。

本研究只证明8个人工有限模型的全部概率恒等式和反例；没有真人心理量表实测的结构拟合、有效构念内容或真实社会历史推广。新增真人E2=0，历史E3=0；R073与PESEN v0.1保持冻结。下一个真实原目录 `10-006 Structural Equation Modeling`，研究号R232，完成原R系列后再统一分类和熔炼。
