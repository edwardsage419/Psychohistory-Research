# TH212补记：1908年鼠疫温度实验与1912年行政统计的证据层级

track: theory
subflow: main
run_date: 2026-11-02 (Asia/Singapore)
observed_main_head_before_write: 093492d465c3498071f439fea9e54ef350ae58d5
target_key: (theory,BombayPlagueCommission1908+BombayAdministration1912,1908-published-original+1912-colonial-administration-original,temperature-transmission-and-geographic-aggregation-identification)
status: COMPLETE_BOUNDED_ORIGINAL_TEXT_READING; COMPLETE_EXACT_ARITHMETIC; PARTIAL_PAGE_IMAGE_AND_1912_COMMISSION_TABLE; NOT_RUN_HISTORICAL_CAUSAL_VALIDATION
evidence_scope: 1908_PUBLISHED_PDF_EXTRACTED_TEXT; 1912_BRITISH_LIBRARY_ARCHIVAL_OCR; ORIGINAL_ANIMAL_EXPERIMENT_COUNTS; NO_HISTORICAL_REESTIMATION; NO_R_E1_E2_E3_UPGRADE
ci_status: NOT_RUN
billing_checked: NO_PAID_ACTION; ACCOUNT_BILLING_NOT_VERIFIED

## 1 来源、版本和实际阅读

[A] Advisory Committee on Plague Investigations in India (1908), “XXXI. On the seasonal prevalence of plague in India”, *Journal of Hygiene* 8(2):266至301, DOI 10.1017/S0022172400003314。直接读取Cambridge原刊PDF文字层，重点印刷页267至268、273至279、282至285及299至301；本轮未逐页检查全部图表。来源：https://www.cambridge.org/core/services/aop-cambridge-core/content/view/A4CF58A9FFFF07650E1D8DD2E9ECD2A2/S0022172400003314a.pdf/xxxi_on_the_seasonal_prevalence_of_plague_in_india.pdf 。PDF页面截图请求超时/503，表III的排版列对齐尚未通过影像独立确认，须将此限制作显式保留。

[A] Government of Bombay (1912), *Report on the Administration of the Bombay Presidency for the Year 1911–1912*, Chapter VI, printed p203, section “Epidemic Diseases: Plague”, British Library India Office Records IOR/V/10/314/5, digitised Qatar Digital Library folio 406r. 直接阅读QDL提供的原始报告机器转录文字，来源：https://www.qdl.qa/en/archive/81055/vdc_100146764806.0x000013 。QDL声明自动转录可能有错，未目视核验该页原始图像；模糊数值不纳入定量结论。该行政年度截止1912年3月31日，地理范围为Bombay Presidency，文内另列Bombay City及Karachi。

[B] Advisory Committee (1912), “XLIX. Statistics of the occurrence of plague in man and rats in Bombay, 1907–11”, *Journal of Hygiene* 12 Supplement:221至226, PMID 20474511, PMCID PMC2167442, https://pmc.ncbi.nlm.nih.gov/articles/PMC2167442/ 。本轮只确认书目与开放原刊入口；原刊pp222至226的表尚未直接读取。绝不将行政报告误称为这篇委员会论文的直接复核。

[C] Nicolas Bacaër (2012), “Le modèle de Kermack et McKendrick pour la peste à Bombay et la reproductivité d'un type avec saisonnalité”, 作者机构公开法文全文§4及Table 2，https://ummisco.pages.ird.fr/france/bacaer/2012JMB2.html 。对应正式英文论文 DOI 10.1007/s00285-011-0417-5。用于检查后世模型对1908实验的引用，未核验英文正式版公式逐式一致性。

## 2 1908原刊新增可检验信息

1908原刊p267将Bombay City的通常季节高峰描述为3月，p268描述Poona通常秋季高峰，p270描述Belgaum的8至12月流行季。原刊pp275至279还明确记录温度适宜时疫情仍可能消退，因此温度单因素不足以解释全部时间序列。不同城市的月份和气温不能简单混用。

原刊p283 Table III，1906年7至8月同时进行室温80至83华氏度与冷室约70华氏度的三组动物实验。按PDF文字层重建，室温与冷室成功次数/实验次数依次为：Bombay rats 5/17与13/28；ship rats 8/25与18/27；guinea pigs 4/8与15/15。成功率分别约29%与46%、32%与67%、50%与100%。Table III图像列对齐未核验，数值保留PARTIAL_VISUAL_TABLE_ALIGNMENT。

原刊p284 Table IV，1907年1至2月豚鼠实验：约75华氏度21/25次成功（84%）；85至90华氏度8/25次成功（32%）。风险差为13/25，即52个百分点，低温组与高温组观察成功率比为21/8，即2.625。该数值是实验样本描述，未执行随机分配核验、置信区间或现代独立复现实验。

原刊p283明确冷室密闭，地面铺石灰用于吸收二氧化碳并使室内较干燥。温度改变同时可能伴随湿度和通风条件差异。原刊研究者认为温度是主要因素，但单凭本轮已读段落不能证明两组环境只有温度一项差异。p285还报告室温75华氏度与热室约90华氏度条件下，蚤排泄物可感染性最长分别到第21天与第3天。该实验观测与人类城市季节死亡曲线之间仍隔着动物宿主、蚤数量和报告机制。

1908作者在p284从温度实验讨论较高温度抑制传播。Table IV的高温实际区间为85至90华氏度，Table III为80至83与70华氏度；不应将文中概括性阈值直接当作经过连续剂量响应实验验证的普适临界点。

## 3 对Bacaër2012模型来源边界的补强

Bacaër作者法文全文§4 Table 2给出蚤到宿主的温度响应假设
`π(θ)=π₀(0.75−0.25 tanh(θ−80))`，将1908 p283列为经验来源，π₀=90%由拟合选择。1908 p283至284提供的是有限温度区间的实验成功比例，没有给出上述连续tanh函数的唯一推导，也没有独立测定π₀=90%。因此该函数的具体形状、拐点和尺度属于2012建模选择；1908动物实验只提供方向性的经验约束。其他单调温度响应函数可能在这些离散温度组上产生类似预测。没有重拟合任何R模型或历史曲线。

## 4 1912行政报告提供的空间聚合警告

1912行政报告印刷p203将整个Bombay Presidency年度鼠疫死亡最高月份记为1911年10月，记载当月22,869人死亡；同页单列Bombay City在1911年4月及5月更活跃。该文本还记录整个Presidency在1912年3月死亡3,138人。由于城市4月的数字在OCR中不清楚，本轮不引用该数值。1912报告属于英国殖民政府的行政登记，可能受到地域覆盖、报告制度、病例定义和人口变化影响。

可检验的结构性警告：设区域总死亡为Y(t)=Σ_j Y_j(t)。即使某城市在春季达到自身最大值，也无法推出包含多个城市和乡村的区域总和在春季达到最大值。两种不同地理单位的峰值月份可以不同。这里是时间聚合的数学事实，1912行政报告提供了对应的历史描述；没有从原始分区逐月数据重算该地区峰值，更没有证明造成差异的因果机制。不能用Presidency的秋季峰值反驳Bombay City的春季规律，也不能用单一城市曲线代表全地区。

## 5 有限精确检查、竞争解释及未完成

本轮用Python标准库Fraction执行6项限定算术检查，6项PASS，覆盖Table III三组成功率差与Table IV两个成功率及风险差。Table III对应差依次为81/476、26/75、1/2；Table IV差为13/25。数学检查只保证录入的分子分母算术一致，不证明历史表转录、实验随机化或历史因果识别。

竞争机制保持分离：温度影响蚤体内细菌存活、湿度及通风、蚤密度季节变化、鼠群易感构成、地理聚合与行政报告偏差。1908原作者自身承认温度不能解释所有流行季结束。后世2012季节模型提供候选解释，连续温度函数和自由拟合参数缺乏独立识别。这里仅为动物实验与历史观察的局部证据关系，未把流行病模型熔炼进心理史学。

未读：1908原刊PDF p283至285原版图像及全部原始实验记录，1912委员会原刊pp222至226原始统计表，1912行政报告p203图像，其他地区完整月序、置信区间、历史因果估计和未来事件预测。状态分别为PARTIAL或NOT_RUN。1927正式勘误仍PARTIAL。

C010于2026-11-02已COMPLETE，D003于2026-W45的2026-11-02已COMPLETE，本轮只读，无新增C/D编号。R073和PESEN v0.1保持冻结，R系列E1/E2/E3及MARKET证据不升级。Codex开放PR不算main成果。未触发GitHub Actions，未使用付费接口，账户账单及免费CI额度未核验。

下一步：优先直接核验1912委员会pp222至226图表与1908 p283 Table III原版排版；若无法取得，转向本周覆盖较弱的其他学科，避免连续占用TH212。先完成全部R系列，再统一分类，最后有条件熔炼。
