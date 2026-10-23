# R267 正式科学报告：三层二维离散拉丁超立方抽样与独立抽样的九世界完整复算

日期：2026-10-23（Asia/Taipei）
原模型目录：11-027 Latin Hypercube Sampling（P1）
正式科研证据：E1，有界人工有限3×3网格概率空间。新真人E2=0，新历史E3=0。

## 1. 第一来源与研究问题
McKay, M.D., Beckman, R.J., & Conover, W.J. (1979), *A Comparison of Three Methods for Selecting Values of Input Variables in the Analysis of Output From a Computer Code*, Technometrics 21(2):239–245, DOI https://doi.org/10.1080/00401706.1979.10489755 。Stein, M. (1987), *Large Sample Properties of Simulations Using Latin Hypercube Sampling*, Technometrics 29(2):143–151, DOI https://doi.org/10.1080/00401706.1987.10488205 。两文献为理论来源，R267没有逐字节复现原研究的数据与软件。本研究固定小样本量n=3、两个独立离散均匀输入各三取值，提出LHS相对IID在什么函数上精确胜出、相等或劣于IID的可反驳演示。

## 2. 先行冻结与完整人工来源
[事前冻结协议](../../protocols/R267_LATIN_HYPERCUBE_9_FINITE_GRID_WORLDS_6885_SOURCE_ATOMS_PRESCORE_FREEZE_2026-10-23.md)，提交[8943746f](https://github.com/edwardsage419/Psychohistory-Research/commit/8943746fab2b7f23256ff537007c9fc902bda386)，先于源码[7240296f](https://github.com/edwardsage419/Psychohistory-Research/commit/7240296fb36c100d3debf7a99c85c1b6765581db)。

被积变量(X,Y)独立取{0,1,2}，目标E[f(X,Y)]=九格输出平均。IID每次抽取一个均匀网格点，共三次函数评价：9³=729个原来源元组，原质量1/729。离散LHS分别独立均匀生成X/Y各一个三元排列、按位置匹配：3!²=36个原来源双排列，原质量1/36；每个边际层级使用一次，函数评价次数也为三次。原完整来源**每world共765种**，九world共**6885种**（IID6561和LHS324）。这只是完整概率空间内可能设计的人工类型数，不是6885次真实实验。

## 3. 独立精确核验
路线A穷举九世界、两设计全原source，按每条精确概率质量直接聚合三点评估平均值的完整PMF，得E、Var、bias和MSE。

路线B不使用原设计穷举器：IID以九格单次输出的概率分布自卷积三次；LHS将X排列固定为(0,1,2)，仅穷举6个等概率Y相对排列，由于原36个独立双排列对应每个相对排列恰6个来源，该方法能重建同一PMF。**全部18个完整PMF逐Fraction一致**。

第三独立方差验算以三阶离散双向ANOVA残差
```text
r_ij = f(i,j) - mean_of_row_i - mean_of_column_j + overall_mean
Var(IID three-evaluation average) = Var(f(X,Y)) / 3
Var(LHS three-evaluation average) = sum_{i,j} r_ij^2 / 18
```
独立三层排列的LHS方差公式可由排列两两无放回协方差直接推出。全部九world与来源完全枚举的方差逐有理数一致；两个设计都无偏、MSE=Var。

## 4. 九世界精确数值

|冻结函数|真均值|IID方差|LHS方差|LHS/IID|
|---|---:|---:|---:|---:|
|ADD_X|1|2/9|0|0|
|ADD_X_PLUS_Y|2|4/9|0|0|
|ADD_SQUARES|10/3|52/27|0|0|
|PRODUCT_XY|1|16/27|2/9|3/8|
|CENTERED_INTERACTION|0|4/27|2/9|3/2|
|EQUAL_INDICATOR|1/3|2/27|1/9|3/2|
|MODULAR_SUM|1|2/9|1/3|3/2|
|THRESHOLD_SUM_GE2|2/3|2/27|1/27|1/2|
|CORNER_22|1/9|8/243|2/81|3/4|

三种加性f=g(x)+h(y)的网格双向残差严格全零，固定三层完整覆盖使该离散LHS样本均值完全准确；包括加性非线性平方项。乘积、阈值及稀有角点的LHS方差分别为IID的3/8、1/2和3/4。中心化交互、相等指示与模3三种非加性函数LHS比IID**增加50%方差**，因而在本研究固定n=3和离散三层条件下，不能声称LHS总会降低所有被积函数的方差。

该小样本有限反例与Stein 1987论文所讨论的**大样本渐近**性质的适用条件不同，须保留n=3、固定网格取点、二元输入独立、相同函数评价预算等限定。

## 5. 实际机器证据
源码：[r267_exact_discrete_latin_hypercube.py](r267_exact_discrete_latin_hypercube.py)；全部原CSV：[R267_ALL_6885_ORIGINAL_GRID_SAMPLE_SOURCES.csv](R267_ALL_6885_ORIGINAL_GRID_SAMPLE_SOURCES.csv)；世界级完整PMF和解析方差：[R267_EXACT_RESULTS.json](R267_EXACT_RESULTS.json)；SHA256凭证：[R267_MACHINE_RECEIPT.json](R267_MACHINE_RECEIPT.json)。

实际[GitHub Actions run39901198271](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39901198271)三个job completed/success，Python3.11和3.12分别136项unittest通过，合计272项，第三来源审计独立逐行检查6885原source及其18完整PMF，并通过双向ANOVA方差复核；永久原来源commit：[82087648](https://github.com/edwardsage419/Psychohistory-Research/commit/82087648e4be587e156ee32846d4cc83c8cef9fd)。

原CSV的SHA256：`95008933124b100798820610eb427467fa8dc7ea104a230f22582c44bd17869a`；结果JSON的SHA256：`2c2f11fbee6360f825164c800a9c75b5c7c7d07defbaa00bdfa519a183352e1a`。

## 6. 严格科学边界
有限层级的离散LHS仅有排列而没有连续层级内随机jitter；没有实跑任何随机样本模拟；没有原论文的真实高维案例、连续输入分布、相关坐标依赖或渐近样本过程复验；没有真实人类数据，不能宣称社会心理、历史过程或大规模模型预测误差已获外部验证。新增E2=0、E3=0，R073及PESEN v0.1不变。

当前研究顺序仍是原目录逐项完成R系列；下一模型目录11-028 AIC and BIC（拟R268）。R系列全面完成后再统一归纳分类，最后熔炼新模型。
