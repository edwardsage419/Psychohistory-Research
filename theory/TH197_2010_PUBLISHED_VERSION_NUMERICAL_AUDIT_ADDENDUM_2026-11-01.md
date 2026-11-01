# TH197补记：Ostrom 2010正式发表版核验与灌溉案例数字内部不一致

track: theory
subflow: main
run_date: 2026-11-01 (Asia/Singapore)
source_access_date: 2026-11-01
target_key: (theory,Ostrom2010_AER100_3_641_672+Ostrom2009_Indiana_revised_draft,published-versus-draft-v1,rights_rules_and_irrigation_count_consistency)
baseline_main_before_write: ea8a3fe02b92c8230fbf6b4e59d0c89c82f4b3e2
status: COMPLETE_BOUNDED_SOURCE_VERIFICATION; PRIMARY_TANG_DENOMINATORS_OPEN
evidence_scope: PUBLISHED_PDF_DIRECT_PAGE_IMAGE; AUTHOR_DRAFT_DIRECT_PAGE_IMAGE; NONBLIND; PUBLISHED_AGGREGATE_ARITHMETIC_ONLY
r_e1_e2_e3_upgrade: NONE
ci_status: NOT_RUN
billing_checked: NOT_VERIFIED
new_paid_services: NONE

## 1. 文献身份与本轮实际阅读

[A，正式刊印版直接阅读] Elinor Ostrom (2010), “Beyond Markets and States: Polycentric Governance of Complex Economic Systems,” *American Economic Review* 100(3):641–672, DOI:10.1257/aer.100.3.641。出版社原始书目：https://www.aeaweb.org/articles?id=10.1257/aer.100.3.641 。大学网站公开的正式排版PDF：https://web.pdx.edu/~nwallace/EHP/OstromPolyGov.pdf 。本轮直接核验印刷页641至653的相关章节，655至658的实验、灌溉和森林段落；尤其PDF第10页（从1计）的印刷页650，用原始页面图像复核数字，排除纯HTML/PDF文本抽取错误。未通读正式版659至672的全部结论与书目，未做整篇逐字差异比对。

[B，2009年作者修订讲稿直接阅读] Elinor Ostrom (2009), Nobel Lecture revised draft, Indiana University Digital Library of the Commons，32页，封面注明DRAFT。https://dlc.dlib.indiana.edu/dlc/bitstreams/0a7a52e6-8cf0-42c3-ae20-776095e6fd1d/download 。本轮复核草稿PDF第11页（从1计，印刷页10）的灌溉数字，及草稿印刷页11至13的五类权利、七类规则与设计原则。草稿仅用于版本比对，不摘录版权正文。

[C，原始研究身份与待核数据] Shui-Yan Tang (1989), *Institutions and Collective Action in Irrigation Systems*, Indiana University原始博士论文馆藏摘要：https://dlc.dlib.indiana.edu/dlc/items/8da18e3f-143b-4fc3-9c75-06f4d1355596 。摘要确认47项深入案例研究，但没有给出本文所需各组分母。Ostrom2010引文指向Tang (1994:234)，该页原作尚未获得可逐页核验版本，不能由其他摘要代替。

## 2. 已确认的正式版本范围

正式版印刷页651至652直接保留五项产权权利：进入、提取、管理、排除、转让；七类规则：边界、位置、选择、信息、范围、聚合、收益。对应2009草稿印刷页11至12的分类及原作者报告的27种边界规则、112种选择规则均可在正式版找到。正式版印刷页653的设计原则表述亦与2009草稿第13页同一理论框架。正式版印刷页655附近的自选制裁实验90%最优收益，以及657至658页的229个灌溉系统和163处森林（76保护区、87其他），均可在正式版核对到作者陈述。

上述结果只说明选定命题在正式版仍出现，不能据此断言全部正文、表格和引用完全一致。90%、229、163均为原作者转述的上游研究结果，本项目未取得参与者或场址级数据复算。

## 3. 本轮真正新增的可复核数字问题

正式版印刷页650（大学公开PDF第10页，已直接查看页面图像）在同一段报告：
1. 灌溉系统总体47个。
2. 政府管理12个，其中高绩效 n=7，同时报告比例40%。
3. 农民管理25个，其中高绩效 n=18，同时报告超过70%。

人工精确算术核验：
47-(12+25)=10，已列出的两类共37个，尚有10个的分类、缺失或样本口径没有交代；
7/12=58.333...%，与同一句40%不一致；
18/25=72%，与超过70%的陈述相容。

2009作者修订稿印刷页10经原始页面图像核验，包含完全相同的47、12、7、40%、25、18数字组合。因此这一数字内部不一致在已核两个版本均存在，并非2010刊印新增，也非网页抽取误差。

**严格边界：**这里只确认文本数字之间的内部不一致。无法判定哪一个数字应修正，也不能断言上游Tang原始分析错误、治理理论被推翻或具体效果大小改变。可能存在子样本、缺失、分母转录、百分比转录或排版错误；目前均属未证实的解释。尤其不得把7/17近似41.2%作为真实分母，也不得把37直接视为实际分析样本。

## 4. 对理论和未来实证研究的影响

这一问题提示跨层治理研究中必须保存每一分析结果的分母、分类规则、缺失样本、绩效定义和研究版本。总体样本数与分组样本数不同，可能只是不同分析子集；没有清楚标注就无法独立重建统计结果。跨群体比较还须处理政府/农民管理的非随机选择、地理生态条件、规则执行、进入和退出选择。

四层关系：个体为使用者激励与绩效测量，群体为成员资格及共同治理，制度为管理权与实际规则，历史为灌溉系统存续、扩展样本及跨时期制度选择。当前仅建立测量审计要求，不构成统一分类或模型熔炼。

## 5. 测试、协作、开放事项

执行：Python标准库Fraction算术直接核对三项数值关系，原始PDF两版本各一页图像目视核验；无真人原始数据、无模型拟合、无历史因果估计、无预测检验。已阅读TH197研究笔记及TH072至TH074在索引中登记的相关范围，本次为非盲态原作版本补记，不另开TH198。

C：2026-11-01 C009已存在且只读核验。D：2026-W44 D002研究日期2026-10-26，已存在且只读核验。R：2026-11-01 07:45 UTC R336/R340 P0原生负例交接确认局部工程门，生产修复仍PARTIAL，R E1/E2/E3新增0；12个Codex PR仍OPEN，未合并证据不得当作main结论。R073及PESEN v0.1冻结保持。

后续首要核验Tang (1994:234)的原始表、47个案例的分母口径、政府与农民管理分类是否穷尽；取得合法原文后逐格审计。其次回到政治权力与行政可读性原著。TH187正式2022刊文符号、Kirby2017 S7逐格差异、Segovia-Martín2020勘误图像仍OPEN。无新增费用，无CI触发，账户计费未独立核验。
