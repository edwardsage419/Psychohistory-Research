# TH136 跨历史制度与心理测量等值：潜变量标尺、锚定情景和多群组对齐

研究日期与英文文献检索日期：2026-10-30（Asia/Singapore）。状态：THEORY_NOTE_BOUNDED。
目标键：(theory,CROSS_HISTORICAL_PSYCHOMETRIC_INVARIANCE_ANCHORING_ALIGNMENT,theory-v1,latent scale and vignette/alignment assumption failures)。
本轮已读取TH135、C007、D002、R233/R234/R236科研索引、R271 S67交接和开放Codex PR摘要。已知R233/R234有限人工世界中的潜均值和截距漂移观察等价结论。本轮属于非盲态原始理论阅读、原刊数字审计和竞争方法比较，未重复冻结R系列拟合。

## 一、原始来源与实际阅读范围

S1 [B：出版社原刊摘要及书目，未获取付费全文] Meredith W (1993). “Measurement Invariance, Factor Analysis and Factorial Invariance.” Psychometrika 58(4):525–543. DOI:10.1007/BF02294825。https://www.cambridge.org/core/journals/psychometrika/article/abs/measurement-invariance-factor-analysis-and-factorial-invariance/914A4C29515ACA7E0554B9E79F20D36C 。原作者提出弱、强、严格因子等值与公平性的理论问题；未核其全部数学证明。
S2 [A限定：PMC开放原刊在搜索结果中可见的方法、结果、表1及讨论长段落；打开全文遇验证页] Putnick DL, Bornstein MH (2016). “Measurement Invariance Conventions and Reporting: The State of the Art and Future Directions for Psychological Research.” Developmental Review 41:71–90. DOI:10.1016/j.dr.2016.06.004。https://pmc.ncbi.nlm.nih.gov/articles/PMC5145197/ 。审阅157篇初筛、126篇纳入、269项检验及各等值层级的报告方式；未逐页通读所有附表。
S3 [A：开放原刊直接阅读第2至6节、表1及Monte Carlo章节] Muthén B, Asparouhov T (2014). “IRT Studies of Many Groups: The Alignment Method.” Frontiers in Psychology 5:978. DOI:10.3389/fpsyg.2014.00978。https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2014.00978/full 。含CIVED1999、ICCS2009的17个连接题与28组比较；作者是所用Mplus软件的开发者，需披露这一利益关系，不为本项目引入收费软件。
S4 [B：作者原始网页摘要、机构PDF归档元数据，全文PDF本轮429] King G, Murray CJL, Salomon JA, Tandon A (2004). “Enhancing the Validity and Cross-Cultural Comparability of Measurement in Survey Research.” American Political Science Review 98(1):191–207. DOI:10.1017/S000305540400108X。https://gking.harvard.edu/publication/enhancing-the-validity-and-cross-cultural-comparability-of-measurement-in-survey-research/ 。机构PDF https://dash.harvard.edu/bitstreams/7312037c-7d27-6bd4-e053-0100007fdf3b/download 。2004为修正2003年初刊印刷错误的版本，不能计作两项独立证据。
S5 [B：原刊PubMed摘要] Heine SJ, Lehman DR, Peng K, Greenholtz J (2002). “What's Wrong With Cross-Cultural Comparisons of Subjective Likert Scales? The Reference-Group Effect.” Journal of Personality and Social Psychology 82(6):903–918. DOI:10.1037/0022-3514.82.6.903。https://pubmed.ncbi.nlm.nih.gov/12051579/ 。讨论文化内参照群体造成的自评标尺差异，全文未通读。
S6 [B：原始工作论文摘要，PDF未取得] Kapteyn A, Smith J, van Soest A, Vonkova H (2011). “Anchoring Vignettes and Response Consistency.” RAND Working Paper WR-840，无DOI。https://econpapers.repec.org/paper/ranwpaper/wr-840.htm 。研究五个健康领域，非参数结果支持睡眠领域的一致性条件，对其他领域的拒绝也可能涉及辅助假设。
S7 [B：原刊出版社摘要] von Davier M, Shin HJ, Khorramdel L, Stankov L (2018). “The Effects of Vignette Scoring on Reliability and Validity of Self-Reports.” Applied Psychological Measurement 42(4). DOI:10.1177/0146621617730389。https://journals.sagepub.com/doi/10.1177/0146621617730389 。锚定调整后alpha或相关升高可能在假设不满足时出现。
S8 [B：作者官网摘要及原刊书目] King G, Wand J (2007). “Comparing Incomparable Survey Responses: Evaluating and Selecting Anchoring Vignettes.” Political Analysis 15(1):46–66. DOI:10.1093/pan/mpl011。https://gking.harvard.edu/publication/comparing-incomparable-survey-responses-new-tools-for-anchoring-vignettes/ 。锚定情景的选择和评价需要独立方法约束。
S9 [B：原刊书目及摘要] Chen FF (2007). “Sensitivity of Goodness of Fit Indexes to Lack of Measurement Invariance.” Structural Equation Modeling 14(3):464–504. DOI:10.1080/10705510701301834。https://doi.org/10.1080/10705510701301834 。拟合指标对参数违例的敏感性依赖违例结构及样本特征；未重跑原模拟。

检索均为英文原刊、作者、机构或英文书目站点。没有购买论文、使用付费API或转载第三方全文。

## 二、16项理论命题、机制、反例与适用边界

T136-01 [S1,S2] 跨群体与跨期分数比较必须检查构念、题目映射及测量误差是否可比。相同问卷措辞无法独立证明同一潜在状态。
T136-02 [S1,S2] 构型、载荷、截距/阈值、残差等值分别施加不同限制。仅构型相同不足以直接比较潜均值。
T136-03 [S2] 拟合准则和部分等值释放规则存在研究者选择空间。报告应保存完整约束、检验次序及释放题目理由。
T136-04 [S3] 二元IRT项目的难度和区分度随群体变化时，观察分数差异可由真实能力和项目参数共同产生。
T136-05 [S3] Alignment允许部分项目参数变化，利用跨群组近似稳定结构估计潜均值，适用于多群组候选比较。
T136-06 [S3] 多数项目发生同向漂移时，alignment的稀疏违例假设可能失效；原作者明确指出其可能错把漂移多数当作锚。
T136-07 [S3] 原作约25%非等值比例属于经验警示，需结合群组数、样本量和漂移模式进行Monte Carlo压力测试，不能作普适合格阈值。
T136-08 [S4,S8] 锚定情景通过受访者对假想人物的评分提供回答阈值信息，依赖情景等价和自评/情景应答一致性。
T136-09 [S6,S7] 锚定假设可能在不同健康领域或样本失效；调整后相关或alpha变高不能自动当作效度提升。
T136-10 [S5] 参考群体不同可能改变Likert分数。竞争解释包括真实文化差异、样本构成和翻译差异，单个自评均值不能识别贡献。
T136-11 [S2,S9] 大样本可能拒绝微小精确等值偏离，宽松拟合判据又可能遗漏实质性漂移。需检验实际潜均值和排序对限制的敏感性。
T136-12 [S3] CIVED1999和ICCS2009是两波调查，不可当作同一批人纵向跟踪；国家比较还受样本、年龄与题目版本影响。
T136-13 [方法推断] 历史医疗编码、教育考试、政治自由问卷和幸福感自评都需要分开登记类别定义、潜变量标尺、样本框和版本。
T136-14 [方法推断] 历史语义、翻译、政治敏感性与教育背景可能改变锚定情景的理解；须对锚本身做跨期验证。
T136-15 [R233/R234范围] R系列已在冻结人工世界证明部分观察等价，本轮仅补充原作真实调查案例、方法假设及失败条件，未产生新R验收。
T136-16 [规范边界] 即使跨期量尺达到等值，人生价值权重和政策目标仍属主体选择，不能从统计等值推出普适唯一最优人生或历史必然性。

## 三、8项算术核验与人工反例

E136-01 [S3原刊] CIVED分析样本29,449与ICCS分析样本10,643合计40,092；14国×2波=28群组。40,092是两个横断面样本合计，不能当作纵向配对人数。
E136-02 [S3原刊] 17连接题的阈值参数33%和载荷参数11%报告非等值，简单均值22%，与作者所述平均22%相符。百分比经过舍入，不能据此恢复精确非等值参数个数。
E136-03 [S3原刊] 28群组Monte Carlo作者报告潜均值相关0.996。本轮只核对公开数值，未独立执行原Mplus模拟或核验其全部随机种子。
E136-04 [S2原刊] 初筛157篇减去31篇=126篇，包含269项等值检验。269为检验次数，不是独立论文或真人数量。
E136-05 [S2原刊] 残差等值110/269=40.89%约41%；载荷220/269=81.78%约82%；截距232/269=86.25%约86%。每层实际检验的子样本不同，不能把其成功比例用总论文数作分母。
E136-06 [人工观察等价] 连续量表Y=nu+lambda×eta。初期(nu,lambda,eta)=(0,1,2)得Y=2。后期世界甲(1,1,2)得Y=3，世界乙(0,1,3)也得Y=3。可见上升1不能唯一识别潜态上升。
E136-07 [人工IRT观察等价] 令P(Y=1)=1/(1+exp(-(eta-b)))。世界甲(eta,b)=(0,0)与世界乙(1,1)都给0.5；共同平移潜态与题目难度保持可见概率。
E136-08 [人工锚定失败] 两组自评分数同为4，对同一文字情景因文化语义分别理解为高低不同状态，情景分数不同。该差异可来自情景理解或回答阈值，未验证情景等价时无法唯一分解。

E136-01/02/04/05为原刊汇总算术，E136-03仅为原作者模拟指标核对，E136-06/07/08为人工反例。真实原始学生或健康调查记录复算0，独立因果估计0，前瞻预测0。

## 四、四层联系、竞争方法与下一步

个体层：参照群体、潜在状态、回答阈值和认知偏差。群体层：文化、年龄及网络形成共同语义。制度层：调查平台、学校测验、医疗编码和政策披露。历史层：制度更替、翻译与语义长期漂移。以上为待检验的机制联系。

严格等值适合有可信固定锚、可检验约束的设计。部分等值需要预先说明释放哪些参数及原因。Alignment适合多群组且多数参数近似稳定的情景，须审计违例比例与群组规模。锚定情景适合可检验情景等价和应答一致性的自评问卷。四种方法均应保留原始分数、锚选择、替代模型与排名敏感性；不能选出普适唯一最优方法。

未来最小验证清单：固定构念和历史目标总体；逐题核对翻译及版本；检查构型、载荷、阈值、残差；对alignment做违例结构模拟；对情景锚检查等价和应答一致性；以外部行为指标及负对照检验语义漂移；核查失访、样本构成和历史冲击；报告不可识别部分与规范性权重。

C今日：2026-10-30的C007已完成，本轮只读。D本周：2026-W44的D002已完成，本轮只读。未读取用户个人敏感资料，未开发个人决策产品，未主动运行CI。R系列新增E1/E2/E3均为0。现有R073及PESEN冻结不变。
下一专题TH137：历史词义漂移、跨语言锚定与多群组等值的反证设计；避开R237/R238已完成的模型拟合。
