# R183 Python Fraction 优化模式加固及第二轮原生 CI

日期：2026-11-17 UTC。此前 `NATIVE_CI_VERIFICATION.md` 记录的初版运行 44031127806 保留为正确的历史证据。本文件仅补充**后续代码改进及真实新验证**。

## 变更

历史追加 Python 交叉验算程序 `python_crosscheck.py` 仍采用 4 处原生 `assert` 来判断 PMF 归一化、边际均值、解析差值和三个固定测试用例。使用 `python -O` 时会跳过这些校验。

已在同一辅助程序中改为 `require(...)` 显式拒绝，原有数值公式及三个测试向量完全不变，并新增样本量和合法概率范围检查。修复后的脚本 SHA256：
`c5d063d345ea9a30140cfa09c30ba2c92251aeba19a4675fba363a9f5fd6aee8`

原先生成的 `receipt.json` 中旧脚本 SHA256 对应**修复前的当时版本**，它是历史执行收据。本次不静默覆写；Git 历史与新增 CI run 证明变更顺序。

## 实际验证

- 真实 GitHub Actions：https://github.com/edwardsage419/Psychohistory-Research/actions/runs/44031429966
- Trigger SHA：`c696fdc7611c6aa3d25c327c796789d5ba07f57d`；job `133864058625`；`completed / success`。
- Node 22 精确 45 人工世界运算、归档数值与原输入 SHA256 检查全部通过。
- Python 3.11 正常模式及 `PYTHONOPTIMIZE=1` 模式，均实际运行 3 个固定有理数例子并通过。
- 两种模式下的无效参数负控制分别拒绝 `n=0`、`p=-1/100`、`p=101/100`。
- 子程序内两项模拟 PMF 与归档分数篡改控制均拒绝；替换整个归档输入的 SHA256 检查也拒绝。
- GitHub 日志包含两次 `PYTHON_FRACTION_SPOT_CHECK_PASS 3` 与两次 `R183_PYTHON_NEGATIVE_CONTROLS_PASS`，且有 `R183_45_WORLDS_NATIVE_EXACT_BRIER_PASS`、`R183_SUBSTITUTED_SOURCE_REJECTED`。

使用公有仓库标准免费 GitHub Linux 运行器，没有推送 `main`，没有更改任何冻结协议、原 45 世界的历史输入或旧科研评分。

## 科研边界

**COMPLETE**：第二次真实原生 CI 的 45 人工世界解析和 Python 双模式拒绝式验证。

**NOT_RUN**：新的真人个体样本外数据、外部科学独立复现、历史 E3 预测、原始 4125 行 CSV 独立扫描。

R183 原结题上限仍是有限人工 E1。研发状态补全不等于新科学样本或证据等级升级。