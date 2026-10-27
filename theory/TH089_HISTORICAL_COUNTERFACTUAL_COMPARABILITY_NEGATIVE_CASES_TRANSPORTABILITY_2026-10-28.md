# TH089 历史反事实的可比性、负面案例与机制外推边界

日期及非中文原始文献检索日期：2026-10-28（Asia/Singapore）。状态：THEORY_NOTE_BOUNDED。承接TH088过程追踪。仅理论阅读、人工数学及逻辑审计。未开展真实历史因果估计、R系列拟合、前瞻预测或模型熔炼。

## 1. 原始书目与直接访问范围

A1. King, Gary & Langche Zeng (2006), “The Dangers of Extreme Counterfactuals,” *Political Analysis* 14(2):131–159, DOI https://doi.org/10.1093/pan/mpj004 。作者公开原刊 https://gking.harvard.edu/files/counterft.pdf 。直接审读原刊pp.131–136、138–140、152–154相关段落，包括模型依赖、凸包、共同支持与局限。论文证明的条件与实际因果识别应分别检查。

A2. Pearl, Judea & Elias Bareinboim (2011), “Transportability of Causal and Statistical Relations: A Formal Approach,” *AAAI Proceedings* 25(1):247–254, DOI https://doi.org/10.1609/aaai.v25i1.7861 。会议正式开放PDF https://ojs.aaai.org/index.php/AAAI/article/view/7861/7720 。直接审读pp.247–250，涵盖例1至3、selection diagrams、定义1、定理1至3及标准化公式；未独立复证形式证明。

A3. Fearon, James D. (1991), “Counterfactuals and Hypothesis Testing in Political Science,” *World Politics* 43(2):169–195, DOI https://doi.org/10.2307/2010470 。作者斯坦福原文索引 https://web.stanford.edu/group/fearon-research/cgi-bin/wordpress/wp-content/uploads/2013/10/Counterfactuals-and-Hypothesis-Testing-in-Political-Science.pdf 。检索可见原刊pp.170–171片段，直接打开PDF时重定向失败。出版社原始摘要 https://www.cambridge.org/core/journals/world-politics/article/abs/counterfactuals-and-hypothesis-testing-in-political-science/1DE902D41097CEF599E73F84A47BBE4F 。仅据可见原文片段与原始摘要，不声称全文审读。

B1. Mahoney, James & Gary Goertz (2004), “The Possibility Principle: Choosing Negative Cases in Comparative Research,” *American Political Science Review* 98(4):653–669, DOI https://doi.org/10.1017/S0003055404041401 。出版社正式摘要 https://www.cambridge.org/core/journals/american-political-science-review/article/abs/possibility-principle-choosing-negative-cases-in-comparative-research/49BA71629FB9FA8E7FC0D00203C37E0B 。正文受限，尚未核对操作细节。

B2. Seawright, Jason & John Gerring (2008), “Case Selection Techniques in Case Study Research,” *Political Research Quarterly* 61(2):294–308, DOI https://doi.org/10.1177/1065912907313077 。出版社摘要 https://journals.sagepub.com/doi/10.1177/1065912907313077 。核验七种案例选择策略，正文未逐页审读。

B3. Pearl, Judea & Elias Bareinboim (2014), “External Validity: From Do-Calculus to Transportability Across Populations,” *Statistical Science* 29(4):579–595, DOI https://doi.org/10.1214/14-STS486 。作者机构原始书目及摘要 https://cris.technion.ac.il/en/publications/external-validity-from-do-calculus-to-transportability-across-pop/ 。仅摘要与书目，未当作独立实证验证。

## 2. 十六项条件性理论命题

P01【A3片段】历史因果陈述常隐含“原因C缺席时结果E如何”的反事实。需事前界定原因、时间窗与干预含义。

P02【A3片段】实际案例比较与反事实思考均依赖可比性判断。小样本难以找到完整现实对照，假想对照的机制约束须公开。

P03【A1原作】反事实远离观测数据时模型依赖风险上升。样本内拟合良好不足以保证远端预测有效。

P04【A1原作】凸包外是外推警报；凸包内可能缺少局部密度或因果可交换性。几何判定本身不识别因果效应。

P05【A1原作】凸包成员资格可转化为非负且权重和为1的线性规划可行性问题，结果依赖协变量选择与测量质量。

P06【A1原作】共同支持缺失时，缩小研究总体可能降低外推风险，同时改变目标估计对象；应同时报告覆盖比例。

P07【B1摘要】选择负面案例需要确认结果在该案例中有发生机会。机会规则应在观察结局前冻结，避免事后筛选。

P08【B2摘要】典型、异质、极端、偏离、影响、最相似与最不同案例有不同用途；选择规则应服务明确的检验问题。

P09【A2原作】跨人口和制度环境迁移因果效果需要识别源目标之间的机制差异。观察分布相似不能证明干预效应相同。

P10【A2原作】若事前协变量Z上的条件干预效应跨环境不变，且目标Z分布已知，可用目标权重标准化源环境条件效应；须核验共同支持。

P11【A2原作】将代理指标误当效果修饰因素，或将处理后变量当事前变量，可能产生错误的迁移公式。

P12【A2原作】selection diagrams把结构变化作为明确假设。缺乏结构证据时迁移状态应为UNKNOWN。

P13【本项目竞争解释】案例相似可由共同冲击、模仿、选择性存档造成；相似结果无法单独证明同一机制。

P14【本项目竞争解释】历史事件缺席可由预防、抑制、未暴露、未记录或观察窗口过短造成；需分开审计。

P15【本项目待检验】跨时代变化可能同时影响个体激励、群体传播、制度执行与历史记录存续。四层各自列出可变机制。

P16【本项目待检验】反事实适合提出可检验研究问题。未识别的反事实须保留条件性结论、竞争解释和不确定区间。

## 3. 八项人工数学与逻辑审计

E01 设观测x只有0、1，f1(x)=x，f2(x)=x+0.01x(x-1)。两函数在观测点一致，x=0.5相差0.0025，x=10相差0.9，x=100相差99。远端预测无法由两个观测点唯一确定。

E02 观测协变量点为(0,0)、(0,2)、(2,0)、(2,2)；(1,1)位于凸包内，附近却无观测点。凸包内不等于局部数据充足。

E03 设Z=0时只有处理样本，Z=1时只有对照样本。无论每组增加多少相同分配方式的样本，条件于Z的处理对照差都缺乏正概率支持。

E04 人工100个案例有10个阳性、90个阴性；阴性中只有10个满足事前机会标准。全部阳性比例10%，机会集合阳性比例50%。分母不同，推断对象不同。

E05 高风险群体基线事件率80%，低风险20%，干预真实效应为0；干预仅给高风险群体时，观察组差60个百分点，不能作为因果效应。

E06 源环境两个事前亚组效果为0.1、0.5，源权重(0.8,0.2)，总体效果0.18。目标权重(0.2,0.8)，在条件效应不变假设下目标效果0.42。直接照搬源总体值偏差0.24。

E07 沿用E06目标权重，若目标亚组效果改为0.1、0.2，则目标总体效果0.18。源数据与目标组成相同仍允许不同目标效果，表明机制不变性是实质假设。

E08 若规则R影响联盟A再影响政策Y，删除R且固定A是受控直接效应情景；删除R并允许A响应是总效应情景。两种反事实必须分别登记。

全部是人工构造，无真实历史数据、原作者模型复算或独立因果识别。

## 4. 竞争观点、四层联系及验证清单

历史反事实的积极方法观点：明确反事实有助于暴露隐藏的因果假设，设计可比较的实际案例【A3】。限制性观点：远端反事实受模型形式支配【A1】，跨环境因果迁移需结构性许可【A2】。负例机会原则【B1】与多种案例选择策略【B2】适用不同研究目标。双方证据层级已标注，不能把规范建议伪装成历史因果发现。

个体层：决策、意图与反事实记忆。群体层：联盟、模仿、共同冲击。制度层：规则、执行能力、预防机制。历史层：时期、冲击、档案保存及人口技术结构。各层应列可观测的竞争性机制证据。

候选机制H1制度驱动，H2共同外部冲击，H3行动者联盟先行，H4联合机制，H5选择性保存。未证互斥，不赋予虚构的后验概率。

验证清单：冻结事件与时间窗；定义干预及联动变量；事前划定机会集合；选择阳性、合格阴性与偏离案例；审计可交换性、共同支持、凸包距离及协变量测量；标注源目标结构不变、变化、未知；保留竞争机制、来源依赖和存档缺失；报告敏感性区间；要求独立证据复验。

## 5. 归档边界与下一主题

本轮直接审读两份公开正式原作指定章节，另核验一份作者原文可见片段及原出版社摘要、三份原始摘要或机构书目。16项条件命题，8项人工审计。真实历史数据复算0，独立因果估计0，前瞻预测0，模型熔炼0。C005（2026-10-28）与D002（2026-W44）已归档，本轮只读。未接入个人敏感资料、未开发产品、未新增费用、未主动运行CI。

下一主题TH090：历史比较中的机制异质性、测量等值与负例选择敏感性。
