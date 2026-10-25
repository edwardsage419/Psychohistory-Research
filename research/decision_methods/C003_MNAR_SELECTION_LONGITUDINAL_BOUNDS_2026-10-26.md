# C003 MNAR 缺失、选择偏差与纵向敏感性界限

研究与检索日期：2026-10-26（Asia/Shanghai）。研究日 2026-10-26 的首项实质增量。状态：METHOD_NOTE_BOUNDED。只研究未来候选方法，不接入任何真实个人健康、财务、关系或其他敏感数据，不开发决策产品。

## 一、原始来源及阅读等级

1. [B] Rubin, Donald B. (1976). “Inference and Missing Data.” *Biometrika* 63(3):581–592. DOI https://doi.org/10.1093/biomet/63.3.581 。出版社原刊摘要 https://academic.oup.com/biomet/article-abstract/63/3/581/270932 和 ETS 作者机构书目 https://www.ets.org/research/policy_research_reports/publications/article/1976/itce.html 已核；全文未审。相关 1975 年作者前版 https://doi.org/10.1002/j.2333-8504.1975.tb01053.x 只核验摘要，版本不可混称。
2. [B] Little, Roderick J. A. (1993). “Pattern-Mixture Models for Multivariate Incomplete Data.” *Journal of the American Statistical Association* 88(421):125–134. DOI https://doi.org/10.1080/01621459.1993.10594302 。出版社原刊摘要 https://www.tandfonline.com/doi/full/10.1080/01621459.1993.10594302 已核，全文访问受限。作者开放机构存档 https://escholarship.org/uc/item/9jb3w254 元数据已检索，访问受限，本轮不冒充全文审读。
3. [B] Manski, Charles F. (1990). “Nonparametric Bounds on Treatment Effects.” *American Economic Review* 80(2):319–323. 原刊书目 https://ideas.repec.org/a/aea/aecrev/v80y1990i2p319-23.html 。开放扫描检索结果存在，但直接访问受阻，正文未审；以下界限由本项目直接从概率公理推导。
4. [A] National Research Council (2010). *The Prevention and Treatment of Missing Data in Clinical Trials*. National Academies Press. DOI https://doi.org/10.17226/12955 。直接审读第4章“Drawing Inferences from Incomplete Data” https://www.nationalacademies.org/read/12955/chapter/6 和第5章“Principles and Methods of Sensitivity Analyses” https://www.nationalacademies.org/read/12955/chapter/7 的开放原文。该报告讨论临床试验，跨到人生状态追踪时需重新论证外部效度。
5. [B] Lee, David S. (2009). “Training, Wages, and Sample Selection: Estimating Sharp Bounds on Treatment Effects.” *Review of Economic Studies* 76(3):1071–1102. DOI https://doi.org/10.1111/j.1467-937X.2009.00536.x 。作者开放工作论文 2005 NBER 11721 https://www.nber.org/papers/w11721 ，本轮核验原始摘要，未读全文；trimming bounds 依赖额外选择单调性等条件，不能直接套用。

所有检索使用非中文网站，检索日期同上。A 表示开放原作/权威报告指定章节已直接阅读；B 表示原刊摘要与书目。

## 二、方法命题、竞争解释及适用边界

M1：缺失机制与目标变量有关时，完整案例的均值可能偏离目标总体。Rubin 1976 的可忽略条件包括 MAR 及参数可分离等限定，不能仅凭观测数据认定 MAR。竞争解释：完全随机缺失、由已测协变量解释的 MAR、测量错误和构念变更。

M2：纵向失访可能依赖未观察到的后续状态。过去评分、退出理由、时间压力与研究参与意愿可能共同影响观察概率。适用条件：预先固定目标总体和测量时点，明确失访、拒答、跳题、结构性不适用的差异。

M3：selection model 用结果解释观察概率，pattern mixture model 用缺失模式划分结果分布。Little 1993 提供后者的理论家族；National Research Council 2010 第5章解释两类模型如何通过无法从观测数据验证的假设识别缺失分布。不能仅凭模型拟合优度选出“真实”MNAR机制。

M4：先报告部分识别界限，再按明示的主观敏感性参数给出条件性结论。Manski 1990 是非参数界限的重要原始研究线索，本轮界限计算为独立代数。界限宽不代表方法失败，可能忠实反映信息不足。

M5：Lee 2009 的修剪界限针对处理影响结果可观察性的问题，需要随机分配或相应识别条件以及选择单调性等假设。未来 N-of-1 和微随机设计也可能有干预后失访，不能把随机化当作消除缺失偏差的保证。

## 三、可核算的纵向二元指标反例

仅使用人工计数。100个假想观测单位在基线有60个正例，基线比例0.60。下一期仅70个有结果，其中49个为正例，已观察比例49/70=0.70；另外30个缺失。

记缺失者正例率 q，完整目标总体下一期比例 μ=(49+30q)/100=0.49+0.30q。只知道 0≤q≤1，得到 μ∈[0.49,0.79]，相对基线的变化 Δ∈[-0.11,0.19]。变化方向无法由现有数据确定。

若额外假设缺失者与观察者下一期比例相同，q=0.70，则 μ=0.70，Δ=+0.10。若假设 q=0.20，则 μ=0.55，Δ=-0.05。若假设 q=0.90，则 μ=0.76，Δ=+0.16。三个世界对已观测记录完全一致。q 是不可由这些数据识别的敏感性参数。这个人工例子没有真实参与者，也没有声称 MAR 在真实数据中成立。

对多时点连续指标，候选方法可用 pattern mixture 的偏移参数 δ_t 描述缺失者条件均值相对可观测同类个体的差异，按事先给定的可解释区间做 tipping-point 分析。必须同时审计分数尺度的等值性、缺失时点、变量支持集与非线性，不能把 δ_t 当作已估计的真实偏差。

## 四、人生状态候选测量与规范价值限制

身体及现实条件：活动时间、可达服务、精力记录，警惕状态较差时不回答造成乐观偏差。
财务资源：缓冲能力的非敏感代理指标，警惕资源压力与失访相关；本轮不获取实际账户数据。
精神体验：即时情绪、意义感与满意度，警惕极端体验时拒答或记忆偏差。
社会关系：可获得支持与互动质量，警惕关系冲突导致拒答以及他人隐私。
能力成长：可验证任务结果，警惕失败任务选择性不记录。
环境与自由度：可行选项与限制，警惕不可达场景根本没有被抽样。

这些维度及任何效用权重都涉及价值判断，指标高低无法自动推出生活更好。动态偏好、跨期反应转移和不同维度的不可比较性须独立审计。不存在由此推导的普适唯一最优人生。

## 五、候选验证清单、四层映射和下一题

1. 先固定估计对象、观察时间、题项版本、失访定义与数据权限；本轮无实际采集。
2. 报告各时间点各维度的缺失比例、模式、原因和已观察协变量差异，严禁只保留完整案例而不报告损失。
3. 主分析声明 MCAR/MAR/MNAR 及识别假设，辅以分布支持约束、极端界限、δ 敏感性区间和结论翻转点。
4. 检验权重、动态偏好、量表等值、干预后失访、时变混杂和不合理外推的交互影响。
5. 只在伦理许可且有单独授权后讨论低风险 N-of-1 或微随机验证设计；本轮无干预。
6. 个体层审计自评和失访；群体层审计社会比较与选择进入；制度层审计问卷激励和隐私规则；历史层审计跨时代样本留存与指标语义漂移。

今日 C003 状态：COMPLETE，METHOD_NOTE_BOUNDED，EMPIRICAL_TEST=NOT_RUN。下一 C 专题：动态效用权重、多目标偏序和鲁棒决策的识别条件。C 与 R 系列及商业产品分析独立归档。
