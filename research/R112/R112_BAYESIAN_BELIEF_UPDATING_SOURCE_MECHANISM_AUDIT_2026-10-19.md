# R112 贝叶斯信念更新：有限假说、条件证据、Beta-Bernoulli 共轭

日期：2026-10-19
研究类别：模型学习阶段A；原2026-10-14知识目录P0条目 02-006 Bayesian Belief Updating。
**本项为R112研究编号，02-006是知识目录条目；不能按研究编号断言239模型均已学习。**

## 1. 真实文献来源及读取范围

历史第一手来源：Thomas Bayes and Richard Price (1763), An Essay towards solving a Problem in the Doctrine of Chances, Philosophical Transactions 53, 370–418. DOI https://doi.org/10.1098/rstl.1763.0053 。原刊首段与1763年引介在 https://en.wikisource.org/wiki/Page:Philosophical_Transactions_-_Volume_053.djvu/436 可核对，全文PDF在 https://bayes.wustl.edu/Manual/an.essay.pdf 。所引原历史文章主要处理反向估计事件发生概率的问题；本项目的现代有限假说公式与Beta参数记号是当代形式化，不宣称原论文原样写出这些函数及Python算法。

现代认知模型作者第一手手稿：Griffiths TL, Kemp C, Tenenbaum JB (2008), Bayesian models of cognition. Cambridge Handbook of Computational Cognitive Modeling / Cambridge Handbook of Computational Psychology, 59–100. 原作者C. Kemp自托管PDF https://charleskemp.com/papers/bayeschapter.pdf 。本次核阅该原稿PDF第5–6页，原稿§2.1 的式(1)至(5)分别给出联合分解、Bayes规则与离散假说的归一化后验，作者明确说明概率模型给出了关于学习和归纳推理的规范性计算分析，在认知研究中仍须有经验或过程层证据。出版方章节DOI https://doi.org/10.1017/CBO9780511816772.006 。

上两项是出处。程序本身实现的是本轮明定的有限状态与共轭玩具模型，没有声称复现作者具体人类实验、模型比较结果或参数拟合。

## 2. 机制结构和可识别输入

假说集合 H={h_1,...,h_K}，先验 p_i>=0，总和1。每次合法证据事件 e 的离散似然 l_i=P(e|h_i,e_1,...,e_{t-1}) 属于[0,1]，且必须依赖正确的已观察历史。后验

p_i' = (p_i l_i) / sum_j (p_j l_j).

若所有已支持假说的该事件概率为0，则分母为零，必须明确失败并检查模型错设、信息定义或样本来源；不可任意返回均匀后验。先验恰为0的假说在一般Bayes乘法更新后不会重获质量，这既是数学性质，也是先验支持设置的实质假设。模型归一化采用对数权重与log-sum-exp样式移位，保持极低似然下的数值稳定；有限浮点实现仍受机器精度制约。

二元假说的证据似然比 LR = P(e|h1)/P(e|h0)；后验odds = 先验odds × LR。在后验概率0或1等边界，odds表示需要另行处理，不能把无穷比值作为可靠已估计证据。

## 3. 本轮核心假设检验：重复消息非独立证据

人工案例先验P(h1)=P(h0)=0.5，首条观察在两假说下的似然分别0.9和0.1，后验P(h1|e1)=0.9。若第二条信息是原消息的确定性拷贝，条件似然P(e2=e1|h1,e1)=P(e2=e1|h0,e1)=1，因此正确更新后P(h1|e1,e2)=0.9。若错误重复使用原0.9/0.1似然，相当于假设两个条件独立的消息，错误得出81/82≈0.987804878。**更高的信念数值无法证明获得了新的独立证据**。在谣言重复、共用信息源与社交网络传播中，这类条件依赖尤其需要来源标记；但本项是纯构造概率反例，没有实际网络用户、社会传播数据或真实认知效应的经验验证。

本程序允许顺序输入每个事件“给定之前所有已知证据”的条件似然向量，并明确将是否独立视为调用者必须论证的结构假设。它不会从给定数字自动识别来源独立性。

## 4. Beta与Bernoulli模型的限定延伸

未知且跨观测不变的成功概率 θ 先验Beta(alpha,beta)，alpha,beta>0。在观测相互条件独立且每次给定θ都是Bernoulli(θ)时，s次成功和f次失败的后验为Beta(alpha+s,beta+f)，下一次成功预测概率为(alpha+s)/(alpha+beta+s+f)。θ后验方差为 a'b'/((a'+b')²(a'+b'+1))。

一串指定顺序的二元数据边际概率为 B(alpha+s,beta+f)/B(alpha,beta)，**不额外乘组合数**；只有忽略顺序、聚合成成功数的Beta-binomial概率才出现二项组合因子。这两种目标单位必须分开。代码通过 lgamma 保持计算数值范围，并和一步预测概率逐项相乘的对数结果独立比较。

独立同分布、固定θ、观测值合法与模型状态完整性均为前提。时间变化、策略选择、观察者过滤或消息重复可能令共轭公式模型错设；对真实群体决策不能仅由先验计算精确性断言心理过程遵循Bayes。规范性推理和实际认知机制需不同证据。

## 5. 程序、验收门与剩余工作

标准库原生实现：research/R112/r112_bayesian_belief_updating.py。
合成测试：research/R112/test_r112_bayesian_belief_updating.py。

本轮计划25项纯合成单元测试：贝叶斯归一、先验支持、零似然、不可观测事件严格拒绝、极小似然数值安全、维度与布尔伪装拒绝、二元odds、独立证据顺序条件，以及完美复制消息反例；Beta参数、批量与逐次更新、方差、精确边际概率和非法输入均测试。所有脚本不得取得真人数据，后续CI实跑通过前仍只能称“代码已提交待验”。SCI_E2=0，真实数据端到端复现=NO，真实人类描述性认知符合度=NOT_ESTABLISHED；不得跨实验复用为R073/PESEN正式机制融合。

**阶段完成门**：实际GitHub CI按原25项测试成功、匿名无真人源文件、源码哈希记录一致，才将本条标注LEARNING_COMPLETE_BOUNDED_FOR_DISCRETE_MATH_AND_CONJUGATE_SYNTHETICS。数学学会的边界仍是该模型实例，不代表所有Bayesian cognition家族或239条目录掌握完成。
