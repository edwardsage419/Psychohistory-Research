# R182 线性回归：240个人工世界的Frisch Waugh Lovell残差化、遗漏变量偏差和系数方向反转

日期：2026-10-21。原239研究目录 P0/08-006 Linear Regression。科研状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_OLS**。全部240个人工模型世界、2880条原始样本均由研究者事前冻结的有理数线性方程构造；没有真实人类行为、历史社会或因果干预数据。

## 研究来源与范围

Frisch and Waugh (1933), [Partial Time Regressions as Compared with Individual Trends](https://doi.org/10.2307/1907330)，提出局部回归与多元回归系数的连接思想；Lovell (1963), [Seasonal Adjustment of Economic Time Series and Multiple Regression Analysis](https://doi.org/10.1080/01621459.1963.10480682)，进一步讨论回归式和残差化的关系；Simpson (1951), [The Interpretation of Interaction in Contingency Tables](https://doi.org/10.1111/j.2517-6161.1951.tb00088.x)，提示合并观察后的统计关系与分层解释可能不同。本研究只在自己构造的二元解释变量下证明标准最小二乘恒等式与聚合反转，未声称复现三原著的原数据、原列联表或宏观回归案例。

[事前冻结协议](../../protocols/R182_OLS_FWL_240_WORLDS_PRESCORE_FREEZE_2026-10-21.md)提交`e05a3f6d3bd21ea1ac50c8895150277396da4f8f`早于模型实际评分。全体世界固定如下。二元解释变量x,z各取0/1，四套原始联合样本计数设计分别为BALANCED(2,2,2,2)、POSITIVE(4,2,2,4)、NEGATIVE(2,4,4,2)、STRONG_POSITIVE(6,2,2,6)，顺序为(x,z)=(0,0),(0,1),(1,0),(1,1)。每格人数为正偶数。

所有人工y严格取`a+b*x+c*z+epsilon`，其中a=0或1、b=1/4或1/2、c∈{−2,−1,0,1,2}，且e∈{0,1/4,1/2}。每格内一半残差+e，一半残差−e，因此在截距、x、z三个列上均有零加总。四设计×2×2×5×3=**240个人工世界**，完整原始数据共**2880条**，所有数均为Python Fraction有理数。

## 同一数据两种拟合模型的严格双路结果

M0只拟合`y=alpha0+beta0*x+error`并遗漏z。M1拟合`y=alpha1+beta1*x+gamma1*z+error`。两者都由独立路径计算：

* 方法A直接根据原始2880条观察形成两个模型的X'X与X'y，通过有理数Gauss Jordan消元解2×2和3×3正规方程。
* 方法B在M0按x=0与1的y均值求简单斜率；在M1独立按z层剔除x、y的条件均值求partialling out后的x系数，另按x层残差化求z系数，以样本均值恢复截距。**方法B没有调用方法A的正规方程消元。**
* 全240世界，两条算法对M0与M1的每个系数逐分数完全一致。M1完整模型恰好恢复事先已指定的结构系数(a,b,c)，其残差平方和严格`N*e²`；所有残差同截距、x、z精确正交。M0残差平方和不小于M1。

直接验证遗漏变量偏差恒等式`beta0=b+c*[P(z=1|x=1)−P(z=1|x=0)]`，以及同一表达的Cov(x,z)/Var(x)系数形式。每个世界均严格一致，无浮点近似。

## 事前固定关键反例

STRONG_POSITIVE设计四格人数(6,2,2,6)，z在x=0组的频率1/4，在x=1组的频率3/4。冻结`a=0,b=1/4,c=−2,e=1/4`，共有16人工观察，真实结构x斜率为正1/4。

* 遗漏z时，简单回归`beta0=1/4−2×(3/4−1/4)=−3/4`，残差平方和**13**。
* 完整控制z后，调整回归`beta1=+1/4`、`gamma1=−2`、截距0，残差平方和**1**。
* 两次回归源于完全同一批16条数值观察，处理目标x相同；模型说明“遗漏有系统差异的变量可使聚合相关性反号”，且这个结论不依赖拟合中任何随机性。

在全部240世界中，简单回归给出负x斜率而真实预设结构x斜率仍为正的世界数恰为**54**。正反对照同时完整通过：BALANCED设计x与z恰好独立时，无论c大小均无遗漏斜率偏差；c=0时全部设计都无遗漏斜率偏差；变更人工e只影响残差平方和，不改变回归系数；人为令x=z造成设计矩阵奇异时，程序明确拒绝虚假的唯一最小二乘解。

## 正式测试、结果溯源和永久归档

[GitHub Actions39559935431](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39559935431)：双Python3.11与3.12分别执行27种独立测试，合计**54次单测全部成功**，另有第三个job全240世界的原始正规方程及FWL残差化实际复算、2880行原始数据、全部机器验收和确定性ZIP检查，三个job全部success，结果归档至main提交[9f2aabe](https://github.com/edwardsage419/Psychohistory-Research/commit/9f2aabe4207fc766427ce38397222440be57fd8a)。

永久研究文件：
* [R182_EXACT_RESULTS.json](R182_EXACT_RESULTS.json)：全部240模型真实系数、分层样本比例、两个回归的残差平方和、方向反转54组与固定正反例；SHA256 `d815885ead6771865fb6343e5ae205f5e77c8c6f341ceb57bbb7412b49b0b7eb`。
* [R182_ALL_2880_ARTIFICIAL_OBSERVATIONS.csv](R182_ALL_2880_ARTIFICIAL_OBSERVATIONS.csv)：2800余条人工来源数据记录，确数**2880行**；SHA256 `a12a98d4f6163ed14d3028e07eec50b3d29513c85b3c8def07d3cc358edb28d7`。
* [R182_FINAL_MACHINE_ACCEPTANCE.json](R182_FINAL_MACHINE_ACCEPTANCE.json)：全量接受数量、双独立算法、源哈希和科研证据等级。
* [r182_exact_ols_fwl_omitted_variable.py](r182_exact_ols_fwl_omitted_variable.py)：生成原始行及两个Fraction解算过程，包含27种数学测试。
* [R182_Exact_240_OLS_FWL_Worlds.zip](R182_Exact_240_OLS_FWL_Worlds.zip)：先冻结协议、源码、2880行原始CSV、科研JSON和验收JSON完整永久可复验档案。

## 科研分级及下一研究

研究最终验收为**E1人工线性模型代数证明**。原始设定的b是人工数据生成方程的直接系数；真实社会研究若存在共同原因、测量误差、选择偏差、未知混杂等，回归中保留一个z变量并不能自动得到因果效果。当前没有独立样本外预测评价，没有真实标准误覆盖率检验，没有真人行为或历史趋势实证。E2/E3增量均0，R073与PESEN v0.1继续冻结。

下一原239目录经实际核验为 **R183 P0/08-007 Logistic Regression（逻辑回归）**。继续按全部R模型研究完成后统一归纳分类、最后再熔炼的既定路线推进。
