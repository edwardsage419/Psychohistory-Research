# 心理史学 R254–R256：随机谱、图拉普拉斯与有限排队理论 — 原R有界E1科研验收索引

日期2026-10-23（Asia/Taipei）。本索引对应用户原239模型候选目录连续三项：11-014 Spectral Methods（R254，P2）、11-015 Graph Laplacian（R255，P2）、11-016 Queueing Models（R256，P2），全部有界有限人工E1研究已形成独立先行冻结协议、源代码、完整原结构来源CSV、独立理论路线、全原source SHA256机读收据、双Python真实CI验收与GitHub bot永久main归档、科学报告、正式结题状态。**全部原source结构类型不是真人样本，也不是历史扩散、意见共识和等待效率经验记录**。新增真人E2=0、真实历史E3=0，R073及PESEN v0.1继续冻结。用户约定先完成全部原R，再统一归纳分类，最后模型熔炼；不提前构建个人决策系统。

## R254（11-014）：有限三节点带符号随机对称邻接矩阵谱

[事前冻结协议](../protocols/R254_SPECTRAL_RANDOM_TRIANGLE_9_WORLDS_18432_COMPLETE_ATOMS_PRESCORE_FREEZE_2026-10-23.md) · [全部原来源和源码导航](../research/R254/README.md) · [完整科研报告](../research/R254/R254_SCIENTIFIC_REPORT_2026-10-23.md) · [正式验收与首次失败记录](../research/R254/R254_FINAL_ACCEPTANCE_STATUS.json) · [最终CI run39896198396](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39896198396)。

九随机矩阵world，每world独立6edgebit×3初seedbit、四时点2048完整人工源，共**18432条原source**，每条设计概率1/2048。原生整数矩阵乘法 vs 不调用matvec的独立walk完全展开三时点全部源逐状态精确相同；3×3特征多项式`λ³−(a²+b²+c²)λ−2abc`、Cayley–Hamilton也以独立行列式/矩阵检验，并以完整Bernoulli边概率独立重建九world谱期望。在三边随机开放率p=1/2的正三角与一个潜在边取−1的signed三角，**每条相同原source的谱半径平方完全一致**，都Eρ²=13/8，但预期最大代数实特征值前者`5/8+(3/8)√2`、后者`1/2+(3/8)√2`，严格差1/8；所以ρ不能替代全部特征值、正模态或社会传播机制。未研究大维随机矩阵极限定律。首次[CI run39896118162](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39896118162)两个模型job success，但独立归档审计误将CSV数字文本传给要求整数分子分母的Fraction导致整体failure；保存失败记录、仅修源审计类型转换，最终[run39896198396](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39896198396)三job success，Python3.11/3.12各83真实测试，共**166项实际通过**；全source/JSON/SHA bot永久commit[7c5cb714](https://github.com/edwardsage419/Psychohistory-Research/commit/7c5cb71403cf22308741e26720daed79f021eafb)。全人工E1。

## R255（11-015）：三节点随机图组合拉普拉斯与线性共识

[事前冻结协议](../protocols/R255_GRAPH_LAPLACIAN_9_WORLDS_18432_COMPLETE_SOURCE_ATOMS_PRESCORE_FREEZE_2026-10-23.md) · [全部原source/源码导航](../research/R255/README.md) · [正式科学报告](../research/R255/R255_SCIENTIFIC_REPORT_2026-10-23.md) · [独立科研验收](../research/R255/R255_FINAL_ACCEPTANCE_STATUS.json) · [实际成功CI run39896308708](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39896308708)。

九world每world6独立边bit、3初意见seedbit×四时点2048个完整人工原source，共**18432源点**。明确L=D−A，矩阵W=I−L/4对任意本三点无向简单图为对称非负行随机。3节点四种边数m=0,1,2,3对应Laplace实特征谱`(0,0,0)`、`(0,0,2)`、`(0,1,3)`、`(0,3,3)`；零特征根数逐mask等于BFS连通分量数，代数连通λ₂>0当且仅当图连通。独立概率公式`Eλ₂=3p²`、`P(观察图连通)=3p²−2p³`、`E components=3−3p+p³`，ER p=1/2得到Eλ₂=3/4，连接概率1/2，平均分量数13/8。逐原source四时点三维意见状态由直接W迭代与独立完全walk求和验证，平均意见保持且V=∑意见与全体原平均的平方差`V_{n+1}≤V_n`。固定连通图可从严格W非零模态谱得到最终全体平均共识；固定不连通图一般只能在连通分量内部共识，不能据有限四时点声明真实人类共识。另有“真图完全空、报告器模拟随机图”的完全sourcewise观察别名，须外部真实观测核验。最终[run39896308708](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39896308708)三job success，Python3.11/3.12各84实际单测、共**168通过**；全source/JSON/SHA bot永久commit[c823c63e](https://github.com/edwardsage419/Psychohistory-Research/commit/c823c63ede1d93570b12b3a32a78774fb1cd649d)。全人工E1。

## R256（11-016）：四时格双容量单服务台离散队列

[事前冻结协议](../protocols/R256_QUEUE_9_FOUR_BIN_CAPACITY_TWO_WORLDS_4608_SOURCES_PRESCORE_FREEZE_2026-10-23.md) · [4608完整外生源和代码导航](../research/R256/README.md) · [正式科学报告及失败CI保存](../research/R256/R256_SCIENTIFIC_REPORT_2026-10-23.md) · [独立验收状态](../research/R256/R256_FINAL_ACCEPTANCE_STATUS.json) · [最终成功CI run39896631038](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39896631038)。

九world每worldU固定类别加四格各到达/服务bit，全部512个九bit原source，共**4608个完整人工来源类型**；每source质量1/512。四格初始队长0、容量2、每格最多1到达和1服务，服务优先与到达优先定义明确，同格新任务只可在到达优先时立刻被服务。第一真实原source九bit源生成队长Q1..4 vs 第二独立按Bernoulli到达/服务构造3×3状态转移核并计算完整四格路径联合，九world逐81种可能四位队长路径严格Fraction相等；隐藏U同一期固定的world使用U条件核的混合`1/2 ΠT_U0+1/2 ΠT_U1`，绝不误用边际0.5跨期独立。所有512×9源逐格验证`Q_prev+arrival=Q_next+served+rejected`和整个四格容量守恒。两个同Bernoulli到达1/2/服务1/2世界仅更改服务先后，P(Q1=1)由1/2变1/4；相同每格边际请求1/2但U跨期固定则P(Q1=0,Q2=1)由独立模型1/4变0。首次[run39896586661](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39896586661)结果JSON将`map(str(k))`误写为错误函数参数，九个summary测试失败，3.11取消，整体failure；仅改`map(str,k)`而不改模型或冻结源，保留失败记录。最终[run39896631038](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39896631038)三job success，Python3.11/3.12各82真实单测，共**164项通过**；全部原source/JSON/SHA机器人永久归档[559ea6cf](https://github.com/edwardsage419/Psychohistory-Research/commit/559ea6cf3ee4de82c2822526dee5d04941f0372a)。**只有四格有限离散容量2模型，不是真正连续时间Poisson+指数服务M/M/1，不涉及真实客户等待时间或长期稳态。**全人工E1。

## 统一实际验收数与下一原目录

三项原R连续结题：**27个不同先冻结人工世界，18432+18432+4608=41472条完整原结构source，166+168+164=498次两个Python版本实际通过的测试**。三条最终GitHub Actions runs全部completed/success且各三个job success（共9jobs），全部来源CSV/完整结果JSON/SHA256机读凭证已bot长期main归档，科学报告/正式有界E1资格另行确认。两个先失败的CI run保留，且只采用最终完整成功测试统计。不把41472结构类型误称独立真实人类样本，也不把此三点/四格模型数学闭合冒称历史预测、因果识别或真人复现。

新增真人E2=0、历史E3=0，R073/PESEN v0.1始终冻结。原239候选目录下一条核实为**11-017 Optimization Theory（P1，拟R257）**，之后**11-018 Optimal Control（P2）**；按用户既定决策完成全部原R、最后统一分类，最终原创模型熔炼。
