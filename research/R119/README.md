# R119：Watts (2002) 邻居阈值网络级联及原始分支判据

日期：2026-10-19（Asia/Taipei）。既定候选目录 P0 **04-002 Watts Cascade Model**（旧文献索引R03）。正式状态：**CLOSED_BOUNDED_WATTS_2002_ORIGINAL_NEIGHBOR_CASCADE_FINITE_GRAPH_AND_BRANCHING_THEORY**；学习验收：**LEARNING_COMPLETE_BOUNDED_WATTS_NEIGHBOR_THRESHOLD_AND_BRANCHING_ANALYTICS**。真人原始E2预测0条，R073与PESEN v0.1维持冻结。

## 原始文献和确切范围

[Duncan J. Watts (2002), PNAS 原文](https://doi.org/10.1073/pnas.082090499)，[一手原全文PMC](https://pmc.ncbi.nlm.nih.gov/articles/PMC122850/)。实读 Model Specification、Exact Solution on an Arbitrary Random Graph、Results and Discussion。原论文以每个节点**已激活邻居比例**达到自身阈值时采纳，以少量外生种子触发网络演化，激活后不退出。与R118全群体可见的**人数**阈值不同，R119明确加入真实邻接边。

本轮精确Fraction小图版本，n=1..10，严格无自环无重复的无向简单图，单种子，节点阈值(0,1]，禁止零度孤立非种子节点无来源自发激活。两套各自独立实现：同步轮次与固定顺序异步公平扫描；**最终激活成员集合一致**，但没有重现作者随机异步路径的概率分布及10,000节点随机ER网络相图。

## 数学成果

1. 六节点**路径**与**星形**都只有5条边；路径端点种子扩散至6人，星形叶节点种子只维持1人，而星形中心种子可触发6人。
2. 更强的反例：**六节点环C6**与**两个不连通三角形**均6条边，全部节点度数严格为2，单种子传播却分别激活6人和3人。相同度数分布不足以决定某个确定有限网络的实际传播路径。
3. 四节点菱形图中，节点3度为2、阈值3/4，不满足单邻居脆弱条件φ≤1/2，但两个邻居先后激活时仍可加入。早期一邻居不脆弱不等于不可能后来参与。
4. 原PNAS Eq.(5)的无限局部类树随机图数学条件可写为 R=Σ_k k(k−1)p_kρ_k / z。严格计算 R>1过临界、R<1欠临界、R=1临界边界。源文的无限随机网络**理论分支判据**不能当作某个有限图的成功概率或“必然级联”规则。

[GitHub Actions 39251971404](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39251971404) 已成功，**43项独立数学/合成单元测试全通过、0失败**。对n=1至4所有无向简单图、每人三种有理阈值1/3、1/2、2/3、所有可能初始种子**21,423种纯人工数学配置**完整穷举，两套求解器均得相同最终激活集合，全部达到固定点。代码、测试、详细报告三件套SHA256由CI机器人提交并在main回读。21,423不是人类实验数量，也未测量社会网络中实际心理门槛。

## 代码、协议与正式科学档案

- [计算前冻结协议](../../protocols/R119_WATTS_2002_NETWORK_CASCADE_EXACT_FINITE_AND_BRANCHING_PRESCORE_FREEZE_2026-10-19.md)
- [第一手来源、局部传播、无限分支判据与反例详细报告](R119_WATTS_2002_PRIMARY_NETWORK_CASCADE_FINITE_GRAPH_AND_EQ5_BOUNDED_SCIENTIFIC_REPORT_2026-10-19.md)
- [标准库Python精确数学程序](r119_watts_2002_fraction_neighbor_cascade.py)
- [43项严格单元测试](test_r119_watts_2002_fraction_neighbor_cascade.py)
- [真实GitHub CI验收机器收据](R119_PHASE_A_WATTS_2002_EQ5_AND_21423_GRAPH_SYNTHETIC_CI_ACCEPTANCE.json)
- [研究正式限定结题状态](R119_FINAL_ACCEPTANCE_STATUS.json)

复跑：`PYTHONPATH=research/R119 python -m unittest -v research/R119/test_r119_watts_2002_fraction_neighbor_cascade.py`（仅Python 3.11标准库）。

这属于真实原创理论的有界数学学习，不包括原作者整个随机图相图的复算、个体阈值校准、外部真实社交网络独立预测E2或人类社会规范因果识别。先继续R系列其他候选，全部学完后再统一分类、最后熔炼，不提前构建个人决策系统。
