# 心理史学原始239目录：R301 BOCPD完整有限人工E1与v1.5证据核验

日期2026-10-23 Asia/Taipei。沿既定顺序先完成全部R系列，再统一归纳分类，最后熔炼模型。此研究正式范围是**人工E1**，并未产生真人/动物E2或历史E3，原始239整体科学结题**未成立**。

## R301 原始对应02-012 Bayesian Change Point Detection（P1）

源论文Adams & MacKay (2007), *Bayesian Online Changepoint Detection*, [原作者论文](https://lips.cs.princeton.edu/pdfs/adams2007changepoint.pdf)、[arXiv:0710.3742](https://arxiv.org/abs/0710.3742)。[事前协议](../protocols/R301_BAYESIAN_ONLINE_CHANGEPOINT_BERNOULLI_192_SOURCE_PRESCORE_FREEZE_2026-10-23.md)在[commit1e0209ff](https://github.com/edwardsage419/Psychohistory-Research/commit/1e0209ffa2c8597d3d3f2a7ccef40eea0be4485e)冻结，先于源码结果。

人工Bernoulli–Beta(1,1)变点模型，用h=0、1/4、1/2三档固定变点先验风险，所有16个四位观测序列×1至4位前缀穷举，共**48个人工世界、192条完整来源状态**。短前缀在不同四位序列中重复，非192个独立观测或真实人群。每状态保存完整分段长度的未归一化联合概率、后验质量、最近边界变点概率与下一期观测预测，全部为精确Fraction。

独立审计程序对每个前缀穷举2^(t−1)种完整分段，利用每段Beta积分似然重算后验与下一观察预测，**完全不导入正式BOCPD程序**。同时对去重后的所有同长度前缀执行严格总概率=1校验，防止误把重复行当成抽样数据。

| 人工观测末端 | 固定风险h | 最近一轮边界变点后验 | 下一期1概率 |
|---|---:|---:|---:|
| 0000 | 1/4 | 135/757 | 1717/6056 |
| 0001 | 1/4 | 135/323 | 1301/2584 |
| 0001 | 1/2 | 15/23 | 849/1564 |
| 0000 | 0 | 0 | 1/6 |
| 0001 | 0 | 0 | 1/3 |

同样观察`0001`，改变先验风险会改变变点后验，因此**不应根据一次异常观测就宣称变点已经真实发生**。在h0的无变点负对照中，模型仍因观察1而更新单段成功率预测，这种学习不是变点发现。该计算未涉及实际环境转折真值标注、检测虚警率/漏报率、心理主体信念变化或真实历史事件预测。

完整[科学报告](../research/R301/R301_SCIENTIFIC_REPORT_2026-10-23.md)、[192行原source](../research/R301/R301_ALL_192_ORIGINAL_BAYESIAN_CHANGEPOINT_PREFIX_SOURCES.csv)、[48世界完整结果](../research/R301/R301_EXACT_CHANGEPOINT_RUN_LENGTH_RESULTS.json)、[SHA256凭证](../research/R301/R301_MACHINE_RECEIPT.json)、[独立分段全枚举程序](../research/catalogue_audit/independent_r301_source_audit.py)、[有界机器验收](../research/R301/R301_FINAL_ACCEPTANCE_STATUS.json)全部GitHub main归档。[科学CI run39930227033](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39930227033)3/3 SUCCESS：Python3.11、3.12分别通过588项模型单测及16项独立源审计，第三job独立重算后将原始CSV、结果JSON与SHA永久归档[commitfc948ef4](https://github.com/edwardsage419/Psychohistory-Research/commit/fc948ef418947e4c6adc958b619796cc9e30b9de)。

## 原始239来源交叉索引v1.5

| 证据关联状态 | v1.4 R300后 | **v1.5 R301后** |
|---|---:|---:|
| 已有原候选主R关联 | 188 | **189** |
| 共享有界数学来源（非单独主R） | 3 | **3** |
| 仅旧有限范围来源链接 | 4 | **4** |
| 已核材料未见逐项链接 | 44 | **43** |
| 剩余待核主R来源 | 48 | **47** |
| 原始候选条目 | 239 | **239** |

[全239行v1.5证据索引](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.5_2026-10-23.json)从[v1.4](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v1.4_2026-10-23.json)只更新**02-012一行**，对应R301源与SHA、受限科研验收。原目录239项身份、次序、优先级未动，R300 HMM、R299 model-free及原R063社会模仿旧证据都保持原有来源归属。**189项主R关联仅表示已建立来源追踪，不表示189项独立真人实证复现**。

[当前47项P1/P2研究来源待核队列](ORIGINAL_239_PENDING_47_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-23.csv)：P1 **20**、P2 **27**。下一项**02-016 Multi Armed Bandits**。[目录独立审计源码](../research/catalogue_audit/verify_p1_r301_crosswalk_v1_5.py)及[GitHub Actions run39930492102](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39930492102)均实测3 job SUCCESS，双Python各15项元数据测试、第三独立原始CSV分段重算。明确归档完整和人工科学证据等级的差异。

R073、PESEN v0.1保持冻结，未开始统一分类或熔炼。
