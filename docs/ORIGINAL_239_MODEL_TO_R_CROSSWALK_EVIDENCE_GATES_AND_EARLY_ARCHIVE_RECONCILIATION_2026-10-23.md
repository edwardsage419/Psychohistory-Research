# 心理史学：原239模型目录逐项R系列证据来源交叉索引、66项待核与R001—R064早期ZIP归档对账

日期：2026-10-23（Asia/Taipei）。性质：**来源与归档结构元数据审计**，不是239个模型全部掌握、原论文复现或E2/E3科学结题。已完成模型学习与当前证据的等级必须另外逐项验收；先全部R研究，再统一分类，最后熔炼的用户顺序不变。

## 一、不可替代的原始资料

1. 唯一原始239条目录：[MODEL_CANDIDATE_CATALOG_v0.1.json](MODEL_CANDIDATE_CATALOG_v0.1.json)，Git blob SHA1 `f312a618223a0e96f1dcc99df49fe169d2ff50b3`；目录239项、12类、P0/P1/P2原优先级保持字节未改。
2. 本轮[239行全目录逐项机读交叉索引](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v0.1_2026-10-23.json)：每项独立记录原catalogue id、学科、模型名、优先级、候选主R、来自实际README的Git blob SHA1及目录ID首次出现偏移、科学报告/正式验收文件**路径候选**、旧文献关系叠加表，以及**科研效度级别仍待独立确定**。
3. [10组R111—R285原README目录编号提取记录](audits/)：每条保留真正Git blob SHA及目录token偏移，按真实README来源追索；第一出现的目录ID仅为候选映射，绝不从token出现自动推定原论文完整复现。
4. 旧[2026-10-18原239知识条目叠加表](../research/KNOWLEDGE_239_CATALOG_EVIDENCE_OVERLAY_2026-10-18.json)只用于**有界早期相关关系**，不自动等同后期主研究包或E2/E3。
5. 历史[原239目录映射勘误](R_SERIES_CATALOG_MAPPING_CORRECTION_2026-10-22.md)：原目录不存在08-032、08-033，R208/R209是需要保留但不计原239条目唯一覆盖的补充研究。

## 二、实际逐项关联结果

| 原目录状态 | 条目数 | 正确解释 |
|---|---:|---|
| R111—R285实际README扫描，经过R173纠正与R208/209排除后，找到候选主R研究链接 | **173** | 已建立可溯源的研究包关联，**尚不等于173项全部科研结题** |
| 未找到后期候选主R，但旧2026-10-18叠加表有相关有界研究链接 | **7** | 已存在关联研究证据，需要核对是否为同一原模型、同一验证合同 |
| 两项来源都未给出一对一可核主R或早期叠加链接 | **59** | 当前扫描未确认，不可写作“从未研究”或“实验失败” |
| 合计 | **239** | 每个原catalogue ID恰有一行，目录顺序、类别、原优先级一致 |

原239候选目录的**66个尚无主R关联条目**按原优先级分：**P0三项、P1三十六项、P2二十七项**。完整原CSV队列：[66项待核主R链接、优先级及旧证据入口](ORIGINAL_239_PENDING_66_PRIMARY_R_LINK_TRIAGE_QUEUE_2026-10-23.csv)。

P0优先检查：
* **01-008 Softmax Choice Rule**：本次R111—R285的README主研究扫描无对应项，旧10-18叠加表也没有该条的直接链接；须查R001—R064早期知识包/强化学习或选择模型文档、实际公式与验证范围，不应直接新造“从未研究”结论。
* **02-002 Temporal Difference Learning**：旧叠加表关联[R063机制审计](../research/R063/R063_EVIDENCE_AUDIT.md)，但R063是特定原作者模仿学习源码语义审计，不能因名字相关就自动宣称完整TD-learning原方法已结题。
* **04-001 Granovetter Threshold Model**：旧叠加表关联[R069正式状态](../research/R069/R069_FINAL_ACCEPTANCE_STATUS.json)，另外[R118](../research/R118/README.md)主目录身份为03-019 Threshold Participation；概念邻近并不使R118自动成为04-001的主目录研究证明。须逐机制核验。

10组README的自动关联另检查出**R173**例外：R173当前README第一条目录数字为R174的预告07-016，但[R173的科学报告](../research/R173/R173_SCIENTIFIC_REPORT_2026-10-21.md)明确写原07-015 Cross Societal Comparison Models，故已手动按直接科研报告归属更正，且07-016仍归R174。对于R208/R209，保留其研究档案和不合原目录的历史标签作为纠错证据，但两个无效ID不计入239分子。

## 三、早期历史档案追回与“缺少目录”解释修正

早先[仅按research文件夹的结构快照](ORIGINAL_239_CATALOGUE_AND_R213_R285_REPOSITORY_COVERAGE_AUDIT_2026-10-23.md)列出R001—R285中48个缺少`research/Rnnn/`单独目录的早期编号。**本轮已明确证明该指标不是“研究包不存在”**。

读取[Library原ZIP清单](../manifests/LIBRARY_ORIGINAL_ZIPS_2026-10-15.csv)和[R001—R064历史轮次到ZIP索引](../manifests/RECOVERY_STATUS_R001_R064.csv)，检查仓库树中原ZIP路径：
* Library共**74**个ZIP文件记录，其路径全部存在于GitHub树；清单记录全部`zip_crc=PASS`。CRC状态系历史归档审计记录，本轮验证清单与路径存在，**没有重新对74份ZIP二进制独立执行CRC计算**。
* R001—R064有**64个轮次**，全部存在至少一份关联原ZIP；轮次索引共**73个不同原ZIP文件名**，均可以在74份Library原文件清单中找到，未发现重复计名或找不到对应的引用。
* 剩余的独立一份为`心理史学_模型研究第二轮知识包_v0.2.zip`，这是**额外知识包**，并非丢失的R编号或没有保存的资料。
* [原先2026-10-15恢复报告](../manifests/FULL_LIBRARY_RECOVERY_2026-10-15.md)确认历史原件和CRC，且说明ZIP CRC/字节来源归档不代表其中每个历史研究结果已被独立统计复算。
* 因而“48个独立目录缺位”应继续保留为**独立目录结构缺位**，不能归入“48个模型没有历史材料”；也不能反向用74个ZIP证明原目录239个模型逐项科学结题。

## 四、真正执行的独立审计及失败史

[可重跑Python3.11/3.12逐项验收程序](../research/catalogue_audit/verify_239_crosswalk.py)对每个目录条目独立测试原名称/类别/优先级、主关联R的readme路径、**当时原README真实Git blob SHA1和目录token偏移**、R173勘误、R208/209补充排除、旧关联路径存在性、239/173/7/59精确分类、R001—R064轮次与全部74 ZIP清单对应及额外知识包。

[最终GitHub Actions #39908490800](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39908490800)三job全部completed/success；Python3.11、3.12各**251项实际unittest**，共502项通过；第三独立审计直接读取目录JSON、239行crosswalk、173份README及其Git blob、64轮和74原ZIP路径，哈希独立相同。由GitHub机器人永久归档[机器审计结果](ORIGINAL_239_CROSSWALK_MACHINE_AUDIT_RESULTS.json)及[所有关键文件SHA256凭证](ORIGINAL_239_CROSSWALK_MACHINE_AUDIT_RECEIPT.json)，来源归档提交[2a1fd391](https://github.com/edwardsage419/Psychohistory-Research/commit/2a1fd3913a21c16c42bb2b064b23a538bee89aed)。

首轮[run39908245511](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39908245511)失败，由于JavaScript和Python默认单词边界对相邻中文汉字的处理不同。明确改成ASCII字母/数字边界规则、两个审计程序统一，首次失败、代码修复和重新成功的CI历史均保留，未静默宣告首次成功。科研研究冻结协议不是此次回顾性仓库对账的前置要求，**本审计不产生新的E1模型证明、真人E2或历史E3**。

## 五、尚未通过的科研验收门槛与下一主线

机器本轮**只证明239条目录信息及路径交叉核对成功**。没有逐份重新阅读239篇原作者论文，没有重新执行每一项R的原研究统计分析、原受试数据获取或E1/E2/E3科学验收。比如R173的真实跨社会观测评估科研范围已明示，但其符合本轮常规命名模式的`FINAL_ACCEPTANCE_STATUS.json`缺位，不能单凭“没检出特定文件名”推断其科研失败；同样有些旧R报告用不同命名方式。

建议下一轮严格按顺序：
1. 对**66个主R候选尚未确认目录条目**，优先3项P0，检查早期74原ZIP的实际成员、原论文/机制公式和已有R063、R069、R118的真实范围，去重并只对确实缺乏模型学习的项目建立补充R研究。
2. 对已有**173个主R链接**，逐研究读取真正正式验收JSON和科学报告，逐项录入模型版本、原文核实、人工E1、真实观察E2、跨实验E3、反例/失败/来源不可达等，不能仅靠链接存在标为“科学通过”。
3. 在239逐项主映射、早期材料、真实缺口和科学结论均完成核验以前，**保持总目录科学结题判定为NOT_ESTABLISHED**，不进入统一归纳分类或原创熔炼。完成后才按用户确立的顺序统一归纳分类、最后熔炼。R073和PESEN v0.1仍冻结，个人决策系统继续暂缓。
