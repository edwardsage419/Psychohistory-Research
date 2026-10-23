# R239 定性比较分析 QCA：九人工三条件世界、144完整配置来源、逻辑剩余与观察充分性非因果性；评分前冻结

日期2026-10-23（Asia/Taipei）。原239目录 `10-013 Qualitative Comparative Analysis`（P2），编号R239。继续完成全部R系列再归纳分类、最后模型熔炼。E1有限人工机制，无新增真人E2/历史E3；R073、PESEN v0.1冻结。

## 原始方法与评价界限
Ragin (1987), [*The Comparative Method*](https://www.jstor.org/stable/10.1525/j.ctt1pnx57), University of California Press, 以布尔代数与配置条件表为定性比较研究框架；Schneider & Wagemann (2012), [*Set-Theoretic Methods for the Social Sciences* 第六章：有限多样性与逻辑余项](https://doi.org/10.1017/CBO9781139004244.009) 区分逻辑上可能而未见证据的真值表配置。Baumgartner & Thiem (2020), [*Often Trusted but Never (Properly) Tested*](https://doi.org/10.1177/0049124117701487) 对QCA因果识别的实验评估提出方法争议。本R不对真实历史国家、制度、冲突做配置归纳，不会将样本内集合包含关系直接认定为真实跨环境因果定律。仅 crisp-set QCA，不涉及 fuzzy membership 校准或真实QCA软件的全部标准优化过程。

## 冻结全集及所见数据
每个人工世界四个互相独立均匀Bernoulli原源`X,B,C,U∈{0,1}`，每世界**16条原结构行**且每行1/16；九世界**144条**。实际条件`A=X`，但在两组特意构建的观察别名中`A=U`以制造非正值性。B/C按原源为独立配置条件，隐藏U只用于人工机制和Oracle；结果真`Y=f(A,B,C,U)`。另针对两有限支持世界使用`selected=S=0`当A=0且C=1，否则S=1；未入选来源**仍保留在原CSV**，但对于QCA统计观察结果`observed_Y=-1`（缺失符号）且不能将缺失当反例。实际QCA可见`A,B,C,Y`只来自S=1。数据原CSV保存4原源、真实当前Y、实际处理A、选中标志、可见Y、人工干预Y_doA0/Y_doA1。

## 九个预冻结机制
1. `AND_AB`：A=X、S全1、Y=A∧B。可观察两配置阳性（C可变）；充分条件A∧B，A和B均对于Y必要。
2. `OR_AB`：A=X、S全1、Y=A∨B。最简阳性配置A∨B，A/B各不必要。
3. `EQUIFINAL_AB_OR_NOTA_C`：A=X，Y=(A∧B)∨(¬A∧C)。不同路径组合，A或B单独非必要也非充分。
4. `CONTRADICTORY_A_XOR_U`：A=X，Y=A XOR U。同一观察A/B/C配置出现正负结果各半，任一完整配置的一致性=1/2，冻结严格1.0阈值下**没有任何被一致为真的行**。
5. `LIMITED_A_AND_B`：A=X，Y=A∧B，A=0,C=1两配置完全未选中，其余六种配置存在。
6. `LIMITED_UNSEEN_BRANCH`：A=X，Y=(A∧B)∨(¬A∧C)，同样A=0,C=1两配置未见；两个世界所有**已选择的实际QCA配置/结果与完整所见分布逐原源一致**，但在未观察配置上真值不同。
7. `ALIAS_A_CAUSAL`：A=U，Y=A；所有八配置实际可见A/B/C/Y联合概率与8逐原外生源完全相同，真平均`do(A=1)−do(A=0)`=1。
8. `ALIAS_U_CONFOUNDED`：A=U，Y=U；观察A/B/C/Y与7逐原来源完全相同，真平均do(A)效应0，说明QCA观察充分性A⇒Y不自动证明A对Y的因果操作有效；反例依赖A=U没有共同U层内处理对照。
9. `NEGATED_A_AND_C`：A=X，Y=(¬A)∧C，用于逻辑否定的必要充分检查。

## 完全预冻结的统计及结题口径

A. 枚举全16原source，按S=1观察的实际`A,B,C,Y`构造完整2³=8行真值表。每行保存观察样本源个数、正例数、负例数、一致性=positive/(positive+negative)，当样本计数=0标为**logical remainder**而非“阴性”。严格正例配置阈值是观察行的一致性**恰等于1**，严格阴性配置阈值一致性**恰0**；半数阴阳配置单独标为contradiction，既非正也非真逻辑余项。
B. 统计观察一致性和覆盖率，以任意布尔配置公式P定义`suff_consistency=P(Y=1 | P(A,B,C)=1,S=1)`，`necessity_consistency=P(P(A,B,C)=1 |Y=1,S=1)`。若分母0返回null并注明不定义，禁止以0混淆无充分条件或必要前提。报告观察条件A、B、A∧B及正式最简阳性表达式。
C. 对严格全有据阳性最小析取范式（DNF）枚举27个三变量`{-1,0,1}`模式子立方，−1代表 don't care；以集合覆盖动态规划寻找**能够覆盖所有观察100%阳性配置、且不覆盖任何观察阴性或矛盾配置**的最优布尔析取；conservative 模式还不允许覆盖逻辑余项，parsimonious 模式允许余项作为未检验假设。固定优化次序依次是最少子立方个数、最少总字面量、词典序的模式组合；若无观察阳性结果则空DNF。归档每模式对全8配置的逻辑支持集及覆盖。独立第二路枚举8观察配置真值，并直接评估所得DNF在每个观察行的正确性；对八完整支持世界，若没有矛盾，DNF必须与所有观察配置0/1完全匹配；当有限支持，余项不能当作证实的社会历史案例。这里的自写最小化只限冻结3布尔条件，不等于所有QCA现有软件的完整模型选择策略。
D. `LIMITED_A_AND_B`与`LIMITED_UNSEEN_BRANCH`完整选择数据和真值表、源概率严格相同，但未选中A=0,C=1配置的真Y分别为0与1；非观察来源不能使用来“验证”所归纳的结果。须显示有限多样性对路径推断的弱化。
E. `ALIAS_A_CAUSAL`与`ALIAS_U_CONFOUNDED`完整选择的(A,B,C,Y)观察联合严格相同，在两模型中A观察为充分且必要条件；然而全源人工Oracle do(A)真实平均效果分别1与0。报告人工未测U混杂、给定U下A缺少重叠的确切边界；不扩张为所有具有足够外部实验支持下的QCA因果不可识别性。
F. `CONTRADICTORY_A_XOR_U`的每一配置应恰两行，阳/阴各一，一致性1/2；严格最小DNF空与整个观察人口结果成功率1/2并存，不能把“无可接受的充分配置”误说成从没有Y=1。
G. Python 3.11/3.12各至少50真单测、GitHub Actions第三作业产生全144原来源CSV、九世界源/真值表/最小DNF/observational aliases/干预真值JSON和SHA机读收据，独立审计source概率和、logical remainders、两个完整观察别名与实DO差、最小DNF承诺；成功且归档main之后才出具报告及正式有界结题。冻结接口、未知原源不可见、非因果路径结论不能扩大。
H. 下一原239目录10-014 Inter Coder Reliability Models，拟R240。本项不改变R073或PESEN v0.1。
