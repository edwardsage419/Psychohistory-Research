# C004 动态效用权重、多目标偏序与鲁棒决策：候选测量方法

研究日及检索日期：2026-10-27（Asia/Shanghai）。状态：METHOD_NOTE_BOUNDED。2026-10-27 首项实质增量。只研究候选方法、适用条件与验证清单。无个人健康、财务、关系等敏感资料，无产品开发。

## 一、原始书目与阅读等级

[A] Schwartz, Shalom H. (2012). “An Overview of the Schwartz Theory of Basic Values.” *Online Readings in Psychology and Culture* 2(1), DOI https://doi.org/10.9707/2307-0919.1116 。开放原刊 https://scholarworks.gvsu.edu/orpc/vol2/iss1/11/ ，完整原刊公开副本 https://www.rwlnetwork.org/media/66744/an_overview_of_the_schwartz_theory_of_basic_values.pdf 。直接审读价值相容与冲突、SVS与PVQ量表、价值优先次序的原文段落。原作是价值心理学，以下多目标优化为本项目方法推导。
[B] Keeney, Ralph L. (1971). “Utility Independence and Preferences for Multiattributed Consequences.” *Operations Research* 19(4):875–893, DOI https://doi.org/10.1287/opre.19.4.875 。出版社原刊摘要 https://pubsonline.informs.org/doi/10.1287/opre.19.4.875 与作者机构书目 https://scholars.duke.edu/publication/1126388 已核，全文未审；可加效用需要检验偏好独立等条件。
[B] Greco, Salvatore, Vincent Mousseau & Roman Słowiński (2008). “Ordinal Regression Revisited: Multiple Criteria Ranking Using a Set of Additive Value Functions.” *European Journal of Operational Research* 191(2):416–436, DOI https://doi.org/10.1016/j.ejor.2007.08.013 。原刊摘要 https://www.sciencedirect.com/science/article/pii/S0377221707008752 已核。作者2005年开放工作稿 https://www.lamsade.dauphine.fr/CahiersLAMSADE/CahiersLamsade240.pdf 检索到，但直接读取超时，不能标记全文审读。作者提出对所有相容价值函数成立的必要偏好与对至少一个相容函数成立的可能偏好。
[B] Lahdelma, Risto, Joonas Hokkanen & Pekka Salminen (1998). “SMAA: Stochastic Multiobjective Acceptability Analysis.” *European Journal of Operational Research* 106(1):137–143, DOI https://doi.org/10.1016/S0377-2217(97)00163-X 。作者机构摘要 https://sal.aalto.fi/publications/abstracts/plah98.html 和大学书目 https://research.aalto.fi/en/publications/smaa-stochastic-multiobjective-acceptability-analysis/ 已核；全文未审。该方法在权重空间和输入不确定性下计算接受度，概率化权重空间本身需要正当化。
[B] Strotz, R. H. (1955). “Myopia and Inconsistency in Dynamic Utility Maximization.” *Review of Economic Studies* 23(3):165–180, DOI https://doi.org/10.2307/2295722 。出版社书目 https://academic.oup.com/restud/article-abstract/23/3/165/1532695 已核，付费全文未读。动态不一致作为后续待审理论线索。
所有来源均为非中文网站，检索日同上。A为直接原文指定章节，B为原刊摘要及书目。

## 二、候选人生状态测量与主观价值约束

候选维度：身体与现实条件、财务资源、精神体验、社会关系、能力成长、环境与自由度。每维需预先说明可观察代理量、观察窗口、单位、量表方向、测量误差、重测信度、内容效度及缺失原因。例：财务流动性是资源代理，不能等同福祉；社交次数不能等同关系质量；主观幸福评分可能受反应转移影响。所有数值只是未来可检验指标，不构成个人诊断或价值规范。

M1：价值权重由决策者在特定时间和信息下作出主观选择。研究者可量化可观察后果，不能从行为数据唯一反演规范性权重。
M2：线性加权 U_t(a)=Σ w_{jt} x_{jt}(a) 仅是有条件的候选模型。需要指标同向归一、可比性、可补偿性及偏好独立性审查。生存底线、不可交易权利等约束可能使加权形式不适用。
M3：先报告Pareto非支配集合及必要/可能偏好，再报告指定权重下的排序。偏序与多解是合法研究结果。
M4：权重不确定时使用集合W_t，比较 min_{w∈W_t}[U_w(a)-U_w(b)] 与 max。只有最小值为正才能称a在该集合内稳健优于b；集合W_t的界限依赖研究者或参与者的主观设定。
M5：SMAA类接受度依赖给权重分配的概率测度。没有可信权重分布时，只报告几何比例并明确其为约定，不能称现实概率。
M6：动态权重 w_{t+1} 可受价值学习、资源冲击、适应、社会压力和量表重校准影响。观察到评分变化不自动证明偏好改变。
M7：风险偏好、损失函数、折现与多目标权重属于不同模型部件。未来比较必须固定情景概率、损失口径与决策时域。
M8：动态决策可能存在时间不一致和承诺装置。Strotz 1955是原始研究线索，全文缺口未补前不援引具体定理。
M9：缺失非随机、共同方法偏差、行动选择反馈及指标可操纵性均可能影响推断。须继承C002、C003的纵向等值与缺失敏感性审计。
M10：可选N-of-1或微随机研究只作为未来设计候选。需要自愿知情、可逆低风险干预、随机化可行性、无干扰和序列依赖检查，不能用观察数据冒充反事实识别。

## 三、可复核人工计算与反例

E1 [人工，权重敏感性] 设A=(0.8,0.4)、B=(0.5,0.8)，第一维代表抽象成长、第二维代表抽象资源，两维均已假设无量纲且越高越好。令w为第一维权重，则U(A)-U(B)=0.7w-0.4。w>4/7时A较优，w<4/7时B较优。w∈[0.3,0.7] 时两种偏好均可能，稳健必要排序为空。假设w在区间上均匀分布，A获胜的权重区间比例为9/28≈0.321429，B为19/28≈0.678571。该比例来自人为均匀假设，绝非现实获胜概率。
E2 [人工，动态权重] 保持A、B状态不变，w_t=0.4时U(A)=0.56、U(B)=0.68；w_{t+1}=0.7时U(A)=0.68、U(B)=0.59。最优行动反转可以完全由权重变化产生，不能据此断言外部环境发生变化。
E3 [人工，测量误差] 若每项观测得分有±0.05误差，A与B在w=4/7附近的微小效用差可被误差淹没。应对状态得分区间与权重区间联合求最坏值，避免报告伪精确单一排名。
E4 [人工，观察欠识别] 某人选择A可能源于w较高，也可能源于其主观预测A的第二维收益较高。只观测选择而不测主观信念，偏好权重与信念误差不可唯一识别。
E5 [人工，硬约束] 若某项身体安全指标必须≥0.6，方案A安全指标0.5，B为0.7，则无论A在其他维度加权分数多高，硬约束方案都会排除A。阈值0.6为人工伦理和风险约束，不能假称普适阈值。

## 四、方法验证清单与适用边界

先定义目标总体、维度和时间尺度；记录每个量表的效度、信度、响应转移、缺失机制；区分事实性后果与规范性权重；检查偏好独立和可补偿假设；报告Pareto集合、必要/可能偏好、权重敏感性及风险尾部；区分偏好改变、环境改变和信息改变；预先指定纵向外推、反事实识别和撤销条件。若资料不足，明确报告不可识别或部分识别。此文没有提出普适唯一最优人生，也没有读取私人资料、计算真实个人分数或开发产品。

下一研究日候选：多维生活状态的测量不变性、跨维效用交互与N-of-1序贯因果识别条件，先查当日研究日历。