# B轨 R270 S66 独立游程计数与完整收据审计

日期2026-10-29 UTC。目标键：(B,R270,S66,exact-run-composition-vs-direct-enumeration)。证据E1人工。研究者已阅读原R270九世界和冻结协议，属于非盲态内部复算。

## 事前目标与独立计算

R270 S66先行冻结协议提交 `31207d91096972d59749d524f6d145b119cdec68`，然后开始新评分。R使用JavaScript BigInt直接枚举64观察乘64复现。B使用Python Fraction独立游程计数：固定成功数k、相邻相同次数t时，游程数r=6-t，按起始符号拆分1游程与0游程数量，再用组合数C(k-1,r1-1)C(5-k,r0-1)计算序列个数。k=0或6单独处理。B没有调用R的直接复现枚举函数。

B完整核验64个六位串的(k,t)计数，7个k层的总数均为C(6,k)，总计64。三种先验的64项下尾共192项，和R结果逐项精确一致。3先验×3生成概率×3阈值的27项告警概率、告警序列数和相对名义差全部一致。原R270冻结观察`101010`的三个下尾也与历史结果相同。

## 归档和真实执行

R源码 `research/validation/r270_s66_exact_ppc_alarm.js`，持久化JSON `research/validation/R270_S66_EXACT_PPC_ALARM_RECEIPT_2026-10-29.json`，收据Git blob `20fc7f616a3ce2e3b9d30714646f3173d1ffea08`。B可移植Python CLI `research/evidence_audit/r270_s66_independent_run_composition_cli.py`，Git blob `b79636d2969d353954d997717cddbe7115e8e5cd`。本地实际执行脚本的Git blob与远端一致，`python ... --selftest --check <完整JSON>`退出码0。

完整JSON在本地独立Python直接计算的字节Git blob与远端持久化JSON严格相同，避免只比较选取摘要。R归档源码在V8实际执行并重新核验持久化JSON全部字段。R的Node原生命令行仍NOT_RUN，B的Python原生命令行PASS。

## 负例与范围

五项错误注入：篡改概率、删减下尾、增加重复下尾、升级E2标签、布尔值冒充整数，B严格检查全部拒绝。R独立检查器同样拒绝五项。

本轮无样本外真人预测、无概率经验校准、无重采样置信区间、无历史事件数据、无外部团队复现。完整有限枚举消除这套人工空间的Monte Carlo随机误差，但不能消除真实世界模型错设、样本选择或观察测量误差。结论只对冻结网格成立。原R270正式E1验收保持不变，S66仍为`PARTIAL_BOUNDED_INTERNAL_EXACT`。无新增收费计算，无Actions运行。
