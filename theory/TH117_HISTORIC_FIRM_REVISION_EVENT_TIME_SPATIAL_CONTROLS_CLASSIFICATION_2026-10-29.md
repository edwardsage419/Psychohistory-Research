# TH117 历史FIRM修订事件时间线、空间对照与风险分类变化识别

日期与非中文原始来源检索日：2026-10-29（Asia/Singapore）。状态：THEORY_NOTE_BOUNDED。
纯理论与公开史料核查。未实施真实地图空间叠置、地块因果估计或预测。

## 一、原始来源与审读层级

A=直接审读原始英文机构网页、公开原始PDF可抽取文本或原刊公开方法节选；B=原刊摘要/原始书目或机构搜索摘要；C=本项目人工反例或条件性推论。

1. [A] FEMA, *IS-0273 Lesson 6: Map Service Center*, https://emilms.fema.gov/is_0273/groups/173.html 。官方区分历史静态FIRM与吸收后续LOMR的动态FIRMette，说明面板编号、生效日期及Revisions/Amendments/Revalidations检索。无DOI。
2. [A] Town of Hingham, MA, *FEMA Flood Insurance Rate Maps (FIRMs)*, https://www.hingham-ma.gov/310/FEMA-Flood-Insurance-Rate-Maps 。地方政府记录1986、2012、2015、2017、2018、2020、2021、2022及2023年地图、LOMR、申诉事件；后续正式生效仍须逐图核验。无DOI。
3. [A-仅文本] Hingham, *Revised FIRM 25023C0018J effective 8-14-15*, https://www.hingham-ma.gov/DocumentCenter/View/1522/Revised-FIRM-25023C0018J-effective-8-14-15-PDF 。PDF可抽取文本确认修订生效日期；地图像素、几何及面积未读取。无DOI。
4. [A] Town of Exeter, NH, *FEMA LOMR Flood Maps effective 11/5/18*, https://www.exeternh.gov/building/fema-lomr-flood-maps-effective-11518 。官方记载Great Dam于2016年10月拆除，2018年11月5日LOMR生效，并采用更新地形与水文数据。无DOI。
5. [B-访问限制] Massachusetts MassGIS, *FEMA National Flood Hazard Layer*, https://www.mass.gov/info-details/massgis-data-fema-national-flood-hazard-layer 。原机构检索摘要表明NFHL汇集生效FIRM及后续LOMR；原站返回403，未全文审读。无DOI。
6. [B] Gibson, M. & Mullins, J. T. (2020), “Climate Risk and Beliefs in New York Floodplains,” *Journal of the Association of Environmental and Resource Economists* 7(6):1069–1111. DOI https://doi.org/10.1086/710240 。原刊摘要：2003至2017纽约交易双重差分，新纳入洪泛区且未受Sandy淹水房产估计价格下降11%；正文需付费，未读。原始数据目录 DOI https://doi.org/10.7910/DVN/57HPYU ，未下载。
7. [B] Keele, L. J. & Titiunik, R. (2015), “Geographic Boundaries as Regression Discontinuities,” *Political Analysis* 23(1):127–155. DOI https://doi.org/10.1093/pan/mpu014 。原刊摘要说明地理边界RD的二维运行变量与边界两侧可比性，正文未通读。
8. [A-方法节选] Sun, L. & Abraham, S. (2021), “Estimating Dynamic Treatment Effects in Event Studies with Heterogeneous Treatment Effects,” *Journal of Econometrics* 225(2):175–199. DOI https://doi.org/10.1016/j.jeconom.2020.09.006 。出版者网页开放摘要及方法引言，指出分批处理下传统TWFE lead/lag的异质效应污染；正式全文未通读。
9. [B-访问限制] Ohio Department of Natural Resources, *Flood Maps & Studies*, https://ohiodnr.gov/discover-and-learn/land-water/issues-for-landowners/floodplain-mapping 。原机构检索摘要区分LOMA、LOMR-F、LOMR与CLOMR；页面打开404，未全文审读。无DOI。

## 二、已核验制度时间线及待核空间事实

候选地区：Hingham, Massachusetts。2015年地方政府称2015-03-31发出LOMR，2015-08-14生效，列出5个修订图幅。2017-09-08调整LiMWA，地方政府明确其他洪水区、洪水标高及洪道未修订。2017-12-13、2018-01-24的相关LOMR亦未改变Hingham这些洪水区数据。2021-07-07重新发布2017相关LOMR，2022-01-21另有LOMR，地方政府均说明相关Hingham洪水区没有变化。这些是SFHA分类变化的候选零变化时点，尚未做独立几何复验。

Cape Cod流域图于2020-01-22完成最终决定，原计划2020-07-22生效，地方政府称后被撤销，2021-07-06无实质改变重新发布。2021重新发布的实际监管生效日仍需独立核验。Charles流域2020-06-19发布预备图，2023-02-03重新发布部分预备图，2023-07-05至2023-10-03为第二次申诉窗口。网页所述预计最终决定日期不能视为已证实生效日期。

Exeter为竞争解释案例：2016-10拆坝、2018-11-05地图修订生效，同时发生工程和测绘变化。此类地图修订同时可能记录实际水文变化和测量更新，无法直接分离纯信息效应。

## 三、16项条件性命题及四层联系

T117-01 [1,2] 公告、预备、最终决定、正式生效、后续LOMR分别形成不同事件时钟，结果变量须对应具体时钟。
T117-02 [1] 当前动态FIRMette吸收后续修订，直接回填历史年份会产生未来信息泄漏。
T117-03 [2,3] 2015年5个图幅受修订，只能确定候选图幅集合，不能推断每个地块的SFHA分类都变化。
T117-04 [2] LiMWA与SFHA是不同风险信息层，2017年可能出现LiMWA变化而SFHA不变。
T117-05 [2] 2017、2018、2021、2022部分LOMR是SFHA分类的候选安慰剂时点，需验证其排除限制与具体几何。
T117-06 [2] 2020年原计划生效但被撤销，按计划日期编码正式实施会造成处理误分。
T117-07 [2] 2023预备图与申诉期可能改变预期，公告效应与正式监管生效效应需要分开识别。
T117-08 [4] 工程改造、地形测绘与地图修订共同发生时，地图前后变化不能唯一归因于信息披露。
T117-09 [7] 地理RD需边界附近潜在结果可比，洪水地形可能在SFHA边界两侧系统不同。
T117-10 [8] 分批生效与效应异质可能污染传统TWFE事件研究，需预先冻结队列、时钟和对照集合。
T117-11 [6] 房价反应可能混合风险信念、强制保险、信贷与灾害记忆；原刊11%是特定估计，不是普适纯地图效应。
T117-12 [1,2] 历史扫描图的坐标配准、投影和边界不确定带可产生伪分类转移。
T117-13 [2] 需固定住宅总体和地理支持集；新建房、地块拆分、迁移会改变分类分母。
T117-14 [2,4] 相邻地区可能受同一灾害、保险市场和住房迁移冲击，空间对照须检验干扰。
T117-15 [6] 仅成交房产的估计目标不同于全部房产或居民福利，选择进入交易可能改变估计。
T117-16 [综合] 个体层涉及风险信念、住房预算；群体层涉及保险池、价格、迁移；制度层涉及图幅、申诉、信贷；历史层涉及灾害、工程和测绘技术。不同机制可相互抵消，福利权重具有价值判断。

## 四、8项日期、原文数字与人工识别审计

E117-01 [日期算术] 2015-03-31至2015-08-14为136天；这只是地方政府记录的发行至生效间隔，不能推出居民实际获知日。
E117-02 [原始资料计数] Hingham 2015修订图幅5份，2022相关LOMR列3份；3/5不能解释为风险面积变化率。
E117-03 [人工转移] 固定100格，旧SFHA20格，其中5格转出，旧低风险20格转入，新SFHA35格。净增15格，实际改变25格。
E117-04 [人工IoU] 依据E117-03，交集15格，并集40格，IoU=37.5%；缺乏洪水真值，不能称其为模型准确率。
E117-05 [人工事件错置] 公告t=0、正式生效t=2，若住房在t=1已有预期反应，将t=0当监管生效使事件时间提前两期。
E117-06 [人工安慰剂] 100格SFHA均未变但发生LOMR文本更新，若“任何LOMR=处理”，则100格全部被误标为SFHA变化处理；其他信息效应仍可能存在。
E117-07 [人工配准误差] 100格中20格落在边界不确定带，确定区80格有8格改变，全体改变率逻辑界限为8%至28%。
E117-08 [人工DID] 处理区均价100降至92，对照区100降至96；简单差为负8，双重差分为负4；平行趋势或无干扰不成立时仍不能因果解释。

## 五、竞争机制、验证清单及阻塞

竞争解释A：信息更新改变居民风险信念，行为可能在正式生效前发生。B：监管生效改变强制保险及信贷成本。C：工程与水文危险改变，同时驱动地图更新。D：地图配准、样本组成和交易选择造成表面变化。

优先以Hingham图幅25023C0018J为候选，独立核对2012原图、2015修订图、适用LOMC、生效日期、空间坐标、图幅哈希；先在固定支持集形成SFHA转移矩阵，再检验LiMWA与SFHA的结果特异安慰剂。对公告与生效窗口、地理带宽、空间溢出、分批处理和配准不确定带分别做敏感性分析。原始图幅若不可免费取得则记录阻塞，禁止付费数据或可能收费的CI。

证据边界：9项英文原始来源或机构资料线索，16项条件性命题，8项人工与日期审计；真实双期地块空间叠置0、独立因果估计0、前瞻性预测0、模型熔炼0。主要阻塞：HISTORIC_PANEL_GEOMETRY_NOT_REGISTERED；LOMC_SPATIAL_OVERLAY_NOT_DONE；2021_REISSUE_ACTUAL_EFFECTIVE_DATE_UNVERIFIED；PARCEL_OUTCOMES_UNAVAILABLE；FULL_COVERAGE_FLOOD_TRUTH_UNAVAILABLE。

C今日C006已完成，只读。D本周D002已完成，只读。未读取个人敏感资料，未开发个人决策产品，未新增费用，未主动运行CI。下一题TH118：历史地图修订零变化安慰剂、公告与生效时差及空间选择的联合识别。R系列全部完成后才统一分类，最后模型熔炼。
