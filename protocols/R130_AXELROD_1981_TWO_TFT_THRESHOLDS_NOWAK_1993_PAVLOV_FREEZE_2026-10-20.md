# R130 Repeated Games：1981两种以牙还牙入侵者、1993 Pavlov修复、有限/无限重复的来源冻结

日期2026-10-20。原目录P1 05-006。R128已用Skyrms2004原书的收益(2,0,3,1)在Trigger/Foole两种策略间做了无限折现转换；R130完全换为Axelrod/Hamilton1981原论文数值(R=3,S=0,T=5,P=1)，研究ALLD及交替背叛ALT_DC这两种不相同的原刊入侵条件，另外复核Nowak/Sigmund1993原刊Pavlov策略的一次误执行恢复。不得将R128和R130计为新增独立真人E2。本轮没有融合同类后续R模型。R073和PESEN v0.1保持冻结。

一手源1：Axelrod, Robert & Hamilton, William D. (1981), The Evolution of Cooperation, Science 211(4489):1390-1396, DOI 10.1126/science.7466396，作者自己密歇根大学原刊PDF https://public.websites.umich.edu/~axe/research/Axelrod%20and%20Hamilton%20EC%201981.pdf 。PDF原印刷p1392 (PDF page3) Figure1明确R3,S0,T5,P1，前提T>R>P>S、R>(T+S)/2；原刊p1393 (PDF page4) Eq(1) **同时**给出继续概率w>= (T-R)/(T-P)及w>= (T-R)/(R-S)来抵御ALLD、ALT_DC相对TFT/TFT在无穷折现收益上超过。原作者又叙述原参加策略竞赛，最初14参赛规则每配对200轮及第二阶段62参赛规则和大量模拟选择，本期并没有取回原程序/所有参赛规则，不能称已重跑原竞赛、全策略总体进化稳定性或作者完整证明。概率w不是观测历史关系的估计值。

一手源2：Nowak, Martin & Sigmund, Karl (1993), A strategy of win-stay, lose-shift that outperforms tit-for-tat in the Prisoner's Dilemma game, Nature 364:56-58，DOI 10.1038/364056a0。哈佛大学原刊影印3页 https://abel.math.harvard.edu/archive/153_fall_04/Additional_reading_material/A_strategy_of_winstay_loseshift_that_out_performs_titfortat_in_the_Prisoners_Dilemma_game.pdf 。已可视阅读原刊印刷p56、57：Pavlov/WSLS按自己的前次R/T结果保留前次行动、按S/P结果转换。作者一阶记忆合作向量按过去本人结果(R,S,T,P)的次序为(1,0,0,1)，并实用了R3,S0,T5,P1。原文做的是含变异、选择、噪声的长时间计算机演化模拟，不是我们这次要重新执行的5策略有限状态机。本轮不会声称独立复现自然群体的Pavlov优势。Friedman(1971) A Non-cooperative Equilibrium for Supergames, Review of Economic Studies 38(1):1-12, DOI10.2307/2296617，只核官方发行的元数据和摘要，未取得原文完整证明，不能假装已原文复算全部folk theorem。

原1981严格数学合同：对人行动C/D一轮行收益CC3, CD0, DC5, DD1，列方按对称交换。无限折现0<=w<1、w须标准库Fraction且禁float/bool。TFT/TFT得3/(1-w)，ALLD对TFT得5+w/(1-w)，ALLD不超TFT/TFT的条件w>=1/2。ALT_DC（第1轮D，第2轮C，如此无限交替）对TFT每轮获得5,0,5,0,...，得5/(1-w^2)，不超TFT/TFT条件w>=2/3。故w=3/5下ALLD已无法取得更高折现分数，但ALT_DC仍可入侵；只有两条件都满足才通过原刊这两道不入侵比较。w=2/3时ALT_DC恰与TFT/TFT打平，不单凭两个相等数宣告严格ESS，也不由检查5个固定策略就完成原作者对全部可行策略的演化稳定性论证。

项目策略集：ALLC每轮C、ALLD每轮D、TFT首轮C随后模仿对方上次行动、ALT_DC按轮次D,C交替、WSLS首轮C之后根据自己的前次已实现收益R或T保留动作，S或P切换动作。WSLS的上一轮联合动作映射CC->C, CD->D, DC->D, DD->C与1993书面定义相符。两人同时行动、策略正确观察前一轮实际实施的动作，不假定绝对不可犯错。

独立数学审计1：对每个有序策略配对5×5，用两种不相互调用的算法——显式1..12轮真实历史行动与得分、以及不依赖预先给定闭式的有限状态循环检测（状态包含上一轮双动作及ALT奇偶轮次），精确求无限期前导+循环收益折现。对w in [0,1/4,1/2,3/5,2/3,4/5,9/10]及N in [1,2,3,5,8,12]，每对每w每N检验“直接模拟N轮的前缀收益 + 独立循环尾项 = 无限总值”，共25×7×6=1050个完全合成精确有理数恒等式，不是1050个真人行动。额外针对原论文TFT/TFT、ALLD/TFT、ALT_DC/TFT三个模式逐值独立解析与状态机精确吻合。

独立数学审计2：在原先TFT/TFT和WSLS/WSLS本应首轮CC的理想路径中，外部强制首轮只有行玩家执行D（对手仍C），之后不再注入任何执行噪声，双方依原规则继续。TFT两人六轮的实际行动是DC,CD,DC,CD,DC,CD，缺少自主恢复；WSLS两人的实际行动是DC,DD,CC,CC,CC,CC，第三轮即共同合作恢复。此结论仅适用于单次单方误执行、后续无随机噪声的明定toy，不可以宣称现实TFT永久无法在所有机制中恢复或Nowak1993全文演化模型已重现。

有限已知终局、完全信息且单期D对C和D均严格最优的N轮PD，在共同理性和子博弈完美均衡下每一期D（从末期逆向归纳）；不能从此推说真实有限实验受试者一律全背叛。有限N和几何随机停止不可混。测试至少45独立unittest，严格边界与w=1拒绝，无真人逐行E2。真实Github CI success，机器人写回代码、测试、科研报告SHA256收据，main独立回读后才关闭有界学习，状态 LEARNING_COMPLETE_BOUNDED_AXELROD_HAMILTON_1981_TFT_TWO_INVADERS_AND_NOWAK_SIGMUND_1993_PAVLOV。研究顺序不变。
