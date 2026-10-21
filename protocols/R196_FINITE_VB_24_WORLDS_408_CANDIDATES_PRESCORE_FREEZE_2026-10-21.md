# R196 变分贝叶斯：24个人工二潜变量后验世界、408固定均值场候选、ELBO与反向KL精确审计，计算前冻结

日期2026-10-21。原239目录P2/08-020 Variational Bayes。状态 PRESCORE_FROZEN_E1_ARTIFICIAL_FINITE_MEAN_FIELD_VI。

## 文献及适用范围

Jordan, Ghahramani, Jaakkola and Saul (1999), *An Introduction to Variational Methods for Graphical Models*, Machine Learning37:183–233, https://doi.org/10.1023/A:1007665907178，说明对概率图的简化变分推断和概率界限。Blei, Kucukelbir and McAuliffe (2017), *Variational Inference: A Review for Statisticians*, JASA112:859–877, https://doi.org/10.1080/01621459.2017.1285773，阐述变分近似与目标后验、反向KL和应用边界。本次只构建可穷举的**两个二元潜变量、乘积均值场近似与固定有限候选网格**，不复现上述来源的真实研究数据、任何神经网络近似、coordinate ascent无限精度优化或高维大规模VB。

## 六个人工目标和24完整受控世界

人工隐藏状态z=(z1,z2)∈{00,01,10,11}，先验P(z)=1/4。条件观测事件Y=1概率为`P(Y=1|z)=w_z/M`，M=max_z w_z，所有权重为严格正整数。条件已观测到m∈{1,2}次独立Y=1的后验真概率`P(z|m个1)=w_z^m/Σ_k w_k^m`；真实证据`P(m个1)=(Σ_z w_z^m)/(4 M^m)`，均是Fraction有理数。

六种固定权重按状态(00,01,10,11)顺序分别：
1. UNIFORM: (1,1,1,1)；
2. INDEPENDENT_SKEW: (9,3,3,1)，m1时真P(z1=1)=P(z2=1)=1/4；
3. POSITIVE_COUPLED: (16,1,1,16)，对角两峰；
4. NEGATIVE_COUPLED: (1,16,16,1)，反对角两峰；
5. ASYMMETRIC_COUPLED: (16,1,1,4)；
6. WEAK_COUPLED: (9,2,2,3)。

变分工作族强制`q(z1,z2)=Bern(z1;p)Bern(z2;r)`，q00=(1−p)(1−r), q01=(1−p)r, q10=p(1−r), q11=pr。预先选择两个嵌套搜索网格：
* COARSE: p,r∈{1/4,1/2,3/4}，9套候选；
* FINE: p,r∈{1/8,1/4,1/2,3/4,7/8}，25套候选。

六目标×2种m×2类网格=**24个完整评分世界**，每一个目标+m的真实后验只有12种*来源配置*（UNIFORM的两种m可以相同，绝不将配置数误报为12个互异分布）。每个实际候选都按固定网格先p后r顺序评分，总共`6×2×(9+25)=408`条完整变分候选测评。COARSE候选是FINE的真子集。任何结果不允许改变网格、来源权重或未来证明方式。最佳候选按**70位Decimal得到的ELBO最大值**选择，只有真实完全相等时按固定先p再r的字典顺序选择，最大值比较不使用事后人工设定容差挑选有利模式。

## 全证据、真实后验、均值场ELBO及独立双数值实现

两套Fraction真后验算法：A先验(1/4)乘m次显式`w_z/M`似然得到unnormalized joint、归一后计算证据；B直接使用四个`w_z^m`归一化，另从求和计算证据。四类每态分数与证据逐项精确一致。

候选变分目标`ELBO(q)=Σ_z q(z)log(P(z,Y=1^m))−Σ_z q(z)log q(z)`，真证据`log P(Y=1^m)`与候选反向KL`KL(q||P(z|data))`满足`log evidence = ELBO + KL`。对全部408候选：
* 方案A独立使用常规浮点`math.log`直接评估ELBO所含的完整joint、entropy；
* 方案B使用70位`Decimal.ln`先计算完整真后验和反向KL，再用70位证据对数减KL得到ELBO；
* 两个ELBO、KL与数值log-evidence恒等式必须在绝对1e−12内同值；KL不允许为超容差的负数。
* 已知完整无约束的精确真后验可取q=P，因此完整自由家族KL=0、ELBO=log证据；有均值场限制及固定网格时通常不能达到该上界。

记录每个真后验的z1、z2边际成功率与严格Fraction协方差`Cov(z1,z2)=P(z=11)−P(z1=1)P(z2=1)`。任一均值场近似协方差严格为0，故即使ELBO很好，也不能复制非零联合依赖。记录所选q的两个边际均值偏差、完整近似四状态分布、posterior/近似对角一致概率，全部Fraction，不将这些潜在指标视为真人精神状态。

## 特别固定三个机制对照

1. **精确可表示后验**：UNIFORM在m1、m2下的真后验全为1/4，两个网格都有p=r=1/2，反向KL和ELBO gap精确0。INDEPENDENT_SKEW m1的真后验由p=r=1/4独立表示，两个网格都可以实现KL=0；但m2时真边际由独立变为p=r=1/10，两个网格都不含1/10，故即使真后验独立、最优固定网格仍有正KL。不得把全部非零KL归咎于潜在依赖。
2. **多峰变分模式选择风险**：POSITIVE_COUPLED与NEGATIVE_COUPLED在m1或m2都具有非零真潜在协方差，乘积族无论选择何p,r都不可能恢复真实相关结构。反向KL是从工作q对真后验的覆盖代价，它的有限网格最优值可能偏向单个后验峰，导致一个或两个潜在边际与真值1/2不一致。记录实际选择及误差，不先假定一定选择哪个对称模式。
3. **ELBO改善不保证真实联合后验可恢复**：FINE包含COARSE，故对每个12来源配置必须满足`best_ELBO_fine ≥ best_ELBO_coarse`，相当于反向KL_fine ≤ coarse。但高度依赖的后验可能仍有正的KL与显著非零真实协方差，不能从单独较高ELBO推断潜在关联已被识别。还需分别记录`P(z1=z2)`与q的对应值。

可补充报告“前向KL最佳独立族”为真边际乘积`q_forward(z)=P(z1)P(z2)`，但此对照通常不在上述有限候选网格内。**前向KL优化方向与本轮ELBO反向KL目标不同，不能将其性能混淆，也不得把解析边际乘积当作变分网格实际找到的最优候选。**

## 验收及长期归档

双Python3.11/3.12各≥25项测试，完整12来源配置/24评分世界/408个候选、双Fraction真后验/证据计算、双float与Decimal ELBO及KL恒等式、所有候选q和为1、固定网格包含关系、UNIFORM/INDEPENDENT_SKEW正对照、相关真后验非可表示性、边际乘积前向KL辨析、非法输入失败和固定压缩包哈希。正式输出408候选完整CSV、24世界选定拟合及双数值评分JSON、12真后验及其相关/真证据库JSON、完整源码、科研报告、机器验收及冻结协议的固定时间戳ZIP。三个CI job success及实际结果永久入库main后才允许`CLOSED_BOUNDED_E1_ARTIFICIAL_FINITE_VARIATIONAL_BAYES`。

科研只限人工有限格点近似的E1数学反例，新增真人E2=0，历史E3=0；R073/PESEN v0.1冻结。下一R197应对应原目录08-021 ARIMA，需进入前再核对。仍坚持先全部R学习研究、后统一归纳分类、最后熔炼。
