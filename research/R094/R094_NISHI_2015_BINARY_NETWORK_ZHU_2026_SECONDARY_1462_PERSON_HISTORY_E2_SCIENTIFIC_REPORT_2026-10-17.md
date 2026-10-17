# R094 正式科学报告：二元网络公共品中个人上一轮合作信息的可见性条件反转

**2026-10-17，R094=CLOSED_BOUNDED，E2已发表真人二元合作记录、2026次级整理来源、完整留出原受试者预测成功；A01–A06均为限定PASS。** 源未提供原始80个实验场次的标识，因此**不是**真正的原始实验完整留出场次外部复验；不声称人类心理机制因果/新招募E3/历史长期动力。PESEN v0.1依旧FROZEN。

## 1. A01：新独立二元真人实验和源层次的真实性

原2015年真人实验 **Nishi, Shirado, Rand & Christakis**, "Inequality and visibility of wealth in experimental social networks", *Nature* 526:426–429, [DOI 10.1038/nature15392](https://doi.org/10.1038/nature15392)。1462名原始真人，80个原始不同网络实验场次（四种原始禀赋不平等×可见或不可见×十次），每场网络经过10轮互动并有边连接更动。决策是每个个人给每邻居50单位合作/0单位背叛，因此记录为二元选择；**不是**R089的六人全球公共品二元选项，也非同一人跨实验。

可获取而实际使用的是第二研究者 **Zeyu Zhu (2026)** 整理的网络选择和反应时间次级分析包，[*Decision time is associated with future cooperation and social rewiring decisions in network public goods games*](https://doi.org/10.1371/journal.pone.0347919)，该论文重用2015年Nishi原实验并新增之前未公开的研究变量。正式来源[Zenodo v1 19544006](https://zenodo.org/records/19544006)，`individual_data.csv` **720,707字节**，Zenodo正式发布MD5 **`85db2536b5be1cd50266900e61590d5a`**，两次独立取得原文件全SHA256 **`b37fa71434dd46249a0e7f43f9b9e798b1d3cafcffea3c80bc6997b99b6dd0a5`**。这证明**2026次级作者的该文件**来源精确，不能证明其每个单元格与2015年未发布原采集日志相同。来源不作重新发布，不提交个人 `node_id` 或选择轨迹。

## 2. A02：真正的独立源数据资格、先冻结后检视

[Phase A来源MD5/只读安全列名冻结](../../protocols/R094_ZHU_2026_NISHI_2015_BINARY_NETWORK_PGG_SECONDARY_CURATED_ZENODO_CSV_SOURCE_PRE_OUTCOME_FREEZE_2026-10-17.md)，commit`8b8adb815f329227215dae07691b9bfdf16a0c24`。[源真实首轮CI39019242351](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39019242351) **21synthetic/Zenodo真实MD5+SHA均PASS**：原CSV有**14,620行×15列**，`round`, `node_id`, `decision`, `decision_time`, `visibility`, 邻居行为和**未来**`decision_lead`；真正缺失原始 `session_id`、原始贫富条件字段及直接人工/软件代理动作确认字段。没有读取任何真实合作值。

[Phase B按节点身份、轮次、财富可见性来源资格先冻结](../../protocols/R094_PHASE_B_ZHU_2026_NISHI_BINARY_NETWORK_NODE_ROUND_VISIBILITY_METADATA_FREEZE_2026-10-17.md)，commit`6d3d37b88c283433859c6f902375a2c00f2572e5`，[独立再下载同原文件CI39019371936](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39019371936) **合成累计42synthetic全PASS**：`14620=1462 ×10`，1462人各有1..10完整十个轮次ID，没有重复人轮编码，没有丢人号，`visibility=0`原人726、`visibility=1`原人736，所有人在原10轮里可见性不变。然而**单纯1462个独立node_id不能划分80个原始共同网络场次**；任何通过排序重建“80组”都是编造，不可执行R073/R089 leave-one-session-out。

## 3. A01/A03：真实二元行为读取前冻结的个体LOO预测合同

[Phase C计分前源binary 0/1合同和严格隐私](../../protocols/R094_PHASE_C_NISHI_ZHU_BINARY_NETWORK_1462_PARTICIPANT_LOO_M012_PRESCORE_FREEZE_2026-10-17.md)，commit`fb84bf8a427014e416c2db85070330eec4d396f1`。二元决策必须恰好0/1或0.0/1.0，空/NA/null缺失不加入计算亦不补全，来源非这类值即全研究fail closed。2015年原作者论文报实际**13,560次决定**；独立2026整理文件重新核验出14,620人轮数据，其中**13,560个真正有记录的原二元决定**，**1,060个二元选择缺失**。必须同一原始受试者i前轮t−1和当轮t都存在0/1，才能评分t2..10。由此得到**12,110次真实个体下一轮预测目标**；未人为筛选正向任务。

冻结三个无需学习参数的预测器：
- **M0**：相同已公布`visibility`条件与同目标轮t的**其他真实源受试者**合作0/1均值，严格剔除留出受试者本轮乃至所有轮的源记录；由于80个原场次ID不公开，此均值跨不同真正实验场次，**不是实际同场次伙伴均值、不是现实日历实时预测**。
- **M1**：待预测受试者上一轮自己已记录的二元合作/背叛`decision(i,t-1)`，不是2015原件的未验证隐性意图变量。
- **M2**：早期R089/R090/R091/R093固定`(M0+M1)/2`，没有观察此次score之后更新权重。
- 统一目标Brier误差`(p−decision(i,t))²`；不引用2026数据中的已算好未来结果列`decision_lead`，不用可能泄漏未来行为的邻居合作/连边事件，也不用响应时长作为事后增添模型变量。

不声称目前M0拥有2015年同组历史信息；此对照的难度与早期研究不同，不能跨研究相加增益形成总体心理定律。

## 4. A03：真实完整原始来源二元预测结果与透明阴性

**完整个人留出人—轮二元选择共12,110组有效目标**，其中财富不可见5910、可见6200。同一记录的平均二元Brier误差越小越好：

| 原始2026出版数据条件 | 真实配对目标 | M0其他可见性同轮均值 | M1本人前轮选择 | M2固定各半 | M1对M0的预测改善 | M2对M0的预测改善 |
|---|---:|---:|---:|---:|---:|---:|
| **财富不可见 0** | **5910** | 0.2016297951 | 0.1532994924 | **0.1277109717** | **+0.0483303028** | +0.0739188234 |
| **财富可见 1** | **6200** | 0.2417716537 | **0.2654838710（更差）** | **0.1928013012** | **−0.0237122172** | +0.0489703525 |
| **全部** | **12110** | 0.2221813660 | 0.2107349298 | **0.1610355004** | **+0.0114464362** | +0.0611458656 |

**最关键的预冻竞争模型发现是M1信息价值“条件反转”：**只用自己的上一轮真实选择相对其它人的同轮均值，财富不可见层正改善 +0.04833，而可见层却明显**更差** −0.02371。两层M2固定混合优于M0，说明个体短期历史与条件轮信息有互补的**回顾性预测意义**，但M1单独优于条件基线不是无条件规律。正式源人级配对误差符号 **856个原人M1较好、558人更差，48人没有合法连续两轮的评分目标**，没有删去任何负例。其它人工分层或复杂模型没有在读数后引入。

这两个来源`visibility`层的M1改善差是描述性而非正规聚类不确定性界限；源只有两个可见性水平，论文原本有80共同实验场次和四种贫富初态，但次级CSV**丢失原始group分配和贫富初态**；因此不能把可见性差异当政策/因果处理效应，不能做准确的session-cluster区间。人员共享网络互动和信息、初态混合导致协变量相关性；有效12,110个预测不是12,110个独立小组。

## 5. A04：真实测试拦截与复制、负结果保留

R094 Phase C最初 synthetic测试某可见性层仅三名模拟参与者，其中一名丢当轮选择后其它训练者不足，正确触发冻结的两位其它人要求：[CI39019608534](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39019608534) FAIL; 仅把合成测试补一位原模拟同条件参与者，**没有降低真实评分门槛**，[CI39019647183](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39019647183) 80项合成PASS，真实程序严格拒绝 `KeyError`。以后严格先冻结[Phase C2只输出异常类而不打印原节点ID](../../protocols/R094_PHASE_C2_FIRST_TRUE_BINARY_MODEL_SOURCE_EXCEPTION_CLASS_ONLY_2026-10-17.md) (commit`147f63e8eb191d7307e3be73c9ac2ea49efeb286`)，[CI39019811350](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39019811350)确认KeyError后，另冻[Phase C3仅安全Python源码文件和行号](../../protocols/R094_PHASE_C3_SAFE_KEYERROR_CODE_LOCATION_BEFORE_REACCESS_2026-10-17.md) (commit`f6d63f5bc56b975270efb3a1a40b6f3da1a24839`)，[CI39019903763](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39019903763)定位源码行152，发现读取已审计来源元数据的固定键`number_of_original_node_IDs_with_visibility_change_across_rounds`拼写少了`original`，是**仅代码来源校验键拼写错误**，与真实合作或模型选择无关。只修正此来源变量键、不读源行为据效果优化，[首次80synthetic + 全原真实二元行动成功CI39019950466](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39019950466)。既往5次真实/合成失败永久保留，非编造阳性。

## 6. A03/A06：两次真实原始来源独立下载与永久匿名证据

- 第一份[CI39019950466](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39019950466) 80项全部合成PASS，官方真实2015次级数据整源MD5/SHA及13,560合法原二元行动、12,110有效个体下一轮预测均真正运行；生成**3685字节匿名结果**，SHA256 **`2b68edc1efc87cf63df4eb915c09e19ac5fc5696bcbdd54874601393718045f0`**。
- 第二份[CI39020029476](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/39020029476) **SUCCESS**，完全从Zenodo再次重取出版方整个720,707字节原件，80synthetic全部重新PASS，得到**同字节数与相同完整SHA256的3685字节原研究统计**；严格校验来源MD5/全SHA、1462源参与者、1060缺失、两层M1符号反转和M2正改善后，永久提交到本GitHub `research/R094/R094_ZHU_NISHI_2015_BINARY_NETWORK_1462_ACTORS_12110_INDIVIDUAL_HOLDOUT_E2_RESULTS.json`（Git blob`eea544b6b61d1f0658284456c760862b646a9edd`）。没有原版或次级版作者个体数据、原node_id或微观行为文件重发布。
- 80 synthetic由[首个作者安全来源21项](test_r094_zhu_nishi_2015_binary_network_original_sessions_secondary_source_gate.py)、[元数据21项](test_r094_phase_b_nishi_2015_2026_binary_network_person_round_visibility_only.py)、[二元目标38项](test_r094_zhu_nishi_2015_1462_binary_network_participant_holdout_E2.py)组成。可完整复现的[真人二元行为原数据复算源码](r094_zhu_nishi_2015_1462_binary_network_participant_holdout_E2.py)及三份独立阶段安全源程序已入main。所有规范均在相应真人源内容调用之前独立提交。

## 7. A01—A06有界结题与后续

A01事前区分2015实验与2026次级整理、二元模型及目标冻结**PASS**；A02完全源MD5+SHA、原1462×10十轮、可见性固定和80场次标记不可得审计**PASS**；A03纯synthetic80及双真实原源独立重下载、同SHA12110个合法二元下一轮预测**PASS**；A04最初模拟设计错误、真实KeyError严格拒绝、安全诊断与只修来源索引、可见层M1的**负**向和558原人负效应全保留**PASS**；A05本轮只是2026次级整理Nishi2015真人记录的个体层回顾性E2，非可见性因果、不是作者原始日志逐字节、不是LOSO跨场次、不是前瞻E3**PASS**；A06冻结协议、源程序和完整匿名真实结果、自动CI及主repo索引**PASS**。

**`R094=CLOSED_BOUNDED`, `ORIGINAL_HUMAN_BINARY_INDIVIDUAL_LAG_INFORMATION=HETEROGENEOUS_0_POSITIVE_1_NEGATIVE`, `M2_FIXED_MIX_BOTH_VISIBILITY_STRATA_POSITIVE`, `ORIGINAL_80_SESSION_LOSO=NOT_ESTABLISHED`, `PESEN v0.1=FROZEN`。**

**R095优先**：寻找保留真实80场次ID的Nishi2015一手原日志、或另一不同实验室多场次同二元合作的原始数据，使真正的留出完整场次与可见性分层聚类检验可行。若无法获得，保留R094的组间不可推断边界，而不是从`node_id`、自然行次或标签臆造场次。
