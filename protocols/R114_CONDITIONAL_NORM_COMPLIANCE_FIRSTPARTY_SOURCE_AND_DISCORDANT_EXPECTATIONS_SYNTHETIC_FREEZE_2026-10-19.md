# R114 条件性规范遵从：原论文范围、预期冲突与数学可辨识性预冻结

冻结日期：2026-10-19（Asia/Taipei）
知识目录定位：既定239候选条目 P0 / 03-008 Conditional Norm Compliance。R114是研究阶段编号，不把R号与模型目录ID混同。
类型：原始出版方来源学习 + 纯合成数学反例。没有真人微观数据输入、参数拟合或行为E2。此协议在生成或执行本阶段的合成数值案例之前提交。

## 固定第一手来源与证据范围

一手研究：Bicchieri, C. & Xiao, E. (2009), Do the right thing: but only if others do so, Journal of Behavioral Decision Making, 22(2), 191–208，doi:10.1002/bdm.621。出版方全文可能需付费，本研究只将出版方Wiley开放摘要与第一作者所在Penn Center for Social Norms and Behavioral Dynamics所存论文摘要作为核读依据：
- https://onlinelibrary.wiley.com/doi/10.1002/bdm.621
- https://normsandbehavior.sas.upenn.edu/publication/do-right-thing-only-if-others-do-so

原作者公开延伸论述：Bicchieri, Lindemans & Jiang (2014), A structured approach to a diagnostic of collective practices, Frontiers in Psychology 5:1418，doi:10.3389/fpsyg.2014.01418，官方开放全文 https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2014.01418/full 。其中“辨别社会规范和其他集体行为”部分明确社会规范需要：参考网络中的经验预期、规范预期以及对这些预期有条件性的偏好；仅依赖经验预期的实践属于描述性规范/惯例类别。

2009年实验开放摘要报告：在该独裁者博弈的预期操纵情境下，冲突时经验预期显著预测分配行为，控制经验预期后规范预期没有额外显著预测力。该结论仅可按公开原摘要范围准确转录，不得将“不显著”理解为严格零效应、普适定律或本项目独立回归复验；不得臆造人数、系数、置信区间和处理大小。2008-10-16的online-first和2009年第22卷为同一论文，不算两个实验。

## 本轮冻结的纯合成数学课题

变量 E,N 各取0或1，分别表示同一明确定义参考群中经验预期/规范预期是否处于高状态，是研究者的合成因子，不等于真实测量百分比。对行动 A 设人为定义的logit形式：

logit P(A|E,N) = alpha + beta_E E + beta_N N + beta_EN E N.

此方程仅是自构的结构辨析工具，不属于2009作者原模型、原结果的再估计，也不构成社会规范的充分判定标准。为方便精确计算，冻结四种数学机制参数：
- DESCRIPTIVE = (-1, 2, 0, 0)，只响应经验预期；
- NORMATIVE_ONLY = (-1, 0, 2, 0)，只响应规范预期；
- BOTH_ADDITIVE = (-1, 1, 1, 0)，两项预期都有关联；
- INTERACTION = (-1, 1, 1, 1)，含额外交互。

精确四格顺序为 E0N0、E1N0、E0N1、E1N1。对角一致条件 E=N 的概率：
- DESCRIPTIVE 与 NORMATIVE_ONLY 在E0N0和E1N1完全相等；仅靠这些观察不能判别哪一种预期控制行为。
- 在E1N0和E0N1预期冲突的条件下，两种概率相反；单纯增加同向观察无助于识别。
- 上述BOTH_ADDITIVE则在两个冲突格概率为0.5，说明即使都与两种预期有关，也未必存在乘积交互。
- 完整四格对数几率交互对比为 logit(p11) − logit(p10) − logit(p01) + logit(p00) = beta_EN。仅有三格时不允许声称完整自由交互系数可识别。

必须测试边界和错误输入：所有实数参数有限；E和N是显式二元0/1，不接受布尔、字符串、缺格重复等；数值稳定的sigmoid和反logit仅可对严格(0,1)输入取logit；四格全存在才能反解参数，任何缺失格与非法概率应fail-closed。独立合成数据的可运行单位测试不少于20项，CI实际通过后才能记合成数学学习完成。

## 科学防误读

完整四格的数学识别不等于随机化实验、受试者实际预期操纵成功、因果效应识别或心理机制识别。真实研究还需要明确的参考人群、对E/N的测量有效性、可操作干预、分配随机性、遵从、信息排除限制、退出与社会网络扩散干扰等。即使beta_EN在合成四格中可估计，也不能仅据此称“社会规范存在”。EE/NE/实际行为/个人规范信念不得混同。

严格沿既定R研究顺序推进，每阶段代码与测试及失败归档GitHub main。R073冻结模型与评分规则不修改，PESEN v0.1继续冻结。不得借本阶段先行对全239模型分类、熔炼或建立个人决策系统。
