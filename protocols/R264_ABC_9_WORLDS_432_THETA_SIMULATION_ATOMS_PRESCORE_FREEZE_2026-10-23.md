# R264 近似贝叶斯计算：九人工三参数双Bernoulli观测模型、432完整先验—随机模拟源；ε/摘要损失与精确后验独立验收，计算前冻结

日期2026-10-23 Asia/Taipei，原239目录`11-024 Approximate Bayesian Computation`（P2），研究编号R264。学术原始文献 Beaumont, Zhang & Balding (2002), *Approximate Bayesian Computation in Population Genetics*, Genetics 162(4):2025–2035，https://doi.org/10.1093/genetics/162.4.2025。本R采用最简单**纯拒绝ABC**与严格算得的离散后验比较，不复制原论文基于模拟摘要的局部线性回归调整、高维人口遗传统计推断或真实族群数据。只有有限人工数学E1，真人E2=0、历史E3=0，R073/PESEN v0.1不变。

## 原完整先验/随机模拟来源、摘要与容忍度
参数Θ∈{0,1,2}离散三档，冻结均匀先验π=1/3。对给定θ，从独立公平原2bit均匀r1∈{0,1,2,3}、原2bit r2∈{0,1,2,3}得到两项人工模拟观测`Y1=1{r1<4q1θ}`、`Y2=1{r2<4q2θ}`，q1,q2均从{0,1/4,1/2,3/4,1}取。每world 3 θ×4位公平随机数16种 = **48完整原先验—模拟来源**，每条联合源设计概率1/48，九world全部**432完整原source**。每条源保留world,θ,原4随机bit,r1,r2,Y1,Y2,两个概率参数、联合源概率、固定人工目标观测`yobs=(1,0)`。这是完整模型模拟空间而非432个真人样本，真实观测没有被测得。

冻结9个θ0,θ1,θ2下(q1θ,q2θ)：
1 IID_GRADIENT: q1=(1/4,1/2,3/4),q2=(1/4,1/2,3/4)。
2 COMPLEMENTARY_GRADIENT: q1=(1/4,1/2,3/4),q2=(3/4,1/2,1/4)。
3 REVERSED_COMPLEMENT: q1=(3/4,1/2,1/4),q2=(1/4,1/2,3/4)。
4 FIRST_ONLY_INFORMATIVE: q1=(1/4,1/2,3/4),q2=(1/2,1/2,1/2)。
5 SECOND_ONLY_INFORMATIVE: q1=(1/2,1/2,1/2),q2=(1/4,1/2,3/4)。
6 NO_SIGNAL: q1=q2=(1/2,1/2,1/2)。
7 DETERMINISTIC_ENDS: q1=(0,1/2,1),q2=(1,1/2,0)。
8 NONMONOTONE_IID: q1=q2=(1/4,3/4,1/2)。
9 FIRST_WITH_SECOND_QUARTER: q1=(1/4,1/2,3/4),q2=(1/4,1/4,1/4)。

每world明确三种summary/mismatch函数与三个冻结容忍度ε∈{0,1,2}：
- FULL_HAMMING = |Y1−1|+|Y2−0|，严格ε=0接受精确(1,0)，ε=1还接受(0,0)与(1,1)，ε=2所有模拟。
- COUNT_SUM = |(Y1+Y2)−1|，ε=0接受两个数据(1,0)和(0,1)，ε≥1**所有模拟**。COUNT丢失顺序信息。
- FIRST_COMPONENT = |Y1−1|，ε=0接受Y1=1而不使用Y2，ε≥1**所有模拟**。FIRST可能在q2独立于θ时成为充分summary，但一般不是。

## 两条完全独立后验计算
**第一ABC源路线**枚举全部48先验—随机模拟原结构，对9个(距离,ε)组合分别过滤满足`d(S(Ysim),S(yobs))≤ε`的source，按每来源先验联合质量1/48规范化到θ的精确拒绝ABC后验，保存ABC总接受概率、三个θ后验、对正确完整Bayes后验的总变差`TV=(1/2)Σθ|posteriorABCθ−posteriorExactθ|`。当某世界参数候选的接受质量0则允许该θ后验0（前提整体接受率正），不将其视作软件错误。无需通过显式似然来决定ABC接受/拒绝。

**第二独立解析路线**只用冻结q1,q2和Bernoulli乘法式计算所有四种可能Y=(0,0),(0,1),(1,0),(1,1)的精确`P(Y|θ)`，不读取原4bit模拟器/源CSV。对三个距离/ε分别在这四种可能观测上**独立计算接受事件概率Pθ(d≤ε)**，再以均匀prior 1/3归一成解析ABC后验。对每world×9组合源拒绝与第二解析给出的全部posterior及整体接受概率**逐Fraction精确相同**。此外用全数据正确精确Bayes后验`π(θ|Yobs=(1,0))∝q1θ(1−q2θ)`独立校准，FULL_HAMMING ε=0严格等于完整Bayes，TV=0；FULLε2、COUNTε1/2和FIRSTε1/2所有θ都接受，后验恰回到先验(1/3,1/3,1/3)，即便真实数据对θ具有信息；不得把大容忍度的先验回归误称推断成功。

## 事前锁定非充分摘要反例
COMPLEMENTARY_GRADIENT下观察(1,0)的完整Bayes后验是`(1/14,2/7,9/14)`；REVERSED_COMPLEMENT仅调换q1,q2在每θ的观测位置，完整Bayes后验反向`(9/14,2/7,1/14)`。**两world在每个θ下的总数K=Y1+Y2完整生成分布完全相同**，因q1/q2交换不改变和的Bernoulli卷积。COUNT_SUM ε=0的ABC后验二者皆`(5/14,2/7,5/14)`，无法区分方向。这精确展示：即使ε=0，没有充足摘要的ABC也可能与完整数据精确Bayes差异很大，收窄ε无法恢复摘要已丢失的位置信息。
IID_GRADIENT下两个模拟观测交换对称，因此对观测(1,0)总数K=1是同一等价类，`COUNT_SUM ε=0`后验应与FULLε0完整Bayes严格一致（两者`(3/10,2/5,3/10)`）；但`FIRST_COMPONENT ε=0`一般不充分。FIRST_ONLY_INFORMATIVE world中q2θ为常量1/2，`FIRST_COMPONENT ε=0`则与FULLε0一致，证明一个摘要是否充分依赖**冻结的模型结构**，并非任何一项数据汇总永远充分/不充分。对NO_SIGNAL全部9个拒绝距离/ε后验都为先验，正确说明未含信息而不冒称算法失败；DETERMINISTIC_ENDS允许theta后验出现0，但总接受事件仍有正概率。

## 验收与外推阻断
第三GitHub CI读取全部432 source、每world48唯一θ×4位，质量1/48；从bit独立核对两个模拟Y与9world q；对每个world×9摘要/ε给出完全独立的四Y解析概率、拒绝ABC后验、接受率、TV和以上正/反例；SHA256原CSV/JSON机器凭证匹配。Python3.11/3.12各≥45实际测试，第三CI全部success并机器人永久main归档后，正式报告/科研验收仅`CLOSED_BOUNDED_E1_EXACT_FINITE_REJECTION_ABC_AND_SUMMARY_INFORMATION_LOSS`。不能将此称为已实现复杂不可积似然情况下的高效ABC、对连续参数真实后验校准或人口遗传学经验复现。下一原目录11-025 Sobol Global Sensitivity（拟R265/P1）。
