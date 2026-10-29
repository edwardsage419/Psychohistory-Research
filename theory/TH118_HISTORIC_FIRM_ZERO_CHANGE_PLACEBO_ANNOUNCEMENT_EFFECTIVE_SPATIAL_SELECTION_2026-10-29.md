# TH118 历史FIRM零变化安慰剂、公告与生效时差及空间选择的联合识别

研究及非中文原始来源检索日期：2026-10-29（Asia/Singapore）。
状态：THEORY_NOTE_BOUNDED。纯理论、公开原始制度文本及人工数学反例。未开展地理叠置、房价估计、真实因果复算或前瞻性预测。与TH117相衔接，补充原始LOMR文件逐页证据，区分可检验的零变化结果与无效安慰剂假设。

## 一、原始资料、书目及实际审读层级

证据级别A为本轮直接核验的公开英文原始机构文本或PDF指定页；B为原刊摘要或官方文档公开片段；C为本项目提出的条件性命题和人工演示。所有链接均于2026-10-29检索。

1. [A] Town of Hingham, MA, *FEMA Flood Insurance Rate Maps (FIRMs)*, https://www.hingham-ma.gov/310/FEMA-Flood-Insurance-Rate-Maps 。直接审读历史修订时间线、受影响图幅清单、2020撤销与2021重发、2023预备图。机构网页无DOI。该网页是地方政府的行政记录，不是已独立验证的历史地块空间真值。
2. [A] FEMA, *Letter of Map Revision, Case 21-01-1137P*, issue/effective 2021-07-07, 15页，https://www.hingham-ma.gov/DocumentCenter/View/13105/LOMR-Effective-7-7-21-PDF 。直接审读第1至2页。第1页说明部分重新发布2017-09-08的16-01-2154P，第2页明确仅LiMWA更新，SFHA、1%年超越概率基准洪水高程与洪道不修订，并说明无附带注释FIRM图幅。无DOI。
3. [A] FEMA, *Letter of Map Revision, Case 22-01-0074P*, issue/effective 2022-01-21, 8页，https://www.hingham-ma.gov/DocumentCenter/View/17883/LOMR-Effective-1-21-22-PDF 。直接审读第1至2页。明确LiMWA为更新对象，其他SFHA、基准高程和洪道不修订；地方政府进一步指出Hingham自身LiMWA也未修订。无DOI。
4. [A] FEMA, *Letter of Map Revision, Case 18-01-0249P*, issue/effective 2018-01-24，PDF共10页，前4页为决定文本，https://www.hingham-ma.gov/DocumentCenter/View/17884/LOMR-Effective-1-24-18-PDF 。直接审读决定文本第1至4页；正文明确主要对象为Hull LiMWA与2017-12-13版本一致，监管洪水危险不改变，并说明有注释图幅但不会立即全面重印FIRM。其后图像附件未做几何分析。无DOI。
5. [B] FEMA, *Flood Map Changes Viewer: Instructions*, June 2019, https://www.fema.gov/sites/default/files/documents/fema_flood-map-change-viewer_instructions.pdf 。公开官方文本片段说明预备、待生效和生效层用途不同，预备或待生效层不能直接用于正式保险费率和强制购买；PDF打开受限，未全文审读。无DOI。
6. [A] FEMA, *IS-0273 Lesson 6: Map Service Center*, https://emilms.fema.gov/is_0273/groups/173.html 。官方历史图幅、现行图幅、LOMC与动态FIRMette检索说明，直接核验公开课程文本。无DOI。
7. [B] Roth, Jonathan (2022), “Pretest with Caution: Event-Study Estimates after Testing for Parallel Trends,” *American Economic Review: Insights* 4(3):305–322. DOI https://doi.org/10.1257/aeri.20210236 。原刊摘要直接核验；原刊PDF打开403，未声称全文审读。前趋势检验功效不足与条件选择导致推断偏差是作者观点。
8. [A/公开原文可用，摘要和方法概述核验] Lipsitch, Marc, Eric Tchetgen Tchetgen & Ted Cohen (2010), “Negative Controls: A Tool for Detecting Confounding and Bias in Observational Studies,” *Epidemiology* 21(3):383–388. DOI https://doi.org/10.1097/EDE.0b013e3181d61eeb 。作者开放稿 https://pmc.ncbi.nlm.nih.gov/articles/PMC3053408/ ，本轮PubMed原刊摘要核验 https://pubmed.ncbi.nlm.nih.gov/20335814/ ；PMC页面曾返回浏览器校验，未声称完整原文逐页审读。
9. [B] FEMA, *Letter of Final Determination* public dataset metadata, https://catalog.data.gov/dataset/letter-of-final-determination ，记录更新2025-09-01。官方定义LFD后六个月的正式生效准备期，作为制度时钟的候选核对来源。无DOI。
10. [A] MassGIS, *FEMA National Flood Hazard Layer*, July 2025, https://www.mass.gov/info-details/massgis-data-fema-national-flood-hazard-layer 。州级机构说明现行NFHL汇集已生效FIRM和LOMR，随生效日期更新；现行数据不能无条件充当历史版本。无DOI。

## 二、行政事件事实与本轮新核验

事实F118-01：FEMA 2021-07-07文件编号21-01-1137P，明确部分重发2017-09-08的16-01-2154P，更新LiMWA，SFHA、BFE和洪道不变。该文件的行政更新与风险区分类变化分属不同变量。
事实F118-02：FEMA 2022-01-21文件编号22-01-0074P，明确更新LiMWA且SFHA、BFE和洪道不变。Hingham地方网页说明本镇LiMWA也没有变化。
事实F118-03：FEMA 2018-01-24文件编号18-01-0249P，针对Hull的LiMWA协调，地方网页说明Hingham现行洪水危险信息不变。文件提到注释图幅及未立即全面重印，不能用PDF更新时间代理法规风险区变化。
事实F118-04：Hingham 2017-09-08 LiMWA事件涉及7个列示图幅，2018-01-24列示4个，2022-01-21列示3个。它们属于行政列示图幅数量，不代表有同等数量的Hingham地块改变SFHA。
事实F118-05：Cape Cod流域2020-01-22最终决定，原定2020-07-22生效，2020-06撤销，2021-07-06无实质内容变化重新发布。2021地方分区条例同步修改。重新发布并不自动意味着2020原定生效日曾产生正式监管效力。
事实F118-06：Charles流域2020-06-19预备图，2023-02-03多数预备图重发，2023-07-05至2023-10-03为申诉期。预期最终决定日期不能当作实际最终决定日期。

## 三、16项条件性理论命题、竞争解释与四层联系

T118-01 [1,2,3] 行政LOMR发生与SFHA改变是两个不同处理变量。前者可伴随LiMWA信息变化，后者需要固定空间单位的分类转移证据。
T118-02 [2] 2021重发属于历史信息谱系更新。若把2017与2021视为两次独立SFHA冲击，会重复计算同一监管主题。
T118-03 [3] 2022文件给出SFHA不变的行政文本证据，可作为SFHA分类的候选零变化时点；地块几何层面的零变化尚未独立证明。
T118-04 [4] 2018文件中的图幅附件存在，并不蕴含Hingham监管危险变化。行政附件数量和风险分类变化数量须分开。
T118-05 [2,3,8] 对SFHA分类作为结果，LiMWA专项修订可充当结果特异的候选安慰剂。对房价、建造标准、风险认知或地方政策结果，LiMWA可能有真实影响，安慰剂排除限制可能失败。
T118-06 [1] 2021条例修订与图幅重新发布同年发生，观察到房价变化可能混合地方制度采纳与信息效应。
T118-07 [1,9] 公告、最终决定、撤销、重新发布、正式生效和条例采纳应建立六类独立时钟，缺少真实日期时以UNKNOWN标记。
T118-08 [5,9] 预备图可能影响预期行为，正式强制保险监管需核对实际生效；公告与实施效应不应机械合并。
T118-09 [7] 未发现显著前趋势不足以证明平行趋势，尤其样本量小、成交选择严重或公告前行为已经发生。
T118-10 [8] 负对照需要事前指定为何不能受目标机制影响，同时尽可能共享同类混杂；零变化SFHA不自动保证价格的零效应。
T118-11 [1,4] 相邻Hull与Hingham的跨镇图幅和共享沿海环境可能产生溢出，不能把相邻镇机械视为未处理对照。
T118-12 [6,10] 现行NFHL汇集历次生效修订，不能无条件回填2017或2021历史时点；须保存as-of版本与当时已知信息。
T118-13 [1] 仅成交房屋的价格结果具有选择进入交易的机制，风险信息可能改变交易概率，使成交均价与存量价值分离。
T118-14 [1,4] 若地块拆分、住房新建或边界重投影同时发生，分类变化需要固定空间支持集并对边界不确定带做上下界。
T118-15 [2,3,4] 对风险区分类、LiMWA、BFE、强制保险、住房交易应分别建立结果向量；不同结果的安慰剂有效性不可互相转移。
T118-16 [综合] 四层路径：个体风险理解与购房；群体保险池、邻里传播及迁移；制度图幅修订、地方条例、贷款约束；历史海岸水文、测绘技术及法规时钟。不同路径的净福利依赖价值权重和可识别性，尚无统一最优政策推断。

竞争解释A：真实风险或水文变化。B：LiMWA等非SFHA信息变化。C：地方分区条例和金融保险制度变化。D：邻近地区共同冲击。E：历史版本回填、配准与交易选择偏差。任何一项均可能使“零变化LOMR”在某个具体结果上失去安慰剂性质。

## 四、8项原文数字与人工识别审计

E118-01 [日期算术] 2017-09-08至2021-07-07为1398天，跨越多个制度和市场环境。2021重发不可直接视作2017首次信息冲击的独立重复实验。
E118-02 [日期算术] 2017-09-08至2018-01-24为138天。行政时差不能作为真实居民信息接收滞后的无偏估计。
E118-03 [日期算术] 2020-01-22最终决定至2021-07-06重发为531天，2020-07-22原计划生效至2021-07-06为349天。原计划日期已撤销，监管处理编码应单独标记。
E118-04 [日期算术] 2023-07-05至2023-10-03为90天。申诉窗口长度只说明制度安排，不能据此推断任何申诉的成功率。
E118-05 [图幅计数] Hingham网页列示2017年7个、2018年4个、2022年3个受影响图幅。7、4、3不是地块变化数，也不能相加当作14个独立空间单元，因为图幅有重叠。
E118-06 [人工零结果安慰剂] 100个固定格点SFHA均不变，但20格LiMWA状态改变。若结果是SFHA分类，观测改变数0；若结果是LiMWA，改变数20。相同LOMR事件对不同结果的零假设相反。
E118-07 [人工公告与监管拆分] 假设基期房价100，公告后98，正式生效后97，且对照组始终100。公告阶段差为负2，公告至生效增量负1；缺少反事实趋势和共同冲击排除，二者均不能直接解释为因果效应。
E118-08 [人工选择与空间界限] 固定100格，80格可无歧义配准，其中8格SFHA改变，20格边界不确定。全体改变率逻辑界限为8%至28%。若只观察成交的20套房，成交组分类比例也不能代表100格总体。

## 五、可执行验证清单与明确阻塞

1. 从2012及2015官方历史图幅建立固定格点支持集，保存原始文件字节哈希、面板号、投影和有效时间。对2017、2018、2021、2022各LOMR逐案核对文件编号、覆盖社区、覆盖图幅及是否有几何变化。
2. 先对SFHA、LiMWA、BFE分别生成转移矩阵及边界不确定带，再预注册候选零变化结果和禁止作为负对照的结果。2021-07-07重发与2021-07-06 Cape Cod图幅重发必须区分。
3. 对事件时钟使用announcement、LFD、rescission、reissue、effective、bylaw_adoption独立字段，缺日期保留空值与证据来源，不根据预计日期补造事实。
4. 真实住房研究另需事前冻结对照镇、空间缓冲区、重复交易样本和迁移分母；同时审计相邻镇溢出、提前反应及成交选择。前趋势检验只作为诊断。
5. 若历史图幅、地块数据或独立洪水真值无法免费合法取得，停止实证因果声称并保留阻塞。不得购买数据、运行可能收费的CI或访问个人敏感资料。

阻塞状态：HISTORIC_GEOREFERENCED_VINTAGES_MISSING；PARCEL_PANEL_OVERLAY_NOT_DONE；2021_CAPE_COD_ACTUAL_EFFECTIVE_DATE_NOT_VERIFIED；2017_SCANNED_LOMR_TEXT_NOT_FULLY_EXTRACTED；SPATIAL_CONTROLS_NOT_DEFINED；PARCEL_OUTCOME_DATA_NOT_OBTAINED。特别强调：FEMA 2021和2022官方PDF给出行政文本层面SFHA不变证据，不能替代逐地块独立空间核验。

本轮真实地块空间叠置0，独立因果估计0，前瞻性预测0，模型熔炼0。C006（2026-10-29）与D002（2026-W44）已完成，保持只读。R系列继续独立推进，全部完成后再统一归纳分类，最后熔炼。下一专题TH119：LiMWA与SFHA的结果特异安慰剂、沿海建筑标准及地方条例共同冲击。
