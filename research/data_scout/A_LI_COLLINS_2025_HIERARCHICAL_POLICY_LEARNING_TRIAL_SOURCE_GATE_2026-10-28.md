# A轨 Li 与 Collins 人类层级策略学习逐试次数据资格审计

日期：2026年10月28日。状态：PUBLIC_CODE_AND_SCHEMA_VERIFIED / ORIGINAL_TRIAL_ROWS_NOT_READ / LICENSE_UNCONFIRMED / E2_READY=NO。

一手来源：Jing-Jing Li 与 Anne G. E. Collins，*An algorithmic account for how humans efficiently learn, transfer, and compose hierarchically structured decision policies*，Cognition 254 (2025), 105967。原作者公开仓库 https://github.com/jl3676/learning_hierarchy ，main commit `85e637a07cdb0a28d0c0777b22c337e73fcf25fd`（2024年11月22日）。公开 README blob `572dfdc36bddb553cabca613956e7aa89a7bcb6d`。官方文件清单核实：`data.csv` 23,441,134 bytes，Git blob `6b5dd7c32b826b10c2be4c008fb552b0ab426957`；`data.pkl` 77,532,451 bytes，blob `3e009120fc4b0ea76e43e2aa262fbfd96b7e0ef1`。有建模、拟合及质量控制代码。

README声明两项人类实验，数据按 `participant`、唯一 `id`、`experiment`、`condition`、`block`、`trial` 组织，另含阶段1与阶段2的刺激 `s1/s2`、动作序列 `a1/a2`、奖励序列 `r1/r2` 及按键次数。block 1到12，试次编号每区块重置；原始任务中第1、2区块有表现依赖的提前结束或缺失，第3至12区块各有32个试次。CSV中动作及奖励可为以分号连接的多次尝试序列，必须按真实行为顺序展开，不能把一个CSV单元当作单次选择。原作者指出两项实验的任务版本和条件不同，未来复现需按人和实验分层、避免跨任务泄漏。

实际核验层次：通过GitHub连接器读取官方 README、仓库文件清单及Git blob身份，确认结构说明与文件可公开访问的元数据。此次未下载23.4MB完整CSV或77.5MB原始pickle，故没有实际逐行确认参与者数量、有效试次、动作时间、缺失率、唯一身份与独立性。未见GitHub仓库根目录 LICENSE，GitHub API license 字段为 null，无法确认原始数据再分发许可。原始行为记录可获取性仍需无付费条件下的分块读取或下载检验。此处禁止从文档字段推断已经完成数据验证。

适用性：候选适合学习、策略迁移、纵向任务内动态及层级认知模型的E2独立验证准备。它没有人类对手的双人重复囚徒困境结构，R073冻结直接评分资格=NO。不能因其为真实人类数据而将其自动升级为R231的心理量表CFA实证检验。来源不与既有R073、R074、R095实验混合。下一步需先确认许可，安全获取公开CSV，逐行核验身份、试次、动作奖励编码、阶段边界、独立被试，再预冻结适配任务的模型与样本外划分。当前新增真人E2评分=0，历史E3=0，无任何个人级数据入库。

本轮没有付费下载、账户注册或原始参与者数据复制。研究数据源只使用英文一手公开仓库。
