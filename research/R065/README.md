# R065 关键试次测量审计

日期：2026-10-15。阶段：**PHASE A COMPLETE；完整 R065 研究仍 OPEN**。

本阶段完成对 Levy 等人 2025 年公开处理后数据的 Git blob 字节哈希重算，在 GitHub 连接器执行环境内进行 16,103 条真实记录的关键试次审计。原始固定文件 Git blob `01bf211468abe093618dfa5e5c39e883230c9c03`（4,427,523 字节）。源数据未在本仓库重新分发。

成果文件：

1. [研究与证据审计](R065_EVIDENCE_AUDIT.md)：全部/关键试次的测量边界与竞争预测模型对照。
2. [实际来源数据派生结果](R065_CONNECTOR_CRITICAL_RESULTS.json)：226 人、1,808 个诊断试次，含参与者重抽样区间。
3. [可运行 Python 复现程序](r065_critical_replay.py)：只能在本地给定严格 SHA1 对应的完整作者 CSV 后运行。
4. [合成数据程序测试](test_r065_critical_replay.py)：本轮 9 项 PASS。

运行：

```bash
cd research/R065
python -m unittest discover -p 'test_*.py' -v
python r065_critical_replay.py --source /path/to/unified_data_2025-01-16_00.csv --output replay.json
```

状态边界：研究结果由连接器读取并哈希核验的真实 CSV 计算；本地 Python 仅运行合成数据测试。尚待作者原始处理 CSV 本地端到端复算。原 R064 事前主要结局、PESEN v0.1 冻结状态均未改变。
