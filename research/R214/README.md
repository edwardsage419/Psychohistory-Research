# R214 回归不连续设计（09-005）：12真人工门槛世界与192原噪声来源，正式E1结题

日期2026-10-22。真实原239目录 **09-005 Regression Discontinuity Design（P1）**。**CLOSED_BOUNDED_E1_ARTIFICIAL_SHARP_RDD_DISCRETE_GRID**。

[完整科学报告](R214_SCIENTIFIC_REPORT_2026-10-22.md) · [计算前来源/模型/评分冻结](../../protocols/R214_RDD_12_WORLDS_192_ORIGINAL_NOISE_SOURCES_PRESCORE_FREEZE_2026-10-22.md) · [12世界完整结果JSON](R214_EXACT_RESULTS.json) · [192原完整独立四噪声来源CSV](R214_ALL_192_ORIGINAL_RDD_NOISE_SOURCES.csv) · [原SHA机器验收](R214_FINAL_MACHINE_ACCEPTANCE.json) · [正式结题机读收据](R214_FINAL_ACCEPTANCE_STATUS.json) · [原生Python与39单测](r214_exact_sharp_rdd.py)。

固定X=(-2,-1,1,2)、门槛0、D=1{X≥0}，人工12个真潜在结果来源模型×独立四个Rademacher±1噪声的全部16扰动可能，共192条真正有限来源。三个事先冻结的观测估计器GLOBAL、NEAREST、TWO_SIDED_LINEAR只读固定四X及实际Y，比较真结构oracle门槛处理效果tau的完整来源MSE。三个噪声方差严格为**1、2、10**。LINEAR_CAUSAL_TWO和BASELINE_STEP_FALSE_CAUSAL的四X处**所有完整观察联合分布精确一致**，但真tau分别**2和0**；无潜在结果连续性假设，观测跳跃不能唯一解释为处理因果效应。RIGHT_QUADRATIC即使未处理基线于0连续，固定四点两侧线性外推仍偏差−2；FLAT_TAU_TWO无复杂趋势时全局均值MSE1，小于两侧线性MSE10，展示人工固定网格上复杂估计未必降低MSE。该实验**没有密集门槛点**、没有McCrary密度跳跃检验，不可外推真实RDD证据。

[GitHub Actions run39740585568](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39740585568) Python3.11与3.12各39项单测共**78项测试全部成功**，第三完整12世界、192真原来源、独立Fraction方差与三文件SHA归档job也success；机器人[真正原始数据提交af59326b](https://github.com/edwardsage419/Psychohistory-Research/commit/af59326bd3990d83e94e1d490ce5e839f2d5d3ce)。

人工数学E1有界方法研究，新增真人E2=0、真实历史E3=0；R073/PESEN v0.1冻结。下一真实原目录 **09-006 Difference in Differences**，研究编号拟R215。完成全部原R系列后统一分类，最后熔炼。


## 2026-10-22 增量研究 R214-S2：7168原十位置噪声来源，原正式研究不变

本节为**独立补充，绝不替代上述12世界192来源R214正式验收**。[增量完整科学报告与归档修复记录](R214_S2_SCIENTIFIC_REPORT_2026-10-22.md) · [事前增量冻结协议](../../protocols/R214_RDD_7_WORLDS_7168_ORIGINAL_GRIDS_PRESCORE_FREEZE_2026-10-22.md) · [7世界56配置完整S2结果](R214_S2_EXACT_RESULTS.json) · [7168条完整原噪声及真实评分](R214_ALL_7168_ORIGINAL_TEN_POINT_SHOCK_SOURCES.csv) · [S2独立机器哈希验收](R214_S2_FINAL_MACHINE_ACCEPTANCE.json) · [独立正式验收收据](R214_S2_FINAL_ACCEPTANCE_STATUS.json)。

S2固定十个真实人工X位置−5..−1,+1..+5及阈值0，7个生成函数×完整1024独立噪声向量=**7168条原人工来源**，四个带宽h2/3/4/5与局部常数/线性两算法共56评分，Python3.11及3.12各40项测试共**80测试通过**；[最终S2 run39743169253](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39743169253)三job全部success，[机器人独立增量归档73372995](https://github.com/edwardsage419/Psychohistory-Research/commit/73372995fd7eeb0c21b8829a7cfd181e549bb82c)。

核心反例：真实因果效果2的FLAT_TAU2和效果0的CONTINUOUS_HIDDEN_RAMP在十个实际观察位置上**完全同分布**，即便后者潜在未处理均值在阈值连续并且一、二阶导数连续，实际观测网格离阈值最小距离仍为1，也不能仅从该数据估计真阈值因果效应。另有不合法基线突跳机制同样观察等价。只有人工E1，E2/E3=0。

**归档纠错**：新增S2第一轮因结果同名暂时覆盖原R214的`R214_EXACT_RESULTS.json`和`R214_FINAL_MACHINE_ACCEPTANCE.json`；已通过原正式机器人提交[af59326b](https://github.com/edwardsage419/Psychohistory-Research/commit/af59326bd3990d83e94e1d490ce5e839f2d5d3ce)恢复，S2自此**只写独立S2前缀结果与收据**。本页原始正式R214的12世界192来源研究正文、正式结果、机器验收和结题收据均保留，S2不产生第240个目录项目。


## 2026-10-22 R214-S9 九世界原冻结协议单独补充结题

原2026-10-22冻结的九人工世界、576条R×U×E来源及36组局部外推现在也已**独立执行及归档**，其研究身份为 `R214-S9`，不覆盖R214原主研究12世界192来源、R214-S2七世界7168来源，也不额外计算一个239目录项目。主要文件：[原S9计算前冻结协议](../../protocols/R214_RDD_9_WORLDS_576_ORIGINAL_SOURCES_36_LOCAL_EXTRAPOLATIONS_PRESCORE_FREEZE_2026-10-22.md) · [S9科学报告](R214_S9_SCIENTIFIC_REPORT_2026-10-22.md) · [576条完整人工原来源CSV](R214_S9_ALL_576_ORIGINAL_RDD_SOURCES.csv) · [36组固定局部拟合CSV](R214_S9_ALL_36_LOCAL_EXTRAPOLATIONS.csv) · [9世界结果JSON](R214_S9_EXACT_RESULTS.json) · [SHA机器验收](R214_S9_FINAL_MACHINE_ACCEPTANCE.json) · [S9独立正式结题收据](R214_S9_FINAL_ACCEPTANCE_STATUS.json)。

[GitHub CI run39786552882](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39786552882) 三作业全部success，Python3.11与3.12各48单测共96次，第三作业核验并将全源资料永久归档于main，原始机器人归档提交 [3b73602f](https://github.com/edwardsage419/Psychohistory-Research/commit/3b73602f026f85ef469b6e4f7eeee76340d80330)。密度跳跃、未处理基线跳跃、U构成变化、有限跨度曲率偏差已各自保留独立真效果与实际观察外推；仅有人工数学E1，真人E2与真实历史E3新增均0。

原有 [并行协议审计](../../docs/R214_R215_CONCURRENT_PROTOCOL_PROVENANCE_AUDIT_2026-10-22.md) 所记录“9世界576来源尚未完成”为**更早时点的真实状态**，本次独立补充验收对其作有日期的状态更新，不改写原时序证据。
