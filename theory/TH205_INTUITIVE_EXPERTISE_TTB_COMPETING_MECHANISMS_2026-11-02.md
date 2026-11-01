# TH205 原始研究：专家直觉的环境效度、单线索搜索与真人策略异质性

track: theory
subflow: primary_theory
run_date: 2026-11-02 (Asia/Singapore)
observed_head_before_write: 302170861c7d16c82cedd931bcde7fcb3d46a29d
target_key: (theory, KahnemanKlein2009+GigerenzerGoldstein1996+NewellShanks2003+NewellWestonShanks2003, original-published-selected-pages, expert-intuition-validity-vs-fast-frugal-heuristic-vs-observed-strategy)
status: COMPLETE_BOUNDED_PRIMARY_READING; NO_REAL_DATA_REESTIMATION; NONBLIND
evidence_class: THEORY_ORIGINAL_READING; ORIGINAL_SIMULATION; ORIGINAL_HUMAN_EXPERIMENTS_REPORTED_NOT_REPLAYED
freeze_preserved: R073; PESEN_v0.1; R_E1_E2_E3; MARKET_SEPARATE

## 原作来源与直接阅读范围

[A1] Daniel Kahneman & Gary Klein (2009), *Conditions for Intuitive Expertise: A Failure to Disagree*, *American Psychologist* 64(6):515至526, DOI 10.1037/a0016755。大学公开的原刊排版PDF https://bear.warrington.ufl.edu/brenner/mar7588/Papers/kahneman-klein-2009.pdf 。直接审读印刷pp515至525的Two Perspectives、Skilled Intuition as Recognition、Imperfect Intuition、Professional Intuitions、Augmenting Professional Judgment和Conclusions；pp526参考文献未逐条核验。属于作者共同提出的理论边界与既有研究评论，不是该文新做的随机实验。

[A2] Gerd Gigerenzer & Daniel G. Goldstein (1996), *Reasoning the Fast and Frugal Way: Models of Bounded Rationality*, *Psychological Review* 103(4):650至669, DOI 10.1037/0033-295X.103.4.650。MIT机构保留的原刊排版PDF https://web.mit.edu/curhan/www/docs/Articles/biases/Gigerenzer_Goldstein_Reasoning%20Fast%20and%20Frugal.pdf 。直接审读pp650至659的任务定义、Take The Best搜索/停止/决策规则、经验支持与83城模拟方法和初步结果；p655 Table1与有限N判别率公式经原刊页面图像目视核验。pp660至669其余结果和附录未逐格复核，不能称全文数值复算。该论文主要新增的是使用真实城市特征构造的计算模拟；文中引用其他真人实验，不能当成本次独立读取那些实验。

[A3] Ben R. Newell & David R. Shanks (2003), *Take the Best or Look at the Rest? Factors Influencing “One-Reason” Decision Making*, *Journal of Experimental Psychology: Learning, Memory, and Cognition* 29(1):53至65, DOI 10.1037/0278-7393.29.1.53。作者大学网站公开原刊PDF https://www2.psy.unsw.edu.au/Users/BNewell/NS2003.pdf 。直接审读pp53至57的设计、Experiment1及Table1/2，pp58至63的Experiment2/3结果与General Discussion指定段落；p57 Table2经图像目视核验。pp64至65参考文献和附录未逐项核验。作者页面明确仅供非商业学术使用、不得未经许可再上传，仓库只存原创分析与链接。

[A4] Ben R. Newell, Nicola J. Weston & David R. Shanks (2003), *Empirical Tests of a Fast-and-Frugal Heuristic: Not Everyone “Takes-the-Best”*, *Organizational Behavior and Human Decision Processes* 91(1):82至96, DOI 10.1016/S0749-5978(02)00525-3。作者大学公开原刊PDF https://www2.psy.unsw.edu.au/Users/BNewell/NWS2003.pdf 。直接审读pp82至83、88至92的原始实验分类、表4和讨论；其余页未完整审读。该文与[A3]由同一研究团队开展，属于不同实验报告，不能视为完全独立团队复现。

## 原作命题与独立竞争解释

1. [A1]认为专家直觉可靠的必要条件包括环境有可学习的稳定有效线索，以及个体有足够的实际练习与清晰反馈。作者区分消防、医疗诊断中的部分高效任务与长期政治预测、个股方向等低效度任务。高效度不等于无随机性；专业资历与主观确信无法直接替代独立准确率测量。作者提出“fractionated expertise”，同一人在不同子任务可能有完全不同的能力。长期政治事件“不可预测”的强措辞属于该文根据既有证据提出的解释，未建立所有历史事件和时间尺度的数学不可能定理。
2. [A2]提出Take The Best(TTB)：在仅识别一个对象且识别与目标相关时用识别规则；两个对象均识别时，按线索效度排序查询，遇到第一个区分线索便停止，选择该线索指向的对象。它是非补偿式的过程模型，不能用一个人的选择正确率直接证明其真的遵守搜索、停止和选择三个过程规则。识别启发式与[A1]专家经验形成的模式识别是不同机制。
3. [A2]德国83城市、9个二元线索的模拟，设置6档线索知识、84档城市识别和每格500名合成个体，对3403个城市对做推断。26名芝加哥学生的先导调查提供约80%的识别效度设定。回归比较器权重使用全部83城市的真实人口，包括合成个体未识别的城市；这不是跨时代、跨地区或严格留出城市的预测检验。作者报告TTB在该环境准确率与若干整合算法相当，搜索量更低；此结论受城市参考类、识别率、线索效度、缺失填补和模拟知识生成假设限制。
4. [A3]真人实验1有16名参与者，每人60训练试次和120测试试次，四个二元线索，随机分配高/低相对信息成本。原刊Table2记录高成本组平均购买1.36个线索、发现区分线索后继续购买的比例0.15；低成本组分别2.54与0.64。后者为按参与者汇总的平均比例，不能未经原始数据检查转换成精确试次数。实验2给出线索效度顺序提示，实验3使用确定性结果，均仍观察到部分违反停止规则的行为。跨实验比较不能直接等同同一随机化处理的净因果效应。
5. [A4]两个实验各24人，共48人；作者用允许10%错误的规则，把16/48约33%分类为同时满足TTB搜索、停止、选择条件。该33%是特定任务和分类阈值下的观察结果，不能作为所有人的固定TTB采用率。原作同时指出部分人只采用一个规则或额外查询信息，策略可能因信息成本、风险和反馈改变。
6. [A1]中的专家经验学习理论、[A2]的简约搜索算法和[A3/A4]的真人过程观察保留竞争关系。高效度环境可能允许经验直觉，也可能允许统计模型获益；算法在某一模拟环境获胜并不能推出真实人类普遍采用；真人选择正确也无法唯一识别内在搜索机制。未来对R的理论问题仅为：何种任务存在稳定线索、可检验反馈、可观测搜索过程及时间漂移？本轨未拟合R模型或评估R预测。
7. 构造性反例：假定两条线索中第一条对训练环境的区分正确率为0.9，部署环境由于制度变化降为0.1，TTB若保持原排序则预测方向可系统性反转。该构造仅说明无稳定性条件时，训练环境效度不能保证跨环境有效；数值是人为设定，无真人/历史数据支持。另一个反例是观察到相同最终选择时，一位决策者仅查询首个线索，另一位查完全部线索但同意首个结论，行为结果相同而过程不同。必须记录查询顺序与停止点才能区分。

## 数学边界与人工精确检查

[A2] p655对N个对象、正负线索边际比例x与y（x+y=1）定义不放回随机配对的区分率 d=2xy/(1-1/N)。本轮仅用Python标准库Fraction枚举N=4的6个无序配对，检查2正2负时d=2/3、1正3负时d=1/2、全负时d=0；公式与枚举逐一相等，合计4项断言PASS。该测试仅证明有限N算术一致，不验证原作者83城数据、真人行为、现实因果或历史预测。若含未知值、权重抽样或不同参考类，公式不能直接套用。

## 适用层级、识别与限制

个体：专家直觉、策略切换、主观信心、信息购买及反馈。群体：专业共同体对专家的声誉评价可能与外部预测准确率分离。制度：组织任务、绩效反馈、成本、行动后果和算法监管决定学习条件。历史：制度和线索结构改变可能破坏跨期外推。四层联系仅是局部研究问题，没有统一分类或模型融合。

未读取[A1]引用的Meehl1954、Grove2000、Tetlock2005原著，不能把其转述升级为本轮独立证据。[A2]原始83城9线索数据未重建，全部模拟未复算。[A3/A4]没有真人逐试次数据或随机化日志复算，分组效应的外部效度和实验者选择仍有限制。无真实个人敏感数据、无产品实现、无新增费用；账单NOT_VERIFIED。R E1/E2/E3与MARKET分级不变。

## 本轮子流程、测试与下一步

C010：2026-11-02 COMPLETE，只读，未新增C编号。
D003：2026-W45，2026-11-02 COMPLETE，只读，未新增D编号。
数学人工检查：4 PASS；真实原始实验重算、独立现实因果估计、历史预测：NOT_RUN；CI：NOT_RUN。
下一步优先补读[A2] pp660至669的模拟结果与附录，独立核验原作线索表可否合法重建；另找原始专家直觉的前瞻性校准研究，防止连续停留于同一微主题。R全部完成前仅储备竞争理论。
