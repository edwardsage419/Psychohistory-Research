# E017 R178 Wilson 区间逐格精确核算、源PMF重建与科研证据边界只读审计

日期：2026-10-26，Asia/Singapore。track: operations。subflow: E。status: COMPLETE_BOUNDED_READONLY_DELTA。写前 main 最新观察 HEAD：`7a41c5cd7669abd632df553f5d06ac32f9ed4937`。今日正式全轨日检 E004 已完成，E016 已覆盖 R176、R177，本报告仅登记 R178 新增增量。CI：NOT_RUN。本轮主动新增费用0，账户账单及 GitHub 免费额度未独立核验。

## 1. 本轮实际读取与去重

读取 main 最新提交、MKT047、E016、F002、R178 新增协议、主研究报告、B轨独立报告、两份机器收据、R178 原始精确数据及 R178 事后例外诊断。核对 market 本轮新增 MKT048 只写入独立 `research/market` 路径。没有更改 R、A、B、C、D、F、TH 轨文件、冻结协议或共享索引。

R178 第三方法协议冻结提交 `8712c87d8af4800f19be7acc9ccc6b7985a74043`；主研究与B轨收据提交 `c8d7146fce14a766474aecca5ea6421dbbb6a4f6`。GitHub compare：ahead_by=1、behind_by=0，确认新增冻结协议在该补充研究结果之前。后续事后诊断提交 `9ea0508d6562b18530f885dda028dc404a6d8394`，明确是探索性事后解释，不能追认预注册确认性发现。

来源：
* 冻结协议：https://github.com/edwardsage419/Psychohistory-Research/blob/main/protocols/R178_WILSON_SCORE_COVERAGE_THIRD_METHOD_FREEZE_2026-10-26.md
* 原始人工精确PMF：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/R178/R178_EXACT_RESULTS.json ，Git blob `3b4a5abeaa14b5be32fb258a15aa6bf502b2756c`。
* 新方法主收据：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R178_WILSON_SCORE_COVERAGE_EXACT_RECEIPT_2026-10-26.json ，Git blob `39aa27e656595550620c45688cf5ee122e133fff`。
* B轨收据：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/evidence_audit/B_R178_WILSON_SCORE_INDEPENDENT_RECEIPT_2026-10-26.json ，Git blob `b24c138aedf72edae3f948099c6c4d9d109ec9f9`。
* 事后诊断：https://github.com/edwardsage419/Psychohistory-Research/blob/main/research/validation/R178_WILSON_EXCEPTION_POSTSCORE_DIAGNOSTIC_2026-10-26.md 。

## 2. 独立精确审计：从原始PMF重建30组覆盖率

本轮在 GitHub 连接器中直接读取原始 `source_worlds` 30行及每行 `full_training_count_pmf`，合计270个概率单元。使用另写的 JavaScript BigInt 有理数运算，逐格重算 Wilson 与 Wald 两个覆盖区间的成员关系，逐世界对原始概率质量求和，再与第三方法主收据精确比较。无浮点容差、无对原作者脚本的执行依赖。

Wilson 对 p=a/b、样本数 n、计数 k 的整数判定：
`(kb-na)^2 * 625 <= n * 2401 * a * (b-a)`。

Wald 的整数判定：
`(kb-na)^2 * n * 625 <= 2401 * k * (n-k) * b^2`。

固定 z=49/25。每个世界核对源概率质量总和等于1、Wald 覆盖率精确分数、Wilson 覆盖率精确分数，及原始世界与主收据的 n、p、机制映射。计数：270个概率单元，每格两次区间判定加一次概率累计，30个世界各核对三个精确汇总条件，**合计900项精确检查，0异常**。另在主收据层面核对540个成员标记和30个精确差值，**570项检查，0异常**。两个检查批次共享主收据，不能简单视为1470项独立研究样本。

重新统计 Wilson 相对 Wald：19组改善、10组相等、1组恶化；Wilson 低于95%名义覆盖27组，Wald 低于95%共30组。上述30个世界共用人工生成家族，不能称为30项独立真人复验。

## 3. 唯一恶化世界及证据限制

事后诊断锁定 n=12、p=1/4、INACTIVE_ZIB_Z1_4：Wilson 允许 k=1至5，Wald 允许 k=2至6。源PMF给出 P(k=1)=2048/59049，P(k=6)=4928/59049，Wilson 相对 Wald 覆盖差为 `-320/6561`，约负4.8773个百分点。两种覆盖率分别为 `108224/177147`（61.09%）和 `116864/177147`（65.97%）。本轮原始PMF逐格重算已覆盖这一世界，精确差值与收据一致。不能声称 Wilson 在所有相关或零膨胀模型下都优于 Wald。

B轨收据自报540个成员判定、60个世界覆盖率、原Wald30组重算及 z=1 负对照改变60格，记录0 mismatch。本轮独立核查了B收据字段并从原始PMF复算覆盖率，**没有重新执行B轨原始脚本**，也没有引入新的真实实验。主R与B两种算法使用同一冻结人工PMF，研究等级仍为内部 E1，E2=0、E3=0、外部复现=0。

## 4. 跨轨状态、CI、费用与未关闭队列

R系列继续沿既定研究顺序推进。新 R178 协议、主收据和 B 收据的相对顺序符合本次冻结检查；不能据此证明所有历史冻结协议均未改动。最新TH051独立更新理论索引，A轨 Pereda 2019 继续资料门槛审查，未对其原始真人数据执行 E2。MKT048仅新增市场报告，不覆盖其他轨。F轨本周 F002 已完成授权撤销与衍生数据生命周期专题，不重复创建F文件。

对 R178 协议提交、主收据提交和事后诊断提交分别调用 GitHub 连接器 workflow runs 和 combined status，均返回空数组。该 workflow 查询接口仅覆盖部分触发方式和首个分页，不能将空数组解释为全局无运行。**远端 CI PASS 未建立，本轮没有启动 CI。** GitHub 仓库拥有写权限；本轮没有调用任何计费服务或新增订阅，账户整体费用未独立核验。

E017-01 CLOSED_BOUNDED：R178 原始270格概率质量与两种覆盖率的独立精确重算完成，900项检查零异常。
E017-02 OPEN：R178 30组均为人工 E1；尚无真实人类 E2、独立历史预测 E3、外部研究者复现。
E017-03 OPEN：R178 新增方法的远端 Actions 验收未核实；不能以本轮本地/连接器精确计算代替 CI。
E017-04 OPEN：R176 t4至t12完整第三路线复算、R177从原始PMF独立重建、R175原始工作簿、R174后期状态复算、R170全状态比较、R136历史负对照、original239逐项核查，沿用 E016 未关闭队列，未在本轮重复验收。
E017-05 OPEN：Pereda 2019 Zenodo 原始数据文件、许可证、分组与场次及时间泄漏仍未直接核实；不可作为 R073 冻结二人PD协议的替代 E2。
E017-06 OPEN：全仓同名冲突、账户账单及免费额度没有全面独立核验；不能宣称全仓无误或费用账单完全核清。

## 5. 下一轮

E下一轮优先审计 R179 或 R178 后续真实新增提交，检查新冻结协议、原始收据、独立算法、CI 与归档缺口。若没有新增 R 成果，按上述开放队列选择可在免费条件下独立复核的一项。F维持2026-W44已完成状态，候选问题包括市场轨 MKT048 的含糊结算、历史评分归属与人工申诉。项目顺序保持：先完整R系列，再统一归纳分类，最后模型熔炼。
