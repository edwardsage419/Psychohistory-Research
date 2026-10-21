# R162 声望偏向学习｜72组人工注意力彩票、正确性与线索可识别性验证

日期：2026年10月21日。原候选目录 **P1/07-004 Prestige Biased Transmission**。本阶段 **CLOSED_BOUNDED_E1**，所有声望线索均为项目人工指定的注意力票数，三个示范者的行为A/B与预设答案没有真实人群、社会地位、学习成绩或实际能力含义。

核查三份一手出版材料：[Henrich与Gil-White2001原期刊](https://doi.org/10.1016/S1090-5138%2800%2900071-4)区分自愿受尊重的声望与强制支配，[Chudek等2012原期刊](https://www.sciencedirect.com/science/article/pii/S1090513811000481)研究儿童对他人注意力线索的学习，[Jiménez与Mesoudi2019原出版方综述](https://www.nature.com/articles/s41599-019-0228-7)讨论声望学习的证据和开放问题。未获取儿童原始实验选择记录、真实注意力和能力测量，也没有重算原作者模型。

**冻结72组合：** 四种三人示范者行为型（000、100、011、111），偏向注意位置三种，额外注意票数三档（0、1、3），人工正确答案两种，合计72个有理数算例。模型每个示范者初始有一张采样票，被偏向注意的人额外获得指定票数，学习者抽取一张票并复制该示范者行为。实际答对概率仅以模型外指定的正确答案计算。**直接权重计算与另一套完整采样票枚举**对所有72案例的复制概率、基准概率、人工正确率与差值严格完全一致。

**预定反例：** 三人行为为(1,0,0)，偏向唯一采用A的人并给其额外三票时，学习者采用A的概率为2/3，无偏学习只有1/3。若A恰好正确，则人工正确率增加1/3；若B正确，人工正确率反而降低1/3。若将偏向注意对象换为采用B的人，复制A概率可降至1/6。全部行为一致、或额外票数为0时，从最终复制频率无法确定谁受到注意。**传播频率的上升并不保证传播了准确知识**，这一数学结论不能替代真实声望线索可靠性研究。

**真实GitHub验证：** [首次CI run39526761194](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39526761194)成功；[最终固定四项SHA256、三任务CI run39526844299](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39526844299)成功。Python3.11、3.12每轮各99项真实单测，独立归档任务再跑99项，总共495次实际执行、99种不同方法、0失败。[原始完整JSON及源码测试ZIP归档提交6600e68](https://github.com/edwardsage419/Psychohistory-Research/commit/6600e6829a707310281e678928edb55f737aec39)已永久入库。

材料：[计算前协议](../../protocols/R162_PRESTIGE_PROXY_72_ATTENTION_LOTTERIES_PRESCORE_FREEZE_2026-10-21.md)（提交67c6805）｜[科学报告](R162_SCIENTIFIC_REPORT_2026-10-21.md)｜[程序](r162_prestige_attention_exact.py)｜[99项测试](test_r162_prestige_attention_exact.py)｜[完整JSON](R162_EXACT_RESULTS.json)｜[源码数据ZIP](R162_Prestige_Cue_72_Worlds_99_Tests.zip)｜[机器验收](R162_FINAL_MACHINE_ACCEPTANCE.json)。

固定SHA256：
* 程序 `261738a8d2a53f649157d04f79ae198b6d96553cca5daabbbe32727b350382ff`
* 测试 `fb83f7d68f2ce3d34083f81543153ac8617c1bd77c20c1f30ad5fee083f364ea`
* JSON `405ee44d302da5ba79ea31a8df2c364a6bd7712eed85d120d48a42c4860cd264`
* ZIP `d9b39445b6b632a7fd86d120a7a7cd18f2a665572109f777e9031dfdf1d0c660`

进入 `research/R162` 执行 `python r162_prestige_attention_exact.py > R162_EXACT_RESULTS.json` 和 `python -m unittest -q test_r162_prestige_attention_exact.py` 可独立复验，无第三方依赖。

本阶段新增真人E2=0、真实历史预测E3=0；R073及PESEN v0.1仍冻结。下一原目录是 **R163 P1/07-005 Success Biased Transmission（成功偏向学习）**，须与声望线索研究独立比较。先全部R系列，再归纳分类，最后熔炼。
