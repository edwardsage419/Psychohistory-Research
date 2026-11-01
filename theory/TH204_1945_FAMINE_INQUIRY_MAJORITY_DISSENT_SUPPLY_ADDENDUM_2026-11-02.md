# TH204补记：1945年饥荒调查委员会原始报告中的粮食供给分歧

track: theory
subflow: primary_theory
run_date: 2026-11-02 (Asia/Singapore)
observed_head: 6ba6365cdca1d50de1b701fbcb599c6f775ce84f
target_key: (theory,India-Famine-Inquiry-Commission-1945-Report-on-Bengal,1945-original-report-majority-and-Husain-minute,1943-rice-carryover-and-shortage-estimand-disagreement)
status: COMPLETE_BOUNDED_PRIMARY_SOURCE_AUDIT; HISTORICAL_CAUSAL_CONTEST_PARTIAL; NO_REAL_REESTIMATION

## 来源与实际阅读范围

[A原始官方报告] India, Famine Inquiry Commission (Woodhead Commission), *Report on Bengal* (1945), Manager of Publications, New Delhi。原报告目录、Chapter III pp12至15、Chapter XI p103指定段落、附录II pp202至203、210至213、Statement I p213及Statement IV p216、M. Afzal Husain独立意见 pp187至189。在线两段扫描原件： https://indiaofthepast.org/sites/indiaofthepast.org/files/pdf/1940s/bengalfamine/ficreportpart1.pdf 和 https://www.indiaofthepast.org/sites/indiaofthepast.org/files/pdf/1940s/bengalfamine/ficreportpart2.pdf 。原件书目与北孟加拉大学开放馆藏 https://ir.nbu.ac.in/handle/123456789/1939 交叉核对。直接读取扫描PDF可抽取文本，目视核对原印刷p14、p189、p212及p216表格；p15文字已读，截图抓取超时，故该页视觉核验PARTIAL。无DOI，稳定书目见 https://books.google.com/books/about/Report_on_Bengal.html?id=QIAj0gEACAAJ 。第三方PDF再分发许可未核，不向仓库复制原件或长篇原文。

## 独立增量：同一1945年一手报告内部已有正式分歧

1. 委员会多数在Chapter III p15与Appendix II pp211至212估计1943年当期供给约43周，年初结转约6周，总供给49周，按52周需求推算绝对短缺约3周。Husain签署报告但保留单独意见（报告p179标注），在p189直接质疑年初仍有6周结转的假设，提出1942年底结转近零，估计1943年1至9月aman可用量约550万吨，9个月需求按每人每周3 seers为670万吨，按3.2 seers为720万吨；其文字认为短缺至少150万吨。两种解释同在原始官方报告，不能将“委员会估计”表述为无异议单值。
2. Appendix II p216 Statement IV列1943年当期供给836万吨、假设需求1014万吨，故当期缺口178万吨。若直接加多数估计结转116万吨，剩余缺口为62万吨；Husain p189转述多数估计为58万吨，差4万吨。此差来自已四舍五入的周数/吨数口径的可能性较大，但原文未给出能唯一消除差异的未舍入计算。应标注ROUNDING_OR_DEFINITION_UNRESOLVED，不能将62万吨改写成58万吨或断言造假。
3. Husain的9个月需求与多数的全年需求并非相同估计对象。550万吨与670万吨的算术差为120万吨，与720万吨差为170万吨；其“至少150万吨”不能由较低的3 seers情景直接推出，需补充更高最低配给标准、时间/库存或其他假设。没有取得能证明150万吨为严格下界的独立依据。
4. Appendix II p212承认没有直接的历年结转库存数据，1943年6月粮食调查推算106万吨短缺，报告又指出持有人低报/隐匿库存及按已核库存增加25%的假设未获独立校准。结转量、统计需求、种子扣除、作物年度、替代粮与进口到达月份会共同影响供给结论。p189独立意见指出实际进口约65万吨且到达时间不均；到货时点与全年总量不能混为一项处理。
5. Chapter III pp12至13与Chapter XI p103同时承认粮食实物供给和价格/购买力/分配均影响饥荒。1945年原始材料的内部争论增强了Sen1981与Tauger2003竞争解释的历史背景，但既不能独立证明Sen的因果结论，也不能独立证成Tauger的灾害产量估计。该调查委员会成立于1944年，回溯1942至1944年战争与灾害，行政记录及证词具有选择性和测量误差。

## 精确算术与可证伪要求

Python Decimal 9项人工断言PASS：10.14−8.36=1.78；1.78−1.16=0.62；0.62−0.58=0.04；6.7−5.5=1.2；7.2−5.5=1.7；43+6=49；52−49=3及两项周均需求下界比较。该测试仅核对所抄历史表值与算术，非独立历史数据复算。

未来历史可证伪检查：获得原始产量/库存/进出口逐月记录及其统计修订版，分别冻结作物年与日历年、稻谷折米、种子扣除、人口基数、实际最低消费口径，核对1942年底实物结转能否支撑6周假设；将6月库存抽查的漏报区间与逐月粮食到货及市场价格对齐。1945报告中的两种估计均应保留。不能用1943年的总供给差异单独识别饥荒死亡的因果机制。

证据：1945原始官方历史调查及意见分歧，非随机实验；Tauger2003全文、Sen1981历史原表独立复算、原始粮食逐月数据和独立历史因果识别NOT_RUN。原始报告其余章节及附录大部分未读。

覆盖：补强殖民时期南亚粮食统计、历史档案内部异议、时间口径及行政测量不确定性；沿用TH204，不新增TH编号，不进入R模型复算、统一分类或熔炼。

C_today: C010 COMPLETE 2026-11-02, read_only
D_week: D003 COMPLETE 2026-W45, actual 2026-11-02, read_only
R_status: R344归档有限人工E1，E2/E3未建立；R073/PESEN v0.1冻结；本轮R E1/E2/E3新增0
CI: NOT_RUN
billing: new_paid_operations=0; actual_billing=NOT_VERIFIED
next: 查原始1942年末库存及1943年月度粮食到货统计，比较Sen与Tauger所用统计修订；保留同源官方报告的多数/少数意见差异。
