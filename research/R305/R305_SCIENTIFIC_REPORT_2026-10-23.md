# R305 科学研究报告：Self-Categorization Theory 情境对比适配与个人层级回退

日期 2026-10-23 Asia/Taipei，原始239目录 **03-004 Self Categorization Theory，P1**。科学范围 **CLOSED_BOUNDED_E1_ARTIFICIAL_R305_SCT_CONTEXT_COMPARATIVE_FIT**。仅为有限的人工数学例示；无新真人/动物 E2、无历史 E3，未验证社会理论的真实人群参数和预测精度。

## 第一手理论及与 R304 的独立边界

John C. Turner (1985), *Social categorization and the self-concept: A social cognitive theory of group behaviour*, *Advances in Group Processes* 2:77–122，原著书章档案由[Harvard研究参考条目](https://inclusionandbelongingtaskforce.harvard.edu/publications/social-categorization-and-self-concept-social-cognitive-theory-group-behavior)索引。Turner、Hogg、Oakes、Reicher、Wetherell (1987), *Rediscovering the Social Group: A Self-Categorization Theory*, Blackwell，第42–67页 Turner 章 *A self-categorization theory*。Turner、Oakes、Haslam、McGarty (1994), *Self and Collective: Cognition and Social Context*, DOI https://doi.org/10.1177/0146167294205002。

这些原著解释自我分类在不同对照背景下具有情境性，个人与社会身份层级会变化，类别原型与比较适配性、规范适配性、认知可及性相关。本文采用的特征数值和乘法适配评分是**本项目自己提出的教学型机制**，不构成原著定量公式的复制或任何人类观察结果。

相邻[**R304 社会认同理论的资源分配**](../R304/R304_SCIENTIFIC_REPORT_2026-10-23.md)关注预设内外群体标签下资源分配中的相对群体优势与整体收益冲突，不评价情境如何改变自我类别适配。R305完全不含群体分配点数/奖赏，也没有 R063 真人社会模仿原CSV或 R073 真人重复博弈。因此不能从三个项目共有的“社会”语词认定独立真人复现。

## 事前冻结的人工研究

[完整冻结协议](../../protocols/R305_SELF_CATEGORIZATION_METACONTRAST_486_SOURCES_PRESCORE_FREEZE_2026-10-23.md)在源码/计算前通过 [GitHub commit a4dfc1f5](https://github.com/edwardsage419/Psychohistory-Research/commit/a4dfc1f582c9a58eec6cf45b63a34f577800e0eb) 归档。

四个虚拟对象 0、1、2、3，允许两个候选分类 P=(0,0,1,1) 与 Q=(0,1,0,1)，两者皆非观察到的真实群体。X 情境特征 (0,1,4,5)，Y 情境 (0,4,1,5)，中间 MID 情境 (0,5/2,5/2,5)。每个分类内的两对对象绝对距离平均为 W，每个分类间的四对对象绝对距离平均为 B，自行定义**对比适配性** MC=B/W。所有人工配置 W 严格正，不需零分母平滑。

进一步人为设定可及性 r∈{0,1/2,1}，两种类别的规范适配值 nP、nQ∈{0,1/2,1}，与个人层级竞争的阈值 t∈{0,1,2}。群体类别得分分别是 S_P=r*nP*MC_P、S_Q=r*nQ*MC_Q；个人层级得分 t。仅在某群体分数**同时严格大于**其他群体分数及个人层级时选该群体，否则选择 PERSONAL（所有并列保守返回个人层级）。这不重建 Turner 提出的完整三层个人／社会／人类自我分类体系，而是限制为两个群体候选与一个个人默认层级。

由 **3情境×3可及性×3规范P×3规范Q×3阈值=243个人工世界**，每个世界记录 P/Q 两个完整候选来源，因此共有 **486条人工完整original source**，非486个受试者、真实观察轨迹或可识别人物。每条数据记录情境、特征、类别成员、组内和组间成对距离、对比适配、规范因子、群体得分、比较对象得分及最终分类，全部使用 Python Fraction 精确数学。

## 已冻结的对照结果

| 情境 | MC_P | MC_Q | r=nP=nQ=1、个人阈值 t=1 的最终分类 |
|---|---:|---:|---|
| X | 4 | 5/8 | **P** |
| MID | 1 | 1 | **PERSONAL** |
| Y | 5/8 | 4 | **Q** |

不改变候选分类 P/Q 的成员关系而仅替换情境，就能在此数学机制中由 P 转换成 Q。无群体成员实际更换，没有真实人被改变认同。MID 里两类相等且都没有严格超过个人阈值 t=1，预设保守规则选择个人层级，不是从实验估得真实的身份回退频率。

**规范适配性作为独立负对照：** 在 X 环境 r=1、nP=0、nQ=1、t=0 下，虽然原始比较适配 MC_P=4 大于 MC_Q=5/8，但社会分类 P 得分0而 Q 得分5/8，故选择 **Q**。这说明本文不同计算因子的作用不会被“组内小组间大”单一结论覆盖。若 r=0 或 nP=nQ=0，无论 X/MID/Y 情境如何，所有群体分数都是0，在 t∈{0,1,2} 时始终返回个人层级；只是人为选择函数的必然结果，不证明任何真实人类身份形成机制。

## 两条独立计算路径与透明范围

[主程序](r305_exact_self_categorization_metacontrast.py)从预定两种类别标签生成两组 within pairs 与四组 across pairs，依照概率有理数运算计算每条 source 的适配度、得分及选择；包含**1473个实际unit tests**。 [完全独立审计程序](../catalogue_audit/independent_r305_source_audit.py)不导入主程序，直接穷举四对象所有六对组合，按类别标签独立分组计算平均距离和 MC，独立实现人格层级选择规则；包含**18个恶意篡改／负对照测试**，并对完整CSV、JSON逐字段复算。缺行、重复行、错误配对、异常规范因子、伪造分数/决策和 SHA篡改均被拒绝。

[486条完整source CSV](R305_ALL_486_ORIGINAL_SELF_CATEGORIZATION_SOURCE_CELLS.csv)、[243人工世界完整计算结果](R305_EXACT_SCT_COMPARATIVE_FIT_RESULTS.json)、[原来源及结果SHA256机器凭证](R305_MACHINE_RECEIPT.json)已由[GitHub Actions run39937267071](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39937267071) 3/3 jobs completed/success 核验。Python3.11、3.12各运行主程序1473项unit tests和独立审计18项测试；第三作业重新生成486条source并独立复核后，归档到 main [commit c57d76c1](https://github.com/edwardsage419/Psychohistory-Research/commit/c57d76c1d8e42b95e83eff0ffe72f23a9803da7c)。机器报告原 source SHA256 f58fd8b279bc6418521f863d190071ae60b88adb29163abbd5a71aecf3c89bdb。

**科研证据界限：** 这只表明一个冻结的项目专属有限模型能以情境和规范条件重排分类，不说明人们确实计算 MC=B/W 或遵循乘法门控，未测量自我分类表现，未证明人类群体原型真实存在、社会影响方向或历史事件概率。R304 03-003、R303 03-001、R063旧范围证据均不改；R073/PESEN v0.1保持冻结，分类与原创熔炼尚未开始。
