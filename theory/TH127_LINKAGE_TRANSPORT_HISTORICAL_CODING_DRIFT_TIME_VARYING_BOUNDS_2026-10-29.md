# TH127 跨机构链接质量可运输性、历史编码漂移与时变识别集

研究及英文来源检索日期：2026-10-29（Asia/Singapore）。状态：THEORY_NOTE_BOUNDED。
目标键：(theory,TH127:linkage-transport-and-code-vintages,no-R-freeze,subgroup-transport-time-varying-measurement-bounds)。
本轮先读main HEAD、最近提交、理论索引、TH126、C006、D002、R262 S58最近提交及开放Codex PR标题摘要；相关PR未合并的工程审计仅作待审查证据。已知TH126部分识别和去重反例，TH127聚焦跨机构/分层误差可迁移性与历史编码时间断点，属于非盲态互补理论研究。

## 一、原始文献与核验层级

A：本轮直接阅读开放原刊指定方法/结果章节或官方原始政策全文；B：核验原始摘要、大学机构存档或开放检索结果；I：前轮已审读材料，仅作背景；S：本项目独立人工反例。检索日期均为2026-10-29，全部英文网页。

1. [A] Randall, Sean, Adrian Brown, James Boyd, Rainer Schnell, Christian Borgs & Anna Ferrante (2018). “Sociodemographic differences in linkage error: an examination of four large-scale datasets.” *BMC Health Services Research* 18:678. DOI https://doi.org/10.1186/s12913-018-3495-x 。原刊全文 https://link.springer.com/article/10.1186/s12913-018-3495-x 。直接审读Methods、Results、Discussion、data availability及其公布的分层recall/precision；四套数据在各自内部去重，没有跨四库链接；原始微观数据因隐私限制不公开。
2. [A] U.S. Centers for Medicare & Medicaid Services (CMS), *Measures Management System: International Classification of Diseases (ICD)*, 页面更新2025-05。https://mmshub.cms.gov/measure-lifecycle/measure-specification/specify-code/ICD 。直接审读历史代码保存、2015-10-01切换、跨版本映射限制；是现行官方方法指导，不能代替2015年当时逐项业务执行记录。
3. [A] U.S. CDC NCHS, *ICD-10-CM/PCS Transition: Background*, 历史归档。https://archive.cdc.gov/www_cdc_gov/nchs/icd/icd10cm_pcs_background.htm 。直接审读诊断与住院程序编码区别、2015-10-01切换、死亡统计早在1999年采用ICD-10；死亡与发病编码时钟不同。
4. [B] Yang, Hannah, Emilia Pasalic, Peter Rock, James W. Davis, Sarah Nechuta & Ying Zhang (2021). “Interrupted time series analysis to evaluate the performance of drug overdose morbidity indicators shows discontinuities across the ICD-9-CM to ICD-10-CM transition.” *Injury Prevention* 27(S1):i35–i41. DOI https://doi.org/10.1136/injuryprev-2019-043522 。作者大学公开摘要 https://scholarworks.gvsu.edu/ph_articles/9/ 及原刊检索摘要；本轮未通读论文全部回归表。作者分析六州数据，发现编码转换可能造成测量不连续。
5. [B] Hsu et al. (2021). “Effect of ICD-9-CM to ICD-10-CM coding system transition on identification of common conditions: An interrupted time series analysis.” *Pharmacoepidemiology and Drug Safety*. DOI https://doi.org/10.1002/pds.5330 。原刊摘要 https://pubmed.ncbi.nlm.nih.gov/34258812/ 。台湾32类疾病的两种映射方案分别有19类和11类出现水平显著变化；摘要核验，全文未读。
6. [B] “Impact of ICD-9 to ICD-10 Coding Transition on Prevalence Trends in Neurology” (2021). *Neurology: Clinical Practice*. DOI https://doi.org/10.1212/CPJ.0000000000001046 。原刊摘要 https://pubmed.ncbi.nlm.nih.gov/34840874/ 及开放检索 https://pmc.ncbi.nlm.nih.gov/articles/PMC8610531/ 。原刊报告16种神经疾病中6种跨编码转换的横截面患病率发生显著变化；全文访问时出现验证页面，本轮只按原刊摘要及公开检索节选引用。
7. [B] Pearl, Judea & Elias Bareinboim (2014). “External Validity: From Do-Calculus to Transportability Across Populations.” *Statistical Science* 29(4):579–595. DOI https://doi.org/10.1214/14-STS486 。作者机构摘要 https://cris.technion.ac.il/en/publications/external-validity-from-do-calculus-to-transportability-across-pop/ ；原作开放稿 https://arxiv.org/abs/1503.01603 。本轮核验原刊摘要；其因果效应transportability框架不能自动证明链接误差可迁移。
8. [I] Harron et al. (2017). “A guide to evaluating linkage quality for the analysis of linked data.” *International Journal of Epidemiology* 46(5):1699–1710. DOI https://doi.org/10.1093/ije/dyx177 。https://pmc.ncbi.nlm.nih.gov/articles/PMC5837697/ 。前轮TH126已审读，作为链接误差与质量审计背景；本轮无新增逐页审读。

## 二、16项条件性理论命题、竞争解释与适用边界

T127-01 [1] 跨机构迁移链接误差率需要核对匹配字段、缺失模式、候选配对生成、阈值、人员流动和机构信息系统；仅共享算法名称不保证错误分布相同。
T127-02 [1] 原作四套澳大利亚行政数据的年龄与偏远程度差异方向较一致，但社会经济地位差异方向可跨库逆转；不同数据生成机制可能支配表面群体规律。
T127-03 [1] NSW医院数据中私人医院姓名字段缺失被作者提出为反向社会经济梯度的候选解释；这是一项有原文支持的机制推测，缺少随机化分离，不能称为已证明的唯一原因。
T127-04 [1] 一套数据的高精度、召回率不意味着另一套数据同等表现；pair-based precision/recall还不能直接当作episode-level结果偏差。
T127-05 [1] 以已链接和未链接记录的人口特征差异估计链接误差，会混入目标记录根本不存在的覆盖缺失；必须区分coverage、missed link和false match。
T127-06 [1] 原刊以既有高质量链接键作为truth-set，仍承认金标准可能存在误差；外推时需要审计验证样本是否覆盖目标机构与时期。
T127-07 [1,7] 可运输性至少需要条件误差机制在已观察分层变量给定下足够稳定，且目标分层存在共同支持；源总体的平均链接率不能直接迁移到目标总体。
T127-08 [7，方法推断] Pearl与Bareinboim处理的是结构因果效应外部有效性；链接算法的错误率迁移属于测量机制问题。两者可用选择图表达异质性，但不能把因果transport公式无条件套到误配率。
T127-09 [2,3] 美国2015-10-01的诊断及住院程序编码切换是明确的行政时钟；死亡统计自1999年采用ICD-10，研究须先固定结果类型和编码版本。
T127-10 [2] CMS明确指出ICD-9-CM与ICD-10-CM/PCS不存在简单一一对应的crosswalk；回填历史记录可能引入不可逆的分类误差，应保存原始vintage。
T127-11 [4,5,6] 原刊不同疾病、不同指标和不同映射方案表现各异；历史编码切换不能被当作所有疾病统一固定比例的测量调整。
T127-12 [4,5,6] 编码转换与真实患病率、服务利用、诊断实践、报销激励可同时变化；仅有转换前后时间序列无法唯一分解测量与真实机制。
T127-13 [1,2] 若同一时期更换标识字段和诊断编码，链接误差与结果误分类会联合作用；只校正其中一个过程可能仍留下趋势偏差。
T127-14 [1,5] 分层错误率的跨期可比需要相同episode定义、机构覆盖、分母、验证设计及结果代码集合；否则所谓链接改善可能只是分母重定义。
T127-15 [5,6，方法推断] 分段回归和负对照可帮助发现测量断点，但须处理季节性、同步政策、提前适应、编码切换执行滞后和负对照排除限制；断点显著本身不是纯编码因果证据。
T127-16 [综合推断] 四层联系：个体层为身份和诊断记录的动态可见性；群体层为年龄、地区和机构构成；制度层为字段标准、数据共享与报销规则；历史层为版本更替、长期趋势和机构重组。所有跨层主张须分别核对机制、时间及证据。

## 三、8项独立算术与人工识别审计

E127-01 [A1公布分层数值，独立算术] NSW急诊大城市recall 0.984、偏远地区0.967，相差1.7个百分点；漏配比例分别1.6%和3.3%，后者约为前者2.0625倍。属于记录对recall，非患者死亡风险。
E127-02 [A1公布分层数值，独立算术] SA急诊大城市recall 0.971、偏远地区0.918，差5.3个百分点；漏配比例2.9%与8.2%，约2.8276倍。地区人群构成和录入方式尚未独立分解。
E127-03 [A1公布分层数值，独立算术] WA住院大城市recall 0.963、偏远地区0.896，差6.7个百分点；漏配比例3.7%与10.4%，约2.8108倍。不能把三州差异当作同一因果处理效应。
E127-04 [A1公布分层数值，独立算术] WA住院偏远地区precision 0.944，城市/区域约0.998，差5.4个百分点。相应错误发现比例5.6%与0.2%，比值28倍；分母是算法判为匹配的记录对，不是所有就诊事件。四库原始记录数6,772,949+19,874,083+4,304,459+813,839=31,765,330，只是记录行数之和，非独立人或跨库episode数。
E127-05 [S，群体构成变化] 两分层的条件链接召回率固定为0.99和0.90。源地区90%在高召回层，平均0.981；目标地区仅10%在高召回层，平均0.909。即使分层条件机制完全不变，总体差7.2个百分点；若条件机制也变，重加权不能保证校正。
E127-06 [S，测量断点与真实变化不可区分] 二元真实结局率在两期均0.5。第一期灵敏度0.8、特异度1.0，观测阳性率0.4；第二期灵敏度1.0、特异度0.8，观测率0.6。另一个世界测量完全准确、真实结局率由0.4变为0.6。两世界观测一致，缺少验证样本时不能唯一归因。
E127-07 [S，时变缺失识别集] 期0有100个episode、80个结局可核、40个成功，真实成功率界[0.40,0.60]；期1有100个episode、60个结局可核、30个成功，界[0.30,0.70]。期1减期0的变化界为[-0.30,+0.30]；可见成功率均0.5，不能推断总体无变化。
E127-08 [S，非双射编码] 假设旧版仅有代码A，旧期100例A；新版将A拆为A1/A2，后期分别60/40。若只追踪A1会出现40%虚假下降；合并A1+A2为100例则无变化，但若A2同时纳入新诊断人群，合并也可能高估。缺少双编码验证样本时映射无法自动识别真值。

## 四、竞争理论、识别边界与可执行验证

竞争解释：人口构成改变、字段质量改善或恶化、医疗机构数据覆盖改变、编码映射变化、真实疾病变化、诊断行为和医保报销激励变化。原刊Randall等发现分层阈值调整对质量改善极小，提示单靠分组阈值调参未必有效；这一结果限于其四套数据及指定链接方法。

未来候选验证清单：
1. 固定person/episode/record-pair目标单位、时间窗口、源机构与目标机构分层、旧版与新版字段词典。
2. 获取公开无身份标识的分层precision、recall、coverage和真值抽样方法；未提供时只报告不可识别或保守界。
3. 保存原始ICD版本、映射算法版本、诊断字段位置及生效时钟；对跨期结果采用多个公开代码集合进行敏感性检查。
4. 对跨期指标预设真实结果不变、仅编码变化、真实结果与编码同时变化的竞争世界，寻找独立验证子样本或合理负对照。
5. 报告目标群体组成重加权的共同支持、各组误差界及未测异质性敏感性；避免把统计外推写成真实因果效应。

## 五、证据和协作边界

本轮新增开放原刊完整指定章节直接阅读1项，官方英文机构原始政策/方法页面直接阅读2项，原刊或作者机构摘要核验4项，沿用TH126原刊1项。原刊分层数字算术4项，人工反例4项。没有下载患者级、个人身份、用户健康财务关系等敏感数据。没有运行GitHub Actions或任何收费服务。

真实微观记录独立复算0，新增独立因果估计0，前瞻性预测验证0，R系列E1/E2/E3新增均0，模型熔炼0。Randall等原始微观数据因隐私不公开，若公开汇总不足则明确记录阻塞；历史编码断点研究没有独立底层数据，不能断言特定历史患病率实际变化。

C006（2026-10-29）和D002（2026-W44）已完成，本轮只读并核验blob。R262 S58主线提交只作协调观察，未修改R研究与冻结协议。开放Codex PR含R257 S53比较器问题，仅为待审查非盲态工程证据，不能视为主线已修复。

下一研究队列：TH128 分层链接误差与诊断误分类联合界、双编码桥接样本设计和跨期负对照有效性。
