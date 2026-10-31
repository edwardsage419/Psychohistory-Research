# B R305 S101 原生CLI补验及保留优化模式失败

日期：2026-10-31 UTC。非盲态内部数学/工程复验。此文补充前一份B报告，原始B v1优化模式失败保持不变。

## 原生来源身份

在可用本地计算环境使用 Node v22.16.0 与 Python 3.13.5。先将归档源码逐字节恢复到隔离目录，按Git blob对象算法重算源码身份：

| 源码 | 与main归档相同的Git blob SHA1 |
| --- | --- |
| R Node `r305_s101_interpolated_context.js` | `bc7694766dba68a5203c5a7bda3d26eeb550d951` |
| B Python v1 | `a39cbba20d93616e3a283eddaffd3d010bcd2122` |
| B Python v2 | `cd7ba36240144f17e314a9ce1b00bbd4101d8457` |

## 实际执行

1. `node r305_s101_interpolated_context.js --emit <temp_dir>`，退出码0，输出405世界、36次切换、55/16/10/0/0轨迹分布。生成的27133字节CSV与main Git blob `b940c07bfe6d2ef4f29c806f752b6989202af63f` 完全一致；22216字节JSON与main Git blob `e3771b29c4e7eeaeef57690ecd9541880881a15c` 完全一致。
2. `python r305_s101_independent_fraction_audit_v2.py --check <native_csv> <native_json>`，退出码0，audit=true，9项篡改均拒绝。
3. `python -O r305_s101_independent_fraction_audit_v2.py --check <native_csv> <native_json>`，退出码0，audit=true，9项篡改均拒绝。
4. 保留原v1失败：`python -O r305_s101_independent_fraction_audit.py`，退出码1，错误 `AssertionError: mutation escaped`。v1旧版本在优化模式下仍不安全，不回填旧报告的PASS。
5. 原R305 X/MID/Y三个冻结情境的243条决策，在此前的V8读取原R305完整JSON后核对243/243一致。

原生程序与B v2的源码身份及数据归档字节身份均已经闭合，状态 `NATIVE_CLI_REPLAY_COMPLETE`。这只覆盖当前S101的计算和持久化收据。历史R305原有的正式E1有界验收保持不变。

## 科学范围

本轮无真人样本外预测、真实概率校准、跨实验复现、独立外部研究者或历史预测。原始S101科学状态仍为PARTIAL，E1人工机制。未触发GitHub Actions，CI=NOT_RUN；没有计费计算操作，账户余额未知。见[机器收据](B_R305_S101_NATIVE_CLI_AND_OPTIMIZED_MODE_RECEIPT_2026-10-31.json)。
