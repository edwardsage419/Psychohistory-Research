# 心理史学：R303观察学习与R304社会认同的独立限定E1结题、原239来源v1.8

日期2026-10-23 Asia/Taipei。继续既定顺序：**先完成原R系列所有研究与分级验收、最后统一分类、再开展模型熔炼**；个人辅助决策系统具体建设暂缓。原始239候选的整体科学结题**NOT_ESTABLISHED**。本轮没有新真人/动物E2，没有历史E3；来源文件完整可核验不等于原论文在人群中的外推验证。

## 第一手理论出处和不能重复计数的科研事实

**R303原候选03-001 Social Learning Theory**。Bandura(1965), *Influence of models' reinforcement contingencies on the acquisition of imitative responses*, *Journal of Personality and Social Psychology* 1:589–595, https://doi.org/10.1037/h0022070。原实验区分了观看受奖励、惩罚、无后果的榜样以后，儿童自发模仿行为与额外激励后的模仿表现差异。R303不是Bandura原1965数学模型拟合，也没有其原始儿童逐人资料，更不是R063 Najar2020社会伪奖励学习真人实验的第二次独立预测。

**R304原候选03-003 Social Identity Theory**。Tajfel, Billig, Bundy & Flament (1971), *Social categorization and intergroup behaviour*, *European Journal of Social Psychology* 1:149–178, https://doi.org/10.1002/ejsp.2420010202。原作者真实最小群体分配实验将内群体偏好、最大群体差异和最大总收益的冲突分开研究；本项目没有重新获得/分析该文儿童或其他人类参与者的原始逐次分配资料，也没有复现原论文的效应大小。其后原候选**03-004 Self Categorization Theory**仍待独立研究，不从此自动认定为完成。

两项项目自建数学关系与上述原作者的学术理论问题相关，但**不是原作者提交或拟合的心理方程，更不是复制真实实验**；R063作者源码和Figure6归属始终固定为其自身旧范围审计。

## 本轮人工研究实际结果

| 研究 | 事前冻结SHA | 人工完整source | Python3.11/3.12主unittest | 真实科研CI |
|---|---|---:|---:|---|
| R303 观察学习痕迹和外显反应区别 | [5adc32ae](https://github.com/edwardsage419/Psychohistory-Research/commit/5adc32ae7c91c150fe82bb16f99a059d2a62e991) | 486阶段行，243人工世界 | **1473×2** | [run39934165046](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39934165046) 3/3 SUCCESS |
| R304 最小群体分配中的标签、相对差异与效率冲突 | [60f6406c](https://github.com/edwardsage419/Psychohistory-Research/commit/60f6406cede7eb5bb7cea9dc622835d8fe3f4c41) | 432分配选择行，216人工世界 | **1310×2** | [run39934709217](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39934709217) 3/3 SUCCESS |

两研究合计**918条人工来源行**，不是918个真人样本/独立观察；两个Python版本累计通过**5566项真正模型unittest**，还各有独立不导入主程序的**17项**审计及第三来源复算job。原CSV/JSON和SHA256永久归档：R303 [commit8b1c570e](https://github.com/edwardsage419/Psychohistory-Research/commit/8b1c570e13921d4c4170d7eec48f36ea76cbd96e)，R304 [commit52e09ce5](https://github.com/edwardsage419/Psychohistory-Research/commit/52e09ce525958221447cb88c76996ea570e7f505)。

### R303计算结果与首次CI失败透明记录

R303人工注意A、保持R、动作生成P、基础动机M都取{0,1/2,1}，榜样后果奖励/无后果/惩罚有**项目发明**权重1/1/2/1/4。人工学得痕迹 A·R，外显自发概率A·R·P·M·权重，第二阶段全部额外激励后概率A·R·P。固定A=R=P=1、M=1/2时，三种后果自发模仿概率1/2、1/4、1/8，额外激励后均为1。缺乏注意或保持时不能从激励中凭空生成未学得的痕迹，动作不能生成时即使有痕迹也无法外显。差异**根据人造乘法门控预先假设**，没有识别真实人类潜在认知。

R303 **首次**[run39934080577](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39934080577)失败：主1473模型测试均通过，但原source SHA256生成因局部CSV路径变量被P门控重名覆盖导致AttributeError，故首次并未通过结果归档验收。[修复commitf49c949b](https://github.com/edwardsage419/Psychohistory-Research/commit/f49c949b3b9ff95b3c13b87a22b611a490083087)仅改路径变量，不变更冻结机制或参数。全部重新执行run39934165046三个job成功，合格研究结果才算正式E1验收。

[研究正文](../research/R303/R303_SCIENTIFIC_REPORT_2026-10-23.md)、[正式验收](../research/R303/R303_FINAL_ACCEPTANCE_STATUS.json)、[独立全概率门控源审计](../research/catalogue_audit/independent_r303_source_audit.py)。

### R304计算结果与群体标签负对照

人工分配者不获得任何个人分配，只向A、B两位人工收件人分配点数。每世界提供BASE=(8,8)，另可选择偏向A/B的等总量(10,6)/(6,10)，或偏向A/B但总量更低的(9,3)/(3,9)。项目**自行创造**效用U=总点数+s·d·内外群体点数差−e·绝对不平等，s、d、e分别身份显著、相对差异偏好和不平等惩罚，每档0/1/2/1；内群体标签指向A或B；所有确切平局选BASE。可检验的反例：s=d=1,e=0时，A为内群体则(10,6)效用20＞(8,8)效用16；只交换标签令B为内群体，同样(10,6)效用12＜16。另在同样参数A为内群体时，(9,3)总点数12虽小于16，计算效用18＞16，因此人工模型为群体差异放弃4点总效率。s=0或d=0则全部菜单不选择偏差替代方案。在全部**216种预设人工组合**中，12次选择偏差替代（10次等总量，2次较低总量），与任何现实人群偏见比例都无关。

[研究正文](../research/R304/R304_SCIENTIFIC_REPORT_2026-10-23.md)、[正式验收](../research/R304/R304_FINAL_ACCEPTANCE_STATUS.json)、[独立432项源级选择审计](../research/catalogue_audit/independent_r304_source_audit.py)。

## 原始239证据来源链接审计 v1.6→v1.7→v1.8

| 来源分级 | v1.6 R302后 | v1.7 R303后 | v1.8 R304后 |
|---|---:|---:|---:|
| 已链接原候选专属主R研究 | 190 | 191 | **192** |
| 共有旧有限数学对应但非新主R | 3 | 3 | 3 |
| 仅有早期范围有限旧研究链接 | 4 | 4 | 4 |
| 已检查资料无逐条主R证据链接 | 42 | 41 | **40** |
| 尚待取得专属主R证据链接 | 46 | 45 | **44** |
| 初始唯一原模型候选 | 239 | 239 | 239 |

[完整原239目录v1.8候选证据交叉索引](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.8_2026-10-23.json)相对于[v1.7](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.7_2026-10-23.json)只有03-003唯一一行改变；v1.7相对于v1.6只有03-001唯一一行改变。原始239候选身份、名称、次序、P1/P2不动。旧R063社会强化学习、R073冻结人类重复博弈、R303独立Bandura-inspired人工学习仍分档保存。**192个主R来源是证据追踪和归档覆盖，不表示192项原论文完成真实独立预测复验。**

[待核44原候选队列](ORIGINAL_239_PENDING_44_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv) P1 **17**、P2 **27**，下一条03-004 **Self Categorization Theory**，随后是已有R072范围有限真实资料的03-010 Social Sanction and Reputation Mechanisms。须按每篇一手来源、冻结实验对象、原始数据证据级别逐项重新验收，避免混淆social identity和self-categorization。

四个完整成功CI工作流共**12个job completed/success**（首次R303失败另列不算）：
[R303科学39934165046](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39934165046)、
[R303原目录v1.7审计39934442021](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39934442021)、
[R304科学39934709217](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39934709217)、
[R304原目录v1.8审计39934971026](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39934971026)。两项原目录均具各16个跨Python核验、第三独立来源复算，证明只变更一项原始候选的主来源索引。

结论：R303、R304**人工数学E1限定科研关口完成**，没有新增真实人/动物E2或历史E3；原始239所有候选整体结题未成立，继续R系列，R073/PESEN v0.1冻结，先不分类、不融合。
