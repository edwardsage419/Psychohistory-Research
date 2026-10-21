# R191 混合效应模型：24个已知方差随机截距人工世界

2026-10-21。原目录P1/08-015 Mixed Effects Models。科研级别 **CLOSED_BOUNDED_E1_ARTIFICIAL_EXACT_MIXED_EFFECTS**。

[事前冻结协议](../../protocols/R191_MIXED_EFFECTS_24_WORLDS_1440_PATHS_PRESCORE_FREEZE_2026-10-21.md)固定隐藏双点群组截距U=±τ（τ=0/1/2/1）、非高斯三点误差−2σ/0/+2σ（概率1/4、1/2、1/4，σ=1/2/1）以及重复测量次数n=1/2/3/4，共**24个人工世界、1440条带原始潜在标签及真生成概率的完整训练路径、1136种独特可见后验配置**。逐训练向量以独立逐观察乘积与观察值直方图频数幂两条Fraction计算真实Bayes后验；以群组新独立事件测试真实源概率评价GLOBAL、RAW_GROUP_MEAN、LINEAR_BLUP、EXACT_DISCRETE_POSTERIOR四种预测，并通过不枚举训练路径的独立解析方差公式逐世界Fraction相等。

**预冻结数学边界和实证风险**：τ=σ=1/2时，n1下真正的离散Bayes后验精确`E(U|Y)=Y/3`，与线性BLUP完全一样，二者新独立同群MSE均2/3；n2时线性BLUP独立未来MSE5/8=0.625，而真实离散Bayes后验49/80=0.6125，改善1/80。新的完全独立群组正确零均值预测风险3/4=0.75，若错误复用旧群组n2的BLUP则升至7/8=0.875。完全无随机截距τ0时使用原群均值拟合纯噪声会在同群新事件预测额外增加v/n。未从真实社会数据估计方差组件，不等于高斯LMM或一般REML的实证复现。

首次CI[39578606061](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39578606061) 30测29过，剩余项不正确地要求n1也严格改善，故失败并保留；[独立测试边界更正档案](../../protocols/R191_N1_BAYES_BLUP_TEST_ASSERTION_ERRATUM_2026-10-21.md)先归档数学证明，完整参数不变。中间[39578807306](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39578807306)双版本30测都成功，但因ZIP增至7文件而验收断言仍为6失败；最终修正档案计数。**正式[GitHub Actions39578838588](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39578838588)三个job全success**，Python3.11/3.12各30单测合计60次、第三job完整1440训练来源及1136 profile科研验收并归档main。[全部数据结果提交a6db677](https://github.com/edwardsage419/Psychohistory-Research/commit/a6db6777c81ae09145af78a2c5981abb6c7dc0d0)。

[正式科学报告](R191_SCIENTIFIC_REPORT_2026-10-21.md)、[24世界完整结果JSON](R191_EXACT_RESULTS.json)、[1440条原始潜在路径CSV](R191_ALL_1440_LATENT_TRAINING_PATHS.csv)、[1136完整后验配置](R191_ALL_OBSERVABLE_POSTERIOR_PROFILES.json)、[科研机器验收](R191_FINAL_MACHINE_ACCEPTANCE.json)、[源码及30单测](r191_exact_finite_mixed_effects.py)、[含事前冻结和纠错档案的七文件ZIP](R191_Exact_24_Mixed_Effect_Worlds.zip)永久归档。原始文献：[Laird/Ware1982](https://doi.org/10.2307/2529876)、[Robinson1991](https://doi.org/10.1214/ss/1177011926)。

科研仅限E1人工已知方差非高斯随机截距，新增真人E2=0、真实历史预测E3=0；R073与PESEN v0.1冻结。下一 **R192 P2/08-016 Latent Class Models**，仍坚持先全部R，后分类，最后熔炼。