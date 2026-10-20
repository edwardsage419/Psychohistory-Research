# R144 计算前冻结：Mahoney (2000) 与 Capoccia–Kelemen (2007) 历史制度主义、反应性序列与关键转折点

日期 2026-10-20。目录 P1 / 06-002 Historical Institutionalism。此协议必须先于R144代码、测试、机器结果生成入库。不得在看到数值后修改定义或消除反例。

## 原始文献及直接核读
1. James Mahoney (2000), “Path Dependence in Historical Sociology,” *Theory and Society* 29:507–548, DOI 10.1023/A:1007113830879，ETH高校保存原印刷影印 https://archiv.soms.ethz.ch/teaching/OppFall09/MahoneyPathDependence.pdf 。实读原刊507、508、509页，包括contingency论证、self-reinforcing sequences与reactive sequences的不同及“任何过去影响未来”过度宽泛的警告。
2. Giovanni Capoccia, R. Daniel Kelemen (2007), “The Study of Critical Junctures: Theory, Narrative, and Counterfactuals in Historical Institutionalism,” *World Politics* 59(3):341–369，DOI 10.1017/S0043887100020852；作者牛津大学托管的原刊扫描 https://users.ox.ac.uk/~ssfc0073/Writings%20pdf/Capoccia%20and%20Kelemen%20WP%202007.pdf ，实读印刷341、342、343页，确认“短暂结构约束松动的关键转折点”以及必须分析真实可行替代选择、反事实与序列过程追踪。上述两篇主要是解释与方法论，不附本期人工模型数值，不冒称原作者数学仿真、真实历史事件因果识别。

## 去重及科研任务
R143已精确研究Arthur(1989) **技术采用正反馈吸收马尔可夫链**，本期不得重复其收益-规模、概率吸收机制。R144关注**反应性（responsive）事件序列**及关键转折窗口中的机会约束、后续抵抗、制度巩固，严格区分“次序有关”的人工逻辑事实与现实历史识别。

## 事前固定的项目自建状态转移模型（非论文原数学模型）
状态四元组 (reformed∈{0,1}, coalition∈{0,1}, window∈{0,1,2}, entrenched∈{0,1})，初始(0,0,0,0)，一旦entrenched=1必须reformed=1且永久不倒退。事件字母恰为6种：
O = OPEN: 若尚未巩固，window设为2；其余状态不改。
M = MOBILIZE: 当入场前window>0，coalition设为1；随后window减1至最小0。
A = ADOPT: 当入场前window>0且coalition=1，reformed设为1；随后window减1。
E = ENTRENCH: 若入场前reformed=1，entrenched设为1；随后window减1。
B = BACKLASH: 若entrenched=0，reformed=0、coalition=0；随后window减1。
W = WAIT: 仅window减1。
所有非O事件都统一做window=max(0,window-1)；E成功后窗口无需强制清0，之后O对已巩固状态无作用。此人为定律仅是合成结构因果玩具，绝不声称“真实转折期必持续2次事件”，M/A/E/B没有符合社会调查的可靠概率。

## 完整冻结实验，不预设实际计数
A. 严格穷举长度5的6^5=**7776条人工事件流**，逐步保存全四元组状态与最后regime、entrenchment、window、coalition。分别按regime∈{0,1}、entrenched∈{0,1}输出直方计数。
B. 对全部5种独特事件{O,M,A,E,B}的5!=**120**种顺序，固定完全相同事件多重集合，求最终制度/巩固异同，并按精确顺序索引输出所有120项。冻结见证：OM AEB（连续5事件“O M A E B”）能改革且巩固，B E A M O不能。该命题必须经过程序检验。
C. 对7776条长度5人工流的每个时点t=0..4，做`do(e_t=W)`的**38880次成对反事实计算**（包括原本W替换为W无差别），记录reformed/entrenched差异、按事件身份和时间位置分组；该数不是真人样本量、不是真实历史干预、不具可推广的统计置信区间。对每个固定前后事件及初始状态，用纯函数显式取替代轨迹，而不是擅自用真实观测估计因果效应。
D. 同一最终reformed=1但未巩固与已巩固两条历史“OM AWW”与“OM AEW”在观测终点的regime相同，entrenched不同；附加同一个B后的下一期结果不同，证明若观测只有制度存续的二元终点，不能识别潜在的制度稳固机制。请保留完整的节点路径，不能只输出终点。
E. 负对照：构造只看6类事件总次数的`count_signature`，所有120种不同排列签名必须相同，但真实最终regime/entrenched可以不同。证明顺序事实不由事件集合完全决定；这本身不证明真的有现实路径依赖过程。
F. 独立验证：逐状态主状态机与按事件拆分的第二个规范解释器交叉对照所有7776条事件流的完整路径；关键约束(entrenched⇒reformed, 0≤window≤2)逐步检查；若有差异不得宣称验证通过。

## 计算和发布条件
全整数标准库、itertools.product/permutations，确定性JSON，源程序＋不少于45个真实unittest、原始结果、协议和科学报告一起SHA256归档；严格区分“数学定义复验 E1”与“作者理论的实例化 E1”及“外部真实史料与历史反事实识别 E3=0”。必须GitHub Actions Python3.11及3.12各跑所有unittest、源ZIP和内含3文件四项SHA256、全部7776完整序列和38880 paired-do反事实机器JSON重算逐字节一致后才能标CLOSED_BOUNDED。
人级E2新证据0，外部历史E3新证据0。R073/PESEN v0.1冻结。既定R系列学完以后统一归纳分类，最后熔炼；下一目录P2/06-003 Principal Agent Models（拟R145）。