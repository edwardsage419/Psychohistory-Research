# R299 科学报告：无模型强化学习、在线TD(0)与Monte Carlo完整回报估值

日期：2026-10-23 Asia/Taipei。原239候选编号**02-005 Model Free Reinforcement Learning（P1）**。正式科学验收范围只限**人工有限数学E1**：固定策略状态价值预测，不涉及行为选择政策优化、不拟合真实人/动物实验，也不产生历史E3证据。R073及PESEN v0.1冻结。

## 原始作者文献与R063历史范围的严格区分

Sutton, R. S. (1988), *Learning to Predict by the Methods of Temporal Differences*, *Machine Learning* 3:9–44, DOI https://doi.org/10.1007/BF00115009；[原始论文档案](https://mlanthology.org/mlj/1988/sutton1988mlj-learning/)、[原文PDF](https://jmvidal.cse.sc.edu/library/sutton88a.pdf)。Sutton & Barto, *Reinforcement Learning: An Introduction*, 第二版Chapter6 关于TD与Monte Carlo直接从经验进行无模型政策评价的区别，[作者原版在线教材](https://incompleteideas.net/book/RLbook2020.pdf)。这些一手资料支持机制定义，R299全部数字、奖励和两状态链均是本项目预先人工构造，不是上述原作者测量或拟合结果。

原始候选02-005的历史[**R063真实机制审计**](../R063/R063_EVIDENCE_AUDIT.md)分析Najar、Bonnet、Bahrami、Palminteri (2020), *The actions of others act as a pseudo-reward to drive imitation in the context of social reinforcement learning*, [PLOS Biology原文](https://doi.org/10.1371/journal.pbio.3001028)。R063原作者固定提交554ee8007ff6fd1c51cd68d7d254f22a34e6dab1，实读metaVS.m和VS2.m，澄清社会模仿率更新、该状态先前私人历史门控、参数不可直接类比，并复核Fig6汇总值及精确检验。**R063的作者生成数据与既有统计结果不重新标记为R299的通用无模型强化学习真人验证，也不取代R063本身缺少完整trial CSV本地端到端拟合的开放关口。**

另R297对应原02-003 Watkins–Dayan Q-Learning离策略动作最优化；R298对应原02-004已知模型式规划。R299专门学习一个固定策略的**无动作选优、不使用环境转移模型**的TD(0) vs MC时序预测机制。因此三项数学机制具有关系，但不能借此称为三项独立真人实证复现。

## 事前冻结的全源宇宙

[事前冻结完整协议](../../protocols/R299_MODEL_FREE_TD0_VS_MONTE_CARLO_24_WORLDS_120_SOURCE_PRESCORE_FREEZE_2026-10-23.md)，commit [f8885c13](https://github.com/edwardsage419/Psychohistory-Research/commit/f8885c130b2d6d12280cd6ace30085b3ad90e835)，先于R299源码、数据或计算。

冻结固定的确定性回合序列为S0 --奖0--> S1 --奖R--> 终端；R∈{0,2}，折扣γ∈{0,1/2,1}，步长α∈{1/2,1}。每一个同参数合成世界应用TD0_ONLINE或MC_FULL_RETURN两种无模型预测更新，训练前n0与训练后的n1..4都完整保存。故**2×3×2×2=24个人工世界，每世界5行，共120条确定性人工原source状态**，不是120个人、没有随机试次或真实奖励观察。

两方法看到完全一样的回合序列，每次都从上一轮完整状态起更新。

* TD(0)在线：先在S0更新δ0=γ V_old(S1)−V_old(S0)，再到回合终端更新S1的δ1=R−V_old(S1)。**S0不能在当前回合先偷看S1之后的新估计**。
* Monte Carlo完整回报：等待回合结束，把S0的回报目标设为γR，S1目标设为R，并以同样学习率更新两状态。
* 终端不自举。没有任何转移估计、下一动作最大值、Q控制参数搜索或实证留出拟合。

全部源行含世界ID、奖励、折扣、学习率、方法、训练轮次、两个状态旧价值、更新目标及误差、两个新价值、oracle策略回报与绝对误差；所有分数采用Python Fraction精确分数。

## 独立解析式与反例

设q=1−α、n为训练回合数。两算法V_n(S1)=R(1−q^n)，蒙特卡洛V_n(S0)=γR(1−q^n)。在线TD(0)先得到V_0(S0)=0；对n≥1：

`V_n(S0)=γR[1−q^n−α n q^(n−1)]`。

后一项是当前迭代中旧S1估计形成的延迟传播差异，不是通用MDP优劣定理。程序按原冻结先后顺序递推，另以闭式公式独立验算，**全部120条原source逐值相等**。第三不导入主程序的审计又独立重建、检验所有原source/结果。

| 人工世界和冻结对照 | TD(0) | Monte Carlo | 两算法共同 |
|---|---:|---:|---|
| R=2, γ=α=1/2，第四轮S0估值 | **11/16** | **15/16** | 真值S0=1 |
| 同一设置第四轮S1估值 | 15/8 | 15/8 | 真值S1=2 |
| R=2, γ=1/2, α=1，第一轮S0估值 | 0 | 1 | 真值S0=1 |
| 同一设置第二轮S0估值 | 1 | 1 | 真值S0=1 |

在本任务内，TD(0)的旧S1目标意味着早期S0奖励信息延后传递；MC结束整轮即能用真实回报更新S0。但MC需要先观察完整回合，并不能由这个特例推论在含噪声、截断或长回合任务中MC有更低方差、更高样本效率或始终优于TD。

**必要负对照：** 若R=0，两个状态估值及所有更新误差恒0；若γ=0，两个算法的S0估值恒0，但S1仍能学习终端奖励R。α=1时TD首次S0为0、第二次才得到此前S1新学到的价值。反之本研究不为真人指定实际折扣和学习率，也未验证一般情形的收敛定理。

## 源码审计、来源指纹与正式科学等级

[主原生程序与492项单元测试](r299_exact_model_free_td_mc.py)；
[120完整原人工源状态CSV](R299_ALL_120_ORIGINAL_MODEL_FREE_TD_MC_STATES.csv)；
[24人工世界×5轮完整结果JSON](R299_EXACT_MODEL_FREE_TD_MC_RESULTS.json)；
[原source和完整结果SHA256凭证](R299_MACHINE_RECEIPT.json)；
[完全不导入主模型的120条来源复算及16项逆向检验](../catalogue_audit/independent_r299_source_audit.py)。

[GitHub Actions run39927231561](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39927231561)：Python 3.11/3.12两套各492项主模型单测+16项独立审计全部通过，第三独立job重新生成并核验全部源、公式、结果及哈希，三个作业completed/success。全部原CSV/JSON/SHA已永久归档[commit8f74e565](https://github.com/edwardsage419/Psychohistory-Research/commit/8f74e56573be6a9fde21e12bb886c9f041d3f74b)。

最终有界等级**CLOSED_BOUNDED_E1_ARTIFICIAL_R299_TD0_MC_FIXED_POLICY**。不再为原始R063未取得的完整真实trial数据补造结果；不修改R073或PESEN v0.1；不增加真人/动物E2、历史E3，也不承诺全部239候选已满足实证科研验收。
