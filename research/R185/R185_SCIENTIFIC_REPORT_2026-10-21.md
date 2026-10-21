# R185 负二项回归：135个人工计数机制与固定离散参数的全概率比较

日期2026-10-21。原目录P1/08-009 Negative Binomial Regression。科研等级 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_NEGATIVE_BINOMIAL**，新增真人E2=0，真实历史外部预测E3=0。

## 来源及计算前协议

Cameron and Trivedi (2013), [Regression Analysis of Count Data, Second Edition](https://doi.org/10.1017/CBO9781139013567)，对Poisson、负二项、混合与零膨胀计数模型的真实统计动机进行比较。[Nelder and Wedderburn (1972)](https://doi.org/10.2307/2344614)提供GLM的历史原始依据。本研究使用自行设计的人工R177生成过程，没有复现教材原始实证数据或完整回归程序。不能从人工模型的拟合分数直接推断历史事件出现概率。

[计算前正式冻结协议](../../protocols/R185_NEGATIVE_BINOMIAL_135_WORLDS_PRESCORE_FREEZE_2026-10-21.md)以commit`1e6ddf31802c90039bb55972558ba1e7263940d4`先于评分永久入库。人工数据源完全绑定R177原始程序Git blob SHA1`2d032513ce84141214b6b3f84df9c0ed9976a02b`和源结果SHA256`57410cf2c110ce3117b7af72e4b7473cee0c3ffd013e6fb99fd43de62165a535`；正式源评分时严格复核原字节、独立封闭PMF公式和原始逐事件DP，每条来源概率一致。

每个人工世界两个独立人工计数训练单元，x=0和1分别有n=4/8/12次潜在二元事件机会，真边际成功率对为(1/8,1/4)、(1/4,1/2)、(1/4,1/4)，每个组的K来自R177固定独立二项、Beta二项浓度2/8、零膨胀二项结构零1/8或1/4之一。基础人工数据来源共3×3×5=45组；每一个来源固定三个**不会根据结果改变的负二项shape r=2、6、8**，合计135种预测比较世界、**12,375条有序训练计数对及真实人工联合概率**。

## 完整负二项PMF与双路径

负二项工作模型的预测概率`P(Y=y)=C(y+r−1,y)*(r/(r+λ))^r*(λ/(r+λ))^y`，均值λ，方差λ+λ²/r，r是固定已知整数形状。本轮以两种真正独立精确算法逐一验证：

1. 直接由组合数和两个有理数幂建立封闭PMF。
2. 从精确`P0=(r/(r+λ))^r`出发，逐级递推`P(y+1)=P(y)*(y+r)/(y+1)*λ/(r+λ)`。

在全部135世界和所有训练条件、每个真实源测试计数支持上**Fraction严格全等**。工作NB在0..n以外仍有预测概率，程序没有把这个源有限支持概率向量重新归一，因为重新归一会暗中将NB替换成截断NB。所有135世界都按真实源完整计数分布计算测试评分。

两个比较预测使用同一个事前固定、严格正的平均强度`λ=K_train+1/2`，以排除估计平均强度不同引起的混杂。一个预测为Poisson(λ)，另一个为NB(λ,r)，测试Y从另一个与训练独立、真实人工源分布产生。两种预测的期望负对数损失都以所有真实计数源概率加权，并分别使用数学库log/lgamma与60位Decimal.ln及整数阶乘两套数值路线核验；单次条件及完整加权结果差异不超过1e−12。作为边界证据，未正强化的工作NB均值MLE`λhat=K`同Poisson一样在正概率训练K=0时会赋正测试计数以0概率，故全部135世界原工作模型的独立测试期望logloss为INF，正式比较**只使用两种同一正强度预测**。

## 同均值同方差却不同零频率的预冻结反例

在n=8、p0=p1=1/4下，以下两种人工计数生成机制拥有完全一致的前两阶矩：

| 人工数据来源 | 真均值 | 真方差 | 真P(K=0) |
| --- | ---: | ---: | ---: |
| BetaBinomial浓度8 | 2 | 8/3 | 1/5 = 20.000% |
| ZeroInflatedBinomial，结构零1/4 | 2 | 8/3 | 2443/8748 ≈ 27.926% |

固定按照负二项方差等式`Var(K)=μ+μ²/r`推断仅由前两阶矩确定的描述性形状，得到相同`r_moment=μ²/(Var−μ)=6`。用同一个NB(μ=2,r=6)计算理论零事件概率，是`(6/(6+2))^6=(3/4)^6=729/4096≈17.798%`。其零频率无法同时匹配上述两种来源，**证明仅匹配平均计数与方差不足以识别结构零或单位内相关生成机制**。该反例在研究开始前事先固定，所有数据与概率通过原PMF、NB封闭与递推三套路径验收，并非根据结果挑选出的相似数据。

## 预先固定的NB与Poisson样本外评分

n=8、p0=p1=1/4的五个源机制各固定三种NB形状，因此事先要求并保存全部15种预测比较，不得只公布更好的一档。固定r=6时，预计未来真实计数的平均负对数损失如下：

| 真实生成机制 | Poisson(λ_H)测试loss | NB(λ_H,r=6)测试loss | NB减Poisson |
| --- | ---: | ---: | ---: |
| IID_BIN | 1.978333 | 1.929736 | −0.048597 |
| CLUSTERED_BB_C2 | 3.189694 | 2.762495 | −0.427199 |
| CLUSTERED_BB_C8 | 2.416161 | 2.236360 | −0.179801 |
| INACTIVE_ZIB_Z1_8 | 2.235217 | 2.124530 | −0.110688 |
| INACTIVE_ZIB_Z1_4 | 2.550167 | 2.358869 | −0.191298 |

两种预测统一使用`λ_H=K_train+1/2`。本固定5项中NB的测试负对数损失均较低，全部135项比较结果均保存在完整JSON，不能将五项结果作为真实计数或所有条件下NB普遍优于Poisson的证明。参数shape在结果计算前已经固定，并未进行任何根据测试得分的模型选择。

## 双环境测试及永久证据归档

[GitHub Actions39562923374](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39562923374) Python3.11与3.12各执行27项单测，合计**54次真实单元测试执行全部成功**；第三job单独运行全部135世界、12,375条训练计数对和两种概率预测评分、原始数据SHA与完整ZIP验收，三个job均success。正式结果原始提交为[0475e6b](https://github.com/edwardsage419/Psychohistory-Research/commit/0475e6b0db88bd1563b4a290f2874ab569fae31a)。

* [R185_EXACT_RESULTS.json](R185_EXACT_RESULTS.json)：135世界、完整固定形状比较、两源相同矩数反例及全部来源真零频率，SHA256`c75e42e3f5e211acc8f64c4ea31941072736cd34893d473400cb1262f6d96a30`。
* [R185_ALL_12375_SOURCE_WEIGHTED_TRAINING_PAIRS.csv](R185_ALL_12375_SOURCE_WEIGHTED_TRAINING_PAIRS.csv)：完整12,375条带源联合概率的训练计数数据及Poisson/NB未来独立评分，SHA256`9a0df853512a3ed70986174b47c88d06a3848ab696f38abb9be2cdfef8d78548`。
* [R185_FINAL_MACHINE_ACCEPTANCE.json](R185_FINAL_MACHINE_ACCEPTANCE.json)：原来源散列、双PMF方法、数值评分一致性及真实E2/E3=0标记。
* [r185_negative_binomial_exact.py](r185_negative_binomial_exact.py)：四套来源/概率/数值路径、全部27个数学测试及原始CSV生成。
* [R185_135_Negative_Binomial_Exact_Count_Worlds.zip](R185_135_Negative_Binomial_Exact_Count_Worlds.zip)：源码、冻结协议、完整原始数据、机器审计JSON与科研结果JSON的确定性永久档案。

科研等级正式为**E1人工精确负二项计数机制研究**。未证实真实社会事件服从Poisson或NB、未以真实样本估计负二项shape和未预测独立历史事件发生概率。新增真人E2=0、历史E3=0，R073和PESEN v0.1维持冻结。

下一研究按原候选目录核对为 **R186 P2/08-010 Zero Inflated Count Models**。继续原R系列主线，全部完成后统一归纳分类，最后熔炼。
