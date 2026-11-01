# TH202 南非养老金、家庭内分配与制度冲击的竞争解释

track: theory
run_date: 2026-11-02 (Asia/Singapore)
observed_head: 5479d1e4dc5e775d0d7f6ea8bd9e01b76622f0f3
target_key: (theory,Duflo2000-NBER8061+CaseDeaton1996-NBER5572+BrowningEtAl1994-JPE,original-v1,recipient_identity_vs_income_pooling_and_household_selection)
status: THEORY_NOTE_BOUNDED; PRIMARY_ORIGINAL_SELECTED_PAGES; NONBLIND; REAL_REESTIMATION_NOT_RUN

## 原始来源、版本与实际阅读范围

1. Esther Duflo (2000), *Grandmothers and Granddaughters: Old Age Pension and Intra-Household Allocation in South Africa*, NBER Working Paper 8061, DOI 10.3386/w8061, https://www.nber.org/system/files/working_papers/w8061/w8061.pdf 。直接阅读原始工作稿印刷pp1至12、14至19，重点§2.1至2.3、§3.1至3.2、§4.1至4.2、§5.1至5.4和原作者局限。2003年正式发表版为 *World Bank Economic Review* 17(1):1至25，DOI 10.1093/wber/lhg013；本轮仅核验正式版出版页摘要，未逐页对照，故2000稿数值不可自动视为2003版的完全相同数值。
2. Anne Case, Angus Deaton (1996), *Large Cash Transfers to the Elderly in South Africa*, NBER Working Paper 5572, DOI 10.3386/w5572, https://www.nber.org/papers/w5572 。实际读取作者原始工作论文的官方摘要与出版信息，全文PDF访问受阻。1998正式版 *Economic Journal* 108(450):1330至1361，DOI 10.1111/1468-0297.00345，出版社摘要核验。作者报告养老金支出行为与收入来源中性相容，需保留为与Duflo结论的竞争性描述，且两篇使用相近政策背景，不能视为独立随机实验。
3. Martin Browning, François Bourguignon, Pierre-André Chiappori, Valérie Lechene (1994), *Income and Outcomes: A Structural Model of Intrahousehold Allocation*, *Journal of Political Economy* 102(6):1067至1096, DOI 10.1086/261964, https://discovery.ucl.ac.uk/id/eprint/16866/ 。实际读取UCL机构馆藏原刊摘要及研究设计说明，PDF正文读取超时。作者假设家庭内部决策产生有效率配置，报告加拿大无子女伴侣的成员相对收入与个人支出分配相关；这一假设不能被直接移植到南非扩大家庭。
4. Martin Browning, Pierre-André Chiappori (1998), *Efficient Intra-Household Allocations: A General Characterization and Empirical Tests*, *Econometrica* 66(6):1241至1278, DOI 10.2307/2999616，https://ora.ox.ac.uk/objects/uuid:d0bce5ad-f966-4c78-ab98-0c4b0f723f25 。仅机构开放摘要及工作稿元数据，全文未读。集体家庭模型的有效率配置为可反驳假设。

## 原文支持的命题与理论边界

A. Duflo2000§2将单一家庭效用作为特例，集体模型允许成员不同效用及Pareto权重。原文假设没有跨期储蓄/借贷，并写出每期预算约束 sum_h p_t q_t^h=sum_h y_t^h。永久、未被家庭形成时预期的非劳动收入冲击，在单一家庭模型中只通过家庭总收入影响配置；集体模型还可能改变获得收入成员的谈判权重。工资收入与资产收入的横截面相关性无法直接识别该差异，因劳动供给、资产归属和配偶匹配内生。短期非劳动收入冲击的非合并可能挑战更广的效率假设，不能与永久收入冲击检验混同。

B. Duflo2000§3记载1993年南非调查约9000户，儿童分析限制为6至60个月；养老金女性资格60岁、男性65岁，年龄合格与实际领取不同。原作者将领取资格用于工具变量及不同出生队列的比较。§4报告女童体重身高比中，女性年龄合格的约0.60个标准差系数（标准误0.19），通过资格工具变量得到女性领取的约1.19个标准差；这是不同估计对象，不能把0.60与1.19当作同一效应或精确比值。男性领取和男童的相应结果未检出统计显著性，并不证明零效应。

C. §5比较不同年龄儿童的身高年龄比，利用养老金扩张时间与儿童生命历程暴露长度。原作者承认家庭居住安排可随养老金改变，使用“祖父母存活”作为替代工具，女性领取对女童的点估计约1.06，原文仅在15%显著性水平附近，精度较低。祖父母存活仍可能与家庭资源、文化和照护联系，排除限制需另证。同期营养项目、年龄测量、样本选择、历史种族歧视及家庭组成均为竞争解释。

D. Case/Deaton1996官方摘要认为养老金收入的支出方式与其他收入来源相近；Duflo2000的性别差异集中在儿童人体测量结局。两种证据的结局、识别设计和可见层级不同。宏观消费类别的收入合并与某类儿童的营养差异可以同时出现；也可能因样本选择或不同识别假设出现冲突。不能把“家庭总支出相近”升级为“家庭内部所有人结果相同”。

E. 独立构造性不可识别反例：两个两人家庭的可见总消费都为10，成员私有消费分别为(2,8)与(8,2)。在缺少成员层面记录时，观察者无法由总额识别内部分配，更无法由总额唯一恢复谈判权重。即使成员消费可见，Pareto效率、威胁点、利他主义与社会规范仍可能给出相同结果。该反例仅为逻辑示范。

## 四层、反证与未读范围

个体：照护、营养与成员目标；群体：家庭共同居住、代际转移、成员议价；制度：养老金资格、领取渠道与行政改革；历史：南非1991至1993年政策转变及长期歧视遗产。此处仅列局部理论联系，未开展R系列统一分类或熔炼。

可证伪的竞争路径：在明确随机或准实验的收入接收者变化、固定家庭构成与可测量的个人结果下，检验相同家庭总收入时接收者身份是否改变个人结果；记录资格、领取、同住、营养项目、家庭外转移及儿童出生队列；检验处理前趋势、家庭迁入、排除限制和儿童测量误差。该设计尚未实施。

证据层级：Duflo2000作者原始工作论文指定页为A级原作阅读；Case/Deaton1996、Browning等1994/1998和Duflo2003正式版为B级摘要/书目。原作者实证发现属于真人观察研究的作者声明，本项目独立微观复算、现实因果估计、历史预测均NOT_RUN。不可识别反例只证明逻辑。未读：Duflo2003正式全文逐页差异、原始微观数据与代码、Case/Deaton全文、Browning等全文。不得把2000与2003或1996与1998稿当成独立实证复现。

下一步：优先核验Duflo2003正式发表表格与2000稿的估计对象差异，寻找独立南亚或非洲家庭资源分配原始研究；同时扩大到此前弱覆盖的历史人口与非西方亲属制度。C010、D003分别归档，不重复本笔记。
