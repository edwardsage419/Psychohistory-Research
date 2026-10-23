# R270 后验预测检验：九个六位人工Bernoulli观察世界、576完整原复现实验源及顺序敏感性；先行冻结

日期：2026-10-23 Asia/Taipei。原239目录11-030 Posterior Predictive Checks（P1），研究R270。理论文献Gelman, Meng & Stern (1996), "Posterior predictive assessment of model fitness via realized discrepancies", *Statistica Sinica* 6:733–807（主论文733–760，后接讨论），原作者论文 https://sites.stat.columbia.edu/gelman/research/published/A6n41.pdf；本文仅设自行构造的六次人工二元数据和解析贝叶斯二项式模型，未对原作者实例或代码进行复现。目标：总成功次数相同并不保证时间顺序统计量相同，后验预测检验要事前定义具体检查目标与尾部。

## 先冻结九世界、后验及原复现来源

观测长度n=6，每个world有一个明确的六位冻结观察序列：BLOCKED=`111000`（相邻相同对数T_adj=4），ALTERNATING=`101010`（T_adj=0），MIXED=`110010`（T_adj=2）；三个序列成功次数K_obs均恰好3。三种模型先验Beta(a,b)：Beta(1,1)、Beta(2,2)、Beta(1,3)，共三先验×三观察序列=9world。给定θ时全部y_t|θ独立Bernoulli(θ)。各world posterior θ|y=Beta(a+K_obs,b+6−K_obs)=Beta(a+3,b+3)。

对每world生成新的长度6的有序posterior predictive复现序列y_rep，所有2⁶=64个有序六bit复现源逐项穷尽、world合计**576条模型标识的人工原source配置**。有序复现序列K_rep=k的单条精确质量为
```text
mass(y_rep | observed) =
  rising(a+3,k) * rising(b+3,6-k) / rising(a+b+6,6)
```
其中rising(x,m)=x(x+1)...(x+m−1)，全部Fraction运算；各world全部64源总质量严格1，同一先验的三个观察序列共享相同后验与复现来源，因此总576绝不是576独立真人实验、独立拟合或独立外部验证。

两个冻结检验统计量及尾部：
* K_count(y)=∑ y_i，使用`P(K_count(y_rep)≥K_count(y_obs)|y_obs)`；同先验下三观察的K_obs都3，因此该count p_tail严格相等、无法识别观察排列顺序。
* T_adj(y)=∑_{i=1}^{5}1[y_i=y_{i+1}]，分别记录上尾`P(T_rep≥T_obs|y_obs)`、下尾`P(T_rep≤T_obs|y_obs)`和T_rep完整概率质量表。ALTERNATING的T_obs=0，上尾必1但下尾低，证明单看一个错误方向的尾部会漏掉明显顺序异常。**尾部不是经典独立样本均匀p值，也不能按传统0.05一次校正阈值当作真实世界因果结论**。

## 两条独立数学路线
A：遍历每个world全部64个完整有序复现源，根据Beta后验混合的单序列质量直接Fraction累加K_count与T_adj完整概率分布和各上下尾；CSV保存先验、观察六位、后验超参数、复现六位原source、K_rep、相邻相同对数、原精确质量。
B：不调用A的有序source枚举器，首先计算每个K_rep=k的Beta-binomial质量`C(6,k)*rising(A,k)*rising(B,6-k)/rising(A+B,6)`；再用**按游程数量r=6−T_adj的正整数分拆组合计数**N(6,k,t)，独立恢复所有T_adj的完整PMF和上/下尾。对于0<k<6，若首位1，则1游程数ceil(r/2)、0游程数floor(r/2)，相反首位0互换；相同总数k的序列计数是正整数分拆组合`C(k−1,runs_1−1)*C(6−k−1,runs_0−1)`，有效正游程才计数。k=0或6只允许单序列T=5。全64序列计数必须经组合解析式恰好复原，不允许让B调用A的列表。

## 预冻结九世界精确上尾、下尾及count结果
|先验|观察序列|T_obs|P(Trep>=Tobs)|P(Trep<=Tobs)|P(Krep>=3)|
|---|---|---:|---:|---:|---:|
|Beta(1,1)|BLOCKED|4|26/99|129/143|529/858|
|Beta(1,1)|ALTERNATING|0|1|10/429|529/858|
|Beta(1,1)|MIXED|2|28/33|175/429|529/858|
|Beta(2,2)|BLOCKED|4|71/286|131/143|89/143|
|Beta(2,2)|ALTERNATING|0|1|7/286|89/143|
|Beta(2,2)|MIXED|2|241/286|11/26|89/143|
|Beta(1,3)|BLOCKED|4|196/715|49/55|5/11|
|Beta(1,3)|ALTERNATING|0|1|16/715|5/11|
|Beta(1,3)|MIXED|2|122/143|283/715|5/11|

同一先验下复现序列概率完全相同，后验拟合时观察K=3是充分统计量；排列敏感统计T_adj观察值不同导致后验预测尾概率变化。极端ALTERNATING的下尾小于0.05是在**本有限先验和人工观测**中的模型检查信号，仅作为理论反例；不宣称序列真正来自模型且无先验选择偏差、不适合直接宣称显著发现。

## 统一验收及范围
必须先GitHub提交本冻结协议，后实现无第三方包Python源码并在Python3.11/3.12各至少45项真实单测、第三独立来源逐条CSV校验及组合计数审核、全576原source/完整PMF JSON/SHA256机器凭证永久归档后，三job全部completed/success，才发布正式E1结题。不得以“模型拟合通过”替代对未观察变量与竞争机制评估；没有真实人类E2、真实历史E3、样本外预测验证。R073及PESEN v0.1均继续冻结；优先完成原R系列之后再统一分类与熔炼。下一原目录须核对11-031。
