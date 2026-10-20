# R130 重复博弈：Axelrod–Hamilton 1981双入侵者稳定边界与Nowak–Sigmund 1993 Pavlov失误恢复

日期：2026-10-20。既定P1候选05-006 Repeated Games。

**科学结题状态**：CLOSED_BOUNDED_AXELROD_HAMILTON_1981_TWO_TFT_NONINVASION_PAYOFF_CONSTRAINTS_AND_NOWAK_1993_PAVLOV。
**有界学习状态**：LEARNING_COMPLETE_BOUNDED_AXELROD_HAMILTON_1981_TFT_TWO_INVADERS_AND_NOWAK_SIGMUND_1993_PAVLOV。
**新增真人独立预测E2=0**。本轮只完成真正原创论文原始收益/两条约束的数学复算和有界确定性策略行为；R073、PESEN v0.1继续冻结，不能提前统一分类或熔炼。

## 第一手来源审阅，而不是重复R128

[Axelrod & Hamilton (1981), *The Evolution of Cooperation*, Science 211(4489):1390–1396](https://doi.org/10.1126/science.7466396)，[作者本人美国密歇根大学的原刊全文PDF](https://public.websites.umich.edu/~axe/research/Axelrod%20and%20Hamilton%20EC%201981.pdf)。本期真正核阅原刊1392页Fig1四个PD支付值 **R=3,S=0,T=5,P=1**、1393页Eq(1) **同时**比较无条件背叛ALLD与交替背叛D,C,D,C这两类侵入TFT的历史序列，以及1394页作者对成功策略和合作群落的论述。原作者最初14策略比赛每场200轮、后来62规则与原研究报告中的大规模竞赛**未由R130实际再次运行**。TFT在限定数学里首轮合作，随后复制对手上一轮实际采取的动作。

[Nowak & Sigmund (1993), *A strategy of win-stay, lose-shift that outperforms tit-for-tat in the Prisoner's Dilemma game*, Nature 364:56–58](https://doi.org/10.1038/364056a0)，[哈佛大学保存Nature正式全文原扫描](https://abel.math.harvard.edu/archive/153_fall_04/Additional_reading_material/A_strategy_of_winstay_loseshift_that_out_performs_titfortat_in_the_Prisoners_Dilemma_game.pdf)。原刊56、57页实际可视阅读，对照1993作者以本轮自身收益R/S/T/P为状态、合作向量**(1,0,0,1)**的Pavlov/WSLS（win-stay, lose-shift，赢则保持、输则转换），并关注一次错误后恢复CC的机制。其真正论文还报告对随机概率性一阶记忆策略加入变异、选择及失误的漫长演化模拟；**本期没有独立重现作者的种群模拟结果、长期策略优势及真实人类行动率**。

[James W. Friedman 1971 *A Non-cooperative Equilibrium for Supergames*](https://doi.org/10.2307/2296617)本期只核发行摘要与元信息，未精读并重证全文定理。R128以前已经完成不同阶段PD原Skyrms2004收益[2,0;3,1]在Trigger/Foole两策略之间的猎鹿转换，本期**不是**再次做Skyrms的[[5,1.5],[4.5,2.5]]相同研究。R130固定Axelrod1981四支付[3,0;5,1]和Nowak1993的另一种历史更新规则，提出真正不同的可验证比较。

## 关键数值：仅抵御永远背叛并不足以保住TFT

原1981 Eq(1)需要两道条件都满足：

1. TFT面对TFT得**3/(1−w)**。无条件背叛ALLD面对TFT首轮得5，之后每轮双方D得1，合计**5+w/(1−w)**；前者不低于后者需要继续概率w≥**1/2**。
2. 交替背叛ALT_DC面对TFT首轮5、第二轮0、第三轮5、第四轮0，...，合计**5/(1−w²)**；TFT/TFT收益要不低于这一侵入者，需要w≥**2/3**。

在w=3/5（60%）的精确例：
- TFT/TFT：**15/2=7.5**；
- ALLD对TFT：**13/2=6.5**；
- ALT_DC对TFT：**125/16=7.8125**。

因此虽然始终背叛已不能取得更高分，交替背叛仍能取得更高分。这是1981作者原论文的两条不同约束，不是研究者事后改变来源收益。**w=2/3时ALT_DC与TFT/TFT收益平手**；这一弱不超条件不直接证明整个演化策略空间中严格ESS或历史中的合作必然稳定。原作者进一步的全部策略/初始进入群落与策略竞赛结果都需要与有限样例验证严格区分。

## 明确的原1993 Pavlov策略映射与只注入一次执行错误

给定上一轮自己真实执行的C/D和对手C/D四种结果：

| 上轮动作（自己/对手） | 自己得到原1981/1993收益 | Pavlov下一步 |
|---|---|---|
| CC | R=3 | C（保持） |
| CD | S=0 | D（转换） |
| DC | T=5 | D（保持） |
| DD | P=1 | C（转换） |

本项目新造的、但严格遵循原刊策略规则的唯一误执行对照：原本两方应首轮CC，但外部**仅强制第1轮行方实际D、列方实际C**；从第2轮起双方不再产生任何随机执行错误。所得八轮双方实际行动：
- TFT/TFT → **DC,CD,DC,CD,DC,CD,DC,CD**：两方交替报复，未自己回到共同合作。
- WSLS/WSLS → **DC,DD,CC,CC,CC,CC,CC,CC**：仅第二轮双方D，第三轮即同步恢复合作。

此现象是**特定单次/单边/后续无噪声**环境中的精确有限状态机演示。不能解读为TFT在所有噪声/学习/制度条件下都无法恢复，或真实参与者会按这八轮策略实际行动，也不能声称Nature1993的种群模拟已经复刻。

## 有限已知终局与未来概率不确定性

原图Fig1单轮严格占优为D（对方C时D5胜C3；对方D时D1胜C0），在**共同事先知道固定总轮数**的有限完全信息PD、所有人理性且收益只含所给值的假设下，最后一轮D，向前递推得到所有轮D的子博弈完美均衡路径。相对若每轮结束还有概率w继续，没有提前公布固定终点，历史条件可使合作自利回报随w变化。这只说明明确假设内的理性决策边界，不能宣称所有真实有限轮实验都发生全部D，也不可把实际熟人长期相处的时长随意转换成本文几何停止概率。

## 真正数学复算、机器CI与证据归档

选取TFT、ALLD、ALLC、ALT_DC、Pavlov/WSLS五个有界确定性策略（**并非**1981原14/62全部参赛策略）。一套完全独立的实际策略逐轮模拟器输出之前真实执行的双行动与现金流；另一套对有限状态（前轮C/D与交替回合奇偶性）检测前导和循环，再通过**严格Fraction**自动计算无限期循环的精确几何折现和、以及从任意N轮起的旋转周期尾项。针对5×5=**25个有序策略对**、w的**7个格点**、有限轮次N的**6种**配置，总共**25×7×6=1,050个合成折现数学恒等式**；显式N轮现金流加独立尾项必须严格等于独立无限循环闭式，且TFT-TFT、ALLD-TFT、ALT_DC-TFT另需和原1981的真实闭式对照。非法策略/历史/float/bool/w=1均失败拒绝，不用随机近似或未允许的数据。

[GitHub Actions 39354120663](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39354120663) **completed success，65项unittest全部通过、0失败**，并从新的独立步骤重复验证1981的两道门槛、1993的Pavlov状态图、两种误执行序列和全部1050精确对照。实际GitHub机器人生成带源码、测试、科研报告三个文件SHA256的[真实机器收据](R130_PHASE_A_1981_1993_65_TEST_1050_CYCLES_TWO_INVADERS_CI_ACCEPTANCE.json)，收据已单独从main读取核验。

全部正式文件：
- [事前冻结协议](../../protocols/R130_AXELROD_1981_TWO_TFT_THRESHOLDS_NOWAK_1993_PAVLOV_FREEZE_2026-10-20.md)
- [源论文全限定科研报告](R130_AXELROD_1981_DUAL_TFT_THRESHOLD_NOWAK_1993_PAVLOV_EXACT_SCIENTIFIC_REPORT_2026-10-20.md)
- [原生Python程序](r130_axelrod1981_tft_nowak1993_pavlov_repeated_exact.py)
- [65项真实unittest](test_r130_axelrod1981_tft_nowak1993_pavlov_repeated_exact.py)
- [机器运行结果与源代码/测试/报告SHA256回读](R130_PHASE_A_1981_1993_65_TEST_1050_CYCLES_TWO_INVADERS_CI_ACCEPTANCE.json)
- [正式科学验收和限制](R130_FINAL_ACCEPTANCE_STATUS.json)

本地复算（Python3.11无第三方依赖）：PYTHONPATH=research/R130 python -m unittest -v research/R130/test_r130_axelrod1981_tft_nowak1993_pavlov_repeated_exact.py。

**科研适用边界**：本期已完成原创论文原始支付与两条不同历史入侵者的不超收益比较、Pavlov记忆状态图及可复算的确定性误差修复，**没有重新运行原作者整个演化群体/全部锦标赛，也没有真人逐行实验或历史外部概率预测E2/E3**。用户明确R系列主线优先，后分类最后熔炼；R073与PESEN v0.1继续冻结。
