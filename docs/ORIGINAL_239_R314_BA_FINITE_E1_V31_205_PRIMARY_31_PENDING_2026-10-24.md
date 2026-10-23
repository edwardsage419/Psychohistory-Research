# 心理史学原239候选v3.1：R314 BA优先连接有限E1及来源归属

日期：2026-10-24 Asia/Taipei。项目严格按原有顺序完成所有R系列候选研究后再分类，最终才进行熔炼；R073及PESEN v0.1均保持冻结。

## 科研结论与范围

本轮新增原239条目`04-016 Preferential Attachment Network`（P1）专属有限机制研究R314。文献源Barabási & Albert (1999), *Science*, DOI https://doi.org/10.1126/science.286.5439.509 ，作者网络科学教材 https://networksciencebook.org/chapter/5 。

事前冻结 [R314协议](../protocols/R314_BARABASI_ALBERT_THREE_SEED_TWO_ARRIVAL_54_TARGET_SOURCE_PRESCORE_FREEZE_2026-10-24.md) Git [commit0426722f](https://github.com/edwardsage419/Psychohistory-Research/commit/0426722f05cb409655f0bee5897d4b57c87cfa0a)，明确仅考察P3、K3、S4三个连通起始种子图，每步增加一节点一边，度数比例选取已有目标节点，连续两步不采样而全枚举。

本轮得到**54条完整有条件目标原source**和**44条两步路径**。初始条件：P3目标权重(1/4,1/2,1/4)，K3全部1/3，S4中心1/2、三叶各1/6。路径终态分布在每个初始种子图分别精确归一。验证每条路径中节点数递增，新增节点度数1，被选目标度数+1，总度数+2，且保持无向简单连通。

对真实群体网络是否出现度数幂律、形成过程是否因果由度数驱动、长期尺度不变网络性质或可用于现实社会历史预测，**本轮不作任何肯定推断**；新增E2=0、E3=0。

科研来源：[R314科学报告](../research/R314/R314_SCIENTIFIC_REPORT_2026-10-24.md)、[54 source CSV](../research/R314/R314_ALL_54_ORIGINAL_TARGET_SOURCE_ATOMS.csv)、[44完整路径JSON](../research/R314/R314_EXACT_44_TWO_ARRIVAL_PATH_RESULTS.json)、[机器来源收据](../research/R314/R314_MACHINE_RECEIPT.json)、[正式E1验收](../research/R314/R314_FINAL_ACCEPTANCE_STATUS.json)。

科研实际[CI run 39994420445](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39994420445)已**3/3 completed/success**，Python3.11与3.12分别32项unit tests通过，独立实现逐条复算54 source与44条最终路径，无共享计算模块。

## 完整239原始候选v3.1证据索引

从[原239 v3.0](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v3.0_2026-10-24.json)演进到[原239 v3.1](ORIGINAL_239_CATALOGUE_TO_R_EVIDENCE_PROVENANCE_CROSSWALK_v3.1_2026-10-24.json)，严格只将原`04-016`的缺主R状态绑定为已完成有限E1的R314。其余238个原候选名称、顺序、优先级和来源归属均未变。

| 类型 | v3.0 | v3.1 |
|---|---:|---:|
| 有专属主R来源归属（含历史暂拟README） | 204 | **205** |
| 仅共享限定数学链接 | 3 | 3 |
| 仅既有有限审计无主R | 1 | 1 |
| 已检查来源但仍无逐项主R | 31 | **30** |
| 主R来源仍待核 | 32 | **31** |
| 原始唯一候选 | 239 | 239 |

[剩余31项队列](ORIGINAL_239_PENDING_31_P1_P2_EVIDENCE_TRIAGE_QUEUE_2026-10-24.csv)保留**4项P1和27项P2**，下一条是`04-017 Watts Strogatz Small World`。旧有173条`PROVISIONAL_PRIMARY_README_LINK`的研究证据等级尚应维持逐项审计，不把目录关联数205视作205个具有真实经验效力的模型。

机器[完整原239 v3.1不变量审计](../research/catalogue_audit/verify_p1_r314_crosswalk_v3_1.py)由[CI run 39994606508](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39994606508) **3/3 successful jobs**确认：只04-016变化，完整候选编号名称优先级一致，R314全部原source Git blob SHA1与收据一致，队列只移走04-016，所有计数与原始239持平。项目整体239项实证验收、统一分类及融合阶段继续开放。

下一步优先查阅原有R系列早期存档中是否覆盖`04-017 Watts Strogatz Small World`。如无已验证的逐项专属证据，则先冻结有限重连协议，再研究短路径与集聚聚合的可反驳机制，且不夸大成人类社交网络实际生成机制。
