# R231 S27 有限样本 tetrad 零值的精确误判边界

日期：2026年10月28日，Asia/Singapore。证据 E1 人工。先冻结协议 commit `4f8a999530f8c8f6227c461b0c30f42d02574815`，后执行枚举。原 R231 8 个世界、512 个外生来源、原正式验收状态全部保留。原 CSV blob `f56003f4b18f1dfcbdcd00aabc22fa0815205b64`。

## 研究问题与预设

四指标的三项 tetrad 人口协方差多项式可以在正确单因子模型下为零。有限样本以零值直接决定接受或拒绝会怎样失效？冻结 n=2、n=3 有放回抽样，八世界每世界各 64² 和 64³ 个有序序列，总计 2,129,920 个。使用分母 n 的样本协方差 `C`，以整数矩 `A=n² C` 计算三项 tetrad。分类 `ZERO` 表示三项全部精确为零，`NONZERO` 表示至少一项非零。它是有限样本描述性代数分类，未指定显著性水平或阈值，不能视为正规的CFA统计检验。

## 精确结果

| 原世界 | 人口 tetrad 全零 | n=2 样本 NONZERO /4096 | n=3 样本 NONZERO /262144 |
|---|---|---:|---:|
| ONE_FACTOR_VALID | 是 | 0 | 99648 |
| ONE_FACTOR_SIGNED | 是 | 0 | 99648 |
| TWO_FACTOR_BLOCK | 否 | 0 | 107016 |
| CORRELATED_RESIDUAL_METHOD | 否 | 0 | 119304 |
| SECOND_FACTOR_SEMANTIC_ALIAS | 否 | 0 | 119304 |
| TETRAD_FALSE_REASSURANCE | 是 | 0 | 130176 |
| CROSS_LOADING_CANCEL | 否 | 0 | 121296 |
| ONE_FACTOR_UNEQUAL_LOAD | 是 | 0 | 122592 |

**反例一：** 两个观察值的中心化样本协方差秩至多1，故所有四指标 tetrad 必然为零。即使 TWO_FACTOR_BLOCK 人口 tetrad 非零，4096/4096 个两次抽样仍显示 ZERO。把零值作为支持单因子的直接证据，在此样本量完全失效。

**反例二：** ONE_FACTOR_VALID 是原冻结真实单因子世界，n=3 的262144个有序样本中，99648个（约38.013%）产生至少一个非零样本 tetrad。将任何非零样本值直接视为真实总体模型错误，会在本人工设计下产生大量错误指示。

**反例三：** TETRAD_FALSE_REASSURANCE 的原指定 T 条件残差存在六对共同 U 关联，人口 tetrad 仍全零；n=3 的非零比例约49.658%。有限样本 tetrad 的零与非零均无法恢复原始 T 的心理构念含义。

共享方法残差世界与第二因子语义别名世界，在 n=2 与 n=3 的全部计数精确一致，符合原 R231 的源点级可观察等价。ONE_FACTOR_SIGNED 与 ONE_FACTOR_VALID 的全部计数也一致，符合符号反转不改变零判别。

## 算法、核验和证据边界

R 轨直接遍历每个世界64个原来源的有序二元与三元组合，采用观测差分恒等式构造整数协方差。B 轨只读取可见四元组，按不同观测值聚合频数，枚举无序多重集并使用排列重数及二阶矩重建统计量。B 轨覆盖16个世界样本量组合、48项字段精确比较，全部一致，失败0。B 轨处理了140412个加权可观察多重集。故意篡改一项 ZERO 计数后成功检出 `AUDIT_MISMATCH`。

复算入口：`research/validation/r231_s27_finite_sample_tetrad_exact_20261028.js` 和 `research/evidence_audit/b_r231_s27_grouped_multiset_audit_20261028.js`，要求 Node.js 和原始 CSV 在原仓库相对路径。正式机器收据：`research/validation/R231_S27_FINITE_SAMPLE_TETRAD_RECEIPT_2026-10-28.json`。本轮在连接器 JavaScript 执行环境运行两套算法，完整 Node.js CLI 和 GitHub Actions 本轮未运行，CI 标为 NOT_RUN。

研究不包含真人问卷、实际CFA拟合、标准误、样本外预测或心理测量等值性实证。所有概率只属于原冻结八个人工世界。新增 E2=0、E3=0、外部独立研究团队复现=0。R073 模型评分及 PESEN v0.1 继续冻结。原 R231 正式有限 E1 验收不被此次增量改写。
