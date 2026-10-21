# R169 共演化网络：72组四节点网络与观点的精确联合概率研究

2026年10月21日。原研究目录 **P2/07-011 Coevolving Networks（共演化网络）**。科研状态 **CLOSED_BOUNDED_E1**，仅代表项目自建四节点有限数学实验已完成，不代表真实人群意见、真实社会关系或宏观网络相变得到验证。

一手文献：[Holme与Newman2006美国物理学会原刊](https://doi.org/10.1103/PhysRevE.74.056108)提出网络关系与观点状态同时演化模型；[Vázquez、Eguíluz与San Miguel2008原刊](https://doi.org/10.1103/PhysRevLett.100.108702)研究异见边上随机观点模仿与网络重连竞争，原作者给出特定平均场模型的临界参数；[Gross与Blasius2008原开放综述](https://doi.org/10.1098/rsif.2007.1229)整理适应性网络研究。本轮核对原始出版记录及原作者arXiv文本入口，**没有执行作者的复杂网络程序，也没有复制原作者在大型网络上得到的相变结论**。完整学术限制见[科学报告](R169_SCIENTIFIC_REPORT_2026-10-21.md)。

**72组事前冻结：** 四种四节点无向简单图（链式、中心星形、闭环、三角形加尾巴）×三种节点0/1观点组合×三种网络重连概率α（0、1/2、1）×两种可连对象规则（限同观点，或任意不相邻节点），总计72组。每组追踪t=0、1、2、3时的**全部带标签网络边与所有人观点的联合概率分布**。规则预先在[冻结协议](../../protocols/R169_FINITE_ADAPTIVE_NETWORK_72_LABELED_GRAPH_WORLDS_PRESCORE_FREEZE_2026-10-21.md)（提交e991aec）固定。

模型事件规则：每期如果还有连接不同观点的边，均匀选择一条异见边，再均匀选其一端作为主动节点。概率1−α时主动节点模仿另一端观点，连边不变；概率α时尝试拆断该连边，并连接一个符合规则、此前尚未相邻的节点。若没有可连接对象，事件**不作任何改变**，不能暗中把该概率重新分配给模仿行为。全部连边、节点状态及完整概率使用Python Fraction精确表示。

**独立数学验证：** 一套程序直接枚举无向异见边、方向及目标，另一路独立枚举所有有向异见边、行为分支和重连目标，再单独计算马尔可夫传播。两套实现对于72组×4时间点**每个网络与观点状态的概率都精确相等**。完整[1512645字节JSON](R169_EXACT_RESULTS.json)可查阅所有图结构、观点组合、概率、异见边数期望、A观点人数期望及连通分量数期望。

**主要机制：**
* α=0时网络连接在每条可能演化路径上完全不变，允许观点因相邻者模仿而改变；此时重连规则不可识别。
* α=1时个人观点在每条可能路径上完全不变，允许网络改变；单纯的观点占比无法发现网络已经重组。
* 同观点重连成功会恰好移除一条异见边；任意目标重连也可能改连到另一个不同观点的人，使异见边数不降但具体网络结构发生改变。
* **一个精确的统计量不足反例：** 从四节点链式图、观点(0,0,1,1)、α=1开始，经过两期，限同观点与任意目标两种规则生成的**完整网络状态分布总变差距离为1/2**，但两种规则下预期异见边数均严格等于1。只记录异见边数量，将忽略相当大的结构分布差异。这是人工数学性质，并不意味着现实社会存在同样大小的极化效应。

**真实CI及永久归档：** [首轮GitHub Actions 39540425684](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39540425684)、[固定四项SHA256与完整归档39540516277](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39540516277)均success。Python3.11、3.12分别在两个工作流各执行111项真实单测，独立归档任务再执行111项，累计**555次实际执行、111种不同测试方法、0失败**。JSON及源码/测试/完整结果ZIP已由[归档提交c27bb03](https://github.com/edwardsage419/Psychohistory-Research/commit/c27bb0329bbfa8daecf142846719086840287e0c)永久写入main。

**文件清单：** [研究科学报告](R169_SCIENTIFIC_REPORT_2026-10-21.md)｜[冻结协议](../../protocols/R169_FINITE_ADAPTIVE_NETWORK_72_LABELED_GRAPH_WORLDS_PRESCORE_FREEZE_2026-10-21.md)｜[原创程序](r169_adaptive_network_exact.py)｜[111项测试](test_r169_adaptive_network_exact.py)｜[完整JSON](R169_EXACT_RESULTS.json)｜[原生ZIP](R169_Adaptive_Network_72_Worlds_111_Tests.zip)｜[正式机器验收](R169_FINAL_MACHINE_ACCEPTANCE.json)。

固定SHA256：
* 程序 `6f60b15ebbde33502ec660f4c7602960368eb6bbd8243d94483d7243f4005a3a`
* 测试 `2f40e938e9b90c2099f7545707ae205c7ff130477d4e7d9d769b8c2f2368ba74`
* JSON `171c529917d8cdd3443b13883681cf4b020522f6ba0a807d1cb685c70cfd31e1`
* ZIP `64b02b3ccd90f31548fde255ca2e9da14fa2d949fb92b0b7e73d0dbd7119a518`

独立复验：进入 `research/R169`，执行 `python r169_adaptive_network_exact.py > R169_EXACT_RESULTS.json`，再执行 `python -m unittest -q test_r169_adaptive_network_exact.py`；仅需Python标准库。

**证据边界：** 新增真实人类独立验证E2=0、真实历史外部预测E3=0；R073和PESEN v0.1继续冻结。下一原目录 **R170 P2/07-012 Language Evolution Models（语言演化模型）**。继续先完成既定R系列，后统一归纳分类，最后开展模型熔炼。
