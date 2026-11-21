# R272 P0：冻结三项科研 CI 的独立来源校验补充

日期：2026-11-17 UTC。此文件是 R272 既有工程审查 PR #51 的增量回归，原报告、原 CI 失败记录及冻结科学结论保持不变。

## 精确研究目标和非重复范围

原 R272 2026-10-23 事前冻结合同要求完整来源枚举、Python 3.11 与 3.12 的原生数学测试，以及一个**不依赖原生成器**的第三来源审计。现行正式 main 生产 workflow 包含优化敏感 assert、在来源核验前先 --emit，以及自动写回 main 的安全缺口。本 PR 的既有候选隔离 v2 已在实际 GitHub 3.11、3.12 验证旧单入口及攻击回归。

此前 PR #51 的三个成功 job 分别为两个不同 Python 的数学验收、一个**安全攻击** job。**第三项独立科研来源 job 当时仍然缺失**。本轮使用独立源码补上，避免把安全攻击 job 误算成冻结科研验收所要求的第三种方法。

## 新增独立程序

新程序：`research/validation/r272_frozen_independent_third_source_20261117.py`。

程序仅使用 Python 标准库 `csv`、`fractions.Fraction`、`json`、`itertools`、`hashlib` 及 `math.comb`，不 import R272 原作者/本项目原生成器、原 pinned wrapper、原单入口候选，也不复用隔离 v2 的验证函数。

该程序执行以下精确检查：

1. 先核对原归档 CSV SHA256 `dc40ed773491817caf242ba6416e1bdf98ef2f1a2cd05e1956bdf5aec5801663`，原结果 JSON SHA256 `f891df1c4640c2f49a457c436bc043f6bc08b768ac92594050e7e08061495a40`，核对冻结提交 `52f84dbfbe8563cf5c9a491e67d5e320223e0a56` 及真实机器收据里的这两个哈希。
2. 读取全部 **576 行** 原始带模型来源，要求九个 world 各拥有全部 64 种有序六 bit、概率质量总和精确为 1。
3. 对每行重新验证四位训练与两位未来测试的原始拆分、预测器固定规则、独立测试 bit 不参与拟合、逐 bit Brier、每行训练及独立测试平均、未截断 log loss 的正无穷失败事件标志。
4. 九世界各自的加权训练 Brier、真正独立测试 Brier、无限 log loss 概率，与原始冻结结果 JSON 精确一致；**第二条完全独立的解析路径**按 K∼Binomial(4,p) 的五个 K 值重新求和核对。
5. 在内存中对概率质量、测试 bit 分割、单条独立测试分数制造三类错误，各自必须走预期的显式错误拒绝。CI 再复制恶意改写的源 CSV 至临时目录，验证完整来源 SHA256 在评分前就拒绝该输入。
6. 全部科研检查均使用显式异常和精确有理数，普通 Python、`python -O`、`python -OO` 的输出需要字节一致。

与原研究相同，每种真 p 下三模型共享同一组 64 个有序人工源，576 是带模型标签的完整来源行数，**没有 576 名独立真人**。这也没有引入新的论文、真正目标受试者或外部研究队伍。

## 实际 CI 运行

新独立科研任务 `frozen-third-independent-source` 设为依赖现有 `full-checkout-candidate` 矩阵任务。两种 Python 各有一项真实成功的原生验收 job，待两者完成后，第三个科研 job 才直接读取原固定数据和结果，进行新的独立检验；另外保留一项攻防回归 job，便于防止旧候选伪造成功再次出现。

**真实 GitHub Actions [44041940672](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/44041940672)，completed / success。** 触发提交 `5eb9674f5d0e1f19042f989ca2bb130b1a71e23d`。

实际四个 job 全部 success：

* `133898344542`，Python 3.11 完整仓库原生测试及隔离 v2。
* `133898344995`，Python 3.12 完整仓库原生测试及隔离 v2。
* `133898736345`，不导入原科研生成器的第三来源精确复算，三种优化模式，576 行、九 world、三项原数据故障拒绝、整体输入 SHA 篡改拒绝。
* `133898344976`，旧单入口完整误接受负向重现和隔离 v2 阻断回归。

第三 job 的真实日志标志：

```
R272_FROZEN_THIRD_SOURCE_576_ROWS_9_WORLDS_PASS
R272_THIRD_SOURCE_ALL_THREE_PYTHON_MODES_IDENTICAL
R272_FROZEN_THIRD_SOURCE_SHA256_NEGATIVE_REJECTED
```

第一项成功标志实际出现三次，对应正常、`-O`、`-OO`。两个 Python 版本的 v2 完整审计均保留 `R272_QUARANTINED_V2_REAL_CHECKOUT_3_MODES_PASS`。

## 科学等级、费用及正式准入

此次是**原科研所要求的三类方法在一个新增、只读、独立审计工作流中的真实可执行性验证**。原冻结协议要求的历史三 job 已有自己的科学验收证据；此新增运行**不是原生产 workflow 的替换或正式追溯验收**。GitHub main 正式工作流未修改。

冻结及归档状态：
* 原 R272 CLOSED_BOUNDED_E1 人工结题、R073 与 PESEN v0.1 保持不变。
* original239 12-002 P0 保留，正式 154 项待核队列减少 0。
* 没有新的真人 E2、历史 E3、额外外部科学独立复现。
* 使用现有公开仓库标准只读 GitHub Actions，无付费 API、额外订阅、私有 runner。实际账户结算账单未查询。

**剩余生产阻塞：** 当前 main 未启用保护规则；要使科研 CI 成为强制合并条件，需要明确的 owner 权限设置及冻结协议兼容的正式 workflow 变更。配置治理、Actions 固定 SHA、来自 PR 的 untrusted code 执行与运行器信任边界，以及可能触发自动写入和竞态的历史发布步骤，均需单独审议。不因本轮三科研 job success 而自动解除 P0。
