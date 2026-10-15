# 心理史学 R064 正式研究包

日期：2026-10-15

研究状态：完成锁定方案的连接器源数据分析；并提供可运行的本地SHA验证复现程序。**本地没有作者4.4MB原始CSV字节**，因此源码程序只通过构造数据的16项单元测试，当前包不能称作本地原始文件端到端复现。

## 本地复现操作

Python 3.10及更高版本，无第三方依赖：

```bash
python -m unittest -v test_r064_observational.py
python r064_observational.py --source /path/to/unified_data_2025-01-16_00.csv --output local_r064_results.json
```

源CSV必须与作者Git blob `01bf211468abe093618dfa5e5c39e883230c9c03` 全字节一致，否则脚本拒绝分析。可通过作者公开仓库取得；本包未重新分发源CSV。

文件说明：

- `R064_CONNECTOR_RESULTS.json`：从固定Git blob连接器端实时计算的实际结果。
- `R064_EVIDENCE_AUDIT.md`：解释、准入、排除、边界与未闭合项。
- `r064_observational.py`：本地原始CSV字节检验与等权/留一人/重抽样分析完整实现。
- `test_r064_observational.py`：构造数据单元测试。
- `SHA256SUMS.txt`：归档文件指纹。

锁定方案原件：研究资料库 `R064_PROTOCOL_PRECOMMIT.md`，创建时间比本次R064源CSV结局读取更早，未被修改。源代码独立估计R064自身目标，不覆盖PESEN v0.1。
