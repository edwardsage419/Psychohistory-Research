# R080：64个原作者真实人机混合网络的完整合作与时变拓扑 E2 审计

**2026-10-17，结题范围：`CLOSED_BOUNDED`，证据级别 `E2_TRUE_FIRST_PARTY_HUMAN_BOT_NETWORKS_DESCRIPTIVE`。** 已永久归档原作者全部64个真实网络、每份官方SHA256原始JSON的统一合作率和30步网络拓扑指标，明确保留正负处理与初始来源资格FAIL；**不构成机器人策略因果影响的重新识别、不将实验30轮解释为历史演化，更不升级PESEN v0.1。**

## A01：研究问题与来源

R078的纯合成数学反例表明：单个人行为历史预测相同，不代表人际因果机制相同；R079以另一真人实验获得双人配对网络与随机重配对非因果数学参照。本次首次尝试使用**完整多人动态网络**的原作者实验资料，确认每个真实网络内哪些节点是人类、哪些是机器代理，以及短期人类合作与网络边连接如何同时变化。

原论文 Hirokazu Shirado & Nicholas A. Christakis (2020)，*Network Engineering Using Autonomous Agents Increases Cooperation in Human Groups*，*iScience* 23(9):101438，[论文DOI](https://doi.org/10.1016/j.isci.2020.101438)。作者Hirokazu Shirado独立发布 [Mendeley Data “Bot Cooperation Experiment Dataset” v1](https://data.mendeley.com/datasets/t963ktp6ft/1)，[数据 DOI `10.17632/t963ktp6ft.1`](https://doi.org/10.17632/t963ktp6ft.1)，2020-07-21，数据许可 **CC BY 4.0**。原文宣称1024名真人、64个实验网络，有涉及机器代理如何介入伙伴网络选择的随机化设计；**论文先前已公布其方向性结论**，R080只能独立重复原始数据计算，不可宣称2020实验前的预先注册或真正新收集人群E3。

## A02：从实际受阻到完整原作者原始字节

最初官方Mendeley新版页面能够浏览，但某些REST endpoints需认证。没有使用任何用户凭据或付费账号。通过[来源访问CI 38997492623](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38997492623)发现官方公开 `https://data.mendeley.com/public-api/datasets/t963ktp6ft` 能读取版本固定的v1元数据以及70份文件的官方 `content_details.sha256_hash` 与短期有效的下载地址。官方通用`/datasets/t963ktp6ft/1/files/download.zip`虽然HEAD返回200，GET却并非有效ZIP，[结构检查 CI 38997632125](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38997632125)准确给出 `R080_PUBLIC_DOWNLOAD_IS_NOT_VALID_ARCHIVE`；这一失败仍然保留。

绕过**失效的聚合下载接口**而非绕过文件完整性检验：[文件级 SHA/结构审计 CI 38997838267](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38997838267) 首次取得原作者数份R代码、原JSON，所有文件按**发布方自行登记的SHA256**精确验证；[作者代码/深层JSON语义核验 CI 38997937026](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38997937026)确认：

- `players=[{player,is_bot}]` 是原始每网络人物/机器身份；`result_behaviors`是30条真人/代理行为回合，含 `cooperation=[{player,action}]`、`rewiring`；`result_networks`是31个快照，含 `nodes=[{id}]`、`links=[{source,target}]`、图是否有向/允许多重边。
- 原作者R脚本按 `cooperation=="C"` 记录真人合作，正式数值评价须排除 `is_bot=True` 所有机器代理；因此不能把32个原始节点误当32个真人。
- 固定版本官方清单恰70份文件：**64原始网络JSON、3分析R脚本、3汇总CSV**。JSON分两个原作者目录（56/8），结果处理结构由每个JSON自己的`treatment`字段而非猜目录得到。

首个全网络数据门虽然实际取到64份SHA正确的原始JSON，但错误地强制 `network.nodes==players`：[真实全网络CI 38998214433](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38998214433)因此 `R080_NETWORK_SNAPSHOT_NODES_NOT_EQUAL_REAL_ACTORS` **FAIL CLOSED**，没有输出任何真人指标。随后在仍**未出现一项真实全网指标**时，[独立全部64个官方SHA来源的节点语义检查 CI 38998347906](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38998347906)确认：原始31×64快照里，某些**没有任何边的真人**不写入图节点列表，但机器人节点全部列出，没有任何陌生节点或边连向快照外节点，缺失真人总节点出现次数按处理有差异。此乃源图存储方式而非实验参与者被招募排除。正式冻结[**Rev-002 评分前修订协议**](../../protocols/R080_PRE_FIRST_REAL_NETWORK_METRICS_GRAPH_ISOLATE_AMENDMENT_REV002_2026-10-17.md)，提交 `f0b4dc6d206b0a4f036115b316cf46d76fbfd8fd`；只允许没有任一边的零度真人不出现在网络节点集合，**完全保留每个JSON原始完整16名真人及30轮行为风险集**。原始Rev-001持续留档并明确FAIL，绝不倒写为初始直接成功。

## A03：真实核验宇宙与冻结指标

64个原作者真人/机器人图全部按官方SHA256匹配，完整源指纹为 `555e2127ac21f4532c33a2e0a08f2e081b5f970891bd772c9bac3155d1d53571`（将64个官方原始SHA256排序后再做 SHA256）。真正的复原：

| 实际原始实验单位 | 数量与门槛 |
|---|---:|
| 独立原作者真实网络 | 64/64 |
| 每网络真人 `players.is_bot=false` | 16/16 |
| 全部原始网络内真人身份槽 | **1024** |
| 原始实验处理类别 | **8 × 8网络** |
| 30期人机原始行为状态 | **1920** |
| 31期真实网络图状态 | **1984** |
| 可能的真人行动槽 | 30,720 |
| 已真实观测的真人 C/D 行动槽 | **27,656（90.026%）** |
| 实际机器人分类和全部有效边两端身份核验 | PASS |
| 原始机器人间BB边（所有处理网络平均初、末） | 0 |

机器人节点数视处理而异：`no_bots`0；六种主要机器人处理（包括单独可见处理）各网络16；`single_mgmt_bot`网络的原始`is_bot`节点数是**5**。最后这一点与自然语言“single bot”标签间的实体层级（五个bot身份节点是否对应一个控制算法/五个触角）未经原作者开发文档独立验证；**数据结果只称为5个机器人标记节点**，不得直接断言单一算法实体等于五个人类或五个互不相关的自主智能。

### 冻结统计口径

只取 `action="C"` 为真人合作、`"D"` 为真人背叛；一回合 `human_coop_rate=#真人观测C/#真人观测(C,D)`，缺席的真人行为不强行按D补齐，也不将任何机器人行动计入。对每一个真实网络的第1与第30轮、前15与后15轮等权求值，再对处理内8个原始独立网络及全部64网络等权平均。网络快照只用原 `result_networks` 里的真实无向边，按`is_bot`严格拆HH、HB、BB，边增减由连续两快照真实边集合差确定；不会把`rewiring`请求等同于已经变更的边。缺失的零度人类节点对该时点边数贡献0，但仍保留在16名真人候选分母的身份集合中。

### 首末人类合作变化：八个真实来源处理全部呈报

| 原作者原始处理标签 | 独立网络 | 首轮真人合作 | 第30轮真人合作 | 变化（百分点） | 改善/持平/变差网络 |
|---|---:|---:|---:|---:|---|
| `no_bots` | 8 | 65.052% | 36.728% | **−28.324** | 1/0/7 |
| `allc_bots` | 8 | 65.625% | 31.004% | **−34.621** | 0/0/8 |
| `tft_bots` | 8 | 80.629% | 47.272% | **−33.357** | 0/0/8 |
| `random_mgmt_bots` | 8 | 67.188% | 68.124% | **+0.936** | 4/1/3 |
| `engaged_mgmt_bots` | 8 | 70.136% | 31.667% | **−38.470** | 0/0/8 |
| `disengaged_mgmt_bots` | 8 | 60.000% | 79.363% | **+19.363** | 6/0/2 |
| `disengaged_mgmt_visible_bots` | 8 | 68.464% | 85.781% | **+17.317** | 8/0/0 |
| `single_mgmt_bot` | 8 | 66.749% | 75.317% | **+8.568** | 6/0/2 |
| **64网络等权汇总** | **64** | **67.980%** | **56.907%** | **−11.073** | **25/1/38** |

**负结果不得删除**：即使是“网络干预”，`engaged_mgmt_bots`仍在8/8网络下降，`disengaged_mgmt_bots`亦有2场恶化。不能把最好的`disengaged`与基线的描述差直接当作全部机器人技术必然改善合作，更不能借跨处理结果在已观察真实数据后任意挑选“获胜规则”并升级PESEN。作者论文摘要报告的约 `60.4%→79.4%` 是某具体网络干预处理的文献结果；本次在`disengaged_mgmt_bots` 的8个源网络等权、排除机器人、仅真实C/D口径下算得 `60.0%→79.363%`，方向和量级接近，但基线相差0.4百分点；原文真实参与、行为完整性和可能不同权重尚需独立核查，不能宣称逐字重复论文所有图与表。

### 真实群体拓扑随实验轮次变化

| 64网络等权组级变量 | 第0原图快照 | 最后网络快照 |
|---|---:|---:|
| 每网平均HH真人-真人边 | 35.922 | 52.719 |
| 每网平均HB真人-机器人边 | 12.625 | 12.625 |
| 每网平均BB机器人-机器人边 | 0 | 0 |
| 每网平均全部实际连接边 | 48.547 | 65.344 |
| HH可能边密度（按16真人，120种无向对） | 0.29935 | 0.43932 |

在全部30个相邻快照的每网均值中，新增边`80.96875`，消失边`64.171875`，合计改变边`145.140625`，净增加`16.796875`；这属于**固定30轮、真实作者时变图的直接观察**。它没有测试“HH边增加造成真人合作增加”的因果作用：全网平均HH边增长而真人合作均值下降，已足以警告不可把静态更多边解释为必然更高合作率。不同处理具有不同机器人总数和实验安排，绝对连接数不宜用于未经设计证据的因果跨处理比较。

## A04：完整可审计的失败链与再运行

1. [通用ZIP结构资格CI 38997632125](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38997632125)：真正GET并非ZIP，但metadata与单文件有效，无任何人类真实分数。
2. [初版全64网络 CI 38998214433](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38998214433)：42项合成PASS，真实来源全64 SHA也已取得，但因网络图未列出零度真人节点，**没有任何真实合作率/图变化结果**；后经[源结构审计38998347906](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38998347906)独立核实，仅以 `Rev-002` 严格允许零度真人不出现，未改变任何真人配额、结果定义、范围或预设指标。
3. [CI 38998538237](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38998538237) 属Rev-002过程中的旧合成断言未同步，发生纯测试FAIL、真人作业未执行。随后新加必须“不容遗漏机器节点、不得编造陌生节点、确证真零度真人”的测试，**45项合成全PASS**；[第一次真实64网络 E2 CI 38998549613](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38998549613) 两job `success`，真实结果JSON `11,745 bytes`、SHA256 `7b7d231d97a98c4b08e7d3658fa8e943bacd60aef1d8529754cd1f75179b99c8`。
4. [第一次额外重下载CI 38998713165](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38998713165) 又出现一次原作者签名CDN文件返回字节与发布方SHA不符，按**严格真实来源门中止**且没有写入Git。后来仅增加**有限3次下载重试/刷新签名URL**（每一次仍必须是同一个v1原文件ID/文件名/大小/**相同官方SHA**，完整实验与所有科学算法不变）；重试并不接受任何不同原始字节，也不调整人类指标或排除“问题”网络。
5. [最终独立SHA重下载并和首次数值逐字节完全一致的CI 38998839902](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38998839902) success，将匿名官方64网络结果永久写到 [R080_FIRST_PARTY_64_HUMAN_NETWORKS_TOPOLOGY_E2_RESULTS.json](R080_FIRST_PARTY_64_HUMAN_NETWORKS_TOPOLOGY_E2_RESULTS.json)，SHA256 `7b7d231d97a98c4b08e7d3658fa8e943bacd60aef1d8529754cd1f75179b99c8`，Git blob `c7e9a3ed76302f6eb4878acb278818d1db91e3c0`。所有原始真实participant ID、逐轮真人历史、bot节点ID及网络边均未永久发布在我们仓库。

**证据守则**：A01–A06的“科学报告流程通过”绝不等于初版资格门/初次CDN重下载成功；失败和修订的时间顺序均可独立从上述GitHub Actions审核。

## A05：推断等级与四层心理史学的位置

- **个体层**：1024个实验人物身份槽、真实C/D行为、明确机器节点与欠缺约10%人类行为槽；但没有评估R073七模型对新群体的来源数值迁移，不能自称第五项独立E3个体预测复验；30轮相互依赖，不能当30720独立人类因果观测。
- **群体层**：在独立64个网络中直接实读`HH/HB/BB`身份边、网络时间变化及真人组级合作，说明跨尺度测量对象确实可取得；但没有识别社会感染、潜在共同组冲击和网络干预效果各自贡献，不证明R078人工组方差公式实际成立。
- **制度环境层**：八种原作者策略或网络展示条件确实存在，不保证在本项目计算代码中已重建原实验分配随机化、响应缺失机制、机器人算法和真人受试者在轮内看到什么；所以当前只报告各组结果描述和原作者原论文引用，不重新发布因果效应量。
- **历史演化层**：30轮实验是**短程群体过程**，没有真实制度更替、代际文化传播、人口迁移、政策实施或几十年历史条件样本外评估。绝不把“网络随30轮变化”宣称为长时段心理史学预测成功。

## A06：验收状态与后续

依据 [统一科学验收标准](../../protocols/RESEARCH_ACCEPTANCE_STANDARD_V1_2026-10-16.md)：
- **A01 PASS**：64组真实网络独立数据、8处理、完整30轮、机器人严格分离的有限问题边界；
- **A02 PASS**：一手Mendeley发布方DOI/v1、完整70文件清单、全部64原始JSON逐一官方SHA256一致、CC BY许可；无法用通用ZIP下载的负证据保留；
- **A03 PASS**：45项合成、64真实图/source字节、人类C/D标签、无向边源核验、完整第二次独立下载/精确结果SHA重放；
- **A04 PASS_WITH_NEGATIVE_RETAINED**：初版图节点不完整性FAIL、修订、一个过渡合成测试FAIL、第一次独立CDN SHA失败与八处理多个真实合作下降完整记录；
- **A05 PASS**：真人群体描述E2、预测E3、因果识别及历史模型等级严格分开；
- **A06 PASS**：本正式报告、数字匿名宏JSON、最终机读验收、README及主仓索引、GitHub最新提交可核对。

`R080=CLOSED_BOUNDED` 仅本项有界真实网络E2来源与描述验收完成；核心原创心理史学数学-计算社会机制的因果识别与未来历史预测仍 OPEN。后续独立研究可探索这些网络中的**外生配对/机器人部署分配核验、机器人5节点语义与离散失访过程**，先冻结识别方案并避开已有成绩择优，再做下一项R081。

`R080_OFFICIAL_DATASET_VERSION=1`  
`R080_ORIGINAL_SHA_VERIFIED=64/64`  
`R080_REAL_HUMAN_NETWORK_UNITS=64`  
`R080_REAL_HUMAN_SLOTS=1024`  
`R080_E2_HUMAN_END_MINUS_FIRST=-0.11073225819319567`  
`R080_REV001_NODE_EXACTNESS=FAIL_RETAINED`  
`R080_REV002_PRE_REAL_SCORES=FROZEN`  
`R080_SOURCE_CDN_FIRST_INDEPENDENT_REPLAY=FAILED_RETAINED`  
`R080_INDEPENDENT_ORIGINAL_SHA_REPLAY=SUCCESS`  
`R080_CAUSAL_EFFECT=NOT_IDENTIFIED`  
`PESEN_v0.1=FROZEN`
