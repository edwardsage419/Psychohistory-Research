# 心理史学研究主控台 v4.5（2026-10-16）

继承 [v4.4](RESEARCH_CONTROL_v4.4_2026-10-16.md)，不覆盖历史 ZIP、R001–R064 归档或前四阶段记录。

## 实际完成事项

R065 Phase E 的事后冻结方案在对比新数值之前提交：`protocols/R065_PHASE_E_DAY89_BOUND_2026-10-16.md`，对应提交 `1f7f14c6a4e9abe4a03ea3dfa2ea5cbbb2b4eb4a`。

核验的外部处理数据仍为 Levy 等作者固定 CSV Git blob `01bf211468abe093618dfa5e5c39e883230c9c03`，295 原参加者、226 合格参加者、1,808 个关键试次。日 `89` 是第六次关键选择，当日 73/226（32.30%）为直接模仿，与既有 Phase B 相同。

作者公开七模型源码固定 Git blob `5e98133fa274ef2a112b24f6fdcd802d4f9d3eec`，在 `day=89` 提前清零各自历史状态，结合来源标准化三代币转移行与两动作设置，导出每个选择的等概率 `[0.5,0.5]`。这是源码数学后果，不是作者完整模型已被本地重拟合的证明。

## Phase E 源码条件的预测对照

| 评价指标 | 公开初始化规则导出的 uniform | 使用其他 225 位参与者数据的 Beta(4,4) 留人基线 |
|---|---:|---:|
| day89 平均 logloss | 0.69314718 | 0.63346543 |
| day89 平均 Brier | 0.25000000 | 0.22059212 |

`uniform - leave-person-out` 的平均 Log loss 差 `+0.05968175`，个人级固定预测的 20,000 次配对 Bootstrap 描述区间为 `[0.01513433,0.10422917]`。Brier 差 `+0.02940788`，Bootstrap 区间 `[0.00804727,0.05076849]`。

重要限制：此第六诊断日来自先前已观察到的源码问题，属于**事后目标选择**，且配对 Bootstrap 不含跨新样本重新拟合与完整发现流程不确定性；不能得出原作者发表结果错误、代码修改后的真实增益、潜在认知切换、长期社会动态机制或 PESEN 参数应修改的结论。

真实来源结论在连接器执行环境中计算，本地原始第三方 CSV 访问受阻，原始作者七模型拟合未执行。Phase E [研究报告](../research/R065/R065_PHASE_E_DAY89_AUDIT.md)、[JSON 汇总](../research/R065/R065_PHASE_E_DAY89_RESULTS.json)、[Python 可复算程序](../research/R065/r065_phase_e_day89.py)和[构造样本测试](../research/R065/test_r065_phase_e_day89.py)均已归档。**本地测试 8 项真实执行，0 失败**，且上架 GitHub 的代码与本地运行文件 Git blob 完全一致。GitHub Actions 中新增 Phase E 自动复算步骤，但成功日志目前**尚未核实**。

## 研究准入状态

`R065_PHASE_A_TO_E_BOUNDED_AUDITS=ARCHIVED`

`R065_SOURCE_DAY89_PREDICTION_BOUND=SUPPORTED_CONDITIONALLY`

`R065_ALL_SEVEN_AUTHOR_MODELS_REAL_FIT_REPLAY=NOT_EXECUTED`

`GITHUB_ACTIONS_FULL_SOURCE_REPLAY=NOT_VERIFIED`

`R065_FULL_RESEARCH_GATE=OPEN`

`PESEN_v0.1=FROZEN`

下一步按最小范围建立作者原始模型对两种状态重置时间轴的**真实原始实验文件预测敏感性检验**，包括相同参数、种子、训练测试分组、同等优化预算与完整实验结果差异。需要原作者完整原始单人试次文件和 CI 实际作业记录，否则不得宣称该比较闭合。
