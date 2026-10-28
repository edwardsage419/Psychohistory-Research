# TH116 免费区域洪水风险数据版本可比性、空间单元组成与历史FIRM可行性审计

日期及非中文原始来源检索日期：2026-10-29（Asia/Singapore）。状态：THEORY_NOTE_BOUNDED。研究对象为公开文献、数据目录和可检验的方法，不涉及个人敏感资料、产品开发、付费服务或主动CI。

## 一、原始出处及证据等级

A：直接审读原机构原始页面、数据目录、正式开放论文指定章节。B：原刊摘要或书目。C：本项目的条件性推断及人工反例。供应商说明只能证明其公开宣称，不能证明独立预测精度。

1. [A] First Street Foundation, *Flood Risk Summary Statistics*, AWS原始公开数据目录 https://aws.amazon.com/marketplace/pp/prodview-g7s2ug7z3t4ue 。目录注明美国本土48州、县/ZIP/国会选区统计、无需订阅及AWS账号、匿名S3访问示例，CC BY-NC-SA 4.0许可。未下载数据。无DOI。
2. [A] First Street, *First Street improvements and updates*, https://help.firststreet.org/hc/en-us/articles/360053574994-First-Street-improvements-and-updates 。官方注明季度数据、年度洪水模型更新及2022年评分方法和地理覆盖变化。无DOI。
3. [A] First Street Foundation (2021), *Property Level Flood Risk Statistics V1.3*, DOI https://doi.org/10.5281/zenodo.5768332 。公开页面列出4.1kB样例，完整地块数据另需购买。
4. [A] First Street Foundation (2022), *Property Level Flood Risk Statistics V2.0*, DOI https://doi.org/10.5281/zenodo.6459076 。公开页面亦列出4.1kB样例；两版样例MD5均为3a4907d33f873294bc176a6fbd54a0d3，未下载重算。
5. [A] FEMA, *IS-0273 Lesson 6: Map Service Center*, https://emilms.fema.gov/is_0273/groups/173.html 。直接审读历史FIRM、图幅生效日期、LOMC修订与动态FIRMette的区别。无DOI。
6. [A] FEMA (2017), *Flood Hazard Products Direct Download*, https://msc.fema.gov/msccontent/FEMA_Hazard_Products_Direct_Download.pdf 。两页原始官方说明，直接审读产品ID与标准下载URL；未实际下载历史图幅。无DOI。
7. [A] NFIP/FEMA, *FAQs About NFIP Data*, https://agents.floodsmart.gov/flood-maps-and-data/faqs-about-nfip-data 。原始隐私说明，核验坐标脱敏、保单与索赔不能逐条关联。无DOI。
8. [A] Hallisey, E. et al. (2017), “Transforming geographic scale: a comparison of combined population and areal weighting to other interpolation methods.” *International Journal of Health Geographics* 16:29. DOI https://doi.org/10.1186/s12942-017-0102-z ，开放全文 https://link.springer.com/article/10.1186/s12942-017-0102-z 。直接审读方法、结果、讨论和局限。原研究是癌症死亡计数的空间转换，转用于洪水风险属待检验外推。
9. [B] Schroeder, J. P. (2017), “Hybrid Areal Interpolation of Census Counts from 2000 Blocks to 2010 Geographies.” *Computers, Environment and Urban Systems* 62:53–63. DOI https://doi.org/10.1016/j.compenvurbsys.2016.10.001 ，原刊摘要 https://pubmed.ncbi.nlm.nih.gov/28260826/ 。全文PMC5330682本轮遭验证码，未通读。
10. [B] Fotheringham, A. S. & Wong, D. W. S. (1991), “The Modifiable Areal Unit Problem in Multivariate Statistical Analysis.” *Environment and Planning A* 23(7):1025–1044. DOI https://doi.org/10.1068/a231025 。仅原刊摘要，空间尺度与分区敏感性需结合数据验证。
11. [A] USGS, *Short-Term Network* https://apps.usgs.gov/stnweb/ 及 *High-Water Marks and Flooding* https://www.usgs.gov/water-science-school/science/high-water-marks-and-flooding 。直接核验历史洪水高水位痕迹的观测用途与选择性覆盖。无DOI。
12. [A] First Street Foundation (2021), *Normalized First Street Census-Tract Data V1.3*, DOI https://doi.org/10.5281/zenodo.5710940 。目录可见，文件Restricted；未申请访问。

## 二、16项条件性理论命题、前提、竞争解释及四层联系

T116-01 [1] 公开区域CSV可以支持县、ZIP或国会选区的统计比较，前提是字段、年份、样本范围和模型版本一致；公开目录尚未证明可取得双版本面板。
T116-02 [1] AWS页面宣称无需订阅与账户，执行环境对S3域名的匿名请求却出现DNS解析失败。对象清单、大小、真实可达性及潜在传输费用均待核实。
T116-03 [1] CC BY-NC-SA 4.0对商业使用有限制；当前非商业理论研究可以记录该来源，未来商业利用必须另行确认授权。
T116-04 [2、3、4] 不同书目版本不等于已取得不同地块评分；两版公开样例MD5相同，完整版本配对缺失。
T116-05 [2] 地区风险评分变化可能来自地形、建筑定位、评分阈值、模型范围或实际风险改变；仅地区均值无法点识别原因。
T116-06 [8、9] 跨年比较须固定空间支持集与目标总体；人口迁移、住宅新建、边界变更会改变分母。
T116-07 [8] 简单面积加权隐含区域内均匀分布假设；人口加权隐含人口可代理目标暴露的假设，洪水暴露与人口密度可能不一致。
T116-08 [8] Hallisey等在其特定研究中联合面积人口权重的绝对误差均值最低，但方法间成对检验未发现统计显著差异，不能推出通用最优。
T116-09 [9、10] 跨期边界插值可能改善表面可比性，同时引入MAUP和生态推断误差；需要保留插值假设和区间。
T116-10 [5、6] FEMA历史图幅编号、生效日期及LOMC有助于构造官方分类时间轴；静态原图与已吸收修订的动态地图不能混用。
T116-11 [5] FEMA教程示例列1974、1975、1982年图幅与日期；这只证明检索界面具备历史记录，不代表已取得某房产的两期分类。
T116-12 [6] 官方产品ID提供可重复定位机制，后续仍需核对实际文件、坐标系、空间覆盖及修订有效期。
T116-13 [7] OpenFEMA脱敏位置及无法联结保单与索赔限制地块因果研究，理赔记录还受投保与申报选择影响。
T116-14 [11] USGS高水位痕迹可验证局部洪水高度，受灾地点选择性采样导致全域误报率与概率校准不可直接识别。
T116-15 [竞争解释] 地区风险变化可由模型、边界、样本、自然危险和行为反馈共同生成，需保留多机制并行解释和部分识别界限。
T116-16 [四层与价值] 个体涉及住房安全与负担，群体涉及迁移和保险池，制度涉及地图与许可，历史涉及洪水和版本；各层机制可能冲突，安全、财务、关系等价值权重没有普适唯一解。

## 三、8项原刊数字与人工审计

E116-01 [原刊核算] Hallisey等五方法的平均绝对计数差为5.50、5.00、4.17、2.74、3.43。方法4相对方法1减少(5.50−2.74)/5.50=50.18%，仅是样本内描述；作者报告方法间成对检验没有统计显著差异。
E116-02 [人工组成效应] 旧地区100处房屋20处高风险；新增50处其中25处高风险，旧房不变时总体风险率由20%变为45/150=30%。
E116-03 [人工边界效应] 原辖区40处房屋8处高风险，边界并入60处其中42处高风险，地区率由20%升至50%，任何房屋本身风险都未变化。
E116-04 [人工权重效应] 两区分别30处中10处高风险、70处中10处高风险；区比例33.33%和14.29%的简单均值23.81%，按房屋数加权为20%。
E116-05 [人工缺失界限] 120处房屋仅80处成功跨版本配对，其中12处标签改变；整体改变率逻辑界限为12/120=10%至52/120=43.33%，配对样本改变率15%并非总体已识别估计。
E116-06 [官方示例核验] FEMA培训页示例产品的有效日期为1974-08-08、1975-10-24及1982-02-03。尚未下载图幅或验证空间重叠，不能声称发生真实风险分区改变。
E116-07 [数据可达性审计] AWS目录标注免费无订阅，Zenodo两版公开文件均只见4.1kB样例，另一个普查区目录Restricted。匿名S3对象清单未取得，标记ACCESS_UNVERIFIED。
E116-08 [人工真值缺口] 20个高水位痕迹点命中18个，条件命中率90%；缺少非洪水点及完整抽样框，不能估计全域特异度、校准或历史时点的可实现预测精度。

## 四、机制边界、验证清单及阻塞

个体层：风险理解、保险和住房选择；群体层：迁移、住房新建与保险池组成；制度层：FEMA生效图、LOMC、供应商评分与授权；历史层：灾害事件、测绘技术、地形和发布时间。竞争解释包含真实环境变化、模型修订、样本组成和行为适应，现有资料不能排序。

下一步优先：选择有免费历史图幅的单一FEMA辖区，记录社区代码、图幅ID、生效日、LOMC及文件哈希；只在确定不收费的匿名路径下核验公开区域CSV对象清单；冻结相同地理边界、分母、指标和历史可见版本后才比较；对USGS高水位痕迹记录选择性采样与垂直基准。禁止使用事后重建冒充历史预测，禁止由脱敏数据反向识别住户。

本轮来源12项，其中开放正式论文直接审读1篇，官方/数据目录直接审读9项，原刊摘要2项。新增16项条件命题、8项审计。真实地块复算0、独立因果估计0、前瞻性预测验证0、模型熔炼0。

阻塞：AGGREGATE_OBJECT_LIST_UNVERIFIED；PARCEL_VINTAGES_NOT_RECOVERED；HISTORIC_FIRM_PANEL_NOT_DOWNLOADED；INDEPENDENT_FULL_COVERAGE_TRUTH_NOT_RECOVERED。C006为2026-10-29已完成日增量，D002为2026-W44已完成周专题，本轮只读。下一题TH117：历史FIRM修订事件时间线、空间对照与风险分类变化识别。研究顺序仍为全部R系列完成、统一分类、模型熔炼。
