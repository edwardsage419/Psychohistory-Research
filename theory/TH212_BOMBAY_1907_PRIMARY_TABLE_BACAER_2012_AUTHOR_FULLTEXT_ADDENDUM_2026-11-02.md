# TH212补记：1907年孟买鼠疫原始周表与2012年Bacaër作者全文

track: theory
subflow: main
run_date: 2026-11-02 (Asia/Singapore)
target_key: (theory,KermackMcKendrick1927+Bombay1907+ Bacaer2012,1907-primary-scan+2012-author-french-fulltext,original-weekly-denominator-and-parameter-identifiability)
status: COMPLETE_BOUNDED_PRIMARY_TABLE_READING; COMPLETE_CONSTRUCTIVE_IDENTIFIABILITY_AUDIT; PARTIAL_FORMAL_ERRATUM; NOT_RUN_HISTORICAL_CAUSAL_REESTIMATION
evidence_scope: ORIGINAL_1907_PAGE_IMAGES; AUTHOR_HOSTED_FRENCH_2012_FULLTEXT; EXACT_SYNTHETIC_FRACTIONS; NO_REAL_DATA_REESTIMATION; NO_R_E1_E2_E3_UPGRADE
ci_status: NOT_RUN
billing_checked: NO_PAID_ACTION; ACCOUNT_BILLING_NOT_VERIFIED

## 1 原始资料和实际阅读范围

[A] Advisory Committee on Plague Investigations in India (1907), “XXII. The Epidemiological Observations Made by the Commission in Bombay City”, *Journal of Hygiene* 7(6):724至798, DOI 10.1017/S0022172400033684。直接目视阅读PMC保存的原刊图像印刷页752、753、754、794、795，另目视Chart III插页及Table XXIV的p796图像。原刊完整目录及原始影像入口：https://pmc.ncbi.nlm.nih.gov/articles/PMC2236259/ 。本轮仅指定页直接审读，其他页未系统阅读。PMC影像用于研究查看，没有复制到仓库。

[A] Nicolas Bacaër (2012), “The Model of Kermack and McKendrick for the Plague Epidemic in Bombay and the Type Reproduction Number with Seasonality”, *Journal of Mathematical Biology* 64:403至422, DOI 10.1007/s00285-011-0417-5。直接阅读作者机构网站提供的**法文全文版本**“Le modèle de Kermack et McKendrick pour la peste à Bombay et la reproductivité d'un type avec saisonnalité”，第2、3、4、6、7节，含公式1至10、16至19及表1、表2：https://ummisco.pages.ird.fr/france/bacaer/2012JMB2.html 。该版本由作者提供，与英文正式刊本的逐式同一性未独立核验。此前TH212仅阅读正式英文摘要，此处为独立原作者全文增量。2012论文在本文中属于后来的理论和历史资料解释，不等于1907年原始观察。

[B] 1908年委员会“XXXI. On the seasonal prevalence of plague in India”，*Journal of Hygiene* 8(2):266至301，DOI 10.1017/S0022172400003314，https://pmc.ncbi.nlm.nih.gov/articles/PMC2167146/；1912年“XLIX. Statistics of the occurrence of plague in man and rats in Bombay, 1907至11”，*Journal of Hygiene* 12:221至226，https://pmc.ncbi.nlm.nih.gov/articles/PMC2167442/ 。仅核验原刊书目及影像入口，本轮未逐页阅读，不将它们计作已复核的跨年度数据。

## 2 1907年原始表提供的独立证据及口径限制

1907年原刊p753 Table IX列出1905年10月至1906年9月孟买逐周的“plague mortality”以及两类鼠感染指数。直接目视读得：1906年3月25日至31日人类死亡779，4月15日至21日870，4月22日至28日925，4月29日至5月5日802，5月6日至12日578。以上为**原刊表内读数**，非独立数据库重算。1927年曲线拟合峰值890每周，与p753的925不是同一数值；不能将拟合峰值当作原始观察最大值。1907原刊Chart III另显示两类鼠疫情与人类死亡的时间曲线，图像可见但没有逐点数字化。

p752说明孟买全市与分区的时间分组及校正处理不同，Table IX鼠感染列是对七天周进行校正的指数，不能直接当作捕获感染鼠的原始只数。p794 Appendix II说明其相关分析使用68个周段和Table XXIV的原始鼠检验数，短周按六天校正。**Table IX的感染指数、Table XXIV的鼠只数和人类死亡数具有不同分母和处理方法。**

p754作者从原刊曲线提出decumanus鼠疫情平均比rattus提前约十天，属于同一城市的时间顺序描述。p795的历史作者统计报告，同周人类疫情与rattus相关约0.8801，与decumanus约0.7481，两鼠种相关约0.945；在控制rattus后，人类与decumanus的偏相关被报告为负约0.538。p795同时明确其统计解释依赖诊断准确和捕鼠活动均匀等假设。上述相关值只转述原刊，没有独立重新计算，也不能单独识别鼠种、鼠蚤、温度或人群迁移的因果贡献。

## 3 2012作者全文对1927公式疑点的独立支持

Bacaër法文全文第2节由Riccati近似写出 dz/dt≈A sech²(Bt−φ)，其中 Q²=(kx₀/l−1)²+2x₀y₀k²/l²，A=l³Q²/(2x₀k²)，B=lQ/2。这里A明确包含Q²。与TH212此前从1927年式(30)求导得到的l³(−q)/(2κ²x₀)一致，支持1927年p714式(31)印刷为sqrt(−q)的内部不一致判断。**2012年作者全文使用一致系数，不等于出版社正式发布过1927年勘误**。正式勘误状态仍PARTIAL。

第3节说明拟合曲线只有(A,B,φ)三项可观察形状参数，而原始常数率模型有(x₀,y₀,k,l)四项未知。作者给出在y₀分别固定为1、2、3时，相同拟合曲线对应不同x₀及平均感染期的例子，原作者表1列x₀约57368、35439、28202，感染期约1.6、3.0、4.3天。此为作者原文模型反推，尚未以历史底层数据独立复算。第4节引入鼠、蚤、人类及季节温度传递模型，明确K、ω、π₀等参数经过手动调节拟合，未完成独立样本外识别。第7节强调风险人口分母N的不确定性。原始曲线匹配不唯一，季节性与人口耗竭的相对因果份额仍需外部设计。

## 4 新增严格构造性不可识别反例

对Bacaër第2节的参数映射进行独立精确代数检查。设A=B=1，tanh(φ)=1/2。取R=kx₀/l=2，则(x₀,y₀,k,l)=(2,3/2,1,1)，Q=2。取R=3，则(x₀,y₀,k,l)=(9/4,9/2,2/3,1/2)，Q=4。两组都满足Q²=(R−1)²+2Ry₀/x₀，并严格给出相同的(A,B,tanhφ)=(1,1,1/2)。计算使用Python标准库Fraction，两个世界的Q²、A、B、tanhφ共8项精确断言全部PASS。

结论严格限定：**仅凭同一条近似sech²曲线的三个形状参数，四个原始参数不能唯一恢复。** 人工参数包含非整数y₀，属于代数反例；若附加真实人口整数、感染期、暴露范围等约束，识别集合会改变。此结果不能直接作为1906年真实流行参数或历史因果验证。

## 5 竞争解释、四层边界与未完成

1907年原刊直接观察人类死亡、鼠疫情及周序；1927年以常参数人类隔室模型作粗略拟合；Bacaër2012用季节温度和鼠蚤宿主模型给出竞争解释。观察口径、时间先后、气温共变、鼠蚤生理机制、人口迁移及诊断质量必须分别记录。1907年统计相关不证明2012年季节模型唯一正确，2012年手动拟合亦不排除其他竞争机制。

理论覆盖在TH212内补强：早期印度城市公共卫生原始统计、观察分母、宿主时间先后、参数欠识别。可供后续R理论问题参考的仅为“观察层数据口径与潜在机制之间的识别限制”，没有把疾病动力学融合到社会历史模型。1908年和1912年跨年度原始表逐页阅读、1927正式勘误检索终局、英文2012正式版逐式比较、原始周序数字化、真实因果估计、历史预测均NOT_RUN或PARTIAL。没有R E1/E2/E3及MARKET升级。

C010已于2026年11月2日完成，D003已于2026年第45周的11月2日完成，本轮只读。R272最新main记录的固定来源原生重放仅为内部非盲人工E1，真实外部复现为false；Codex开放PR未合并不计入main。R073及PESEN v0.1冻结不变。

下一步优先阅读1908年p283至285及1912年p222至226原始图表，核对季节性机制和跨年度口径；若来源不可用，转向其他弱覆盖领域。全R完成后才统一分类及有条件熔炼。新增付费操作0，未触发CI，实际账户账单NOT_VERIFIED。
