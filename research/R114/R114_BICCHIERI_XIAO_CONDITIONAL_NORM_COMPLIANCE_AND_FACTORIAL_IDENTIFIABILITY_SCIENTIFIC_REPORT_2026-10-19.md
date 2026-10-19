# R114 条件性规范遵从：Bicchieri与Xiao一手实验边界及社会预期不一致条件下的可识别性

日期：2026-10-19（Asia/Taipei）
知识目录：P0 条目 03-008 Conditional Norm Compliance。
本文件只覆盖单项模型的原文学习和数学合成反例，**不是** R113 既有2014 Table 2群体百分比的重复归档，不在当前阶段统一分类所有239项或构建PESEN融合模型。

## 1. 第一手文献与获取边界

**一手论文公开摘要，非全文拟合**：Bicchieri, C. & Xiao, E. (2009). Do the right thing: but only if others do so. Journal of Behavioral Decision Making 22(2):191–208. DOI: https://doi.org/10.1002/bdm.621 ，Wiley出版方网页 https://onlinelibrary.wiley.com/doi/10.1002/bdm.621 ，作者第一人所在的 Penn Center for Social Norms and Behavioral Dynamics 原作者论文主页 https://normsandbehavior.sas.upenn.edu/publication/do-right-thing-only-if-others-do-so 。文章出版方标记 **2008-10-16 First published online**，2009为正式期刊卷期；这是一篇论文而非两项独立研究。原摘要报告在独裁者博弈中通过操纵关于过去参与者选择/应当选择的信息来改变实验分配者的社会预期。预期冲突时，**经验预期**对自身选择有显著预测信息；控制经验预期后，**规范预期**额外统计预测影响不显著。这只是论文摘要的作者结果陈述，本项目没有下载其实验逐行行动，也没有重新估计原回归系数、置信区间、p值或实验平均处理效应。不能把“不显著”提升成心理作用永远严格为0。

**同研究团队开放原作者全文的测量边界**：Bicchieri, C., Lindemans, J. W., Jiang, T. (2014). A structured approach to a diagnostic of collective practices. Frontiers in Psychology 5:1418，https://doi.org/10.3389/fpsyg.2014.01418 ，一手开放全文 https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2014.01418/full 。核读“Distinguishing social norms from other collective practices”及原文Table 3/预期操纵说明。作者界定社会规范：社会实践由参考网络中关于他人的经验与规范预期，以及依赖两种预期的条件性偏好支撑；仅取决于经验预期的一类实践可属描述性规范/惯例。2014原文Table 3举的是2009论文已使用的真实信息提示，分别呈现他人**做了什么**或**认为应该做什么**，并以不同方向信息诱导公平/自利预期；它不是本项目构造的四格回归拟合数据。

与R113区别：R113已经做作者2014 Table 1/2概念与不同样本公开百分比的算术复核，本项R114新增检验**偏好条件性与两项预期不一致时的机制识别**，不增加新真人来源或重复记数。

## 2. 规范性分析的必要变量

经验预期 E：关于相关参考网络中他人实际行为的信念。
规范预期 N：关于同一相关网络成员认为何事应做的信念。
个人规范信念 PNB：自己认为何事应做的判断。
当前行为 B：已执行的行动（与预测或表态要分开）。
条件偏好：某人的选择/偏好随E或N改变。**行为与E/N相关并不足以断定因果偏好**，参考网络、环境奖罚、选择、身份、行动时间和心理成本均可能影响结果。依作者定义，仅观察到E与行为相关可支持探索描述性规范，但不能推断E和N同时支撑的社会规范已确认。

二项式互动中的**统计交互项**也不等同于作者社会规范定义。依赖两项信念不必产生非零 E×N 乘积项；反过来，在某个逻辑回归里E×N非零也不证明有明确参考网络、真实规范预期测量或条件性心理偏好。

## 3. 预先冻结的研究者构造四格模型

仅为检测数学可辨识性，自构二元信念水平E,N∈{0,1}与人工Logit：

logit P(B=1|E,N) = α + β_E E + β_N N + β_EN E N，

其中logit(p)=ln[p/(1-p)]。模型系数不来自2009作者估计，无现实心理学单位。每组系数依2026-10-19独立冻结协议设定：

| 合成模型 | α | β_E | β_N | β_EN | 解释 |
|---|---:|---:|---:|---:|---|
| DESCRIPTIVE | -1 | 2 | 0 | 0 | 只响应经验预期 |
| NORMATIVE_ONLY | -1 | 0 | 2 | 0 | 只响应规范预期 |
| BOTH_ADDITIVE | -1 | 1 | 1 | 0 | 两项各自响应，**无乘积交互** |
| INTERACTION | -1 | 1 | 1 | 1 | 附加乘积交互 |

第一项模型与第二项模型在E=N=0及E=N=1的两个**一致条件**下概率完全相同，分别为logistic(-1)≈0.268941和logistic(1)≈0.731059。若观察样本**只覆盖这两个一致条件**，即使有无限精确该两格概率，也无法决定是“别人做了什么”还是“别人认为应当做什么”驱动选择。

但在冲突条件下：
- E=1,N=0：描述性预期模型≈0.731059，纯规范性预期模型≈0.268941；
- E=0,N=1：描述性预期模型≈0.268941，纯规范性预期模型≈0.731059。
BOTH_ADDITIVE模型在这两个冲突格皆为0.5。因而仅收集社会预期相互一致的人群，本来就无法凭相同行为观测识别主导信念来源。

完整四格若每格p∈(0,1)，模型数学上可由
α=logit(p00);
β_E=logit(p10)-logit(p00);
β_N=logit(p01)-logit(p00);
β_EN=logit(p11)-logit(p10)-logit(p01)+logit(p00)
**精确反解四个统计对比参数**。这不是因果推断；若只观测三个格，则在这个不加约束的四参数模型中，交互参数不能唯一确定。即使数学识别全部成功，没有真实随机分配、测量效度和参考网络确认，也无权断言任何效应是由规范施加的。

## 4. 程序与测试

第一手来源与合成冻结：protocols/R114_CONDITIONAL_NORM_COMPLIANCE_FIRSTPARTY_SOURCE_AND_DISCORDANT_EXPECTATIONS_SYNTHETIC_FREEZE_2026-10-19.md

可复算代码：research/R114/r114_conditional_norm_compliance_discordant_expectations.py。
纯合成测试：research/R114/test_r114_conditional_norm_compliance_discordant_expectations.py。

代码稳定计算logistic及反logit（有效概率仅(0,1)），对真实E/N二元水平、有限参数及完整四格失败情形严格拒绝；全四格反算参数，比较两项一致观察的等价与预期冲突时的方向反转。30项合成测试覆盖数值边界、逻辑辨识与无因果声明。实际GitHub CI成功前，测试数仅为提交的候选数量，不报告为完成。

### 科学分级与退出

可成立：2009论文原出版方和原作者研究机构开放摘要叙述、2014原作者全文机制定义、四格数学反例与无形态/极值数值测试（待CI完成）。
不可成立：2009个体数据重放、原回归系数/置信区间再估计、该实验社会规范额外解释力的独立判断、真实个体心理因果、跨制度/跨社会外部验证或未来事件概率预测。

若CI真通过且机读结果SHA归档，将限定学习状态列为 LEARNING_COMPLETE_BOUNDED_PRIMARY_ABSTRACT_AND_MATHEMATICAL_IDENTIFIABILITY；如果不通过，保留失败并修正真实数学/源码错误后再验。绝不擅自扩充2009论文摘要范围或把纯构造系数写成真人效应。R073与PESEN v0.1保持冻结，继续按R系列既有目录选题。
