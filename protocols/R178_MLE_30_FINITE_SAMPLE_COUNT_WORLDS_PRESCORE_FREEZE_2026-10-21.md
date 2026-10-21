# R178 最大似然估计：30个有限样本机制世界的精确偏差、均方误差、区间覆盖与留出预测风险，计算前冻结

日期：2026-10-21。239候选模型原目录 P0 / 08-002 Maximum Likelihood Estimation。状态 PRESCORE_FROZEN_ARTIFICIAL_E1。必须在任何完整R178生成、评价或结果挑选前提交本协议。以原项目R177已经成功验收的真实源码**人工分布**为唯一测试分布来源，绝不将其误认为真人实验或真实社会数据。

## 一手统计方法来源及科学问题

* [NIST/SEMATECH Binomial Distribution](https://www.itl.nist.gov/div898/handbook/eda/section3/eda366i.htm)明确固定n、独立Bernoulli模型下最大似然估计为k/n。
* [Brown, Cai & DasGupta (2001), Interval Estimation for a Binomial Proportion](https://doi.org/10.1214/ss/1009213286)讨论常见比例区间的有限样本性质。本研究只评价一个明确指定的传统Wald区间，不能把它称为通用95%精确覆盖区间。
* [He et al. (2015)](https://doi.org/10.1080/02664763.2015.1023270)研究有限事件计数中的结构零；[NIST Beta Binomial](https://www.itl.nist.gov/div898/software/dataplot/refman2/auxillar/bbnpdf.htm)说明正相关重复行为的混合生成机制。

聚焦模型**似然函数与真实生成过程不一致**时的有限样本风险：按Bernoulli独立试验模型拟合的MLE p_hat=k/n，并不意味着真实组内行为必须独立；总体无偏也并不保证按独立性计算的方差与置信区间合理。

## 严格冻结输入与30个有限机制世界

核验 `research/R177/r177_four_finite_count_families_exact.py` Git blob **2d032513ce84141214b6b3f84df9c0ed9976a02b**，`research/R177/R177_EXACT_RESULTS.json` SHA256 **57410cf2c110ce3117b7af72e4b7473cee0c3ffd013e6fb99fd43de62165a535**。在计算前将整个R177的公式/逐次抽样程序作为实际概率支持来源，必须两路严格一致；如果来源散列变动立即fail closed。

固定n∈{4,8,12}，真实单次机会边际概率p∈{1/4,1/2}，生成机制共五类：

1. `IID_BIN`：独立Bernoulli(p)，对应R177 BIN regime0。
2. `CLUSTERED_BB_C2`：单位内BetaBinomial浓度c=2，对应R177 BB regime0。
3. `CLUSTERED_BB_C8`：单位内BetaBinomial浓度c=8，对应R177 BB regime2。
4. `INACTIVE_ZIB_Z1_8`：结构零z=1/8、活跃试验q=p/(1-z)，对应R177 ZIB regime0。
5. `INACTIVE_ZIB_Z1_4`：结构零z=1/4、活跃试验q=p/(1-z)，对应R177 ZIB regime1。

3×2×5=**30个世界**、完整计数PMF共 2×5×(5+9+13)=270个精确Fraction概率单元。每个世界随机取单个训练单位的成功数K∈{0,...,n}；单位之外从相同总体另取一次Bernoulli(p)独立的测试事件Y。该外部Y是人工机制设计中的独立新个体级试验，区别于组内条件相关训练试验；不能用作真实社会外推。

## 冻结拟合与评价

* 模型M0为错误或正确指定的IID Bernoulli似然L(q|K=k)∝q^k(1-q)^(n-k)，`q`可取[0,1]。固定MLE `q_hat=k/n`，用导数或边界理论与独立离散网格q∈{j/(4n):j=0,...,4n}证明似然最大点存在于该值；不得偷换成拟合BB或ZIB的真正完整生成似然。
* 用**实际生成PMF**对每个k精确求E[q_hat]、偏差、均方误差E[(q_hat-p)^2]、错误独立模型理论方差`p(1-p)/n`、真实误差与错误独立方差之比。这是概率完整枚举，非随机Monte Carlo估计。
* 评价固定近似双侧Wald区间`q_hat ± (49/25)*sqrt(q_hat(1-q_hat)/n)`的真实覆盖率；包含条件通过纯有理数的不等式 `(p-q_hat)^2 <= (49/25)^2 q_hat(1-q_hat)/n` 计算。Wald“名义95%”不等于真实精确95%覆盖，尤其小n和边界值时；所有30世界如实披露，不能选出有利参数宣称方法有效。
* 固定无平滑MLE用于独立新事件Y的预测。任何q_hat=0且Y=1或q_hat=1且Y=0的正概率事件，使未经平滑的**无条件预期负对数损失为正无穷**。全30世界只要P(K∈{0,n})>0且0<p<1，必须诚实标记预期logloss = `INF`，禁止人为添加clip改写MLE。
* 固定Laplace平滑替代估计`q_L=(k+1)/(n+2)`，对30世界精确计算偏差、均方误差，使用公式`∑_k P(K=k)[−p log q_L −(1−p)log(1−q_L)]`计算有限独立新事件的期望负对数损失。该logarithm为数值评分，不冒充Fraction精确值；两条独立实现（Python math.log浮点与Decimal.ln高精度）须在绝对误差1e-12范围内一致。
* 固定主要说明性对比：n=8，p=1/4，五种机制各报告MLE均方误差/相对IID方差倍数、名义Wald实际覆盖、边界MLE出现概率、Laplace期望新事件负对数损失，不按成果挑选好看的世界。

## 竞争情形与数学负对照

1. 当IID模型正确时，所有世界理论无偏，真实MLE均方误差等于p(1-p)/n；当真实训练单位内相关性为正或包含结构零，仍可保持无偏，但理论IID方差与真实均方误差不同。对所有同(n,p)严格计算。
2. 零成功或全成功的训练样本出现概率对所有30世界为正，均可令MLE未来测试logloss变成正无穷；报告实际边界概率而不隐藏。
3. MAP/贝叶斯后验不是R178目标；Laplace平滑仅是为预测对数评分设定的固定外部竞争基线，R179另行研究完整贝叶斯推断，不能当作MLE自身性能提升。
4. 每次训练数据严格是随机单组计数，不能假定组内每条观测独立便自动得到正确方差；同时每个世界已知真值p，属于人工完全信息审核，不代表真实研究可取得p。
5. 对无独立性结构来源的数据，基于单组计数无法识别群内依赖；必须使用多群重复、时间或外部结构证据，不能将人工准确公式直接当社会参数真实CI。

## 验收与归档

要求至少18种单测，Python3.11/3.12双环境执行；30×所有支持状态完整核对R177 PMF双算法、真实均值、MLE极值、MSE、覆盖、正无限新事件风险、两个Laplace对数损失实现。源码、完整机器JSON、测试程序、冻结协议、固定时间戳ZIP由GitHub Actions永久归档并核验主分支commit与完整散列。实际CI成功前不得标记结题。仅E1人工解析；E2/E3新增0，R073与PESEN v0.1保持冻结。完成全部R系列后再统一分类、最后熔炼。下一R179按原目录08-003 Bayesian Posterior Inference。
