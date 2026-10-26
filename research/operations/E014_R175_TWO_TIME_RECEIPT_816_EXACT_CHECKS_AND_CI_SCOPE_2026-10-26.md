# E014 R175 两期噪声观测收据的独立只读审计

日期：2026-10-26，Asia/Singapore。track: operations。subflow: E。status: COMPLETE_BOUNDED_READONLY_AUDIT。observed_head: 6d2fe97df634b0339540cffa47261086038c5c56。本日 E004 已完成日检，E005 至 E013 为增量审计；本轮针对 E013 后出现的 R175 研究，避免重复其他轨的科学报告。ci_status: NOT_RUN。billing_checked: 主动新增费用 0，账户整体账单及 GitHub 免费额度未独立核验。

## 1. 仓库进度及冻结先后

2026-10-26 09:48:37 Asia/Singapore，R175 新增协议冻结提交 c6e3867a7667a74451b1e9ef1fbe3b3966bfab04；09:50:25 新增主程序、机器收据、B 独立代数程序与 A 数据侦察提交 1dcefc533e2301989cbeabe34f12e61b91b0023f。GitHub compare 返回 ahead_by=1、behind_by=0，七项文件均为新增，未在该提交修改原冻结协议。

本轮从 main 直接读取原始 R175_EXACT_RESULTS.json，Git blob 98da532e3656ff86caf5238d5174d211e3ca28d3；原 R175 预评分协议 Git blob 4a989e7d00a54147e3e3c7fbccc37fcb9042b509，与新增冻结协议声明的上游 blob 一致。新增协议 Git blob 641e500c50f8edef2166a461ebaa8eb6b98588a9。

新增研究是原 R175 已有结果之后冻结的独立补充实验，冻结顺序仅支持“补充实验计算前冻结”，不支持将其描述为原始 R175 首次评分前的盲法协议。

## 2. 独立重算收据一致性

直接读取：
1. research/validation/R175_NOISY_TWO_TIME_EXACT_RECEIPT_2026-10-26.json，Git blob 40e18b7b0a9a2d88d47eb9ee8a2c429720c505d2。
2. research/evidence_audit/B_R175_COVARIANCE_IDENTITY_EXACT_RECEIPT_2026-10-26.json，Git blob 7b01dc2066b2ed12649841ea07da53dea6cccd77。

使用独立编写的 JavaScript BigInt 分数运算解析两个 JSON，按 π、ε、lag 配对48组。对每组的 n1、n3 各四格联合概率逐格跨收据比较，共384项；各分布归一、两期边际匹配所报单期概率，共288项；对每组按半个 L1 距离独立重算 TV，并分别核对 R 与 B 的 TV 以及 R 的等先验 Bayes 错误率，共144项。总计816项精确有理数断言，0项失败。

复算发现全部48组 TV>0；最小约 0.00000039173640816605，最大 15/448，约0.03348214285714。固定 π=1/2、ε=1/4、lag=1 的 TV=15/448，Bayes 分类错误率=433/896，与原报告一致。

本轮检查对象是已归档的两个 JSON 收据及其内部数学关系。没有重新从原始转移矩阵独立生成48组联合概率，也没有运行 R/B 两份 Node.js 源程序。因此“816项收据检查通过”仅是收据级第三路径的部分独立核验，不能等同完整算法复现或外部团队独立验证。

## 3. CI、数据与证据等级

GitHub Actions 按 head_sha 分别查询 c6e3867a7667a74451b1e9ef1fbe3b3966bfab04 和 1dcefc533e2301989cbeabe34f12e61b91b0023f，均返回 total_count=0。仅能认定所查两个 SHA 无关联 Actions 运行，不能宣称远端 CI 成功或仓库全部 CI 缺失。两次提交信息包含 [skip ci]，不代表测试已通过。本轮没有触发 CI。

A 轨 Cornish、Smith、Kirby 2008 爱丁堡大学数据侦察报告记录官方 DOI 10.7488/ds/1586、CC BY 4.0 和发布者 MD5，但原始 CornishData.xlsx 字节、实际字段、链身份及 SHA256 尚未核验。该数据的人工语言传承机制与 R175 二元潜在记忆模型之间的冻结映射尚未建立，暂不能升级真人 E2。当前新增 E1 数学补充、E2=0、E3=0。

TH048 是理论轨独立报告，不计为 R175 实证证据。市场 MKT045 已在独立路径归档，F002 本周专题已完成，本轮未重复建立 F 文件。

## 4. 新增与继承的未关闭问题

E014-01 HIGH OPEN：R175 两条源码路线的完整独立重跑、由原始转移矩阵生成收据及第三方复验仍待确认。当前仅收据层816项精确核对。

E014-02 HIGH OPEN：CornishData.xlsx 原始字节、MD5、工作簿字段及冻结模型映射未闭合；真人实验评分保持阻塞。

E014-03 MEDIUM OPEN：新补充协议冻结于原 R175 结果之后，所有正式报告应标明 postscore addendum。

E014-04 MEDIUM OPEN：指定新增提交无 Actions 运行，不能借用原 R175 历史 CI 作为新算法验收。

E014-05 HIGH OPEN：沿用 E013 的 R174 后三期独立逐时概率复核、E009 的 R170 全状态跨路线比较、R136 冻结负对照与原始239项索引未完成逐项核验。未因本次 R175 检查关闭。

E014-06 MEDIUM OPEN：本次只覆盖最新 R175 文件和相邻提交，没有对整个仓库全部文件名、冻结协议、证据分类或所有 Actions 进行穷举审计；费用账单未独立核验。

研究顺序继续完整 R 系列，再系统归纳，最后模型熔炼。E 仅新增只读问题记录，不修改 R、B、A、TH、market、F 或任何索引。

## 5. 来源和下一项

冻结协议：https://github.com/edwardsage419/Psychohistory-Research/blob/main/protocols/R175_NOISY_TWO_TIME_OBSERVABILITY_THIRD_METHOD_FREEZE_2026-10-26.md

主收据：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R175_NOISY_TWO_TIME_EXACT_RECEIPT_2026-10-26.json

B 收据：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/B_R175_COVARIANCE_IDENTITY_EXACT_RECEIPT_2026-10-26.json

A 来源资格：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/data_scout/CORNISH_KIRBY_SMITH_2008_EDINBURGH_ITERATED_LANGUAGE_RAW_GATE_2026-10-26.md

下一次 E 优先核查 R176 近期增量与原冻结顺序，或追踪 R175 原始数据阻塞；如未出现新文件则不重复归档。
