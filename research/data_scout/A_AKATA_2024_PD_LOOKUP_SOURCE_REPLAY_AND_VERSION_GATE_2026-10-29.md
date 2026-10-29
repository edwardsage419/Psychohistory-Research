# A轨：Akata真人与LLM重复博弈数据的原始查表重放及版本缺口

日期：2026-10-29 UTC。目标键：`(A,eliaka/repeatedgames@224a605a21127cac69763f990e077f7b05abd422,PD lookup,cleaned CSV payoff and chronology)`。此前 [A轨原始3900行审计](A_AKATA_2024_REPEATEDGAMES_HUMAN_LLM_CSV_AND_PAYOFF_GATE_2026-10-29.md) 已确认195名匿名真人，每人10轮PD和10轮BoS，并发现第3061行 `action=0,score=0` 异常。

## 本轮实际读取的公开英文原始材料

* 原作者 cleaned CSV `human_experiment/analysis/repgames.csv`，Git blob `2dd67c6ff80f2d7aa07a70b470e26fe3592c6d95`，3900行：https://github.com/eliaka/repeatedgames/blob/main/human_experiment/analysis/repgames.csv
* 实验 JavaScript `human_experiment/experiment/js/script.js`，Git blob `4b7be85e8b3b964bfd0722d796f5ed6c2b8f0a19`：https://github.com/eliaka/repeatedgames/blob/main/human_experiment/experiment/js/script.js
* 原作者 `pd_gpt4_lookup.json`，Git blob `f37f26aad7942099f1158ac8f84eb071960b4929`，以及 `pd_variation_predict_gpt4_lookup.json`，Git blob `93e1840fec47b77cf899582c62b53cde603058f1`；各有1023个历史行动前缀键。路径均在 `human_experiment/experiment/lookups/`。
* 实验 README Git blob `77115c8edb43dbc7ef8bc46e596f67d58f2c8f81`，原始收益矩阵；Rmd `ca9991b6d0917156672e1e2fea923548562d945e`，声明 CSV 为清洗后的 Prolific 数据。
* 根目录 MIT 软件许可证 `LICENSE.md`，blob `108cffb7c9fcd38dadc419f4c18e4e3e0afb4407`；真人数据文件的单独再分发许可仍未得到确认。

## 实际新复核

新增 [可重放的 JS 原始查表审计程序](a_akata_pd_lookup_crosscheck_20261029.js)，已在 V8 环境以三个原作者文件完整内容运行，并在提交后重新读取远端归档脚本运行。

脚本按 CSV 中每名真人的 PD 记录顺序推导历史行动前缀，按 `Base` 或 `Prompted` 选择相应的原作者查表 JSON。然后根据原作者实验 JS 的收益函数逐条重建期望收益。

| 诊断项 | 数量 |
| --- | ---: |
| 原始总记录 | 3900 |
| PD记录 | 1950 |
| 匿名真人ID | 195 |
| 查表及收益一致 | 1826 |
| 查表与收益不一致 | 124 |
| 历史前缀未命中 | 0 |
| 第一轮不一致 | 0 |
| 存在至少一处不一致的参与者 | 85 |
| Base条件一致 / 不一致 | 907 / 63 |
| Prompted条件一致 / 不一致 | 919 / 61 |

第3061行位于匿名ID 153的PD第10轮。按 CSV 推导前九轮行动前缀为 `JFFFFJJFF`。原作者Base查表在该前缀返回 `F`。第10轮真人行动 `0` 即 `F`，原JS收益应为5，CSV记录为0。

原始 `calculate_points_pd` 先将收益设为0，然后按合法行动及对手行动组合赋值。故某个查表值缺失或不被识别时可能留下0。当前前缀在仓库归档查表中确实存在，无法据此确定采集当时查表文件是否相同，也无法排除清洗转换或数据导出顺序差异。124处不一致均只登记为**版本或时间序列对齐待查诊断**，不判定124个真实实验记录错误。

## 复现门与后续

公开来源与文件字节身份：VERIFIED。CSV的PD行为/匿名ID/十轮区块：VERIFIED。CSV区块内行序与原采集时序完全一致：OPEN。当前仓库查表版本等于实际实验运行时查表版本：OPEN。124处差异的来源：OPEN。真人数据再分发许可：OPEN。独立场次身份及真人对手逐轮行动：NOT_PRESENT，实际为人机互动。R073冻结的双人100轮直接复验：NO。

本轮新增真人E2正式预测0项，历史E3预测0项。没有重新分发原始真人CSV，也没有重写其异常值。下一步需作者的实验版本/清洗代码及真实行序证明，之后才可考虑单独冻结适合10轮人机实验的预测协议。
