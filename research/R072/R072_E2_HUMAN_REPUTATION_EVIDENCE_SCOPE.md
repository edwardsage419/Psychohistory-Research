# R072 真实间接互惠与信誉实验候选及不可越过的数据门

2026-10-16。此文件是**已出版论文/数据目录适用性核查**，不是对原始真人记录的数据下载、字段复核或人类信誉机制校准。R072 的 11,664 条结果全部仅为 E1 合成机制，不能用这份文献目录替代 E2。

## 理论锚与不可直接复算的作者结果

- [Nowak & Sigmund (1998), *Evolution of indirect reciprocity by image scoring*](https://doi.org/10.1038/31225)：提出间接互惠中观察信誉的重要性；R072 使用其思想做独立四人固定规则数学玩具，并未复算原模型的进化动力学。
- [Ohtsuki & Iwasa (2004), *How should we define goodness?—reputation dynamics in indirect reciprocity*](https://doi.org/10.1016/j.jtbi.2004.06.005)：论文理论检验 4096 类声誉判断情形，发现能稳定维持合作的候选“leading eight”与评判拒绝坏名声人的行为相关；**本项目只对IMAGE/STANDING/STERN三种显式简化规则的 11,664 个不同策略初态/信息制度组合模拟**，没有计算原文演化稳定策略、突变/观察错误稳态。
- [Kandori (1992), *Social Norms and Community Enforcement*](https://doi.org/10.2307/2297925)：社会记忆如何支持不同配对的社区层面执行；R072没有实现其自实施协议或民间定理，四人循环排程中的复遇也不是“从未再遇”的严格间接互惠设计。

## 真人候选 A：有公开 XLSX 原始附件的现场间接互惠研究

[*Indirect Reciprocity; A Field Experiment* (2016), PLOS ONE DOI 10.1371/journal.pone.0152076](https://doi.org/10.1371/journal.pone.0152076)，期刊官网/PMC 明确列出 Supporting Information [S8 原始数据 XLSX](https://doi.org/10.1371/journal.pone.0152076.s008)、约37.7KB。出版者声明相关研究数据在原论文及 supporting information 中。

**本阶段仅确认 publisher 公共附件链接存在，尚未下载或固定 XLSX 原始字节 SHA256、未读取表名/列名或抽样行，未建立真实贡献或声誉标签测量。** 该研究是在真实网络社区中做间接互惠相关的现场干预，行动机会/回馈方式可能不是 R072 五个假设条件中的任一个：`4人明确轮转、二元donor成本1 recipient收益2、每次事前二元公共信誉、三种评判规则、精确1/4报告出错`。在逐项确认记录字段和伦理/匿名限制前，不得把标题中的“indirect reciprocity”直接解释为匹配 R072 的数学规则。

该附件可作为后续单独**仅元数据和去标识 schema**审计候选。需要遵守公开数据原授权、不将个体 profile 文本、图片、成员特征或收到请求的原始逐行内容自动发布到 GitHub。

## 真人候选 B：交替公开物品与间接互惠的实验

[Milinski, Semmann & Krambeck (2002), *Reputation helps solve the ‘tragedy of the commons’*, Nature DOI 10.1038/415424a](https://doi.org/10.1038/415424a)。作者报告跨公开物品轮次与声誉游戏交错，信誉可能提高前者贡献。它研究的跨任务转移、在几个不同游戏间的声誉保全，和 R072 的每轮捐赠不同，**原始逐笔事件数据与本项目可用许可证目前未恢复**，不可将作者 Figure 1 的均值当作本项目独立数据 E2。

## 缺失的识别合同

任何真正 R072 E2 至少需明确：行动者、受赠者、捐赠时刻和当时真实帮助/拒绝**机会风险集**；实验者展示给捐赠人的事前信誉状态与其生成规则；报告是否存在噪音及错误的实测日志；该行为的成本和受益者支付定义；重复身份隐私许可、实际随机化和独立组划分、非行动者是否可观测。即便现场 XLSX 可读，其 S8 是否包含这些字段仍 `UNKNOWN`，对外部真实信誉规范与机制的因果识别 `NOT_ESTABLISHED`。

`R072_E1_SYNTHETIC=PASS`；
`R072_HUMAN_DATA_S8_BYTES=NOT_RETRIEVED`；
`R072_HUMAN_IMAGE_STANDING_STERN_EXACT_CONTRACT=NOT_ESTABLISHED`；
`R072_REAL_REPUTATION_CAUSAL_MECHANISM=NOT_ESTABLISHED`；
`R072_E3_EXTERNAL=OPEN`；
`PESEN_v0.1=FROZEN`。
