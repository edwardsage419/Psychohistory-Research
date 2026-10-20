# R129 胆小鬼博弈：1973原始五策略实验、两策略反协调及升级风险——计算前冻结

日期2026-10-20。目录P2 05-005 Chicken Game。R128已有猎鹿两对角协调纯Nash，本轮重点Chicken两非对角纯Nash、双方同时升级损失、分布相关、角色执行噪声，不替代R131后续进化理论的完整学习。R073和PESEN v0.1冻结；继续全部R研究后分类再熔炼。

## 一手原文和确切来源级别

Maynard Smith, J. & Price, G. R. (1973), The Logic of Animal Conflict, Nature 246:15–18, DOI https://doi.org/10.1038/246015a0；机构所托原刊完整4页PDF https://public.ek-cer.hu/~szabo/EGT20/library/maynard_n73.pdf。本轮实际阅读原论文、可视核验刊印p15原问题与策略、p16五策略和Table1全部25格。原作者真正模拟的5种策略是Mouse、Hawk、Bully、Retaliator、Prober-Retaliator，而非现代简化2×2 Hawk–Dove表。原文p16称15种无序对抗配对，每种2000次随机计算机模拟，严重受伤概率0.10、探测概率0.05、胜利+60、严重受伤−100、非严重受击−2、节省时间0..+20，最后表是按1位小数报告的原作者模拟均值，既不是原始野生动物数据，更不是本轮重新运行的3万次模拟。本期严格转录原表，不能据表格声称已复现原RNG与策略过程。

原p16 Table1行列顺序Mouse,Hawk,Bully,Retaliator,Prober-Retaliator，显示一位小数数值：
Mouse [29.0,19.5,19.5,29.0,17.2]
Hawk [80.0,-19.5,74.6,-18.1,-18.9]
Bully [80.0,4.9,41.5,11.9,11.2]
Retaliator [29.0,-22.3,57.1,29.0,23.1]
Prober-Retaliator [56.7,-20.1,59.4,26.9,21.9]
逐列最佳应对：对手Mouse时Hawk/Bully并列80；对手Hawk时Mouse19.5；对手Bully时Hawk74.6；对手Retaliator时Mouse/Retaliator并列29；对手Prober-Retaliator时Retaliator23.1。原文作者报告Retaliator为ESS、Prober近ESS，但发表到一位小数的Retaliator/Mouse相关单元全显示29而无法仅用这个精度确认严格二阶ESS判据，因此应标为作者报告的进化稳定性、而非项目由舍入表严格数学重新证明。同样该表不是人类冲突E2。

Bertrand Russell (1959), Common Sense and Nuclear Warfare书中的道路对冲Chicken类比，可通过出版社电子书介绍 https://www.perlego.com/book/1615329/common-sense-and-nuclear-warfare-pdf 核实；未获得1959书内原印刷逐页文本，不归其历史政治例证以定量统计效力。后续理论来源：2025 Arigapudi & Heller, Stable mixing in Hawk–Dove Games under best experienced payoff dynamics, Games and Economic Behavior 151:148–161, DOI https://doi.org/10.1016/j.geb.2025.03.003，及开放Scientific Reports 2019 https://www.nature.com/articles/s41598-019-43770-x ，明确简化鹰鸽/Chicken模型两非对角纯均衡与一个内部混合均衡。以下具体V,C公式及矩阵是本项目明确另外定义的简化模型，不冒充1973原五策略作者模拟。

## 事前精确合同1：两人Hawk–Dove/Chicken纯数学模型

H代表坚持/升级、D代表退让，价值V>0、争斗成本C>V，两参数必须标准库Fraction且禁float/bool/未经许可转型。对行人:
HH=(V−C)/2；HD=V；DH=0；DD=V/2。列人按对称角色交换。两个非对角严格纯Nash为(H,D)和(D,H)；HH双坚持在C>V时每人收益负，转向D得0因而不是Nash；DD各V/2，单偏离H可得V，亦不是Nash。完全不同R128两个对角纯Nash。

对手H边际概率q∈[0,1]，E(H)=q(V−C)/2+(1−q)V，E(D)=(1−q)V/2，差(EH−ED)=(V−Cq)/2，所以混合无差q*=V/C、0<q*<1；对称独立混合双方H时冲突概率q*²，每人均衡期望V(C−V)/(2C)。预固定V=2,C=6，行收益[[-2,2],[0,1]]，q*=1/3、双方H概率1/9、每人期望2/3、总4/3。

## 事前精确合同2：同边际不同相关性时的同时升级风险

固定双方H边际均1/3，所有有序联合结果按HH,HD,DH,DD排列，完全显式非负、sum1：
独立 [1/9,2/9,2/9,4/9]：同坚持1/9，两人期望总4/3（各2/3）。
互斥配对 [0,1/3,1/3,1/3]：同坚持0，两人期望总2（各1）。
完全同向 [1/3,0,0,2/3]：同坚持1/3，总期望0（各0）。
三种两个个体的边际H概率完全相等，仅联合依赖不同。此只证明冲突概率与福利不能由边际唯一决定，不自动证明此三组都是相关均衡或真实人群行为。

## 事前精确合同3：角色实施错误与冲突成本敏感性

从单个角色分配(H,D)出发，两位分别独立以实施错误率ε翻转自己的行动，HH概率ε(1−ε)，HD概率(1−ε)^2，DH概率ε²，DD概率ε(1−ε)；ε为Fraction 0..1。这是研究者独立定义的机制噪声，不是1973实验伤害率或现实国家冲突率。ε=1/2同时坚持概率为1/4；ε=0、1时为0。固定价值V=2，C取3,4,6,8,12时混合Nash H概率V/C，独立双坚持概率(V/C)^2随C增加下降；**仅在双方真的独立采取该均衡混合行动条件下成立**，若外生固定H概率1/3，则C增加不降低独立双坚持概率1/9而会增大损失。不得把数学成本参数变化直接当历史冲突因果估计。

## 完整验收

精确Fraction；拒绝非法输入、转型、未归一耦合和不一致边际。全部25原作者刊印数进入版本源码并检查本刊逐列best response、可从舍入表推出的弱对称Nash，但禁止借此宣称论文随机仿真复现或精确ESS证明。两套独立四结果player payoff与纯Nash单人偏离算法，对51个合法参数组合V=1..6、C=V+1..12及13点q=k/12逐例检查完整期望与解析混合阈值，共51×13=663对照，另外逐参数用真无差q*=V/C再核对。对13个ε=k/12分别穷举四种行动翻转结果并检查闭式总额；三种共同边际分布核对期望与冲突概率。至少45项真正unittest，GitHub Actions真实成功后机器提交源码/测试/报告SHA256收据并回读，方可限定状态 LEARNING_COMPLETE_BOUNDED_CHICKEN_ORIGINAL_1973_TABLE1_AND_EXACT_ANTICOORDINATION。没有完整重跑1973的30000原模拟战斗、没有真人E2、没有真实历史E3。保持R073与PESEN冻结。
