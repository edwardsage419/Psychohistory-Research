# TH197 补记：Tang 与 Ostrom 1993 原始工作论文的治理权、操作规则及14例子样本

track: theory
subflow: main
date: 2026-11-01 (Asia/Singapore)
retrieved: 2026-11-01
target_key: (theory,Tang_Ostrom1993_NetworkPaper23,Indiana-original-v1,governance_vs_management_and_bureaucratic_subgroup_table2)
baseline_main: 56499969f3973622d5b8836a2decfb830bd7aae3
status: COMPLETE_BOUNDED_PRIMARY_READING; OSTROM2010_DENOMINATOR_RECONCILIATION_PARTIAL
evidence: ORIGINAL_AUTHORS_WORKING_PAPER_SELECTED_PAGES; NONBLIND; NO_REAL_CAUSAL_REESTIMATION
r_e1_e2_e3_upgrade: NONE
ci: NOT_RUN
billing: NOT_VERIFIED

## 1. 来源身份、实读范围及去重

Shui Yan Tang and Elinor Ostrom (1993), *The Governance and Management of Irrigation Systems: An Institutional Perspective*, Irrigation Management Network Paper 23, Indiana University Digital Library of the Commons, stable handle https://hdl.handle.net/10535/4589 ; institutional PDF https://dlc.dlib.indiana.edu/dlc/bitstreams/6c4046d1-bb0d-42ab-a7e6-0a89fb8510c8/download . 直接阅读机构所藏作者工作论文的Introduction、Institutions as Rules-In-Use、Developing Irrigation Institutions、Crafting Operational Rules、Crafting Governance Structures、Community/Bureaucratic Irrigation Systems及Conclusion，主要印刷页1至4、7至11、13至20；直接目视核验印刷页17 Table 2（PDF第11页，零起算10）。参考文献未逐条核验。该文为原作者公开工作论文，不能直接称为同行评审发表版本，亦没有独立DOI。

这是TH197原著链的独立文本证据，数据却来自同一Tang灌溉案例系列，不能作为独立第二样本。既有TH197已审1989博士论文印刷pp60至68、78至82，及Ostrom2010 p650。本轮新增1993作者原文对治理权、规则适应及14个官僚治理案例的分组结果；不新增TH编号、不修改既有1989/2010记录。

## 2. 原始命题与实证表

A. [原作者理论，印刷pp1至4] 农民参加日常维护与供水管理，和农民能否制定、修改、执行规则及追责官员，是不同制度安排。作者明确批评将劳动参与等同治理参与的项目做法。区分正式法规与实际执行规则，指出行政罚则也可能被官员转化为寻租机会。规则改变须审视实际激励及地方物理条件。

B. [原作者理论，印刷pp4至8] 操作层、集体选择层、宪制选择层形成不同层级的规则修改权限。土壤、地形、水量与季节变化使地方规则需要持续调整；同一项目的全域统一配水时段可能与水流周期错配。原作者记载37例有相关配水程序资料，其中22例仅采用固定时间配水；19例有两套季节或水量条件下的配水规则，其中18例在水少时采用更严格规则。两个分母不同，不能混成47例总体率。

C. [原作者观察，印刷pp10至11] 只有11例同时报告维护劳动强度与劳动贡献规则。7个等量贡献案例平均每人每年2.3劳动日，4个按受益比例贡献案例平均17.7劳动日。分组由条件与制度共同决定，资料缺失严重；差异不能当作规则的因果效应。作者提出比例规则的核算成本可能在低维护强度环境超过收益，紧急维护则可能优先采用便于快速动员的等量规则。

D. [原作者Table 2，印刷p17，PDF页10图像已核] 官僚治理14例中，8例有地方集体选择机构，6例没有。结果定义为「规则遵守与设施维护两者均为良好」：

| 结果 | 有地方集体选择机构 | 无地方集体选择机构 |
| --- | ---: | ---: |
| 两项均良好 | 6 | 0 |
| 至少一项较差 | 2 | 6 |
| 总计 | 8 | 6 |

原文报告75%对0%，并给出带连续性校正的卡方约5.1、自由度1、P<0.05。表注来源Tang (1992)。该结果指标不包括供水是否充足，不能直接与Ostrom2010 p650所称high performance视为同一估计对象。

E. [原作者定性案例，印刷pp2至3、15至19] Tanrwan案例转述Sengupta (1991)，显示政府建立正式农民组织后，行政规定与既有地方维修及配水实践发生冲突；该例属于作者援引的二级案例，Sengupta原始文本本轮未读。1993作者另描述政府体系内地方水务组织受限、官员对上级负责而较少受农民监督的机制。案例说明候选机制，无法单凭叙述排除逆向因果或选择偏差。

## 3. 独立精确算术核验及局限

基于原文Table 2的四个整数(6,2,0,6)，用Python标准库Fraction与math.comb进行8项断言，全部PASS。按表格边际固定、超几何抽样假设计算，Fisher精确单侧尾概率为4/429（约0.009324），按概率不大于观测表的双侧规则为29/3003（约0.009657）；Yates连续性校正卡方为5887/1152（约5.11024），与原文5.1一致。计算是原表格的派生算术，不能替代原始47案例编码、非随机分配的因果识别，也不能当成外部样本复现。Fisher概率仅为特定条件分布下的描述性检验，不表示制度因果效应成立的概率。

对照关系：1989原始博士论文的29社区、14官僚、4其他分类与1993官僚14例分组一致。1993表2的6/8与0/6进一步解释「地方集体选择权」的观察关联。Ostrom2010 p650的12政府、25农民、7/12与40%不一致仍未解决；1993表2并未提供2010正确分母，也不能推定出版错误原因。Tang1994正式章pp229至234仍未通过出版社授权全文逐页核验。

## 4. 竞争解释、四层联系、测量与可证伪条件

竞争机制一：地方治理权改善信息适配和规则执行。机制二：原本合作较好的地方更容易建立自治机构，存在反向选择。机制三：水资源、地形、上游调度与资金决定组织形式和维护绩效。机制四：行政登记/分类与实际运作脱节，官方机构存在不代表实质规则制定权。Mann1984的基础设施/专断双维、Mitchell1991的国家社会边界构成此前已读的理论对照；Scott1998原著仍仅书介级，不把它伪装成已读正文。

未来区分需要设施唯一ID、各时间切片、治理权实际行使证据、地方会议和规则变更记录、旱季水量、上游调度、资金、人员流动、绩效编码原表及缺失机制。若规则变更先于维护改善且可排除同时变化的供水和组织选择，才可能增强治理机制证据；仍需适当对照或可识别设计。当前仅有选择性案例及汇总表，无因果识别。

个体层：劳动与规则遵守的成本和信任；群体层：组织与共同决策、监督；制度层：正式权限与实际规则修改权、问责；历史层：水文冲击、工程折旧、地方与中央治理安排的长期变迁。只作局部关联，未开展R系列拟合或项目级融合。

## 5. 执行状态和后续

原始机构工作论文指定正文及Table 2核验：COMPLETE。独立人工算术8项PASS。1994正式章节与2010数字分母闭合：PARTIAL。真实微观数据重算、独立现实因果估计、历史留出、预测、R E1/E2/E3升级：NOT_RUN。C009于2026-11-01完成、D002于2026-10-26（2026-W44）完成，本轮只读，不创建新编号。R333至R340 P0仍有未采纳验收门，Codex PR均未合并；R073/PESEN v0.1保持冻结。未触发CI或付费服务，账单未核验。

下一步优先转换到弱覆盖的政治人类学原作：Scott (1995), “State Simplifications: Nature, Space and People”, *Journal of Political Philosophy* 3(3):191–233, DOI:10.1111/j.1467-9760.1995.tb00035.x。出版社已核正式书目，全文仍未读；1998著作的原著章节亦待合法获取。并行保留Tang1994正式章pp229至234的出版社授权全文与Ostrom2010分母核验。已有原始版本差异与未读项须明确保留。