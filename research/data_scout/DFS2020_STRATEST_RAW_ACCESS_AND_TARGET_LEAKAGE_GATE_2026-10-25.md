# A 数据侦察增量：DFS2020 的原始文件获取阻塞与目标变量泄漏门槛

日期：2026-10-25。前置登记：`research/data_scout/STRATEST_DF2011_FRD2012_DFS2020_PUBLIC_SOURCE_DEDUP_AND_SCHEMA_TRIAGE_2026-10-25.md`。本轮仅审查此前登记的 **Dvorak、Fischbacher、Schmelz 2020 三人社会影响实验**，避免将同一数据重复计数。主线 R143 独立计算优先，本记录为辅助子流程。

## 真实来源与固定版本

作者/CRAN 镜像 `cran/stratEst` 固定提交 `a6373b23d80dc816a63f18f973d372c9e8421914`，二进制 `data/DFS2020.rda` Git blob `8aa04408d48ceb504cde44e58c8bcad7f440ca3a`（1931字节），另有派生对象 `data/data.DFS2020.rda` Git blob `bad46f196c56d9dd2f78618ea3ee02380efd3963`（1997字节）。官方英文说明：https://search.r-project.org/CRAN/refmans/stratEst/html/DFS2020.html 及 https://search.r-project.org/CRAN/refmans/stratEst/html/data.DFS2020.html 。来源镜像：https://github.com/cran/stratEst/tree/a6373b23d80dc816a63f18f973d372c9e8421914/data 。

## 本轮新增的具体字段审计

官方说明的 `DFS2020` 为569行、7列：`id, game, period, others.choices, choice, intercept, conformity.score`。其派生 `data.DFS2020` 为569行、8列，额外 `input` 字段。官方文档明确指出 `input` 为 `choice` 的派生表示，反映当前回合是否偏离个人偏好。**若用派生 `input` 预测同一行的 `choice`，属于目标变量直接泄漏**。此为字段语义级审计；未读取569行实际值，不能宣称逐行恒等关系已复算。

`conformity.score` 来自实验后的问卷，不能无条件当作实验进行中的实时已知特征。 `others.choices` 是其他两名群体成员的选择是否符合本人的偏好，必须核查信息展示与决策先后，才可用于实时预测。 `game` 是游戏序号，**未提供独立 session 或完整对手身份字段**；`id` 仅为参与者标识。文档的 Usage 小节将 DFS2020 错写成 `data(DF2011)`，实际对象应按固定 Git 树中的名称核对，避免误加载 DF2011。

## 原始字节尝试与复现资格

实际尝试 GitHub 连接器直接读取上述二进制 Git blob，得到 `UnicodeDecodeError`（非 UTF8 压缩对象）。尝试公开 GitHub blob URL 的文本获取也被拒绝为非 UTF8。免费本地环境外部网络请求未解析域名，未取得原始 RData 字节；不使用付费 API、注册账户或访问私人数据。**本轮不能完成逐行字段、身份唯一性、期次一致性、群组/场次划分及实际许可再分发资格核验。**

项目适配判定：`SOURCE_METADATA_CONFIRMED_RAW_BINARY_BLOCKED`；`CURRENT_TARGET_INPUT_LEAKAGE_RISK_CONFIRMED_FROM_DOCUMENTATION`；`R073_FROZEN_BINARY_PAIR_PROTOCOL_INELIGIBLE`。三人从众任务不同于 R073 的双人重复囚徒困境，禁止重编码或调参强行适配。后续可在获得公开原始字节后使用免费 R 或开源读取器，先校验 Git blob/文件 SHA256、行数和字段，再核实 `id×game×period` 键及实验时序。新 E2 预测=0，E3=0。软件包 GPL-3 许可与人类数据再分发授权分开审查。
