# C013 补充：稳定个体差异导致虚假交叉滞后的解析构造反例

track: theory / C
run_date: 2026-11-07 (Asia/Singapore)
observed_main_head_before_write: 7d6a70ffae1da48058e0111faf7de40f72ee7809
target_key: (theory-C,Hamaker2015,original-published,analytic-stable-trait-spurious-cross-lag)
status: CONSTRUCTIVE_MATHEMATICAL_COUNTEREXAMPLE_ONLY; NO_HUMAN_DATA; NO_CAUSAL_ESTIMATION

## 原著定位与增量性质

原著：Hamaker, Kuiper & Grasman (2015), A Critique of the Cross-Lagged Panel Model, Psychological Methods 20(1):102–116, DOI https://doi.org/10.1037/a0038889 。本次基于已经归档的 C013 原著 p102–106 的 CLPM 与 RI-CLPM 模型定义，补充一个独立手工推导；本次没有新增阅读原著页码。原始C013：research/decision_methods/C013_HAMAKER_2015_CLPM_RICLPM_WITHIN_PERSON_IDENTIFICATION_2026-11-07.md 。

## 构造性数据生成机制

对每个人 i、时期 t，令 X_it=A_i+e_it，Y_it=B_i+f_it。稳定随机截距 (A_i,B_i) 均值为零，方差分别 a,b，协方差 c；独立的白噪声 e_it、f_it 均值零、方差 u,v，彼此及跨期与随机截距均独立。取 a,b,u,v>0，|c|<sqrt(ab)。于是两变量的个体内跨期交叉效应均为零，甚至所有个体内跨期协方差均为零。两变量的稳定个体间相关 c 可非零。

令 CLPM 的总体线性回归为 Y_it = beta_X X_i,t-1 + beta_Y Y_i,t-1 + residual（均值零）。上一期预测量的总体协方差矩阵为 [[a+u,c],[c,b+v]]，与 Y_it 的协方差向量为 [c,b]。正规方程直接给出：

D=(a+u)(b+v)-c^2>0
beta_X = (c(b+v)-bc)/D = c v / D
beta_Y = ((a+u)b-c^2)/D

所以只要 c≠0 且 v>0，CLPM 总体跨滞后系数 beta_X 就非零，尽管真实的个体内 X 到下一期 Y 的效应严格为零。其符号由 c 决定。该伪关联来自稳定截距相关与上一期 Y 的有噪测量所造成的剩余预测信息，不能解释为干预因果效应。

具体参数：a=b=u=v=1，c=1/2。D=15/4，beta_X=2/15，beta_Y=7/15。若 c=0 或 v=0，beta_X=0。后者为边界反例，说明有稳定相关并不足以单独保证非零交叉滞后；上一期结果变量的噪声方差也是条件之一。

## 可证伪与限制

可观测量：同一对象至少三期 X/Y 重复测量、时间戳、测量误差代理；不可直接观测：A/B 与真正个体内状态。合成检验可用已知 a,b,c,u,v 的模拟样本，预先要求样本扩大时 CLPM beta_X 收敛至 c v / D，分离稳定截距后的跨期状态回归收敛至零。模拟尚未执行。这里的白噪声是构造中的真实状态波动，额外的量表测量误差没有单独加入。模型完全不含时间变化混杂、趋势、反馈或干预；因此不能说明任何实际面板数据的 CLPM 一定有偏，也不能证明 RI-CLPM 在真实数据中无偏。

数学类型：解析构造性反例；真实行为实验 NOT_RUN；真实数据复算 NOT_RUN；历史预测 NOT_RUN；CI NOT_RUN。没有个人数据、模型熔炼或R轨改动。R073、PESEN v0.1及证据等级不变。

C 当日完成：2026-11-07，原始 C013 已合格，本记录是补强，未另设 C 编号。D 本周完成：2026-11-02，D003。新增收费服务：0；账单状态 NOT_VERIFIED。
