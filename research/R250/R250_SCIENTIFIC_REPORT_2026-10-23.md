# R250 临界现象与相变：九个人工三节点渗流世界、576完整来源与有限图无真实相变

日期2026-10-23（Asia/Taipei）。原239目录 `11-010 Critical Phenomena`（P1）。科学资格 **`CLOSED_BOUNDED_E1_EXACT_FINITE_THREE_NODE_PERCOLATION_NO_THERMODYNAMIC_TRANSITION`**。本R是三节点人工有限键渗流及人工观察图映射的严格数学实验，**不是临界现象热力学极限的实证复现，不含真正临界概率、无限连通簇、临界指数或发散易感率**。新增真人E2=0、真实历史E3=0。

## 一手文献、方法边界与事前协议

Broadbent, S. R. & Hammersley, J. M. (1957), [*Percolation processes: I. Crystals and mazes*](https://doi.org/10.1017/S0305004100032680), *Proceedings of the Cambridge Philosophical Society* 53(3):629–641，研究随机介质中的连接与渗流机制。Scullard (2012), [*Percolation critical polynomial as a graph invariant*](https://doi.org/10.1103/PhysRevE.86.041131), *Physical Review E* 86:041131，讨论周期图格上的临界多项式。两者的理论背景并不意味着固定三节点有限图有热力学临界阈值。对任意有限图，任一边配置事件概率都是`p^k(1−p)^{m−k}`的有限项之和，是p的光滑多项式；因此本项不存在无限体系相变的非解析点，也不存在无限大的连接簇。报告仅用“有限图连通簇响应”，不命名任何p为真实临界点。

[全部九人工机制、576原来源和无相变资格的事前冻结协议](../../protocols/R250_CRITICAL_9_FINITE_THREE_NODE_PERCOLATION_WORLDS_576_ATOMS_PRESCORE_FREEZE_2026-10-23.md)先于任何程序、计算与结果提交，冻结commit [f511d839](https://github.com/edwardsage419/Psychohistory-Research/commit/f511d8390c4d7439ad14a5315447b335af9df26c)。所有比较指标与独立概率公式预定，没有事后选出某一经验阈值。

## 三节点、三潜在边、六原bit与两独立路线

三个标记顶点为0、1、2，固定根顶点0，潜在无向边e01、e02、e12。每边对应两独立公平原bit，组合为R∈{0,1,2,3}均匀；对于图拓扑允许的边，按`edge_open iff R<4p`独立开边，不在拓扑内的边则始终禁用。每world**64种完整六位原来源**、各源权重1/64；九world总**576人工完整源结构类型**，不是实际社交节点观测数或历史案例数。每行保存原六bit、观察三边开闭Y01/Y02/Y12、报告根连通簇大小Cobs、oracle真物理边H和真实根簇Ctrue。

第一路线从完全原六位源抽取观察边配置，再用图搜索BFS计算根0实际能到达的顶点数量，按源权重积分出完整三位边掩码联合分布及根簇大小1、2、3的分布。独立第二路线**不读取源CSV或调用BFS**，直接从有限独立Bernoulli边配置的乘积概率`p^k(1−p)^{m−k}`构造完整三位观察边概率，并使用事前闭式多项式直接重算根簇大小分布。九world全部结果逐格Fraction相等，另通过解析微分计算根簇平均大小随p变化的有限斜率。

九world如下：CHAIN_P_QUARTER/CHAIN_P_HALF/CHAIN_P_THREE_QUARTER（仅有边01和12，p分别1/4、1/2、3/4）；TRIANGLE_P_ZERO/P_QUARTER/P_HALF/P_THREE_QUARTER/P_ONE（三条边全部允许且p分别0、1/4、1/2、3/4、1）；TRIANGLE_STATIC_TRUE_GRAPH_REPORT_ALIAS（真实物理三边全闭，但报告器按TRIANGLE_P_HALF同一原六bit人工生成虚拟观察边）。

## 两种拓扑的完整解析概率公式

**三节点链0—1—2：**
[
P(C_0=1)=1-p,quad P(C_0=2)=p(1-p),quad
P(C_0=3)=p^2,
]
[
E[C_0]=1+p+p^2,quad {d E[C_0] over dp}=1+2p.
]
根0要连到2必须依次有01与12两条边，都独立开放，因此三节点全连接p²。

**三节点三角形：** 根0与节点1的连接既可通过直接边01，也可通过02再12，因此`P(0↔1)=p+(1−p)p²`，对节点2对称。三节点全部连通至少有三边中两条开放，故
[
P(C_0=1)=(1-p)^2,quad
P(C_0=2)=2p(1-p)^2,quad
P(C_0=3)=3p^2-2p^3,
]
[
E[C_0]=1+2p+2p^2-2p^3,quad
{dE[C_0]over dp}=2+4p-6p^2.
]
这些公式都是有限低阶多项式，在p∈[0,1]光滑无奇点，且无论p如何变化都严格有`1≤C_0≤3`。这里的平均根簇规模只是有界有限图统计量，不可不加定义地叫无限体系临界易感率。

## 九world精确结果和反例

| 冻结人工拓扑/连边概率 | E[根簇规模] | P(根簇含全部三节点) |
|---|---:|---:|
| 链 p=1/4 | 21/16 | 1/16 |
| 链 p=1/2 | 7/4 | 1/4 |
| 链 p=3/4 | 37/16 | 9/16 |
| 三角 p=0 | 1 | 0 |
| 三角 p=1/4 | 51/32 | 5/32 |
| 三角 p=1/2 | 9/4 | 1/2 |
| 三角 p=3/4 | 89/32 | 27/32 |
| 三角 p=1 | 3 | 1 |
| 三角虚拟报告 p=1/2、真物理无边 | 可见9/4，真恒1 | 可见1/2，真0 |

**同一键率p，网络拓扑就能改变连通规模。** 在p=1/2时，链平均根簇大小7/4、全三节点连通率1/4，三角平均9/4、全连通率1/2。这一差别完全来自是否存在第三条替代路径边02，并非p差异，也不是任何现实社交网络的自激证据。预冻结完整64来源和闭式公式两路一致。

**观察曲线增长不是无限体系相变。** 三角模型的全连接概率从p=1/4时5/32上升到p=1/2时1/2，再升至p=3/4时27/32，表现为随边概率上升的有限平滑连通增强。但是其公式`3p²−2p³`及其导数对所有p都是解析多项式，没有任何非解析跳跃/无限簇；`p=1/2`恰使全连通概率1/2**不等于**真实无限格子临界阈值。链/三角同p=1/2时平均根簇斜率分别2及5/2，斜率仍有限。

**完整观察网络也不能自动证明隐藏真实物理图相同。** TRIANGLE_P_HALF的真边与观察边完全相同；TRIANGLE_STATIC_TRUE_GRAPH_REPORT_ALIAS的真隐藏三边全部关闭，真实根簇恒为1，但人工报告器生成和TRIANGLE_P_HALF在相同全部64原六bit上**逐来源完全相同的观察三边与观察根簇**，因此全部可见联合统计相同。此别名需要“报告器可生成虚构连边且无独立真图校验”的严格假设；拥有可信网络测绘/实证真值便可打破别名。不能凭此人工反例断言历史中的群体网络不存在。

## CI实际成功、原来源与SHA审计

[原生Python Fraction+BFS及独立多项式源码](r250_exact_finite_bond_percolation.py) · [576全部原六bit边来源CSV](R250_ALL_576_ORIGINAL_THREE_NODE_EDGE_SOURCE_ATOMS.csv) · [九world全部边/根簇分布、解析斜率JSON](R250_EXACT_RESULTS.json) · [原CSV与结果SHA256机器收据](R250_FINAL_MACHINE_ACCEPTANCE.json)。

[GitHub Actions run39894296482](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39894296482)总体completed/success、三job均completed/success，Python3.11和3.12运行日志各`Ran 84 tests`、`OK`，共**168次真实双版本测试通过**。第三独立档案作业逐条核验九world×64唯一原六bit、各源概率1/64、每world全观察边PMF和根簇PMF质量1、闭式链/三角期望及全连接概率、解析响应导数、真隐藏图伪报告别名和SHA256，并实际输出`R250_ALL_576_THREENODE_BOND_ORIGINAL_SOURCES_AND_NO_PHASE_TRANSITION_VERIFIED`。GitHub bot将全CSV、结果及SHA机器收据永久归档main，提交[2634b5eb](https://github.com/edwardsage419/Psychohistory-Research/commit/2634b5ebc4887d70939b86a5cd5e808cce28a620)。

原CSV SHA256 `b964b44a23d77e985d95e19487b1f7bc7dae8c076edda1dd4a3b06f3c2a9b636`，结果JSON SHA256 `e35e87903f4a8c5aee8fafa4807e4c10c3f28efd8d26a89f88d6c2e338880d72`。

最终科研状态只能为`CLOSED_BOUNDED_E1_EXACT_FINITE_THREE_NODE_PERCOLATION_NO_THERMODYNAMIC_TRANSITION`；未对真实自然网络/历史社群、临界指数、无限图阈值、系统尺寸外推或真实相变进行验证。新增真人E2=0、历史E3=0，R073和PESEN v0.1继续冻结。下一个原目录`11-011 Lyapunov Stability`（拟R251，P2），继续先完成全部原R，再统一归纳分类，最后熔炼。
