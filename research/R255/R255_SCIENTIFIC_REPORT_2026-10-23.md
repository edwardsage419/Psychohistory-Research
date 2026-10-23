# R255 图拉普拉斯算子：九人工三点随机图、18432完整原来源与代数连通度/线性共识严格界限

日期2026-10-23（Asia/Taipei），原239目录`11-015 Graph Laplacian`（P2）。正式资格`CLOSED_BOUNDED_E1_FINITE_THREE_NODE_RANDOM_GRAPH_LAPLACIAN_CONSENSUS`。研究仅对三节点无权无向随机图、人工二元初值和离散线性平均算子进行精确数学计算，没有真人E2、真实历史E3或大规模网络极限经验验证。R073及PESEN v0.1冻结。

## 经典图谱依据与直接有限界限

Fan R. K. Chung, *Spectral Graph Theory* (1997), [American Mathematical Society CBMS 92](https://doi.org/10.1090/cbms/092)，研究图拉普拉斯谱与连通性。这里的`L=D−A`是无权无向简单图的**组合拉普拉斯**，并非所有文献中归一化Laplace。只研究三点与四个离散时点的线性模型`x_{n+1}=Wx_n`、`W=I−L/4`。对这个特定最大度数≤2的模型，W对称、每项非负、行和1且对角项至少1/2。因此数学平均状态严格保持。**实际人类同意、政治观点收敛或真实群体共识不能由这个人工平均规则自动推出。**

[事前冻结九图世界、18432完整外生来源与闭式谱预测的协议](../../protocols/R255_GRAPH_LAPLACIAN_9_WORLDS_18432_COMPLETE_SOURCE_ATOMS_PRESCORE_FREEZE_2026-10-23.md)，独立先提交[1b5b16fe](https://github.com/edwardsage419/Psychohistory-Research/commit/1b5b16feb1291a017c1ab01b7dd1deda87ae138f)后才实现模型和CI。

## 九人工图源与两套独立精确计算

各world以潜在边01、02、12对应6独立公平edge bits，三条边分别按冻结概率0、1/4、1/2、3/4或1开放（被禁用边强制0，原bit仍保留）。另有3个公平独立初始意见bit和时间n=0,1,2,3。每world完整64种边bit×8个初态×4时点=**2048完整人工结构来源点**、每点设计质量1/2048；九world合计**18432条完整原source**。真正独立外生种类是每world512种九bit组合，四个时点从属于同一初值动态，不能将18432条称作独立受试者。CSV逐source保留全部原bit、公开边状态、可见三维意见x_n/下一状态、平方意见离差V_n和V_{n+1}、oracle的观察图λ₂、零根重数及真实物理图连通分量数。

第一路径实际构造L、W并迭代三次，保存Fraction状态、`V_n=∑_i(x_{n,i}−mean(x_0))²`、完整原source。第二独立路径**不调用前一步迭代和矩阵向量乘法函数**，直接枚举每个时点所有长度n的顶点序列，累积W沿路径系数乘积与种子状态，逐source三个意见值精确相同。第三谱路径用独立3×3行列式、迹/迹平方推出特征多项式，再与根据三边开放数量的完备四类图的特征根核对；以独立BFS审计连通分量等于零特征根数。第四概率路径不用完整source CSV，直接根据所有允许边i.i.d. Bernoulli边配置乘积求全部edge-mask联合和Eλ₂、连通概率、分量期望；九world概率和原source逐项完全一致。

## 三节点图的完备拉普拉斯谱与共识条件

| 图类型 | m条开放边 | L特征值（升序） | λ₂ | 连通分量数 |
|---|---:|---|---:|---:|
| 空图 | 0 | 0,0,0 | 0 | 3 |
| 单边、一个孤点 | 1 | 0,0,2 | 0 | 2 |
| 三点链/星形（同构） | 2 | 0,1,3 | 1 | 1 |
| 三点三角图 | 3 | 0,3,3 | 3 | 1 |

无向非负简单图的这四种完备类型得到`λ₂>0 ⇔ 图连通`。空图、单边图存在多个独立零模态，可保持互不连通社区意见差别；仅有同一簇内部的平均会收敛，并不保证所有顶点最终统一。两边的路径图非平凡W特征值`1−1/4=3/4`和`1−3/4=1/4`，均小于1；三角图两个非平凡共识模态都为1/4，因此对固定连通图和任何初态最终趋向全体原算术均值。**有限n≤3的源验证了这些模型的状态与V下降，理论长期收敛凭确切W谱证明**，不拿四时点样本冒充无限实验追踪。

对任意上述W，它都是对称非负行随机矩阵，所以每步均值不变：`sum_i x_{n+1,i}=sum_i x_{n,i}`；正交于常量向量1的偏差子空间受W映射而各模态平方乘上`(1−λ/4)^2≤1`，因此`V_{n+1}≤V_n`。全部18432条人工源逐项验证精确有理不增。有些初始状态本来就全体相同、V=0，不能由其n=3仍共识断定图连通；也不能由观察报告图连通推断真实网络连通。

## 九world图结构的来源统计与闭式期望

对于三个潜在边独立p开放，m∼Binomial(3,p)，若m≤1则λ₂=0、m=2则λ₂=1、m=3则λ₂=3，故：
[
E[lambda_2]=3p^2(1-p)+3p^3=3p^2,
]
[
P(lambda_2>0)=3p^2-2p^3,qquad
E[	ext{连通分量数}]=3-3p+p^3.
]
所有预冻结p源结果和这三条独立多项式精确一致：

| 冻结图world | E[λ₂] | P(观察图连通) | E[观察图分量数] |
|---|---:|---:|---:|
| EMPTY_P0 | 0 | 0 | 3 |
| EDGE01_P1 | 0 | 0 | 2 |
| EDGE12_P1 | 0 | 0 | 2 |
| PATH_01_12_P1 | 1 | 1 | 1 |
| TRIANGLE_P1 | 3 | 1 | 1 |
| ER_TRIANGLE_P_QUARTER | 3/16 | 5/32 | 145/64 |
| ER_TRIANGLE_P_HALF | 3/4 | 1/2 | 13/8 |
| ER_TRIANGLE_P_THREE_QUARTER | 27/16 | 27/32 | 75/64 |
| STATIC_EMPTY_TRUE_GRAPH_OBS_REPORT_HALF | 可见3/4 | 可见1/2 | 可见13/8，真恒为3 |

**测量别名不等于物理相同。** STATIC_EMPTY_TRUE_GRAPH_OBS_REPORT_HALF的真实隐藏物理图三边全0、真连通分量恒3，但报告器对相同六个原edgebit、相同三个初态意见、相同n，产生与ER_TRIANGLE_P_HALF逐完整source一致的全部**可见边和人工意见动态**，即全部观察图统计、λ₂以及线性模型报告轨迹都相同。这只在观测网络记录器和意见动态可同时按伪图生成报告的严格**人工结构**成立；若真实边或真实意见独立验证则可排除。不得据此声称真实社交网络没有连通性，或历史共识是假造的。

## 三job真实CI、SHA和有界科研资格

[原生Python Fraction图谱与完整独立walk执行程序](r255_exact_random_graph_laplacian.py) · [九world全18432原边bit×初态×时点CSV](R255_ALL_18432_ORIGINAL_LAPLACIAN_CONSENSUS_SOURCE_ATOMS.csv) · [全部world谱隙、连通概率及分量期望JSON](R255_EXACT_RESULTS.json) · [完整SHA256来源凭证](R255_FINAL_MACHINE_ACCEPTANCE.json)。

[GitHub Actions run39896308708](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39896308708)总状态completed/success，三个job均success，Python3.11及3.12实际日志各`Ran 84 tests`、`OK`，**168次真实双版本单测通过**。第三独立source audit实际读取18432原source，核验九world各2048独特六edgebit+三seedbit+n组合、各源1/2048、四图型λ₂与零根数、初始三意见总和恒定、V_{n+1}≤V_n、九world完整边联合归一、全部多项式解析Eλ₂/连通率/分量期望、伪报告观察别名与SHA，日志`R255_ALL_18432_ORIGINAL_LAPLACIAN_AND_CONSENSUS_SOURCE_ATOMS_VERIFIED`与`R255_ALL_18432_SOURCE_ATOMS_PERMANENTLY_ARCHIVED`。所有原CSV/完整结果JSON/SHA机器人永久归档main提交[c823c63e](https://github.com/edwardsage419/Psychohistory-Research/commit/c823c63ede1d93570b12b3a32a78774fb1cd649d)。

原CSV SHA256 `7dce525d752c167dcf692873e2ef833b00506d0eb3fbe4c41ef06deb82abef65`，结果JSON SHA256 `4f9ceb536a0fa4ee0196affb46790fc8d504c2c9f722e705a9e05444fedf93d6`。

科学资格`CLOSED_BOUNDED_E1_FINITE_THREE_NODE_RANDOM_GRAPH_LAPLACIAN_CONSENSUS`，没有真实组织共识、社会网络连通性或历史信息传播证据，E2/E3均未新增。R073及PESEN v0.1继续冻结；下一原目录11-016 Queueing Models（拟R256/P2），全部原R完成后再分类熔炼。
