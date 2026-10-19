# R116：规范性社会影响与信息性影响的区别——公开服从、私人信念与社会地位机制

研究时间：2026-10-19（Asia/Taipei）。原既定候选P0 03-005 Normative Social Influence。研究R116是独立归档编号，不代表目录中的全部规范性社会影响理论已验收。

## 1. 第一手原始文献核阅及证据

**原始人类实验文献1**：Solomon E. Asch (1955). *Opinions and Social Pressure*, Scientific American 193(5):31–35，DOI 10.1038/scientificamerican1155-31。原出版方历史记录：https://www.scientificamerican.com/article/opinions-and-social-pressure/ 。MIT高校托管原刊全文副本：https://web.mit.edu/curhan/www/docs/Articles/15341_Readings/Influence_Compliance/required_readings/1Asch_1955_Opinions_and_social_pressure.pdf 。本阶段直接核阅原刊全文第3–4印刷页/原PDF第2–3页（从零计）。作者自己写明：被试在18次线长试次中有12次面对预先训练的错误多数判断；在涉及**123名受试者**的系列中，被试在错误一致多数下的相关选择中**36.8%**随群体给出错误判断，且个体间有显著差异。他还报告有些跟随者相信自己判断错、有些担心公开显得另类、有些保持独立。**这是原刊作者汇总陈述，不是本项目独立获取原试次表得出的新百分比。**不能将36.8%解释为“36.8%的受试者始终服从”，因为其分母是相关的选择次数。

**原始人类实验文献2**：Deutsch M, Gerard HB (1955). *A study of normative and informational social influences upon individual judgment*, Journal of Abnormal and Social Psychology 51(3):629–636，DOI 10.1037/h0046408，官方PubMed书目 https://pubmed.ncbi.nlm.nih.gov/13286010/ 。APA出版方预览/可见摘要提供面对面、匿名及事前/公开承诺等判断条件信息。本轮不声称已经读完整论文方法与原始数据，且没有从该研究真实计算信息性与规范性影响分别有多大；匿名条件未消除全部错误，不能直接当作纯规范因果差额。

**原始博弈理论文献**：B. Douglas Bernheim (1994), *A Theory of Conformity*, Journal of Political Economy 102(5):841–877，DOI 10.1086/261957。原作者Stanford页面 https://bernheim.people.stanford.edu/publications/theory-conformity；Haverford公开原刊PDF https://www.haverford.edu/sites/default/files/Bernheim1994.pdf ，本轮直接核阅其印刷第841–844页。作者的理论核心：地位/社会认同与消费内在效用都重要；旁观者观察行动推断不可观察的个人**偏好类型**，社会地位由他人对类型的推断决定，偏离规范的地位惩罚**均衡内生**。Bernheim原模型与BHW 1992年基于信息推断的理性级联明确为两种竞争解释，不能单凭行动一致判别。

**文献证据边界**：有真实原论文、原作者汇总和理论模型，但本项目无这些论文的原始个人试次CSV、均衡求解源码、独立估计、交叉实验因果检验；因此真人E2新增0。

## 2. 本项目独立声明的极简教学结构

本阶段在任何测试前冻结的模型是**研究者自构的外生固定公众异议成本toy**，既不是Bernheim原论文的类型信号均衡，也不是Asch或Deutsch–Gerard的真实拟合方程。它的价值是构造一个精确可重复的最小反例，明确区分（a）信念更新，（b）公开声明，以及（c）地位损失。不能把toy中的固定社会地位惩罚误称“Bernheim原模型得出这组系数”。

真实价值V为二元，个人有一个私人信号0，其准确率3/5，故Pr(V=1|本人信号0)=2/5。报告的群体意见指向行为1；当选择**把它视为一条独立信息线索**时，强信号准确率3/4，理性后验为Pr(V=1|自身0,群体1)=2/3；弱线索11/20时，理性后验为22/49。这里群体一条可观察报告只当**一个**来源，不能把许多人重复发表相同源消息擅自累计成多个独立私人信号。

行动正确预期收益：若选择1则q，若选择0则1-q。仅在看见群体意见且本人回答可归因公开时，对与群体意见相反的行动固定扣除1/4收益。匿名回答、未接收群体消息没有此成本。无信息通道的模型看到报告也不更新私有信念；无地位通道的模型不会因公开回答额外扣成本。最大净收益选择，严格平局执行行动0，所有有理数由Python Fraction精确计算。

四种冻结toy：NO_INFLUENCE（信息关、地位成本0），NORMATIVE_ONLY（信息关、成本1/4），INFORMATIONAL_ONLY（信息开、成本0），BOTH（信息开、成本1/4）。

## 3. 2×2强线索设计中的机制等价

同一人先获得支持0的私人信号；因素1为是否实际看见群体对1的报告（C0无、C1有），因素2为回答是否公开可归因（ANON匿名、PUBLIC公开）。冻前预测二元选择1：

| Toy模型 | C0_ANON | C0_PUBLIC | C1_ANON | C1_PUBLIC |
|---|---:|---:|---:|---:|
| NO_INFLUENCE | 0 | 0 | 0 | 0 |
| NORMATIVE_ONLY | 0 | 0 | 0 | 1 |
| INFORMATIONAL_ONLY | 0 | 0 | 1 | 1 |
| BOTH | 0 | 0 | 1 | 1 |

关键一：**只有C1_PUBLIC群体压力条件时，三种机制都呈现相同的跟随**，仅观察公开服从无法知道他是改变了“真实事实”的私人信念，还是为避免地位损失而隐藏自身判断。

关键二：规范性toy在C1_PUBLIC仍私下认为行为1正确的概率是2/5，公开却选1；信息性toy在同条件下私下认为行为1正确的概率是2/3，也公开选1。相同行动对应不同的私人信念与动机。

关键三：即使观察**全部四格**，INFORMATIONAL_ONLY和BOTH在强线索条件下的动作向量也完全一致，故匿名条件虽有助区分“纯规范”与“纯信息”这两个toy，**并不能保证检出强信息影响下额外存在的地位成本**。未观察潜在信念，不能声称严格一般识别。

## 4. 更弱群体消息下的条件反例与门槛

弱群体线索准确率从3/4降至11/20，但仍将其作为条件独立的**一条**信号。接收弱消息后主观Pr(V=1)=22/49≈44.898%，单靠信息，私人证据仍支持行动0；于是INFORMATIONAL_ONLY在C1_ANON与C1_PUBLIC都保持行为0。

若再有外生地位成本1/4，BOTH模型在C1_PUBLIC选择1，在C1_ANON仍选择0。因此增加弱信息环境可能帮助区分“纯信息”与“信息+公开压力”这两个**指定玩具世界**。它不是推导已在真实实验中成功操纵受试者信号可信度，也不证明真实人群不存在其它同时作用机制。

当完全不进行信息更新、q=2/5时，个人原行动0与群体行动1的内在收益差为(1-q)-q=1/5。固定地位成本c>1/5才会让公开选择转为1；c=1/5两行动严格平局，按事前约定保留0。这条阈值由人工设定效用直接推导，不是Bernheim类型信念模型的内生社会惩罚强度。

## 5. 实验与跨项目的实际研究资格

未来若要真正将R115（信息级联）与R116（公开声誉压力）做外部竞争评价，需要：
- 私人信号是否被正确测量，公众对他人消息可信度是否能独立校准；
- 群体报告的共同上游来源以及多个意见是否相关；
- 回答公开/匿名处理与本人感知公开性的实际操作合规；
- 真实目标选择是否有退出、奖金、公开声誉和其它共同激励；
- 预先冻结样本按真正实验场次、群组或参与者完全独立划分；
- 与社会规范预期/个人规范信念的测量区别，以及测量时序和随机化机制。

上述项目未经检验，R116并没有“隔离出一个真实规范心理因果效应”。R115已数学复现贝叶斯行动级联，R116则数学区分公开地位成本与私人信念变化。项目仍处在逐模型学习阶段，不在本轮互相融合或修改PESEN参数。

## 6. 执行、证据等级与结题准则

冻结协议：protocols/R116_NORMATIVE_SOCIAL_INFLUENCE_PRIVATE_PUBLIC_STATUS_VS_INFORMATION_SOURCE_FREEZE_2026-10-19.md。
模型：research/R116/r116_normative_public_status_vs_informational_cue_exact.py。
单元测试：research/R116/test_r116_normative_public_status_vs_informational_cue_exact.py。
完整合成验证48项，含信念准确分数、阈值、四模型2×2、弱信号作用、公开私人信念等价、非法Fraction/布尔/动作、无实人数据伪称。在CI实际运行并归档源码三件套的SHA256以前，仍只能称“代码提交待机器验证”。验收成功后仅给出 LEARNING_COMPLETE_BOUNDED_PRIMARY_SOURCES_AND_STATUS_INFORMATION_IDENTIFIABILITY；从不称真实原行为E2、前瞻E3或原创跨尺度融合完成。

R073/PESEN v0.1继续冻结；先完成既定R系列再统一分类熔炼。
