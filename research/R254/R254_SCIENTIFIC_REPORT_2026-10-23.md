# R254 随机矩阵与谱方法：九人工三点对称随机矩阵世界、18432完整来源与谱半径同值非识别边界

日期2026-10-23（Asia/Taipei）。原239目录`11-014 Spectral Methods`（P2），科学状态`CLOSED_BOUNDED_E1_FINITE_THREE_NODE_RANDOM_SIGNED_SPECTRAL_METHODS`。仅人工三节点随机带符号对称邻接矩阵和线性代数；所有六位边、三位独立种子及四时点全结构原source不是真人行为、历史传播或大规模随机矩阵样本。新增真实人类E2=0、历史E3=0。

## 经典来源和明确边界

Fan R. K. Chung, *Spectral Graph Theory* (1997), [AMS CBMS第92卷](https://doi.org/10.1090/cbms/092)，作为图的矩阵谱与拓扑关系的原始数学文献之一。本R刻意研究固定维度3×3的有限随机矩阵**ensemble**，不是无限大随机矩阵特征值极限分布、半圆律、真实大网络随机游走、经验文化扩散或所谓“临界传播阈值”。签名邻接矩阵含−1边时不能照搬非负不可约矩阵的Perron正模态语义；**同样的谱半径不代表相同的代数最大实特征值或带符号影响传播行为**。

[九world、18432完整原source及准确谱公式事前冻结协议](../../protocols/R254_SPECTRAL_RANDOM_TRIANGLE_9_WORLDS_18432_COMPLETE_ATOMS_PRESCORE_FREEZE_2026-10-23.md)，先于模型源码和正式评分commit [74740c27](https://github.com/edwardsage419/Psychohistory-Research/commit/74740c27108b2a203c5860824f6862a0866d69d3)。

## 完整外生矩阵与四时点线性传播原来源

每world三个无向潜在边01、02、12，各由2独立公平bit产生均匀R∈{0,1,2,3}，按冻结允许拓扑与概率p∈{0,1/4,1/2,3/4,1}阈值激活。SIGNED族仅在12边打开时取权−1，其他打开边权+1。再枚举三个独立公平初值位(S0,S1,S2)∈{0,1}³和四时点n=0…3，每world64六bit×8种seed×4时点共**2048条完整原结构来源**、每条结构权重1/2048；九world**18432个原来源点**。真实独立外生位只有每world512种组合（六边bit与三seedbit），同一初始结构的四时点是**相关的确定性重复状态**，不能称18432个独立人类个体。

人工观测矩阵`A=[[0,a,b],[a,0,c],[b,c,0]]`，状态按`x_{n+1}=Ax_n`演化。这是无上界的线性有理/整数传播数学算例，不是人体人数变化，也不保证状态非负（signed世界下尤其如此）。完整原CSV逐source保存外生六边bit、三seedbit、实际三边符号、初态、四时点状态、来源权重及精确谱指标。

## 两条相互独立的线性与谱验证路径

路线A按每条source实际边权构造3×3矩阵，逐步矩阵—向量相乘模拟四时点。路线B**不读来源生成器的前一步状态或调用递推矩阵乘法**，对每个时点n显式枚举所有三节点长n的walk索引串，直接求`(A^n v)_i=Σ_{j_1,...,j_n} A_{ij_1}A_{j_1j_2}...A_{j_{n−1}j_n}v_{j_n}`。九world×2048原source的全部三维状态在整数意义上逐位一致。第三条精确谱审计通过独立3×3行列式与迹公式核对
[
det(lambda I-A)=lambda^3-(a^2+b^2+c^2)lambda-2abc
]
并直接验证Cayley–Hamilton矩阵等式`A³=mA+2abc I`。源矩阵mask概率另由不读取原source的独立Bernoulli边乘积公式生成，全部九world完整edge组合频率逐格Fraction相同。

由于每边权只可能0/±1，非零边数m确定大部分谱；完全三角的边符号积决定其余区别：
- m=0，特征值(0,0,0)，谱半径ρ=0。
- m=1，特征值(−1,0,1)，ρ²=1。
- m=2，特征值(−√2,0,√2)，ρ²=2，最大代数实特征值√2，**保留√2符号，不误写有理数**。
- m=3、abc=+1，特征值(−1,−1,2)，ρ²=4、最大代数特征值2。
- m=3、abc=−1，特征值(−2,1,1)，ρ²=4、最大代数特征值1；最大绝对值特征值是**负**的−2，不能拿正模态增长解释其动力。

## 九个随机矩阵世界的精确期望

| 冻结结构 | E[ρ²] | 精确E[最大代数实特征值] |
|---|---:|---|
| EMPTY_P0 | 0 | 0 |
| EDGE_01_P1 | 1 | 1 |
| PATH_01_12_P1 | 2 | √2 |
| TRIANGLE_P1 | 4 | 2 |
| ER_TRIANGLE_P_QUARTER | 49/64 | 29/64+(9/64)√2 |
| ER_TRIANGLE_P_HALF | 13/8 | 5/8+(3/8)√2 |
| ER_TRIANGLE_P_THREE_QUARTER | 171/64 | 63/64+(27/64)√2 |
| SIGNED_ER_TRIANGLE_P_HALF | 13/8 | 1/2+(3/8)√2 |
| SIGNED_TRIANGLE_P1 | 4 | 1 |

对三条i.i.d. Bernoulli(p)允许边，`ρ²=m+1{m=3}`，所以`E[ρ²]=3p+p³`。每一种world从全2048源实际积分，与不使用原source的理论mask概率求和完全一致。对相同六bit/三seed/时点的p=1/2正三角与带一个负边的signed三角，所有边开闭模式和所有源上的ρ²**严格一样**，但只有三条边都打开（概率p³=1/8）时，签名三角的最大代数实特征值从2变为1。因此虽然都`E[ρ²]=13/8`，前者`Eλmax=5/8+(3/8)√2`，后者`Eλmax=1/2+(3/8)√2`，精确相差1/8。**不能把谱半径当唯一的结构相似、传播效果或实际行为因果指标**。这只是有限人工数学反例，不构成真实网络出现负边/信任传播的经验发现。

## CI、原source SHA、失败记录与科学资格

[可执行Fraction和整数矩阵/独立walk/Perron语义约束源码](r254_exact_signed_spectral.py) · [九world 18432原人工矩阵×初值×时间来源CSV](R254_ALL_18432_ORIGINAL_SIGNED_SPECTRAL_SOURCES.csv) · [全部图组合概率和精确谱期望JSON](R254_EXACT_RESULTS.json) · [完整SHA256机读收据](R254_FINAL_MACHINE_ACCEPTANCE.json)。

[初次CI run39896118162](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39896118162)两个模型Python jobs都成功，但第三独立归档审核将CSV文本数字误传为`Fraction(string,2048)`引发TypeError，故**overall failure不可算正式归档**；仅对第三审计脚本显式转换`int(string)`，既定冻结机制、原code及谱预测未改，修复commit [67e83d28](https://github.com/edwardsage419/Psychohistory-Research/commit/67e83d28827e1a0cafce79a77bf0977b337997b5)，完整失败历史保留。完成修复后[最终CI run39896198396](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39896198396)总体completed/success、3个job全部completed/success；Python3.11与3.12各`Ran 83 tests`、`OK`，合计**166次实际双版本单测通过**。第三独立审核验证九world源2048×9、各原源1/2048、唯一六bit/seed/time组合、每source谱半径平方、完整边组合联合、精确Eρ²与Eλmax中的√2系数、ρ²相同但λmax不同的 signed反例、CSV/JSON SHA，实际日志`R254_ALL_18432_ORIGINAL_RANDOM_SIGNED_MATRIX_SPECTRA_AND_WALKS_VERIFIED`及`R254_ALL_18432_SOURCE_ATOMS_PERMANENTLY_ARCHIVED`。原CSV/JSON/机器验收已由bot永久提交main [7c5cb714](https://github.com/edwardsage419/Psychohistory-Research/commit/7c5cb71403cf22308741e26720daed79f021eafb)。

原source SHA256 `bebfd725715ac5e7127525ded1f966038d36077004a2d775f84c06d20d3456cf`，结果JSON SHA256 `e56b41b3f5e40f028c227a474eaf8818af1b44f56a5ccd2ea9ec092c461297ab`。

本R科学状态仅`CLOSED_BOUNDED_E1_FINITE_THREE_NODE_RANDOM_SIGNED_SPECTRAL_METHODS`，不得称已复算大规模随机矩阵极限、真实社群扩散速度、现实社会网络信任传播或经验政策判断。新增真人E2=0、历史E3=0，R073与PESEN v0.1冻结。下一原目录11-015 Graph Laplacian（R255，P2），仍先全部R后分类与熔炼。
