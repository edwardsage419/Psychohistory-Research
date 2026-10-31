# E138 R308 S104 原始收据元数据覆盖与原生重放状态审计

UTC 2026-10-31T06:23:11.467Z。目标键 (operations,R308,S104,archived-B-metadata-and-native-scope)。只读 R/B 原始研究及跨轨记录，非盲态工程审计。没有修改冻结协议、R/B源码、original239、待核队列或其他轨索引。

## 当日 HEAD 与证据变化

main 基线 ce7f71296afca3a0160335b856f3e77e5fb03bc8（TH173）；此前市场交接 c51b75eea86aa02b9a2c3a328c1048cc82f12228。R308 S104 冻结 e3d2b690a794d4fd3e748b43a59e71d56eda09cf，早于研究产物。R轨于 05:49 UTC 追加 v2 原生 Node 及独立 Python Fraction 重放报告，原始 v1 序列化失败保留。后续补充报告记录 Node v22.16.0 原生命令行 PASS、Python 普通及 -O PASS、两个输出字节与远端 blob 相等。这些是 R/B 轨的已归档执行证据；本 E138 轮没有重新运行原生 Node 或 Python。

## 本轮独立检查

GitHub 直接读取原始 S104 CSV blob 5a535fdb7f54737b2cc4af48707518176b7dd177、结果 JSON blob 7fed42e415e537c932203b41c251077c57392837、B 原始 Python 检查器 blob 6a685c2e89256c84ca6c4636b38be16c2060d5a7、原生重放收据 blob 1781e2ab6132701b86338360ded0e0a8dfc5c25a。

在连接器 V8 中实际解析 432 条持久化 CSV，核对 432 个唯一世界键，对七项门控代数逐条进行 3024 项精确整数比较，全部一致。16组的四方案类别合计 [56,186,276,276]，单例合计 [20,140,270,270]，与归档 summary 一致。冻结提交、schema、证据级别字段当前值一致。

静态检查原始 B Python main() 只读取 data['groups'] 和 data['rows'] 来验证原始 JSON，没有校验顶层 schema、freeze_path、freeze_commit、schemes、summary。其数值核验在自身范围内有效；这些身份及证据声明的完整性需额外守卫。此处是源码可直接确定的覆盖范围，原始 B 对这些字段的动态篡改接受本轮未用原生 Python 复现。

本轮在 V8 对实际持久化 CSV/JSON 运行独立补充守卫：基线 PASS，10 项内存副本变异全部拒绝，覆盖 schema、冻结提交及路径、方案顺序、summary 世界数、E2 声明、类别汇总、重复世界、代数字段、组类别。补充程序 research/operations/e138_r308_s104_metadata_guard_20261031.js 可在本地 Node 对相同归档文件复跑，尚未在本轮原生 Node 执行。

## 治理与未完成项

R308 原正式有限 E1 验收保持，S104 科学状态 PARTIAL。v1 序列化失败及 v2 重放成功并存；不得以 v2 通过抹去 v1 失败。原始 B 的元数据覆盖待补充回归；本轮 E138 保护属于新补充证据。R073 第二独立真人数据集资格仍受限；A轨 PHDCN 原始受限问卷未取得。TH173 只新增理论轨材料。开放 Codex PR #1 R257 S53 原问题与 PR #3 候选修复均未合并，不能视为 main 采纳。R299 S95 语言偏离问题保留开放。无新 E2/E3，未主动运行 Actions，未核实账单及免费额度。

来源：
* https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/b_r308_s104_independent_fraction_audit.py
* https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/B_R308_S104_NATIVE_NODE_AND_PYTHON_REPLAY_ADDENDUM_2026-10-31.md
* https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R308_S104_EXACT_OBSERVABILITY_RESULTS.json
* https://github.com/edwardsage419/Psychohistory-Research/pull/1
* https://github.com/edwardsage419/Psychohistory-Research/pull/3

证据：真实持久化来源 V8 独立整数复算、静态 Python 检查器审阅、非盲态补充人工 E1。新 E2=0、E3=0。下一项：在可用免费 Node 环境对远端归档运行 E138 补充脚本，并请 R/B 轨自行考虑原始 B 的元数据覆盖回归。
