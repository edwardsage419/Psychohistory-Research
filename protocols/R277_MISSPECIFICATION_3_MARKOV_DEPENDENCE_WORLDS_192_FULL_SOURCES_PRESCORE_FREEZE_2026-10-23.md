# R277 模型错设诊断：三种二元Markov依赖、192个完整有序原source；先冻结

日期：2026-10-23 Asia/Taipei。原239目录12-007 Model Misspecification Checks（P0），研究R277。主要理论参照：Gelman, Meng & Stern (1996), *Posterior predictive assessment of model fitness via realized discrepancies*, Statistica Sinica 6:733–807（主文733–760，后续含讨论），公开原文 https://sites.stat.columbia.edu/gelman/research/published/A6n41.pdf；Roberts et al. (2017), *Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure*, DOI https://doi.org/10.1111/ecog.02881 。本项建立独立的人工Markov过程及诊断反例，不声称复现这些文献的实际数据或模型。

## 三个人工真实数据生成机制
六个有序二bit X1...X6，首个X1公平Bernoulli(1/2)，其后5个转移各自独立选择“保持相同”的概率s、或“翻转”的概率1−s，形成一阶对称二状态Markov链。三种冻结真机制：
* ANTIPERSISTENT：s=1/4；
* IID_FAIR：s=1/2；
* PERSISTENT：s=3/4。

每机制完整列出2^6=64种原有序六bit source，原质量(1/2)*s^T*(1-s)^(5−T)，T=sum_{t=2}^6 1[X_t=X_{t-1}]，全部严格正质量。三个机制共192个带真机制标签的完整人工原source类型，每source随机源只是数学空间配置，非独立真人或历史观察。由于对称转移和公平首状态，三个机制在每个时刻的**边缘P(Xt=1)=1/2完全相同**，因此事前固定的常数预测器q=1/2对每一原source六个时间点的单行Brier均1/4，完整来源加权的整体逐点Brier也恰是1/4。不能用此单点分数推出链的依赖机制正确。

## 两个冻结诊断目标及预定方向
* 只看边缘的MARGINAL_HALF_DIAGNOSTIC：六个预测概率均1/2；每行Brier恒1/4，三个机制无区别。注意单次样本中“边缘拟合优良”不等于该次样本证明真边缘已知，真实研究需要独立校准检验。
* JOINT_TRANSITION_DIAGNOSTIC：统计完整有序观测的T“相邻相同转移数”，关注两类事前冻结定向区域T≥4（持续性过高）或T≤1（持续性过低）。IID_FAIR参考分布T_rep~Binomial(5,1/2)，上、下尾各3/16。因此每个定向诊断参照水平3/16，不能把两尾检查各自当成整体家庭误报3/16；联合区域在IID下为3/8。

独立解析真值：
|真机制|s|E[T]|P(T≥4)|P(T≤1)|每行边缘Brier|
|---|---|---|---|---|---|
|ANTIPERSISTENT|1/4|5/4|1/64|81/128|1/4|
|IID_FAIR|1/2|5/2|3/16|3/16|1/4|
|PERSISTENT|3/4|15/4|81/128|1/64|1/4|
以上T来自独立的5个转移保持指示，相比完整64个六bit原source求和，另可从Binomial(5,s)公式得到：P(T≥4)=5s^4(1−s)+s^5；P(T≤1)=(1−s)^5+5s(1−s)^4，E[T]=5s。对真实持续性机制s3/4，上尾T≥4的触发概率为81/128；对真实反持续机制s1/4，下尾T≤1触发概率同为81/128，而参考IID机制的对应各侧误报3/16。以上只是所选尾区发生概率/诊断敏感性，不是复现真人动力学，也没有经典显著性门限或多重比较校正声明。

## 三条独立检验路线
A：逐真实机制穷举全部64种完整六bit有序source，保存每原序列X、真s、转移保持指标、T、原精确质量、六行逐点Brier以及两侧预先定义的事件标记；积分各机制质量和两端概率、E[T]。
B：完全不使用六bit原source枚举，从首状态公平性及5独立转移保持变量直接用Binomial(5,s)组合计算T完整PMF、尾区概率、均值和P(Xt=1)=1/2的边缘结论。
C：GitHub Actions第三job独立重读原192源CSV，用单独代码重算六bit长度和顺序、转移计数、精确来源质量、各单点Brier与两种尾事件、全部精确源概率和SHA256，并比较两路PMF和解析式。
必须先将本协议提交GitHub并冻结SHA，再实现无第三方包Python标准库代码，Python3.11/3.12各≥45真实单测、三job全部completed/success、原192源CSV/结果JSON/SHA256机器收据机器人永久归档后，方按**有界人工E1**正式结题。
不解释为真实人类行为的Markov证据，新增真人E2=0、真实历史E3=0；R073及PESEN v0.1继续冻结。下一原目录12-008 Model Averaging and Ensembles（拟R278），完成原R系列之后才统一归纳分类与模型熔炼。
