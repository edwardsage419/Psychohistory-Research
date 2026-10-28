# R237 S33：主题模型前缀预测的精确三分类Brier风险

日期2026-10-28。证据E1，仅限已知概率的九个有限人工LDA世界。正式R237既有验收保持不变。原239目录10-011 Topic Models。

## 冻结及数据身份
研究协议事先独立提交 [58bd39d7](https://github.com/edwardsage419/Psychohistory-Research/commit/58bd39d7c0b7b7b9bb261fdca364ab797edbb80d)，在计算本轮风险前冻结九世界、三种预测器、评分函数、对照及负例。输入为 [R237已验收的完整27格联合概率](../R237/R237_EXACT_RESULTS.json)，Git blob `01af9a479bd6aca2f2555b5e5127039f8bb89728`；原人工来源CSV SHA256 `8fb107920ffa30de566ed8a67937f57255f02cbc6819323d752a3e6dd8b4f442`。没有修改α、β、主题标签或旧R237文件。

三分类目标是第三词w3，观察前两词w1,w2。比较已知联合分布条件预测ORACLE_PREFIX、忽略前缀的UNIGRAM和均匀UNIFORM。多类Brier定义为三类one-hot平方误差之和，不作除以3的额外缩放。

## 九世界精确结果

| 冻结人工世界 | 前缀oracle风险 | 单词边际风险 | 均匀风险 | 单词边际相对oracle的超额风险 |
|---|---:|---:|---:|---:|
| BASE_TOPICS | 12599/18954 | 2/3 | 2/3 | 37/18954 |
| LABEL_SWAP_ALIAS | 12599/18954 | 2/3 | 2/3 | 37/18954 |
| DUPLICATE_TOPICS_A | 11/18 | 11/18 | 2/3 | 0 |
| DUPLICATE_TOPICS_B | 11/18 | 11/18 | 2/3 | 0 |
| CONTRASTED_TOPICS | 1383/2240 | 5/8 | 2/3 | 17/2240 |
| ALPHA_CONCENTRATED | 323567/485514 | 2/3 | 2/3 | 109/485514 |
| ALPHA_SPARSE | 3364/5103 | 2/3 | 2/3 | 38/5103 |
| UNIFORM_WORDS | 2/3 | 2/3 | 2/3 | 0 |
| ASYMMETRIC_ALPHA | 60871351/93312000 | 47/72 | 2/3 | 40649/93312000 |

BASE的前缀预测比单词边际预测降低精确风险37/18954，约0.001952。相同单词边际概率1/3的三世界中，ALPHA_CONCENTRATED超额风险109/485514约0.0002245，BASE为37/18954，ALPHA_SPARSE为38/5103约0.007447。主题混合先验影响文档内可利用的预测依赖。两个完整观察别名对在所有三预测器的风险上完全一致，说明更好的前缀预测仍不能识别被交换的隐主题标签或重复主题的先验。三个独立词的负例中，oracle与unigram严格相同；UNIFORM_WORDS全部预测器严格相同。

## 数学与实际计算
R轨对每个世界27格联合分布逐项累积 `P(x,y)Σ_k(q_k(x)-1[y=k])²`。9世界、9个前缀、3类，完全有理数BigInt运算。独立B轨从二阶矩 `R(oracle)=1-Σ_xΣ_k P(x,k)²/P(x)`、`R(unigram)=1-Σ_k P(k)²`、`R(uniform)=2/3` 计算，再用 `Σ_x P(x)Σ_k(q_k(x)-oracle_k(x))²` 验证风险差。两种方法对9世界3种风险及两种超额风险严格一致，无浮点容差。R轨在隔离JavaScript环境执行1222次已计数的算术及一致性操作，B轨执行423次已计数的二阶矩及一致性操作；这些计数不是1222或423个相互独立的科学假设检验。

上传后的R轨源码 [r237_s33_prefix_brier_exact_20261028.js](r237_s33_prefix_brier_exact_20261028.js) 已从远端重新读取，在隔离JavaScript执行环境以同一冻结JSON模拟Node fs输入实际运行，完整九世界结果与 [机器收据](R237_S33_PREFIX_BRIER_EXACT_RECEIPT_2026-10-28.json) 精确一致。上传的B轨Python脚本 [b_r237_s33_second_moment_independent_20261028.py](../evidence_audit/b_r237_s33_second_moment_independent_20261028.py) 尚未完成Python命令行运行。两种数学路线已在隔离JavaScript执行环境分别实际计算，属于项目内部程序性复核。GitHub Actions本轮没有启动，CI=NOT_RUN。

## 科学限制与验收
已知人工概率的Bayes oracle风险是理论期望，不能视为真实训练后独立留出样本的经验Brier、真实语料校准、时间外推或历史语义有效性。真实E2=0，历史E3=0，外部独立团队复现=0。R073模型及评分规则、PESEN v0.1冻结。既有R237有界正式验收状态保持不变，S33为新增有界E1研究。
