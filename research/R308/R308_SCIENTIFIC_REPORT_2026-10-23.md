# R308 科学报告：集体效能信念、邻里干预意愿与资源门的有限数学分离

2026-10-23 Asia/Taipei。原始239模型候选 **03-018 Collective Efficacy** P1。状态 **CLOSED_BOUNDED_E1_ARTIFICIAL_R308_COLLECTIVE_BELIEF_ACTION_PROXY**。仅根据项目自行设计的聚合与门控数学构造，计算 **432个完全人工世界、864条原始人工渠道数据**；不代表真实社区、学校、受试者、暴力事件、资源评估或干预数据。

## 原始学术证据及其不可偷换的三个构念

Bandura (2000), *Exercise of Human Agency Through Collective Efficacy*, *Current Directions in Psychological Science* 9(3):75–78, https://doi.org/10.1111/1467-8721.00064。共同效能强调成员对集体行动能力的共享信念（perceived collective efficacy），不是行动已经发生或一定有资源完成行动。

Sampson, Raudenbush & Earls (1997), *Neighborhoods and Violent Crime: A Multilevel Study of Collective Efficacy*, *Science* 277(5328):918–924, https://doi.org/10.1126/science.277.5328.918，[NLM PubMed原文书目信息](https://pubmed.ncbi.nlm.nih.gov/9252316/)载明作者调查**8,782名居民、343个芝加哥邻里**，把邻里社会凝聚与为了公共利益愿意干预结合，使用多层模型发现与暴力状况的**调整后负向相关**。本研究**没有取得或处理该论文居民记录、邻里编码、既往犯罪率、对照变量或多层回归结果，更没有确认现实因果影响**。

Goddard, Hoy & Woolfolk Hoy (2000), *Collective Teacher Efficacy: Its Meaning, Measure, and Impact on Student Achievement*, *American Educational Research Journal* 37(2):479–507, https://doi.org/10.3102/00028312037002479，研究实际学校集体教师效能的测量与学习成绩的相关性。R308不重跑原问卷项目、学校抽样或学业成就指标。不能把Bandura、Sampson和Goddard对不同群体/测量单元的证据合并为普适已证实公式。

相关R307少数派公开/私有表达，R306群体极化，R305自我分类，R304社会身份资源分配，R072公共声誉等都不是这个“相信能做／愿意去做／有资源做”的同一科学问题，也没有把其原始数据转为新的R308真实E2。

## 事前冻结模型与精确变量

[完整科研协议](../../protocols/R308_COLLECTIVE_EFFICACY_BELIEF_WILLINGNESS_RESOURCE_864_SOURCE_PRESCORE_FREEZE_2026-10-23.md)在代码/结果之前固定于[GitHub commit cf0f4894](https://github.com/edwardsage419/Psychohistory-Research/commit/cf0f4894fba5acd22700cc6ea7cdc74e6ff80bed)。

本项目自行选择**八个人工的三名成员信念三元组**，例如(0,0,0)、(1/2,1/2,1/2)、(1,1,1)、(1,1,0)、(1,1/2,1/2)等；这八种只是特定反例集合，**不是**对全部27种有序三元组穷举或对人口代表性抽样。选择两个互竞的项目自建聚合规则：共同信念B=三个成员信念的**算术平均MEAN**，或弱链接聚合B=三个成员信念的**最小值BOTTLENECK_MIN**。两者没有被Bandura等人原论文数据拟合或证实为真实心理尺度。

额外三个项目虚拟门控：邻里凝聚c、愿意干预w、资源可用r，各取{0,1/2,1}。人为设定一个类比Sampson构念的**凝聚×意愿结合项 C=c*w**，再设完全项目原创的**假想行动倾向代理量 A=B*C*r**。A仅是一个假设性条件概率/代数记号，**不是现实社区的实际干预率、犯罪发生概率或学生学业成绩概率**。这只说明任何门控为0都会强制A=0，而不是检验真实社会里行为怎样受资源或信念影响。

组合8信念模式×2聚合×3凝聚×3意愿×3资源=**432个人造世界**，每世界分别有PERCEIVED_COLLECTIVE_BELIEF与RESOURCE_GATED_ACTION_PROXY两种渠道，**864条完整原始source**，均保存三人信念、聚合类型、各门控、B、C、A及信念-假想行动差、完整世界标号和来源编码，无受试者ID。

## 关键反例与可识别性边界

当(1,1,1)全员自报集体信念均1、c=w=r=1时，B=A=1；当w=0但信念与资源仍全1，B依然1、C=0、**A=0**；当r=0、群体信念与愿意干预都保持1时B=1、C=1、**A=0**。这证明**本项目人为设定的公式**不会把“非常相信共同能力”偷换为“实际能完成干预”。但不构成真实群体行为证据。

比较(1,1,0)与(1,1/2,1/2)：它们的成员信念算术均值均为**2/3**，但若用最弱成员聚合，前者B=0，后者B=1/2。在c=w=r=1时MEAN规则令两者**假想A=2/3**，而BOTTLENECK_MIN规则下两者分别A=0与1/2。因此即使有相同群体平均信念，**个人分布结构及选择何种聚合函数仍决定人工机制结果**。数据本身没有辨别MEAN还是MIN哪个更符合真实邻里，亦未给出社会效能测量因子载荷。

其他负对照：凝聚c=0或干预意愿w=0、资源r=0全部令假想A=0但可能B>0；全部概率严格0≤A≤B≤1，随三个门控单调不降。以上是乘法形式直接推导而非真实随机试验新发现；真实结构性贫困、犯罪历史、关系网络等共同原因在此根本未测量，故不得做因果推断。

## 真正可执行的计算、独立验证及归档

[主源程序与2607次真实unit tests](r308_exact_collective_efficacy_belief_action.py)、[864条全人工原source CSV](R308_ALL_864_ORIGINAL_COLLECTIVE_EFFICACY_CHANNEL_SOURCES.csv)、[432世界完整双渠道JSON](R308_EXACT_COLLECTIVE_EFFICACY_RESULTS.json)、[原始数据/结果SHA256机器凭证](R308_MACHINE_RECEIPT.json)永久归档。

[独立全源审计](../catalogue_audit/independent_r308_source_audit.py)不导入主模型，而采用**四个独立假设Bernoulli门控的全部16种成败组合**重新累计“B、凝聚、意愿、资源均通过”的概率，复算A，并重建完整864条CSV及432世界JSON，含18项恶意删改源、篡改数值、伪造真实暴力渠道、改写阴性控制、伪造SHA等测试。这个双路径验证只证明冻结人工公式被可靠计算，不证实独立门控假设在现实中成立。

[实际GitHub Actions science run39954221447](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39954221447)全部3个jobs **completed/success**，Python3.11和3.12各完成2607模型unit tests与18项独立审计，第三job独立检查全部864原source及来源SHA，结果永久归档main[commit 831e7e24](https://github.com/edwardsage419/Psychohistory-Research/commit/831e7e246a833ff7fc79d8ab719ab5fed9bf4361)。CSV SHA256为**1c6f7210bfbf793f87b7b49fd0db9dfa496d3d46810444d2802d54820dfe86e8**，结果SHA256为**00691106c8c27ae25a47fb0b202539c368608802feaf52ae8f17af15d9e4d42e**。

限定科学结论：R308的项目原创E1机制完整且可复算；实证真实群体E2与跨尺度历史E3均未实现，本轮不能指导邻里犯罪政策或教学质量因果决策。R073和PESEN v0.1冻结，仍按原R系列主线推进至完结后才归纳分类与模型熔炼。
