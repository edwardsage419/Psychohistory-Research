# R066：Larson–Lewis 2026 真实纵向态度与家庭网络源数据审计

日期：2026-10-16。研究属性：**E2 真实来源结构与源码派生网络可行性审计**。R066 依旧 ACTIVE；三模型实证预测的模型拟合、交叉村庄验证和独立外部 E3 尚未发生。

## 1. 研究来源与已发布数据核实

Larson & Lewis, *Networks shape political attitude change*，*Network Science* 14, e23（2026），DOI [10.1017/nws.2026.10038](https://doi.org/10.1017/nws.2026.10038)。论文描述 16 个乌干达村庄的家庭/人际关系提名、针对难民态度的基线、随机部分受访者的干预后即时评估，以及 2–3 周后的全体末次评估。作者原生数据 DOI [10.7910/DVN/RAHSVM](https://doi.org/10.7910/DVN/RAHSVM)。

先于实证查询冻结 [数据集目录可用性方案](../../protocols/R066_E2_DATAVERSE_CATALOG_AVAILABILITY_2026-10-16.md)。实际 [GitHub Actions run 38862426339](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38862426339) 全部 PASS，Harvard Dataverse 返回**公开发布 V1.0**，发布时间 2026-07-29 00:35:44 UTC，许可 CC0 1.0，3 份公开文件。已同步 [目录元数据及 ID](R066_E2_DATAVERSE_CATALOG_RESULTS.json)；查询了另一个已知公开数据集作 API 可达性对照，同样成功。

按新冻结的 [三个文件原始字节与结构协议](../../protocols/R066_E2_LARSON_LEWIS_FILE_SCHEMA_AUDIT_2026-10-16.md) 在远端 runner 下载真实文件，逐个核对目录长度与 SHA256，并解析后删除原始记录。

| Dataverse 文件 | 公开 ID | 字节 | SHA256 |
|---|---:|---:|---|
| Data_LarsonLewis_nws.tab | 14101729 | 444,658 | `10b3e31a6d160e003ff9edf96fc1f6e1a8549ea547b8b8b08aadab1f52b40cae` |
| LL_SpecialIssue_Replication.R | 14101728 | 72,914 | `2e7b7b22887c69c057a6f2fa1a1ff393566826fdb19e6aad6360393ea9f86ff2` |
| Uganda_Codebook_NWS_2026.docx | 14101730 | 30,623 | `48741e3447d27fbf57bb54c995ff68c45ade21592c89e2454e71ab840fc8d161` |

[真实来源文件核验 run 38862848577](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38862848577)：两个作业 success，15 项合成测试 PASS；**数据表 2,125 行×66 列**、R 复现源码 2,163 行、代码本有 187 段与 223 文本节点。结果留存 [V1 schema JSON](R066_E2_LARSON_LEWIS_V1_SCHEMA_RESULTS.json)。

## 2. 初次精确身份拼接为何受阻

初步审计使用 `(village_number,ego)` 作为唯一节点键，四类网络提名直接匹配 `ego`。按照源前冻结 [直接联结门](../../protocols/R066_E2_LARSON_LEWIS_NETWORK_JOIN_GATE_2026-10-16.md)，[run 38863706284](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38863706284) 两个作业成功执行，但科学判定是 **JOIN_CANDIDATE_BLOCKED**：同村 ego 键出现 20 次重复，提名精确匹配仅占各类约 29%。真实样本六题基线及末次同时完整 1,872 行。

该结果真实有效地说明简单 ego 拼接不能作为已授权的网络构造方法。**它并不能证明作者家庭网络不可重建。** 源记录永久留存 [初始匿名联结 JSON](R066_E2_VILLAGE_NETWORK_JOIN_AGGREGATES.json)。

## 3. 原作者 R 程序揭示正确的网络语义

随后通过严格来源哈希的**原作者 R 脚本**核查，确认原算法按 16 个村庄分别处理，村内按 `hhnum` 排序，先 `make_el` 建立个人提名边，然后 `convert_to_hh` 通过各户 `ego,hhh,hh1…hh11` 家庭成员名单，把每条个人提名转成所有可能的家庭连接，最后删除无向重复边和自环。来源行号：原脚本 117–182、206–320。该来源取证已通过 GitHub Actions [run 38864150195](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38864150195) 与更早的代码审查作业。

同时，作者 R 脚本第 31–33 行清楚规定三时段态度量表：`proref1`、`proref2`、`proref_e` 分别为 `noprob+fit+burden+values+land+threat` 六题**直接相加**。在真实数据中，各个非缺失题目均为 1–5，完整量表值在 6–30；不用假设性题目反向计分。

## 4. 按原作者算法派生的家庭网络聚合

在发现初始直接联结错误后，另行冻结 [事后纠错用的原作者家庭网络协议](../../protocols/R066_E2_AUTHOR_HOUSEHOLD_NETWORK_MAPPING_2026-10-16.md)，在未公开原始身份或网络边的情况下用 Python 建立村庄隔离的家庭映射和**匿名网络规模统计**。[真实 run 38864457996](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38864457996) 两作业成功，6 项附加合成测试通过。

| 关系类型 | 非空个人提名 | 可转换为家庭关系的提名 | 去重无向家庭边 |
|---|---:|---:|---:|
| 走访 visit | 7,493 | 3,900 | 4,845 |
| 共同用餐 meal | 6,387 | 3,498 | 4,110 |
| 借用物品 borrow | 4,014 | 2,205 | 2,785 |
| 讨论传闻 rumor | 4,375 | 2,408 | 3,027 |

四类无向关系并集 **8,659 条独立家庭边**，在 2,125 个家庭行节点中覆盖 **2,067 个有边节点，58 个孤立节点**。本研究还发现 456 个家庭成员别名在同一村的多个家庭集合出现，后续建模必须保留多对多映射及由此引起的关系结构不确定性。村内 `hhnum` 未发现重复。

三波完整六题量表分别为 **1,981、905、2,016** 行；前后配对完整为 **1,872 行**，三波全部完整为 858 行。记录来源、计算口径与结果的 [原作者算法派生 JSON](R066_E2_AUTHOR_HOUSEHOLD_NETWORK_RESULTS.json) 已同步。

**重要科学边界：** 这里复现了作者 R 源码描述的家庭映射逻辑并真实计算匿名聚合，**还没有执行原作者 R/igraph 并逐边验证 Python 图的完全一致性**。故状态应当是 `AUTHOR_ALGORITHM_DERIVED_PYTHON_COUNTS`，不是 `EXACT_AUTHOR_R_EDGE_PARITY_PASS`。无论四类边有多少，都未单独证明网络因果作用、确定性意见状态模型的真实性或历史层面的可预测性。

## 5. 三模型下一研究关口

R066 E1 的三模型合成基线已成功；如今取得同一来源中的真实家庭关系候选与纵向六题意见量表，**构建一个受审的跨村庄训练—留出预测设计已经具有可操作的输入基础**。下一次真实拟合前至少冻结：

1. 作者原始 R 网络逐边一致性或明确记录未一致部分；对 456 个跨家庭别名及 58 个孤立节点作处理约束。
2. 干预发生在基线与末次之间，对受处理人员有立即反应 `proref2`、对其他受访者只有 `proref1`；必须明示如何形成预测初态，不能让末次结果泄漏入网络/拟合参数。
3. DeGroot/FJ/HK 必须事先规定同一网络 W、更新步数、参数范围、共同时间冲击/漂移对照、预先固定的整村留出折，不能从观察到的模型误差反向修改。
4. 原作者网络数据的可用性属于 **E2 来源证据**；三模型在人群中的有效性、因果识别、独立其他国家队列依然 **OPEN**。本次没得到任何三模型实证预测排行榜。

下一阶段结束后，应按照 [统一验收标准](../../protocols/RESEARCH_ACCEPTANCE_STANDARD_V1_2026-10-16.md)及时完成有限范围 R066 研究包，避免把一项 R 编号无限扩大；继续引入其它群体、制度和文化演化模型。

`R066_REAL_SOURCE_INTEGRITY=PASS`
`R066_SOURCE_66_FIELD_INDEX=PASS`
`R066_NAIVE_EGO_JOIN=FAIL_CLOSED`
`R066_AUTHOR_ALGORITHM_DERIVED_HOUSEHOLD_NETWORK=PASS_BOUNDED`
`R066_AUTHOR_R_IGRAPH_EDGE_PARITY=OPEN`
`R066_REAL_THREE_MODEL_HELDOUT=OPEN`
`R066_EXTERNAL_E3=OPEN`
`PESEN_v0.1=FROZEN`
