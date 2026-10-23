# R311 限定科研报告：有界信任关系的网络连通性与非传递性

日期：2026-10-23（Asia/Taipei）。原始239候选 **04-011 Bounded Confidence Models（P1）**。等级：**CLOSED_BOUNDED_E1_ARTIFICIAL_R311_CONFIDENCE_RELATION_GEOMETRY**，不是完整HK或Deffuant更新模型的结题，更不是真实人类意见E2或历史E3。

## 1. 原论文、旧研究范围与新增问题

Hegselmann & Krause (2002), *Opinion dynamics and bounded confidence: models, analysis and simulation*, JASSS 5(3) art.2，原作者开放论文 https://www.jasss.org/5/3/2.html ，研究同步有界信任意见动力学。Deffuant、Neau、Amblard、Weisbuch (2000), *Mixing beliefs among interacting agents*, *Advances in Complex Systems*, DOI https://doi.org/10.1142/S0219525900000078 ，提出置信阈值内两人随机相遇并调整意见。Lorenz (2007), *Continuous Opinion Dynamics Under Bounded Confidence: A Survey*, DOI https://doi.org/10.1142/S0129183107011789 ，指出两支更新规则不同而共享近邻选择的概念。

[旧R066研究](../R066/README.md)已经实现HK同步平均化与DeGroot、Friedkin–Johnsen三模型比较；早期[正式验收](../R066/R066_FINAL_ACCEPTANCE_STATUS.json)还涉及16个真实村庄、1,872条完整配对的**内部村庄留一预测**，但其HK部分未使用原始家庭关系网络，因此不能直接宣称真实社会网络上HK机制的独立识别。R311**不重复R066的HK动态，也不将R066真实数据当作R311新E2**，而是从整个有界信任模型家族抽取一个更一般、理论上必要但远不足以推出实际演化的结构性问题：**阈值邻接关系是否传递，以及局部可达是否代表所有节点直接相容**。

## 2. 事前冻结及完整人工来源

[冻结协议](../../protocols/R311_BOUNDED_CONFIDENCE_FOUR_NODE_1944_PAIR_SOURCE_PRESCORE_FREEZE_2026-10-23.md)先行写入main [commit 98f463ac](https://github.com/edwardsage419/Psychohistory-Research/commit/98f463acd827ab9535ae134c4d22bbe3235da837)，未读取原人类试验数据。

构造四个不同编号的**纯人工意见节点**，每个意见独立取0、1/2、1，共3^4=81个有序配置；置信阈值epsilon取0、1/4、1/2、1，共**324个人工图世界**。任意不同节点无向相容边(i,j) 当且仅当 |x_i−x_j|≤epsilon，阈值等号也允许相容；每世界枚举6条无序不同节点对，总共**1944条完整人工source行**，不是1944名受访者。自己到自己的4个自环在概念上存在，但不计入6个source dyad。

每source精确保存完整四意见向量、epsilon、两节点编号与意见、精确距离、是否有边、两端归属连通分量、分量数、边数、图是否连通、是否六对全部相容、是否存在三节点非传递见证。所有数值以Fraction有理数保留，不通过有损浮点比较阈值。

## 3. 冻结前明确的数学反例

四意见序列(0,1/2,1,1)，各阈值下：

| 阈值epsilon | 六对中的相容边数 | 连通分量数 | 全员两两相容? |
|---|---:|---:|---|
| 0 | 1 | 3 | 否 |
| 1/4 | 1 | 3 | 否 |
| 1/2 | 4 | **1** | **否** |
| 1 | 6 | **1** | 是 |

epsilon=1/2时，节点0与1相容，1与2相容，但0与2的距离1大于阈值，不相容。网络**连通而非完全图**，近邻可达关系不具有一般传递性；不能据此推出所有两人会直接平均化，更不能推出以后全体达成共识。epsilon增加时，任何原有边不会消失，连通分量数不能增加；epsilon=0时，只能因完全相同的意见产生不同节点间边；epsilon=1时，所有意见均在[0,1]，故每个世界全部6条边存在。

这些是**固定的数学图结构性质**，不是对真实社交意见聚类、共识概率、文化传播或历史极化的测量。R311未更新任何一轮个体意见，未计算最终聚类或时间趋近速度；真正HK同步/Deffuant异步状态转移需保持独立研究项目。

## 4. 独立证明和GitHub永久归档

[原生有限主程序](r311_exact_bounded_confidence_relation.py)覆盖完整324个图与1944原dyad，实际**5845项主unittest**在Python3.11/3.12分别通过；[独立来源审计](../catalogue_audit/independent_r311_source_audit.py)严格不导入生产源码，使用不同的union-find算法构造所有连通分量，再独立逐source比较边、距离、分量、非传递见证及JSON世界，附缺行/重复/篡改等12项unittest。两个算法共验证阈值单调性和完全图负/正对照。

完整[1944条原始人工来源](R311_ALL_1944_ORIGINAL_CONFIDENCE_DYAD_SOURCES.csv)、[324人工世界全部原结果](R311_EXACT_BOUNDED_CONFIDENCE_GRAPH_RESULTS.json)、[SHA256原始字节收据](R311_MACHINE_RECEIPT.json)经[GitHub Actions run39956812166](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39956812166)全部**3/3 completed/success**，第三作业永久归档到main [commit 2e5674e6](https://github.com/edwardsage419/Psychohistory-Research/commit/2e5674e6251718475372b485b6443592540bea23)。CSV SHA256 `6165ad285463128177742ef26bfe2097fb88a2c13713ac511f4f9dffd45ce5f8`，原结果JSON SHA256 `1fc9e2b120082dd13304a066b1668024c357901890c822b677aa990ff033cd62`。

本轮没有新真人/动物E2、没有历史E3。R066当前真实16村留一研究不改，R073及PESEN v0.1冻结，全部原R模型学习未结束，因此暂不进入分类或模型熔炼。
