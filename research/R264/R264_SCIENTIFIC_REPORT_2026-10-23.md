# R264 近似贝叶斯计算：九人工有限拒绝ABC、432完整先验模拟来源与81组解析后验复核

日期2026-10-23 Asia/Taipei；原目录`11-024 Approximate Bayesian Computation`（P2）。有界科学结题状态`CLOSED_BOUNDED_E1_EXACT_FINITE_REJECTION_ABC_AND_SUMMARY_INFORMATION_LOSS`。没有使用人口遗传学真人数据、真实参数后验、连续参数复杂模拟器，也没有实现原作者的局部线性ABC校正。全部原source只对应人工完整概率枚举E1；新增真人E2=0、历史E3=0，R073/PESEN v0.1仍冻结。

## 一手来源及冻结合同

Mark A. Beaumont, Wenyang Zhang, David J. Balding (2002), [*Approximate Bayesian Computation in Population Genetics*, Genetics 162(4):2025–2035](https://doi.org/10.1093/genetics/162.4.2025)，用模拟统计摘要和局部线性回归接近参数后验。本R研究受其模拟后验思想启发的**基本拒绝ABC**，只是一个受限的检验基准，不能以本项结果宣称复现其回归校正效率、群体遗传模拟与真实经验发现。[九模型、432完整原source、九种ABC摘要/ε组合和严格后验反例的独立预评分冻结](../../protocols/R264_ABC_9_WORLDS_432_THETA_SIMULATION_ATOMS_PRESCORE_FREEZE_2026-10-23.md)，先行冻结提交[58f17a0b](https://github.com/edwardsage419/Psychohistory-Research/commit/58f17a0b73556dfb2517c4bf26da3bd82c719bd6)，后提交模型及CI。

## 全模型概率定义与两个完全独立计算路线

对每个人工world，冻结θ∈{0,1,2}三个等先验候选，`P(θ)=1/3`。条件给定θ，原模拟器读取两个**独立2bit均匀**随机数r1,r2∈{0,1,2,3}，生成`Y1=1{r1<4q1θ},Y2=1{r2<4q2θ}`。q1,q2只能是0,1/4,1/2,3/4,1，从原四位可以完整实现严格Bernoulli概率。因此每world3个先验θ×16种原4bit=**48完整人工原联合来源类型**、每条质量1/48；九world共**432完整原source**，不是人口遗传学432个真人样本。全部CSV保留每θ、原四位随机数、两个q、模拟Y和固定目标人工观测`Yobs=(1,0)`、源质量。

对每world冻结三种距离：全向量Hamming `|Y1−1|+|Y2|`，计数摘要 `|Y1+Y2−1|`，仅首项 `|Y1−1|`；三种阈值ε∈{0,1,2}。**第一拒绝ABC路线只读取原全部48source模拟输出和距离阈值**，依照“满足距离≤ε”的原source质量求每个θ的未规范化接受质量，再归一成后验并保留全部三θ、接受率及与完整精确贝叶斯后验的总变差距离（TV）。ABC接受过程**不调用似然函数**；当接受率为0的某个θ出现时，其后验质量合法为0，整体接受率仍为正。

**第二独立解析路线不使用原source模拟器**，根据Bernoulli乘积完整计算给定θ的四种可能结果`P(Y=(a,b)|θ)=q1θ^a(1−q1θ)^(1−a)q2θ^b(1−q2θ)^(1−b)`，对每种距离/ε分别在四结果上求解析接受率和θ后验；九world×九种ABC设置=**81组模型—距离—ε完整后验、接受率和TV与原source逐Fraction精确相同**。再独立计算完整观测真正后验`P(θ|Yobs=(1,0))∝(1/3)q1θ(1−q2θ)`作为参照，所有world的FULL_HAMMING ε=0 ABC与精确全数据Bayes后验严格一致，TV=0。容忍度为2时三距离必接收所有source、后验全部(1/3,1/3,1/3)回到先验；COUNT_SUM和FIRST_COMPONENT的距离最大只为1，故ε≥1即已经完全抹掉所有观测信息。

## 九world的关键完整贝叶斯 vs COUNT摘要ε=0后验

| 冻结模型world | 完整Y=(1,0)后验θ0,θ1,θ2 | COUNT_SUM ε=0后验 | TV |
|---|---|---|---:|
| IID_GRADIENT | (3/10,2/5,3/10) | (3/10,2/5,3/10) | 0 |
| COMPLEMENTARY_GRADIENT | (1/14,2/7,9/14) | (5/14,2/7,5/14) | 2/7 |
| REVERSED_COMPLEMENT | (9/14,2/7,1/14) | (5/14,2/7,5/14) | 2/7 |
| FIRST_ONLY_INFORMATIVE | (1/6,1/3,1/2) | (1/3,1/3,1/3) | 1/6 |
| SECOND_ONLY_INFORMATIVE | (1/2,1/3,1/6) | (1/3,1/3,1/3) | 1/6 |
| NO_SIGNAL | (1/3,1/3,1/3) | (1/3,1/3,1/3) | 0 |
| DETERMINISTIC_ENDS | (0,1/5,4/5) | (2/5,1/5,2/5) | 2/5 |
| NONMONOTONE_IID | (3/10,3/10,2/5) | (3/10,3/10,2/5) | 0 |
| FIRST_WITH_SECOND_QUARTER | (1/6,1/3,1/2) | (1/4,1/3,5/12) | 1/12 |

**即使ε=0，摘要不充分仍会错误识别后验。** COMPLEMENTARY_GRADIENT与REVERSED_COMPLEMENT仅调换每个θ下两个观测变量的伯努利概率，即(q1θ,q2θ)互换；给定θ的计数K=Y1+Y2的完整概率分布逐θ**严格相同**，故任何只读取总K的ABC根本无法区分两world。观察Y=(1,0)时，前一world完整Bayes偏向θ2、后者偏向θ0，确切后验分别为(1/14,2/7,9/14)与(9/14,2/7,1/14)，但COUNT摘要ε0两者都输出对称(5/14,2/7,5/14)，TV皆为2/7。继续减小容忍度无法恢复已被映射K丢弃的变量身份，此为**模型层的摘要非充分性而非单纯样本不足**。

**摘要是否充分依赖模型结构。** IID_GRADIENT的两个观测在给定θ下独立同分布，完整数据(1,0)与所有K=1的数据有相同似然比，所以COUNT ε0与完整Bayes一致；NONMONOTONE_IID也一致。FIRST_ONLY_INFORMATIVE中q2对θ是常量1/2，FIRST_COMPONENT ε0保留了所有关于θ的变化，故尽管忽略了Y2仍与完整Bayes一致；但其COUNT ε0却将θ后验冲淡回统一先验。SECOND_ONLY_INFORMATIVE则正好相反：FIRST_COMPONENT完全无参数信息、ABC返回先验，而完整数据Y2=0给出了(1/2,1/3,1/6)。NO_SIGNAL中全部q均1/2，真正完整Bayes也仍是均匀先验，不能把后验未变化称成ABC失效。DETERMINISTIC_ENDS允许θ0完整Yobs发生概率严格0，所以全数据后验θ0=0；若仅取总K会掩盖Y=(1,0)与Y=(0,1)的根本方向差别。

## CI实际记录、归档和科学边界

[完整原生Python simulator拒绝ABC与独立Bernoulli四结果解析程序](r264_exact_finite_rejection_abc.py) · [九world432完整原先验—模拟source CSV](R264_ALL_432_ORIGINAL_THETA_SIMULATOR_SOURCE_ATOMS.csv) · [九world81后验/接受率/TV和精确Bayes JSON](R264_EXACT_RESULTS.json) · [原CSV及结果SHA256机读来源](R264_FINAL_MACHINE_ACCEPTANCE.json)。

[GitHub Actions run39899758034](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39899758034)总体completed/success，三job全部success；Python3.11与3.12实际日志各`Ran 82 tests`、`OK`，合计**164次真实双版本单测通过**。第三完全独立archive作业读取全部432source，检查每world48个原θ×四随机bit唯一性、源1/48和Bernoulli阈值重算、独立四可能Y后验积分与全部81距离/ε设置完全一致、全部9world精确Bayes与TV、两world摘要计数非识别反例及松阈值先验回归、CSV/JSON SHA256；真实打印`R264_ALL_432_ORIGINAL_PRIOR_SIMULATOR_AND_81_ABC_EXACT_POSTERIORS_VERIFIED`以及`R264_ALL_432_ORIGINAL_ABC_SOURCE_ATOMS_ARCHIVED`。全部原CSV/计算JSON/机器收据由GitHub bot永久提交main [ce269471](https://github.com/edwardsage419/Psychohistory-Research/commit/ce26947160448c00cbeae80fb6c136be53dd3fe0)。

原CSV SHA256 `6363dce373d6698b7f23f0585aa11bc897aebf03ab96dcee65f1d84477a80167`；结果JSON SHA256 `8cb635342ca85a35058a42f2c70824c7293da09b6942350bcf27c6e60181133b`。本项只允许结题为`CLOSED_BOUNDED_E1_EXACT_FINITE_REJECTION_ABC_AND_SUMMARY_INFORMATION_LOSS`。未来若用于心理史学实际实验模型，必须另做独立真实数据、参数辨识、摘要充分性检验和后验校准，不能直接继承人工模型的准确性。E2/E3新证据0，R073/PESEN v0.1冻结。下一原11-025 Sobol Global Sensitivity（拟R265，P1）。
