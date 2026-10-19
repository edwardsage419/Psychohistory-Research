# R124：同质性网络模型（Homophily）——人口基线、机会结构与三种生成途径

日期：2026-10-19（Asia/Taipei）。原239候选目录P0 04-015 Homophily Models。
**科研状态**：CLOSED_BOUNDED_FIRSTPARTY_HOMOPHILY_MEASUREMENT_OPPORTUNITY_AND_SYNTHETIC_CAUSAL_AMBIGUITY。
**限定学习验收**：LEARNING_COMPLETE_BOUNDED_HOMOPHILY_FIRSTPARTY_BASELINE_MEASUREMENT_AND_SYNTHETIC_NONIDENTIFICATION。
**真人原始网络逐人E2新预测成绩=0**。R073及PESEN v0.1保持冻结。

## 第一手文献范围

- [McPherson, Smith-Lovin, Cook (2001), *Birds of a Feather: Homophily in Social Networks*](https://doi.org/10.1146/annurev.soc.27.1.415)，[Penn大学所托原刊扫描全文](https://ndg.asc.upenn.edu/wp-content/uploads/2016/04/McPherson-2001-ARS.pdf)。本期真正阅览原印刷**415–419页**并可视检查419页。原作者区别因潜在关系人口构成产生的**baseline homophily**与超出机会集合的**inbreeding homophily**；419页脚注明确指出即使超出人口基线，也可能来自组织/生活场所/结构，而不一定是个人主动偏好。
- [Newman (2003), *Mixing Patterns in Networks*](https://doi.org/10.1103/PhysRevE.67.026126)，[原Phys Rev E全文扫描](https://pdodds.w3.uvm.edu/research/papers/others/2003/newman2003e.pdf)。核读原刊第**026126-2页**Eq.(1)–(3)的类别混合矩阵e_ij及有理式r，进行可视核查。a_i是**边端份额**而非总人口类别比例，分母为0时必须标未定义。
- [Kossinets & Watts (2009), *Origins of Homophily in an Evolving Social Network*](https://doi.org/10.1086/599247)，[作者所属Google Research公开摘要](https://research.google/pubs/origins-of-homophily-in-an-evolving-social-network/)。本期**只核实一手出版社及作者摘要**，作者报告新的相似关系形成与triadic closure/focal closure机会约束共同作用。原2009论文全文回归表和真人大学纵向记录均未获得，故没有进行独立人类网络数据实证复算。

## 真正算出的数学结果

全部样例均为本项目自行构造的**匿名合成网络**，不是引自原论文的人类关系记录。对无向简单图两个类别，使用两套完全独立的Fraction算法计算：
1. 直接按Newman2003 Eq.(2)构建每条边的两个有向半边类别混合矩阵，r=(Σ e_ii−Σ a_i²)/(1−Σ a_i²)。
2. 不调用矩阵算法，独立统计无向同标签边比例S、A与B类别的degree/stub份额，再计算同一个r。严格校验S、端点份额与r都相等。

预设例子：n6中两个各自完整三角形、成员标签AAA BBB，所有6条边同类别，**S=1、r=1**；同标签六节点环C6有4条同类边、2条跨类别，**S=2/3、r=1/3**；同标签K3,3完全二部网络则r=**−1**。

更有价值的分母和基线反例：标签**AAAAAB**的六节点完全网络K6，有10/15条边同类，原始S=**2/3**，但全人群“两个不同成员等概率抽取”的人口机会基线也恰为**2/3**，所以与该明确机会基线相比没有超额相似；然而Newman端点独立基线为13/18，对应r=**−1/5**。这**不矛盾**：人口无放回随机pair与Newman的边端独立零模型不同，不能互换。如果观测网络中只A–A边而B节点均孤立，S=1但所有活跃边端为A，Newman r分母0，必须报告None未定义，不能输出“完美r=1”。

## 为什么真实机会集合很重要

固定相同AAA BBB两组三角形网络作为观测结果S_obs=1：
- 若假设**全6人中任何不同二人都有等价形成关系机会**，15个潜在pair只有6个同类，基线B_pop=6/15=**2/5**，所谓超额S_obs−B_pop=**3/5**。
- 若存在两个互不交流的三人活动场所，每个仅允许三人彼此联系，潜在关系全集刚好是原两个三角形6条边，机会同类基线B_foci=1，超额**0**。结果完全一样，变化的是“真正风险集允许形成的关系”。

为示范有限人口随机分配类别的可复算null，在保持两组三角形边固定时，A和B各3人的C(6,3)=**20种**可能标签分布中，只有**2种**使全部6条边同类，其余**18种**只给2条同类边。假设20种等概率交换、预定观察6条同类边的理论右尾质量是**1/10**；这是人工样例的纯数学条件概率，**不是2001/2009人类研究的p值**，尤其不能忽略真实类别与社区机会的相互制约。

## 相同终态下三种不同历史（机制不可识别教学反例）

该固定网络加最终标签AAA BBB的**同一个完整可观察快照**可以由三种项目自造、明确不同的产生路径构造：

1. 关系选择：同类属性先存在，在15个所有潜在pair中只挑出6条同类边，形成两组三角形。
2. 接触机会：属性先存在，但各自组织只允许3人内部相互接触，全部6个可行pair自然形成两三角形，不需要任何人有同质偏好。
3. 社会影响：两组三角形关系一开始便已存在，初始属性A,A,B以及B,B,A混合。项目设定**一次包含本人在内的本地三人多数更新**，群内多数使终态变为AAA BBB，关系始终不变。这是项目原创数学toy，而不是任何原作者2009实测机制。

三条路径最终产生**同样的6条边、同样的6个标签、同样S=1/r=1**，但生成原因并不相同；仅凭横截面无法区别选择、机会及影响。该证明**不意味着三种现实机制同样常见、也不能在纵向独立实验中被区别**。要实证识别，必须真实观测不同时刻的属性、联系机会、形成与消失的关系、接触与结果，并准备对照模型与独立预测。

## 实际机器验收和研究文件

[GitHub Actions run 39277478470](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39277478470) **success：56项实际unit tests全部通过，0失败**。另遍历全部n=2..4简单无向网络结构乘二元A/B标签混合，合计**948个人造配置**；其中空边不可算r的22个被明确保留，另外**926个非空图**经两套独立算法核验相同完整Fraction S、端点边际与r（含r未定义情形）。另验证20种完整随机标签分配、两种接触机会基线及三条自造的因果历史。**机器由真实CI回写程序/测试/报告三个文件的SHA256收据，仓库main再独立读取核验**。

- [计算前研究冻结和科学约束](../../protocols/R124_HOMOPHILY_FIRSTPARTY_BASELINE_ASSORTATIVITY_OPPORTUNITY_AND_NONIDENTIFICATION_FREEZE_2026-10-19.md)
- [第一手文献范围、Newman公式、机会与选择因果反例报告](R124_FIRSTPARTY_HOMOPHILY_NEWMan_2003_BASELINE_OPPORTUNITY_SYNTHETIC_IDENTIFICATION_REPORT_2026-10-19.md)
- [独立数学程序](r124_homophily_baseline_assortativity_causal_ambiguity.py)
- [56项可复现单元测试](test_r124_homophily_baseline_assortativity_causal_ambiguity.py)
- [GitHub Actions机器收据与文件SHA256](R124_PHASE_A_HOMOPHILY_56_TEST_948_GRAPH_20_PERMUTATION_CI_ACCEPTANCE.json)
- [正式科研结题状态](R124_FINAL_ACCEPTANCE_STATUS.json)

复跑（Python 3.11标准库）：PYTHONPATH=research/R124 python -m unittest -v research/R124/test_r124_homophily_baseline_assortativity_causal_ambiguity.py 。

**证据边界**：一手概念/统计指标E1与原创数学反例成立；原始人级纵向关系记录E2=0，新真实因果效应E3=0。2009原论文完整实证回归未复算；不可据r、同类占比或合成标签置换得出真实个体选择或影响强度。按照用户研究顺序，继续完成既定R系列其余模型学习，统一分类与熔炼后置。R073及PESEN v0.1始终冻结。
