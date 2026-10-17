# R080：Shirado/Christakis（2020）64真实网络人机混合资料——原始来源访问和实体语义资格门冻结

**日期：2026-10-17；Phase A `ORIGINAL_SOURCE_ACCESS_AND_HUMAN_BOT_ENTITY_GATE`。** 在 R080 任何网络群体数值统计、组内方差、模型拟合、因果对比出现之前冻结本协议。前面 R077 的第四个真人重复博弈零样本预测与 R079 的真实双人动态网络 E2 描述已经看过；本轮既不以这些已知结果筛选新的赢家，也不声称实验开始前的前瞻性注册。

## 必须严守的原作者来源

Hirokazu Shirado & Nicholas A. Christakis (2020), “Network Engineering Using Autonomous Agents Increases Cooperation in Human Groups”, *iScience* 23(9):101438 DOI `10.1016/j.isci.2020.101438`，公开数据由 **Hirokazu Shirado 本人**上传的 [Mendeley Data `Bot Cooperation Experiment Dataset`](https://data.mendeley.com/datasets/t963ktp6ft/1) ，永久 DOI `10.17632/t963ktp6ft.1`，**版本 v1**、2020-07-21、CC BY 4.0。原作者论文报告总共1024人类参与者分布于64个实验网络，但该**论文本身的总量不是我们已经实读/逐字节校验的研究数据库**，不可直接变为R080实际样本分母。

官方说明 `data/raw` 为每场实验 **JSON**，`exp1` 为6种 bot treatment + bot visible treatment；`exp2` 为单个网络工程bot、5条边的补充实验，`code`为R分析。**不得合并 exp1 与 exp2 的不同真实实验分配，也不可把机器人节点/机器人决策计为真人**；禁止将论文报告的1024名和64网络直接视为某个 exp1 子实验的分母。对每项真人、机器人、网络和阶段字段，以完整官方原始JSON及作者原分析R脚本核验为唯一依据。

## Phase A 策略与停止规则（无真人性能数值）

1. 探查无须令牌的官方Mendeley v1公开页面、API与ZIP下载接口，严格限制HTTP超时、最大metadata体积及重定向，记录HTTP状态、是否读到官方版本ID、摘要性文件数量/大小/扩展名；禁止打印个人行为JSON片段、文件内容、临时下载令牌、任何签名URL。潜在开放接口仅为假设，不能宣称已成功。
2. 若官方可公开列出文件，逐项确认真实官方`data/raw` JSON 和作者分析`code` R文件是否存在，保留**官方给出的文件内容摘要或SHA256**；**无官方HASH时也可首次下载后固定我们自己获取的SHA256，但须明确是研究方观测的固定字节，不冒充作者预先公布。**
3. 在人类行为网络统计前必须检验：`exp1/exp2` 来源区分、跨网络单元不可串号、`human`与`bot`实体类别、原始真人与机器人行动的独立计数、互动边的真实时序与双方边规则、基线及终局轮次定义、各网络独立单位和源代码语义。未核实则 `R080_REAL_NETWORK_E2=OPEN`，不能用论文汇总充数。
4. 数据许可是CC BY 4.0，仍不把原始人类个人ID或时间行动轨迹写进我们Git。官方原始资料可以留存在临时GitHub Actions runner被读取审计，永久仓库只存来源SHA、代码和不泄漏个人的汇总。
5. 如果Mendeley网络访问失败或文件不公开，则`SOURCE_ACCESS_BLOCKED`、网络E2 OPEN，保留有界来源审计负结果；可检索同一原作者 GitHub/Dryad/Zenodo 官方镜像，但不可捏造文件。
6. **Phase B 另行评分/检验前冻结**：若能获得完整原始资料，先确认真实人节点、机器节点、动态接线、组层指标，以及实验类型和权重，另提交真正的评分协议才可实跑有实数结论。不允许借论文“合作提升60.4%→79.4%”当成R080独立运行的计算结果。任何因果估计必须经独立分配/干扰/公开反馈证据审计，不能因bot共现和群体合作变化便称因果效应。

第一步只提交无需第三方凭据的公开资源访问/原始字节可达性程序、10项以上合成安全断言及远端GitHub Actions真实运行；无法读到source即如实失败归档。原始 R079双人E2 不可等价于这个多人固定网络。PESEN v0.1全程冻结。

`R080_FIRST_PUBLIC_METADATA_TEST=NOT_RUN_AT_FREEZE`  
`R080_MENDELEY_V1_ORIGINAL_HUMAN_BOT_NETWORK_BYTES=UNVERIFIED`  
`R080_ALL_HUMAN_NODES=UNVERIFIED`  
`R080_GENUINE_NETWORK_E2=OPEN`  
`R080_PHASE_A_METRICS=NONE`  
`PESEN_v0.1=FROZEN`
