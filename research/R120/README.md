# R120：Kempe、Kleinberg、Tardos（2003）线性阈值扩散与活边模型概率等价

日期：2026-10-19（Asia/Taipei）
原有239候选模型目录：P0 / 04-003 Linear Threshold Diffusion。
**正式科研状态：CLOSED_BOUNDED_KKT_2003_UNIFORM_RANDOM_LINEAR_THRESHOLD_AND_LIVE_EDGE_MATHEMATICS；限定学习验收：LEARNING_COMPLETE_BOUNDED_KKT_2003_UNIFORM_LINEAR_THRESHOLD_AND_LIVE_EDGE_EQUIVALENCE。**
此结题只表示原作者2003年公开理论中的LT机制、活边等价与小图期望次模性质获得独立有理数数学验证，并不意味着整篇论文实验性能或真人社会行为实证已经被重跑。R073和PESEN v0.1维持冻结。

## 第一手资料

[Kempe, Kleinberg & Tardos (2003) 原始SIGKDD论文](https://doi.org/10.1145/956750.956769)，[Cornell作者本人发布的原刊PDF](https://www.cs.cornell.edu/home/kleinber/kdd03-inf.pdf)，本轮直接阅读其PDF第2页基本扩散模型和PDF第4-5页Theorem 2.5、Claim 2.6与证明。作者规定有向图u→v的每条边影响权重b(v,u)非负且每节点全部入边权重和≤1，每个节点独立只抽一次Uniform[0,1]门槛，累计已激活邻居入边权重到门槛才采纳，采纳后不退出。

2003原论文的Claim 2.6证明上述随机过程与“每个目标节点以入边权重为概率随机选择至多**一条进入自己的活边**，或选择无活边”的有向可达集合具有**完全相同的最终活跃节点集合分布**。这不代表现实人物只选择一个朋友，也不允许把每条进入v的边独立随机为活边。原作者Theorem 2.5关于**期望**最终激活人数σ(A)的次模性不同于一个固定门槛样本的个别激活人数；后一函数不一定次模。

## 真实可执行成果

R120实现了两个独立有理数概率算法：
- 按每人所有入边权重子集和划分连续Uniform门槛可能区间；每区间概率长度严格为Fraction，再调用确定性阈值闭包，得所有终态集合及其精确质量。
- 独立枚举“每节点至多一条进来的活边或没有”的分支及其权重，直接算从初始种子经活边可达的节点集合；算法没有调用第一个过程。

因此输出接受的是逐个终态节点集合的**完整概率分布**而非只比较平均规模。

真实CI [GitHub Actions run 39254086771](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39254086771) 已success：**45项数学/合成单元测试全部通过；0失败。** 另外对n=1、2、3所有有标签无自环有向简单图分别1、4、64种、按目标入度平均分配权重1/d_in、每图所有初始种子集合，总计**530组有向图与初始种子**逐个核实随机Uniform门槛与活边的**完整终态分布Fraction严格相等**，同时检查这些小图的期望影响σ具有单调性与次模性。530均为源外生成的数学案例，绝不是530个真人群体。

冻结解析数值：三节点0→2权重1/2、1→2权重1/4时，种子{0}/{1}/{0,1}的期望激活数分别**3/2、5/4、11/4**；四节点有向链条期望25/12；三节点有向环期望7/4。另本研究自建确定门槛非次模反例：两种子都不单独触发高门槛目标，但合力可以，固定门槛最终规模为空0、单种子各1、双种子3；Uniform门槛下期望边际收益回归为1.5、1.5而不违反次模。此反例是数学机制，不是2003原文真人样本。

## 研究文件与证据分层

- [源文、样本、机制和独立算法的计算前冻结协议](../../protocols/R120_KEMPE_KLEINBERG_TARDOS_2003_LINEAR_THRESHOLD_DISTRIBUTION_EQUIVALENCE_FREEZE_2026-10-19.md)
- [第一手论文、完整分布定理及非次模反例科研报告](R120_KKT_2003_LINEAR_THRESHOLD_LIVE_EDGE_DISTRIBUTION_EQUIVALENCE_SCIENTIFIC_REPORT_2026-10-19.md)
- [标准库精确Fraction概率双求解器](r120_kkt_2003_uniform_linear_threshold_exact.py)
- [45项真正运行的数学与失败反例测试](test_r120_kkt_2003_uniform_linear_threshold_exact.py)
- [GitHub Actions独立回写的原始SHA256与机器验收](R120_PHASE_A_45_UNIT_530_FULL_DISTRIBUTION_CI_ACCEPTANCE.json)
- [正式科研结题范围](R120_FINAL_ACCEPTANCE_STATUS.json)

复算：`PYTHONPATH=research/R120 python -m unittest -v research/R120/test_r120_kkt_2003_uniform_linear_threshold_exact.py`，Python 3.11原生标准库。

**边界**：未复现2003论文合作网络真实数据或作者贪心最大化实验，真人行为独立预测E2仍0项，没有证明独立门槛、权重和网络结构真实可观测或因果识别，更未产生现实长期历史事件概率预测。R118、R119、R120属于不同明定范围的数学研究，不在本阶段统一分类或融合；先完成既定全部R系列后再统一归类、熔炼。
