# R302 科学报告：02-016 双臂Bernoulli后验与Thompson抽样概率的精确有限模型

日期2026-10-23 Asia/Taipei。原始239研究候选ID **02-016 Multi Armed Bandits**（P1）。限定科学结论 **CLOSED_BOUNDED_E1_ARTIFICIAL_R302_THOMPSON_POSTERIOR_ACTION_PROBABILITY**；本轮不是拉杆后的实际奖励实验、不计算累积遗憾、不对人类/动物作策略拟合，也不测试真实历史事件E3。

## 原著核对及独立研究边界

William R. Thompson (1933), *On the likelihood that one unknown probability exceeds another in view of the evidence of two samples*, *Biometrika* 25(3–4):285–294，出版商原始记录 https://doi.org/10.1093/biomet/25.3-4.285。该文对两种未知成功率的后验相对可能性进行推断，为后来的Thompson抽样决策提供理论来源。Auer、Cesa-Bianchi、Fischer (2002), *Finite-time Analysis of the Multiarmed Bandit Problem*, *Machine Learning* 47:235–256，DOI https://doi.org/10.1023/A:1013689704352；原作者论文版本 https://people.eecs.berkeley.edu/~russell/classes/cs294/s11/readings/Auer%2Bal%3A2002.pdf 。这篇文献分析有限时间多臂老虎机的探索与利用、累积遗憾及UCB类算法，**但R302既没有实现UCB1，也没有验证其数学遗憾上界或实证收益水平**。

早期R297 Q-learning涉及多状态MDP中的离策略最优动作值更新，R299涉及固定策略TD/MC预测，R302则仅从两独立Beta后验精确计算抽样下一次选择概率。旧R序列其他RL实证不可无审计直接作为R302新增真人E2证据。

## 事前冻结与人工原数据全集

[完整冻结研究协议](../../protocols/R302_MULTI_ARMED_BANDIT_THOMPSON_BETA_162_SOURCE_PRESCORE_FREEZE_2026-10-23.md)，[事前commit b3c92f9f](https://github.com/edwardsage419/Psychohistory-Research/commit/b3c92f9f013e795a0db4622dc48613f82eb38bca)，均早于研究源码和计算结果。固定两个可获得二元奖励的行动臂A/B，未观测其真实成功率；独立Beta(1,1)先验。每臂已有“成功”和“失败”次数各取0、1、2，交叉构成**3^4=81个人工证据配置**，每个配置分别记录A和B两行，合计**162条完整人工原source**，不是162个实验受试者，也不是随机生成的连续选择历史。

对于任何A臂s个成功f个失败，后验Beta(1+s,1+f)，后验均值a/(a+b)，方差ab/((a+b)^2(a+b+1))，全部精确分数。冻结**确定性贪婪对照**是后验均值大者，严格相等时选择A；Thompson抽样则从每个后验分别抽一个独立成功率参数，按参数大小选择对应臂。本项目不实际抽随机数，而是精确积分得到下一次选A概率P(theta_A>theta_B)，选B=1减该值。连续Beta后验抽样恰好相等概率0，不额外设计随机平局规则。

主程序利用Beta CDF的二项式多项式对精确积分；独立审计**不导入主代码**，使用另一套Beta CDF交错符号幂级数积分公式对162条source独立重算。全部有理数结果严格一致，此外逐source审计两个后验shape、mean、variance、未来选择概率、贪婪选择以及原证据计数。

## 预设检验结果

| 人工观察计数（A成功/失败；B成功/失败） | 后验均值A / B | 贪婪选择 | Thompson下次选A概率 |
|---|---|---|---:|
| 0/0；0/0（没有证据） | 1/2、1/2 | A（平局） | **1/2** |
| 1/0；0/0 | 2/3、1/2 | A | **2/3** |
| 2/0；0/2 | 3/4、1/4 | A | **19/20** |
| 2/2；0/0 | 1/2、1/2 | A（平局） | **1/2** |

对于2成功0失败和对照臂0成功2失败，后验抽样选择较低后验均值的B仍有**1/20**的概率，说明Thompson不是确定性“只选择后验均值高的一臂”。同时所有计数相同的两个臂，下次抽样概率对半分，而贪婪行为通过明确平局规则始终选A。

证据数量不同但均值相同也不会消除后验不确定性：Beta(3,3)方差1/28，小于无证据Beta(1,1)方差1/12，两者均值同1/2，比较任一与均匀Beta(1,1)时P(theta_A>theta_B)=1/2。由此**不能把后验均值等价、后验置信区间等宽、行为选择概率相同混为一个命题**。

严格科学边界：A/B真实奖励成功率从未作为本轮输入或独立真值测量，未执行真实拉杆，不存在实际累计奖励、真实最优臂、遗憾、反馈后自适应策略评价。上述选择概率是对给定人工**后验分布**下一次Thompson行为随机性的数学陈述，不表示真实人群的探索比例或算法收益水平。原论文2002年对后悔界的结果不由本研究重新证明。

## 可复现性验收

[原生主程序及660项实际unittest](r302_exact_beta_thompson_bandits.py)；
[162条完整原始人工两臂来源CSV](R302_ALL_162_ORIGINAL_BETA_BANDIT_ARM_SOURCES.csv)；
[全部81世界完整后验与选择概率JSON](R302_EXACT_BANDIT_THOMPSON_RESULTS.json)；
[原来源/结果SHA256凭证](R302_MACHINE_RECEIPT.json)；
[独立另一种Beta积分与17项篡改攻击测试](../catalogue_audit/independent_r302_source_audit.py)。

真实[GitHub Actions run39930778614](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39930778614)，三个CI job completed/success，Python3.11和3.12分别通过660项主模型测试与17项独立审计。第三job重新生成所有162条源、完全重算独立Beta积分与哈希，并将CSV、结果JSON及SHA256永久提交main [commit25b895e3](https://github.com/edwardsage419/Psychohistory-Research/commit/25b895e30416f109d38e6bd083163ff08d0d5dd0)。

本轮没有新增人/动物E2、历史E3；原始R073和PESEN v0.1持续冻结。研究顺序为全部R系列完成后统一分类，再尝试熔炼，不把本人工机制过早当作人群决策规律。
