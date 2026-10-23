# R236 调查回答偏差模型：九个有限答卷—真实私人状态机制、576原外生来源及问卷模式效应混淆，评分前冻结

日期：2026-10-23（Asia/Taipei）。原始239模型目录 `10-010 Survey Response Bias Models`（P1），编号R236。全部人工E1。本项只讨论真实私人态度、作答应答、问卷模式与辅助核验数据之间的测量机制，不能据此确认现实公众态度、受访者真实性、历史民意变化或实际谎报率；新增真人E2=0、历史E3=0。R073/PESEN v0.1冻结。

## 一手资料和研究边界

Tourangeau, Rips & Rasinski (2000), *The Psychology of Survey Response*, Cambridge University Press, [原出版社第一章摘录](https://www.cambridge.org/core/books/psychology-of-survey-response/0FC3B13C5ABDC0B6452A3B6D428D3983)（确切出处以原书书目信息为准）；Krosnick (1991), *Response Strategies for Coping with the Cognitive Demands of Attitude Measures in Surveys*, *Applied Cognitive Psychology* 5:213–236, DOI https://doi.org/10.1002/acp.2350050305，[原作者PDF](https://web.stanford.edu/dept/communication/faculty/krosnick/docs/1991/1991%20Satisficing.pdf)，从认知努力与回答策略解释社会认可、顺从及满意化作答。本R只构造有限人工测量反例，不声称原作者曾采用本文九个人工生成模型，不以人工模型量化原样本真实心理策略频率。

## 全部原结构外生源、核验记录及随机模式

六个独立Bernoulli(1/2)二元外生源 `T,S,U,R,E1,E2`，取0或1。T和S分别标记两个私人问题的起始真状态，U是个人隐藏响应策略/顺从者状态，R是独立随机的问卷模式处理（0/1），E1/E2决定两条外部先验代理是否被观测。每世界2⁶=64条完整互斥原来源，各原质量1/64；九世界**576条完整源**。

每条记录实际观察五变量为`(R,P,Z,Y1,Y2)`：P和Z是两个对问卷前真实T的部分核验代理，当E1=1时P=T、否则P=−1表示缺失；当E2=1时Z=T、否则Z=−1（独立，各有半数核验概率）。这两项不是现实理想无误差测谎工具，仅是冻结人工的前期局部核验，且**不直接测量模式之后的新私人真实状态B1**。Y1/Y2是两道回答，真实当前私人态度B1/B2只在人工oracle可见，严禁进入实际观察估计器或MH等拟合。

## 冻结九个人工世界

1. `TRUTHFUL_STABLE`：B1=T，B2=S，Y1=B1，Y2=B2；模式R对真态度与回答均无效。
2. `TRUE_MODE_CHANGE`：B1=T OR R，B2=S，Y1=B1，Y2=B2；随机模式真实改变当下私人B1的`do(R)`效应均值1/2。
3. `REPORT_MODE_CHANGE_ALIAS`：B1=T，B2=S，Y1=T OR R，Y2=S；随机模式仅改变回答，真B1的do(R)效应0。**2/3的五变量实际观察在64全部来源逐点相同、完整观察联合分布一致，但私人真态度因果效果1/2 vs 0**。
4. `TRUE_MODE_COMPLIER_ONLY`：B1=T OR (R AND U)，B2=S，Y1=B1，Y2=S，真do(R)私人态度效应1/4。
5. `REPORT_MODE_COMPLIER_ONLY_ALIAS`：B1=T，B2=S，Y1=T OR (R AND U)，Y2=S；私人态度效应0，但**4/5观测五变量逐源完全一致**。
6. `SOCIAL_DESIRABILITY_U`：B1=T，B2=S，实际Y1=T OR U、Y2=S OR U；真私人B1/B2彼此独立协方差0，但因共享私人响应风格U使实际Y1/Y2可见协方差正。
7. `MODE_SUPPRESS_REPORT`：B1=T，B2=S，Y1=T AND (NOT R)，Y2=S；报告Y1对随机模式的观察差是−1/2，但真私人B1因果模式效应0。
8. `SHARED_ACQUIESCENCE_RESPONSE`：B1=T，B2=S（人工真不同私人概念独立）；Y1=T、Y2=Y1。回答层面模仿第一答案/机械同答造成两道观测回答完全相关。
9. `SHARED_TRUE_CONSTRUCT_ALIAS`：B1=T，B2=T，Y1=T、Y2=T。第8/9世界对所有实际R/P/Z/Y1/Y2**逐源完全相同**，私人B1/B2真实Cov分别0和1/4。共同回答方法可与真正共同私人构念在一次答卷观察上等价。

## 冻结统计、独立检验与结题门槛

A. 对每世界全64源直接计算完整观察`P(R,P,Z,Y1,Y2)`（包含−1缺失值）及随机模式观察`ITT_Y1=E[Y1|R=1]−E[Y1|R=0]`。只读实际观察五列。另按人工真私人结构对每外生源保持T/S/U/E固定施加`do(R=1)`与`do(R=0)`，计算**真私人B1模式效应**。固定独立理论检验九项真效应：`0,1/2,0,1/4,0,0,0,0,0`。两类效果分开，不能把观察ITT=真实私人状态改变。
B. 由全源计算真实`Cov(B1,B2)`、实际`Cov(Y1,Y2)`、两道题真回答不一致的人工率。SHARED_ACQUIESCENCE_RESPONSE是真私人Cov0、可见回答Cov1/4；SHARED_TRUE_CONSTRUCT_ALIAS真私人Cov1/4、可见回答Cov1/4。SOCIAL_DESIRABILITY_U真私人Cov0、可见回答Cov1/16。全部Fraction。
C. 独立第二算法不读取全源CSV，从四个原外生T/S/U/R的16状态及问卷前两个独立核验代理出现/缺失的`1/2×1/2`概率积分，得完整观察五变量概率，并与64原源联合逐格校验；对效应另用人工布尔函数独立枚举固定T/S/U得到上述真模式效果。
D. 三对完整观测等价须逐64原来源一项项检验，包含两个部分核验代理、随机模式与双题观测：TRUE_MODE_CHANGE/REPORT_MODE_CHANGE_ALIAS，TRUE_MODE_COMPLIER_ONLY/REPORT_MODE_COMPLIER_ONLY_ALIAS，SHARED_ACQUIESCENCE_RESPONSE/SHARED_TRUE_CONSTRUCT_ALIAS。对第3对报告实际答卷内真实私人构念之间Cov显著不同（此处‘显著’只指Fraction非零差，不是样本统计显著性）。
E. 模式的随机分配只识别在人工条件下对**实际观测报告**的因果ITT，若没有独立有效的模式后真私人状态测量，不能宣称随机模式对私人态度影响一定被识别。多次独立附加外部测量可能产生新信息，本R不模拟真实纵向方案。所有匿名二元标签没有现实政治/文化对应。
F. Python3.11/3.12各≥45测试，第三Actions独立门槛重新生成全部576原结构源CSV、九世界结果JSON、SHA256机器凭证，验证三对逐源观察等价、真实模式效果、两题观察/私人相关差，永久提交main。失败记录需真实保存，正式有界验收仅根据真实CI与源归档。
G. 全部人工E1、真人人级E2新增0、真实历史E3新增0。下一原239目录顺序以真实目录查询为准。原R主线完成后才统一分类、最终熔炼。
