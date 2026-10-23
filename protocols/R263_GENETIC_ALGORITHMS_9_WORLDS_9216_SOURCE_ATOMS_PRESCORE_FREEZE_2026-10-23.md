# R263 遗传算法：九人工双个体三位基因组、9216完整初始/交叉/突变来源；预评分冻结

日期2026-10-23 Asia/Taipei。原239目录11-023 Genetic Algorithms（P2），科研编号R263。源文献John H. Holland (1975), *Adaptation in Natural and Artificial Systems*, University of Michigan Press 1975／MIT Press edition 1992, https://mitpress.mit.edu/9780262581110/adaptation-in-natural-and-artificial-systems/ 。本R仅验证极有限一代、两个个体、三bit基因组、显式同分决策和遗传算子；不声称复现Holland一般模式定理、长期收敛或优化现实社会策略。只有有限人工数学E1，真人E2=0、历史E3=0；R073/PESEN v0.1冻结。

## 原结构和算法信息顺序
每world人口P=(parent0,parent1)，每父本三基因bit，故6原bit；再有独立公平交叉开关C∈{0,1}、断点位J∈{0,1}指定cut=1+J、两个独立公平候选突变位M0,M1，完整**10bit等质量原类型2^10=1024/world**，九world共**9216完整原人工source**；每个source设计概率1/1024且全部带原父代、原两个交叉bit、两个突变bit（即使某world禁止该算子原bit亦保留但不影响输出）。这里并非9216个人类进化个体，不将一代完整source记录看成长期自适应迭代。

先按冻结world启用规则对双亲执行**一点评价前的同位重组**：C=0或禁用cross则两个候选子代是原双亲不变；C=1且启用cross，则在cut=1或2处切开两份三bit原基因组并交换后缀产生两个子代。之后若启用mut，则M0=1翻转子代0的基因位0，M1=1翻转子代1的基因位2；mut=0禁用则bit无效果。该固定特定位突变**不是各位独立概率突变**，算法局限须明确；变异位只通过两个受限位置传播。世代选择有两种：
- GENERATIONAL_NO_ELITISM：下一代只由两个候选子代组成；
- ELITE_TOP_TWO：按分数越高越好从四个多重记录[parent0,parent1,child0,child1]确定性选择前两名保留，并显式同分规则按三bit基因串升序、同串按原顺序parent0,parent1,child0,child1打破平手。重复基因型可以占两个不同个体位置，不做去重。
冻结适应度ONEMAX(g)=三个bit中1的数量；TRAP(g)=4当且仅当g=000，否则等于ONEMAX(g)，因此TRAP人工真正全局峰是000（f=4），而111为更易局部梯度的f=3；这只是一条人造反例，不是自然选择真实适应度函数。

## 九冻结world
1 CLONAL_ONEMAX：交叉关、突变关、不精英，下一代=原双亲；
2 CROSS_ONEMAX：交叉开、突变关、不精英；
3 MUTATE_ONEMAX：交叉关、突变开、不精英；
4 CROSS_MUTATE_ONEMAX：交叉开、突变开、不精英；
5 ELITE_CLONAL_ONEMAX：交叉关、突变关、精英；
6 ELITE_CROSS_ONEMAX：交叉开、突变关、精英；
7 ELITE_MUTATE_ONEMAX：交叉关、突变开、精英；
8 ELITE_CROSS_MUTATE_ONEMAX：交叉开、突变开、精英；
9 ELITE_CROSS_MUTATE_TRAP：交叉开、突变开、精英、非单调三bit trap适应度。

## 事先锁定命题与证据限制
A. 所有9×1024原source保存父母两三bit genome、实际两个原候选子代、下一代幸存两genome、父母和幸存者最大分数以及分数变化Δ、完整10bit设计质量。ELITE所有world每个原source的下一代最大分数**绝不低于父母最大分数**，因为两个原双亲始终参加生存竞赛；不精英CLONAL最大不变；在不精英交叉/突变world，至少存在一完整source造成最佳适应度下降，也存在另一source造成最佳适应度上升（针对启用算子可达来源）。**不把精英保证“当期最好不下降”混成所有人均值上升、所有轨道收敛或全局最优能保证搜索到。**
B. 独立第二演算不调用原10bit逐事件生成器：对完整64种原父本6bit组合，枚举独立四算子bit全部16种，共每world64×16=1024条件事件，从明示算子映射和适应度函数另外构造**完整下一代双genome联合分布**，逐world与原source按完整父本条件（16个事件、质量1/16）得到的条件PMF严格Fraction一致。采用不同实现路径例如原源用切片，第二用整数mask、独立位拼接与独立sort；所有16事件含算子未启用时导致重复输出，必须合并概率而非误当不同后代。
C. 精英保存best的结论是代数恒等式，不代表无需验证的“平均性能最优”：按每个原父本比较ELITE与不精英（原bit相同）下最佳分数，ELITE最佳总不低于相同原世界对应非精英的下一代最佳，但精英可能消灭新的有潜力但低当下分数多样性，只有一代不能验证长期探索影响。
D. 对两世界CLONAL_ONEMAX与ELITE_CLONAL_ONEMAX，禁用交叉突变且候选原本就是父本，按多重记录确定性精英选择时，幸存的**最佳分数**与原完全相同；但精英可能两个都来自较高分数的原同基因型拷贝，个体基因型排列/多样性未必同值。不能声称sourcewise精英与nonelite完整观察相同。
E. 关闭mutation但启用crossover时，子代每个位置的总体1数量与原两父本跨两个体的**逐位和**守恒（交换后缀而非翻转），但每个个体最佳适应度可降低或提高；启用mutation则可能不守恒。
F. TRAP的人造峰000的适应度4，高于111的3，公开适应度分数定义完全冻结；不允许事后根据观察结果调整适应度目标，不将优化个体社会行为与生物进化等同。
G. Python3.11/3.12各≥45真实tests，第三GitHub Actions原source审计9216唯一10bit组合、每source1/1024、实际算子流程、双算法全部条件下一代分布、适应度比较、原source/结果JSON SHA256，通过后机器人永久main归档与正式有界E1报告。下一目录11-024 Approximate Bayesian Computation（R264/P2）。
