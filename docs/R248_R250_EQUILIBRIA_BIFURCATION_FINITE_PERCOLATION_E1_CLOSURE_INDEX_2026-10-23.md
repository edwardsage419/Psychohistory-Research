# 心理史学 R248–R250：固定点、分岔、有限渗流的连续原目录有界研究正式结题索引

日期2026-10-23（Asia/Taipei）。用途：当前GitHub `main` 原239模型候选序列中11-008至11-010的完整原来源、预评分冻结、源计算、真实CI和正式结题证据导航。**所有结果仅严格人工数学E1**，结构原来源只是给定方程/图所有指定组合，不是人类样本、历史资料、自然群体临界参数、真实测量或实证预测。本轮不变更R073与PESEN v0.1冻结。用户既定研究顺序保持：先完成全部原R系列学习/有界研究、再统一分类、最后模型熔炼。

## R248 = 11-008 Dynamical Systems Equilibria（P1）

[先行九模型冻结协议](../protocols/R248_EQUILIBRIA_9_RATIONAL_MAP_WORLDS_405_IVP_TIME_SOURCES_PRESCORE_FREEZE_2026-10-23.md) · [全部405初值/时点原source和源码](../research/R248/README.md) · [科学报告](../research/R248/R248_SCIENTIFIC_REPORT_2026-10-23.md) · [正式科研状态](../research/R248/R248_FINAL_ACCEPTANCE_STATUS.json) · [实际成功CI run39893826278](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39893826278)。

九人工1D自治离散映射，9有理初值×5时点，每world45，共**405完整人工原source点**。逐步递推与**不读取原source的独立形式多项式复合、Horner求值及解析导数**逐source准确相等，4步限制内自治半群全满足。完整精确固定点及f′乘子表区别超曲吸引、排斥、非双曲线性不足以及恒等映射“所有实数皆固定”。Logistic r3的x*=2/3乘子-1，却由`f²(2/3+y)-2/3=y[1-y²(18+27y)]`、0<|y|≤1/12时严格二步收缩及极限证明**局部渐近吸引**。Cubic`f=x−x³`零固定点乘子+1，在0<|x|<1也严格局部吸引；identity同乘子却不会对某一固定点吸引邻点。Logistic r4的3/4虽固定乘子-2局部排斥，x0=1/4仍恰到达此前像，因此有限不动轨道不是吸引证据。真实CI三job success，Python3.11及3.12各84单测，共**168实际通过**；原CSV/完整JSON/SHA机器人永久提交[10068ac1](https://github.com/edwardsage419/Psychohistory-Research/commit/10068ac15ec8a1f74b5dd9c2e7fb03db16a4af96)。无真实E2/E3。

## R249 = 11-009 Bifurcation Theory（P1）

[计算前五Logistic+四fold参数冻结协议](../protocols/R249_BIFURCATION_9_RATIONAL_PARAMETER_WORLDS_405_ORIGINAL_ATOMS_PRESCORE_FREEZE_2026-10-23.md) · [405全部参数原source/原生Python/机读收据](../research/R249/README.md) · [完整科学报告](../research/R249/R249_SCIENTIFIC_REPORT_2026-10-23.md) · [正式科研状态](../research/R249/R249_FINAL_ACCEPTANCE_STATUS.json) · [实际成功CI run39894061461](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39894061461)。

九人工有理参数机制，9初值×5时点各45，共**405完整人工来源点**。Logistic家族`f_r=r x(1−x)`的固定0、1−1/r两支在r=1交会成代数重根0，其局部乘子分别r和2−r，固定点发生稳定性交换；有理冻结r∈{1/2,1,2,3,4}全部逐项核验，r=1/2的第二固定点−1不在常见人口比例[0,1]内。fold家族`f_μ=x+μ−x²`根`μ−x²=0`在μ<0无实根、μ=0只有重根0、μ>0产生两个实根，冻结μ∈{−1/4,0,1/4,1}计算分离及乘子全对。r=1与μ=0的非双曲固定0在右侧吸引、左侧排斥。对r3正固定点2/3及fold μ=1正固定点1，分别用非线性二次迭代严格多项式证书`y−18y³−27y⁴`和`y−2y³−y⁴`证明**乘子−1仍可局部渐近吸引**，邻域因子缺口均≤9/64；严格区分此解析局部数学结论与任何完整周期翻倍或实际历史分岔预测。真实CI三个job success，Python3.11及3.12各85单测、共**170次实际通过**，原CSV/JSON/SHA机器人永久提交[193cc657](https://github.com/edwardsage419/Psychohistory-Research/commit/193cc6576d9cd93748bb3c518d27ae6e91f621fa)。无真实E2/E3。

## R250 = 11-010 Critical Phenomena（P1）：三节点有限键渗流**不是真实临界相变**

[计算前九有限网络世界及禁止临界过度主张冻结协议](../protocols/R250_CRITICAL_9_FINITE_THREE_NODE_PERCOLATION_WORLDS_576_ATOMS_PRESCORE_FREEZE_2026-10-23.md) · [576完整六bit原图source/概率计算程序](../research/R250/README.md) · [科学报告/与真正热力学相变界限](../research/R250/R250_SCIENTIFIC_REPORT_2026-10-23.md) · [正式科研状态](../research/R250/R250_FINAL_ACCEPTANCE_STATUS.json) · [实际成功CI run39894296482](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39894296482)。

九world都是只有三节点和三条潜在无向边的人工概率图，每world6独立公平二元源、全部64原组合，共**576完整人工结构源**。原source基于两bit阈值独立开边，BFS计算从根0出发的有限簇大小；独立于source/BFS的完整Bernoulli边模式乘积概率及链/三角簇大小封闭多项式与原source所有分布严格相同。链`E C_0=1+p+p²`、`P(C_0=3)=p²`；三角`E C_0=1+2p+2p²−2p³`、`P(C_0=3)=3p²−2p³`。p同=1/2时，链平均簇7/4、三角9/4，三节点全连通分别1/4、1/2；拓扑差异本身改变连通。所有概率是低阶光滑多项式，`1≤C_0≤3`，**有限图不能展示真实无限体积非解析临界点或临界发散，p=1/2不是本项证明的临界阈值**。TRIANGLE_P_HALF与真实隐藏物理图无任何边却由报告器模拟相同边的机制，逐源完整可见网络等价；该别名需允许人为伪网络观测，不是现实社会传播是否真实的证据。真实CI三job success，Python3.11/3.12各84单测共**168次实际通过**；全部原CSV/JSON/SHA机器人永久提交[2634b5eb](https://github.com/edwardsage419/Psychohistory-Research/commit/2634b5ebc4887d70939b86a5cd5e808cce28a620)。无真实E2/E3。

## 本轮统一验收统计和下一目录

原239候选目录11-008、11-009、11-010的**三项独立有界研究正式结题**；**9×3=27个不同预评分冻结人工世界**，**405+405+576=1386个完整原结构类型**，**168+170+168=506次两个Python版本真实通过的单测**。本轮三条最终GitHub Actions run总体和全部9个子jobs均success；每项有独立先提交的协议、原生源代码、实际全源CSV、独立数学复算、完整机器SHA256凭证、原source永久归档、正式报告和科研结题状态。**1386不是实际历史人物、真实社会数据、无限网格样本或任何实证相变参数。** 新增真人E2=0、历史E3=0，R073及PESEN v0.1依旧冻结。

经原239目录此前核对，下一条是**11-011 Lyapunov Stability（P2），拟R251**，再后需核实11-012；遵守用户选择的原R全部优先完成、再统一分类、最后原创熔炼，个人辅助决策系统继续暂缓。
