# R065 正式结题报告：观察性社会学习的测量、模型来源与有限预测复现

**结题日期：2026-10-16**
**档案状态：CLOSED_BOUNDED（限定范围正式结题）**
**研究科学结论级别：E2（真实作者数据、严格来源验证、内部留整人评价）；E3 外部独立证据未形成。**
**适用规程：** [研究统一验收与结题标准 v1.0](../../protocols/RESEARCH_ACCEPTANCE_STANDARD_V1_2026-10-16.md)。

本报告为**事后确定的范围结题**。R065 原先较广的七模型全样本、原作者层级 EM/iBIC 和外部独立预测任务没有完成；绝不将事后缩减范围冒充研究开始前的完整成功条件。结题仅意味着限定研究包已有足够可引用的真实审计、计算与失败记录，未完成问题另存 BACKLOG，今后主要研究资源转向新的模型家族。

## 1. 研究问题与阶段性回答

**问题：** 对公开观察性社会学习实验中的关键选择、社会学习/目标模拟的模型实现和状态重置机制，我们能核验哪些原始证据，并在来源一致的真实行为数据上获得何种**限定的**可重复预测表现？

回答：

1. 已核验原作者固定提交的处理数据 `unified_data_2025-01-16_00.csv`，16,103 条记录、226 名符合预设条件的参与者及 1,808 个诊断试次；精确输入 Git blob `01bf211468abe093618dfa5e5c39e883230c9c03`。相关条件先后顺序、模仿趋势、基础测量解释在 A–G 档案逐项保留。单纯模仿率变化不能辨别时间学习、疲劳、收益变化或特定学习机制。
2. 原作者七个原生模型目标函数均可从作者固定原始源码直接导入运行。作者源码七处重置日 `[23,45,67,89,111]` 与数据中的实验块起点 `[18,35,52,69,86,103,120]` 不同；该实现差异客观存在，但**不自动证明论文结论错误**。
3. 在固定并逐份 SHA1 核验的 24 名参与者（每人 136 条正式实验行、合计 1,327 次 `play`）上，真实执行七个作者目标函数，并以相同固定双起点、L-BFGS-B 和两折受试者级隔离策略各自训练一套共享参数，七模型两折全部完成。此任务级内部留人评价中 Model 6 的均值 NLL/选择最低，为 **0.6482591689606808**；Model 7 为 0.6506295449887813。**只是该特定样本和共享参数策略下的描述性成绩**，不属于新的独立队列或层级 EM 复现。
4. 两套重置规则在七模型中的额外研究：六模型按冻结门控得到可配对结果，其中每一个模型的 A 折候选时钟改善、B 折候选时钟恶化。Model 5 虽两套时钟拟合都数值收敛，重跑原作者时钟与 Phase L 的精确容差门控不一致，因此 **FAIL_CLOSED**；不存在完整七模型候选时钟验证结论。
5. 对失败后的 Model 5 进行独立标记为**事后诊断**的固定参数原作者目标函数重播：原 Phase L/M 两次运行保存的四组潜在参数，分别准确重现对应训练与留出损失。说明固定参数评分可复算，重跑优化的参数终点不同；具体优化差异原因尚未识别。**不修改失败状态。**

## 2. 六项统一验收

| 门控 | 结果 | 精确边界 |
|---|---|---|
| A01 问题/范围 | PASS（限定范围） | 本次结题范围是已完成的来源审计与 24 人七模型内部留出，属于事后范围固定；226 人全样本与作者层级重跑另列 OPEN |
| A02 原始证据 | PASS | 固定作者仓库提交 `fd5f435b5368b69916e7acc6a9991aa5f46b3ddb`、精确作者程序与处理/原始 CSV SHA1；仅记录校验值与匿名聚合，不再分发原始参与者行 |
| A03 真实执行 | PASS（限定范围） | Phase K 七作者目标函数真实导入；Phase L 七模型两折结果真机 CI 全成功；Phase M 六模型完整双时钟 PASS、一模型 FAIL，已保留远端日志 |
| A04 负结果 | PASS | 研究未掩盖 Phase M Model5 原生重跑不一致，已固定来源及事后复诊，未放宽 `1e-7` 阈值，也不称失败实验 PASS |
| A05 推断等级 | PASS | E1 合成程序验证与 E2 原始实验来源/内部留出区分；无 E3 外部独立验证、无人级误差置信区间；机制因果与长历史外推不成立 |
| A06 结题与移交 | PASS | 本报告、机读结题清单、GitHub 文件与已实跑作业、未完成问题 BACKLOG 与下一研究 R066 均建立版本化入口 |

此表是**限定研究包验收**，不是将 Phase M 错误地写成完整 PASS，也不是将未实施的试验标为 N/A。

## 3. 关键可验证证据

- [Phase A–G 研究索引](README.md)，保留每项测量、建模设计与反例。
- [Phase J 24 人精确原始文件来源与 Model 3](R065_PHASE_J_SCREENED_24_RESULTS.json)；GitHub Actions run [38840809171](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38840809171) 两项作业成功。
- [Phase K 原作者七目标函数核验](R065_PHASE_K_NATIVE_AUDIT.md)；run [38842410238](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38842410238) 两项成功。
- [Phase L 七模型同预算两折复现](R065_PHASE_L_NATIVE_HELDOUT_AUDIT.md) 与 [固定匿名聚合 JSON](R065_PHASE_L_NATIVE_HELDOUT_RESULTS.json)；run [38843245182](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38843245182) 八项成功。
- [Phase M 时钟变化与 Model5 严格失败](R065_PHASE_M_TWO_CLOCK_AUDIT.md)，[七模型聚合 JSON](R065_PHASE_M_TWO_CLOCK_AGGREGATE_RESULTS.json)；run [38844279247](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38844279247) **七成功、一失败**。
- [事后 Model5 四固定参数评分结果](R065_PHASE_M_MODEL5_FIXED_PARAM_DIAGNOSTIC_RESULTS.json)；run [38844938066](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38844938066) 两项成功，另有七项 synthetic 测试。
- 全部程序及离线测试均存放于 `research/R065/`，源码/时钟适配严格按各自冻结方案运行。有关训练终点、函数调用数量等确切字段可查 CI Artifacts，长期归档另留聚合重放摘要。

## 4. 最重要的限制与不得宣称的结论

- **完整 226 人七模型原生参数重拟合：OPEN**；仅已审计处理数据的 226 人结构与关键行为，并在其中固定 24 人完成完整七模型比较。
- **原作者层级 EM/iBIC：OPEN**；Phase L/M 采用统一的折内群体共享参数优化，不是作者已发表层级方法的逐参数复制。
- **Model 5 双时钟严格结论：FAIL_CLOSED**，固定参数可重放的事后诊断仅缩小原因范围，原先验收失败仍有效。
- **外部独立研究队列与机制因果：OPEN**；模型性能排序未经新样本、事先模型选择程序、受试者级不确定性分析确认。
- **将群体预测提升至历史级推断：UNSUPPORTED**。单个实验不能直接支持群体制度演化的历史预测。
- 本研究**没有提出或验证独立原创的完整心理史学模型**；PESEN v0.1 保持 `FROZEN`。

## 5. 正式结题与后续移交

**结题决定：R065=CLOSED_BOUNDED**，且公开保留 `ORIGINAL_BROAD_REPLICATION_NOT_COMPLETED=TRUE`。

今后不再因本项目内部阶段编号增殖而无限占用研发精力。新研究转向 **R066：DeGroot、Friedkin–Johnsen 与 Hegselmann–Krause 群体意见动力学的统一机制比较**。R066 独立制定数学定义、来源与合成机制测试，优先真实经验预测数据验证；严禁未经数据支持宣称群体历史预测能力。

任何重新启动 R065 的 226 人、层级 EM/iBIC、Model5 优化数值稳定性、外部样本，都需要新版本化续研究计划与自己的验收条件。问题记录见 [R065_POST_CLOSURE_OPEN_GATES.md](R065_POST_CLOSURE_OPEN_GATES.md)。

**记录状态：`R065=CLOSED_BOUNDED`，`R065_FULL_AUTHOR_REPLICATION=OPEN`，`R065_PHASE_M_MODEL5=FAIL_CLOSED`，`PESEN_v0.1=FROZEN`。**
