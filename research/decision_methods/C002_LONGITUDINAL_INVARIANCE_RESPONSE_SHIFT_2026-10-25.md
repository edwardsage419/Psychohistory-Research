# C002 纵向测量等值性、反应转移与动态偏好

研究与检索日期：2026-10-25（Asia/Shanghai）。C 今日首项实质增量。
观察 main HEAD：a43c0f1ecc2fc43c36796cd61db943c0a5864539；写入前路径不存在。状态：METHOD_NOTE_BOUNDED；无个人敏感资料；无个人决策产品；无实证拟合；无收费资源。

## 一、原始来源、DOI 与审读范围

1. Sprangers, M. A. G. & Schwartz, C. E. (1999). “Integrating response shift into health-related quality of life research: A theoretical model.” Social Science & Medicine 48:1507–1515. DOI https://doi.org/10.1016/S0277-9536(99)00045-3 。PubMed 原刊摘要 https://pubmed.ncbi.nlm.nih.gov/10400253/ 已审；全文未审。
2. Vandenberg, R. J. & Lance, C. E. (2000). “A Review and Synthesis of the Measurement Invariance Literature.” Organizational Research Methods 3:4–70. DOI https://doi.org/10.1177/109442810031002 。出版社摘要已审，全文未审。
3. Oort, F. J. (2005). “Using structural equation modeling to detect response shifts and true change.” Quality of Life Research 14:587–598. DOI https://doi.org/10.1007/s11136-004-0830-y 。作者机构原刊摘要 https://pure.amsterdamumc.nl/en/publications/using-structural-equation-modeling-to-detect-response-shifts-and-/ 已审，全文未审。
4. Chen, F. F. (2007). “Sensitivity of Goodness of Fit Indexes to Lack of Measurement Invariance.” Structural Equation Modeling 14:464–504. DOI https://doi.org/10.1080/10705510701301834 。出版社摘要已审，全文未审。
5. Verdam, M. G. E., Oort, F. J. & Sprangers, M. A. G. (2016, online 2015). “Using structural equation modeling to detect response shifts and true change in discrete variables.” Quality of Life Research 25:1361–1383. DOI https://doi.org/10.1007/s11136-015-1195-0 。开放全文 https://link.springer.com/article/10.1007/s11136-015-1195-0 ，已直接阅读模型方程、序数阈值假设、两阶段分析和结果。原研究例子为485名患者，本项目未接触其个体记录。
6. Vanier, A., Oort, F. J. et al. (2021). “Response shift in patient-reported outcomes: definition, theory, and a revised model.” Quality of Life Research 30:3309–3322. DOI https://doi.org/10.1007/s11136-021-02846-w 。开放全文 https://link.springer.com/article/10.1007/s11136-021-02846-w ，已审概念争议、两时点模型、测量与构念分离、旧定义修订；出版社提示2021年5月勘误，未来引用图表需核对。
7. Sébille, V. et al. (2021). “Critical examination of current response shift methods and proposal for advancing new methods.” Quality of Life Research 30:3325–3342. DOI https://doi.org/10.1007/s11136-020-02755-4 。开放全文 https://link.springer.com/article/10.1007/s11136-020-02755-4 ，已审11种方法的综述与竞争解释。
8. Kahneman, D. & Thaler, R. H. (2006). “Anomalies: Utility Maximization and Experienced Utility.” Journal of Economic Perspectives 20:221–234. DOI https://doi.org/10.1257/089533006776526076 。RePEc 原刊摘要 https://econpapers.repec.org/article/aeajecper/v_3a20_3ay_3a2006_3ai_3a1_3ap_3a221-234.htm 已审；全文未审。

所有检索日期：2026-10-25。非中文网站。未获免费全文者仅按摘要处理。

## 二、命题与竞争观点

Vandenberg 与 Lance 主张跨时间比较先检验测量等值性。Chen 2007 模拟指出 CFI、RMSEA、SRMR 对不同非等值形式的敏感性随模式、比例、样本结构变化，单一拟合阈值不足以证明等值。

Sprangers 与 Schwartz 1999 把 internal standards、values、conceptualization 的变化纳入反应转移。Oort 2005 提出 SEM 识别路径。Verdam 等 2016 对序数题项先建潜在连续反应及阈值模型，再考察截距、载荷、残差的跨期变化，说明分数变化可能混入测量关系变化。

Vanier 等 2021 明确区分目标构念 target construct 与测量 measure，并将 response shift 形式化为观测变化无法完全由目标变化解释的情形。该修订把传统三种变化视作可能的机制而非定义本身，与1999年概念口径存在分歧。Sébille 等 2021 比较11种方法，指出每种方法都有替代解释和假设，尚无统一最优检测方法。

## 三、不可识别性：可核算的理论反例

用两时点的单因子表达：Y_it = tau_t + lambda_t * eta_it + epsilon_it。
Y 是可观测自评分数，eta 是潜在状态，tau 是截距，lambda 是载荷。假设 lambda 两期均为1，观测均值从5变6。方案甲：潜在状态增加1，截距不变。方案乙：潜在状态不变，截距增加1。两者给出相同观测均值，说明没有额外约束时无法由均值变化唯一识别真实变化。

序数评分还涉及阈值不变性。锚定题项、外部行为指标、质性认知访谈及更多时点可缩小解释空间，但锚定假设也须验证。缺失非随机、失访、语言改变、天花板效应、时变混杂与情境效应可能产生类似信号。测量非等值不自动证明价值观变化；等值检验未拒绝也不能证明真实等值。

## 四、六个候选人生维度与价值边界

身体与现实条件：自评活动限制、精力与可用时间，风险为日内波动与主观参照。
财务资源：可支配缓冲与风险承受，风险为口径、隐私和安全感与资产额不等价。
精神体验：即时感受、意义和满意度，风险为回忆偏差及概念变化。
社会关系：支持质量、互动与冲突，风险为关系隐私和数量与质量不等价。
能力成长：可证明任务表现和自评能力，风险为目标改变和自信混杂。
环境与自由度：可行选项、约束和实际自主，风险为机会数量与真实可行性不同。

以上是未来候选测量，未读取用户真实资料。价值权重 w_{k,t} 可随经验变化，假设 U_t(a)=sum_k w_{k,t} f_{k,t}(a) 时，跨期权重和刻度的变化会使单一总分失去稳定意义。Kahneman 与 Thaler 2006 的原刊摘要讨论预测未来体验的系统误差，不能据此由研究者替个人指定正确人生权重。部分多目标排序只能形成偏序，未必存在唯一最优行动，更不存在普适唯一最优人生。

## 五、候选方法、适用条件与验证清单

方法A：纵向 CFA 或 IRT，先审结构、载荷、截距、阈值等值及模型敏感性。要求多时点、足够题项、合理锚定与样本，输出不可识别区域。
方法B：认知访谈、锚定情境和重复自评。用于检查题义和内部标准变化；须警惕访谈诱导、回忆偏差及社会期望。
方法C：仅规划未来低风险 N-of-1 或微随机研究的伦理和统计条件，包括可逆干预、预设观察窗、滞后与携带效应、序贯混杂、缺失机制；本轮无干预或产品实现。
方法D：动态权重区间、Pareto 支配与不可比较方案的敏感性分析。所有权重取舍需由未来使用者自主决定并可修改。

未来验收：明确构念及评价主体；登记题项版本和时间窗口；至少两个方法核对效度；预设失访与非等值敏感性；分离预测、因果与规范价值判断；公开拒绝唯一排序的条件；未另行授权不读取个人资料。

四层联系：个体层为自评与动态偏好；群体层为社会比较与参照；制度层为量表激励与选择约束；历史层为指标意义的跨期跨文化变化。跨层映射待检验。

今日状态：C002 COMPLETE，METHOD_NOTE_BOUNDED，EMPIRICAL_TEST=NOT_RUN。
下一 C 专题：MNAR 缺失非随机、选择偏差及纵向敏感性界限，优先 Rubin 1976、Little 1993、Manski 1990。
