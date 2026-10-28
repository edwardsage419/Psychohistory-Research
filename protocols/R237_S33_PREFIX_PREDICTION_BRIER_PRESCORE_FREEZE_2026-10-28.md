# R237 S33：冻结三词主题模型的前缀预测及Brier风险事前协议

日期：2026-10-28。证据等级仅E1人工精确概率。研究对象为已正式验收的R237九个人工世界。原目录10-011 Topic Models。不得修改R237原始源、R073模型或评分规则、PESEN v0.1。

## 固定输入
只读取 `research/R237/R237_EXACT_RESULTS.json` 中九世界完整27格 `exact_observable_three_position_word_joint`，对应Git blob SHA1 `01af9a479bd6aca2f2555b5e5127039f8bb89728`。原始完整来源CSV SHA256 `8fb107920ffa30de566ed8a67937f57255f02cbc6819323d752a3e6dd8b4f442`。不拟合模型，不选择新世界，不调整任何α、β。所有数值使用有理数精确计算。

## 事前冻结任务及模型
每个文档由三个有序符号w1,w2,w3组成，预测目标为第三位置的三分类one-hot向量。观察前两词的前缀x=(w1,w2)，可见9个前缀，每个前缀均有正概率。三个固定预测器：
1. `ORACLE_PREFIX`：q(k|x)=P(w3=k,x)/P(x)，从同一世界的完整真实联合分布计算，是人工Bayes oracle。
2. `UNIGRAM`：q(k)=P(w3=k)，完全忽略前缀。
3. `UNIFORM`：q(k)=1/3，忽略世界和前缀。

每个预测器的三分类Brier风险为 `R(q)=Σ_{x,k}P(x,k)Σ_{j=0}^2(q(j|x)-1[j=k])²`。冻结两组超额风险：`R(UNIGRAM)-R(ORACLE_PREFIX)`及`R(UNIFORM)-R(ORACLE_PREFIX)`，均应非负。严格对照公式 `R(q)-R(oracle)=Σ_x P(x)Σ_j(q(j|x)-oracle(j|x))²`，作为B轨独立的二阶矩算法。对全部九世界逐格计算风险及该公式，不使用浮点容差。

## 冻结负例与边界
`BASE_TOPICS` 与 `LABEL_SWAP_ALIAS` 的三个风险及所有前缀条件预测应完全一致。`DUPLICATE_TOPICS_A` 与 `DUPLICATE_TOPICS_B` 同样完全一致。对 `DUPLICATE_TOPICS_A/B` 和 `UNIFORM_WORDS`，ORACLE_PREFIX与UNIGRAM的超额风险应严格为0。`UNIFORM_WORDS` 三预测器全部同风险。对BASE_TOPICS，ORACLE_PREFIX应严格优于UNIGRAM。所有前缀概率正、每个预测分布归一、全部风险非负。故意篡改一个风险分数应被B轨检出。

## 科学验收限制
这是对已知人工概率分布的oracle决策风险积分，不能作为真实语料训练、样本外独立预测、概率校准的经验估计或历史E3证据。B轨属于同一项目内部独立公式程序性复核。E2、E3均新增0。成果需新增独立路径中的源码、机器收据、科学报告及B轨审计。任何程序性失败应明确登记，不能改写本协议追求通过。GitHub Actions仅在确认不会产生费用时执行，其他情况记录NOT_RUN。