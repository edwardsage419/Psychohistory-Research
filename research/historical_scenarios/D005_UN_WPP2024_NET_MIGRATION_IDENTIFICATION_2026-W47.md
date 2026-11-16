# D005 候选：联合国WPP2024净迁移测量与长期情景识别边界

track: theory
subflow: D
run_date: 2026-11-16 (Asia/Singapore)
week: 2026-W47
observed_head_before_write: 980ee6b638f49bf4d4d6a2104de43fff898fbeb5
target_key: (theory-D,UN-DESA-WPP2024-Methodology,2024,net-migration-inflow-outflow-nonidentification-and-projection)
status: PARTIAL; PRIMARY_OFFICIAL_METHOD_EXCERPT; CONSTRUCTIVE_IDENTIFICATION_ARGUMENT; NO_HISTORICAL_VALIDATION

## 原始来源与实际阅读范围
United Nations, Department of Economic and Social Affairs, Population Division (2024), *World Population Prospects 2024: Methodology of the United Nations Population Estimates and Projections*. 联合国官方方法报告，未见该报告独立 DOI，稳定官方 PDF：https://population.un.org/wpp/assets/Files/WPP2024_Methodology-Report_Final.pdf 。
2026-11-16 实际核对可检索的官方报告第26页有关净迁移的段落，以及第47页 Section E, “Projecting international migration in the medium scenario” 的方法描述和步骤1。该范围是官方原始报告的可检索正文节录，尚未逐页核验PDF扫描版全部公式、图表、其余步骤及附录。

## 直接来源命题
第26页：WPP2024使用净国际迁移量，通常没有可独立分解为移入和移出两项的观测资料。由于多数国家迁移流入/流出资料不足，某些国家的净迁移量由两次普查人口变动扣除自然增长及覆盖/质量调整后的残差估计。故净迁移序列有时含人口普查、出生死亡估计及调整的复合误差，不能将其自动视作独立直接测得的跨境流量。
第47页：国际迁移相较其他人口组成部分具有较高不确定性，部分国家的迁移方向可能迅速反转。2024版首次在中位方案中使用基于Azose与Raftery方法的贝叶斯分层概率净迁移率预测，历史输入为1950至2023年国家年度净迁移率，模型使用一阶自回归结构；该预测为条件情景，不是确定性事件预言。

## 新的构造性不可识别性论证
令 I_t 为移入，E_t 为移出，N_t=I_t-E_t。观察N_t=0时，(I_t,E_t)=(0,0)与(100000,100000)都满足观测；净值无法识别双向流动规模。更一般地，任意非负k使(I_t+k,E_t+k)产生相同N_t。仅有净迁移的历史时间序列，即使长度任意增加，仍不能在缺少额外约束时恢复总流量 I_t+E_t。此为代数构造性反例，非人口行为实验。

若人口存量满足 P_{t+1}-P_t=B_t-D_t+N_t+u_t，则用残差计算的净迁移估计为 Nhat_t=ΔP_t-Bhat_t+Dhat_t-uhat_t。出生、死亡、人口覆盖误差和残差迁移的误差可能混合，不能把迁移估计与上述输入视为独立测量后再作因果归因。

## 竞争解释、可检验条件与适用边界
竞争解释：真实双向高周转但净流量低；真实低周转；人口普查漏计、出生死亡统计偏差；边境政策或冲突冲击；长期经济与人口年龄结构变化。区分这些解释需独立流入/流出记录、登记或抽样覆盖校准、年龄性别分层、政策时点与外部冲击证据。
历史覆盖：WPP2024方法中的历史输入1950至2023，覆盖多个国家；研究仅核查方法说明，未下载或分析国家级原始数列。未来至2100年属于模型投影，不能以模型区间直接解释真实世界预测准确率。
可证伪/诊断：比较有高质量独立流入和流出登记的国家净值与人口残差法；预先固定年份、行政边界、年龄性别口径；对历史修订、人口普查覆盖、战争及政策结构断点做敏感性分析；采用时间外验证评价概率区间校准。仅凭净值不能检验双向流动机制。
局限：第47页后续9步及参数细节、国家原始数据、跨国测量可比性、实际样本外性能尚未审读或复算。不可宣称完成D005科学验收、历史预测验证或R证据升级。

## 协作与状态
此前D004为2026-W46的EIA电力容量专题，已读其跨表残差与舍入上界审计；本次选题为2026-W47独立人口迁移测量问题，避免重做D004。C014已在2026-11-08归档Robins等(2000)关于IPTW正值性与失访的原著研究；不再重建C014。
C当日：未核实2026-11-16有正式合格记录，PARTIAL。
D本周：本文件是第47周新专题候选的原始方法阅读和识别论证，PARTIAL，后续须完成更多原始页章与竞争解释方可判断合格完成。
Tests: NOT_RUN. CI: NOT_RUN. Billing: no paid API, cloud, CI or purchase triggered; account charges NOT_VERIFIED. R073/PESEN v0.1 frozen; R E1/E2/E3 and MARKET unchanged.
Next: 核查WPP2024 Section E其余预测步骤和人口残差法限制，并找独立登记数据/竞争论文进行比较；不得从净迁移推断移民总流量。

## 2026-11-16 后续原著增量：Section II.E pp.48–53（官方印刷页）
来源仍为同一份UN DESA 2024官方方法报告，PDF物理页56–61；本次直接阅读Section II.E步骤2至10、Table II.3 A/B/C、II.E.2。任务键沿用D005，不新增编号。

1. **参考期与专家约束（印刷pp.48–50）**：步骤2对部分国家更改1950–2023默认拟合期；Table II.3.A列42个国家/地区的特定参考期（如德国1950–2021、乌克兰2000–2021）。步骤3以专家确定的基线恢复目标年、难民回流比例及插值调整概率轨迹；Table II.3.B列28项目标年。步骤5又对部分国家的长期净迁移率加入Table II.3.C的32项人工目标。这些为**条件性模型假设**，不能被当作独立观测的未来迁移事实。表格项数是本次按原表序号阅读得到，尚未与原始机器表复核。
2. **模拟和全球守恒（印刷pp.50–52）**：步骤4/7输出每国2000条轨迹；步骤8从率转换为人数时尚未保证全球净迁移为零；步骤9对每年每条轨迹以人口比例再分配残差，使全球净迁移人数合计为零，且按非劳工国、劳工国、全部国家三阶段调整；步骤10用于最终人口投影。**新识别边界**：某国调整后净迁移人数包含跨国平衡操作的贡献，不能直接解释为该国独立估计的原始流量。该守恒属于模型会计约束，不构成历史准确率证据。
3. **净值拆分的关键补充（印刷p.53）**：II.E.2明确2024版为按年龄性别分配净迁移，先把净值分解为移入/移出人数，再使用Rogers–Castro模型；迁移率、峰值年龄、性别比例等参数利用最近观测分布、优化及Abel & Cohen (2022)等来源估计。**对先前D005的限定**：本报告确实生成移入与移出两个模型量，但仅凭净值依然无法唯一识别真实双向流量；模型拆分依赖额外参数、来源和结构假设。不能将模拟拆分量误标为独立登记观测。
4. **新增构造性反例**：两国原始净迁移估计分别为+120和−100，全球残差+20。若按人口各半平衡，两国调整后变成+110与−110。第二国的−110含−10的全球守恒分摊。此例仅演示所述按人口再分配原则，不声称复现UN具体三阶段算法或真实国家数据。
5. **可证伪/敏感性检查**：固定各国参考期、Table II.3目标和原始轨迹，比较平衡前后各国净值差异；分别更改专家恢复年份和长期目标，检查区间宽度及跨国相关性；对有独立移入/移出登记的国家比较模型拆分误差。尚未取得国家级原始轨迹、登记资料或开展样本外检验。预测校准、模型参数和许可细节仍待核实。

状态：D005 PARTIAL；原始报告Section II.E pp.48–53指定内容阅读COMPLETE；独立数据验证NOT_RUN；R验收关闭0；C当日合格归档仍未核实。未触发CI/收费资源。此记录为理论D轨补强，不构成R轨科学验收。


## 2026-11-16 独立统计机构口径审查：Eurostat 与 OECD（原始官方方法网页）
本次直接阅读公开官方方法网页，不涉及国家级原始数据下载或计算。来源：Eurostat, *International migration and citizenship: Methodology*, https://ec.europa.eu/eurostat/web/migration-asylum/international-migration-citizenship/methodology ；Eurostat, *Information on data*, https://ec.europa.eu/eurostat/en/web/migration-asylum/international-migration-citizenship/information-data ；OECD, *International Migration Outlook 2024*, Statistical Annex, https://www.oecd.org/en/publications/international-migration-outlook-2024_50b0353e-en/full-report/statistical-annex_dab396da.html 。阅读范围为Eurostat定义、数据来源与两套年度数据收集说明，以及OECD附录中美国、瑞典、瑞士等国的来源和口径注释。均为官方方法说明，非独立历史预测实验。

1. Eurostat入境与出境通常以在另一国家建立或终止至少12个月的通常居住地为口径。国家统计机构可用人口登记、税务、医保、普查、镜像流量、抽样等不同来源。统一定义无法自动消除来源差异与登记遗漏。
2. Eurostat区分人口平衡表（demo_gind）中的“净迁移加统计调整”与更详细的国际移入/移出流量采集。前者包含统计调整，不能直接以其数值等同于详细流量表的移入减移出，差额也不能未经核查归因于迁移行为。
3. OECD附录列明美国永久迁移采用合法永久居民身份，包括已在美国境内转换身份者，且按财政年度；瑞典以至少一年居留意图及登记为主，瑞士部分流出含行政更正。这些与Eurostat通常居住地口径以及UN WPP人口净迁移估计不完全同构。直接跨表比较存在事件定义、年份、身份与行政更正的混杂。

构造性口径反例：同一人在t年已居住于美国，t+1年转为永久居民。OECD美国永久居民批准数可于t+1年增加1，但当年跨境实际入境人数增加0。此为定义推导，不代表对真实行政记录的单人核查。故“OECD永久移入数减Eurostat移出数等于UN净迁移”没有一般会计恒等式基础。

新的比较准入条件：预先固定国家、日历年/财政年、居留时长、国籍/出生地、境内身份转换、难民/临时迁移、行政注销、人口普查修订及统计调整；对每组指标逐项证明相同事件总体和时间口径后才可做数量差或误差比较。若无法建立映射，标记NONCOMPARABLE，不以相关系数或残差当作UN模型错误。真实国家级对照、独立登记核验和样本外检验均NOT_RUN。D005继续PARTIAL，R科学验收关闭0，C当日完成仍待核验，CI NOT_RUN，未调用收费资源。
