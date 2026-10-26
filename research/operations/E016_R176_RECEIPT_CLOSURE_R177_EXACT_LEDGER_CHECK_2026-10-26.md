# E016 R176 完整收据归档关闭核查与 R177 两群组判别精确收据独立只读审计

日期：2026-10-26，Asia/Singapore。track: operations。subflow: E。status: COMPLETE_BOUNDED_READONLY_DELTA。写前 main HEAD `fbf347602df7c40218147fbdf0f500e7ab9b53b9`。本日正式全轨日检 E004 已完成，本报告只处理 E015 之后的实质新变化。CI: NOT_RUN。主动新增费用0，账户账单与免费权益余量未独立核验。

## 1. 本轮实际核查的来源与时间顺序

读取 main 最近提交、MKT046、E015、F002、R176 补档及命令更正报告、R177 主科学报告、B独立方法报告、两份R177机器收据及R176完整机器收据。检查 MKT047 与本报告目标路径的占用状态。没有修改其他研究轨文件、共享索引或冻结协议。

* R176 完整原始收据新增提交 `672093197b246bd1032a4f7b5d5d4e0e5d9c10cb`，新路径 `research/validation/r176_institution_observability_receipt_20261026.json`，Git blob `bb9b4d604575478846f40120dde3b1fdbed2d6fc`。GitHub 读取文本长度 60487 字符，内容是纯ASCII JSON，与补档报告所述60487字节相符。补档报告记录原始 SHA256 `a7c45ab4637a49cbf80958e3deade64e8cd3be0a758edfeaf44b5fc95933aa0a` 和远端回读核验。本轮独立核实远端文件存在、blob与结构，未重新对全部原始字节计算 SHA256，故此SHA256匹配结论仍由R轨补档报告支持。
* R176 补档报告 `R176_FULL_RECEIPT_ARCHIVE_CLOSURE_AND_STATIC_CHECK_2026-10-26.md` 已存在，另有 `R176_FULL_RECEIPT_REPLAY_COMMAND_CORRECTION_2026-10-26.md`，更正B脚本真实路径为 `research/evidence_audit/r176_b_path_mass_identity_20261026.py`。不改动原始历史 `full_receipt_archived=false` 摘要。
* R177 新第三方法冻结提交 `95fcf7536e31f2ab214c205bd6fdc5b03223d99d`，主报告提交 `333494324e9da33977310d3c9e8e21b77e62e12f`。GitHub compare 为 ahead_by=6、behind_by=0，说明新增协议早于这次补充计算报告。期间另有R176补档与R177源程序、收据提交，不能把整段6提交全部称为R177独立研究。
* R177 主报告 Git blob `94f70df975fa9f8aa2bf5df638e48a4c388e0fad`，B报告 blob `b76d3bc7b0bd243236b092205d6687711b625814`。本轮未改写。

## 2. R177 精确机器收据独立一致性审计

直接读取 `research/validation/R177_TWO_GROUP_BAYES_ERROR_EXACT_RECEIPT_2026-10-26.json`，Git blob `a5b155e54614bb931a1dc02529bff49fce11f009`，405行 pairwise_exact。用独立 JavaScript BigInt 有理数交叉乘法逐行检查：

* 恰有9个(n,p)分层，每层45对，合计405对；405个配对键均唯一。
* 全部405对满足 `0<=TV1<TV2<=1`；405次严格增益、0次相等、0次等价对。
* 全部405对同时满足 `BayesError_m=(1-TV_m)/2` 的精确有理数恒等式，两个m共810个错误率值核对无异常。
* 重新扫描全部405行的TV1和TV2精确最小最大值，4个极值均与摘要相等。
* B独立收据 `research/evidence_audit/B_R177_OVERLAP_EXACT_RECEIPT_2026-10-26.json`，Git blob `8268f10deaea98f83f59b32d5b100219348a2763`，记录 `checked_pairs=405`、`checked_order_swap=405`、`exact_mismatch_count=0`，source_blob_sha与主收据同为 `8a8819e4d85989b518b9152cfc98336457c76a9c`。本轮核对B收据字段，没有重新执行B脚本或原始PMF的全部张量积计算。

这里的405对共享90个理论参数世界，不能视为405个独立真人实验；误差率只对已知候选、等先验、独立群组假设成立。原n2 BB/ZIB分布等价反例保持存在。当前是内部E1数学结果及收据结构核验，真人E2=0、历史E3=0、外部复现=0。

## 3. R176 完整收据静态复核及 E015-01 状态变化

直接读取60487字节对应的完整 JSON，包含48个世界、每行13期 `joint_tv` 和 `count_tv`，共1248个精确分数单元。独立用BigInt逐项核对：624个时点全部满足 `0<=TV_count<=TV_joint<=1`；24组 `dropout=0` 的13期值全为0；24组 `dropout=1/4` 的联合首次非零期均为t2、人数首次非零期均为t3；`first_joint`、`first_count` 元数据48行全一致。异常0。

因此 E015-01 的“完整原始收据尚未上传”归档问题现可标记 `CLOSED_ARCHIVE_BYTES_PRESENT`。完整SHA256独立复算、R/B实际脚本重新执行、t4至t12第三路线逐状态算法复验仍是单独验收问题，不能因文件已归档自动关闭。

## 4. CI、费用、跨轨边界与未关闭问题

通过GitHub Actions REST按 `head_sha` 分别查询 R177主报告提交 `333494324e9da33977310d3c9e8e21b77e62e12f` 和R176补档提交 `672093197b246bd1032a4f7b5d5d4e0e5d9c10cb`，两者返回 `total_count=0`。只能认定指定SHA未查询到关联运行，不能将代码提交或本轮独立静态核查称为远端CI通过。未启动Actions。

本轮新文件只在 `research/operations` 增量新增，不触及R、A、B、TH、C、D、F、market或冻结协议。没有全仓文件名冲突与哈希穷举，未作全局无误声明。MKT047在 `research/market` 独立归档，F002已完成2026-W44专题，未重复创建F文件。零新增费用约束继续有效。

E016-01 CLOSED_ARCHIVE_BYTES_PRESENT：R176完整收据已经远端归档；本轮仅核验存在、blob和结构，原始SHA256比对仍以R轨报告为依据。
E016-02 OPEN：R176 t4至t12完整第三路线独立计算与B脚本实际重跑未核验。
E016-03 OPEN：R177 B收据报告405对一致，尚缺本轮从原始R177 PMF独立生成全部405个张量积的第三条计算路径。
E016-04 OPEN：指定R176/R177新增提交没有关联Actions运行，不能宣称远端CI PASS。
E016-05 OPEN：继承E015的R175原始工作簿、R174后期独立路径、R170全状态复核、R136冻结负对照、original239剩余逐项审计等未关闭事项。原E004对R073来源缺口的早期表述已有后续E006等报告更新，不沿用过期结论。
E016-06 OPEN：账户实际账单、免费权益余量、全部冻结协议与全仓同名冲突未作独立全面核验。

## 5. 主要来源与下一项

R176完整原始收据：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/r176_institution_observability_receipt_20261026.json

R176补档：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R176_FULL_RECEIPT_ARCHIVE_CLOSURE_AND_STATIC_CHECK_2026-10-26.md

R177主报告：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R177_TWO_GROUP_BAYES_ERROR_THIRD_METHOD_SCIENTIFIC_REPORT_2026-10-26.md

R177主收据：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R177_TWO_GROUP_BAYES_ERROR_EXACT_RECEIPT_2026-10-26.json

R177 B收据：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/B_R177_OVERLAP_EXACT_RECEIPT_2026-10-26.json

下一轮E优先检查新R178及以后真实新增成果，跟踪R176完整后期复算、R177独立原始PMF重算、CI状态和未关闭队列。先完成全部R系列，再系统归纳，最后熔炼；不得更改冻结协议或提前开发个人决策产品。
