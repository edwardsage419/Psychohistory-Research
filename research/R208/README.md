# R208 网络中心性：1024人工五节点图的全来源E1结题

日期2026-10-22。原239目录P1/08-032 Network Centrality。**CLOSED_BOUNDED_E1_ARTIFICIAL_BOND_CENTRALITY**。

[原评分前冻结协议](../../protocols/R208_NETWORK_CENTRALITY_1024_GRAPHS_118098_BOND_SOURCES_PRESCORE_FREEZE_2026-10-22.md) · [科学报告](R208_SCIENTIFIC_REPORT_2026-10-22.md) · [全世界结果JSON](R208_EXACT_RESULTS.json) · [2048图×p四模型评分原CSV](R208_ALL_2048_GRAPH_P_SEED_RANKING_WORLDS.csv) · [118098全来源激活边状态和五种子触达CSV](R208_ALL_118098_ORIGINAL_BOND_ACTIVATION_SOURCES.csv) · [三个文件真实SHA机器验收](R208_FINAL_MACHINE_ACCEPTANCE.json) · [正式有界结题机读记录](R208_FINAL_ACCEPTANCE_STATUS.json) · [原生Python与40项测试](r208_exact_network_centrality.py)。

带标号五节点的全部1024张无向图，固定独立边激活概率p=1/4或3/4，共2048个图×p人工世界。完整118098条活跃边源及原Fraction概率真正全部保留。对每个固定图，四种只看图结构的中心性DEGREE/HARMONIC/BETWEENNESS/KATZ α=1/8分别选出一个种子节点，传播结果定义为独立随机活跃边子图中包含该种子的无向连通分量人数，由BFS和UnionFind逐来源完全一致。Freeman最短路全部简单路径分数、Fraction Katz消元与固定点公式经原测试核对。

预冻结果在本**特定五节点×两个概率**完备来源中，KATZ四模型比较中**2048/2048**图×p世界都选中至少一个正确oracle种子，平均regret=0；HARMONIC为989/1024，DEGREE为949/1024，BETWEENNESS为229/256。只有边12的图中BETWEENNESS全节点零分按tie选择孤点0，真实传播oracle取1或2。KATZ结果**不等于**所有p、网络规模、真实社交影响下的普遍规律。

[GitHub Actions run39731679240](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39731679240) Python3.11/3.12各40项、合计80通过，第三完整118098原来源永久归档作业success。[原数据机器人提交40a45828](https://github.com/edwardsage419/Psychohistory-Research/commit/40a458287e7144605f63a2573f003c60a42b1882)。

该研究只有人工图论E1，新增真人E2=0、历史E3=0，R073及PESEN v0.1仍冻结。下一 **R209 P2/08-033 Diffusion of Innovations**，继续完成全R模型后统一分类、最后熔炼。
