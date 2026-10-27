# TH090 历史比较中的机制异质性、测量等值与负例选择敏感性

研究日期及非中文来源检索日期：2026-10-28（Asia/Singapore）。状态：THEORY_NOTE_BOUNDED。承接TH089。仅理论阅读、人工数学反例及已发表数字核对；不涉及R系列拟合、个人敏感资料、真实因果估计、产品开发或付费服务。

## 一、原始书目及阅读等级

[A1，直接审读正式开放全文] Cieciuch, J., Davidov, E., Schmidt, P., Algesheimer, R. & Schwartz, S. H. (2014). “Comparing results of an exact vs. an approximate (Bayesian) measurement invariance test.” *Frontiers in Psychology* 5:982. DOI https://doi.org/10.3389/fpsyg.2014.00982 。原刊 https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2014.00982/full 。审读measurement invariance、Methods、Analysis、Results、Summary and conclusions，表3、表5及局限。八国便利学生样本，精确标量等值10/19项，贝叶斯近似在作者拟合标准下可接受19/19项；三项需改变先验方差。

[A2，直接审读正式开放全文] Athey, S. & Imbens, G. W. (2016). “Recursive Partitioning for Heterogeneous Causal Effects.” *PNAS* 113(27):7353–7360. DOI https://doi.org/10.1073/pnas.1510489113 。原刊 https://www.pnas.org/doi/10.1073/pnas.1510489113 ，作者稿 https://arxiv.org/abs/1504.01132 。审读问题设定、honest sample splitting、因果树、模拟表1及结论。其覆盖率结果来自作者模拟，未由本项目复算。

[A3，直接审读作者开放原刊PDF] Imai, K., King, G. & Stuart, E. A. (2008). “Misunderstandings among Experimentalists and Observationalists about Causal Inference.” *JRSS A* 171(2):481–502. DOI https://doi.org/10.1111/j.1467-985X.2007.00527.x 。作者全文 https://imai.fas.harvard.edu/research/files/matchse.pdf 。审读第2至5节的SATE/PATE、样本选择与处理不平衡分解、随机抽样及匹配设计。作者的四项分解采用加性假设，未包含全部现实误差。

[B1，原刊摘要与书目] Mahoney, J. & Goertz, G. (2004). “The Possibility Principle: Choosing Negative Cases in Comparative Research.” *APSR* 98(4):653–669. DOI https://doi.org/10.1017/S0003055404041401 。出版社 https://www.cambridge.org/core/journals/american-political-science-review/article/abs/possibility-principle-choosing-negative-cases-in-comparative-research/49BA71629FB9FA8E7FC0D00203C37E0B 。正文未读，具体操作规则待核。

[B2，原刊摘要与书目] Meredith, W. (1993). “Measurement Invariance, Factor Analysis and Factorial Invariance.” *Psychometrika* 58(4):525–543. DOI https://doi.org/10.1007/BF02294825 。出版社 https://www.cambridge.org/core/journals/psychometrika/article/abs/measurement-invariance-factor-analysis-and-factorial-invariance/914A4C29515ACA7E0554B9E79F20D36C 。付费正文未访问。

[B3，原刊摘要与书目] Vandenberg, R. J. & Lance, C. E. (2000). “A Review and Synthesis of the Measurement Invariance Literature.” *Organizational Research Methods* 3(1):4–70. DOI https://doi.org/10.1177/109442810031002 。出版社 https://journals.sagepub.com/doi/10.1177/109442810031002 。正文未逐页审读。

## 二、十六项条件性理论命题及竞争解释

T01【A1/B2】同名历史指标的语义、采集方式、受访群体与制度定义可能跨期改变；必须核对测量锚点。反例是经独立校准的稳定物理单位，仍需查仪器与覆盖率。
T02【A1】构型等值支持结构比较，载荷等值支持关系比较，截距等值与潜在均值比较有关；均依赖因子模型识别与合适的锚定条件。
T03【A1】精确等值要求指定参数相等，近似贝叶斯等值允许小幅差异并依赖先验。更宽松的模型拟合通过不能自动证明跨期均值无偏。
T04【A1】八国19项价值量表的近似等值发现来自学生便利样本、不同调查模式及有序量表近似连续的处理；不能直接移植至历史总体。
T05【A2】平均处理效果可能掩盖不同群体中相反方向的效应；必须冻结处理、结果、时间窗口、目标总体及预处理修饰因素。
T06【A2】同一数据同时发现最优分组并估计组内效应可能导致选择后偏差；honest分割降低这种偏差，代价是估计样本变小。
T07【A2】因果树的因果解释要求随机化或条件可忽略性、正概率、无干扰及正确结果定义；历史制度改革常不满足。
T08【A3】样本选择误差与处理分配不平衡需分别审计。可见档案的覆盖不等于历史总体的覆盖。
T09【A3】SATE与PATE属于不同目标；匹配、删样本、档案毁损可能改变估计对象。原作加性分解无法包揽测量误差及处理后选择。
T10【B1摘要】负面案例应具有事件发生的机会；机会集合由研究理论确定，可能产生循环定义，必须公开排除理由和边界敏感性。
T11【项目推断】将从未暴露于某冲击的单位算作未发生事件的负例，会改变发生率分母。若研究目标是全体单位描述，广口径可能仍有用途。
T12【项目推断】机制异质性可来自制度、人口组成、资源、网络、冲击强度或记录方式；应分别设计可反驳的史料预测。
T13【A1/A3综合】测量等值检验无法修复选择性保存；样本加权也无法单独修复历史指标含义漂移。
T14【A2/B1综合】事后按结局筛选负例和寻找异质性分组均可能夸大机制差异；预先冻结规则或保留独立验证集。
T15【项目推断】同一历史现象至少保留机制变化、群体替代、共同冲击、资料选择与测量漂移五类竞争解释，检验各自预测。
T16【项目推断】通过等值、机会集合与分组检验仍可能存在不可观测混杂、干扰、外推失败及规范性价值分歧。未满足识别条件应报告未知。

## 三、八项人工数学与识别审计

E01【测量截距漂移】观测均值E[Y]=α+λμ。时期1 (α,λ,μ)=(0,1,1) 得均值1；时期2 (1,1,1) 得均值2。潜在均值未变，观测均值上升1。设潜在方差和测量误差分布稳定，则观测方差也可相同。
E02【观测等价】时期2另一世界 (α,λ,μ)=(0,1,2) 也产生均值2。若潜在方差相同，E01和E02的观测均值及方差完全相同；无锚定条件时无法识别变化源。
E03【异质性与人口构成】A群体效应+0.4、B群体−0.2。源环境A占25%，总体效应−0.05；目标环境A占75%，总体效应+0.25。群体内效应不变，组成变化足以翻转符号。
E04【负例机会集合】人工设10个正例、10个有机会的负例、80个无机会单位。机会集合描述发生率10/20=50%，全体描述发生率10/100=10%。两种比例的估计对象不同，均不构成因果估计。
E05【负例阈值敏感性】将有机会负例从10扩至20，描述发生率从50%降至10/30≈33.33%。需要独立证据定义“有机会”，并报告宽窄阈值。
E06【未观测混杂】观察T∈{0,1},Y=T。世界甲Y(0)=0,Y(1)=1，效应+1；世界乙U=T，Y(0)=Y(1)=U，效应0。两世界观察(T,Y)相同，非随机资料不能据此确定因果效应。
E07【发表模拟算术】A2报告偏好honest方法90%区间覆盖率接近90%，某adaptive配置为78%；覆盖率差12个百分点。仅对作者表格数字算术核验，未独立重跑模拟。
E08【先验敏感性算术】A1表3 Stimulation的后验预测p值在先验差异方差0.01时为0.001，改至0.02时为0.081，差0.080；Achievement 0.004→0.103；Humility 0.009→0.121。模型接受判断随先验改变。

E01至E06均为人工世界，E07至E08为原刊汇总值核算。没有真实历史资料、个人数据或独立因果验证。

## 四、跨层联系及未来验证清单

个体：潜在态度、偏好与量表回答机制可能变化，需验证同题同尺。群体：人口替代、选择性存活和分层处理效果共同影响总体趋势。制度：政策、行政登记和调查制度改变处理与观测机制。历史：时代、事件机会集合、外部冲击、资料存续与跨期锚定须联合审计。

候选验证步骤：①预注册构念、题项、样本与处理定义；②比较构型、载荷、截距和近似等值，并做先验敏感性；③以事前条件划定负例机会集合，记录被排除单位；④分开报告SATE/PATE、各子群效果、失访和选择性保存；⑤有独立数据时使用honest分割，检验正概率与干扰；⑥至少设计一项能区分测量漂移与真实机制变化的史料或负对照。

未决问题：缺少共同锚题的跨时代潜在均值如何部分识别；机会集合的理论定义如何避免循环；有网络干扰和长期依赖时honest推断如何调整；异质效应跨制度环境的迁移条件是什么。

## 五、证据边界与后续

直接审读三份英文开放原刊指定章节；三份原始摘要仅作书目与命题线索。16项条件命题、8项人工或汇总算术审计。真实历史数据复算0，独立因果估计0，前瞻性预测0，模型熔炼0。未触发付费CI。C005（2026-10-28）及D002（2026-W44）已完成，本轮只读。下一候选TH091：事件时间对齐、处理前趋势与负对照的共同识别边界。
