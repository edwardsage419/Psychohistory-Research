# C016 Bayesian N-of-1 的设计秩、先验敏感性及不可识别性

track: theory
subflow: C
run_date: 2026-11-11 (Asia/Singapore)
observed_head: 0cdea3ac60168dab58bdd694177f4c8e49871e60
target_key: (theory-C,SchmidYang2022,doi:10.1162/99608f92.3f1772ce,prior_identification_under_time_collinearity)
status: PARTIAL
source_links:
  - https://doi.org/10.1162/99608f92.3f1772ce
  - https://hdsr.mitpress.mit.edu/pub/b6efwlql/release/1
source_access: 开放正式发表HTML，直接核读第1节、第2.1至2.4节、第3.1至3.3节；后续第3.4至8节未系统核读。

## 原著范围与核心命题
Christopher Schmid and Jiabei Yang (2022), Bayesian Models for N-of-1 Trials, Harvard Data Science Review, Special Issue 3, DOI如上。原著式(2.4)给出处理效应与线性时间趋势并存的观测模型；式(2.5)至(2.7)区分误差自相关与滞后结局回归，后者的处理系数是条件于上一期结局的比较。第2.4节明确指出残留效应估计需要交替期，交替过少时难以识别。第3.1至3.3节指出后验依赖似然与先验，数据少或似然平坦时先验影响显著，须开展先验敏感性分析。作者在引言明确限定短效、稳定状态、可反复交叉等适用条件。

## 本轮独立推导：先验可以给出数值后验，不能自动修复秩亏
设Y_t=mu+tau A_t+lambda S_t+epsilon_t，epsilon_t独立同方差正态；S_t是已观测时间阶段指示变量。若每期A_t=S_t，则设计矩阵两列完全相同，似然仅依赖theta=tau+lambda。对于任意常数c，(tau+c,lambda-c)给出完全相同的观测分布。重复相同安排、增加观测数量均不改变这个不可识别性。

令tau与lambda的先验独立、均值0、方差分别为v_tau与v_lambda的正态分布；当theta由大量观测近乎精确获知时，tau条件于theta的后验均值为[v_tau/(v_tau+v_lambda)]theta，方差为v_tau*v_lambda/(v_tau+v_lambda)。例如theta=2，v_tau=v_lambda=1，后验均值tau=1，条件方差0.5；若v_tau=9、v_lambda=1，均值tau=1.8，条件方差0.9。相同数据因先验分配不同而产生不同的处理效应推断。以上为解析构造性反例，未使用个人数据、真人实验或随机试验。

## 可证伪设计检查、竞争解释及边界
可观测量：处理序列、测量时间、阶段指示、结果、缺失指示、前期处理和干扰边界。设计可检验量：rank([1,A,S])及其最小奇异值；当A=S时rank最多2而参数3个。若阶段趋势预先指定为连续线性t，单次断点A=1(t>=t0)在多于两个不同时间点时通常不与t严格共线，不能将此构造性反例推广为所有单断点均秩亏；仍有未观测同步冲击、模型错误与弱识别问题。

竞争解释：真实处理效应、共同阶段冲击、测量反应性、时间变化偏好、残留效应。事先随机安排多个安全可逆的交替周期可以改善某些设计秩问题，但随机化也不能自动解决残留效应、依从性、结果测量偏差或不可逆干预。未来价值权重只能由使用者决定。

## 与既有C研究去重
C006已经覆盖季节混淆和单次断点构造反例；C015覆盖Chen与Chen(2014)统计报告内部区间一致性。本轮独立增量为直接核读Schmid与Yang的贝叶斯模型章节，并给出在严格秩亏下两套先验导致不同tau后验的闭式反例。不得称为独立真实行为验证。

## 状态
原著指定章节阅读 COMPLETE；解析推导 COMPLETE（代数手工核对）；原著全文阅读 PARTIAL；程序测试 NOT_RUN；真人验证 NOT_RUN；D 2026-W46 D004既有文件 PARTIAL；CI NOT_RUN；billing_checked: 未调用计费API或主动触发CI，账户费用NOT_VERIFIED。
next_action: 后续审读第4至8节，核查跨个体层级先验迁移的可交换性假设及信息性退出；不提前构建个人决策产品。
