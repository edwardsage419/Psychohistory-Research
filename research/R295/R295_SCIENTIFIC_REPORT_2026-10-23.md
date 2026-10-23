# R295 科学报告：01-019 习惯形成、情境线索与奖励贬值的精确人工反例

日期：2026-10-23 Asia/Taipei。正式对应原239目录01-019 Habit Formation，优先级P1。**接受范围仅为有限人工数学E1**。无真人习惯养成行为、动物奖励贬值实验复算、习惯自动性问卷拟合、真实历史事件或神经证据E2/E3。

## 文献直接锚点与解释范围

Dickinson (1985), *Actions and habits: the development of behavioural autonomy*, *Philosophical Transactions B*, 308:67–78, 原作者论文版本 https://www.princeton.edu/~yael/LearningCourse/Targilim/Dickinson1985.pdf；Wood & Neal (2007), *A New Look at Habits and the Habit-Goal Interface*, *Psychological Review* 114(4):843–863, DOI https://doi.org/10.1037/0033-295X.114.4.843；Lally et al. (2010), *How are habits formed: Modelling habit formation in the real world*, *European Journal of Social Psychology* 40:998–1009, DOI https://doi.org/10.1002/ejsp.674。以上资料分别讨论目标重估与习惯的区分、情境–反应联结与目标交互、日常行为自动性发展。**R295采用的训练系数、控制权重、两行动评分及所有数值均为本研究自行构造，不可描述成原作者模型参数、论文被试数据或已被证实的人类习惯形成公式。**

原2026-10-18知识叠加文件的01-019并无可确认逐项first_hand_source_id，现有早期ZIP扫描证据也无此特定目录ID。此前R系列强化学习、历史行为研究可能有概念重叠，但本轮专门冻结情境切换与奖励贬值的区别，并不声称检查了过去全部源码中所有可能的习惯机制。

## 事前协议、原始宇宙与精确计算

[先行冻结完整协议](../../protocols/R295_HABIT_CUE_DEVALUATION_180_ORIGINAL_STATES_PRESCORE_FREEZE_2026-10-23.md)，GitHub [638948a4](https://github.com/edwardsage419/Psychohistory-Research/commit/638948a4fb2fdcc370dbbc2c2f9f634f4d61a57b)。

人工训练率α∈{0,1/2,1}，训练重复n=0..4；可检索的人工情境–行动关联强度H_0=0且H_(n+1)=H_n+α(1−H_n)，精确H_n=1−(1−α)^n。习惯控制份额λ∈{0,1/2,1}，情境匹配cue∈{0,1}，当前结果价值V∈{0,1}，备选行动B固定得分1/2。选择A的人工合成综合得分 U_A=(1−λ)V+λ·cue·H_n；若U_A>1/2选择A，其余含严格相等一律选择B。

完整交叉得到3×3×2×2×5=**180条标签完全列举的确定性人工source**，36个控制世界每个5个训练点。将同学习率、λ、cue、训练重复次数下的V=1和V=0作严格一对比较，得到**90组**奖励贬值配对检查。所有计算使用Fraction，不通过随机模拟、实时拟合或隐藏未来行为选择。

## 预定理论反例与实际源级结果

| 人工控制权重 | 配对数 | 贬值使选择A→B的配对数 |
|---|---:|---:|
| λ=0 完全目标控制 | 30 | **30** |
| λ=1/2 混合控制 | 30 | **8** |
| λ=1 仅习惯关联控制 | 30 | **0** |

在λ=0条件，cue与训练强度都不改变因价值下调发生的A→B反转；在λ=1条件，同一cue下足够强的已学习关联持续选择A，价值V从1改为0也不改变行动，但cue变化为0时不再触发A。λ=1/2时是否价值敏感依习惯强度与即时目标份额的合成分数而变化，其8/30是人为指定网格产生的数量。

α=1/2时H_0=0，H_1=1/2，H_2=3/4，H_3=7/8，H_4=**15/16**。对于n=4、cue=1：

* 习惯λ=1：V=1与V=0两种情况都选择A；把cue切换为0，两者都选择B。
* 混合λ=1/2：V=1时U_A=**31/32**选择A；V=0时U_A=**15/32**选择B。
* 目标λ=0：V=1时选A，V=0时选B，与cue及历史无关。
* α=0：H永远为0，纯习惯控制无法选A，确认先前重复历史的必要性是模型内的假设性质。
* 严格平局选B，避免后验调节临界样本预测。

这些反例明确展示**行为重复、情境检索和当期结果价值**的区别。由于本模型直接用λ定义“习惯占比”，其贬值不敏感是模型机制所赋予的性质；没有从人类行动中估计λ，也没有排除竞争模型（如强化学习、环境奖励约束、目标未改变等）。因此不能由本研究将真人出现重复行为直接诊断为习惯、也不能推断特定干预对真实习惯形成或改变的有效性。

## 实际执行与独立来源重算

[主程序，731项实际unittest](r295_exact_habit_cue_devaluation.py)；
[180条人工原source](R295_ALL_180_ORIGINAL_HABIT_CUE_REVALUATION_STATES.csv)；
[90组完整贬值配对和精确计数结果](R295_EXACT_HABIT_CUE_AND_DEVALUATION_RESULTS.json)；
[原来源与结果SHA256收据](R295_MACHINE_RECEIPT.json)；
[完全不导入主程序的180原来源、90配对重新计算及14项逆向攻击测试](../catalogue_audit/independent_r295_source_audit.py)。

[GitHub Actions run39920355215](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39920355215)三个job completed/success。Python3.11、3.12两边各731项主模型unittest和14项独立来源审计通过；第三job完全重新计算并比对来源摘要，且永久提交[commit324eced6](https://github.com/edwardsage419/Psychohistory-Research/commit/324eced68a19401078b1c60d72c83ae77549b30b)。

正式科学限定状态：CLOSED_BOUNDED_E1_ARTIFICIAL_R295_HABIT_CUE_OUTCOME_DEVALUATION。新增真人E2=0、历史E3=0，原文数据复算=NO。R073与PESEN v0.1继续冻结。原始239全部学习完成后才统一分类，最后开展模型熔炼。
