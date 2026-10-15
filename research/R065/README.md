# R065 关键试次测量审计

日期：2026-10-15。阶段：**PHASE A、PHASE B、PHASE C 已完成限定范围审计；完整 R065 研究仍 OPEN**。

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
