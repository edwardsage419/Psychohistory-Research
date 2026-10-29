# C007 反复测量反应性、应答转移、信息性缺失与动态偏好

研究日期及英文来源检索日期：2026-10-30（Asia/Singapore）。状态：METHOD_NOTE_BOUNDED。
目标键：(theory-C,EMA_REACTIVITY_RESPONSE_SHIFT_MNAR_PREFERENCES,methods-v1,measurement intervention × latent-scale drift × missing outcomes × value weights)。
承接C006时间序列、负对照与自相关框架。本笔记只形成未来候选方法、适用条件和验证清单；不读取用户个人健康、财务、关系等资料，不实施N-of-1、不开发个人产品。

## 一、原始来源与读取层级

C1 [A级，开放原刊直接阅读方法、结果及局限章节] De Vuyst H-J, Dejonckheere E, Van der Gucht K, Kuppens P (2019), *Does repeatedly reporting positive or negative emotions in daily life have an impact on the level of emotional experiences and depressive symptoms over time?*, PLOS ONE 14(6):e0219121. DOI:10.1371/journal.pone.0219121。https://pmc.ncbi.nlm.nih.gov/articles/PMC6597111/ 。90名学生随机分为正情绪、负情绪、非情绪内部状态三组，各30人，7天每日10次提示；组间无显著的预设情绪反应性证据。对照组也可能影响情绪，研究时间短、样本窄，不能推断普遍零反应性。
C2 [A级，开放原刊摘要与研究方法摘要，未逐表复算] Ottenstein C, Hasselhorn K, Lischetzke T (2024), *Measurement reactivity in ambulatory assessment: Increase in emotional clarity over time independent of sampling frequency*, Behavior Research Methods 56:6150–6164. DOI:10.3758/s13428-024-02346-y。https://pubmed.ncbi.nlm.nih.gov/38291223/ 及 https://pmc.ncbi.nlm.nih.gov/articles/PMC11335897/ 。313名学生被随机分为每天3次或9次提示、持续一周；情绪清晰度随时间上升，频率组间变化无显著差异，情绪愉悦度没有系统趋势。不能将组内趋势直接识别为测量因果效应。
C3 [A级，开放正式原刊直接审读方法摘要及参考文献，全文方法PDF未逐页核] King-Kallimanis BL, Oort FJ, Garst GJA (2010), *Using structural equation modelling to detect measurement bias and response shift in longitudinal data*, AStA Advances in Statistical Analysis 94:139–156. DOI:10.1007/s10182-010-0129-y。https://link.springer.com/article/10.1007/s10182-010-0129-y 。三步：确认测量模型、检验跨期参数等值、检查外生变量对指标的直接作用；模型选择与多重比较风险需审计。
C4 [B级，原刊摘要] Sprangers MAG, Schwartz CE (1999), *Integrating response shift into health-related quality of life research: a theoretical model*, Social Science & Medicine 48(11):1507–1515. DOI:10.1016/S0277-9536(99)00045-3。https://pubmed.ncbi.nlm.nih.gov/10400253/ 。重校准、价值重新排序、构念重定义的理论路径；未通读付费全文。
C5 [A级，开放原刊直接审读摘要、设计和测量反应性段] Wrzus C, Neubauer AB (2023，在线2022), *Ecological Momentary Assessment: A Meta-Analysis on Designs, Samples, and Compliance Across Research Fields*, Assessment 30(3). DOI:10.1177/10731911211067538。https://journals.sagepub.com/doi/full/10.1177/10731911211067538 。477篇、496样本、总N=677536，平均遵从率79%；475项样本约95.8%未报告测量反应性检验。跨研究汇总不能替代某个个体的因果识别。
C6 [B级，原始同行评审摘要] Eisele G et al. (2023), *A Mixed-Method Investigation Into Measurement Reactivity to the Experience Sampling Method*, Psychological Assessment 35(1):68–81. DOI:10.1037/pas0001177。https://pubmed.ncbi.nlm.nih.gov/36174163/ 。151人随机分配30/60项目与每天3/6/9次，14天；报告习惯化及部分情绪/自我觉察变化，协议与个体调节效应不一致。全文未通读。
C7 [A级，开放正式综述摘要与讨论] Stinson L, Liu Y, Dallery J (2022), *Ecological Momentary Assessment: A Systematic Review of Validity Research*, Perspectives on Behavior Science 45:469–493. DOI:10.1007/s40614-022-00339-w。https://pmc.ncbi.nlm.nih.gov/articles/PMC9163273/ 。32项与较客观参照比较的研究，符合率跨研究和指标从1.8%到100%；范围不能当作统一测量误差率。
C8 [B级，原刊摘要，开放全文未逐页读] Verdam MGE, Oort FJ, Sprangers MAG (2016), *Using structural equation modeling to detect response shifts and true change in discrete variables*, Quality of Life Research 25:1361–1383. DOI:10.1007/s11136-015-1195-0。https://link.springer.com/article/10.1007/s11136-015-1195-0 。离散指标的潜在连续因子方法，案例485名患者；样本外适用性待验。
所有检索均来自非中文网站，日期2026-10-30。C1、C3、C5指定范围直接审读，其他标明摘要层级；未获取收费文献。

## 二、10项候选方法命题

C007-01 [C1,C2,C6] 高频自我报告可能改变觉察、行为或回答方式；不同实验报告的结果不一致，应预设可能存在反应性，也保留零效应情景。
C007-02 [C1] 只改变被询问的情绪类别时，对照题可能仍引发情绪思考，排除限制不自动成立。
C007-03 [C2] 提示频率的随机分配识别的是给定协议下的频率差异；缺少完全无测量对照时，无法单独识别所有提示共同引发的变化。
C007-04 [C3,C4,C8] 同一分数的变化可能来自潜在状态变化、回答阈值重校准、指标权重改变或构念重定义；需要跨期测量等值及外部锚定。
C007-05 [C5,C7] 完成率、符合率及信度是不同指标。高完成率不能证明有效性，高内部一致性不能证明不存在系统偏差。
C007-06 [方法推断] 漏答可能由情绪低落、工作压力、关系事件、提示负担或设备问题驱动；缺失机制应按MAR/MNAR敏感性情景处理，不能仅插补均值。
C007-07 [方法推断] 若反应性同时改变真实状态与回答阈值，单一观察序列通常不能将两者拆分，需外部结果或设计上的对照。
C007-08 [C4] 偏好与价值权重会随重大生活事件、学习和适应变化；不同时间的效用函数不可在未确认标尺时直接相减。
C007-09 [方法推断] 六个候选人生维度分别需要可观察代理量、测量误差、重测信度、内容效度、缺失标记和不可识别清单。隐私优先，未来设计可用模拟数据验证。
C007-10 [规范边界] 任何效用加权和风险阈值都包含主体的价值选择；不存在经数据证明的普适唯一最优人生。不可逆选择、他人自主性及隐私不得作为自由实验变量。

## 三、7项人工与原刊数字审计

E007-01 [C1原刊] 90人分3组各30人；7天×每日10次=每人最多70次提示，10项/提示意味着每人最多700项回答，不能把700项视为700个独立参与者。
E007-02 [C2原刊] 3次/日与9次/日持续7天对应21与63个计划提示，计划负担3倍；不能从次数差异推出遵从率或因果收益3倍。
E007-03 [C5原刊] 475/496=95.7661%，与“95.8%未报告反应性检验”一致；这是一项研究报告缺口，不等于95.8%存在反应性。
E007-04 [人工标尺漂移] 真实状态S从5保持到5，回答偏移b从0变到2，观测Y=S+b从5变7。观测提升2不必代表真实状态提升。
E007-05 [人工抵消] 真实状态从5到7，回答偏移从0到−2，观测Y均为5。观测稳定也不充分证明状态稳定。
E007-06 [人工MNAR上下界] 100次计划观察、70次应答，其中42次正向，30次未知。未知应答机制下总体正向比例界为42%至72%。若70个可见结果最多7个分类错误，则保守界扩大到35%至79%；此为最坏情景，非真实调查估计。
E007-07 [人工偏好反转] 两个候选结果A=(1,0),B=(0,1)，权重从(0.8,0.2)变为(0.2,0.8)，排序随价值权重逆转。权重变化不等于数据错误，规范排序须注明主体与时点。

## 四、四层联系、冲突解释及未来验证清单

个体层：觉察、重校准、缺失与偏好学习；群体层：被观察者之间的社会比较、提示互动及干扰；制度层：调查平台、劳动日程、量表规则和隐私制度；历史层：文化语义、技术平台及长期冲击导致的测量等值变化。四层映射是研究假说，未形成因果确认。
竞争解释：自我报告趋势可由真实情绪变化、测量反应性、题项阈值漂移、季节趋势、非随机漏答、回忆误差和价值重排共同造成。随机化提示频率、外部参照、锚定题、缺失敏感性和预注册可分别提供部分约束，不能假定任何单一方法解决全部问题。
候选验证顺序：冻结目标维度及主观价值约束；使用模拟数据测试阈值漂移与MNAR联合界；明确计划/完成提示和原因；设计不侵犯隐私的外部锚定与负对照；检验跨期量表参数等值和模型选择敏感性；独立报告状态变化、反应性、偏好权重变化及不可识别范围；评估风险、可逆性与干扰。真实个人资料、N-of-1实验、产品开发均NOT_RUN。
证据边界：C1/C3/C5部分原文直接审读；其余摘要与机构出版页。人工算术7项，独立个体因果估计0，E1/E2/E3新增0。D002为2026-W44既有专题，只读未修改。
下一C专题C008：动态偏好的跨时自我比较、锚定情景与可逆决策的稳健多目标排序。
