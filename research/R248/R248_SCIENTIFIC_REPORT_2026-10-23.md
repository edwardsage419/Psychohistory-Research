# R248 动力系统平衡分析：九人工一维映射、405完整初值来源与非双曲吸引证明

日期：2026-10-23（Asia/Taipei）。原239目录 **11-008 Dynamical Systems Equilibria（P1）**。正式科研状态 `CLOSED_BOUNDED_E1_EXACT_RATIONAL_EQUILIBRIA_NONHYPERBOLIC_PROOFS`。所有结果仅涉及人工有理系数一维离散自治映射及有限四步算例，未引入真实心理、历史和群体动态数据E2/E3；不宣称实际历史社会存在对应稳定平衡。

## 文献和研究范围

Steven H. Strogatz, *Nonlinear Dynamics and Chaos: With Applications to Physics, Biology, Chemistry, and Engineering*, 3rd edition (2024), [Chapman & Hall/Routledge原出版社](https://www.routledge.com/Nonlinear-Dynamics-and-Chaos-With-Applications-to-Physics-Biology-Chemistry/Strogatz/p/book/9780367026509)，第10章包含一维映射的固定点与局部稳定、Logistic映射、动力系统与混沌之间的区别。本R专门研究 (x_{n+1}=f(x_n))、(f(x_*)=x_*) 和局部乘子 (lambda=f'(x_*)) 的适用边界：(|lambda|<1) 时为局部渐近吸引（若f连续可微），(|lambda|>1) 为局部排斥；(|lambda|=1) 是**线性判据不充分**，不等于已证明不稳定。本研究只在本报告明确证明的模型和邻域声称局部渐近稳定，不将有限四步数值观察误当作普遍无限时稳定论证。

[独立事前冻结九机制和有理源评分协议](../../protocols/R248_EQUILIBRIA_9_RATIONAL_MAP_WORLDS_405_IVP_TIME_SOURCES_PRESCORE_FREEZE_2026-10-23.md)，冻结提交[86c2e256](https://github.com/edwardsage419/Psychohistory-Research/commit/86c2e256ab098283d0cc56989ccbb2bc44f3aefb)，先于任何实现代码和CI。预冻结九种映射、全部初值、解析固定点、线性乘子、Logistic参数3的二次迭代证明、参数4的排斥前像以及三阶映射非双曲吸引，不对运行结果选择性改模型。

## 人工九世界与完整来源

冻结初始状态`x0∈{-1/2,-1/4,0,1/4,1/2,2/3,3/4,1,5/4}`，离散时点`n∈{0,1,2,3,4}`，每世界9初值轨道×5时间点=**45条完整人工来源点**、每条结构概率1/45，九world总**405条源点**。这些是每world九条互不相同的初值轨道在五时点的确定性采样，不能视为45个独立实验样本。每条原CSV包含冻结world、原初值、时间、状态x_n、下一映射状态f(x_n)、局部f′(x_n)、初值灵敏度`∂x_n/∂x0`和人工来源权重。

独立计算路线一逐步执行映射，并用链式法则`D_{n+1}=f'(x_n)D_n`推导初值敏感度。路线二**不读取原来源或调用原逐步映射模拟**，根据固定有理系数一元多项式构造`f^{∘n}`、Horner精确求值及多项式形式导数，核对405条状态和敏感度逐项Fraction相同。另以所有初值和`m,n≥0,m+n≤4`独立验证自治离散半群`f^{m+n}(x)=f^m(f^n(x))`。

| 冻结世界 | 方程f(x) | 所有代数固定点 | 对应固定点乘子及数学资格 |
|---|---|---|---|
| AFFINE_CONTRACT_ZERO | x/2 | 0 | 1/2，局部吸引 |
| AFFINE_CONTRACT_ONE | (x+1)/2 | 1 | 1/2，局部吸引 |
| AFFINE_ALTERNATE_CONTRACT | −x/2 | 0 | −1/2，交替方向收缩 |
| AFFINE_EXPAND_ZERO | 2x | 0 | 2，局部排斥 |
| IDENTITY_EVERY_POINT_FIXED | x | **所有实数** | 全部乘子1，各点不吸引其余邻点 |
| LOGISTIC_R2 | 2x(1−x) | 0、1/2 | 2排斥、0吸引 |
| LOGISTIC_R3_BORDER | 3x(1−x) | 0、2/3 | 3排斥、−1线性临界但可证明局部吸引 |
| LOGISTIC_R4_REPELLER | 4x(1−x) | 0、3/4 | 4与−2，两个固定点都局部排斥 |
| CUBIC_NONHYPERBOLIC_ATTRACTOR | x−x³ | 0 | 1线性临界但可证明局部吸引 |

## 非双曲案例严格数学证据

**乘子−1并不否定局部吸引。** 对LOGISTIC_R3_BORDER固定点x*=2/3，令y=x−2/3，严格有理系数展开得到
[
f(2/3+y)-2/3=-y-3y^2,qquad
f^{circ2}(2/3+y)-2/3=y-18y^3-27y^4
=y[1-y^2(18+27y)].
]
对于`0<|y|≤1/12`，有`18+27y∈[63/4,81/4]`，所以`0<y²(18+27y)≤9/64<1`。每二次迭代相对于2/3的偏差因此严格保持符号、减小绝对值并仍留在邻域。非零偏差幅度单调下降，其极限若大于0则与严格乘法因子小于1相矛盾，因此偶数项收敛到0；奇数项由连续函数f在2/3处连续也收敛到0。这一证明不仅是有限点模拟，还给出了**2/3局部渐近吸引**的足够严格条件。CI中的独立形式多项式核对系数恰`[0,1,0,-18,-27]`。

**乘子+1可以同时出现于吸引与完全中性。** 对CUBIC_NONHYPERBOLIC_ATTRACTOR，f(x)=x−x³，固定点0且f′(0)=1。在`0<|x|<1`时`|f(x)|=|x|(1−x²)<|x|`，并保持与x同符号且留在|x|<1内，逐步幅度严格下降；非零极限不可能满足其唯一固定点方程，故趋向0。这给出了另一个非双曲局部渐近吸引。IDENTITY_EVERY_POINT_FIXED也有f′=1，但f(x)=x对每个邻点永远不动、不能吸引到指定的另一个点。因此**“特征乘子等于1”本身没有固定的稳定结论**。

**排斥固定点可以有恰达前像。** LOGISTIC_R4_REPELLER的固定点3/4导数`f'(3/4)=−2`，严格局部排斥。但是原初值x0=1/4满足`f(1/4)=3/4`，以后每一步都仍是3/4。有限样本若恰落不动点或它的前像，不能据“轨道不动”就误判固定点吸引；反过来局部排斥也不意味着没有任何初值能精确到达。这是初值特例，不代表现实系统对初值的有限测量误差可以维持该精确轨道。

所有上述非双曲结论与超曲率线性判据均为明确限定数学映射上的证明；该9世界中某些Logistic负初值或大于1初值会在有限步骤逃出常用人口区间[0,1]，所以本R不宣称这些世界都是合法真实人口比例模型，或其全局吸引盆已被观察样本证明。

## CI真实执行与永久源码证据

[完整Fraction原生Python/独立多项式源码](r248_exact_rational_equilibria.py) · [全部405原初值×时点CSV](R248_ALL_405_EXACT_MAP_IVP_TIME_SOURCES.csv) · [九世界完整路径、固定点、乘子及非双曲代数证书JSON](R248_EXACT_RESULTS.json) · [机器SHA256原来源收据](R248_FINAL_MACHINE_ACCEPTANCE.json)。

[GitHub Actions run39893826278](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39893826278)实际总体completed/success、三job均completed/success；Python3.11/3.12实际日志分别`Ran 84 tests`、`OK`，合计**168次实际双版本测试通过**。第三独立完整来源审计核验每world45唯一初值时间原点、权重1/45、完整状态和局部导数、独立固定点表、LOGISTIC_R3非双曲二次多项式系数与严格上界9/64、CUBIC的内向收缩、R4排斥点的精确前像，以及原CSV/结果JSON的SHA；真实日志输出`R248_ALL_405_RATIONAL_EQUILIBRIUM_SOURCE_MAPS_AND_NONHYPERBOLIC_THEOREMS_VERIFIED`。机器人永久归档完整CSV/JSON/机器收据main，提交[10068ac1](https://github.com/edwardsage419/Psychohistory-Research/commit/10068ac15ec8a1f74b5dd9c2e7fb03db16a4af96)。

原CSV SHA256 `cb7fdcc35c212995a2c9d6f520c23d6f351d3b0c834bd6da50343884b553995b`，结果JSON SHA256 `d31b9f4e1793bd0bcca5084aca80f263ef15070405cda7d94c85730baca75900`。

研究状态为`CLOSED_BOUNDED_E1_EXACT_RATIONAL_EQUILIBRIA_NONHYPERBOLIC_PROOFS`；尚无真实历史制度状态、心理系统平衡、实际吸引盆识别或全局噪声环境预测。新增真人E2=0、真实历史E3=0；R073及PESEN v0.1仍冻结。下一原239目录`11-009 Bifurcation Theory`（R249，P1），原R全完成之后再统一分类和模型熔炼。
