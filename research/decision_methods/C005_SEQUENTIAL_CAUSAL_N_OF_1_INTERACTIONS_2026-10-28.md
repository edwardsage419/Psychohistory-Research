# C005 单人序贯因果识别、携带效应与多维效用交互

研究及英文来源检索日期：2026-10-28（Asia/Singapore）。状态：METHOD_NOTE_BOUNDED。2026-10-28首项C增量。继承C002测量等值、C003非随机缺失、C004动态效用。只储备方法，不读取个人敏感资料、不实施实验、不开发个人决策产品。

## 原始书目及访问等级

[A] Boruvka, Audrey, Daniel Almirall, Katie Witkiewitz & Susan A. Murphy (2018，在线2017). “Assessing Time-Varying Causal Effect Moderation in Mobile Health.” *JASA* 113(523):1112–1121. DOI https://doi.org/10.1080/01621459.2017.1305274 。开放原作 https://pmc.ncbi.nlm.nih.gov/articles/PMC6241330/ ，预印本 https://arxiv.org/abs/1601.00237 。直接审读公开全文第1至8节的潜在结果、近端与滞后效应、加权中心化、可用性、模拟和BASICS-Mobile例子。作者明确该n=28、T=28示范案例并非序贯随机试验，观察因果解释依赖顺序可忽略性。
[B] Klasnja, Predrag et al. (2015). “Microrandomized Trials: An Experimental Design for Developing Just-in-Time Adaptive Interventions.” *Health Psychology* 34(Suppl):1220–1228. DOI https://doi.org/10.1037/hea0000305 。作者机构原始摘要 https://asu.elsevierpure.com/en/publications/microrandomized-trials-an-experimental-design-for-developing-just/ 已核，全文未审。
[B] Walton, Ashley et al. (2018). “Optimizing Digital Integrated Care via Micro-Randomized Trials.” *Clinical Pharmacology & Therapeutics* 104(1):53–58. DOI https://doi.org/10.1002/cpt.1079 。作者公开稿 https://pmc.ncbi.nlm.nih.gov/articles/PMC5995647/ 摘要及N-of-1对比段落核验，未逐节通读。
[B] Luers, Brook, Predrag Klasnja & Susan Murphy (2019). “Standardized Effect Sizes for Preventive Mobile Health Interventions in Micro-Randomized Trials.” *Prevention Science* 20:100–109. DOI https://doi.org/10.1007/s11121-017-0862-5 。作者稿 https://pmc.ncbi.nlm.nih.gov/articles/PMC6037616/ 摘要核验，全文未审。

上述原作主要针对移动健康，迁移至人生决策需要独立的伦理、测量和外推审计。

## 十项候选方法命题与适用条件

C01 六个候选人生维度分别为身体与现实条件、财务资源、精神体验、社会关系、能力成长、环境与自由度。每维预先定义可观测代理量、观察窗口、效度、信度、缺失、误差和隐私风险。时间可用量、流动性缓冲、体验评分、支持质量、任务能力、可行选择集都不能直接等同福祉。
C02【原作】设决策时点t、处理A_t、历史H_t、可用性I_t、近端Y_{t+1}及滞后Y_{t+k}。因果效应需指定未来处理机制与结果窗口。
C03【原作】Boruvka等的中心化加权估计利用已知或可估计的处理概率；普通GEE在时变处理与修饰因素存在时未必一致。需正概率、模型条件和估计不确定性审计。
C04【原作】可用性受既往处理影响时，可用时段的近端效应不自动等于所有时段或长期政策效应。
C05【方法对比】N-of-1适合单人可逆处理与重复周期；微随机设计适合多决策点短期可重复处理。重大不可逆人生选择不适合随意随机化。
C06 处理可影响后续资源、压力、可用性和量表回答。调整既往处理的后果时需明确总效应或条件近端效应，避免中介与碰撞偏差。
C07 单人序列可能存在自相关、季节趋势、携带效应、失访、未盲化与测量反应性。单人高频记录不等于独立样本量很大。
C08 规范权重w_t与客观后果差异须分开。观察到的选择不能唯一反推出个人的正确价值权重，也不存在普适唯一最优人生。
C09 跨维效用交互U_t=Σw_jt x_jt+Σγ_jk,t x_jt x_kt只是候选模型；刻度、可补偿性、硬约束和交互权重需主观说明并做敏感性分析。
C10 近端效应不自动累积为长期人生收益；制度环境、行为适应、偏好变化及外部冲击可能改变长期路径。

## 七项人工反例与算术

E01 A=(0,1,0,1)、Y=(1,3,1,3)时，按处理分组差2。世界甲Y=1+2A；世界乙处理无效、时间趋势恰好为(1,3,1,3)。观察完全相同，非随机时因果效应不可识别。
E02 假设Y_t=2A_t+A_{t-1}，A_0=0，A=(1,0,1,0)，则Y=(2,1,2,1)。按当期处理分组差1，结构方程当期处理系数为2；交替设计混入携带效应。
E03 若60%决策点可用，可用时效应恒为2，且可用性与处理无反馈，所有时点平均即时增量为1.2；反馈存在时该乘积可能失效。
E04 处理概率0.05时，处理组逆概率权重20；概率0.5时权重2。低概率处理可能使估计方差膨胀。
E05 A=(1,0)、B=(0.6,0.6)，U=x1+x2+γx1x2。γ=0时A=1、B=1.2；γ=-1时A=1、B=0.84。排序随主观交互取舍反转。
E06 观察评分从5到6，模型Y_t=η_t+τ_t。潜在状态η增加1与截距τ增加1均相容；须继承C002测量等值审计。
E07 两制度首日近端效应均为1；世界甲后续无携带效应，世界乙后续累积疲劳。单凭首日观察无法确定长期效用排序。

全部为人工数学或结构反例，无个人数据、N-of-1或MRT实施、真实因果估计。

## 验证清单、四层连接与下一步

冻结构念、时间窗、处理可逆性、随机化机制、近端与滞后目标；检查伦理、正概率、时间混杂、季节趋势、携带效应、测量等值和失访；对状态测量误差及价值权重同时做区间敏感性；报告Pareto非支配集与不可比较选项；不允许对不可逆重大选择进行未经伦理批准的实验。

个体层涉及行为、认知和体验；群体层涉及社会比较与干扰；制度层涉及机会约束与处理可行性；历史层涉及长期环境冲击和指标意义变化。四层连接仍为待验证假说。

下一研究日C006：单人时间序列中的干扰、季节趋势与负对照方法。
