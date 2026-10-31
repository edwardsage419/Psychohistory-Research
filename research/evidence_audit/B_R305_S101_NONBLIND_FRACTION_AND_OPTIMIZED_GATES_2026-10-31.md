# B轨：R305 S101 非盲态独立有理数复核与优化模式负例

日期 2026-10-31 UTC。轨 B，内部程序性非盲态复算，**不等于外部团队独立复现**。先行冻结协议 [04dcb04d](https://github.com/edwardsage419/Psychohistory-Research/commit/04dcb04d465002c6f0292887f49ab19f39aa5a11)。

## 方法与实测记录

R路线在V8中以整数化四对象距离计算 MC，并逐世界求社会分类。B路线在可用本地Python中使用 `fractions.Fraction`，独立枚举六对对象距离、两对组内和四对组间均值，重新构造405行和81条五情境路径。没有导入R程序。B计算得到：405世界、810候选评分单元、324相邻比较、36次分类切换，路径变化次数分布 55/16/10/0/0，与R相同。

独立重建的CSV 27133字节，Git blob SHA1 `b940c07bfe6d2ef4f29c806f752b6989202af63f`，与远端R归档CSV完全一致。独立重建的JSON 22216字节，Git blob SHA1 `e3771b29c4e7eeaeef57690ecd9541880881a15c`，与远端R归档JSON完全一致。Git blob哈希包含blob头和长度，证明字节身份，不证明真实人群效度。R程序另读取原R305冻结JSON逐世界对比243项，243项一致。

B的9项变异：删行、重复行、lambda篡改、特征篡改、MC篡改、社会得分篡改、类别选择篡改、总切换数篡改、证据等级E2伪升级。Python正常执行9项全部拒绝。

## 发现并保留的失败

最初归档 [B v1](r305_s101_independent_fraction_audit.py) 采用 Python `assert` 作为主要审计门。实际执行 `python -O` 时出现 `AssertionError: mutation escaped` 且退出码1，证明优化模式可移除关键验证条件。此失败不删除。

新增 [B v2](r305_s101_independent_fraction_audit_v2.py)，将关键断言替换为显式 `ensure` 抛异常。在本地以与归档v2同一逻辑的源代码分别运行普通模式与 `python -O`，两次均为 `audit=true, mutations_rejected=9`，生成的CSV与JSON blob SHA与远端R结果一致。B v2新归档源码未在原生远端环境执行，标记 NATIVE_ARCHIVED_CLI_NOT_RUN。v1失败不被v2通过记录覆盖。

## 验收边界

所有检查为内部非盲态E1数学和归档一致性审计。数据泄漏、真实样本外预测、概率校准、群组重采样与外部独立样本检验均无可用真人数据，状态 NOT_RUN。没有外部研究者复现，没有新增E2/E3。S101 PARTIAL，原R305有限E1验收不变。R073及PESEN v0.1继续冻结。GitHub Actions未启动，费用额度未核实。
