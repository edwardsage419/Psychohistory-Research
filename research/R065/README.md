# R065 关键试次测量审计

日期：2026-10-15。阶段：**Phase A 至 Phase E 的限定范围研究已归档；R065 完整研究仍 OPEN**。

本阶段完成对 Levy 等人 2025 年公开处理后数据的 Git blob 字节哈希重算，在 GitHub 连接器执行环境内进行 16,103 条真实记录的关键试次审计。原始固定文件 Git blob `01bf211468abe093618dfa5e5c39e883230c9c03`（4,427,523 字节）。源数据未在本仓库重新分发。

成果文件：

1. [研究与证据审计](R065_EVIDENCE_AUDIT.md)：全部/关键试次的测量边界与竞争预测模型对照。
2. [实际来源数据派生结果](R065_CONNECTOR_CRITICAL_RESULTS.json)：226 人、1,808 个诊断试次，含参与者重抽样区间。
3. [可运行 Python 复现程序](r065_critical_replay.py)：只能在本地给定严格 SHA1 对应的完整作者 CSV 后运行。
4. [合成数据程序测试](test_r065_critical_replay.py)：首阶段 9 项 PASS。

运行：

```bash
cd research/R065
python -m unittest discover -p 'test_*.py' -v
python r065_critical_replay.py --source /path/to/unified_data_2025-01-16_00.csv --output replay.json
```

状态边界：研究结果由连接器读取并哈希核验的真实 CSV 计算；本地 Python 仅运行合成数据测试。尚待作者原始处理 CSV 本地端到端复算。原 R064 事前主要结局、PESEN v0.1 冻结状态均未改变。

## Phase B：时间趋势与条件先后顺序

* [第二阶段研究审计](R065_PHASE_B_ORDER_AUDIT.md)：第 1 至第 8 实验块的模仿频率变化，及 High 先/Low 先两组的敏感性。
* [第二阶段统计 JSON](R065_ORDER_RESULTS.json)：固定作者 Git blob 的连接器端真实数据结果。
* [第二阶段 Python 复现](r065_order_audit.py)：保持严格来源 Git SHA1 入口；无来源字节不能做真人数据重放。
* [新增 6 项合成单元测试](test_r065_order_audit.py)：连同既有 9 项，总计 **15 项在本地 Python 环境实际运行通过**。

主要现象：前两个实验块模仿率 46.68%，最后两个 34.07%，受试者等权前减后差 +12.61 个百分点，Bootstrap 95% 区间 6.42 至 18.81 个百分点。此下降属于回顾性描述，不能分辨练习、信息积累、疲劳或具体策略。按先出现的收益条件分组的收益差异，其组间对照区间跨零。

完整命令：

```bash
cd research/R065
python -m unittest discover -p 'test_*.py' -v
python r065_critical_replay.py --source /path/to/unified_data_2025-01-16_00.csv --output r065_critical.json
python r065_order_audit.py --source /path/to/unified_data_2025-01-16_00.csv --output r065_order.json
```

当前容器的完整外部 CSV 下载失败，因此两项真实数据 Python 完整重放均仍开放。禁止用测试通过替代原始数据的实证复现。

## Phase C：公开模型源码状态重置对齐审计

* [七模型重置时间轴审计报告](R065_PHASE_C_RESET_AUDIT.md)
* [固定源码取证与可检验结果 JSON](R065_PHASE_C_RESET_RESULTS.json)
* [SHA1 严格门控 AST 复算程序](r065_reset_alignment.py)
* [十项新增合成 AST 和代数测试](test_r065_reset_alignment.py)

真实源代码连接器核对：公开目标函数对模型 1 至 7 均采用 23、45、67、89、111 的状态重置日期；固定作者实验的实际区块起点为 18、35、52、69、86、103、120，零重合。第 89 天又是关键选择，按源码初始化状态会使这些模型在该日的二选一预测退化为等概率。**真实作者拟合和效应幅度尚未重算，不能据此给论文发布结果下结论。**

截至本阶段，R065 三个测试文件的 **25 项本地构造输入测试全部通过**。第三方完整 Python 原始源码和真人实验源文件未进入本地容器，第三方资料继续只读、无再分发。

```bash
cd research/R065
python -m unittest discover -p 'test_*.py' -v
python r065_reset_alignment.py --source /path/to/objectives.py --output reset_alignment.json
```

R065 的研究整体关口依然 OPEN；PESEN v0.1 冻结。

## Phase D（2026-10-16）：不泄漏的留整人预测对照

在看本阶段四模型新分数前已将 [回顾性比较方案](../../protocols/R065_PHASE_D_RETROSPECTIVE_PLAN_2026-10-16.md) 单独提交，研究仍属先前已见数据上的后续分析。

* [Phase D 结果与证据审计](R065_PHASE_D_PREDICTION_AUDIT.md)
* [Phase D 真实 CSV 连接器侧派生结果](R065_PHASE_D_PREDICTION_RESULTS.json)
* [严格 Git SHA 的 Python 复算程序](r065_phase_d_loso.py)
* [Python 构造数据测试](test_r065_phase_d_loso.py)
* [GitHub Actions 独立复算工作流](../../.github/workflows/r065-reproducibility.yml)

四种模型依次为总体模仿率 M0、收益分层 M1、实验块分层 M2、块与收益交叉 M3。在相同 226 人、1,808 条关键试次和 Beta(4,4) 下的完整留整人评估，平均 Log loss 分别 0.664810、0.665154、0.661563、0.663022。M2 的平均分数最好，但相对于 M0 的受试者重抽样差值区间跨零。研究中首次草算的单行扣除数据泄漏已纠正，最终分数与 Phase A 既有 M0/M1 独立交叉核对一致。

**复现与执行边界**：容器中实际运行了四项有限 synthetic 排除逻辑测试。GitHub 的十项新增 synthetic 测试及完整原始 CSV CI 回放已配置，尚需 GitHub 成功作业日志确认；之前三个阶段已记录的测试状态独立保留。公开仓库只保存分析程序、派生结果和来源哈希，不重新分发原作者个体原始数据。

```bash
cd research/R065
python -m unittest discover -p 'test_*.py' -v
python r065_phase_d_loso.py --source /path/to/unified_data_2025-01-16_00.csv --output phase_d_results.json
```

PESEN v0.1 保持 FROZEN。

## Phase E（2026-10-16）：第 89 轮统一重置后的预测信息损失界限

* [事后冻结方案](../../protocols/R065_PHASE_E_DAY89_BOUND_2026-10-16.md)
* [Phase E 源码条件及证据报告](R065_PHASE_E_DAY89_AUDIT.md)
* [固定原作者 CSV 的结果 JSON](R065_PHASE_E_DAY89_RESULTS.json)
* [SHA1 严格门控的 Python 复算](r065_phase_e_day89.py)
* [在本地实际执行 8/8 通过的边界测试](test_r065_phase_e_day89.py)

226 人中的 73 人在 day=89 选择作者定义的 `copied` 行动。公开七模型源代码在该日预先重置，任务所给正规化转移分布与等权代币先验意味着两条动作的初始预测均为 0.5。基于各被试以外其余 225 人的 day=89 结果、固定 Beta(4,4) 的经验概率估计，平均 Log loss 为 0.63346543，相比等概率 0.69314718 降低 0.05968175；个人级配对 Bootstrap 95% 区间为 [0.01513433,0.10422917]。这是后验选择的结构性预测上界比较，**不能解释为重置代码修复后原作者七模型实际获得此种提升**。

本地 Phase E 源代码与测试文件已运行并逐字节比较 Git blob；8 项 synthetic 测试均 PASS。GitHub Actions 已增加 Phase E 固定来源重算，但远端作业是否成功仍未核实。完整研究门仍 OPEN，PESEN v0.1 冻结。
