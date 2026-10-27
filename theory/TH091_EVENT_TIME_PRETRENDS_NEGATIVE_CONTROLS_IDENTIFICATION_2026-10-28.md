# TH091 历史事件时间对齐、处理前趋势与负对照的共同识别边界

日期及非中文来源检索日期：2026-10-28（Asia/Singapore）。状态：THEORY_NOTE_BOUNDED。承接TH090。仅理论学习、原始资料审读、人工识别反例；不执行R系列拟合，不接入个人数据，不开发产品，不使用收费服务。

## 1. 原始书目与证据等级

A1【作者开放原文HTML直接审读】Sun, L. & Abraham, S. (2021). “Estimating dynamic treatment effects in event studies with heterogeneous treatment effects.” Journal of Econometrics 225(2):175–199. DOI https://doi.org/10.1016/j.jeconom.2020.09.006 。作者2020-09-22版 https://arxiv.org/html/1804.05785v2 。审读§2.2识别假设、§3.4动态系数、§3.7预趋势污染、§4交互加权。作者稿与刊版未逐字校勘。

A2【作者开放原文HTML直接审读】Lipsitch, M., Tchetgen Tchetgen, E. & Cohen, T. (2010). “Negative Controls: A Tool for Detecting Confounding and Bias in Observational Studies.” Epidemiology 21(3):383–388. DOI https://doi.org/10.1097/EDE.0b013e3181d61eeb 。全文 https://pmc.ncbi.nlm.nih.gov/articles/PMC3053408/ 。审读负对照暴露与结果、U-comparability、选择和测量误差的诊断边界。

A3【正式开放原刊HTML直接审读】Arnold, B. F., Ercumen, A., Benjamin-Chung, J. & Colford, J. M. (2016). “Brief Report: Negative Controls to Detect Selection Bias and Measurement Bias in Epidemiologic Studies.” Epidemiology 27(5):637–641. DOI https://doi.org/10.1097/EDE.0000000000000504 。全文 https://pmc.ncbi.nlm.nih.gov/articles/PMC4969055/ 。审读选择偏差图1、测量偏差图2和讨论。

B1【MIT机构摘要，作者草稿已定位但未逐页审】Rambachan, A. & Roth, J. (2023). “A More Credible Approach to Parallel Trends.” Review of Economic Studies 90(5):2555–2591. DOI https://doi.org/10.1093/restud/rdad018 。摘要 https://economics.mit.edu/research/publications/more-credible-approach-parallel-trends ，作者草稿 https://asheshrambachan.github.io/assets/files/hpt-draft.pdf 。仅据摘要记录限制平行趋势违背后的部分识别。

B2【正式原刊摘要与书目】Roth, J. (2022). “Pretest with Caution: Event-Study Estimates after Testing for Parallel Trends.” American Economic Review: Insights 4(3):305–322. DOI https://doi.org/10.1257/aeri.20210236 。书目及摘要 https://ideas.repec.org/a/aea/aerins/v4y2022i3p305-22.html 。正文未审。

B3【正式原刊摘要与开放作者稿书目】Callaway, B. & Sant’Anna, P. H. C. (2021). “Difference-in-Differences with Multiple Time Periods.” Journal of Econometrics 225(2):200–230. DOI https://doi.org/10.1016/j.jeconom.2020.12.001 。作者稿 https://arxiv.org/abs/1803.09015 。本轮仅核验摘要，估计器证明未审。

## 2. 十六项条件性命题、前提及竞争解释

T01【A1】历史事件的公告、立法、实施、实际暴露、档案登记日期可能分离。验证需分别建立原始时间锚点；竞争解释为公告引发提前反应。
T02【A1】平行趋势涉及未处理潜在结果的变化。处理前观察趋势相近仍可出现处理后反事实分叉；需考虑共同冲击与选择。
T03【A1】无预期效应要求处理前结果不因未来处理改变。预告、迁移、备货、谈判可能违反该假设。
T04【A1】分批处理下传统双向固定效应事件研究的动态系数可能混入其他相对期的异质效应。
T05【A1】传统处理前系数非零可由污染产生，系数为零也可能掩盖真实趋势差异；需审计规格和权重。
T06【A1】队列与相对期交互加权估计可处理A1指出的跨期污染，仍要求平行趋势、无预期及适用对照组。
T07【B3摘要】分组分期处理效应及聚合方式会改变目标参数；估计公式和推断条件需后续全文校勘。
T08【B2摘要】处理前趋势检验可能低功效，先检验再筛选模型可能影响估计与区间覆盖率。
T09【B1摘要】限制处理后平行趋势违背幅度可得部分识别区间；限制的历史依据与敏感性须公开。
T10【A2】负对照结果须无目标处理的因果作用，且尽可能共享目标结果的相关偏差来源；负对照暴露有对应条件。
T11【A2】负对照出现关联提示偏差风险，无法单凭此确定偏差种类或大小；无关联亦不能排除所有混杂。
T12【A3】差异性入档与测量误差可能形成假关联；负对照因果图错设时诊断会失效。
T13【项目推断】处理时间若仅知区间，固定一个中点可能把真实处理后结果误标为处理前结果；应对可行日期做敏感性分析。
T14【项目推断】按年记录的处理指示变量可混合不同月数的实际暴露；需对照结果形成的时间分辨率。
T15【项目推断】共同冲击、预期行为、队列异质性、日期错置和测量制度变化可形成相似事件图形；至少保留五种竞争机制。
T16【综合】负对照无异常、预趋势检验不显著、时间顺序合理仍不足以保证因果识别；需独立审查干扰、混杂与档案选择。

## 3. 九项人工数学及逻辑审计

E01【零效应与平行趋势】处理组t0=10,t1=12,t2=14；对照组8,10,12。t1到t2双重差分=(14−12)−(12−10)=0。
E02【观测等价】处理组前两期10,12，后期17；对照组8,10,12。观察双重差分为3。世界甲处理组未处理后期14、因果效应3；世界乙未处理后期17、因果效应0且存在组别特有冲击。观测完全相同。
E03【日期错置】真实执行t2、登记t3，t2真实效应+4。以登记日为事件，t2被误标为相对期−1，出现表面预趋势+4。
E04【真实预期】t1公告、t3实施；t2提前反应+2、t3执行效应+5。以实施为时点，t2确有处理前反应；以公告为时点，目标变为公告和执行的复合路径。
E05【原作公式代入】A1§3.7公式(24)在所有处理前CATT=0，CATT(1,0)=4、CATT(2,0)=0、CATT(1,1)=2时，处理前系数=0+(4−0)/2+2/2=3。仅代入作者特殊规格公式，未复算作者样本。
E06【负对照检测】U为0或1且各半，A=U、Y=U、N=U；干预A不改变Y和N，但观察中A与Y、A与N完全关联，N提示共同原因。
E07【负对照假阴性】U1与U2独立，A=U1、Y=U1、N=U2。A与N无关联，A与Y的观察关联仍由U1造成。
E08【趋势违背敏感性】观察双重差分3，若未处理趋势偏差δ∈[−2,2]，τ=3−δ∈[1,5]；若δ∈[−4,4]，τ∈[−1,7]。数值区间为人工假设。
E09【年度暴露剂量】假设每月效应累积+1且无滞后，1月执行年末累计12，12月执行累计1；年度处理标记均为1，暴露长度差11个月。

九项均为人工世界或原作公式代入。没有真实历史数据复算、独立因果估计、前瞻性预测或模型熔炼。

## 4. 四层联系、适用边界、未来验证清单

个体：预期、提前准备、政策接触时点、回忆误差。群体：不同处理队列、网络外溢、迁移和存续偏差。制度：公告、立法、拨款、执行、登记之间的时间差。历史：年代分辨率、历法转换、共同冲击、跨期指标变化和档案缺失。

候选验证顺序：①冻结处理、单位、结果、目标总体及事件时域；②记录公告、实施、实际暴露、登记四类时间及其不确定区间；③按队列绘制原始结果与对照组；④审查平行趋势、无预期、共同支持、干扰和档案存续；⑤对比TWFE与队列分期估计及权重；⑥检查预趋势检验功效和选择后推断；⑦按日期范围与趋势违背范围作敏感性分析；⑧预先指定负对照及其因果图；⑨公开竞争解释与不可识别结果。

未决问题：区间删失事件时间与分批处理的联合识别；公告效应与执行效应分离；结果依赖的档案选择如何影响负对照；网络干扰下队列效应的解释；跨时代测量等值失败后的部分识别。

## 5. C、D日历与归档边界

2026-10-28 C005已完成（Git blob c862a4704d45aa379ef1187ed750aa3c88f628d1）；2026-W44 D002已完成（Git blob b2556a008eca156222acd3f3b85caa50f85c5fac）。本轮只读。直接审读3份开放原作HTML重点章节，另核验3份原始摘要。成本增量0，未主动运行CI，未读取个人敏感资料。

下一候选TH092：政策公告与实际执行之间的预期效应、动态处理定义及历史干扰识别。
