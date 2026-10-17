# R080 Phase B：真实原始网络快照中的孤立真人节点被省略——首次任何真人网络结果前资格门修订 Rev-002

**日期：2026-10-17。唯一触发为原作者来源文件结构，尚未出现本项目任何64网络真人合作率、边变化或八处理宏得分。** 初始 [Phase B Rev-001 协议](R080_REAL_64_HUMAN_NETWORKS_HUMAN_BOT_SPLIT_TOPOLOGY_BEFORE_SCORE_FREEZE_2026-10-17.md) 永久保留，不得回填成直接通过。

## 实际失败及原始数据无评分调查

[首次完整64网络模型门与42纯合成合约 CI 38998214433](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38998214433)：合成42项 **PASS**，64份Mendeley Data v1原作者JSON全部下载并逐个官方SHA256一致；真实网络资格因 `R080_NETWORK_SNAPSHOT_NODES_NOT_EQUAL_REAL_ACTORS` FAIL CLOSED，输出 `all_64_networks=null, per_treatment=null`，未输出任何真人合作率、网络边变化或干预对比得分。**不允许把这项失败标为成功或删去。**

随后 [来源独立严格SHA全64结构审计 CI 38998347906](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38998347906) 成功，只统计按真实作者处理分组的网络节点不一致，**未计算任何真人行为或拓扑二阶结果**：

| 原始 treatment | 真正网络数 | 31×8快照数 | 缺失于快照的真人节点出现总数 | 缺失于快照的机器人节点出现总数 | 额外陌生节点出现总数 |
|---|---:|---:|---:|---:|---:|
| no_bots | 8 | 248 | 222 | 0 | 0 |
| allc_bots | 8 | 248 | 197 | 0 | 0 |
| tft_bots | 8 | 248 | 434 | 0 | 0 |
| random_mgmt_bots | 8 | 248 | 223 | 0 | 0 |
| engaged_mgmt_bots | 8 | 248 | 476 | 0 | 0 |
| disengaged_mgmt_bots | 8 | 248 | 411 | 0 | 0 |
| disengaged_mgmt_visible_bots | 8 | 248 | 502 | 0 | 0 |
| single_mgmt_bot | 8 | 248 | 582 | 0 | 0 |

**关键事实：** 所有1984个真实原作者网络快照均无额外陌生节点、无机器人节点缺失、无任何`links.source/target`指向快照`nodes`集合外（这些错误计数均为0）；换言之仅有本网络的**孤立真人**在部分JSON的graph nodes表示中未列出，而且确实没有任何实际边引用那些真人。64份完整`players`源主表仍恰每网络16真人、共1024个网络内人类身份槽；每个网络的实验对象不得因在某快照没边而被丢掉。断言“缺失者确实是该轮服务器主动删掉但仍参加实验的真人”属于来自文件结构的最合理**图模型表示推断**，尚非独立回访的作者系统日志。

## Rev-002 唯一资格修订（冻结在首次真人 E2 结果之前）

原协议要求任意网络时点`network.nodes == players`，造成合法零度人类节点被视为缺失样本。改成：

1. 每个网络的`players`依旧是原始人物与机器人**唯一、固定的完整身份名册**，每网络恰16个人类，全部64个网络不丢任何人；本人每轮C/D只从原`result_behaviors.cooperation`抽取，**不能以某快照节点是否在network.nodes推断真人行为、缺失或是否退出**。
2. 任意时点`network.nodes`须为`players`的**不含重复、无额外陌生实体的子集**，原始**所有机器人节点必须出现**；允许漏列的对象**只能是人类**，并且该真人不得成为这个快照任何`links.source`或`links.target`，即该快照在观测图中零度。
3. 全部`links`端点必须既在完整`players`又在这个快照的`network.nodes`中，依旧拒绝自环、同一无向边重复、非简单无向图、陌生节点、机器人缺失及任何不合法节点。
4. 第1/第31快照的HH/HB/BB边实际分母仍由原始完全名册决定，真人潜在HH边数固定 `16×15/2=120`；一个未列出但从未连接任何边的真人对边计数贡献0。跨期增减边不编造孤立者的边，也不重新定义处理分层。
5. **除上述图中只缺零度真人的表示例外，初版所有决定与预先指标全部保留不变**：64个真实JSON逐个官方SHA核验，30动作行为轮、31图状态、八处理各8独立网络，唯一64×16=1024人类总身份槽，`is_bot`严格排除机器行为，完全没有真人缺失行动插补；每网络等权30轮首末/两段真人合作率、30次相邻网络实际边差/分类边数及八处理每网络等权表都原样。继续无真人社交/AI因果效果证明。
6. 本次修订是**基于真实源结构预评分校验失败的实质修订**。最终R080报告必须列明初版FAIL+结构排查+Rev-002冻结提交+首次64网络评分运行顺序，不得宣称“从一开始完全不修改资格门”。若修改后产生第二个来源结构错误，必须再次FAIL CLOSED并在任何实际分数前提交新的结构修订，而不是自动放宽其他条件。

`R080_REV001_ALL_NETWORK_NODES_EXACT_PLAYERS_GATE=FAIL_RETAINED`  
`R080_REV002_SNAPSHOT_NODES_SUBSET_PLAYERS=ONLY_MISSING_TRUE_ISOLATED_HUMAN_NODES`  
`R080_NETWORK_HUMAN_POPULATION_STILL_ALL_16_PER_NETWORK=YES`  
`R080_E2_HUMAN_COOPERATION_OR_TOPOLOGY_SCORES_AT_FREEZE=NONE`  
`R080_MENDELEY_PUBLISHER_SHAS_VERIFIED_ALL_64=YES`  
`PESEN_v0.1=FROZEN`
