# R199 隐马尔可夫时间序列：24人工HMM机制、Viterbi最优路径、逐时点平滑与观测不可识别性

日期：2026-10-21。原239模型目录P2/08-023 HMM Time Series。正式科研状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_HMM_SEQUENCE_DECODING**。一切隐藏路径真值、观测序列和未来序列均源于固定人工有理数生成机制；未获取真人重复行为或外部历史序列，新增E2=0、E3=0。

## 原始方法依据及研究适用范围

Baum, Petrie, Soules and Weiss (1970), [A Maximization Technique Occurring in the Statistical Analysis of Probabilistic Functions of Markov Chains](https://doi.org/10.1214/aoms/1177697196), Annals of Mathematical Statistics41(1):164–171，研究隐状态Markov过程所生成随机观测序列及似然估计相关方法。Viterbi (1967), [Error Bounds for Convolutional Codes and an Asymptotically Optimum Decoding Algorithm](https://doi.org/10.1109/TIT.1967.1054010), IEEE Trans. Information Theory13(2):260–269，提出最大似然路径解码的动态规划来源。Rabiner (1989), [A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition](https://doi.org/10.1109/5.18626), Proc. IEEE77(2):257–286，系统回顾离散HMM的完整观测似然、隐藏路径解码和模型参数估计三类不同任务。R199严格只执行**两态、二元观测、已知参数、固定六模型比较**；没有运行Baum–Welch去估计连续未知转移/发射参数，没有声称复现上述原文真实语音或行为数据，也未证实社会隐藏状态存在。

## 计算前冻结、真实来源与完整训练空间

[R199正式计算前冻结协议](../../protocols/R199_HMM_24_WORLDS_2064_TRAINS_PRESCORE_FREEZE_2026-10-21.md)于commit`cb5969ae6eb90caf839478d98a0b7ce71c5db778`先于源码、计算评分及结论永久提交main。隐藏状态X_t∈{0,1}，每条轨迹X1初始公平二点，隐藏状态维持上一状态的真实概率为a，各次有噪声测量Y_t与X_t一致的概率为r，各轨迹彼此独立。六种固定真来源并同时为固定工作候选，模型/平局优先次序：

| 原模型 | 隐藏状态自保持率a | 观测传感器一致率r | 受控作用 |
| --- | --- | --- | --- |
| BASE | 3/4 | 3/4 | 基础相关二态模型 |
| LABEL_SWAPPED | 3/4 | 1/4 | BASE的全部隐藏标签整体置换 |
| IID_HIDDEN | 1/2 | 3/4 | 隐状态时间上完全独立 |
| SWITCH_HIDDEN | 1/4 | 3/4 | 反保持/高切换 |
| WEAK_SIGNAL | 3/4 | 5/8 | 隐状态可见信号变弱 |
| STRONG_SIGNAL | 3/4 | 7/8 | 隐状态可见信号增强 |

观测序列长度L∈{3,4}，每个人工世界训练m∈{1,2}条**独立完整可见序列**。6×2×2=**24个人工完整真实世界**。每个固定真来源、L、m完整穷举所有可见训练序列的有序组合，准确概率和1，合计`6×(2^3+(2^3)^2+2^4+(2^4)^2)=2064`组完整有序训练数据。仅合并训练序列**在训练组内的顺序等价性**，保留8、36、16、136个四种(L,m)唯一无序模型拟合profile，共**196种**；完整的2064条原始有序训练来源没有省略。

## 三种互相独立的真实概率及路径算法

**完整观测Y序列概率**：A使用前向状态质量递推，首时隐藏状态公平、给定状态传感器二元发射，再按真实二元转移和发射更新；B独立枚举全部2^L条隐藏路径、把初始概率、全部真实隐藏转移及各时点观测发射概率直接相乘后求和。两条Fraction算法对全部六候选×L3/4×全部可见轨迹的完整观测概率逐点严格相等且归一，所有源真实概率严格正。

**给定完整可见序列的每时点隐藏概率**：A的前向alpha联合状态质量与向后beta剩余观测likelihood相乘后归一，生成`P(X_t=1|Y1...YL)`；B直接对全部潜在完整路径以真联合概率选择相应时间X_t求和再归一。六候选、L3/4、全部可见样本与每个时点逐Fraction完全一致，绝不把局部过滤误认为已包含未来观测的平滑。

**整条最可能隐藏路径**：标准Viterbi`max-product`动态规划沿前缀保存最大完整联合路径权重与对应路径，包含正确Markov转移与发射；独立算法对全部隐藏路径穷举`P(X,Y)`并直接全局argmax，两算法逐路径完全一致。所有并列取完整路径0/1字典序最小。每时点单独最大后验产生的逐时点解码序列则按`P(X_t=1|Y)>1/2`选1，平局选0。二者数学优化目标不同，不应在真实社会状态分析中互换。

**实得差别而非概念假说**：固定六候选×L3/4×全部可见序列共**144个完整工作模型/观测解码配置**，实际有**54个**的Viterbi整路径MAP与逐时点后验MAP序列不同；其余90例相同。这是明确由真实Fraction动态规划及完整隐路径穷举验收的有限样本差异，不意味着“逐时解码总是更正确”或整条隐藏路径最可能来自每个时间点的独立最大后验。

## 只用训练可见观测选择候选，再评价完全独立未来序列

对于每个实际有序训练组合，只用所有m条训练**可见完整Y**的候选完整观察联合likelihood比较上述六已知参数工作模型；同一候选的训练联合概率另外按观测完整轨迹Counter频数幂计算，所有2064组×六候选逐Fraction相同。训练likelihood并列按固定模型顺序择前一个，绝不使用真隐藏X、原真实源名称或者未来测试序列的可见值来选模。

用独立抽取的同真来源新可见完整序列Y'计算完整未来真实分布下的交叉熵`−Σ P_true(Y') ln P_fit(Y')`，一条由Python math.log直接浮点概率计算，另一条以70位Decimal.ln独立计算，两数值通道每个真源×拟合候选×L及所有世界来源加权分数误差≤1e−12。另向新独立序列预测最后一条测量Y'_L：只见其前L−1条观测，根据预先选好的候选HMM前向过滤及一次转移+发射给出下一观测为1概率；以真实全新序列真概率求二元Brier。第二算法独立将相同完整真源分布按前缀边际化，计算条件Bernoulli Brier再加权，**所有真源×候选×L逐Fraction同值**。

第三类评分只因人工数据给定真实X标签而合法：对独立新序列`P_source(X',Y')`全部穷举，以选中候选的Viterbi解码计算整条真隐藏路径准确概率，以逐时点最大后验与Viterbi分别计算每时间位真隐藏标签准确概率。对工作候选恰等于真源时，逐时真后验MAP分类每时间平均准确率≥Viterbi每时间平均准确率；而已知真源Viterbi整条最大后验路径的整条真路径命中率≥任何其它固定模型作出的解码器。非真来源选择器可能违反这种逐时准确率排序，且现实中无独立真隐藏标签时不应报成可实证验证的准确率。

## 可见分布完全同一，但潜在标签归因相反

两真来源BASE与LABEL_SWAPPED的隐藏状态初始均1/2、保持率都3/4；LABEL_SWAPPED把隐藏0和1在语义上完全交换，相应的观测与隐藏一致率由3/4变为1/4。因此对任意可见Y完整序列都严格有`P_BASE(Y)=P_LABEL_SWAPPED(Y)`，而对任意时点`P_BASE(X_t=1|Y)=1−P_LABEL_SWAPPED(X_t=1|Y)`。对于每个完整隐藏路径，BASE赋予(X,Y)的真联合质量等于LABEL_SWAPPED赋予(逐位翻转X,Y)的质量，原生程序全部逐Fraction验证。这是**类别标签语义不可识别**，无限多可见训练序列在本两个精确定义模型之间也无法决定哪种隐藏标签名称为真。

受限六候选中的其它参数机制也可能在非常短训练上得到更高似然，故训练择优并非简单“永远选BASE”。但由于BASE与LABEL_SWAPPED每条原数据likelihood全相等、且BASE优先，**LABEL_SWAPPED工作候选在全部196种唯一profile中一次都没有被选出**；BASE作为工作模型本身也可能输给IID_HIDDEN、SWITCH_HIDDEN、STRONG_SIGNAL等其它固定候选。BASE和LABEL_SWAPPED两真实源的**完整24世界中对应(L,m)的真实训练选模分布及新独立可见序列预测成绩全部相同**。但由于实际源人工X标签相反，隐藏路径与逐时真标签准确率差别巨大。

取L=4、两条独立训练完整可见序列(m=2)的真实完整数据积分：
| 真实人工来源 | 新可见完整序列logloss | 新末观测Brier | 人工真隐藏整条Viterbi路径命中 | 逐时边际解码真标签准确率 |
| --- | ---: | ---: | ---: | ---: |
| BASE | 2.791243 | 0.252627 | 28.8375% | 73.8470% |
| LABEL_SWAPPED | 2.791243 | 0.252627 | 1.0215% | 26.1530% |

这里的“人工真隐藏整条Viterbi路径命中”和“逐时边际准确率”不是由真实社会观测数据得出，而是由于实验知道虚构的每条X路径才能计算。两个来源相同可见预测分数并不支持判断哪个标签方向在现实中正确，必须依靠额外定义、锚定变量或独立人工可追踪真状态的来源才能给标签命名。

同样L4、m2时，工作模型选回真来源的概率因参数候选与人工样本结构而差异显著：BASE≈3.55%，LABEL_SWAPPED固定为0%，IID_HIDDEN≈29.69%，SWITCH_HIDDEN≈45.28%，WEAK_SIGNAL=0%，STRONG_SIGNAL≈62.34%。以上是**具体已知六候选、确定性模型并列规则、两条短训练序列**下的选模现象，不可视为一般HMM研究的普适拟合表现。该有限例也说明“已知真模型的贝叶斯最优隐藏路径”与“有限观测实际选出哪套HMM”必须严格区分。

## GitHub三job正式验收与研究归档

[GitHub Actions39593984143](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39593984143)：Python3.11与3.12各执行40项原生数学及错误输入测试，共**80次全部success**，第三job真实运行24人工世界2064有序原始训练样本、196完整拟合profile和144完整隐藏后验/Viterbi解码配置，独立新序列math/Decimal logloss与真正未来Brier，校验原CSV/JSON行数与全部SHA及七文件确定性ZIP，三项job均success；真实机器结果永久提交main。[机器原数据提交cc464dc4](https://github.com/edwardsage419/Psychohistory-Research/commit/cc464dc45c7b7583a4da091fc70ec9d108dfa0ef)。

研究产物：
* [R199_EXACT_RESULTS.json](R199_EXACT_RESULTS.json)：全部24世界训练选模分布、可见完整新序列对数分数、下一观测Brier、人工真隐藏标签两种目标、BASE与全标签交换反例，SHA256`fd10455eb9923fb8d380a98dc8213a37a217be669961425aab4c45e3fdf557f0`。
* [R199_ALL_2064_ORDERED_OBSERVED_TRAINING_SETS.csv](R199_ALL_2064_ORDERED_OBSERVED_TRAINING_SETS.csv)：全部2064种真实有序人工可见训练轨迹组合及其原始概率、六模型准确训练likelihood、选择模型和其真实新轨迹观测/仅人工真标签评分，SHA256`0e238bc12b69d74badf62a98fbdfdb28e9ef2e5acf7347a59fd649c72b22adbb`。
* [R199_ALL_196_OBSERVABLE_FIT_PROFILES.json](R199_ALL_196_OBSERVABLE_FIT_PROFILES.json)：全部196种观察训练序列置换等价profile，六候选完整Fraction似然、确定性模型选择，SHA256`189b57f9b784a4bf6a765d6207fceff66e321b41a527d8cc835987a832ef336b`。
* [R199_ALL_144_OBSERVABLE_HIDDEN_DECODINGS.json](R199_ALL_144_OBSERVABLE_HIDDEN_DECODINGS.json)：144组完整可见Y与工作模型组合的全部各时点隐藏后验、有理数Viterbi联合质量及完整路径、逐时点最大后验路径和54个差异标记，SHA256`d7498cb7f6d7e53e7e3a57e4efe3a683c4cdafa4d3cd409d03f2b957f9a484d3`。
* [R199_FINAL_MACHINE_ACCEPTANCE.json](R199_FINAL_MACHINE_ACCEPTANCE.json)：前向/穷举、后向平滑、Viterbi/穷举、未来测试双路以及SHA科研验收。
* [r199_exact_hmm_sequence_decoding.py](r199_exact_hmm_sequence_decoding.py)：全部原生Fraction数学计算、独立新序列测试、40项原生双Python测试。
* [R199_Exact_24_HMM_Sequence_Worlds.zip](R199_Exact_24_HMM_Sequence_Worlds.zip)：原协议、源码、原2064训练CSV、196拟合与144隐藏后验全库、结果JSON、机器验收的七文件确定性可复验包。

科研结论限于**E1已知参数有限二态HMM的隐路径解码与可见预测科学方法**，并未产生真实社会、心理或制度隐变量的识别证据，也未复验R073真人重复博弈预测。E2/E3新增0，R073和PESEN v0.1继续冻结。下一原目录 **R200 P1/08-024 Change Point Detection（变点检测）**。保持先完成既定全部R、之后统一归纳分类、最后熔炼。
