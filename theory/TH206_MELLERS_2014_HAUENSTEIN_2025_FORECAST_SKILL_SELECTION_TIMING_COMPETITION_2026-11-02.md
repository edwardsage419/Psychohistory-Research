# TH206：地缘政治预测竞赛中的训练、团队效应与选择性作答竞争解释

track: theory
date: 2026-11-02 (Asia/Singapore)
target_key: (theory,MellersEtAl2014+HauensteinEtAl2025,2014-published+2025-published,training_teaming_forecast_accuracy_vs_latent_skill_item_selection_and_timing)
status: THEORY_NOTE_BOUNDED; PRIMARY_FULL_TEXT_SELECTED; HISTORICAL_FORECAST_REPLICATION_NOT_RUN; NO_R_E1_E2_E3_UPGRADE

## 1. 原始来源与实际阅读范围

[A] Barbara Mellers, Lyle Ungar, Jonathan Baron, Jaime Ramos, Burcu Gurcay, Katrina Fincher, Sydney E. Scott, Don Moore, Pavel Atanasov, Samuel A. Swift, Terry Murray, Eric Stone, Philip E. Tetlock (2014), *Psychological Strategies for Winning a Geopolitical Forecasting Tournament*, *Psychological Science* 25(5):1106–1115, DOI 10.1177/0956797614524255。直接阅读加州大学eScholarship保存的原作者期刊论文PDF，文件内部页码1至10，重点Methods、Design、Participants、Questions and measures、Results、Table 1、Decomposition of skill、Discussion。原始PDF：https://escholarship.org/content/qt4rg4n9vr/qt4rg4n9vr.pdf 。这是原文公开副本，非二手摘要。PDF表格依据可检索的原刊文本读取，Table 1图像逐格人工校验本轮NOT_RUN。

[B] Clifford E. Hauenstein, Rick P. Thomas, David A. Illingworth, Michael R. Dougherty (2025), *Rethinking the Role of Teams and Training in Geopolitical Forecasting: The Effect of Uncontrolled Method Variance on Statistical Conclusions*, *Psychological Science* 36(1):3–18；2024-12-04在线发表；DOI 10.1177/09567976241266481。直接阅读出版社免费正式全文的Introduction、Applying IRT to Forecasting、Open Practices Statement、Method、Model description and analysis approach、Tables 1至6、Results、Discussion；特别核验Table 1样本、Table 2参数、Table 3 DIC、Table 4潜在预测能力效应和局限。原文：https://journals.sagepub.com/doi/full/10.1177/09567976241266481 。公开全文与作者原始研究，属于对既有竞赛数据的探索性重分析，独立新参与者实验NOT_RUN。补充材料和OSF代码未读取，数据未下载或复算。

[C] Mellers et al. (2015), *Identifying and Cultivating Superforecasters as a Method of Improving Probabilistic Predictions*, *Perspectives on Psychological Science* 10(3):267–281, DOI 10.1177/1745691615577794；仅出版社正式摘要与书目核验，全文NOT_READ，禁止援引其具体表格。

## 2. 2014年原始现场研究的估计对象

2011-2013两年预测竞赛覆盖199个地缘政治结果，作者记载2011-2012有85个问题结案计分、2012-2013有114个问题结案计分。首年共2246参与者，其中1593为调查预测者、653为预测市场交易者；第二年1648人，其中943为调查预测者、705为预测市场交易者。首年调查预测者随机分配到实验条件，第二年混合了保留原条件、重新分配与新招募者，超级预测者依据前一年表现挑选入组，故超级预测者条件不具同等随机化资格。

2014年用每日、问题、参与者平均的标准化Brier分数比较训练、独立作答、群体讨论和历史表现筛选。原文报告首年训练F(2,1586)=14.29、p<.001；首年群体影响F(2,1586)=60.68、p<.001；次年概率训练F(1,882)=19.12、p<.001；次年团队F(1,882)=62.76、p<.001。Table 1的次年末周平均Brier，独立无训练0.26，团队无训练0.16，超级预测者0.07。它们是特定时段和样本的已发表汇总，不构成同一预测题目集合上的个人能力因果差值。原文也记录超级预测者平均每题更新7.8次，常规团队和独立预测者的更新次数远少。

原作者在问题内标准化以缓解自选题目差异，并以首次预测日期和更新次数作回归控制。该处理未强制不同实验条件预测相同题目，也未强制相同预测时点。原作者报告的随机分配为重要现场实验设计证据；其结论的具体外推对象仍受测量和执行过程限制。

## 3. 2025年同一历史资料的独立竞争重分析

2025年作者使用Good Judgment Project公开Dataverse（2019年2月下载版本），将分析限制为已验证的二元结果问题：首年874名预测者、94个二元题目、36115次预测；次年1235名预测者、111个二元题目、60520次预测。与2014年论文结案题目85/114和总报名人数2246/1648口径不同。不得直接将两文的分母和统计量视为同一抽样框。2025年作者明确承认重分析未预注册、筛选规则与旧论文存在差异。

新方法同时建模：潜在预测能力θ1、选择何题作答的潜在倾向θ3、选择早晚作答的潜在策略θ2、题目难度βi及题目难度随时间变化的λi。方法方差模型M4至M7允许题目选择与作答时间对潜在能力估计发生交叉载荷；M2基准模型不允许该交叉载荷。该方法要求潜在变量结构、参数识别及时间机制假设成立，结论受模型设定影响。

正式Table 4：首年团队效应M2 d=+0.766、95%可信区间[0.591,0.955]；M7 d=−0.285、区间[−0.414,−0.156]。次年排除超级预测者时，团队M2 d=+0.256、区间[0.123,0.414]；M7 d=+0.065、区间[−0.062,0.200]。训练在次年同一比较中M2 d=+0.174、M7 d=+0.038。M7与M2系数属于不同潜在变量测量模型，符号变化不是直接观察到的真实训练伤害。

正式Table 3显示次年排除超级预测者后，首、末、平均预测的最优DIC模型分别为M5、M4、M5，这些模型按参数设计约束潜在能力的实验条件均值差为零。DIC较好只支持指定模型族内的相对拟合，无法单独证明真实因果效应为零。首年最佳模型均为M7，次年包含超级预测者的估计受非随机入组影响。

2025年原文记录，首年36115次预测中5054条时间戳早于起始时间，被设置为起始日；次年60520次中197条同样处理。验证日期后的首年563条、次年277条记录改为缺失。上述清理是影响重算的明确版本条件，不能忽略。

## 4. 可核查的数学反例与因果竞争

二元事件真实发生概率为p，预测者报告真实概率p，若采用2014年两类别平方误差相加的Brier定义，期望分数为2p(1−p)。当p=0.9时为0.18；p=0.5时为0.50。两位预测者均完全校准，选择较容易、基率远离0.5的题目者仍可取得较低平均Brier。由此可严格推出：在题目选择不同的条件下，正确概率报告与较低平均误差可以同时出现，平均分数差异无法唯一识别更强的潜在预测能力。这是合成概率反例，未使用真实竞赛数据。

原文中Brier对固定题目保持严格适当性。此性质不能自动保证自选不同难度题目、不同响应时间的跨人均分可比。题目内标准化可处理部分难度差异，剩余选择性、时间依赖及缺失机制仍需核验。

竞争解释A：训练与讨论提高对相同题目、相同时点的概率判断能力。竞争解释B：干预改变题目选择、参与频率、信息获取和更新时间，使评分改善。竞争解释C：干预同时改变能力与行为策略。2025年对B提供了新的模型支持，仍无法唯一排除A或C。题目选择和作答时点可能是干预后中介，若强行控制会改变估计对象；控制后的潜在能力效应与完整制度干预的总效果应分开报告。后续研究需预先冻结题目集、时点、评分、缺失规则与训练随机化，再分别估计总效果与同题同窗的能力差异。

## 5. 四层关联、测量边界和研究顺序

个体层：概率判断、认知训练与信心校准；群体层：讨论、共享信息、团队参与；制度层：竞赛评分、题目菜单、更新激励和奖励；历史层：2011-2013特定地缘政治题目、结案时间和环境信息变化。跨层只作局部关联，不形成统一模型。

2014年样本多数美国男性且有大学教育资格，不能直接推广至其他文化、历史时期和职业预测制度。2025年再分析使用同一竞赛历史数据，不能当成独立新样本验证。原始补充材料、OSF/JAGS代码、Dataverse数据、IRT参数重算、外部团队复核和真实未来预测均NOT_RUN。Mellers2015仅摘要；任何外推应保持条件性。

与TH205区分：TH205检验启发式搜索规则、实验顺序和人类是否采用TTB；TH206独立检验概率预测竞赛中训练/团队干预的测量对象及2025年同数据竞争重分析。与TH076区分：TH076关注预测部署、反馈与政策损失；TH206关注自选题目、响应时点与潜在预测能力的识别。

C当日：C010于2026-11-02已完成，原文件只读，未创建C011。D本周：D003于2026-W45的2026-11-02已完成，原文件只读，未创建D004。

## 6. 本轮执行和下一步

Python标准库Fraction合成算术断言5项PASS，检验2p(1−p)、p=0.9/0.5和已发表效应系数差值。它们仅证明指定算术，未重现2014年现场实验或2025年IRT结果。

下一步：先读Merkle等2016/2017年原始IRT模型，核对2025年补充材料中的交叉载荷、先验和缺失模型；必要时只做理论可识别性审计。保持跨学科轮换，不因同一预测专题连续扩张TH。R073、PESEN v0.1及R系列E1/E2/E3、MARKET分级不变；全部R完成后才统一分类，随后有条件熔炼。费用新增操作0；账户实际计费NOT_VERIFIED。GitHub Actions不主动触发。
