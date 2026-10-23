# 心理史学原239模型：R307少数派影响、R308集体效能有界E1与来源目录v2.3

日期2026-10-23 Asia/Taipei。性质：两项自创人工数学模型的有界机制研究，**不是1969/1994少数派真人研究、1997年芝加哥街区居民研究或2000年学校效能研究的重拟合**。遵循既定研究顺序：**完成原R全系列→统一归纳分类→最后原创模型熔炼**；个人辅助决策系统构建继续暂缓。R073及PESEN v0.1冻结。

## 1. R307少数派来源一致性、可信度和公开表达

原候选 **03-016 Minority Influence Models** P1。原一手研究Moscovici、Lage、Naffrechoux(1969), *Influence of a consistent minority on the responses of a majority in a color perception task*, https://doi.org/10.2307/2786541，研究真实少数派一致性对多数者颜色知觉判断影响。Wood等人(1994), *Minority influence: a meta-analytic review of social influence processes*, https://doi.org/10.1037/0033-2909.115.3.323，总结**97项真实实验**，报告少数派影响的私人、间接测量通常更明显且与行为一致性有关；**本项目没拿到/复算这些原受试者结果或原元分析效应量**。

本研究[事先冻结协议](../protocols/R307_MINORITY_INFLUENCE_CONSISTENCY_PRIVATE_PUBLIC_864_SOURCE_PRESCORE_FREEZE_2026-10-23.md)提交[4f74448e](https://github.com/edwardsage419/Psychohistory-Research/commit/4f74448e261ac61c65cd60926a056d6916a84e34)，与原作者真实心理参数无关。本项目人工设定先验支持概率p0∈{1/4,1/2}、同一少数派信息接触次数t∈{0,1,2,3}，一致性c、可信度k、公开规范压力n各∈{0,1/2,1}，少数派人数m∈{1,2}（六人虚构组）。虚构似然倍率**L=1+c*k**，私人后验赔率为p0/(1−p0)×L^t；虚构公开表达另由**保留率1−n(6−m)/6**作用于相对先验的私人增量。**这是人为数学方程，不是Moscovici/Wood作者模型，也无实际人群概率校准。**

全组合**432人工世界×2私人/公开来源=864条完整original source**。p0=1/4,t=3,c=k=1时，PRIVATE=8/11；若满规范压抑n=1且m=2/6，PUBLIC=9/22；若m=1/6，PUBLIC=29/88；n=0时两者同8/11。零信息接触或c=0/k=0不会改变先验。最重要**参数辨识反例**：c=1/2,k=1与c=1,k=1/2产生同一L=3/2，t=3且先验1/4的私人概率都9/17；仅有终端表现无法分别推断“有多一致”与“有多可信”。任何真人推断需要独立操纵两个变量。

[完整正式R307科学报告](../research/R307/R307_SCIENTIFIC_REPORT_2026-10-23.md)、[864完整人工source CSV](../research/R307/R307_ALL_864_ORIGINAL_MINORITY_PRIVATE_PUBLIC_SOURCES.csv)、[432原世界全后验结果JSON](../research/R307/R307_EXACT_MINORITY_INFLUENCE_RESULTS.json)、[机器范围验收](../research/R307/R307_FINAL_ACCEPTANCE_STATUS.json)、[独立Bayes逐次归一化重算审计](../research/catalogue_audit/independent_r307_source_audit.py)。数据及结果SHA见[机器收据](../research/R307/R307_MACHINE_RECEIPT.json)。研究[真实GitHub CI39953705822](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39953705822) **3/3成功**，Python3.11/3.12各**2607项主模型unittest**+18独立源反例测试，第三job独立逐项重算来源后永久存入main[commitd4ebc9cb](https://github.com/edwardsage419/Psychohistory-Research/commit/d4ebc9cbbffe550a61aa2d602fc3bceb79fb4850)。

## 2. R308共同效能信念、凝聚、意愿与资源的区分

原候选**03-018 Collective Efficacy** P1。Bandura(2000), *Exercise of Human Agency Through Collective Efficacy*, https://doi.org/10.1111/1467-8721.00064，强调共享的群体行动能力信念；Sampson、Raudenbush、Earls(1997), *Neighborhoods and Violent Crime: A Multilevel Study of Collective Efficacy*, https://doi.org/10.1126/science.277.5328.918，真实调查**8,782名芝加哥居民、343个街区**，把凝聚与愿意为了公共利益干预联系起来，并报告与暴力的调整后关联；Goddard、Hoy、Woolfolk Hoy(2000), *Collective Teacher Efficacy: Its Meaning, Measure, and Impact on Student Achievement*, https://doi.org/10.3102/00028312037002479，研究真实学校集体教师效能测量与教育指标的关系。**这些是真论文的不同实证场景，不是同一套已验证微观/宏观因果公式；R308不重算其原始真人问卷、犯罪数据、成绩或统计量。**

[事前冻结协议](../protocols/R308_COLLECTIVE_EFFICACY_BELIEF_WILLINGNESS_RESOURCE_864_SOURCE_PRESCORE_FREEZE_2026-10-23.md)，冻结[commitcf0f4894](https://github.com/edwardsage419/Psychohistory-Research/commit/cf0f4894fba5acd22700cc6ea7cdc74e6ff80bed)。选择**8种而不是全部27种**的固定三个人工成员信念三元组，两个项目创造的聚合方法MEAN/BOTTLENECK_MIN；另设凝聚c、干预意愿w、资源r各∈{0,1/2,1}。人为定义共同效能信念B=成员信念均值或最小值、凝聚意愿代理C=c*w、**虚构行动倾向A=B*C*r**。A不代表实地实际干预率、犯罪风险、学生成绩或经验证的社会控制因果作用。

全格**8人造信念模式×2聚合×3凝聚×3意愿×3资源=432人工世界×2信念/行动代理渠道=864条完整source**。正例：高信念(1,1,1)、c=w=r=1时B=A=1；若无愿意干预w=0，即使B=1，A=0；资源r=0也令A=0。两个信念配置(1,1,0)与(1,1/2,1/2)**均值同为2/3**；采用MEAN时代理A都是2/3（全部门控为1），但采用BOTTLENECK_MIN时为0与1/2。因而**只看群体平均值无法辨认成员脆弱点，所用聚合规则本身是额外模型假设**。这套结果全部由自建门控公式导出，没有真实行动干预或心理测量构念识别。

[完整正式R308科学报告](../research/R308/R308_SCIENTIFIC_REPORT_2026-10-23.md)、[864人工原始source](../research/R308/R308_ALL_864_ORIGINAL_COLLECTIVE_EFFICACY_CHANNEL_SOURCES.csv)、[432世界结果](../research/R308/R308_EXACT_COLLECTIVE_EFFICACY_RESULTS.json)、[正式机器范围验收](../research/R308/R308_FINAL_ACCEPTANCE_STATUS.json)、[独立4个Bernoulli门全16结果穷举及恶意篡改审计](../research/catalogue_audit/independent_r308_source_audit.py)、[SHA机器收据](../research/R308/R308_MACHINE_RECEIPT.json)。[科学CI39954221447](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39954221447) **3/3成功**，双Python各**2607项unittest**+18独立审计，第三job重新检查全部864原source和SHA，并永久归档[commit831e7e24](https://github.com/edwardsage419/Psychohistory-Research/commit/831e7e246a833ff7fc79d8ab719ab5fed9bf4361)。

## 3. 可重复性事实与科学证据等级

| 研究内容 | 原候选 | 事前冻结早于代码 | 新人造世界 | 新完整source | Python3.11与3.12主unit tests | 成功工作流 |
|---|---|---|---:|---:|---:|---|
| R307少数派影响 | 03-016 | 4f74448e | 432 | 864 | 2607×2 | [39953705822](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39953705822) |
| R308集体效能 | 03-018 | cf0f4894 | 432 | 864 | 2607×2 | [39954221447](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39954221447) |

本轮实际**1728条新人工来源行、共10428次两个版本主unit tests通过**，此外每研究双版本与独立第三归档审计运行18项原source篡改测试。所有新文件经原始字节SHA固定。**1728不代表真人样本**；一切结论限于自造理论机制E1，未新增E2和E3，不能把期望值当实地观测概率。

## 4. 原始239唯一候选来源索引v2.1→v2.2→v2.3

| 档案来源级别 | v2.1 R306后 | v2.2 R307后 | v2.3 R308后 |
|---|---:|---:|---:|
| 已建立原候选专属主R关联 | 195 | 196 | **197** |
| 旧共享数学非独立主R | 3 | 3 | **3** |
| 只有早期有限研究关联 | 3 | 3 | **3** |
| 已查来源暂无逐项连接 | 38 | 37 | **36** |
| 尚待核主R关联 | 41 | 40 | **39** |
| 原始唯一候选总数 | 239 | 239 | 239 |

[最新v2.3原239候选逐项证据交叉索引](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v2.3_2026-10-23.json)，相对v2.2**仅03-018改成R308**；此前v2.2相对v2.1**仅03-016改成R307**。早期R072真人S8来源及REV008无法独立解码处理组的阻塞仍原样存在；R073/PESEN v0.1仍冻结。**197项主R来源不是197项经独立真人实验验证的心理学模型**。

[当前39个未闭合原始候选来源队列](ORIGINAL_239_PENDING_39_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv)，P1 **12**、P2 **27**。下一项**04-006 SIR Epidemic Model**（属于网络传播与动力系统，需明确区分微生物疾病模型和一般文化/思想传播）；随后是04-008 Voter Model。先核对已有早期R研究是否曾研究SIR，防止仅凭原模型术语重做已验证成果。

实际四项三作业工作流全成功：
- [R307科学39953705822](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39953705822)
- [R307原239 v2.2 39953984919](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39953984919)
- [R308科学39954221447](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39954221447)
- [R308原239 v2.3 39954481684](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39954481684)

合计**12个CI job completed/success**。独立原239审计各从上一版本精确比较全部239条，保证仅允许一条候选升级，维持来源、科学等级和完整39条待研究清单。

**结论**：R307、R308完成了有限原始人工数学E1，未新增真实E2及历史E3，不宣告原239整体科学验收完成。之后继续原R系列，不开始全体模型分类和融合。
