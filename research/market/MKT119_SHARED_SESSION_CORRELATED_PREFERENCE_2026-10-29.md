# MKT119 同一询问会话内的相关噪声与虚假高置信度

日期：2026-10-29 UTC。track=market；subflow=product。状态：COMPLETE_BOUNDED_SYNTHETIC_MARKET_E1。target_key=(market,MKT119,none,shared-session-correlation-calibration)。observed_head=acf61773c4f172d9c586084e842b33998268b674。本轮为人工模型，不含个人数据或真人测量。

## 英文公开来源及实际读取范围

1. BoTorch官方PairwiseGP技术说明，https://archive.botorch.org/api/_modules/botorch/models/pairwise_gp.html 。阅读PairwiseGP probit likelihood、成对比较输入及Laplace近似的源码说明；没有运行BoTorch或核验其内部相关噪声处理。
2. Lancaster and Quade, 1983, Random effects in paired-comparison experiments using the Bradley-Terry model, https://pubmed.ncbi.nlm.nih.gov/6871353/ 。摘要明确指出同一评价者的判断可能相关，可用随机效应表达。该论文没有提供本轮人工参数。
3. Wu, Niezink and Junker, 2022, A Diagnostic Framework for the Bradley–Terry Model, https://doi.org/10.1111/rssa.12959 。阅读摘要，支持对评价者和比较对象分别诊断；未将其作为人工数值的验证。
4. Aiyer and Shao, 2026-10-07, How Many Repeated Pairwise Comparisons Are Needed for Ranking under Heterogeneity?, https://arxiv.org/abs/2610.10795 。阅读摘要，作为异质性与重复比较的近期方法背景，未运行其算法。

## 输入、状态、模型与反馈

人工假设两种真实偏好H=0/1，先验各1/2；每个询问会话存在共同潜在质量Z。好会话概率3/4，每次回答正确率9/10；坏会话概率1/4，每次正确率1/10。给定H与Z后，同会话回答条件独立。跨会话的Z独立。单次边际正确率为7/10。固定四次询问、95%置信阈值、三种会话分组：4；2+2；1+1+1+1。错误的朴素推断将所有回答视为独立且准确率7/10。正确推断对每个会话的Z积分。使用Python标准库Fraction精确穷举16种回答序列和两种真偏好，计算后验、贝叶斯误判、拒答覆盖及实际条件误差。

| 四次询问的会话分组 | 正确模型贝叶斯误判 | 朴素模型声称误判 | 朴素95%决策覆盖 | 朴素作出决策时实际错误率 |
| :-- | --: | --: | --: | --: |
| 同一会话4次 | 33/125 = 26.4% | 27/125 = 21.6% | 3281/5000 = 65.62% | 1641/6562 ≈ 25.01% |
| 两个会话各2次 | 33/125 = 26.4% | 27/125 = 21.6% | 2081/5000 = 41.62% | 441/4162 ≈ 10.60% |
| 四个独立会话各1次 | 27/125 = 21.6% | 27/125 = 21.6% | 1241/5000 = 24.82% | 81/2482 ≈ 3.26% |

当四次回答全部为H=1时，朴素模型后验为2401/2482≈96.74%。四次共享同一会话质量时，正确后验为4921/6562≈74.99%；两个会话各两次时为3721/4162≈89.40%；四个独立会话时为2401/2482≈96.74%。共享会话模型的真实95%置信决策覆盖为0。相同四次回答的表面数量并不等于四个独立信息来源。

## 解释、权限、费用与局限

真实输入若未来存在，会涉及选择时间、情境、会话标识、比较对象、回答、拒答及撤销记录，可能揭示敏感偏好。本轮未采集。候选反馈：展示会话分组、重复相关风险、校准后验与拒答，允许用户撤回回答、拒绝自动建议，重要决策需人工确认。自我修正只作为未来候选，必须重新审计会话依赖及漂移；候选控制均UNADOPTED。没有固定人生效用权重。

费用：仅本地Python标准库与公开免费来源，新增收费操作0；实际GitHub账户账单和免费额度UNKNOWN。BoTorch为开源方法参考，未购买产品或调用收费API。

证据边界：MARKET E1，人工条件概率的精确演算。参数、会话分组、真实偏好与噪声机制均由本轮设定。267项显式程序检查失败0，普通Python及python -O输出一致，语法编译通过。脚本 research/market/mkt119_correlated_session_preference_20261029.py 本地SHA256=43f8ce8903f76e51a96f80f7b321167b0201f1cc25af0aff032c37dcfc72e3cb。真人长期稳定性、真实回答相关系数、BoTorch完整模型、外部独立复现、因果改善均NOT_RUN。不同会话并不必然独立，真实应用需要验证。

下一项MKT120：考虑跨会话持续相关、疲劳和真实偏好漂移的竞争解释；先冻结人工模型，再评估停止询问与拒答策略。
