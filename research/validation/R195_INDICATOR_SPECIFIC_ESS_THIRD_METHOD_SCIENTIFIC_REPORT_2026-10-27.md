# R195第三方法科学报告：不同状态事件的有限N64有效样本量

日期：2026-10-27。新增研究状态：PASS_BOUNDED_INTERNAL_E1_POSTSCORE_ADDENDUM。先于计算冻结 `protocols/R195_INDICATOR_SPECIFIC_ESS_N64_THIRD_METHOD_FREEZE_2026-10-27.md`。原R195正式有界E1验收不变。

读取原R195的8套固定三态Metropolis–Hastings核，目标UNIFORM、CENTER、BIMODAL、SKEW，q=1/8或1/4，N=64、真平稳初始状态。原研究只报告事件f2=1{X=2}的有限样本ESS。本次增加f0=1{X=0}、f1=1{X=1}，共16个新增指标核组合，并独立复算原f2八组。主算法逐Fraction通过63阶自协方差直接计算连续64个状态的样本均值方差和ESS。全部8个T行归一化、πT=π、原f2精确结果与归档一致。精确机器收据保存全部分数，表内仅列便于阅读的十进制近似。

| 目标 | q | ESS f0 | ESS f1 | ESS f2（原归档复核） |
| --- | ---: | ---: | ---: | ---: |
| UNIFORM | 1/8 | 5.825402 | 15.258278 | 5.825402 |
| UNIFORM | 1/4 | 11.891613 | 38.722689 | 11.891613 |
| CENTER | 1/8 | 5.551709 | 7.155279 | 5.551709 |
| CENTER | 1/4 | 11.321867 | 15.258278 | 11.321867 |
| BIMODAL | 1/8 | 1.937048 | 10.983051 | 1.937048 |
| BIMODAL | 1/4 | 2.975396 | 25.474201 | 2.975396 |
| SKEW | 1/8 | 4.713688 | 9.499767 | 4.713688 |
| SKEW | 1/4 | 9.275819 | 21.167735 | 9.275819 |

原R195 f2指标在BIMODAL q=1/8下ESS约1.937。新结果展示同一核的不同指标可以有不同的有限样本ESS；UNIFORM对称目标的f0和f2 ESS精确相同。单一状态事件的ESS不能代表所有状态函数的估计精度，更不能单凭该ESS证明任何单条模拟轨迹已经收敛。

主脚本：`research/validation/r195_indicator_specific_ess_20261027.js`，精确机器收据：`research/validation/R195_INDICATOR_SPECIFIC_ESS_24_EXACT_RECEIPT_2026-10-27.json`。来源库 `research/R195/R195_ALL_8_EXACT_MCMC_KERNELS_AND_ESS.json`，原Git blob `17a3bff15e46b96091b292958d07b94da5ac8f31`。独立B审计另行归档。结果仅限人工三态MH核和指定指标，新增E2真人预测0、E3历史预测0、外部独立团队复现0。没有新增收费服务、没有启动GitHub Actions。