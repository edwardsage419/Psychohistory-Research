# C009 等待的信息价值、行动可逆性与跨期偏好锚点

研究日期与英文来源检索日期：2026-11-01（Asia/Singapore）。状态：METHOD_NOTE_BOUNDED。目标键：(theory-C,OPTION_VALUE_INFORMATION_REVERSIBILITY,methods-v1,delay_cost_information_quality_normative_choice)。本轮新的一天独立方法增量，承接C008动态偏好、稳健后悔和价值标尺问题。仅提出未来候选方法和验证清单，不读取任何真实个人敏感资料，不实施个人实验或开发产品。

## 来源、阅读层级和竞争观点

1. [A，开放综述原文] Ginbo T, Di Corato L, Hoffmann R (2021，在线2020). Investing in climate change adaptation and mitigation: A methodological review of real-options studies. Ambio 50:229–241. DOI:10.1007/s13280-020-01342-8。https://link.springer.com/article/10.1007/s13280-020-01342-8 。直接审读Introduction、Review methodology、Option value、Modelling uncertainty及实证文献覆盖。67篇被纳入，原作者指出研究经常假设风险中性利润最大化、风险偏好和战略互动覆盖不足；该综述讨论的是气候投资，不能直接转作个人生活决策的实证效应。2022年更正存在，未核验其全文，引用细节须保留版本注意。
2. [B，原始论文正式摘要] Eckermann S, Willan AR (2008). The Option Value of Delay in Health Technology Assessment. Medical Decision Making 28(3):300–305. DOI:10.1177/0272989X07312477。https://pubmed.ncbi.nlm.nih.gov/18480035/ 。摘要指出等待样本信息价值须扣除信息成本、延迟机会成本和不可逆性；未读取付费全文。
3. [B，原始研究机构摘要] Kreps DM, Porteus EL (1978). Temporal Resolution of Uncertainty and Dynamic Choice Theory. Econometrica 46(1):185–200。https://www.gsb.stanford.edu/faculty-research/publications/temporal-resolution-uncertainty-dynamic-choice-theory 。正式书目及Stanford作者机构摘要，全文访问受阻。研究讨论信息在何时揭示会影响动态偏好，不能假设每人都对提前获知信息具有同一偏好。
4. [B，开放原始实验机构摘要] Devine S, Da Silva Castanheira K, Fleming SM, Otto AR (2024). Distinguishing between intrinsic and instrumental sources of the value of choice. Cognition 245:105742. DOI:10.1016/j.cognition.2024.105742。https://discovery.ucl.ac.uk/id/eprint/10187428/ 。两项实验各100人，原作者报告当行动与结果脱钩时自由选择偏好减弱；未读取PDF逐表细节。选择自由可能具有工具价值及主体本身赋予的价值。
5. [B，原刊摘要及机构书目] Strotz RH (1955/1956). Myopia and Inconsistency in Dynamic Utility Maximization. Review of Economic Studies 23(3):165–180. DOI:10.2307/2295722。https://academic.oup.com/restud/article-abstract/23/3/165/1532695 。收费全文未读；仅用于标识跨时不一致理论谱系，具体机制不归于未读原文。

## 十项候选方法命题

C009-01 [A] 不可逆成本和未来信息使等待具有潜在选择价值，必须同时计算延迟的机会成本。
C009-02 [A] 等待可能使不可逆损失增加，尤其环境或制度机会窗口关闭时，故等待价值不保证为正。
C009-03 [B] 未来信息只有在可能改变行动选择时才具有工具性价值；必须核查信息质量和获得时间。
C009-04 [B] 提前获知信息的主观价值可能独立于物质结果，单纯期望效用差不能穷尽主体偏好。
C009-05 [B] 自由选择可能同时有工具价值与内在价值，不能把可选择数量当成普适福利分数。
C009-06 [方法] 可逆性是程度变量；撤销成本、声誉、他人权益和时间窗口应分别标注。
C009-07 [方法] 多目标结果须先设主体选择的价值权重、单位和跨期锚点；改变权重可逆转排序。
C009-08 [方法] 若信号准确率、先验或外部环境未知，单个等待价值点估计不可识别，需情景区间。
C009-09 [方法] 实验与生活决策存在选择、学习、伦理及干扰差异，不能将投资实物期权公式直接当作人生规则。
C009-10 [规范] 不可逆且影响他人的行动需要保留同意、权利和风险底线；模型不能给出普适唯一最优人生。

## 17项人工数学测试中7项针对C009

纯人工两种环境H/L，各概率1/2。行动A收益H=8、L=-2；行动B收益H=1、L=3。立即选择的期望收益A=3、B=2，故此人工价值标尺下立即最优为3。等待后若完美获知环境，可选H时A=8、L时B=3，期望5.5；等待成本1后为4.5，高于立即选择1.5。等待成本升至3后净值2.5，低于立即选择3。若信号正确率3/4、先验均衡且信号对称，收到正信号选A，负信号选B，信息后期望4，扣成本1恰等于立即选择3。信号准确率1/2时信息前期望仍3，扣成本后反而下降。所有数字为人为指定的同单位效用，不对应用户财务、健康或关系资料。没有引入主观时间折现、风险厌恶、损失分布尾部、信号价格或学习的内生行为，故不能外推。

此例说明信息价值依赖行动可调整性和信号准确率。实际偏好可能随着经验变化，跨期效用标尺也可能漂移，C008的跨时锚点仍为先决条件。若把六个候选人生维度映射到模型，需要为身体和现实条件、财务资源、精神体验、社会关系、能力成长、环境和自由度分别记录可观测代理、误差、缺失、测量反应性、权利约束与价值权重；任何归一化和权重都需主体规范选择。

## 未来验证清单与四层联系

先用完全合成数据冻结行动集合、退出成本、等待成本、信号准确率区间、外部环境情景及主观权重；比较立即行动、等待信息、可撤销试验三种策略；审计信息是否真正改变最优行动，测试无信息和高延迟成本反例；报告偏序、最坏后悔与不确定区间；独立审查隐私和对他人的影响。真实N-of-1=0，真实敏感数据读取0，产品开发0，现实因果识别0，R E1/E2/E3新增0。

个体层为风险偏好、时间偏好与学习；群体层为他人权利和协商；制度层为可撤销性、机会窗口及合同约束；历史层为宏观冲击和跨时期信息环境改变。四层连接属于候选机制，未经验证。

下一C010建议：跨期主观价值锚定、可撤销行动的反事实评价与信息性缺失。D子流程2026-W44已有D002，本轮只读未新建。
