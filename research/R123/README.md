# R123：DeGroot(1974)共识模型及Berger(1981)必要条件纠错的正式限定验收

日期：2026-10-19（Asia/Taipei）。原239候选目录 **P0 04-009 DeGroot Consensus Model**。
**科学状态：CLOSED_BOUNDED_ORIGINAL_DEGROOT_1974_BERGER_1981_CORRECTED_CONSENSUS_AND_EXACT_INFLUENCE**。
**学习状态：LEARNING_COMPLETE_BOUNDED_DEGROOT_1974_BERGER_1981_STRUCTURE_VS_INITIAL_CONSENSUS**。真实人类个体预测E2新增0；R073/PESEN v0.1冻结。

## 本轮真正核阅的一手来源及重要后续学术纠错

1. [Morris H. DeGroot (1974), *Reaching a Consensus*, JASA 69(345):118–121](https://doi.org/10.1080/01621459.1974.10480137)，[UC San Diego托管JSTOR原印刷四页全文](https://pages.ucsd.edu/~aronatas/project/academic/degroot%20consensus.pdf)。**直接视觉审阅原印刷118–121四页**，包括原(2.1)、(3.3)、(4.2)、Theorems1–3及原p120的2×2和3×3数字。原始讨论是每个人的主观概率**分布函数**F_i经固定行随机矩阵做加权池化；标量意见x_i是作者§7允许的特殊情况，不是原论文的全部对象。
2. [Roger L. Berger (1981), *A Necessary and Sufficient Condition for Reaching a Consensus Using DeGroot's Method*, JASA 76(374):415–418](https://www.cse.cuhk.edu.hk/~cslui/CMSC5734/degroot_method-berger_jasa81.pdf)。**直接核阅415–417页**，包括Theorem2。1981论文纠正原1974文章的重要逻辑错误：**矩阵幂所有行趋同并非某一具体初始主观分布最终一致的必要条件**。它能保障任意初始意见最终共识，但即使网络含多个封闭类或周期，特殊初始意见仍可能自始或最终一致。本阶段忠实引入后续修正，**没有**把原始论文中过强的必要性陈述当已证明的正确命题，也没声称实现1981原论文关于任意概率分布全部定理。

## 主要数学结果

DeGroot原印刷第120页的两人矩阵W=((1/2,1/2),(1/4,3/4))的长期影响权重精确为**π=(1/3,2/3)**。项目选定初值(0,1)，则长期共同意见**2/3**，并非初始算术平均**1/2**。原印刷的三人扩展矩阵W=((1/2,1/2,0),(1/4,3/4,0),(1/3,1/3,1/3))长期权重为**(1/3,2/3,0)**，第三人是暂态，其初始意见即使取9也不影响长期c=2/3。**以上W与π是1974原作者理论算例，初始数值是本项目自定的数学输入，不是人类实验。**

严格分开三类问题：
- **U：对任意初始意见保证全体共识**：正权图恰有一个封闭强连通常返类，且周期=1。整张图无需处处强连通，其他节点允许暂态。
- **C：对任意初始意见保证每人分别收敛**：每个封闭常返类均无周期，可以有多个封闭类；C不代表各人最后相同。
- **S：给定此一初始意见实际达成共同意见**：不必满足U。交换W=((0,1),(1,0))配初值(0,1)永远交替、没有极限，但配(1/2,1/2)则永远相同；I2两个各自吸收成员从(0,1)出发各自收敛却永远不同，而从两人均(1/2,1/2)出发则永远相同；W=((1,0),(1/2,1/2))不强连通却对任意初始意见最终被第一人意见主导。这是**项目自构**用于正确理解Berger修订意义的极小反例。

更重要的认识：**达成共识不意味着意见正确、每人初始影响力平等或个体偏好与社会效应已被因果识别**。原1974作者明确设定无外部直接观测真值，当前本研究亦没有真实观察到的个人意见时间序列。

## 互相独立的结构、影响力、数学验收

标准库Python Fraction程序实现：(a)直接按轮次乘行随机W及严格凸包/意见差不增加检查；(b)完全独立的正权网络communicating classes、closed recurrent classes与周期gcd分析，以图区分U/C；(c)精确线性方程Gauss–Jordan求左稳态π；(d)不调用高斯的独立Markov链有向入树组合求π；(e)独立布尔正边矩阵幂识别原1974 Theorem1 **存在至少一列全正**的充分证书。

原n≤3行随机矩阵有界枚举：每行可以是单点权1，或任意两点各1/2，共n1=1、n2=9、n3=216，**226个纯数学矩阵**。经两个独立长期影响π算法与网络结构判据交叉核验：本次枚举中**176个具有普遍共识保证**，**202个每人对任意初始意见均各自收敛**；这些占比不属于真实社会参与人群的估计或经验概率。n1..3的特定有限图族用最多12次布尔矩阵幂检验原文章的“全正列”充分证书，并与独立U结构判定一致；没有据此宣称m=12是一般大图的普适上限。

**GitHub Actions [39263259641](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39263259641) success：58项独立标准库数学/合成测试全通过，0失败，226个合法矩阵穷举与两算法π独立核验成功**。源码、测试和正式报告的SHA256机器收据已由GitHub Actions直接回存main、连接器独立回读；真人个体E2=0。

## 档案路径与可复算方式

- [事前冻结一手文献与结构/初值判据](../../protocols/R123_DEGROOT_1974_BERGER_1981_CONSENSUS_STRUCTURE_AND_INITIAL_OPINIONS_FREEZE_2026-10-19.md)
- [完整1974及1981原文核阅与两类共识问题科研报告](R123_DEGROOT_1974_BERGER_1981_ORIGINAL_CONSENSUS_AND_INFLUENCE_SCIENTIFIC_REPORT_2026-10-19.md)
- [标准库原生精确Fraction程序](r123_degroot_1974_berger_1981_exact_consensus.py)
- [58项数学与失败边界测试](test_r123_degroot_1974_berger_1981_exact_consensus.py)
- [真正GitHub Actions CI结果、226矩阵统计及源码SHA256](R123_PHASE_A_ORIGINAL_DEGROOT_BERGER_58_TEST_226_MATRIX_CI_ACCEPTANCE.json)
- [正式结题科学范围及未建立实证E2](R123_FINAL_ACCEPTANCE_STATUS.json)

复算指令：PYTHONPATH=research/R123 python -m unittest -v research/R123/test_r123_degroot_1974_berger_1981_exact_consensus.py。

**限制**：没有复现Berger对任意初始主观分布F的最一般充分必要定理全文，也没有真人长期重复社会意见轨迹数据、估计W的独立误差界、动态网络真实制度约束或任何历史概率预测。研究顺序严格保留：先完成既定全部R系列候选学习，之后统一归类分类，最后熔炼；本轮未改变R073与PESEN v0.1。
