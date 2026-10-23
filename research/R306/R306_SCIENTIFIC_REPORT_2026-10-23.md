# R306 科学研究报告：群体极化、成员社会比较与论据说服的精确有限模型

日期2026-10-23 Asia/Taipei，原239模型目录 **03-012 Group Polarization Models（P1）**。正式限定等级 **CLOSED_BOUNDED_E1_ARTIFICIAL_R306_GROUP_MEAN_POLARIZATION**。只涉及自设定三个虚拟人意见的有限数学演算，没有真人/动物E2、历史E3，也未进行原作者个体数据复现。

## 第一手文献与明确的原创人工公式界限

Moscovici & Zavalloni (1969), *The group as a polarizer of attitudes*, *Journal of Personality and Social Psychology* 12:125–135, DOI https://doi.org/10.1037/h0027568。该篇真人群体讨论研究报告讨论后群体态度极端化的现象。Myers & Lamm (1976), *The group polarization phenomenon*, *Psychological Bulletin* 83(4):602–627, DOI https://doi.org/10.1037/0033-2909.83.4.602，对社会比较与信息影响作不同解释。Burnstein & Vinokur (1977), *Persuasive argumentation and social comparison as determinants of attitude polarization*, DOI https://doi.org/10.1016/0022-1031(77)90002-6，对说服论据与群体比较机制进行讨论。Sieber & Ziegler (2019), *Group Polarization Revisited: A Processing Effort Account*, DOI https://doi.org/10.1177/0146167219833389，进一步展示论据说服与社会比较条件性贡献的实证理论争论。

R306使用这几篇原文作为**研究问题与竞争机制概念来源**；具体三个意见数值、更新步长、论据目标、讨论机制和实验宇宙完全由本项目人工构建。既没有原1969学生受试者记录，也没有验证2019实验的任何原始参数或结果。不同于R305自我分类认知显著性、R304群体资源分配及R072公开声誉规则；不能把不同社会现象的数据相互冒充独立复现。

## 先验协议及全部人工来源

[完整实验前冻结协议](../../protocols/R306_GROUP_POLARIZATION_CONSENSUS_ARGUMENT_SOCIAL_COMPARE_648_SOURCES_FREEZE_2026-10-23.md)先于源码计算提交 [1db7fc7c](https://github.com/edwardsage419/Psychohistory-Research/commit/1db7fc7cc12cbf1bbec67e3df25c634d689c25b6)。

三位抽象成员原立场分别独立列举−1/2、0、1/2，共27种有序三元组，原群体平均值m。令其原群体方向 q=sgn(m)，无方向时q=0。成员相对比较目标c：m正取已有立场最大者，m负取最小者，m=0取0。支持性论据目标a=q，反向论据a=−q。再用本项目新设计算式：

m_post = m + α(c−m) + β(a−m)。

四个机制α,β分别取(0,0)纯平均化、(1/2,0)仅社会比较、(0,1/2)仅论据说服、(1/2,1/2)两种叠加；最后让三位成员都采取讨论后共识值m_post。研究指标将群体平均值变动与组内分散度归零**严格分开**。m与m_post同号且后者绝对值较大方标记 POLARIZED；由正转负或负转正标记 DIRECTION_FLIP 而不是极化；m初始=0标记NO_INITIAL_DIRECTION，不人为引入任一群体方向。

所有**27三元组×4机制×2支持/反向论据情境=216人工世界**，每世界三条完整成员来源记录，总计**648条原始完整人工来源行**，并非648名真人/648个统计独立受试者。每行有原立场三元组、成员编号和个体立场、平均意见、社会比较与论据目标、α和β、群体均值变化、绝对极端度变化、真实模型结果分类及成员是否改变等；全部Python Fraction精确分数。

## 正例、反例与机制不混淆

| 原立场三元组 | 模型机制 | 群体平均讨论前 → 后 | 判定 |
|---|---|---|---|
| (1/2,1/2,1/2) | 纯平均化 | 1/2→1/2 | 均值不变 |
| (1/2,1/2,1/2) | 仅社会比较 | 1/2→1/2 | 没有更极端的现成成员供比较 |
| (1/2,1/2,1/2) | 支持性论据说服 | 1/2→3/4 | 同方向严格极化 |
| (1/2,1/2,1/2) | 反向论据说服 | 1/2→−1/4 | **方向反转，不是极化** |
| (0,0,1/2) | 仅社会比较 | 1/6→1/3 | 同方向极化 |
| (0,0,1/2) | 支持性论据说服 | 1/6→7/12 | 同方向极化 |
| (0,0,1/2) | 两机制同时支持 | 1/6→3/4 | 同方向极化 |
| (0,0,1/2) | 反向论据说服 | 1/6→−5/12 | 方向反转 |

该设计把平均化、依赖既有最强成员的社会比较、可提供新边界立场的论据说服区分开。均值0的全部七种三元组、任一四种机制/两种论据情境均保持均值0；正负三元组镜像对称；所有意见都保持[-1,1]，因m_post是凸组合。以上**全部是由预定人工公式生成的示例**，没有测量讨论强度、发表真实效应量、估计随机群体的极化频率，也不能因此证明任何实际社交媒体群体的极端化。

在每个讨论情境下27种人工意见三元组中，20种原均值非0、7种等于0。纯平均化均无均值转移；比较机制对20个原有方向中有18个极化、2个不变；支持性论据对20个非零方向全部极化；单独反向论据对这20个方向均发生翻转。在两权重相加的自造强度下也有条件性翻转。这些整数是一个指定小网格的枚举计数，**不是20个真人组的实验频率**。

## 真实执行/独立证明及边界

[原生模型源及1959项真实unittest](r306_exact_group_polarization.py)、[648条完整原人工成员CSV](R306_ALL_648_ORIGINAL_POLARIZATION_PERSON_SOURCES.csv)、[216个完整人工世界及分类计数JSON](R306_EXACT_GROUP_POLARIZATION_RESULTS.json)、[原始字节SHA256凭证](R306_MACHINE_RECEIPT.json)、[完全不导入生产模型的独立凸组合重算和17项篡改测试](../catalogue_audit/independent_r306_source_audit.py)均已永久提交。

[GitHub Actions run39938339913](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39938339913)实际3 job completed/success，Python3.11和3.12各通过1959项主模型unittest与17项独立重构测试，第三job独立验证全部648行、216人工世界、反例/镜像关系、类别统计和SHA后，将原CSV、全部结果JSON及凭证永久归档main [commit a3b9b9be](https://github.com/edwardsage419/Psychohistory-Research/commit/a3b9b9befe6f98610dba796f68f3eed0c94ed85e)。

严格E1人工研究结题，不包含原始人类群体效应的独立确认、网络因果、政治观点传播、长期历史概率；R073与PESEN v0.1冻结，原239主线完成前不进入统一模型分类或熔炼。
