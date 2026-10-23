# R236 调查回答偏差：九有限真实私人状态与回答机制、576完整原来源及三对观察联合等价

日期：2026-10-23（Asia/Taipei）。原始239目录**10-010 Survey Response Bias Models（P1）**，有界科研状态 `CLOSED_BOUNDED_E1_ARTIFICIAL_SURVEY_RESPONSE_BIAS_ALIASES`。本报告完全依据九个人工布尔测量生成式的有限Fraction枚举，未接入任何真实民调、受访者隐私或历史舆论E2/E3数据，绝不能从此人工世界推断现实私人信念/调查谎报比例。

## 原始方法与本模型范围

Tourangeau, Rips & Rasinski (2000), *The Psychology of Survey Response*, Cambridge University Press，[原出版社书籍导读摘录](https://beckassets.blob.core.windows.net/product/readingsample/764311/9780521576291_excerpt_001.pdf)，围绕理解、回忆、判断及报告阶段介绍问卷回答的心理过程。Krosnick (1991), [*Response Strategies for Coping with the Cognitive Demands of Attitude Measures in Surveys*](https://doi.org/10.1002/acp.2350050305), *Applied Cognitive Psychology* 5:213–236，[原作者公开PDF](https://web.stanford.edu/dept/communication/faculty/krosnick/docs/1991/1991%20Satisficing.pdf)，原方法讨论满意化回答、同意偏差、不区分回答与认知努力。本R由这类测量机制激发固定的人工有限反例，不声称已经复现原作者真实调查、真实实验或任何论文估计数据。

事前[九世界独立冻结协议](../../protocols/R236_SURVEY_RESPONSE_BIAS_9_WORLDS_576_COMPLETE_ATOMS_PRESCORE_FREEZE_2026-10-23.md)先行提交[fe60b543](https://github.com/edwardsage419/Psychohistory-Research/commit/fe60b543c601b409a0f3d4737ac9ce06a3fd5d6b)，然后才创建计算代码、完整源归档和评分。机制、评价及实际观察变量与冻结协议一致，首次失败后仅修复测试字段名。

## 全部原生成类型与独立数学路径

人工六独立Bernoulli(1/2)外生源 `T,S,U,R,E1,E2`。T、S是两道私人问题的起始真二元状态，U是潜在作答风格/改变的易感状态，R是单独随机分配的调查模式，E1/E2是问卷前核验代理是否可被观察的指标；均匀枚举2⁶=64个完整原源每世界，九世界**576条**原源，全部各权重1/64。五个**真正观察**字段是 `R,P,Z,Y1,Y2`，其中P=当E1=1时的初始T、否则−1表示缺失；Z类似通过独立E2以1/2概率呈现初始T。P和Z并**非干预后的真实私人态度**，也不具备现实心理测谎设备的效度。两道当前私人真状态B1/B2在人工oracle里另存，不能提供给实际调查估计器。

第一计算路线完全枚举64源，以真实可见R/P/Z/Y1/Y2的联合概率统计报告Y1对随机模式R的观察总处理差（ITT）、报告两题协方差。真正私人B1在`do(R=1)`与`do(R=0)`的干预差则仅由oracle推断，须与观察指标完全分开。第二条独立路径不读取64来源CSV，从四个核心T/S/U/R独立枚举16配置，并将P/Z各呈现或缺失的1/2概率独立积分，严格重构完整五变量联合；真B1的干预差由独立反事实布尔函数对T/S/U的8种配置另算。这两套数学路径逐状态匹配。

## 九人工世界真实/观察结果

| 世界 | 观察Y1随机模式ITT | 真实私人B1随机模式效果 | 真实私人B1/B2协方差 | 观察回答Y1/Y2协方差 |
|---|---:|---:|---:|---:|
| TRUTHFUL_STABLE | 0 | 0 | 0 | 0 |
| TRUE_MODE_CHANGE | 1/2 | 1/2 | 0 | 0 |
| REPORT_MODE_CHANGE_ALIAS | 1/2 | 0 | 0 | 0 |
| TRUE_MODE_COMPLIER_ONLY | 1/4 | 1/4 | 0 | 0 |
| REPORT_MODE_COMPLIER_ONLY_ALIAS | 1/4 | 0 | 0 | 0 |
| SOCIAL_DESIRABILITY_U | 0 | 0 | 0 | 1/16 |
| MODE_SUPPRESS_REPORT | −1/2 | 0 | 0 | 0 |
| SHARED_ACQUIESCENCE_RESPONSE | 0 | 0 | 0 | 1/4 |
| SHARED_TRUE_CONSTRUCT_ALIAS | 0 | 0 | 1/4 | 1/4 |

**完整观察等价一：真实状态改变或仅回答改变。** TRUE_MODE_CHANGE中真实私人B1=T OR R，问卷Y1如实反映B1；REPORT_MODE_CHANGE_ALIAS中B1=T不因模式改变，但问卷报告Y1=T OR R。对全部64个对应潜在源，包括两条只能揭示**模式前初始T**且半数缺失的部分核验代理P/Z，五个实际可见变量每项都相同，完整联合P(R,P,Z,Y1,Y2)逐格完全一致。随机模式对于报告Y1的ITT均1/2，但真B1模式效果一为1/2、一为0。由此表明独立随机分配确能识别报告层面的有限ITTs，而没有单独的**模式之后真私人状态测量或另一些排除/锚定限制**就不能把报告ITT无条件解释为内心态度改变。

**完整观察等价二：只有部分人受模式影响。** TRUE_MODE_COMPLIER_ONLY让真正私人B1=T OR (R AND U)，以U确定的部分真状态可能受模式影响；REPORT_MODE_COMPLIER_ONLY_ALIAS真实B1=T、只有报告随R和U改变。两世界所有实际观测与问卷前核验逐原来源完全相同，观察Y1模式ITT均1/4，但真正私人状态效应为1/4与0。即使存在人群对问卷模式响应的异质性，内部两项已有前期代理也不能自动区分私人变化与答卷风格改变。

**完整观察等价三：共同响应风格还是共同心理内容。** SHARED_ACQUIESCENCE_RESPONSE把两种真实私人内容分别设为独立T与S，但第二道题Y2机械复制第一题Y1=T，两道**观察回答协方差1/4**而两个私人构念真实Cov=0；SHARED_TRUE_CONSTRUCT_ALIAS把两个私人构念都设为T，两道回答均如实反映T，真实Cov=1/4。二者全部五个可见变量逐原来源严格相同，不能以一次问卷内两题的完全相关性自动断定存在共同潜在心理因子。机械重复作答世界的第二题真实不一致率恰1/2，尽管问卷显示两题完全一致。

**共享社会期望性可制造虚假相关。** SOCIAL_DESIRABILITY_U两个私人真状态T/S仍独立，Cov=0，但报告Y1=T OR U、Y2=S OR U对同一个隐藏U存在共同回答偏向，观测Y1/Y2协方差为1/16，两个回答相对于私人真值的失真率各1/4。这种正关联在人工世界纯属共同应答机制产生。MODE_SUPPRESS_REPORT还展示观察Y1因模式R从通常模式转为抑制模式，观察ITT为−1/2但私人B1真实模式效应仍0。

所有比例均为六均匀人工原源的精确Fraction，**不构成实际人口偏差频率**。任何关于“欺骗”“社会期望性”的语义标签仅说明形式机制，不是对真人动机的可验证判断。

## 首轮回归夹具失败及最终CI与原来源永久证据

[原生Python完整人工模型](r236_exact_survey_response_bias.py) · [576完整外生来源原CSV](R236_ALL_576_ORIGINAL_SURVEY_RESPONSE_SOURCES.csv) · [九世界完整五变量联合及真/观察矩JSON](R236_EXACT_RESULTS.json) · [机读源文件SHA收据](R236_FINAL_MACHINE_ACCEPTANCE.json)。

首轮[CI run39883624090](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39883624090)运行失败，另一Python矩阵作业随后cancelled、归档job skipped。首个失败作业的实际日志展示`Ran 66 tests`，其中9个测试因**唯一性回归测试错误地用`oracle_original_E1/E2`字段名访问原来源**而报KeyError；人工原源正确字段从第一次生成起均是`oracle_proxy_ascertainment_E1/E2`。所有实际计算的概率和机制检查均没有因此改变。严格修复仅该唯一性测试的来源字段引用，提交[8647d170](https://github.com/edwardsage419/Psychohistory-Research/commit/8647d1707b6e6f5e61e91bbfbe37abe326cdd956)，原失败日志留在GitHub不得隐去。

修复后[正式CI run39883729551](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39883729551)总体completed/success，全部3个作业completed/success，Python3.11与Python3.12真实日志各`Ran 66 tests`、`OK`，合计**132次真实测试执行通过**。第三原来源归档作业从源码重新生成576条完整六源类型及原概率、核验三对完整观察等价、布尔反事实与私人/报告Cov及源SHA，真实输出`R236_ALL_576_SURVEY_SOURCES_THREE_FULL_OBSERVED_ALIASES_AND_TRUE_MODE_INTERVENTIONS_VERIFIED`。机器人全部原数据与机器收据永久提交[7f41b331](https://github.com/edwardsage419/Psychohistory-Research/commit/7f41b33124b681fb14335868cc9d5e8dea75fa6f)。

原来源CSV SHA256 `f3a539756c925de9cc733864938ba5fc245bf5a04f197eee194340f294786ced`；结果JSON SHA256 `d24b11b96da884a9da5ae7c93a6123729b62f9d7546db490371a34eacd86f692`。

最终科学边界是九个人工独立二元测量机制的有限等式反例，不保证其他问卷、真人长时记忆、真实文化语境、历史文本或真实心理概念有相同非识别性。真人E2与历史E3新增均0，R073/PESEN v0.1冻结。原239目录下一项已经核验为 `10-011 Topic Models`，编号计划R237。按owner顺序先完成原R主线后统一分类，最后原创模型融合。
