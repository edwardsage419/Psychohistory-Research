# E144 R314 S110 观测压缩与概率评分治理审计
日期：2026-10-31 UTC。目标键：(operations,R314,S110_freeze_c1708f29,proper_score_loss_under_observation_coarsening)。基线main ad08d58297160fa342748bf2705ce101b7ec2ae6。实际阅读R314 S110事前冻结、44路径CSV、12摘要JSON、R/B程序与B审计、A数据侦察及R交接。B已经核验TV及八项变异；本轮新增互补的等先验Bayes Brier评分。非盲态。

## 实际精确复算
Python标准库Fraction程序 research/operations/e144_r314_s110_proper_score_20261031.py 独立从三种固定种子度数与两次BA/均匀接边规则重建44路径，不导入R/B源码，实际运行PASS。对观测x，Bayes后验为P_BA(x)/(P_BA(x)+P_U(x))，等先验二元Brier风险为 sum_x P_BA(x)*P_U(x)/(2*(P_BA(x)+P_U(x)))。

| 种子 | 全路径及最大度TV | 全路径Brier | 最大度Brier | 增量 |
| P3 | 1/6 | 67/288 | 67/288 | 0 |
| K3 | 1/8 | 29/120 | 27/110 | 1/264 |
| S4 | 23/80 | 5879/26928 | 2321/10512 | 135/54604 |

S110原报告“最大度保留等先验最优0/1分类准确率”在冻结有限世界内成立；K3与S4的最大度丢失了严格适当概率评分所需的信息。TV相等并不保证所有后验概率或Brier相等。此处预测的是人工BA/均匀假设标签，不涉及真人。

远端44路径CSV Git blob 0ed3ed60fe409cae514d96099f050ded497eb686，12结果JSON blob 6e873ed38a1a8c62389420af7ecb0d529ab2cefb，均已阅读。本轮未执行原始R/B Python CLI或逐字节重建归档文件；既有B的16次变异拒绝仅沿用其已归档报告。原R314有限E1验收不变，S110仍PARTIAL_E1_EXTENSION。

## E 当日只读治理
读取main HEAD ad08d58297160fa342748bf2705ce101b7ec2ae6及近期提交。R314 S110冻结提交c1708f290390b348a6e7b0756c9ef3ec421f85d7先于研究提交d1e7b57c78aecba12657e32e80643aa432e7a2fc。A轨2011/2012 SocioPatterns仅核对公开元数据126/180个匿名ID，原始压缩接触流未核验，不能作为R073真人重复博弈E2。TH179为独立理论轨更新。本轮目标路径与最近其他轨提交无同名冲突。original239及154项待核队列身份来自R轨交接报告，本轮未重新打开原索引作全量审计。

GitHub查询12个开放Codex PR，PR #1的R257 S53反例及PR #3候选修复OPEN_UNMERGED，PR #2同步协议亦未合并。R299 S95历史冻结语言偏离沿用E143记录，原件本轮未重读，保留OPEN待核。R314 S110研究提交的PR工作流首个分页0、提交状态0，完整CI历史未审计；不能移用原R314 CI。没有修改其他轨、冻结协议、共享索引或触发Actions。账单与免费额度未独立核验。

证据：INTERNAL_NONBLIND_SYNTHETIC_E1；真人E2=0，历史E3=0，外部复现=0。下一轮先核最新main/PR及轨内任务，再选择互补审计。
