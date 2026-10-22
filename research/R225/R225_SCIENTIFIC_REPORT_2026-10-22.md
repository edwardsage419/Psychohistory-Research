# R225 自然实验可信性：六个人工分配世界、576条完整来源与观察分布等价的因果反例

日期：2026-10-22。原239研究目录 **09-016 Natural Experiment Designs（P1）**。有界科学状态 **CLOSED_BOUNDED_E1_FINITE_ARTIFICIAL_NATURAL_EXPERIMENT_DESIGNS**。没有真实外部政策、自然灾害、地区配置、真人实验或历史事件作为经验数据。

## 方法学及独立事前冻结

方法背景包括 Dunning (2008), *Improving Causal Inference: Strengths and Limitations of Natural Experiments*, DOI https://doi.org/10.1177/1065912907306470；Dunning (2012), *Natural Experiments in the Social Sciences*, Ch.8, DOI https://doi.org/10.1017/CBO9781139084444.012；Titiunik (2021), *Natural Experiments*, DOI https://doi.org/10.1017/9781108777919.008；以及 Hernán and Robins (2006), *Estimating causal effects from epidemiological data*, DOI https://doi.org/10.1136/jech.2004.029496。方法共识是明确安排机制及可交换性假设、处理时点和研究对象，不能用“外部发生”直接替代因果识别。具体自然实验的称谓与严格定义在文献中有争论；本项目只做固定人工因果机制压力测试，不以模拟冒充实际自然实验研究。

[六世界预先冻结方案](../../protocols/R225_NATURAL_EXPERIMENT_6_WORLDS_576_ORIGINAL_SOURCE_PRESCORE_FREEZE_2026-10-22.md)独立先提交 [7fb54ef2](https://github.com/edwardsage419/Psychohistory-Research/commit/7fb54ef2158bb5e3934e5d7a72bbd135ad891ac9)，随后实现模型与CI。模型的结构函数、六种配额、固定噪声与目标真ATE保持原冻结不变。

## 完整原来源与分析对象

固定4个匿名单位，正式处理post前有单一前期水平pre。每次外部配额恰2个单位处理，共6个可能向量，原六模式概率各1/6；各单位后期独立±1/4噪声，共16种真实有限扰动，每世界96个完整原结构来源，六世界总576行、每行1/96。4单位值只是人工标号，没有观测社会背景。分析程序仅由实际分配、实际pre和post计算三种估计：post处理与对照均值差、pre期处理与对照安慰剂水平差、两期变化差的组间差。真实平均干预效果（ATE）只使用相同结构来源下人工Y1−Y0 oracle。

第二套独立闭式来源对每一个处理组合直接将±1/4噪声均值置0计算条件估计期望，再将四个独立噪声给出的必然条件方差1/16及6个配置条件均值波动方差相加；逐96来源的Fraction估计均值与方差严格逐项一致。

## 完整结果与真假自然识别机制

| 人工世界 | 真ATE | 观察post组差期望 | pre安慰剂水平差 | DiD期望 |
|---|---:|---:|---:|---:|
| AS_IF_RANDOM_VALID | 1 | 1 | 0 | 1 |
| ENDOGENOUS_FUTURE_SHOCK_ALIAS | 0 | 1 | 0 | 1 |
| AS_IF_RANDOM_NULL | 0 | 0 | 0 | 0 |
| AS_IF_RANDOM_HETEROGENEOUS | 3/2 | 3/2 | 0 | 3/2 |
| ENDOGENOUS_VISIBLE_SELECTION | 0 | 1 | 1 | 0 |
| ANTICIPATORY_PRE_RESPONSE | 1 | 1 | 1/2 | 1/2 |

**最强反例：第一与第二世界的完整观察联合概率P(Z向量,pre四人向量,post四人向量)逐状态完全一致**。六个处理模式、四人各自pre期水平、四人每种post后期噪声实现概率全部相同。两者前期平衡安慰剂值均严格0，处理组比例均1/2，观察post及DiD效果期望均1；第一世界的Z真外生且真ATE=1，第二世界的Z完全由潜在未观察未来冲击U驱动，实际处理D对post无效，真ATE=0。因此任何只读上述完整观察分布的估计、置换检验或平衡统计都无法区分这两个机制。真实因果效果的区分依赖于外部制度、赋值过程或有效独立额外证据。

其他机制解释两项边界：ENDOGENOUS_VISIBLE_SELECTION的前期差1让直接post组差1的偏差可被发现，但该人工情形的时间稳定未处理组差可经DiD消除；ANTICIPATORY_PRE_RESPONSE的处理公告提前让pre组差1/2，虽然post处理真效应1，DiD仅1/2，违背no-anticipation。异质处理世界中，均匀配额的post组差设计期望3/2仍等于四人真实ATE3/2，但估计风险方差为23/48，而同质真因果世界方差仅1/16。第一次两版本源测试正常，归档机器验收首次失败是**把相同观察统计误要求为相同含真因果目标的偏差及MSE**；真实世界1/2观察量同分布，真ATE分别1与0，故偏差理应不同。仅修复该错误测试期待值，[测试夹具修复提交73be44a0](https://github.com/edwardsage419/Psychohistory-Research/commit/73be44a093c671e61f166d35dcbb0d255ef37051)。全部生成机制、源码、冻结统计和原来源SHA规则未修改；首轮失败CI原样保留。

## 运行及永久科研验收

* [原代码](r225_exact_natural_experiment.py)、[原576来源CSV](R225_ALL_576_ORIGINAL_NATURAL_ASSIGNMENT_SOURCES.csv)、[六世界完整Fraction结果](R225_EXACT_RESULTS.json)、[机器来源SHA验收](R225_FINAL_MACHINE_ACCEPTANCE.json)。
* 初次CI [run39791326559](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39791326559) 的两个Python测试job均success，第三归档job因上述错误断言失败，run结论failure。不能计入完成归档。
* 修复后的正式CI [run39791457285](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39791457285) 总体success，Python3.11与3.12实际日志各43单测均OK，共86次测试；第三完整来源生成、概率求和、完整观察分布等价、SHA及永久归档job亦completed/success。
* 原全部来源永久机器人提交 [a60f4d6f](https://github.com/edwardsage419/Psychohistory-Research/commit/a60f4d6fc658b65f596469d346a3df2d54585311)。来源SHA256 `11c737f8f08b25afaf5a36bdc94bdc5da47f8ede56d99455c65c50c502c86021`，结果SHA256 `ec537374091d47ed6a566e8029e64d87e0a6c48abbf60c60a58796538eeba9e9`。

本研究没有形式化证明所有自然实验方法或普适不可识别性，只对本六个人工来源世界进行完全有限重放。没有估计现实样本方差、真实处理政策的外生性、同伴干扰或时间趋势的经验等值性。新增真人E2=0，历史E3=0。R073与PESEN v0.1冻结。下一真实原目录条目为 **09-017 Selection versus Influence Identification**，连续研究编号R226，完成全部原R学习后才统一分类和熔炼。
