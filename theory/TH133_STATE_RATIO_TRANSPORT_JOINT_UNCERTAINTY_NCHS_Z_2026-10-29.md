# TH133 州级编码比率运输、统计区间联合不确定性与原始NCHS检验公式

研究及英文来源检索日期：2026-10-29（Asia/Singapore）。状态：THEORY_NOTE_BOUNDED。
目标键：(theory, CDC_ICD9_ICD10_TH133, theory-v1, state transport × ratio sampling error × count uncertainty × model-dependent coding jump)。
研究为非盲态，已读取TH129至TH132的公开结果、C006、D002及主线R268 S64交接。只读原作与官方汇总，无个体数据、无独立因果估计；不修改R系列及C/D。

## 一、原始来源、实际读取范围与版本

A1 [直接审读51页原始指南第1至3、10至17页，特别是第16页Formula 3的PDF图像] Miniño AM, National Center for Health Statistics (2000-12-04). *A Guide to State Implementation of ICD-10 for Mortality, Part II: Applying Comparability Ratios*. 官方PDF，无DOI。https://ftp.cdc.gov/pub/health_statistics/nchs/datasets/Comparability/icd9_icd10/CR_application_sate_guide.pdf 。该指南的例子是虚构计数，区分100例及以上与1至99例，提供比率RSE、修正率RSE、联合Z检验。
A2 [直接审读原刊第110至112页公式9至18及其示例，含第112页图像] Hoyert DL, Arias E, Smith BL, Murphy SL, Kochanek KD (2001-09-21). *Deaths: Final Data for 1999*. National Vital Statistics Reports 49(8). 官方原刊，无DOI。https://www.cdc.gov/nchs/data/nvsr/nvsr49/nvsr49_08.pdf 。此原刊给出联合不确定性公式；它的1999美国人口和死亡率不能直接代替Wisconsin州级分母。
A3 [直接审读州官方9页PDF第1页解释与第2页败血症计数] Wisconsin Department of Health Services (出版年未确认). *ICD-10/ICD-9 Comparability Ratios for 113 Selected Causes of Death*. 官方PDF，无DOI。https://www.dhs.wisconsin.gov/stats/deaths/icd10-9comparetable.pdf 。1998旧码317、1999新码376、调整计数379；州表的375.3至382.7是其所述公式计算值。
A4 [复核正式报告指定表与摘要，已在TH132阅读，当前非独立新来源] Anderson RN, Miniño AM, Hoyert DL, Rosenberg HM (2001-05-18). *Comparability of Cause of Death Between ICD-9 and ICD-10: Preliminary Estimates*. NVSR 49(2), 无DOI。https://stacks.cdc.gov/view/cdc/6425/cdc_6425_DS1.pdf 。1996年初步双编码败血症新码21,258、旧码17,791，R约1.1948738126，报告SE(R)=0.0042。
A5 [直接核验官方字典第3至5页和缺失描述，非本轮下载原始数据] CDC/NCHS (2004-07-16). *Documentation for the Public Use Multiple Cause of Death File on Comparability between ICD-9 and ICD-10*. 无DOI。https://ftp.cdc.gov/pub/health_statistics/nchs/datasets/Comparability/icd9_icd10/ICD9_ICD10_comparability_file_documentation.pdf 。2,318,212记录，21,290条缺新版编码，最终可比较记录2,296,922。
A6 [直接阅读2026-09-16官方更新网页的比率及分层警告] CDC/NCHS (2026-09-16). *Comparability ratio*, Health, United States. 无DOI。https://www.cdc.gov/nchs/hus/sources-definitions/comparability-ratio.htm 。所列最终比率是精选类别；不能以此冒充113类完整最终计数。
A7 [直接阅读出版者原始摘要、作者机构版本元数据；搜索引擎可见开放全文结果段，未逐页读取原刊全文] Chen HS, Zeichner S, Anderson RN, Espey DK, Kim HJ, Feuer EJ (2020). *The Joinpoint-Jump and Joinpoint-Comparability Ratio Model for Trend Analysis with Applications to Coding Changes in Health Statistics*. Journal of Official Statistics 36(1):49–62. DOI:10.2478/jos-2020-0003. https://journals.sagepub.com/doi/10.2478/jos-2020-0003 ；作者机构开放版本 https://authors.library.caltech.edu/records/xnhvx-d5f49 。公开检索段报告败血症模型跳跃1.2542（SE 0.032）与发表的桥接比率1.1949（SE 0.0042）；两者目标和模型假设不同，不可视为独立金标准。
A8 [直接阅读官方技术指南“Calculation”和“Application”节] UK Department of Health and Social Care, *Using comparability ratios for mortality data*, 网页未见确定发布年，无DOI。https://fingertips.phe.org.uk/static-reports/public-health-technical-guidance/Mortality/Comparability_ratios.html 。明确调整计数需要标注，部分ICD修订按年龄、性别分层；其英国方法和美国历史样本不能机械合并。
A9 [直接核验官方目录与文件类型，未获取原始工作表字节] CDC/NCHS (2004-05-26). *Comparability_Ratio_tables.xls*，208,896字节，无DOI。https://ftp.cdc.gov/pub/health_statistics/nchs/datasets/Comparability/icd9_icd10/ 。尝试容器HTTPS下载因DNS解析失败，网页读取XLS返回不支持application/vnd.ms-excel；工作表字段、原始SHA及113类最终行仍未核验。

来源等级：A1/A2/A3/A5/A6/A8为官方原文指定范围直接读取；A4为既有原作再核；A7原刊摘要及公开检索结果，A9仅目录。全部为英文非中文网站。原始作者、政府发布方与本项目数学演示分离。

## 二、16项条件性理论命题

T133-01 [A1,A2] 跨ICD版本比较时，统计目标必须区分旧码年度率R1、新码年度率R2及桥接比率C。比较的是C×R1与R2，不能把计数替代人口风险率。
T133-02 [A1,A2] 若R1与C的估计误差可近似独立，修正率的相对方差包含旧年度率误差、C误差及乘积项。忽略其中一项会改变区间宽度。
T133-03 [A1] 原NCHS指南按计数100及以上和1至99采用不同近似，稀有病因的正态区间不保证覆盖准确；小计数需原刊附录的Poisson因子。
T133-04 [A3,A4] Wisconsin表中379是使用高精度桥接比率得到的描述性调整值，376是1999原始计数。两者的3例差不能直接等同真实死亡风险的年度变化。
T133-05 [A3,A1] Wisconsin州表区间只复算其公开公式。原NCHS完整联合Z公式还包括两个年份的计数变异。两者所估目标及误差来源不同，不能仅比较上下限判定哪一研究“证伪”。
T133-06 [A1,A2] 置信区间包含另一个年份的观察点值并不构成“95%概率没有真实变化”的频率学推断。等效性需要预先给定可接受差距及相应检验。
T133-07 [A1,A5] 全国1996双编码的比率能否运输到1998/1999某州，取决于旧码类别内的病因组合、年龄、地区、选择与编码执行规则；全美样本大不自动保证州级可运输。
T133-08 [A6,A8] 若分层比率不同，目标总体组成变化将改变聚合比率。固定全国比率用于地区或历史子群体必须报告分层支持与权重。
T133-09 [A5] 21,290条新版编码缺失可能与疑难病因、修订时间相关；总体0.9%缺失不保证某个罕见病因的桥接比率稳健。
T133-10 [A7] 基于时间序列估计突跳的Joinpoint-Jump与依赖外部桥接资料的Joinpoint-CR有不同的识别假设。两种估计不一致提示模型敏感性，不能仅据差异确定真实编码效应。
T133-11 [A7] 由时间序列估计的跳跃还可能吸收真实突发公共卫生变化、人口变化、趋势规格错误或测量断点。把模型拟合当作外部独立验证会混淆机制。
T133-12 [A8] 英国指南对于小幅或不显著比率采用置1政策属于明确的决策规则，会产生额外的模型选择不连续性。美国历史比率不应在未说明时套用该规则。
T133-13 [A1,A2] 年度死亡计数可在Poisson过程近似下估计波动；全体死亡登记的描述性计数本身不是随机抽样，推断必须明确随机过程与人口暴露量假设。
T133-14 [A1,A2] 只给州级死亡计数而没有年度分母时，能作条件性“等暴露量计数”演示，不能报告经人口标准化的州级率检验。
T133-15 [A3,A5] 113互斥叶类与135显示层级以及同一死亡证明多病因字段会引发重复计数风险；跨年检验需固定唯一统计单位和编码版本。
T133-16 [综合推断] 个体层是死亡证明的编码与多病因信息，群体层是州别年龄构成，制度层是ICD及发布规则，历史层是编码断点与长期趋势；四层机制需分别审计，不由同一个调整系数全部解决。

## 三、8项算术、公式与反例审计

E133-01 [官方初步计数复算] 21,258/17,791 = 1.1948738126；317×该比率=378.7749986，按整数为379；317×州表显示的1.19=377.23，按整数为377。显示舍入差2例，来源为A3/A4。
E133-02 [州表原样复算] 1.19×0.0042×1.96×379=3.71271432，故379±3.71271432得到375.2873至382.7127，与州表一致。这只是对州表算法的重放。
E133-03 [比率误差单独传播] 若SE(C)=0.0042为绝对标准误，固定1998计数x=317，则1.96×x×SE(C)=2.609544。以未舍入修正计数378.775为中心，区间约376.165至381.385；该区间不包含年度计数波动。
E133-04 [原NCHS联合公式代数] 假设两年度同等人口暴露、独立Poisson计数X=317和Y=376、独立桥接估计C，且SE(C)=0.0042，Var(CX)≈C²×317+317²×SE(C)²+317×SE(C)²，约454.367，SE(CX)≈21.3159，近似95%范围336.996至420.554。该模型假设仅用于方法演示，不能冒充真实州级死亡率置信区间。
E133-05 [联合差异检验] 以上相同人工统计假设下，C×317−376≈2.775，SE差异≈sqrt(454.367+376)=28.8161，z≈0.0963；近似差异95%范围为−53.705至59.255。未检验州级真实人口暴露与最终桥接权重，故不报告州级显著性结论。
E133-06 [运输敏感性] 设州真实桥接比率C_state=C_national×(1+δ)。δ=−5%,−2.5%,0,+2.5%,+5%时，1998调整计数依次约359.836、369.306、378.775、388.244、397.714；对应1999−调整值为+16.164、+6.694、−2.775、−12.244、−21.714。仅约−0.7326%的相对偏移就使1998与1999的调整计数比较方向翻转，δ取值为人工情景而非已估计的州别误差。
E133-07 [竞争模型原刊结果核对] A7公开原文检索段所报败血症Joinpoint-Jump估计1.2542（SE0.032）与外部桥接1.1949（SE0.0042）相差0.0593，约为后者的4.96%。两估计来自不同目标与假设，且该文未由本项目逐页重算，不能直接解释成“州比率偏差4.96%”。
E133-08 [不可识别反例] 保持州观察计数(317,376)不变：若州桥接C_state=1.1949，1998调整约379；若C_state=1.05，1998调整约333。两种机制与同一观察计数相容，后者对应明显不同的跨期差。没有州级桥接验证或额外约束，观察计数不能识别哪个世界成立。

## 四、竞争解释、验证清单与证据边界

竞争解释：真实风险变动、人口年龄构成、死亡证明填写、编码规则、病因组合、诊断习惯、登记质量、版本变更、模型趋势设定及抽样/缺失。NCHS比率校正与Joinpoint-Jump的冲突是方法比较线索，尚无本项目独立历史因果结论。

未来验证：取得2004最终XLS字节并核SHA、工作表、113类与父子层级；核对最终SE和1996缺失权重；取得Wisconsin 1998/1999州人口暴露与年龄分层死亡率；检验州别双编码可运输性、分层共支持、趋势模型的预断点拟合、不同跳跃估计与负对照；预注册敏感性δ及等效性阈值。严禁把固定比例调整当成确定性历史因果修复。

边界：本轮新增独立真实微观记录复算0、独立因果估计0、前瞻预测0、R系列E1/E2/E3新增均0。A1/A2原始指南公式已直接审读并经图像核对，E133-04至08为项目自行构造的统计条件与反例；不将其当作NCHS发布的Wisconsin正式检验。C006和D002只读，不开发个人产品，不使用个人敏感资料，不新增费用，不运行CI。

下一专题TH134：若最终XLS仍受阻，转向多地区历史死亡率与人口暴露量的公开官方表，建立分层桥接的最小可运输验证设计；取得原始XLS时优先完整113类工作表审计。
