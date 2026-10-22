# R227 经典测验理论：八人工双项目世界，128单次完整来源及1024跨次配对原来源，评分前冻结

日期2026-10-23（Asia/Taipei）。原始239目录真实条目 **10-001 Classical Test Theory（P1）**，研究编号R227。只检验人工完全有限随机测量下的原式、跨次独立性、测量误差相关性、两项目α及重复施测信度的边界，科研资格E1。R073及PESEN v0.1继续冻结，不添加真人E2或真实历史E3。

## 第一手文献及阅读范围

* Novick (1965), *The Axioms and Principal Results of Classical Test Theory*, ETS Research Bulletin RB-65-02, https://www.ets.org/research/policy_research_reports/publications/report/1965/hpeu.html；以及 Novick (1966), *The axioms and principal results of classical test theory*, *Journal of Mathematical Psychology*, DOI https://doi.org/10.1016/0022-2496(66)90002-2。文献讨论真分数和误差的定义、平行测量以及独立性条件。当前实际核阅出版社/ETS原文摘要及书目信息，未声称取得并复算全文的所有推导。
* Cronbach (1951), *Coefficient Alpha and the Internal Structure of Tests*, *Psychometrika* 16:297–334, DOI https://doi.org/10.1007/BF02310555。当前核阅原出版方摘要和ETS记录；不声称复原1951文内全部例子。
* Raykov 等 (2015), *The Importance of the Assumption of Uncorrelated Errors in Psychometric Theory*, 公开文献 https://pmc.ncbi.nlm.nih.gov/articles/PMC5965613/，讨论误差相关会影响经典测量推断。作为附加方法背景，并非R227原作者的实证复算。

## 结构与严格意义上的“真分数”

一个人工受试者的**稳定真特征** T∈{−1,+1} 且 P(T)=1/2。每次施测有三个独立等概率误差来源 E1,E2,M∈{−1,+1}，且与T独立。M可在**同一次**施测的两个项目之间共享；下次施测必须重新独立抽取E1',E2',M'，保持**同一个**稳定T。每单次世界有2×2³=16个完整外生状态、每行概率1/16；八世界共128原来源。每世界连续两次测验的完整互斥原来源有2×8×8=128条、每条概率1/128；八世界共1024条**二次施测来源对**，每对明确保留同一个T与两次不同的三元误差，不将1024条当成真实人。

两个项目分数 X,Y。固定每个人在某个世界下的项目真分数为 (q_X(T)=E[X|T])，(q_Y(T)=E[Y|T])。测验总分 S=X+Y，真总分 (q_S(T)=E[S|T])，人工oracle真信度 (r_{m true}=Var(q_S(T))/Var(S))，两次独立误差且相同量尺条件下 (r_{m retest}=Cov(S^{(1)},S^{(2)})/Var(S))。**仅测量T被视为跨次稳定**；共享方法噪声M每次重抽，因此单次“α很高”可能属于不稳定的共同误差。

## 预冻结八个具体世界

所有运算整数/精确Fraction，保持这些生成式与外生概率不变：

1. PARALLEL_INDEPENDENT: X=T+E1, Y=T+E2。项目方差均2，协方差1，α=2/3，真实信度及跨次相关2/3。
2. SHARED_METHOD_WITH_TRAIT: X=T+E1+M, Y=T+E2+M。项目方差均3、协方差2，α=4/5，真实信度及跨次相关2/5。
3. PERFECT_TRAIT: X=T, Y=T。观察项目联合分布为X=Y=±1各1/2，α=1，真实信度1，跨次相关1。
4. PERFECT_METHOD: X=M, Y=M。**观察单次完整P(X,Y)与PERFECT_TRAIT完全一致**，α=1，但真分数相对稳定T始终0，真实信度0，跨次相关0。此世界的M是每次重抽的共同误差，而非个体固定方法特质。
5. UNEQUAL_ERRORS: X=T+E1, Y=T+2E2。项目方差2和5，协方差1，α=4/9，真信度4/9；错误方差不等，违反严格平行测验。
6. OPPOSING_METHOD: X=T+M, Y=T−M。项目方差各2、协方差0，α=0，总分S=2T没有误差，真信度1。
7. OPPOSING_TRAIT: X=T+E1, Y=−T+E2。项目方差各2、协方差−1，α=−2，总分S=E1+E2与稳定T无关，真信度0。
8. NON_EQUIVALENT_ITEM: X=T+E1, Y=2T+E2+1。项目方差2和5、协方差2，α=8/11，真信度9/11。项目因子载荷和项目均值不同，α不能直接当作总分真信度。

## 预冻统计、双路径验算与不可识别边界

A. 对各单次人工原来源计算人口均值、Var(X)、Var(Y)、Cov(X,Y)、Var(S)并用(alpha=2[1-(Var(X)+Var(Y))/Var(S)]=4Cov(X,Y)/Var(S))求两项目 α。若Var(S)=0必须返回NULL和相应原因，绝不杜撰结果。计算各T条件真分数及真总分方差，必须与**独立直接符号方差法**完全一致。

B. 将八世界全部两次独立重抽误差的原来源对完整枚举，计算两次分数Cov(S1,S2)、跨次信度比Cov/Var(S1)，并独立确认与Var(q_S(T))/Var(S)相等。这是按固定T跨次独立误差生成式成立的模型内数学等式，不能在现实测验未知是否存在记忆、学习、疲劳时直接套用。

C. 对PERFECT_TRAIT与PERFECT_METHOD计算完整`P(X,Y)`和双次`P(S1,S2)`联合分布，必须前者完全一致、后者不一致（真信度1与0）。可检测“单次测验无法识别稳定信度”，新一次真正独立施测有额外识别信息。

D. 用所有四个固定误差/真特征单源验证八个预冻解析恒等式：项目Var/Cov、α、真信度、重复信度。每世界源质量归一，每跨次pair质量归一；单次原来源不同时充当新独立测验观测。对共享误差非零协方差、反向误差负协方差、两个项目真分数偏离平行条件给明确诊断。

E. 执行至少40项Python标准库单测，CI在Python3.11/3.12两环境独立运行；第三CI作业真实生成所有**128单次原来源及1024跨次配对原来源CSV**、八世界Exact Fraction结果JSON、三项SHA256机读收据，并永久归档main。失败需留存，不得把GitHub run成功与jobs元数据、实际测试日志相混淆。源码及结果只能在协议先独立冻结并提交之后生成。

F. 仅E1人工、无原作者真人测验微观数据、无现实测试情境的量尺等值性/时间稳定性/预测效度/因果识别。下一实际目录10-002 Item Response Theory，拟R228；先完成原全部R再统一分类、最后熔炼。
