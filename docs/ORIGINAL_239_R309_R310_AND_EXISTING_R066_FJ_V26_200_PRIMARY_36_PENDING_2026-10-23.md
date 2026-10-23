# 心理史学 R309/SIR、R310/Voter 及已有 R066/FJ 真人证据归属——原239目录v2.6

2026-10-23 Asia/Taipei。严格继承既定「先完成全部R模型学习/验收→再统一归纳分类→最后原创熔炼」。原239全部理论科学结题 **NOT_ESTABLISHED**，个人辅助决策系统暂缓，R073/PESEN v0.1均保持冻结。**本轮两项新人工E1机制研究，一项已有真人E2来源重分配，没有增加任何真人或动物观察，也没有外部实验E3。**

## 新增研究R309与R310（均在预先冻结后运行、完整来源和独立CI）

| 项目 | 原始239候选 | 人工原始世界 | 完整人工source | Python3.11和3.12主unittest | 成功工作流 |
|---|---|---:|---:|---:|---|
| R309 离散有限SIR | **04-006** | 189 | 1,134 | 3,417×2 | [science39955168677](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39955168677) |
| R310 随机图Voter | **04-008** | 48 | 416 | 1,262×2 | [corrected science39955796344](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39955796344) |

**合计1,550条新人工原source和9,358项Python双版本主单测通过**，并额外执行每研究17项独立篡改测试、第三独立作业重构全部数据哈希。人工source是所有备选事件而非1,550个真实人/个体，跨世界不能等价看作独立自然样本。

R309原理论 Kermack & McKendrick(1927), *A contribution to the mathematical theory of epidemics*, DOI https://doi.org/10.1098/rspa.1927.0118；但本轮是五虚拟人同步离散独立接触与旧感染者恢复，**不是原作者连续理论原封实现**。冻结[commit aec096d7](https://github.com/edwardsage419/Psychohistory-Research/commit/aec096d72f66c44ac1b13dd5ed1ce9d169f21aac)。S3,I2,R0、每个感染接触p1/2、旧感染者恢复q1/2时每易感者被感染概率3/4，下一步期望(3/4,13/4,1)，概率1/256可以没有新感染且两名旧感染者全部恢复，因而I=0时仍有3个易感者。p=q=1时下一步(0,3,2)而不是错误的(0,0,5)。独立审核穷举**11,664个二元接触/恢复人工微配置**，对**1,134个有标签转移source**全数精确比对。结果永久档案[54997770](https://github.com/edwardsage419/Psychohistory-Research/commit/549977708267ac455d0ac61ec3fee0d0330b43ce)、[科学报告](../research/R309/R309_SCIENTIFIC_REPORT_2026-10-23.md)和[机读验收](../research/R309/R309_FINAL_ACCEPTANCE_STATUS.json)。没有真实疾病、真实文化传播或政策干预检验。

R310依据Clifford & Sudbury(1973), *A model for spatial conflict*, DOI https://doi.org/10.1093/biomet/60.3.581，Holley & Liggett(1975) DOI https://doi.org/10.1214/aop/1176996306。冻结[commit782990a1](https://github.com/edwardsage419/Psychohistory-Research/commit/782990a1cae101a3c0fd5ba37f89dc8ed9c2078c)，用四虚拟节点所有二元意见配置、路径4/环4/完全4三图，逐一列举416个「均匀选择目标节点，再均匀选择邻居复制」人工更新事件。无向图上节点度加权1意见比例期望守恒，但不规则PATH4的**普通**1比例并非必然守恒：初态(1,0,0,0)为1/4，下一步期望7/32；度加权比例为1/6，下一步仍1/6。规则CYCLE4和COMPLETE4普通比例则保持1/4。没检验真人选民或现实意见网络。[首次科学CI39955723523](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39955723523)因独立审核程序将CYCLE4相同边集合排序为另一序列化字节而**failure**；保留首次失败，经[纯审核器序列化修复17a14103](https://github.com/edwardsage419/Psychohistory-Research/commit/17a14103c9f01f1b774883de77df831f759c7792)后新[三job科学CI39955796344](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39955796344) success；模型协议、科学方程、原始源数据不变。[原source永久归档2dc71bae](https://github.com/edwardsage419/Psychohistory-Research/commit/2dc71bae2a70dd3affc892e33712d0541822525b)及[科学报告](../research/R310/R310_SCIENTIFIC_REPORT_2026-10-23.md)、[机读验收](../research/R310/R310_FINAL_ACCEPTANCE_STATUS.json)。

## 本轮最有实证价值的历史来源关联：原04-010 Friedkin–Johnsen → 已有R066

原模型Friedkin & Johnsen(1990) *Social influence and opinions*, DOI https://doi.org/10.1080/0022250X.1990.9990069。R066研究包早已完成数学E1，且实读Larson–Lewis(2026)乌干达**16村、1,872条完整基线与末次态度测量**，Harvard Dataverse原始doi:10.7910/DVN/RAHSVM V1.0 CC0，确实进行每折15村训练/1村留出的内部跨村预测。作者家庭边构造R/Python独立全集对照通过。[冻结于真实计分前的R066留村协议](https://github.com/edwardsage419/Psychohistory-Research/commit/85b8abb398f2e4cc060b6e4b36dc6880893455a1)、[真实CI38866210819](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38866210819)成功，保留原已归档匿名聚合结果。主要16村等权预测MSE：持久性+漂移0.0422710340、DeGroot0.0286146166、**FJ0.0266149142**、HK0.0265478189。FJ个人行加权MSE0.0282227598、MAE0.1290151675。

**重要科学限制：**预测起点部分为干预后即时态度，并非完全在现场干预前预测；被留出的16村仍属同一研究而非独立外部队列，E3仍OPEN；HK使用全村信念接近邻居，**不**使用FJ的真实家庭网络边；HK宏观MSE领先FJ仅约0.000067，欠折级配对不确定性，不能得出HK因果机制胜出、FJ因果机制成立或历史事件可预测。模型训练村来源偏差、共同漂移和社会干预后的观测都可能影响得分。

本轮只进行了[原04-010严谨来源审核](ORIGINAL239_04_010_EXISTING_R066_FJ_INTERNAL_REAL_E2_SCOPE_AUDIT_2026-10-23.md)，事前冻结[commit05764e0c](https://github.com/edwardsage419/Psychohistory-Research/commit/05764e0c19edc0fcf2daf6e805f540ccbfcee266)。在原239目录中把04-010从仅有旧限定研究关联升级到主**R066**，原始R066 E1/E2、历史失败和源码**字节不改**；新真人来源行**0**、新真人复现**0**。本轮[三job跨Python来源范围CI39956477548](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39956477548)成功，独立检查原R066真实16村模型评分与不可支持的机制主张。04-012 HK仍旧范围待重新逐项核验，绝不由本次同时偷渡为完成。

## 原239目录累计状态与严格科研归属

| 可追溯来源层次 | v2.3 R308后 | v2.4 R309后 | v2.5 R310后 | **v2.6 既有R066来源复核后** |
|---|---:|---:|---:|---:|
| 已建立原候选主R来源 | 197 | 198 | 199 | **200** |
| 仅共享早期数学（非独立主R） | 3 | 3 | 3 | 3 |
| 只有有限旧范围研究关联 | 3 | 3 | 3 | **2** |
| 已核验材料无逐项来源 | 36 | 35 | 34 | **34** |
| 待核原候选专属主R研究 | 39 | 38 | 37 | **36** |
| 原始唯一候选 | 239 | 239 | 239 | 239 |

[最新全部239原始候选溯源交叉索引v2.6](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v2.6_2026-10-23.json)相对v2.5仅**04-010来源改为R066**，v2.5相对v2.4仅04-008指向R310，v2.4相对v2.3仅04-006指向R309；原始候选模型目录不改。[最新待核36项队列](ORIGINAL_239_PENDING_36_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv)中 P1 **9**、P2 **27**，下一项**04-011 Bounded Confidence Models**，然后04-012 HK（已有R066但需独立范围审计）和04-013 Deffuant Weisbuch。**200条是可追溯主R档案关联，不是200篇原作者论文的独立真人模型重做或因果确认。**

**五条全部完成且成功的三job GitHub Actions，共15个success作业**（首次R310失败另保留）：
[R309科研39955168677](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39955168677)、
[R309目录v2.4审计39955485250](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39955485250)、
[R310科研修复后39955796344](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39955796344)、
[R310目录v2.5审计39956069738](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39956069738)、
[R066既有真人E2来源目录v2.6 39956477548](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39956477548)。

结论：新增R309和R310有界E1完成，本轮通过完整验收把既有R066真正的人类**内部条件性预测E2**纳入正确原候选来源，却没有新增真人模型复现或历史E3。继续完成全部剩余R候选，最后统一分类和原创模型熔炼。R073/PESEN v0.1冻结。
