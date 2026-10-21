# R175 历史记忆代际传播：72种二元记忆链的精确数学验收报告

日期 2026-10-21，原冻结候选目录 P2 / 07-017 Intergenerational Transmission Models。科研验收状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_BINARY_MEMORY**；新增真人E2=0，真实历史外推E3=0。

## 原始理论与证据层级

[Griffiths and Kalish (2007)](https://doi.org/10.1080/15326900701326576)《Language Evolution by Iterated Learning With Bayesian Agents》明确区分后验抽样与最大后验语言学习，后验抽样在符合其假设时的稳态由先验支配。[Xu and Griffiths (2010)](https://doi.org/10.1016/j.cogpsych.2009.09.002)《A rational analysis of the effects of memory biases on serial reproduction》分析信息经过记忆重构而串联传播的后果。[Kirby, Cornish and Smith (2008)](https://doi.org/10.1073/pnas.0707835105)使用真人人工语言链式传递进行了实证实验。这三份文献是模型设题来源。本研究的二元隐含主题和独立位翻转叙述规则由本项目另外设计，没有复算原文全部贝叶斯语言模型、原始真人数据或实验刺激。

[冻结协议](../../protocols/R175_INTERGENERATIONAL_BINARY_MEMORY_72_WORLDS_PRESCORE_FREEZE_2026-10-21.md)先于实际评分于commit `18651932aff74684773efb7db74f6e07eb710f13`入库。每代的上一代潜在记忆H为0或1，下一代独立观察n条带翻转噪声ε的二元报告，使用先验π进行后验抽样或MAP决策。MAP后验平局一律选择0。

固定三个先验π=1/4、1/2、3/4；两个噪声ε=1/4、1/3；两个叙述数n=1、3；两个学习策略posterior_sample、posterior_MAP；三个初始条件point0、point1、prior，总共72个世界、24个唯一2×2马尔可夫转移矩阵。每个世界观察t=0至8共9代，精确保存1296个Fraction状态概率单元及24×9个祖先条件差异数值。所有世界仅是数学人工数据。

## 所有冻结的研究问题及实际结果

1. **后验抽样的稳态和长期观察歧义。** 12个抽样矩阵全部检验得到P(H=1)=π的严格不动点。即使n和ε不同，一旦初始主题比例等于π，后续所有9个观察时点的**总体主题比例都严格等于π**。这是当前先验和数据生成机制匹配下的数学性质，不能推论真人记忆始终维持某种比例。
2. **相同群体频率不代表相同祖先保留。** 预先指定π=1/2、ε=1/4，对比每代叙述数n=1与3，后验抽样的总体主题比例每代始终1/2。但分别得到转移矩阵
   * n=1: ((5/8,3/8),(3/8,5/8))，祖先记忆特征值λ=T11−T01=1/4，第4代条件祖先差D4=1/256≈0.00390625。
   * n=3: ((85/112,27/112),(27/112,85/112))，λ=29/56，第4代D4=707281/9834496≈0.071918。
   * 两者在静态分布和所有以先验初始化的总体比例时序上完全一致，然而条件祖先保持能力可区分。**只看宏观时间序列不足以反演个体信息传承忠实度。**
3. **MAP学习机制与潜在偏差。** 12个MAP矩阵中，有8个不保持原设先验π为不动点。事前排序的第一个违反案例π=1/4、ε=1/4、n=1：后验平局向0裁决使下代H=1概率在原先验状态下变为0。这说明确定性后验最大化与后验随机抽样可导致不同文化路径，即使学习者使用完全相同的先验与可见报告。
4. **祖先来源记忆差。** 为每一个参数集合构建H0=1和H0=0的条件轨迹，独立验收D_t=P(H_t=1|H0=1)−P(H_t=1|H0=0)=(T11−T01)^t，在t=0至8全部严格Fraction相等。演化有限期数已冻定，不能据此估计真实历史记忆半衰期。

两套程序真正独立构造完整转移：算法A用二项式组合数按成功报告数k汇总；算法B枚举每种长度n的原始位串，逐条独立相乘似然与后验。全部24个转移矩阵、72个世界九代轨迹精确有理数完全相等。概率非负、和为1。单元测试覆盖20种设计，包括平局裁决、人工极限、与手算结果一致、矩阵等价、稳态、完整祖先解析式、规范化、非法参数拦截和全组遍历。

## 机器复验和归档

[GitHub Actions 39550920279](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39550920279)：Python 3.11、Python 3.12各20次单元测试，40次单测执行全部成功；第三个job运行全72世界，双算法验证并生成可复现源码结果ZIP。全3个job **success**。

* [R175_EXACT_RESULTS.json](R175_EXACT_RESULTS.json)：72×9完整分布、24个二维转移矩阵、12组后验抽样先验稳态验证、12组MAP稳态审计、条件祖先持久度。SHA256 `a6ae43f972dbf8ae5b6c214bd97650281cfd2d587364618447b03331ca3a1795`。
* [R175_FINAL_MACHINE_ACCEPTANCE.json](R175_FINAL_MACHINE_ACCEPTANCE.json)：独立演算精确性、样本数量、稳态与负对照、零真人结论。
* [r175_binary_memory_iterated_learning_exact.py](r175_binary_memory_iterated_learning_exact.py)：全部研究程序及20种自动化测试。
* [R175_Intergenerational_72_Binary_Memory_Worlds_Exact.zip](R175_Intergenerational_72_Binary_Memory_Worlds_Exact.zip)：带固定日期时间信息的结果JSON、验收JSON、研究程序与先冻结协议，可恢复计算。

归档提交 [d0b80a0](https://github.com/edwardsage419/Psychohistory-Research/commit/d0b80a054cf588486eb30cd760f72762c68fd514)，已核验main上所有对应结果文件存在。后续科学报告与主README亦应另行提交核验。

## 正式科研验收和下一序列

R175只对本项目明确写下的二元、独立同分布报告生成与贝叶斯规则推导进行了精确受控E1结题。真实人类记忆含选择性叙事、外部档案、制度操纵、语言意义、社会网络和共享冲击；本人工子模型没有实证测量这些因素。**在模型内部稳态下的历史记忆失真与真人记忆遗失不可直接等价。**

下一项R176 P2 / 07-018 Long Run Agent Based History 长时段主体建模。继续执行既定顺序：先全部R系列、再统一归纳分类、最后熔炼。R073与PESEN v0.1保持冻结。
