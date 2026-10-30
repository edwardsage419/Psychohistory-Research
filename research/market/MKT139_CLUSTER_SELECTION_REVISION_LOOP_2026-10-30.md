# MKT139 群组入样、迟到修订与Loop Habit Tracker机制
日期：2026-10-30 Asia/Singapore。目标键：(market,MKT139,none,cluster-selection-provisional-label-Loop-score-category-v26)。状态：COMPLETE_BOUNDED_ARTIFICIAL_E1。

## 人工精确实验
4个群组人数1/2/3/4、最终标签0/1/0/1、独立入样概率3/4、1/2、1/2、1/4。每组所有记录共享标签与入样事件。完整枚举16种入样结果，采用BigInt有理数运算。

| 指标 | 精确值 |
| --- | --- |
| 总体人数加权真值 | 3/5 = 60% |
| 非空入样时普通观察均值的条件期望 | 5189/12810 ≈ 40.51% |
| 群组入样概率正确时HT估计的无条件期望 | 3/5 = 60% |
| HT设计方差 | 13/25 = 0.52 |
| 完全零入样概率 | 3/64 = 4.6875% |
| 两个阳性群组均未入样概率 | 3/8 = 37.5% |

HT无偏依赖入样概率正确已知、固定最终标签、独立群组抽样。其高方差仍然存在。非空样本的普通均值与HT无条件期望不能混淆。不存在已校准的真人结论。

固定入样事件A/B/D可见、C未入样，其概率3/64。D在时点1标签尚未到达，时点2临时标签0，时点3修订为最终1。对未知标签枚举0/1得总体阳性率的确定性可行界：

| 时点 | 可行界 | 是否包含最终真值60% |
| --- | --- | --- |
| 1 | [20%,90%] | 是 |
| 2 | [20%,50%] | 否 |
| 3 | [60%,90%] | 是 |

时点2把错误临时标签视为已核实真值会使可行界错误排除真实结果。这是人工测量错误负例。区间没有统计置信水平含义。建议候选字段cluster_id、selection_probability_provenance、label_status、label_asof、revision_version、abstain_reason。

源码research/market/mkt139_cluster_selection_provisional_revision_exact_20261030.js在隔离V8实际执行16个世界、15项断言、6项非法输入拒绝PASS。原生Node CLI与Actions未运行。人工E1，新增真人预测E2=0、历史E3=0、外部独立团队=0。

## Loop Habit Tracker公开源码及新变化
官方仓库 https://github.com/iSoron/uhabits 。固定2026-10-22上游提交82c1ff287a8ac05321bfa95b61399fa8a2d1da5b：https://github.com/iSoron/uhabits/commit/82c1ff287a8ac05321bfa95b61399fa8a2d1da5b 。本次开发提交新增Habit分类字段、SQLite v26迁移、按分类展示、CSV导出Category列；开发分支提交不能视为正式商店版已发布。

固定Score.kt：https://github.com/iSoron/uhabits/blob/82c1ff287a8ac05321bfa95b61399fa8a2d1da5b/uhabits-core/src/commonMain/kotlin/org/isoron/uhabits/core/models/Score.kt ，Git blob 9b26f3486c2a51b2ed0188195af5d1e2e1a09084。原生代码计算 multiplier=0.5^(sqrt(frequency)/13)，score=previousScore*multiplier+checkmarkValue*(1-multiplier)。frequency为目标重复次数除以日程天数，分数平滑记录习惯强度；未验证其可预测人生长期结果。未运行Kotlin原生测试。

输入是用户打卡、频率、习惯分类；状态是本地历史、分数、提醒和CSV/SQLite导出。官方README称离线运行、无需账号或网络、数据保留在设备、GPLv3免费无广告且无内购。本轮未做网络流量或独立长期效果审计。反馈为趋势图与习惯分数，未发现公开可复算的长期人生效用或因果改善证据。费用为软件本身0，本轮未注册、购买或输入个人数据。产品机制证据=固定源码与官方文档；产品效果独立验证=OPEN。

下一MKT140：入样概率误设敏感性与标签版本冲突。零新增费用，GitHub账单/免费额度未独立核验。R073与PESEN v0.1冻结。
