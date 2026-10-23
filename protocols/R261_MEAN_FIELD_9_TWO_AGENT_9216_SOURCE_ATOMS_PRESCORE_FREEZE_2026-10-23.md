# R261 平均场近似：九人工二行动者两步相互作用世界、9216完整原10bit来源；经验分布有限N偏差与共同随机性，独立计分前冻结

日期2026-10-23 Asia/Taipei。原239目录11-021 Mean Field Approximation（P1），研究R261。原始理论参照H. P. McKean Jr (1966), *A class of Markov processes associated with nonlinear parabolic equations*, PNAS 56(6):1907–1911, https://doi.org/10.1073/pnas.56.6.1907。本文仅研究**固定两个二元个体N=2、两时步、有限三态群体计数**的精确随机动力学与一条确定性均场更新的差异；并没有证明McKean-Vlasov极限、N趋无穷的传播混沌、连续时间非线性随机微分方程或任何真人社会影响。新真人E2=0、真实历史E3=0，R073/PESEN v0.1冻结；按全部原R→统一归类→最后熔炼推进。

## 完整外生结构
每world两位初始个体二元状态x0a,x0b∈{0,1}，每个t∈{0,1}两人各独立两bit随机数 r_{t,i}∈{0,1,2,3}，所以2个初始bit +8个随机bit=**10公平独立原bit，1024完整外生原source/world，九world合计9216完整原source**，每source质量1/1024。CSV保存原10bit、全部三时点个体真实二元状态、可见报告两个状态、可见计数K_t∈{0,1,2}、可见均值M_t=K_t/2和每个更新的条件Bernoulli阈值。每个world总人工源权重1；当固定初始K0=0/2时，每组有256完整噪声来源质量1/256；当K0=1时来源512组，每组1/512。**这不是9216个人或九场真实实验。**

冻结全部world的观察个体更新都只依当期两个公开状态产生群体平均m=K/2，再使用每个world确定性函数q(m)给出下一步状态：
1 FINITE_NEUTRAL_IDIOSYNCRATIC：q(m)=m，两个个体在给定当前群体状态时各使用自己独立r和条件Bernoulli(q)。
2 FINITE_CONVEX_SQUARE：q(m)=m²；在m=0,1/2,1时为0,1/4,1。
3 FINITE_CONCAVE_CONFORMITY：q(m)=2m−m²；在三有限m值为0,3/4,1。
4 FINITE_CONTRARIAN：q(m)=1−m；在三值为1,1/2,0。
5 INDEPENDENT_HALF：q(m)=1/2，无群体状态依赖。
6 UNANIMOUS_ONLY：q(m)=1当m=1，否则0；阈值为“只有全体原为1，下一期才全体1”。
7 MAJORITY_TIE_UP：q(m)=1当m≥1/2，否则0；双人平手按多数规则偏向1（外加明确tie规定）。
8 COMMON_NOISE_NEUTRAL：q(m)=m，但两个个体使用**同一个**个体0的两bit r_t，不符合给定当前群体条件后的个体独立噪声；显示条件共同随机性如何增强方差。
9 OBSERVED_COMMON_NOISE_TRUE_INDEPENDENT_SENSOR：真实隐藏个体按照world1独立随机位更新，但记录器对同一个原10bit运行world8的共同噪声更新，**全部可见个体双时点行为逐source与world8完全一样**，隐藏真群体计数可能不同。这一人工观察别名仅示范真值/报告不可独立校验时的非识别，不声称真人实际伪报。

## 正确均场与有限N精确马尔可夫对照
给定初始mean m0=K0/2，确定性均场近似递推`m^MF_{t+1}=q(m^MF_t)`，在非线性q世界q被定义在整个连续[0,1]上（m²或2m−m²等），在阶跃世界明确设定边界及平手，故对第二时点的`m^MF_2`仍有定义。
第一源路线原完整10bit逐source运行两步两个体，生成M0,M1,M2、两个体状态/报告/隐藏oracle与两期q；无条件初始状态完全均匀随机，但所有**条件初始K0**分析需使用正确条件权重分层。
**独立第二数学路线不读取原bit来源、模拟器或随机阈值生成器**：构造有限群体计数K∈{0,1,2}的3×3转移核。给定当前K=k，q=q(k/2)，对前7世界的独立条件更新，
`P(K'=0)=(1−q)²,;P(K'=1)=2q(1−q),;P(K'=2)=q²`。
COMMON_NOISE世界和人工报告世界的观察计数则
`P(K'=0)=1−q,;P(K'=1)=0,;P(K'=2)=q`，
因为两个报告个体使用同一个bit。把T乘2次获得给定初始K0的完整K1/K2计数分布、条件均值、条件方差、条件全体一致K∈{0,2}概率；与1024完整原bit来源条件积分**每k逐格严格Fraction相同**。不能用“两个agent给定K总是独立”错误计算common shock世界。

## 事前冻结关键反例
固定初始K0=1,m0=1/2：
- FINITE_NEUTRAL_IDIOSYNCRATIC：m^MF1=m^MF2=1/2，有限人口E[M1|K0=1]=E[M2|K0=1]=1/2，**但Var(M1|K0=1)=1/8，Var(M2|K0=1)=3/16**。均场均值准确不等于预测分布准确或波动不存在。
- COMMON_NOISE_NEUTRAL：相同确定性m^MF1=m^MF2=1/2、同样的两个条件均值均1/2，**但Var(M1)=Var(M2)=1/4**，多于独立噪声world的1/8与3/16。共同随机性不可用“个体独立更新”核替代。
- FINITE_CONVEX_SQUARE：m^MF1=1/4、m^MF2=1/16，而有限系统E[M1]=1/4、**E[M2]=5/32**；二者第二时点严格差`+3/32`，是`E[q(M1)]≠q(E[M1])`的有限N Jensen效应，不是软件误差。
- FINITE_CONCAVE_CONFORMITY：m^MF1=3/4、m^MF2=15/16，而有限系统E[M1]=3/4、**E[M2]=27/32**；第二时点严格差`−3/32`。
- OBSERVED_COMMON_NOISE_TRUE_INDEPENDENT_SENSOR：同10bit全部可见两人报告每期逐source等于COMMON_NOISE_NEUTRAL；但真实隐藏状态在初始K0=1时遵循独立的world1分布，其第1时点条件方差为1/8，而报告分布为1/4。此区别依赖人为允许观测记录被伪造的构造，不能推广为历史现实事实。

## 科学验收
每world×全部1024原外生10bit完整来源，原初态K条件质量正确归一，原位重建实际观察更新，两时点计数状态按独立理论核严格吻合。全部9world的T行概率=1、预测分布正确，两个独立世界和两个共同噪声世界不能混核；不擅自宣称N→∞规律。两个Python3.11/3.12各≥45真测试、第三GitHub Actions job独立完整9216源、10bit唯一性、1024/world全量、K条件分布、所有冻结偏差、原source SHA256以及bot永久main归档，之后发布科学报告和正式有界E1结题。下一原目录11-022 Cellular Automata（拟R262，P1）。
