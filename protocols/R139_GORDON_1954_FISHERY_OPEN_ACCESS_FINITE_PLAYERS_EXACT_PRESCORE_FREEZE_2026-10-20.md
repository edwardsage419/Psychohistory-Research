# R139 事前冻结：Gordon (1954) 共池渔业经济最优、自由进入均衡与有限提取者博弈

日期：2026-10-20。原239目录 P1 / 05-015 Common Pool Resource Dilemma。代码与预测计数编写**之前**冻结。任何探索结果不得回写冻结协议。严格区分Gordon原式、项目自构数值例、项目新构的有限个体博弈。

## 去重
R047已有De Geest/Kingsley原始真人CPR处罚与禀赋不平等实验：R067原始可读128人、32四人群、非练习1920条行为记录、16轮、非二元提取；不能将真实行为当作这里的海洋生产函数。正式R047原研究包在 archives/library-originals/心理史学_R047_正式研究包_2026-10-15.zip；R067真实数据匹配状态见 research/R067/R067_E2_R047_APPLICABILITY_RESULTS.json。R139不加载或重估这些受试者的数据，也不假称真实E2再现。

## 作者一手材料
H. Scott Gordon (1954), *The Economic Theory of a Common-Property Resource: The Fishery*, Journal of Political Economy 62(2):124–142, DOI 10.1086/257497，UCSB教学托管原JSTOR扫描 https://faculty.econ.ucsb.edu/~tedb/Courses/Ec100C/Readings/ScottGordonFisheries.pdf。本期直接可视核阅印刷130页Fig1平均/边际生产率与最优、131页Fig2迁移趋向平均生产率、141页Eq(1) P=a−bL、Eq(2) L=cEP、142页Eq(3) R=L−E（作者设置单位投入成本1）、Eq(4) R'=0及随后的 L=caE/(1+cbE)、E_opt=(sqrt(ca)−1)/(cb)。作者符号c为捕获生产率、b为资源枯竭系数。为避免成本重名，本项目记 production gamma、depletion beta、努力单位成本 q，原图和Eq(3)/(4)的q=1作为主基线。作者1954论述开放竞争耗散资源租金与平均/边际差异，并未发表本项目随后的人数n利润份额博弈或整数组合枚举。

## 源方程与冻定参数
P=a−beta L，L=gamma E P，推出 L(E)=gamma*a*E/(1+gamma*beta*E)，P(E)=a/(1+gamma*beta*E)。资源净租金 R(E)=L(E)−qE。参数a>0、beta>0、gamma>0、q>0并gamma*a>q；取 Fraction 精确输入，禁止float和bool。经济社会最优 E_soc=(sqrt(gamma*a/q)−1)/(gamma*beta)，自由进入零租金正根 E_open=(gamma*a/q−1)/(gamma*beta)。若gamma*a/q为整数完全平方，则只用Fraction精确求社会最优。对任意E∈[0,E_open]检验作者原Eq1/2及两套直接代数表达（无仿真）。与土地生产和资金尺度无关的“开采量更大/自然存量更低”仅在此生产方程内成立，不能推出真正生态灭绝或现实历史概率。
主实例 gamma=1,beta=1/4,a=9,q=1：预测E_soc=8, E_open=32, R_soc=16,R_open=0, P_soc=3,P_open=1, L_soc=24,L_open=32。

## 项目新增有限提取者博弈（显式标注非原作者直接模型）
n∈{1,2,3,4,5,8,16,32}个对称用户，个体努力e_i≥0，E=sum e_j，每个个体的**私有捕获收入份额**=e_i·(L(E)/E)，若E=0则连续延拓至gamma*a。收益 u_i=e_i*(gamma*a/(1+gamma*beta*E)−q)。在独立连续动作下同质单人最好反应的内点条件，设z=1+gamma*beta*E, H=gamma*a/q，满足 n z²−H(n−1)z−H=0（源式基础上的新推导，q正常化因子已约）。验证根可被Fraction区间二分严格包住，区间终点的多项式严格异号、上界长度≤8/2^80，任意数字显示必须注明来自精确有理包围而非伪称代数根有理。n=1应恰为社会最优。n增大， E_n 单调增加并趋向 E_open、总租金单调降低且始终正，固定生产参数。对12组冻定合成参数 gamma=1, q=1, a∈{4,9,16,25}, beta∈{1/8,1/4,1/2}、8个人数值=**96**个严格有理区间重算；枚举与理论的解析条件做独立验证；一组作为费用政策演示，社会最优目标点的单位行动费 t=(1−1/n)E_soc*(-A'(E_soc))，来自私利与社会边际收益差，项目自构静态收费政策（转移费不从社会福利中重复减掉），并非作者1954原政策实验、也非完整各参数机制设计研究。

## 项目新增离散博弈与标定边界
仅主实例a=9,beta=1/4,gamma=q=1。3人行动e_i∈{0,2,4,6,8,10,12,14,16}共9³=**729**配置，3×8=**17496**项单侧不同偏离比较。彻查纯策略NE、其集合/社会净租金；逐一求最大福利配置及与纯NE是否一致；比较行动网格量化效应，防止把连续开放准入E=32当成3人离散NE，也不得称这些枚举是真人。冻结不预设离散NE数量，计算若出人意料也保留。

## 可证伪与CI
有数值波动或分类错误即失败，不得为匹配结论改动样本。主对照含a9、n=1、2、8、32；独立边界测试输入0、负参数、float、bool非法，实际E0允许。真实GitHub Actions Python3.11/3.12双job跑unittest、完整96案例＋729个档案/17496偏离和源ZIP/py/results哈希；只有成功后记远端CLOSED_BOUNDED。
真人新增E2=0，外部历史E3=0；不动R073/PESEN v0.1。既定所有R项学完后统一归纳分类，再熔炼。