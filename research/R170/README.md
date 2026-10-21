# R170 语言演化：72组四代理双词命名游戏及精确传递反馈

日期2026年10月21日。原模型目录 **P2 / 07-012 Language Evolution Models**。正式研究 **CLOSED_BOUNDED_E1**。本阶段只研究人工A/B两个词及每人「仅知道A」「仅知道B」「同时知道A和B」的有限记忆，**不涉及真实人类的语言能力、语法规则、濒危语言或语言变迁历史数据**。

**一手研究依据：** [Baronchelli等2006](https://doi.org/10.1088/1742-5468/2006/06/P06014)提出多人命名游戏并研究共享词汇如何形成，[同年网络拓扑命名游戏原刊](https://doi.org/10.1103/PhysRevE.73.015102)研究局部接触与语言惯例收敛。我们另核对[Nowak/Komarova/Niyogi2001语法理论](https://doi.org/10.1126/science.291.5501.114)和[Abrams/Strogatz2003语言衰退模型](https://doi.org/10.1038/424900a)，明确区分词汇惯例、语法学习与人口语言衰退。**原作者无限词汇、相变、语法门槛及语言人口数据未复现**。查看[完整科学报告](R170_SCIENTIFIC_REPORT_2026-10-21.md)。

**事前冻结：** 四种固定四人接触图×三种初始词汇记忆布局×三种人工消息词汇翻转概率（0、1/4、1/2）×两种反馈更新模式（两人共同确认，或只更新听话者），共72组，每组保留t0至t3的完整四人词汇记忆联合概率分布。发言者从自己的库存中随机说出一个词，通过人工噪声渠道有概率把送达词变成另一个；听话者若认识送达词，则按预定反馈策略更新词汇库存；听话者不认识则添加该词。规则已在[计算前协议](../../protocols/R170_TWO_WORD_NAMING_GAME_72_INVENTORY_MARKOV_WORLDS_PRESCORE_FREEZE_2026-10-21.md)（提交1853b17）冻结。人工翻转渠道**不是原作者的同一规则**。

**两套独立数学程序：** 直接枚举无向边及说听顺序、说话者已知词与噪声分支；独立枚举全部有向交流对，并先计算送达A/B的条件概率，再分别实现反馈更新。全部72组四个时点的完整概率分布 **Fraction逐项严格相等**。原始[1062174字节JSON](R170_EXACT_RESULTS.json)保存每组全部词汇库存向量及精确概率、平均记忆负荷和全体一致使用单词的概率。

**事前控制与验证：**
* 噪声为零时，所有人只有A词或只有B词的完全一致状态是吸收态；有非零词汇翻转噪声则可能被打破。初始全A时，链式网络在第一次交流后仍是全A的概率，噪声0为1、噪声1/4为3/4、噪声1/2为1/2。
* 初始都是单词掌握者且无噪声时，两种反馈规则第一次交流的结果相同。存在同时掌握A/B词的代理时，两种反馈规则在第一次交流就能产生不同状态分布。
* 初始(A,AB,B,AB)、无噪声时，初次交流后两反馈模型完整分布的总变差距离：链式图 **1/4**、星形图 **1/6**、环形图 **1/4**、完全图 **1/6**。不同局部网络改变传递与词汇确认的机会，这是人工传递概率的结果，不能直接推广成人类语言学习心理规律。

**真实GitHub计算验证：** [首轮CI39541240078](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39541240078)、[固定四项SHA256与正式归档CI39541318811](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39541318811)均成功。Python3.11与3.12各两轮实际运行111种测试，独立归档任务再运行111项，总计**555次单测执行、111种不同测试方法、0失败**。原始完整结果与源码测试压缩包已通过[提交17bead4](https://github.com/edwardsage419/Psychohistory-Research/commit/17bead42dc93481e4358928dc30ba742e63c3b07)永久进入main。

成果：[计算前冻结协议](../../protocols/R170_TWO_WORD_NAMING_GAME_72_INVENTORY_MARKOV_WORLDS_PRESCORE_FREEZE_2026-10-21.md)｜[原生程序](r170_two_word_naming_game_exact.py)｜[111项测试](test_r170_two_word_naming_game_exact.py)｜[全量JSON](R170_EXACT_RESULTS.json)｜[ZIP原始研究包](R170_Naming_Game_72_Worlds_111_Tests.zip)｜[正式科学报告](R170_SCIENTIFIC_REPORT_2026-10-21.md)｜[机器验收](R170_FINAL_MACHINE_ACCEPTANCE.json)。

四项SHA256：
* 程序 `6587ad073fbc34adc5029c81521ed73f05da319b2c46c1f86361f0a4d31d67ac`
* 测试 `54fc5b8322fd54432c3a619355e54942e4d4fc780dc431c56f28204e492acd97`
* JSON `2e63390bfbb6e0ddbf1622767e94d59b2b1db1a286c8f79caac1d333d61277ce`
* ZIP `1b8cf39c0afec2a90fd5aed661b04ac13dbfd9215910abd27fb7dd2d40f7c0f1`

独立复算：进入 `research/R170` 执行 `python r170_two_word_naming_game_exact.py > R170_EXACT_RESULTS.json` 再执行 `python -m unittest -q test_r170_two_word_naming_game_exact.py`；仅需Python标准库。

新增E2真人独立预测=0、E3真实历史预测=0；R073与PESEN v0.1继续冻结。下一原目录 **R171 P2/07-013 Cultural Phylogenetics（文化系统发育）**。研究顺序不变：先完成R系列全部模型，再统一归纳分类，最后模型熔炼。
