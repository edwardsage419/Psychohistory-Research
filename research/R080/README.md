# R080：原作者64个真实人机混合互动网络的合作轨迹与连接拓扑（E2）

2026-10-17，**正式状态 `CLOSED_BOUNDED`，A01–A06按有限范围验收，证据等级 `E2_TRUE_AUTHOR_NETWORK_DESCRIPTIVE`**。完整数据首次真正建立多个节点的人类互动、人工代理和网络动态三类状态的严格分离；非同伴/机器人因果效果识别、非长时期历史预测，PESEN v0.1冻结。

原作者 Shirado & Christakis（2020），[*iScience*论文](https://doi.org/10.1016/j.isci.2020.101438)，[第一作者Mendeley Data v1](https://doi.org/10.17632/t963ktp6ft.1)，CC BY 4.0。官方 `70`份文件包含 `64`份原始实验JSON、3个R源脚本和3个CSV；通过官方文件公开下载地址**逐个以发布方的SHA256核验全部64份原始网络JSON**，而非自己制造机器人行为或抄论文图表结果。64个实际网络×16真人=1024场次内真人身份槽，8个原作者处理各8网络，30行为轮、31图状态，共1920网络行为期/1984网络快照、30720个理论真人行动槽中实际观测C/D `27656` 次（90.026%）。`players.is_bot`明确拆开真人与机器人，任何bot决策不进真人合作分子或分母；原作者`result_networks`的零度真人有时不出现在节点表，但完整16人名册始终以`players`为准。

### 八种处理实际计算结果，原始网络等权

| 原始实验处理 | 30轮首尾真人合作率 | 改善/持平/恶化的独立网络 |
|---|---|---|
| `no_bots` | 65.1%→36.7%，**−28.3百分点** | 1/0/7 |
| `allc_bots` | 65.6%→31.0%，**−34.6百分点** | 0/0/8 |
| `tft_bots` | 80.6%→47.3%，**−33.4百分点** | 0/0/8 |
| `random_mgmt_bots` | 67.2%→68.1%，**+0.9百分点** | 4/1/3 |
| `engaged_mgmt_bots` | 70.1%→31.7%，**−38.5百分点** | 0/0/8 |
| `disengaged_mgmt_bots` | 60.0%→79.4%，**+19.4百分点** | 6/0/2 |
| `disengaged_mgmt_visible_bots` | 68.5%→85.8%，**+17.3百分点** | 8/0/0 |
| `single_mgmt_bot` | 66.7%→75.3%，**+8.6百分点** | 6/0/2 |
| **64网络总体等权** | **68.0%→56.9%，−11.1百分点** | 25/1/38 |

64网络首末平均真实真人–真人连接边 `35.922→52.719`，相应HH密度 `0.29935→0.43932`，但整体真人合作却下降；**增加连边不代表合作必然增加**。机器人节点每处理可能为0、16或5个，某称为`single_mgmt_bot`处理在原始JSON中有5个`is_bot=true`节点，机器人逻辑实体与此5个节点的映射尚需独立确认。当前只呈报真实样本的组内短期结果，原实验的处理赋值、失访机制和图内干扰的独立因果识别仍未建立，不能把八处理首末差冒充作者论文完整因果分析。

### 研究交付与审计链

- [正式R080科学报告（全部处理、真实拓扑与负面结果）](R080_FULL_64_HUMAN_BOT_NETWORK_E2_SCIENTIFIC_FINAL_REPORT_2026-10-17.md)
- [70项元数据、真人/机器人身份原始来源门冻结](../../protocols/R080_ORIGINAL_64_HUMAN_BOT_NETWORK_SOURCE_ACCESS_AND_ENTITY_GATE_FREEZE_2026-10-17.md)，[第一次全网结果之前冻结的原始Phase B规则](../../protocols/R080_REAL_64_HUMAN_NETWORKS_HUMAN_BOT_SPLIT_TOPOLOGY_BEFORE_SCORE_FREEZE_2026-10-17.md)，[因零度真人在网络节点快照省略、但**在任何真结果出现前**冻结的资格修订Rev-002](../../protocols/R080_PRE_FIRST_REAL_NETWORK_METRICS_GRAPH_ISOLATE_AMENDMENT_REV002_2026-10-17.md)（commit `f0b4dc6d206b0a4f036115b316cf46d76fbfd8fd`）
- [全部64真实SHA核验、45项合成测试成功的首次真人网络E2运行](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38998549613)，[完全独立再次重下载并严格核验所有原始SHA且结果全字节一致的CI](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38998839902)均SUCCESS
- [11,745字节真实来源、匿名八处理/全网络聚合数字结果](R080_FIRST_PARTY_64_HUMAN_NETWORKS_TOPOLOGY_E2_RESULTS.json)，SHA256 `7b7d231d97a98c4b08e7d3658fa8e943bacd60aef1d8529754cd1f75179b99c8`，Git blob `c7e9a3ed76302f6eb4878acb278818d1db91e3c0`
- [完整机读验收（A01–A06）](R080_FINAL_ACCEPTANCE_STATUS.json)，[严格源码](r080_original_64_networks_human_only_cooperation_topology.py)和[45项合成全图与隐私验证](test_r080_original_64_networks_human_only_cooperation_topology.py)

### 不能抹去的失败

[初始全网 Rev-001 数据门](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38998214433) 因真人零度节点未列出而真实评分 `FAIL CLOSED`；随后[全64真实来源的不评分结构排查](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38998347906)核验无陌生节点、无机器人节点省略、无边指向快照外节点，因此只针对零度真人做Rev-002，而非随意减少原始样本。第一份[独立重下载尝试](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38998713165)因至少一个Mendeley CDN下载流不是官方SHA字节也正确拒绝；最后只加**有限下载重试/临时签名链接刷新，不修改发布方SHA、任何样本或任何评分公式**，独立结果才获批准。已完成研究不会抹平这几项负证据。

R080现在止于**真实、复算过的多人网络动态观测 E2**。下一项R081应在已知八类处理完整结果的前提下，先核验原作者组级随机分配和网络干扰及真人动作缺测机制，再决定是否能够注册一个真正有效的因果识别检验或仅有界描述研究。PESEN v0.1继续冻结。

`R080=CLOSED_BOUNDED`；`TRUE_AUTHOR_SOURCE_SHA=64/64`；`HUMAN_NODES=1024`；`E2_NETWORK_BEHAVIORS=COMPLETE_DESCRIPTIVE_WITH_MISSING_HUMAN_ACTIONS`；`R080_PEER_CAUSAL_EFFECT=NOT_IDENTIFIED`；`PESEN_v0.1=FROZEN`。
