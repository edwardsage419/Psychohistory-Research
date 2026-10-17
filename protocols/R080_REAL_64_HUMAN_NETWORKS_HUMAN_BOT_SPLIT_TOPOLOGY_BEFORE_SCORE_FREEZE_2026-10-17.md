# R080 Phase B：原作者64组动态人机混合网络——全字节校验、真人行为与边变化的结果前冻结协议

**2026-10-17；在R080任何真人30轮网络合作率或网络边变化数值被本项目计算之前提交。** 先前Phase A的来源元数据和仅结构审计已经阅读；R077/079真实结果亦已知道。Phase B是**已发表2020年原作者资料的新的回顾性真实群体 E2 描述验证**，不是从2020年实验开始前预注册的效果评估，不证明有已识别的社会网络因果干预，绝不升级PESEN v0.1。

## 0. 当前真实无行为结果来源证据

论文 Hirokazu Shirado & Nicholas A. Christakis (2020), *Network Engineering Using Autonomous Agents Increases Cooperation in Human Groups*, *iScience* 23(9),101438 DOI `10.1016/j.isci.2020.101438`。作者Mendeley Data v1 `Bot Cooperation Experiment Dataset` DOI `10.17632/t963ktp6ft.1`，[官方页面](https://data.mendeley.com/datasets/t963ktp6ft/1)，CC BY 4.0。Phase A 已经成功核验无令牌官方 `https://data.mendeley.com/public-api/datasets/t963ktp6ft`，元数据v1 DOI一致，原清单**70个文件（64个实验JSON、3个原始R、3个CSV）**；官方每个文件都自带SHA256及签名文件下载地址，3份R和多个不同文件夹的真人网络JSON都实际下载且核对发布方原文件SHA256。官方通用`download.zip`地址返回非ZIP，**必须保留该失败，不得宣称整个ZIP已下载**；使用逐个官方文件下载并SHA严格验证方属有效原始资料恢复。

[原始代码/JSON schema无真人评分核验 GitHub Actions 38997937026](https://github.com/edwardsage419/Psychohistory-Research/actions/runs/38997937026)：JSON顶层`game_id,treatment,players,result_behaviors,result_networks`及固定收益参数；`players`是 `{player,is_bot}`，`result_behaviors`是30轮记录`{round,cooperation:[{player,action}],rewiring:[{sender,receiver,action}]}`，`result_networks`是31个快照`{round,network:{directed,multigraph,nodes:[{id}],links:[{source,target}]}}`。作者R分析明确以`cooperation=="C"`为1，否则为0，代码预列`no_bots,allc_bots,tft_bots,random_mgmt_bots,engaged_mgmt_bots,disengaged_mgmt_bots,disengaged_mgmt_visible_bots,single_mgmt_bot`八个处理的统计表述（最终以真实字段一致性为准）。两组文件夹分别56与8原始JSON，但仅据文件夹数量**不得在源文件未核对时推断任何一组的分配/效应**。

## 1. 原始数据强制资格与完整人/机器识别

唯一来源即Mendeley v1官方返回的全部64 JSON **而非仅样本JSON**。必须验证：

- 官方snapshot精确 `version=1` 和永久DOI `10.17632/t963ktp6ft.1`；70原文件数量、3R/3CSV/64JSON数量无变化；每个被读取的64 JSON需尺寸与其官方记录一致并与`content_details.sha256_hash`逐字节通过。禁止将个人JSON或原始网络边、完整ID、签名URL写进Git。
- 每一个JSON对应一个不同 `game_id`（只留内部，不发表）；64个独立原作者网络，不重复；每个`players`自身有唯一的`player`ID且`is_bot`为布尔；必须从**实际JSON而非论文声明**重新数出 `exactly 16 human nodes per original network, hence 64×16=1024 original experiment human slots`。若源结构不符合，则立即FAIL CLOSED且不上报任何筛选后的“成功样本”。
- 一个JSON有30个行为round（每项都具有`round,cooperation,rewiring`）和31个`result_networks`状态，round索引在自身对应集合中不重复。**不提前假定两类round数字应为0或1**，仅将作者给出的原始序列按其JSON列表次序视为原始行为第1..30位及网络快照第0..30位，若原始回合字段不严格递增，则FAIL。
- 每条已实现合作动作必须引用该网络真实`players`中的唯一参与者ID，且`action`只可为`"C"`或`"D"`（样本R明确 C=合作；缺失、不属于此字母时FAIL并明确记录，不可猜测）。同一行为round某人最多一条；**不要将机器人动作计入人类分子或人类分母**。允许某人某回合没有可观察动作，但每网络每正式回合至少一条实际真人C/D记录，记每网络真实人行动覆盖量和缺失人数匿名汇总；缺失绝不以D代替/插补。没有真人记录的网络round则本轮强制FAIL不计算任何结果。
- 每个网络快照的`network.nodes`要与这份JSON的`players`全集完全一致，`links`两个端点都属于这一同图节点集，不能有自环、同轮重复无向边（真实源码为 `directed=false,multigraph=false`；不符合则FAIL）且每条边依`players.is_bot`精确分类为 HH、HB 或 BB。特别不能把HB/BB边误标为人类互惠；行为`rewiring`事件只在source结构门核验发送者/接收者是否属于真实节点，**不拿事件自述动作冒充实际已经变动的网络边**；真实边变化只通过相邻两份网络快照无向边集合对称差来计算。
- 对`treatment`值，先检查精确属于作者三R文件列出的8处理并每原作者网络不改变标签，然后每处理应为8个原始独立网络、共64个网络；不成立就FAIL或在实际数值出现之前新冻真实来源结构修订协议。对原作者数据发布的实际样本与研究题目人类1024/64验证不得混用bot身份或试验2与试验1作为同一干预。

## 2. 唯一主要 E2 观察结果

七模型、R073条件学习概率、R078人工 q0/q1 都不得在本轮使用/拟合；不做任何目标机器学习。

- **人类合作率**：对64个原始网络分别，逐30回合统计 `C_network,t = (#observed human actions=="C")/(#observed human actions in {"C","D"})`。一网络内的第一、最后一个原始行为round分别 `C_first,C_last`；`delta=C_last-C_first`。对各处理8个独立网络分别等权算术平均，并对全部64个原始网络等权算术平均。`first/last`仅为作者实验30轮的首末，不是为拟合预先选择的最佳时期；机器人完全排除。
- **短程演化描述**：对每个网络逐轮计算实际观测人合作率，第1–15与第16–30两段分别等权均值，公布`late_minus_early`按网络再网络等权汇总。不能由此声称跨社会世代演化。
- **拓扑变化**：`result_networks`第一和最后快照分别统计全部真实边数、HH/HB/BB边数；对30个相邻快照集合，逐步`added=|E_next−E_prev|`, `removed=|E_prev−E_next|`，在每网络计算总体30步 added 与 removed；按处理及64个网络等权汇总，同时报告网络边分类三类的总量。对跨不同处理，人类和机器节点总数不同，要提示绝对边数不具直接可比意义；可以报告每网络 HH/HH可能边的密度，但无任何实际人类网络干预因果结论。
- **配对可比较性**：发布每一处理的原始网络数、每网络真人固定16的事实、机器人节点数均值及最小最大、真人行为完整程度、30×64网络round完整性；不发布具体 `game_id`、参与者编号、原始网络边、原始事件或每个网络的单独合作率。
- **主要负例**：每处理报告最后相对首次真人合作 `delta>0,=0,<0` 的**网络数量**，即便某些bot处理呈负值也不删除。跨处理只报告描述性mean，不进行p值/协方差调整、不产生可以解释为bot因果效果的新统计显著性论证；原作者论文已报告“某处理60.4%到79.4%”，是历史文献已知数，不能作为本轮真计算替身。

## 3. 实施、防篡改、退出

**协议先于真实64网络评分**提交，代码只允许在64个原作者sha校验、64×16 human身份证据、全30行为轮、31网络快照、所有动作和双向图边完整规则全部满足时才输出成功E2。至少32项**全合成**人机区分、序列、回合、网络边与伦理隔离合约测试必须先PASS；失败优先、不会筛掉坏网络后改分母；然后在GitHub Actions真实重新下载全部原始64文件，输出匿名总表/八类处理macro，并再次独立运行逐字节复现及永久Git SHA归档。若所有官方文件SHA齐全，独立重放需两次输出字节一致。禁在Git存任何原始人类source行/ID/网络微观轨迹或下载时效签名URL。

真正严格的因果估计需要原作者实验分配/真人招募/网内干扰单位和处理强度的独立核验，**本轮止于可复现E2人机时变网络的描述，不可说真人之间相互感染/AI因果导致增益**。同理R079两人组方差（y=0/0.5/1）不可与本轮64真人网络的二元合作比例直接比较，更不等于长时期历史演化。

`R080_PHASE_B_REAL_NETWORK_SCORE_PROTOCOL=FROZEN_BEFORE_SCORES`  
`R080_ORIGINAL_DATA_VERSION=MENDELEY_V1`  
`R080_SOURCE_SHA256_STRICT=EACH_OF_64_JSON`  
`R080_HUMAN_ONLY_RATE_BOTS_EXCLUDED=YES`  
`R080_REAL_GROUP_CAUSAL_EFFECT=NOT_IDENTIFIED`  
`PESEN_v0.1=FROZEN`
