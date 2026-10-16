# R071 E2 候选：Dryad 随机惩罚噪音真人公共物品数据字节与测量适用性门

日期 2026-10-16。**在首次下载该候选原始 CSV、计算任何真实人类数据统计之前冻结本协议**。本阶段只做原件可达性、匿名结构审计和能否符合 R071 模型测量的诊断，不进行一条真实数据的个人策略分类或拟合。

第三方来源：
- Smerlak, Salahshour & Oberhauser (2022), *The cost of noise: Stochastic punishment falls short of sustaining cooperation in social dilemma experiments*，PLOS ONE DOI `10.1371/journal.pone.0263028`。
- 官方 Dryad 数据库 DOI [10.5061/dryad.n02v6wx03](https://doi.org/10.5061/dryad.n02v6wx03)，发布时间 **2022-01-26**。数据发布页列出 `noisy-PGG.csv`（约 1.30MB）与 `README-noisy-PGG.pdf`。链接 `https://datadryad.org/downloads/file_stream/1283295` 是发布页实际按钮展开的文件地址，**尚未取得任何字节也未声称 SHA 校验成功**。
- 作者公开描述 **384 人、96 个四人小组**完成，剔除存在频繁不回答的小组后**分析 320 人、80 个小组**：control 21、low noise 20、medium noise 20、high noise 19。上述数字属于论文/发布页元数据，**不是**本项目复核出来的真实 CSV 计数。官网显示实验用 oTree 于 2021年3–7月招募；不是2026年实时事件。
- Dryad 平台通用复用页文字不自动赋予本项目转发带标识的原始参与者行的授权。**此轮只向 GitHub 写来源哈希、总行数、公开列名和匿名字段分类，不上传或复制原始个体数据；如有明确许可证才另行确认。**

## 研究设计与字节门

从发布页链接直接取 CSV，HTTP 30 秒超时、≤4 MiB 原始字节、严格 UTF-8-sig decode、≤100000 行且≤120列，CSV 方言使用标准库 csv.reader 自动按逗号解析。必需非空 header，列名互异，任何重复或空标题/行字段数漂移 FAIL_CLOSED。计算**首次**实际 SHA256、字节数、完整数据行数、非空字段数及公开 schema 的列名；不得输出原始数据行、user_id、group_id、country、person-level response vector、唯一标识字段的 distinct values。

为检验是否有贡献、惩罚、群体、处理与时序五类测量，在**列名**做严格大小写忽略的语义关键词检索，匹配 `contrib, invest, punish, fine, group, treat, noise, round, period, player, participant`；这只能给出 `CANDIDATE_COLUMN_NAME_PRESENT`，**不能**宣称数值经过作者 README/文献解释。保留原始 header 以便随后**仅参照论文元数据**人工解释，不做模型拟合。

如果 HTTP 403/数据受限、错误 MIME、下载不足、超限、schema 不可用，则状态 `SOURCE_UNRESOLVED`，失败工作流不能凭发表页面上的“数据 1.30MB”冒充已实读 CSV。若成功最高状态 `E2_REAL_DRYAD_SOURCE_AND_SCHEMA_CANDIDATE_PASS`；E2 真实机制参数依然 `BLOCKED_MODEL_CONTRACT`：作者四人实验、随机惩罚错误和可能连续贡献/惩罚量与 R071 固定**五人、二元贡献、固定 P 职责、三种确定性制度**不同；未复现个体规范、初始信念、目标处罚。除非单独协议对齐全部字段、去泄漏切分、四人数据重新定义相容数学模型，否则不能拿该数据直接填进 R071 的 672 组模拟。

## 执行与存档

至少 8 项纯 CSV 安全/边界测试，实际 GitHub Actions 访问官方原件、只上传匿名 JSON；原始失败/数据变更另单独归档；无真实原始文件进入 Git history。R047 与 R067 已确认的真实 R047 公共资源提取四人数据（Git blob `73c02176bc9e060af987149594a85f9f7b591230`）亦不是这份公共物品贡献/有罚款目标/固定五人机制的精确等价合同。R071 E2 不得因旧项目 E2 来源完整就自动升级。

`R071_E2_DRYAD_FIRST_BYTE_GATE=FROZEN`；
`R071_FULL_HUMAN_MODEL_CALIBRATION=NOT_AUTHORIZED`；
`PESEN_v0.1=FROZEN`。
