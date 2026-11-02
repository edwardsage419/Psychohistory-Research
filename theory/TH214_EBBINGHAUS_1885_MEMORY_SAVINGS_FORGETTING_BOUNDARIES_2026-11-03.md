# TH214 艾宾浩斯1885年记忆实验：再学习节省量、遗忘函数与外推边界

track: theory
subflow: main
run_date: 2026-11-03 (Asia/Singapore)
observed_head: 057287c495d3964cb1f37285b908f1438ccc897c
target_key: (theory,Ebbinghaus1885,1885-German-original+1913-English-translation,learning-savings-vs-forgetting-and-generalization)
status: THEORY_NOTE_BOUNDED; TRANSLATED_PRIMARY_TEXT_SECTIONS_READ; ORIGINAL_GERMAN_PAGE_COLLATION_PARTIAL; NO_R_EVIDENCE_UPGRADE
R073: FROZEN
PESEN_v0_1: FROZEN
E1_E2_E3_MARKET: NO_CHANGE

## 1. 原始来源、版本与实际阅读

[A] Hermann Ebbinghaus (1885), *Über das Gedächtnis: Untersuchungen zur experimentellen Psychologie*, Leipzig: Duncker & Humblot, 原著无DOI。1885年原版书目与188页数字影像入口：美国国会图书馆 https://www.loc.gov/item/e11000616/ 。本轮**只核对原版出版元数据和影像可得性**，没有逐页核读1885年德文原件，不能宣称德文逐字校勘。

[A-T] Ebbinghaus (1885), Henry A. Ruger 与 Clara E. Bussenius 1913年英译 *Memory: A Contribution to Experimental Psychology*, Teachers College, Columbia University。York University公开原著英译转录：
* Chapter III §§11–14，实验材料、恒定条件与误差，https://psychclassics.yorku.ca/Ebbinghaus/memory3.htm
* Chapter IV §17及§18开头，平均值、试次内偏态及分组误差，https://psychclassics.yorku.ca/Ebbinghaus/memory4.htm
* Chapter VII §§26–30，竞争遗忘机制、再学习节省量、原始七个时间点与经验公式，https://psychclassics.yorku.ca/Ebbinghaus/memory7.htm

上述章节为**1913年原作译文的网页转录**，直接审读指定章节文字。原版德文印刷页码、英译排版表格图片逐格和德英术语对照尚未核验；不得把转录视为原件扫描逐页校勘。未读英译Chapter I、II、V、VI、VIII、IX的完整正文。

## 2. 原作命题与竞争解释

1. Chapter III §11：从约2300个可用音节随机组合系列，以首次满足预设无错复述标准所需学习工作量为观测量。作者承认即使无意义音节仍有母语、音韵、感觉通道与注意力差异。故“无意义材料完全消除既有经验”是过强表述。
2. Chapter III §§13–14：尽量控制诵读节奏、间歇、当日时间、疲劳、外界扰动及前一活动。作者明言实验人工化会缩小日常生活外推范围；不同日生活条件无法完全保持相同。
3. Chapter IV §17：作者1879–80年92组测试均值1112秒、观察可能误差±76秒；1883–84年84组测试均值1261秒、可能误差±48.4秒。不同系列长度、停止准则和时间阶段均变化，不能直接将两均值差解释为个人记忆能力的长期进步。§18指出单个系列的学习时长右偏，合并系列后分布更对称，平均值可靠性依赖聚合和条件。
4. Chapter VII §26：原作并列讨论痕迹保留与遮蔽、表征逐渐减弱、复杂表征成分脱落等竞争解释，认为日常内省不足以裁决。不能把单一“痕迹指数衰减”归给原作的已验证机制。
5. Chapter VII §§27–28：用再学习工作量节省测量残留学习效应。设首次学习时长L、再学习时长WL或经修正WLk，D=L-WL，扣除原始两次复述的85秒后，原作指定8组13音节条件的百分比Q=100D/(L-85)。Q是工作节省代理，**不是直接回忆正确率**，也不自动等于个人经历真实记忆的比例。作者还明确1小时与约9小时间隔受日内精神状态影响，修正有不确定性。
6. Chapter VII §29：原作者给出近似经验式 b=100k/((log10 t)^c+k)，其中k约1.84，c约1.25，t按原文从学习结束前1分钟起计的分钟数。作者强调仅对自己在特定13音节条件下的一次系列结果作简写，不宣称跨人普遍规律。这一式子**不是通常被笼统称作的指数遗忘律**，也不能直接用于预测社会历史变化。原文24小时33.7%结果与邻近间隔关系不平滑，作者自己提出随机误差疑问；后续控制实验中12音节24小时约33.4%，材料长度不同。
7. 实验间隔约20分钟、1小时、9小时、1、2、6及31天。作者自己承认9小时与24小时的部分差异可能受睡眠、注意力和修正假设影响。时间相关性不唯一确定衰减、干扰、检索条件或编码质量的因果机制。

## 3. 独立方法反例、范围及证据等级

构造两种世界：世界A记忆痕迹随时间变弱，世界B痕迹不变但提取线索有效性下降。只观测再学习工作量，允许两世界给出相同Q(t)。此为欠识别逻辑构造，尚未形成可估计结构模型。可区分的候选额外观测是控制线索、材料相似性、睡眠/干扰、初学强度并独立测量正确回忆与再学习耗时。未来实验应冻结刺激与停止规则，避免以事后曲线拟合选择“最优”机制。

与C011仅作局部关联：历史自我报告的回忆偏差需要真实事件日志、时间间隔与错误肯定率；艾宾浩斯的音节节省量不能替代生活事件真实性。与TH213的历史调查观察误差是不同证据问题。本轨不执行R模型拟合、实证评分、跨轨科学验收或项目级融合。

## 4. 已执行、未执行及下一步

标准库Fraction限定算术示例：L=1000秒、WL=700秒，Q=100×300/915=2000/61≈32.7869%，验证分母扣除85秒对节省比例的影响。另有C011的6项独立人工断言，均仅证明构造算术。原版德文公式与英译表格逐格比对、原始逐试次数据复算、跨参与者验证、真实人生回忆实验、历史因果与独立预测：NOT_RUN。

C: C011本地日期2026-11-03单独归档，参见research/decision_methods/C011_RETROSPECTIVE_RECALL_DIARY_VERIFICATION_2026-11-03.md。
D: D003 COMPLETE，2026-W45，实际完成2026-11-02，只读。
CI: NOT_RUN；新增付费操作0；实际账户计费NOT_VERIFIED。
next: 合法核验1885年德文§及1913年表格图片，阅读记忆干扰/检索线索的独立原始实验并保持学科轮换；不能将遗忘经验曲线提升为跨人规律。
