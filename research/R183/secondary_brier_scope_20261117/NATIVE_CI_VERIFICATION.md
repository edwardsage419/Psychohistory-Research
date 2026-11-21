# R183 原生 CI 复算新增证据（历史收据保留）

日期：2026-11-17 UTC。此记录是在 R183 二次人工数学研究包形成后，**实际执行**原先标注为 NOT_RUN 的 Node 命令而取得的新工程证据。此前 `receipt.json` 是当时的准确历史状态，不在本轮追溯改写。

## 实际执行

- GitHub Actions：https://github.com/edwardsage419/Psychohistory-Research/actions/runs/44031127806
- Run ID: `44031127806`；job ID: `133863056327`
- CI 触发提交：`72e9f13d4d7f2be3d12ee42248ee6ca14246c60a`
- 真实状态：`completed`，`success`
- 环境：标准 `ubuntu-24.04` GitHub 托管运行器，Node 22、Python 3.11，只读 `contents: read`，无付费第三方依赖，无凭据持久化。
- 新工作流：`.github/workflows/r183-exact-brier-boundary-20261117.yml`

### 原生验证内容

1. 真正从 GitHub 检出的 R183 归档输入调用 `independent_brier.js`，验证数据固定 SHA256，并重新枚举 45 世界的 90 个完整计数 PMF，核对归档期望 Brier、数学矩公式与所有风险差方向。
2. 与前期生成的历史 `receipt.json` 的 45 世界、4125 设计枚举对、每个样本量最小/最大差值、网格外二项反例及 E2/E3 证据状态逐字段核对。这里的 4125 是设定样本的枚举规模，未重新逐行复核原 4125 行 CSV。
3. 直接调用 `python_crosscheck.py`，运行三个独立 `Fraction` 数值交叉测试并核对原始标准输出。
4. 在 CI 中制作恶意修改的 R183 JSON，确认完整输入 SHA256 不符时 `independent_brier.js` 实际失败并显示 `SOURCE_SHA256_MISMATCH`。另外 Node 内建两项内容篡改负控制也通过。

实际 GitHub 日志标记：
```
R183_45_WORLDS_NATIVE_EXACT_BRIER_PASS
R183_OFF_GRID_COUNTEREXAMPLE_NATIVE_PASS
PYTHON_FRACTION_SPOT_CHECK_PASS 3
R183_SUBSTITUTED_SOURCE_REJECTED
```

### 科研证据界限

**COMPLETE**：提交后的 Node 原生执行、Python 三项交叉检查、输入完整性故障拒绝、归档精确分数核对及 CI 收据实存。

**NOT_RUN**：新真人留出样本预测、历史 E3、独立外部科研团队复现、原始 CSV 4125 行逐行复扫。

此 CI **只**证明冻结人工世界上的追加数学风险分析程序可以在标准运行器复算。45 个世界的优势不推广到更小的真实概率：已验证 `n=4,p=1/100` 的严格反例。原 R183 正式 `CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_LOGISTIC`、R073 和 PESEN v0.1 冻结协议保持不变。

本次只新增工作流和追加证据，不改变原研究计算、原始模型或历史原收据。
