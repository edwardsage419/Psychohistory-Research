# R系列编号与239项原目录映射校正公告（2026-10-22）

性质：归档元数据与研究路线修正，不改变已冻结模型机制、得分、原数据或已成功CI。这份校正独立于研究结题的科学证据。

## 核验原始唯一主目录

对main中的[原239项目录JSON](MODEL_CANDIDATE_CATALOG_v0.1.json)完整解析，`models.length=239`。分类`08 统计推断与概率`最后一个条目为**08-031 Matrix Completion（矩阵补全）**，下一条按JSON真实顺序为**09-001 Randomized Controlled Experiment（随机对照实验）**。不存在`08-032`或`08-033`，目录中不存在英文条目`Network Centrality`或`Diffusion of Innovations`。另有关联的实际目录项：**04-005 Simple versus Complex Contagion**、**06-013 Bass Diffusion Model**、**04-001 Granovetter Threshold Model**等；这些目录项都不等同本次特定人工两轮采用模型的整套原作者模型公式或真实实证。

## 具体不实元数据与修正

1. R207报告及映射：`R207 → 08-031 Matrix Completion`确实是原目录最后08条目，保持。
2. R208在2026-10-22创建时被错误标为`P1/08-032 Network Centrality`，该原目录ID并不存在。**R208仍作为已归档的有界补充人工图论模型研究，保留R208身份与全部原证据，但其catalogue_id设为null，catalogue_mapping_status=SUPPLEMENT_NOT_UNIQUE_239_ITEM_CATALOG_ENTRY**。过去的全部R208数学实验与CI证据没有因目录映射改正自动改变。
3. R209在计算前冻结协议中错误写为`P2/08-033 Diffusion of Innovations`，该原目录ID并不存在。**R209保留为当前执行的有界补充人工创新扩散机制审计，并与04-005/06-013做概念关联，catalogue_id=null，仍不得宣称是对任一原作者完整模型或原目录新条目的结题**。所有R209人工数据源、评分与同分规则照此前冻结保持完全不变。
4. 按唯一真实原始239项目录**下一条应为09-001 Randomized Controlled Experiment**。R209完成后，如果沿当前连续R编号推进，则**R210应实际研究09-001（P0 随机对照实验）**，而先前预告的`R210 P1/08-034 Agent-Based Modeling`也不存在于原始目录，不能继续错误映射。不得将R208/R209的补充研究充数为239原条目的已经完成覆盖。

## 程序性保证

- 仅更正研究地图、元数据及报告中的不实目录归属，不偷偷修改或替换R208/R209已冻结来源、候选机制、测试规则、原始结果、CI及SHA。
- 维持全R原计划：逐项完成真实原239目录中尚未完成的模型条目，之后统一分类，再进行模型熔炼。
- 已完成归档的R208补充研究和R209补充人工审计可保留方法学价值，科研证据等级仍限人工E1，新增真人E2=0和真实历史E3=0。
- 下一研究协议必须从`docs/MODEL_CANDIDATE_CATALOG_v0.1.json`动态核实id/name/priority而不是依据前一份报告猜测一个顺序后缀。

校正发现：2026-10-22在R209首次测试运行期间主动读取239原目录全文时发现。原R209计算前协议仍原样保留作为时间顺序证据，不对原文件进行静默修订。
