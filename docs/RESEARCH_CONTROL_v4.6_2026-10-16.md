# 心理史学研究主控台 v4.6（2026-10-16）

本版继承 [v4.5](RESEARCH_CONTROL_v4.5_2026-10-16.md)，保留以前所有研究档案和预先确定的推断边界。新增 R065 Phase F 的**独立汇总算术复核证书**。

## 阶段结果

R065 Phase E 的既有来源结论为作者固定处理数据中：第 89 天 **226 名合格参与者、73 个直接模仿结果**。本轮没有再获取作者原始参与者记录，而是考察在这两个汇总计数和固定 Beta(4,4) 留整人方案之下，是否存在仅依赖计数的数值复现。

纯 Python 标准库的闭式计算得到：

| 指标 | 精确统计量 |
|---|---:|
| 相同二选项均匀预测 Log loss | 0.6931471805599453 |
| Beta(4,4) 留整人基线 Log loss | 0.6334654316626859 |
| Uniform − 留人对数损失 | +0.05968174889725945 |
| Uniform − 留人 Brier | +0.029407878875705663 |

固定预测条件下，bootstrap 样本中模仿次数严格服从 `Binomial(226,73/226)`。精确枚举其 227 个支持点，得到 Uniform − 留人 Log loss 的条件性 95% 百分位区间 `[0.015134327049981177,0.10422917074453769]`；Brier 的条件区间 `[0.008047271428541131,0.0507684863228702]`。这些区间在 `1e-12` 的数学数值公差内重建了 Phase E 历史 20,000 次 Bootstrap 的端点。

[完整审计](../research/R065/R065_PHASE_F_AGGREGATE_CERTIFICATE_AUDIT.md)、[确定性程序](../research/R065/r065_phase_f_aggregate_certificate.py)、[9 项本地真实执行通过的测试](../research/R065/test_r065_phase_f_aggregate_certificate.py)及[结果 JSON](../research/R065/R065_PHASE_F_AGGREGATE_RESULTS.json)已提交并重新读取核验。程序、测试与 JSON 三项文件与本地实际执行文件的 Git blob **完全一致**。

## 不能越过的边界

* 证明的是**给定汇总计数时的统计计算正确性**。不重新证明原始作者 CSV 确有 `73/226`，也不证明原作者七个认知模型的真实拟合。
* 由于第 89 天的选择及预测比较是先前研究结果之后才决定，条件性区间不能充当独立前瞻的效应检验。模型心理机制仍未被识别。
* R065 的 GitHub Actions 工作流新增 **独立离线 `aggregate-certificate` 作业**；可以在源数据下载失败时单独验证汇总算术，但本轮尚未获得 GitHub Actions 实际作业成功记录。
* 除 R065 六个限定研究阶段之外，旧研究档案状态不变。

状态：`R065_PHASE_F_AGGREGATE_ARITHMETIC=LOCAL_PASS`、`GITHUB_ACTIONS_EXECUTION=UNVERIFIED`、`RAW_SOURCE_LOCAL_REPLAY=OPEN`、`R065_FULL_RESEARCH_GATE=OPEN`、`PESEN_v0.1=FROZEN`。

下个技术关口仍是独立取得作者固定原始试次，在同样训练测试与优化预算下重跑七模型原有重置时间轴和对齐实验区块时间轴，避免从事后描述直接创建心理史学机制参数。
