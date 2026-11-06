# C013 纵向交叉滞后模型的个体内识别边界：Hamaker等2015原著审计

日期：2026-11-07（Asia/Singapore）
track: theory / C
target_key: (theory-C,Hamaker-Kuiper-Grasman-2015,10.1037/a0038889,CLPM-vs-RI-CLPM-within-person-identification)
observed_main_head_before_write: a85f59078c07e5a9eba17bf6c12ae36ea7f82b0f
status: PRIMARY_SPECIFIED_PAGES_READ; METHOD_NOTE_BOUNDED; NO_PERSONAL_DATA; NO_PRODUCT

## 原著与阅读范围

Ellen L. Hamaker, Rebecca M. Kuiper, Raoul P. P. Grasman (2015), “A Critique of the Cross-Lagged Panel Model,” Psychological Methods 20(1):102–116, DOI https://doi.org/10.1037/a0038889 。直接读取乌得勒支大学机构开放的最终发表版 https://dspace.library.uu.nl/bitstream/handle/1874/428739/168970_Hamaker_Kuiper_Grasman_2015_A_Critique_of_Cross_Lagged_Panel_Model.pdf?sequence=1 。实际核读p102–105的两模型方程(1a–d)、(3a–d)、(4)，p106相关模型说明，p110–113的实证结果与Discussion。Appendix B式(5)的完整符号代数未逐项核算；全文其他段落及底层原始数据未完整审计。只存原创摘要与研究笔记，不转存受版权保护的PDF。

## 原著的模型机制与可观察量

传统CLPM：x_it=mu_t+p_it，y_it=pi_t+q_it；p_it=alpha_t p_i,t-1+beta_t q_i,t-1+u_it，q_it=delta_t q_i,t-1+gamma_t p_i,t-1+v_it。其滞后参数基于相对于群体当期均值的偏差，稳定的个体间差异可能污染估计。

RI-CLPM：x_it=mu_t+kappa_i+p*_it，y_it=pi_t+omega_i+q*_it；滞后方程作用于相对于个体期望值的p*、q*。随机截距kappa_i、omega_i刻画研究期内稳定差异，相关个体内滞后系数刻画条件预测。作者给出的基本模型至少需要三波数据；两波传统CLPM可恰好识别，拟合完美无法检验模型结构。RI-CLPM模型假定特质部分时间不变，观测值没有单独建模的测量误差，等间隔及参数约束需要核查。

作者的原始经验例子比较父母响应性与青少年抑郁症状。传统CLPM报告负向滞后关联，而RI-CLPM未发现对应显著滞后关联。作者报告稳定特质相关约-0.443（SE .067），其解释为群体间关联，不能直接据此推出干预因果作用。原作者实证数据与软件拟合本轮未复算。

## 新的C轨方法限制与竞争解释

同一对观测变量可以同时存在稳定个体差异相关与短期个体内滞后效应。把个体间横截面关联当作个体内改变效应，可能导致方向、符号或显著性错误。RI-CLPM是与传统CLPM竞争的模型假设；它也未自动解决时间变化混杂、反向因果、测量误差、干预识别、非平稳动态及不等间隔观察问题。作者明确讨论STARTS测量误差模型、ALT趋势模型及连续时间替代方案，不应强制合并为唯一模型。

候选观测量：至少三次有时间戳的两变量重复测量、量表版本、测量间隔、重复测量误差代理、研究期稳定背景指标。不可直接观测：真实稳定特质、时间变化未测混杂、个体内潜在状态。拟议可证伪检验：预先构造已知稳定截距相关而个体内跨滞后为零的合成数据，比较传统CLPM与RI-CLPM估计的伪跨滞后；再引入测量误差、非等间隔与时间变化混杂，检验RI-CLPM是否也偏离生成真值。该实验尚未执行，不能称为真人预测或因果验证。

## 去重、边界与执行

现有C003一般缺失识别、C007测量反应性、C011回顾报告、C012事件捕获均聚焦不同问题。理论索引未找到Hamaker或RI-CLPM原著记录；本条聚焦群体间稳定差异污染个体内滞后参数。R轨若已涉及相关模型仍以R的冻结基线为准，本轨不进行R模型拟合、评分或复核。

本周D003实际完成日期2026-11-02，继续有效。R073、PESEN v0.1及R E1/E2/E3、MARKET分级不变。原著指定页阅读COMPLETE；原著数据复算NOT_RUN；合成模拟NOT_RUN；真人实验NOT_RUN；历史预测NOT_RUN；CI NOT_RUN；新增收费服务0，账户实际计费状态NOT_VERIFIED。后续优先完成合成反例与测量误差条件的审计，再转向弱覆盖的文化人类学与历史制度原著。
