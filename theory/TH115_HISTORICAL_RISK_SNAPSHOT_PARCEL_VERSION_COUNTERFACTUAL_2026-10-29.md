# TH115 历史风险快照、地块版本分解与模型更新反事实

日期及英文原始来源检索日期：2026-10-29（Asia/Singapore）。状态：THEORY_NOTE_BOUNDED。仅研究理论、原始档案与方法；不接触用户个人敏感数据、不进行真实地块模型拟合、不开发产品、不调用付费服务或CI。R系列及C、D子流程独立。

## 一、原始来源与证据等级

A为直接阅读官方原始页面、数据目录或供应商自述的指定段落；B为作者机构正式论文摘要；C为本项目人工推断或数学反例。官方网页只证明制度口径或数据可用性，供应商自述不构成独立预测精度证据。

1. [A] FEMA, *IS-0273 Lesson 6: Map Service Center*. https://emilms.fema.gov/is_0273/groups/173.html 。直接审读历史FIRM、原始生效日期、LOMC修订与Search All Products。无DOI。
2. [A] FEMA, *IS-0274 Lesson 1: Flood Insurance Study*. https://emilms.fema.gov/is_0274/groups/187.html 。历史FIS/FIRM部分需联系档案部门取得。无DOI。
3. [A] USGS (2019), *Providing Major Storm and Short-Term Flood Event Data*. https://www.usgs.gov/mission-areas/water-resources/science/providing-major-storm-and-short-term-flood-event-data 。直接审读STN/FEV高水位痕迹、事件数据和下载渠道。无DOI。
4. [A] NFIP, *FAQs About Policies and NFIP Data*. https://agents.floodsmart.gov/flood-maps-and-data/faqs-about-nfip-data 。直接核验OpenFEMA脱敏坐标、历史时间范围、保单与索赔不可逐条连接、2009年前保单保留偏差。无DOI。
5. [A，供应商原始说明] First Street, *First Street improvements and updates*. https://help.firststreet.org/hc/en-us/articles/360053574994-First-Street-improvements-and-updates 。直接审读2020至2022的模型输入、建筑轮廓、评分阈值及覆盖变化。无DOI。
6. [A，原始数据目录] First Street Foundation (2021), *Property Level Flood Risk Statistics V1.3*. Zenodo DOI https://doi.org/10.5281/zenodo.5768332 。只审目录、字段与公开样例清单，未取得完整地块数据。
7. [A，原始数据目录] First Street Foundation (2022), *Property Level Flood Risk Statistics V2.0*. Zenodo DOI https://doi.org/10.5281/zenodo.6459076 。只审目录、字段与公开样例清单，未取得完整地块数据。
8. [A，数据授权说明] First Street Foundation, *Flood Risk Summary Statistics*, AWS公开数据目录 https://aws.amazon.com/marketplace/pp/prodview-g7s2ug7z3t4ue 。目录标注公开、无需订阅或AWS账号、CC BY-NC-SA 4.0；仅核验页面，未调用云服务或下载。
9. [A，原始数据目录] First Street Foundation (2021), *Normalized First Street Census-Tract Data V1.3*. DOI https://doi.org/10.5281/zenodo.5710940 。记录可见，文件标为Restricted；未申请访问。
10. [A，供应商原始说明] First Street, *Historic Flood Methodology*. https://help.firststreet.org/hc/en-us/articles/360050783973-Historic-Flood-Methodology 。历史洪水重建不同于当年可见的风险评分版本；地块级批量数据注明购买渠道，本轮不采购。
11. [B，作者机构原刊摘要] Croushore, D. & Stark, T. (2003), “A Real-Time Data Set for Macroeconomists: Does the Data Vintage Matter?” *Review of Economics and Statistics* 85(3):605–617. DOI https://doi.org/10.1162/003465303322369759 ，作者机构 https://scholarship.richmond.edu/economics-faculty-publications/3/ 。vintage影响回测的论证来自宏观经济研究，跨域适用待验证。
12. [B，正式原刊摘要与数据声明] Zheng, X., D'Angelo, C., Maidment, D. R. & Passalacqua, P. (2022), “Application of a Large-Scale Terrain-Analysis-Based Flood Mapping System to Hurricane Harvey.” *JAWRA* 58(2):149–163. DOI https://doi.org/10.1111/1752-1688.12987 。作者报告高水位痕迹验证中平均深度误差约0.5米，预测范围覆盖观测推导范围90%以上；研究模型和地点有限，未复算。

## 二、16项条件性理论命题

T115-01 [1、2，制度版本] FEMA历史FIRM及FIS可追溯官方分区，前提是辖区档案完整；官方分区与商业1至10分风险评分属于不同对象。
T115-02 [1，生效时间] 回建某日风险分类需核验图幅生效日及当时生效的修订和LOMC。仅使用初版静态地图会遗漏后续修订。
T115-03 [2，档案缺口] 历史文件无法直接下载时须标记UNKNOWN；检索失败不能推断文件从未存在。
T115-04 [5，评分口径] 同一地块风险评分变化可能来自地形输入、建筑轮廓定位、模型参数或评分阈值改变；跨版本测量等值需独立证明。
T115-05 [6、7，数据vintage] V1.3与V2.0有不同书目与版本说明，但公开目录只附样例，尚不能建立完整免费地块历史面板。
T115-06 [6、7，样例校验] 两版Zenodo目录列出的同名样例文件MD5相同，不能用这些样例推断版本差异。哈希仅按公开元数据核对。
T115-07 [8、9，替代尺度] 公开非商业区域聚合数据提供有限研究路径；另一普查区资料受限。区域平均变化无法识别单一地块评分变化。
T115-08 [10，历史事件与预测] 事后新模型重建旧洪水，与旧时决策者实际可见的评分历史不同；二者混用造成时间信息泄漏。
T115-09 [11，回测信息集] 评价历史决策须固定当时可见的资料版本、发布时间和模型版本；宏观经济vintage方法转移到洪水评分属于研究假设。
T115-10 [3、12，独立真值] USGS高水位痕迹可作为事件级水位观测；采样地点偏向受淹区域时，不能直接推断全域误报率或概率校准。
T115-11 [4，空间隐私] OpenFEMA坐标粗化至一位小数，且保单与索赔不可逐条联结；不能从中还原具体房屋损失与投保史。
T115-12 [4，选择性索赔] 索赔记录受投保、损失、申报共同影响；2009年前保单保留有选择性，不能将索赔率视为全部房屋洪水发生率。
T115-13 [数学推断，交互分解] 旧新模型与旧新环境双向替换可分解总评分变化，交互项使单一路径贡献不唯一；需声明Shapley或其他归因约定。
T115-14 [竞争解释] 地区风险均值变化可由真实危险、模型改良、样本扩张、坐标错配共同产生；只看地区均值无法区分机制。
T115-15 [反馈] 风险披露可能改变加固、保险、迁移及未来观测损失；评估事后误差需区分自然危险、行为适应及样本流失。
T115-16 [价值与跨层] 个体安全和关系成本、群体迁移与保险池、制度地图和供应商、历史气候及地形变动共同作用。多目标权重由主体选择，不能由评分推出普适唯一最优人生。

## 三、8项公开元数据及人工数学审计

E115-01 [双路径，人工] 设f0(x0)=4、f0(x1)=5、f1(x0)=7、f1(x1)=9。总差5；先换环境再换模型为1+4，先换模型再换环境为3+2。两顺序均合计5；环境平均贡献1.5，模型平均贡献3.5。真实应用需四种可运行反事实。
E115-02 [样例哈希，目录核对] Zenodo V1.3与V2.0页面均列同名4.1kB CSV，MD5均为3a4907d33f873294bc176a6fbd54a0d3。未下载重算哈希；两个版本名称不能证明两个样例内容不同。
E115-03 [未来信息泄漏，人工] 事件Y=1，事前风险0.10、事后风险0.25，单事件Brier损失0.81与0.5625。事后更小的损失无法证明历史时点的可实现预测能力。
E115-04 [修订生效，人工] 假设2010年地图生效、2015年修订，2013年应按当时有效地图，2018年应按有效修订。仅使用2010原图可能错分2018暴露；例子不是具体辖区事实。
E115-05 [保险选择，人工] 1000处房屋中100处投保，20处记录索赔，投保样本记录索赔率20%，全部房屋已记录索赔占2%。未投保房屋损失未知，两者都不等于自然洪水发生率。
E115-06 [阳性点偏选，人工] 20处高水位痕迹点中模型覆盖18处，样本覆盖90%。缺少非洪水点及抽样框时无法推断全域特异度或误报率。
E115-07 [缺失界限，人工] 100处房产只有50处可配对版本，其中10处评分改变。配对改变率20%；若其他50处全未知，总体改变率逻辑界限为10%至60%。
E115-08 [分母组成，人工] 旧版100处房产有20处高风险，新版新增100处，其中60处高风险；旧房屋风险全不变时总体高风险比例仍从20%升至40%。样本扩张可伪造风险趋势。

## 四、四层解释与竞争机制

个体层关注风险理解、保险、住房与社会关系损失；群体层关注住房交易、社区适应与保险池组成；制度层关注FEMA地图、LOMC、模型更新、授权与纠错；历史层关注事件时间、地形变化、地图生效和评分发布。竞争解释分别是环境危险变化、模型改良、样本组成变化、行为反馈；这些解释可以并存，现有证据不能排序。

## 五、独立验证清单、阻塞及后续

1. 选择一处免费历史FIRM较完整的辖区，冻结社区代码、图幅ID、修订生效日期、文件哈希与许可，建立制度时间轴。
2. 以USGS事件数据检查高水位痕迹采样位置、日期、垂直基准及非随机覆盖；不得把事件痕迹等同完整地块真值。
3. 对免费非商业区域数据先核验版本、空间单元、样本组成、许可与无费用下载方式；不得主动触发云计费。
4. 冻结地块或地区同一总体，按版本、输入、评分映射、人口组成分层归因；评估配对缺失的逻辑界限。
5. 禁止利用脱敏坐标反向识别具体住户，禁止将事后历史模拟冒充历史评分，禁止把样例文件当作完整面板。
6. PARCEL_VINTAGES_NOT_RECOVERED、MODEL_REPLAY_NOT_RECOVERED、INDEPENDENT_PARCEL_TRUTH_NOT_RECOVERED：完整免费地块双版本、可执行历史模型及完整独立真值均未核实。
7. 真实地块数据复算0、独立因果估计0、前瞻性预测验证0、模型熔炼0。公开来源12项，直接审读原机构网页或目录10项、论文摘要2项；16项命题、8项审计均为有限研究储备。

C006为2026-10-29已完成日增量，D002为2026-W44已完成周专题，本轮只读。下一题TH116：免费区域风险数据版本可比性、空间单元组成效应及历史FIRM修订可行性审计。先完成全部R系列，再统一归纳分类，最后模型熔炼。
