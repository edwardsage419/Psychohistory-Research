# E015 R176 制度观察第三方法的独立只读核查与完整收据归档缺口

日期：2026-10-26，Asia/Singapore。track: operations。subflow: E。status: COMPLETE_BOUNDED_READONLY_DELTA。observed_main_head_before_E_write: fe1311208fb7dd0b02d2ba21911963b427293dcb。本日正式治理检查已由 E004 完成，E015 针对 E014 之后新增 R176 的实质增量，不重复其他研究轨原有报告。CI: NOT_RUN。主动新增费用 0，账户账单与 GitHub 免费额度未独立核验。

## 1. 冻结顺序、文件变更与任务边界

2026-10-26 新增 R176 第三方法协议冻结提交 `c2d86eee113b14809ed8e5cfc953faa8240ce17b`，后续科学执行及 B/A 轨归档提交 `1f422dcc535413a9328af341ae5d39a1fecfe32f`。GitHub compare 核验 ahead_by=1、behind_by=0，执行提交新增 7 个文件，没有修改原 R176 研究文件及本次冻结协议。

冻结协议 Git blob `14272249c51d24f512cc6789ef73daec4b53c0d7`，声明原 R176 源码 blob `0d8ec07b96307f34b352e193ff4fa66d52eb39a9` 和原结果 blob `97d55b9379609802bc38ed076bc1518e22eb5ed8`。本轮独立读取新增主收据 blob `3fb2f410557057235fc609940b8dcf5a8d6003bf`、B 收据 blob `cb85163a26a6dc9da49f41b0b6f362ad8c4a34dc` 及两份 Python 源码。新增协议冻结发生在原 R176 正式结果之后，性质是 postacceptance addendum，不能追溯声称原始结果事前盲法冻结。

## 2. 独立第三路径精确复算

本轮实际使用独立编写的 JavaScript BigInt 有理数运算，未调用 R/B 两份 Python 源程序。重新构造四主体二项转移、两种制度规则和 (k,J) 状态，遍历 mu={1/8,1/4}、beta={0,1/4}、gamma={0,1/2}、dropout={0,1/4}、initial_k={1,2,3}，共48对世界。分别从相同初态精确传播 t=0..3，比较完整状态及 k 边际的总变差距离。

独立计算得到：
* 48 对中 dropout=0 的24对在已检查 t=0..3 完全等价；dropout=1/4 的24对在 t=2 的完整 (k,J) TV 均为正，t=3 的仅 k TV 均为正。
* 所有48对在 t=0、t=1 的完整 TV 为零；t=2 的仅 k TV 为零。
* 活跃24对的 t=2 联合 TV 精确范围 `19929/4194304` 至 `117369/1048576`，与主收据完全一致。
* 活跃24对的 t=3 人数 TV 精确范围 `23113839/17179869184` 至 `629133561/17179869184`，与主收据完全一致。
* 按上述预先列明的分组及极值检查，异常对数 0。

这提供了一个实现语言与代码结构独立的局部复算，支持 R176 t2、t3 的观察分辨率差异。当前 JS 复算止于 t3，没有逐项重算 t4..t12、全部3840个微观聚合单元或主程序完整收据；不能将其称为完整第三方算法复现。主程序与 B 程序在原报告中分别声称3840单元和48对两步路径恒等式，本轮仅通过源码及机器收据核对其声明，没有重新执行全部两份脚本。

## 3. 新发现的归档质量问题

主收据明确记录 `full_receipt_generated_locally=true`、`full_receipt_archived=false`，并给出本地完整精确 JSON 的 SHA256 `a7c45ab4637a49cbf80958e3deade64e8cd3be0a758edfeaf44b5fc95933aa0a`。仓库中有摘要收据及生成脚本，尚缺该完整结果 JSON 的远端原始字节。B 源码读取的文件名是 `r176_institution_observability_receipt_20261026.json`，即需要先执行 R 主脚本生成本地文件，再运行 B 脚本。当前 Git 归档没有该输入文件。

结论：可复算程序与摘要已经归档，B 的原始输入收据尚未作为不可变 Git 对象独立归档；仅凭当前仓库静态文件无法直接重跑 B，必须先运行 R 生成依赖文件。此为复现链和归档完整性问题，不代表 R176 数学结果错误，也不能虚报完整原始收据已上传。修复应由 R/B 轨在各自路径新增完整收据并验证 SHA256，E 只登记问题。

## 4. CI、数据源、证据等级与并发控制

通过 GitHub Actions REST 按 head_sha 查询冻结提交 `c2d86eee113b14809ed8e5cfc953faa8240ce17b` 和执行提交 `1f422dcc535413a9328af341ae5d39a1fecfe32f`，两者返回 total_count=0。只能认定这两个指定 SHA 未查询到关联运行，不能宣称 CI PASS，也不能推断仓库其他历史 CI 状态。本轮没有触发 Actions。

A 轨 V-Dem v16 资料记录官方国家年度数据与 Git blob 存在，但 RData 原始字节、实际列、国家年份及模型适配尚未逐行核验。该数据不能直接验证四主体微观因果机制，新增真人 E2=0、历史预测 E3=0。R176 新增成果仅为内部 E1 数学证据，未产生真实样本外预测或外部独立复验。

同一 main 上的 MKT046 归档路径为 research/market，E015 只新增本文件，不改写 R/B/A/TH/F/market 的研究结果、协议和索引。本轮仅对最近增量做有限审计，尚未穷举整个仓库的同名文件、证据级别、全部冻结协议和账单。

## 5. 未关闭问题

E015-01 HIGH OPEN：R176 完整逐世界、逐期精确收据只记录本地 SHA256，Git 未归档其原始字节；B 运行依赖此文件。应由对应研究轨新增收据并回读核验。
E015-02 MEDIUM OPEN：本轮独立第三路径仅覆盖 t0..t3；t4..t12 的完整跨方法逐格复核仍待补足。
E015-03 MEDIUM OPEN：指定两个 R176 提交无关联 Actions 运行，远端 CI 验收不能认定成功。
E015-04 HIGH OPEN：V-Dem v16 原始 RData 逐行核验、冻结映射与独立历史预测仍被阻塞。
E015-05 HIGH OPEN：继承 E014 的 R175 原始工作簿阻塞、E013 的 R174 后三期第三路线、E009 的 R170 全状态比较、R136 负对照与239项原始模型索引未完全核验。此次增量没有关闭这些问题。
E015-06 MEDIUM OPEN：GitHub 账户账单及免费额度未独立核验；仅能声明本轮主动新增费用为零。

## 6. 来源与下一步

冻结协议：https://github.com/edwardsage419/Psychohistory-Research/blob/main/protocols/R176_INSTITUTION_OBSERVABILITY_THIRD_METHOD_FREEZE_2026-10-26.md

主报告：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R176_INSTITUTION_OBSERVABILITY_THIRD_METHOD_SCIENTIFIC_REPORT_2026-10-26.md

主摘要收据：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R176_INSTITUTION_OBSERVABILITY_THIRD_METHOD_RECEIPT_2026-10-26.json

B 方法与收据：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/B_R176_PATH_MASS_IDENTITY_SCIENTIFIC_AUDIT_2026-10-26.md

A 来源门槛：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/data_scout/VDEM_V16_2026_COUNTRY_YEAR_INSTITUTION_HISTORY_SOURCE_GATE_2026-10-26.md

下一次 E 优先检查新 R 系列研究及 R176 完整收据是否补齐。2026-W44 F002 已完成，本轮没有重复创建 F 文件。项目顺序继续先完整 R 系列，再归纳分类，最后模型熔炼。不得修改任何冻结协议或引入新增费用。
