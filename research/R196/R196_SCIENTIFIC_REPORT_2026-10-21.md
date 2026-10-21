# R196 变分贝叶斯：24个人工二潜变量后验世界、408个均值场候选与ELBO/KL可表达性审计

日期2026-10-21。原目录P2/08-020 Variational Bayes，最终科研状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_FINITE_VARIATIONAL_BAYES**。本研究仅限已知人工离散图模型的后验近似与数学比较，新增真人E2及独立历史E3均为0。

## 一手文献与科研边界

Jordan, Ghahramani, Jaakkola and Saul (1999), [An Introduction to Variational Methods for Graphical Models](https://doi.org/10.1023/A:1007665907178), Machine Learning37:183–233，对图模型上的变分转换、近似推断和概率界限进行系统讨论。Blei, Kucukelbir and McAuliffe (2017), [Variational Inference: A Review for Statisticians](https://doi.org/10.1080/01621459.2017.1285773), JASA112:859–877，讨论以KL散度和优化代替不可行真后验积分的实践。本研究**不**执行上述任何原始作者实测数据复现、连续参数的全局最优变分推断、自动微分或真实高维贝叶斯推断，而是可穷举的两个二值潜变量、固定人工likelihood、受限乘积Bernoulli近似与小型离散网格。

## 事前冻结的6人工生成表、两重复观察、两网格

[原计算前冻结协议](../../protocols/R196_FINITE_VB_24_WORLDS_408_CANDIDATES_PRESCORE_FREEZE_2026-10-21.md)先于源码入库，commit`95643c7eae50f51cc882e29cbb28967a9945994c`。潜在z=(z1,z2)为四类(00,01,10,11)，先验均匀1/4，人工真实条件观测事件Y=1的概率为`w_z/M`，M=max_z w_z。连续独立观察m∈{1,2}次Y=1时，真后验`P(z|m个1)=w_z^m/Σ w_k^m`，原始证据`P(Y=1)^m`应精确理解为**观测到m次独立相同正例的联合边际概率**`Σ_z w_z^m/(4M^m)`（不是单次已边际化概率简单取m次幂，因为潜在z在m次观测间保持同一真值）。为避免形式混淆，正式机器程序统一使用后一条准确联合概率。

六种严格预定人工likelihood权重为：
* UNIFORM (1,1,1,1)
* INDEPENDENT_SKEW (9,3,3,1)
* POSITIVE_COUPLED (16,1,1,16)
* NEGATIVE_COUPLED (1,16,16,1)
* ASYMMETRIC_COUPLED (16,1,1,4)
* WEAK_COUPLED (9,2,2,3)。

六源×2独立正证据数m=1/2，共12个来源配置。变分候选`q(z1,z2)=Bern(z1;p)Bern(z2;r)`，受两套固定格点限制：COARSE`p,r∈{1/4,1/2,3/4}`共9个候选；FINE`p,r∈{1/8,1/4,1/2,3/4,7/8}`共25个候选。真实模型×m×网格是**24个完整评分世界**，所有原始候选共`6×2×(9+25)=408`条。有相同真后验的来源配置仍按预定实验计数保留，不将12种来源配置误称为12套严格互异真分布。两网格严格嵌套，拟合使用70位`Decimal`的ELBO最大化，同分才按固定先p后r候选顺序选首个。不会在连续参数空间内搜索，因此“最优”严格指**有限候选网格的最优**。

## 双Fraction真后验及两套独立数值ELBO

真后验和证据从两条有理数途径逐状态核验：
1. 独立四态均匀先验乘m次Bernoulli观测likelihood后除以联合证据；
2. 将原固定人工整数权重分别取m次幂再整体归一，证据由其总和及4M^m计算。

全部来源12配置的四态后验、证据与各类边际均逐Fraction严格一致。每个均值场候选q的目标为`ELBO=Σ_z q(z)ln p(z,data)−Σ_z q(z)ln q(z)`。数学恒等式是
`ln p(data)=ELBO(q)+KL(q||p(z|data))`，
所以更高ELBO等价反向KL下降，前提必须是同一真数据/模型。为了防止浮点实现掩盖数学目标，单独运行普通`math.log`直接计算原始联合概率加entropy的ELBO，以及70位`Decimal.ln`先计算精确真后验的反向KL，再从证据log值扣除KL。每条候选另用Decimal直接联合+entropy复核恒等式，全部408评分独立数值通道误差小于1e−12。不可约变分误差由真后验与工作族结构决定，`q=p(z|data)`的无约束真后验必然有KL=0，受独立族和格点限制时通常无法达到这个全联合上界。

真正后验的两个单态边际和协方差均从四个有理数态直接计算`Cov(z1,z2)=P(11)−P(z1=1)P(z2=1)`；全部均值场候选独立构造，因此对应协方差始终0。除报告两个边际偏差外，还报告真与变分近似`P(z1=z2)`，检测关联形状被工作族抹除。另单独计算以真边际乘积构造的**前向KL最优独立族分布**，不能混入最大化ELBO的反向KL候选结果。

## 事前指定的独立真后验与网格误差负对照

UNIFORM的m1/m2均有`P(z)=1/4`，COARSE/FINE候选均能取p=r=1/2得到KL严格0。INDEPENDENT_SKEW的m1真后验为`(9/16,3/16,3/16,1/16)`，真p=r=1/4，恰处于两套网格，两个最优KL也严格0。

但同一人工独立真源在m2时真后验变为`(81/100,9/100,9/100,1/100)`，真边际p=r=1/10仍完全**独立**。由于COARSE/FINE均不包含1/10，即使结构假设正确仍留有限离散网格逼近误差：

| 完全独立真后验、m2 | 选中p=r | 最优KL(q||真后验) |
| --- | --- | ---: |
| COARSE | 1/4 | 0.184663 |
| FINE | 1/8 | 0.006487 |

这一负对照明确分离**近似族无法表达相关性**与**给定有限参数搜索网格不能包含真值**两种不同失败，禁止把全部非零变分误差归结为均值场独立假设。

## 强相关人工后验与反向KL模式偏差

POSITIVE_COUPLED(m=2)真后验为`(128/257,1/514,1/514,128/257)`，两个潜变量的真边际均为1/2，协方差`255/1028≈0.248054`，真`P(z1=z2)=256/257≈99.6109%`。

有限网格上用反向KL择优，实际结果：

| POSITIVE_COUPLED, m2 | 最优p | 最优r | 最优KL | 变分q中P(z1=z2) |
| --- | ---: | ---: | ---: | ---: |
| COARSE | 1/4 | 1/4 | 1.651817 | 5/8=62.5% |
| FINE | 1/8 | 1/8 | 1.156513 | 25/32=78.125% |
| TRUE | 1/2 | 1/2 | 0（无约束真后验） | 256/257≈99.61% |

FINE较COARSE的ELBO有所提高、反向KL从1.651817降至1.156513，但变分两个潜在边际都偏到12.5%，而真边际均50%；真后验强正相关也完全丢失，无法仅凭相同网格更高ELBO认定个体潜在概率已正确估计。NEGATIVE_COUPLED(m2)同样真边际都为1/2、真协方差`−255/1028`，其FINE选择p=1/8、r=7/8，仍有KL≈1.156513，真相等概率`1/257≈0.3891%`，均值场相等概率7/32=21.875%。在两个真多峰相关情况下，变分后验的独立假设通过选择一个高概率模式改善反向KL，却失去整个后验的不确定性与相关结构。

该例显示VI优化目标与正确不确定性定量的差距，但不推广为所有平均场变分都一定低估每一特定边际方差或在任何原始分布都选择某个固定峰。真实数据中后验不可直接观察，不能冒用人工真值比较作实证结论。

## 完整测试失败、数值订正与正式成功核验

首轮[GitHub Actions39587074398](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39587074398)发生一次重要纯数值误验：Python3.12的32项单测31项通过，剩下一项粗细网格KL嵌套断言将两项70位Decimal精确评分置于Python默认28位上下文内相加，导致粗网格值经舍入截断、错误判断嵌套性质不成立。首次全量归档没有执行。为保留研究审计先独立提交[数值校验精度订正记录](../../protocols/R196_ELBO_DECIMAL_COMPARISON_PRECISION_ERRATUM_2026-10-21.md)，commit`058d1f2bc8e070fb21af8e20378a979bd02df71c`，仅将粗细网格两个比较点放进显式80位Decimal context，不调整来源、工作族、候选及70位ELBO打分。

接着[中间CI39587234039](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39587234039)双Python32项单测均成功，全24世界408候选真实计算和SHA通过，但源程序的可复现ZIP从原冻结协议+5输出总6文件扩为协议+精度订正+5输出总7文件，工作流旧断言仍为6而失败。最后修正CI archive数量为7，不更改任何数学计算。**正式[GitHub Actions39587254747](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39587254747)三个job全部success**，Python3.11和3.12各32项单元测试共**64次通过**、完整24世界12源真值408候选以及全部7文件ZIP校验，并将所有正式数据提交main。[正式结果提交c414342f](https://github.com/edwardsage419/Psychohistory-Research/commit/c414342f1814358f987394974179d299cc80b51d)。

永久档案：
* [R196_EXACT_RESULTS.json](R196_EXACT_RESULTS.json)：24完整世界真后验/最优两个网格/潜在边际/相关性/双算法评分，SHA256`ce1132479268fafd02978992ee9c26cf84759c5109e9cd40fe25ad0867e6911e`。
* [R196_ALL_408_MEAN_FIELD_ELBO_CANDIDATES.csv](R196_ALL_408_MEAN_FIELD_ELBO_CANDIDATES.csv)：408候选四状态近似、70位ELBO/KL、真log证据、math.log数值核对、真实协方差与零近似协方差，SHA256`cb78b822f8cc7ecd5e63c6787995ca07ec68a59e8cf0419c164c5e0ccde933c0`。
* [R196_ALL_12_EXACT_POSTERIOR_SOURCES.json](R196_ALL_12_EXACT_POSTERIOR_SOURCES.json)：12配置的两独立Fraction后验/证据、解析独立性、真边际协方差及前向KL参考，SHA256`1f5fd4232bf76dde4ac74826af815daba94b38a1dc318a19c5e24c0dce2e3b18`。
* [R196_FINAL_MACHINE_ACCEPTANCE.json](R196_FINAL_MACHINE_ACCEPTANCE.json)：全部原来源、精度/KL/E1审计和三个SHA。
* [r196_finite_meanfield_variational_bayes.py](r196_finite_meanfield_variational_bayes.py)：完整人工Bayes后验、408候选ELBO、两独立数学数值路径及32项测试。
* [R196_24_Exact_Finite_Variational_Bayes_Worlds.zip](R196_24_Exact_Finite_Variational_Bayes_Worlds.zip)：包含冻结原协议、独立数值错误订正、源码、三个完整结果及机器验收的七文件可再生成ZIP。

本项严格限定**E1人工有限二元潜变量后验的均值场格点ELBO与关联信息损失**，不能替代R073真人实验预测研究，不能反推真实社会中“潜在群体类型”的存在。E2/E3新增0；R073与PESEN v0.1继续冻结。下一原目录为 **R197 P1/08-021 ARIMA（时间序列ARIMA）**，按照原全部R研究完成后统一归纳分类、最后熔炼继续。
