# 心理史学：R305自我分类、R306群体极化与既有R072声誉证据复用——原239目录v2.1科研归档

日期2026-10-23 Asia/Taipei。继续用户决策顺序：**先完成此前既定全部R模型学习/逐项研究→再统一归纳分类→最后开展原创熔炼**。个人辅助决策系统实际构建暂缓。R073/PESEN v0.1仍冻结，原239全部科学正式结题**未成立**。

## 1. 两项新增有限人工研究与一项已有证据复核

| 类别 | 原239候选及对应来源 | 人工原source新增加 | 科学范围与审计 |
|---|---|---:|---|
| 新科研R305 | **03-004 Self Categorization Theory** | 486条，243完全人工分类世界 | 比较背景、类别原型适配、规范适配、认知可及性、个人层级回退，**E1仅限项目玩具模型** |
| 现有R072重新归属 | **03-010 Social Sanction and Reputation Mechanisms** | **0条新source、0项新研究** | 重新核对旧R072原 E1 **11,664人工场景/279,936模拟决策**、真人附件REV007匿名汇总描述性一致与REV008代码本阻塞 |
| 新科研R306 | **03-012 Group Polarization Models** | 648条，216完全人工讨论世界 | 意见平均化、成员社会比较、支持/反向论据、共识后群体均值转移，**E1仅限项目玩具模型** |

本轮新创建**486+648=1,134条原始完整人工来源行**，而非1,134位真实参与者；先前R072的11,664人工世界只经独立校验，没有被重复计数为本轮新源。新R305+R306两套Python3.11/3.12合计**(1473+1959)×2=6864项实际主数学unittest通过**，另执行独立源审计测试与第三CI来源复验。没有新增真人/动物E2或历史E3。

### R305：Self Categorization Theory，不等于R304社会认同效用

理论首要来源Turner(1985), *Social categorization and the self-concept: A social cognitive theory of group behaviour*, *Advances in Group Processes* 2:77–122；Turner等人(1987), *Rediscovering the Social Group: A Self-Categorization Theory*；Turner等人(1994), DOI https://doi.org/10.1177/0146167294205002。本轮完整[科学报告](../research/R305/R305_SCIENTIFIC_REPORT_2026-10-23.md)明确声明数值/乘法认知得分为项目自己设计，不是原作者真人分类记录或拟合公式。

四个虚拟对象，P/Q两种固定分类，在X、MID、Y比较情境中的类别内和跨类别配对差异构成MC=组间均值距离/组内均值距离。X的P/Q对比适配为4/5/8，Y为5/8/4，中间为1/1。固定规范/认知可及性全1和个人阈值1，分类选择依次**P→PERSONAL→Q**。负对照规范适配P为0会阻断原本较优的P，可及性为0全部退回PERSONAL。比较情境可重排行为类别只是在这套有限人为公式里成立；没有实测心理分类层级。

冻结commit [a4dfc1f5](https://github.com/edwardsage419/Psychohistory-Research/commit/a4dfc1f582c9a58eec6cf45b63a34f577800e0eb)，[486条原source](../research/R305/R305_ALL_486_ORIGINAL_SELF_CATEGORIZATION_SOURCE_CELLS.csv)和[机器验收](../research/R305/R305_FINAL_ACCEPTANCE_STATUS.json)通过[科学三job CI39937267071](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39937267071)，来源永久[归档commit c57d76c1](https://github.com/edwardsage419/Psychohistory-Research/commit/c57d76c1d8e42b95e83eff0ffe72f23a9803da7c)。独立审计从四对象六对距离开始逐值重算，18项反例测试；模型1473项unittests每Python版本通过。

### 原候选03-010：沿用原R072，保留“有真人原件”和“无真人机制辨识”两个同时为真的事实

不重复研究。[专门逐项科学边界审计](ORIGINAL239_03_010_EXISTING_R072_E1_AND_REV008_CODEBOOK_SCOPE_AUDIT_2026-10-23.md)先行冻结[commitc8427f47](https://github.com/edwardsage419/Psychohistory-Research/commit/c8427f47cdbb0fe7edbda8de7cd7faf2b4737df1)。R072既有[正式E1 11,664世界/279,936事件JSON](../research/R072/R072_E1_FULL_11664_PUBLIC_REPUTATION_RESULTS.json)，源SHA256=6137894586488cabcc684ae350e692ccd0c6c2a731d6e0787153197de3a8868a；9种公开规范×渠道完整固定合成计算。IMAGE_SCORING总体帮助率三渠道均0.5，但逐配置准确与伪造公告差异912/1296，证明在**这个有限人工模型**里宏观均值可掩盖局部变化。

R072后续[REV007真实来源匿名一致性](../research/R072/R072_POSTCLOSURE_S8_REV007_GROUP_RESPONSE_PARITY_STATUS.json)已固定PLOS官方S8原始 XLSX 38,647字节/SHA256，匿名八组(n,回复候选)多集与作者Table1已出版汇总一致，189候选请求、89候选回应，这是真实字节来源与事后描述一致的积极证据；**但**[REV008独立编码本证据](../research/R072/R072_POSTCLOSURE_S8_REV008_AUTHOR_CODEBOOK_GATE_STATUS.json)仍为BLOCKED_NO_UNAMBIGUOUS_SOURCE_CODEBOOK，不能独立把匿名数值组分到serving与neutral处理。禁止用已知发表回应数倒推处理分配再自我证实因果效应。真实社会信誉机制E2**NOT_IDENTIFIED**，历史E3 OPEN。既有[R072首次结题机读快照](../research/R072/R072_FINAL_ACCEPTANCE_STATUS.json)中“原真人附件未取到”的历史字段保留不覆盖，新来源阶段独立记录。

[现有R072原源+REV008跨时点科学门CI39938047785](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39938047785)三个作业成功，严格核对上述E1/真实S8证据限度，**没有开办R306声誉重复模型**。

### R306：Group Polarization，不把立场反转错误计为极化

原文Moscovici & Zavalloni(1969) DOI https://doi.org/10.1037/h0027568，Myers & Lamm(1976) DOI https://doi.org/10.1037/0033-2909.83.4.602，Burnstein & Vinokur(1977) DOI https://doi.org/10.1016/0022-1031(77)90002-6。项目在三名人工代理意见∈{−1/2,0,1/2}、全部27有序三元组上独立设置4种讨论机制和支持/反向论据，形成**216人工世界，648条完整人员来源**；原创公式是群体初始平均加上成员最强既有方向的比较影响与新论据±方向影响的凸组合，**不是原作者拟合统计模型**。

示例三名意见原为(1/2,1/2,1/2)，其群体平均1/2：普通平均化、仅参照最强现有成员都不改变均值，支持性论据令其变为3/4（同方向极化），反向论据令其变为−1/4（方向反转，**不计为原方向极化**）。对(0,0,1/2)，原均值1/6，社会比较后1/3、支持论据后7/12、合并影响后3/4、反向论据后−5/12。任何原始均值=0的三元组模型保持均值0，防止将无方向初始化硬称成极化。以上均为人为指定数学机制，不是对真实群体讨论后态度漂移或历史政策结果的检验。

冻结commit[1db7fc7c](https://github.com/edwardsage419/Psychohistory-Research/commit/1db7fc7cc12cbf1bbec67e3df25c634d689c25b6)，[完整科学报告](../research/R306/R306_SCIENTIFIC_REPORT_2026-10-23.md)、[648人造来源](../research/R306/R306_ALL_648_ORIGINAL_POLARIZATION_PERSON_SOURCES.csv)、[独立凸组合/类别审核](../research/catalogue_audit/independent_r306_source_audit.py)、[机读验收](../research/R306/R306_FINAL_ACCEPTANCE_STATUS.json)均在[科学三job CI39938339913](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39938339913)成功后永久归档[commit a3b9b9be](https://github.com/edwardsage419/Psychohistory-Research/commit/a3b9b9befe6f98610dba796f68f3eed0c94ed85e)。Python3.11/3.12各1959项主模型unittests，另每版本17项独立反例审计并由第三作业再查全部源码状态/哈希。

## 2. 原始239模型来源逐项对照v1.8→v1.9→v2.0→v2.1

| 原候选研究来源状态 | R304后v1.8 | R305后v1.9 | R072已有证据复用v2.0 | R306后v2.1 |
|---|---:|---:|---:|---:|
| 已有主R研究来源关联 | 192 | 193 | 194 | **195** |
| 共享数学但非独立主R | 3 | 3 | 3 | **3** |
| 旧有限范围证据关联（无专属主R） | 4 | 4 | 3 | **3** |
| 已核材料暂未见逐项来源 | 40 | 39 | 39 | **38** |
| 尚待核主R来源链接 | 44 | 43 | 42 | **41** |
| 原始唯一候选 | 239 | 239 | 239 | **239** |

[最新全部239行来源交叉索引v2.1](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v2.1_2026-10-23.json)仅相对v2.0更新**03-012**一行R306；v2.0相对v1.9只更改**03-010**并指回**R072已有研究**；v1.9相对v1.8只更改**03-004**指向R305，原始239模型目录不改。早期R063、R073、R304、R305以及R072旧真人编码来源完整保留。**195条主R关联表示档案证据可查，不是195次真实人类心理学模型重复实验或跨尺度验证。**

[最新41项原候选待核队列](ORIGINAL_239_PENDING_41_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv)，P1 **14**、P2 **27**，下一项原编号**03-016 Minority Influence Models**，须核实原始少数派影响研究、稳定性/一致性机制及负对照，避免与前述群体极化、群体身份混同。

实际核验的**五个独立工作流15个成功job**：
- [R305科学 39937267071](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39937267071)；
- [R305目录v1.9 39937550180](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39937550180)；
- [已有R072来源/真人代码本限度v2.0 39938047785](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39938047785)；
- [R306科学 39938339913](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39938339913)；
- [R306目录v2.1 39938681663](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39938681663)。

以上成功仅证明**数学执行、固定原source完整和逐项科研范围标注**。没有新增真实人/动物E2和历史E3，R072独立处理字典门未闭合。全R系列研究尚未结束，不启动统一分类、个人决策系统或原创模型熔炼。R073及PESEN v0.1继续冻结。
