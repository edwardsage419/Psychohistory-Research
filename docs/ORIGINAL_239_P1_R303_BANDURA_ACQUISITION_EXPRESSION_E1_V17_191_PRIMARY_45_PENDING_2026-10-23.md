# 心理史学R303社会学习理论：原作者证据与本项目人工机制分离，原239 v1.7审计

日期2026-10-23 Asia/Taipei。按既定「全部R系列学习研究→统一归纳分类→最后才原创熔炼」次序。**目前没有原始239项整体科学正式结题，也没有新真人/动物E2或历史E3证据。**

## 第一手理论与严格独立机制

原始候选**03-001 Social Learning Theory（P1）**。Bandura(1965) *Influence of models' reinforcement contingencies on the acquisition of imitative responses*, DOI https://doi.org/10.1037/h0022070。原实验中儿童观看榜样被奖励/惩罚/不受后果，再测试自发模仿，随后用明确奖励引导再现；自发表现差异与后续被激励后获得的模仿反应差异不是同一个心理量。[完整原论文再印](https://www.psychologywizard.net/uploads/2/6/6/4/26640833/bandura_1965.pdf)及[PubMed原刊文献条目](https://pubmed.ncbi.nlm.nih.gov/14300234/)已核对。本项目**没有取得Bandura1965原儿童数据、没有复算其人数和效果量，也没有复现原作者实验因果估计**。

旧有[**R063 Najar2020 社会模仿强化学习**](../research/R063/R063_EVIDENCE_AUDIT.md)研究主要审计metaVS/VS2的动态社会学习率、作者源码与Figure6作者汇总值，不能因为出现“社会/模仿”字眼而冒充Bandura1965的独立人类样本或原机制试验。R303不输入Q价值、示范者可靠性反馈、作者Najar原CSV或任何真人数据。

## 事前冻结与R303数学计算

[冻结前研究方案](../protocols/R303_BANDURA_OBSERVATIONAL_ACQUISITION_PERFORMANCE_486_SOURCE_PRESCORE_FREEZE_2026-10-23.md)在[commit5adc32ae](https://github.com/edwardsage419/Psychohistory-Research/commit/5adc32ae7c91c150fe82bb16f99a059d2a62e991)早于研究代码/结果写入。原创于本项目的**玩具模型**取注意A、保留R、执行能力P、基础动机M各∈{0,1/2,1}，三个模型后果惩罚、无后果、奖励设定人为的自发反应权重1/4、1/2、1。模型人为规定，观察学习痕迹概率A×R，潜在可表现概率A×R×P，自发表现概率A×R×P×M×后果权重；给所有条件再加统一的激励后，表现概率A×R×P（不改变已获痕迹）。**该乘法公式、权重均是项目假设，不是Bandura原作者的统计模型或测得的被试参数。**

81个四门控参数世界×3后果状态×2表现阶段=**243个人工世界，486条独立标号人工原source**。门控条件A=R=P=1、M=1/2时，潜在获得痕迹恒1；榜样获奖、无后果、受惩罚时自发模仿为1/2、1/4、1/8，人工统一激励后3种情境都为1。A=0/R=0时无法获得观测痕迹；P=0时即使痕迹1也无法表现；M=0时自发全被抑制但可在统一激励后表现。**这一人工反例只是揭示“学习痕迹与表现概率可分离”的形式逻辑，不是对真实学习痕迹存在、人的注意概率和儿童模仿率的证据**。

## 归档、独立复算和修复历史

[研究报告](../research/R303/R303_SCIENTIFIC_REPORT_2026-10-23.md)、[486条完整人工source](../research/R303/R303_ALL_486_ORIGINAL_OBSERVATIONAL_SOURCE_PHASES.csv)、[243世界结果](../research/R303/R303_EXACT_ACQUISITION_VS_EXPRESSION_RESULTS.json)、[双原数据SHA256](../research/R303/R303_MACHINE_RECEIPT.json)、[正式机读验收](../research/R303/R303_FINAL_ACCEPTANCE_STATUS.json)、[独立五伯努利门控枚举与恶意篡改审计](../research/catalogue_audit/independent_r303_source_audit.py)齐全并永久归档GitHub main。

[首次run39934080577](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39934080577)**failure**，两个Python版本各1473项主数学测试全部通过，但在输出CSV哈希时变量名被门控参数覆盖造成AttributeError，不能认为该首次实验档案完成。修复[commitf49c949b](https://github.com/edwardsage419/Psychohistory-Research/commit/f49c949b3b9ff95b3c13b87a22b611a490083087)仅处理文件路径局部变量，未修改事前协议或概率机制。随后完整重新运行[GitHub Actions run39934165046](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39934165046) **3/3 jobs completed/success**：Python3.11+3.12各1473项主模型测试，独立五个随机门控全枚举17项审计各一次，第三独立作业完整重算486个原source并校验SHA256后永久归档[commit8b1c570e](https://github.com/edwardsage419/Psychohistory-Research/commit/8b1c570e13921d4c4170d7eec48f36ea76cbd96e)。首次失败与修复可追溯，不虚报为初次全绿。

## 239原候选证据索引更新

| 来源层级 | v1.6 R302后 | v1.7 R303后 |
|---|---:|---:|
| 已确立原候选主R来源 | 190 | **191** |
| 共享有限数学、非独立主R | 3 | 3 |
| 只有较早范围有限关联 | 4 | 4 |
| 已核材料未见该候选逐项来源 | 42 | **41** |
| 待核候选专属主R来源 | 46 | **45** |
| 原始239候选数 | 239 | 239 |

[完整原始239行证据溯源交叉索引v1.7](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.7_2026-10-23.json)相对[v1.6](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.6_2026-10-23.json)只更改原始03-001一个候选的来源/验收字段，原目录名称、ID、顺序及优先级未变。旧R063证据归属仍在原模型02-005旧有限研究路径上。**191项主R来源关联不等于191个独立的人类模型实验复现**。

[当前45项来源待核队列](ORIGINAL_239_PENDING_45_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv)，P1 **18**、P2 **27**，下一个是**03-003 Social Identity Theory**，紧随其后03-004 Self Categorization Theory。须分别定位Tajfel/Turner原作及任务条件，避免把社群类别偏好、在群身份和自我分类解释视为同一数学机制或伪造真实实验。

[原239来源独立审计程序](../research/catalogue_audit/verify_p1_r303_crosswalk_v1_7.py)和[GitHub Actions目录审计run39934442021](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39934442021) **3/3 completed/success**，双Python每个16项完整原239 ID、单行变更、SHA、既有R063关联验证，第三独立全部486源状态审计。未改变R073和PESEN v0.1冻结协议。
