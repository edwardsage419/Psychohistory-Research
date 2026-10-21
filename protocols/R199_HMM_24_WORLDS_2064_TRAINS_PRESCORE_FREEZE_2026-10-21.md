# R199 隐马尔可夫时间序列：24个两态HMM世界、2064完整训练轨迹、196拟合配置与Viterbi/后验解码，计算前冻结

日期：2026-10-21。原239候选目录P2/08-023 HMM Time Series。状态 **PRESCORE_FROZEN_E1_ARTIFICIAL_HMM_SEQUENCE_DECODING**。

## 理论与精确范围

Baum, Petrie, Soules and Weiss (1970), *A Maximization Technique Occurring in the Statistical Analysis of Probabilistic Functions of Markov Chains*, Ann. Math. Stat. 41(1):164–171, https://doi.org/10.1214/aoms/1177697196；Viterbi (1967), *Error Bounds for Convolutional Codes and an Asymptotically Optimum Decoding Algorithm*, IEEE Trans. Information Theory 13(2):260–269, https://doi.org/10.1109/TIT.1967.1054010；Rabiner (1989), *A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition*, Proc. IEEE 77(2):257–286, https://doi.org/10.1109/5.18626。这些原始来源用于前向概率、动态最优路径和隐状态推断的理论背景，**不声称复现原作者数据、一般未知转移HMM的Baum–Welch参数拟合、真实文化状态或历史隐藏制度**。

## 六种冻结生成过程与完整训练全集

每条人工观测序列长度L∈{3,4}，初始隐状态X1=0/1等概率1/2。隐藏状态的每步保留概率`a=P(X_t=X_{t−1})`、传感器正确率`r=P(Y_t=X_t)`均事前已知且严格在(0,1)，观测发射随时间和隐藏状态条件独立。所有轨迹彼此独立，不跨轨迹构造转移。

固定六种真实来源同时作为六个工作候选，候选顺序和全联合似然平局决胜顺序如下：
1. BASE：a=3/4，r=3/4。
2. LABEL_SWAPPED：a=3/4，r=1/4，等价于把BASE的全部潜在标签0↔1交换，同时把观测发射语义反转，真实可见轨迹分布完全一样；
3. IID_HIDDEN：a=1/2，r=3/4，隐藏独立过程；
4. SWITCH_HIDDEN：a=1/4，r=3/4；
5. WEAK_SIGNAL：a=3/4，r=5/8；
6. STRONG_SIGNAL：a=3/4，r=7/8。

独立训练完整可见轨迹数m∈{1,2}。6种来源×2种L×2种m共 **24个人工世界**，真正穷举所有有序m轨迹的完整可见二值向量：`6×(8+8²+16+16²)=2064`套训练样本，全部独立来源概率严格有理数、每个世界全样本空间概率严格和1。训练轨迹组内部交换顺序不改变候选似然，因此每个L,m的无序完整拟合型数量分别8、36、16、136，共**196个精确拟合profile**。原CSV保留所有2064组有序样本及实际概率和六候选准确likelihood，不能只存196个去重训练样本。真隐状态人工标签在训练拟合阶段不可见。

## 五条可独立交叉核验的数学计算

* 真完整可见序列PMF A：标准前向状态概率递推，先初始隐状态概率1/2乘第一次发射，再逐期边际化两状态转移和发射。
* PMF B：独立完整枚举所有2^L隐路径，对完整真实联合`P(X_1...X_L,Y_1...Y_L)`求和，不调用前向递推。对全部六候选×两长度×全部Y状态逐Fraction同值且归一。
* 隐状态平滑：A算法分别构造alpha前向联合状态质量与beta后向观测似然，形成`P(X_t=1|Y_1...Y_L)`；B算法对完整2^L潜在路径逐真联合求和再归一。全部候选、观测及t逐Fraction相同。
* Viterbi整路径最大后验：A算法按上一时点最佳前缀候选`max`运行动态规划，分数是未归一化`P(X,Y)`而非单独各时点posterior乘积，路径并列时固定取**完整0/1字典序最小路径**；B算法穷举所有2^L潜在路径后直接在完整联合概率最大值中取字典序最小，必须逐状态序列完全相同。**逐时间边际最大后验（posterior decoding）并不定义为Viterbi整路径MAP**，二者须分别输出。
* 完整训练m组似然：按每个可见训练轨迹单独边际PMF相乘与无序轨迹Counter频数幂分别求Fraction，全部2064×六候选严格相等；候选依据完整可见训练轨迹联合最大似然选择，平局严格沿上文顺序。不能用真隐标签/真实模型ID/独立未来测试成绩选择候选。

## 独立可见预测评分及人工真潜在标签评分

针对每一个已经完成的训练原样本，固定选中的工作模型，在全新的**独立新观察轨迹**Y'_1...Y'_L的完整支持下，以真来源PMF计算：
1. 整条新可见轨迹交叉熵`−Σ_y P_true(y)log P_model(y)`，必须以math.log浮点和70位Decimal.ln分别计算、绝对差≤1e−12，并按每条真训练样本来源权重整合所有24世界的未来logloss。允许真实BASE/LABEL_SWAPPED的完整观测预测loss完全一样，不能声称凭观察logloss可以区分其隐藏标签。
2. 仅使用新轨迹前L−1条可见测量预测最后一次Y'_L，固定选中模型从新轨迹前缀过滤隐藏X'_{L−1}、向前一转移及一次发射求预测概率；以真完整Y'来源求独立Brier。另一条算法依真前缀概率×真条件下一Y=1的二元方差+偏差得出同一Fraction Brier；全部真来源×工作模型×L都必须双路Fraction相等。测试末状态绝不参与候选训练拟合。
3. 只有人工模型允许知道真正X'_1...X'_L标签时，才可评估工作模型Viterbi整条路径是否全部正确的概率，以及逐时posterior-decoding和Viterbi的真标签准确率。真标签评分对全部Y和真正X两者的联合概率完整积分，全部Fraction而不是以“高概率后验”代替实际真标签。作为检验，对工作候选等于真实生成源时，按真实后验逐时选的单点准确率必须≥同源Viterbi路径各位置准确率；真源Viterbi路径整体命中率必须≥同源任意固定其它工作候选给定Y的整路径命中率。工作候选非真源时不预设哪种解码误差更小。

## 必须锁定的不可识别反例与正负对照

* BASE与LABEL_SWAPPED拥有完全相同的完整可见轨迹概率，对任意L、m即使无限增加只观察到的Y也不能区分；隐藏路径后验则互补：`P_BASE(X_t=1|Y)=1−P_LABEL_SWAPPED(X_t=1|Y)`。这不是“两个类别同义”，而是没有外部锚定的类别**命名语义**不能由观测资料决定。同真来源BASE时固定平局偏好BASE可能在人工标签上正确；若真源LABEL_SWAPPED但模型选BASE，外部可见预测仍可完全准确，而人工真隐藏标签的解码可能出错。必须保留两源全原始风险和隐藏标签准确率。
* IID_HIDDEN的真隐藏状态每期都独立，全部Y可见轨迹实际IID Bernoulli(1/2)；BASE的可见单时期边际也同为1/2，但是连续观测存在相关。因此单时频率不等于真实隐藏转移机制。
* TRUE状态标签整体翻转时完整可见PMF不变，但oracle隐路径标签对照会交换；这不构成外部实证证据。
* 即使真HMM已知，Viterbi最大整条路径与逐时最大后验可能有不同优化目标；如果选定六个候选及L3/4的有限全集恰无不同路径实例，应**如实报告没有观察到不一致**，不能凭概念偷造反例。
* 固定参数候选选择的训练长度很短，真正独立预测性能不必与oracle相等，报告完整24世界、各候选被选概率和真实未来损失，不根据结果修改参数。

## 机器验收与产物

Python3.11/3.12各≥30原生测试：24世界、2064训练有序序列、196完整候选profile、真可见PMF/直接潜在路径求和、前向后向平滑、Viterbi与穷举最大路径、标签互换观测全等和隐藏posterior互补、train sample完整概率归一、两套训练likelihood、70位Decimal与math.log完整新轨迹交叉熵、二路独立未来观测Brier、人工真标签路径/逐时准确率界限、禁止看见未来/隐藏真标签进行选模，错误输入fail-closed。

永久归档2064完整原训练CSV、196精确候选配置JSON、全24人工世界独立预测和真标签解码JSON、每个源×L的全可见历史隐后验/Viterbi解码完整配置库JSON、机器验收、源码、科学报告及含原协议的确定性ZIP。GitHub Actions三个job均success、实际数据提交main并核验后，才准**CLOSED_BOUNDED_E1_ARTIFICIAL_HMM_SEQUENCE_DECODING**。

只限人工E1；新增真人E2=0、独立历史E3=0；R073和PESEN v0.1冻结。下一原目录R200 P1/08-024 Change Point Detection（变点检测）。原R系列全部完成后统一分类，最后熔炼。
